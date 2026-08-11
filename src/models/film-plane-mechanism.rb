# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/generate_film_plane_mechanism_model.py — do not edit this .rb directly.
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

# ── Sketchfab metadata — sketchfab dict fill-only-if-blank; name/desc forced when requested ──
model.name = "TBS-001 Articulated Film Plane Model" if model.name.to_s.strip.empty?
model.description = "The configuration the photosensitive film plane is flush against one of the 20ft long-side walls of the container. This has a view-camera-style moveable film plane \u2014 a mechanism with four independently actuated corners." if model.description.to_s.strip.empty?
model.set_attribute("sketchfab", "model_title", "TBS-001 Articulated Film Plane Model") if model.get_attribute("sketchfab", "model_title").to_s.strip.empty?
model.set_attribute("sketchfab", "model_description", "The configuration the photosensitive film plane is flush against one of the 20ft long-side walls of the container. This has a view-camera-style moveable film plane \u2014 a mechanism with four independently actuated corners.") if model.get_attribute("sketchfab", "model_description").to_s.strip.empty?
model.set_attribute("sketchfab", "model_id", "572b4aaa2d394de1b8852160d7cdcfc3") if model.get_attribute("sketchfab", "model_id").to_s.strip.empty?
model.set_attribute("sketchfab", "model_tags", "sketchup") if model.get_attribute("sketchfab", "model_tags").to_s.strip.empty?

  model.layers.add("Corners") unless model.layers["Corners"]
  model.layers.add("Film Plane") unless model.layers["Film Plane"]
  model.layers.add("Pinhole") unless model.layers["Pinhole"]
  model.layers.add("Context") unless model.layers["Context"]
  model.layers.add("Movement") unless model.layers["Movement"]
  model.layers.add("Shell") unless model.layers["Shell"]
  model.layers.add("Plane Tilt") unless model.layers["Plane Tilt"]
  model.layers.add("Plane Swing") unless model.layers["Plane Swing"]
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
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail STUB (fixed, parks corner) flange BL 303
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) flange BL 303"
  face = grp.entities.add_face([131.mm,2090.mm,303.mm], [169.mm,2090.mm,303.mm], [169.mm,2362.mm,303.mm], [131.mm,2362.mm,303.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail STUB (fixed, parks corner) flange BL 232
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) flange BL 232"
  face = grp.entities.add_face([131.mm,2090.mm,232.mm], [169.mm,2090.mm,232.mm], [169.mm,2362.mm,232.mm], [131.mm,2362.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail STUB (fixed, parks corner) bottom-flange lip BL
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) bottom-flange lip BL"
  face = grp.entities.add_face([164.mm,2090.mm,237.mm], [169.mm,2090.mm,237.mm], [169.mm,2362.mm,237.mm], [164.mm,2362.mm,237.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail REMOVABLE (out for transport) web BL
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) web BL"
  face = grp.entities.add_face([131.mm,0.mm,232.mm], [136.mm,0.mm,232.mm], [136.mm,2090.mm,232.mm], [131.mm,2090.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.3
  grp.material = mat

  # U-rail REMOVABLE (out for transport) flange BL 303
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) flange BL 303"
  face = grp.entities.add_face([131.mm,0.mm,303.mm], [169.mm,0.mm,303.mm], [169.mm,2090.mm,303.mm], [131.mm,2090.mm,303.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.3
  grp.material = mat

  # U-rail REMOVABLE (out for transport) flange BL 232
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) flange BL 232"
  face = grp.entities.add_face([131.mm,0.mm,232.mm], [169.mm,0.mm,232.mm], [169.mm,2090.mm,232.mm], [131.mm,2090.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.3
  grp.material = mat

  # U-rail REMOVABLE (out for transport) bottom-flange lip BL
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) bottom-flange lip BL"
  face = grp.entities.add_face([164.mm,0.mm,237.mm], [169.mm,0.mm,237.mm], [169.mm,2090.mm,237.mm], [164.mm,2090.mm,237.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.3
  grp.material = mat

  # Welded bridge (welded to REMOVABLE, bears on stub, ON TOP) BL
  grp = ents.add_group
  grp.name = "Welded bridge (welded to REMOVABLE, bears on stub, ON TOP) BL"
  face = grp.entities.add_face([131.mm,2030.mm,308.mm], [169.mm,2030.mm,308.mm], [169.mm,2180.mm,308.mm], [131.mm,2180.mm,308.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Locating pin (bridge↔STUB, flush to inner-rail top) BL
  grp = ents.add_group
  grp.name = "Locating pin (bridge↔STUB, flush to inner-rail top) BL"
  ge = grp.entities
  circle = ge.add_circle([150.mm,2135.mm,303.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(17.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Bottom support bridge (STUB → beam underside) BL
  grp = ents.add_group
  grp.name = "Bottom support bridge (STUB → beam underside) BL"
  face = grp.entities.add_face([131.mm,2058.mm,220.mm], [169.mm,2058.mm,220.mm], [169.mm,2122.mm,220.mm], [131.mm,2122.mm,220.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Rail far flange (pivot post) BL
  grp = ents.add_group
  grp.name = "Rail far flange (pivot post) BL"
  face = grp.entities.add_face([95.mm,2350.mm,227.mm], [205.mm,2350.mm,227.mm], [205.mm,2362.mm,227.mm], [95.mm,2362.mm,227.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(86.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Pinhole-wall gusset/seat BL
  grp = ents.add_group
  grp.name = "Pinhole-wall gusset/seat BL"
  face = grp.entities.add_face([94.mm,0.mm,202.mm], [206.mm,0.mm,202.mm], [206.mm,45.mm,202.mm], [94.mm,45.mm,202.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(131.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Length splice (pinhole end, outboard web) BL
  grp = ents.add_group
  grp.name = "Length splice (pinhole end, outboard web) BL"
  face = grp.entities.add_face([119.mm,205.mm,232.mm], [131.mm,205.mm,232.mm], [131.mm,315.mm,232.mm], [119.mm,315.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal roller Ø32 (wide face) BL 2270
  grp = ents.add_group
  grp.name = "Acetal roller Ø32 (wide face) BL 2270"
  ge = grp.entities
  circle = ge.add_circle([140.mm,2270.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel axle Ø10 BL 2270
  grp = ents.add_group
  grp.name = "Wheel axle Ø10 BL 2270"
  ge = grp.entities
  circle = ge.add_circle([140.mm,2270.mm,253.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper roller Ø20 (anti-lift / anti-tip) BL 2270
  grp = ents.add_group
  grp.name = "Keeper roller Ø20 (anti-lift / anti-tip) BL 2270"
  ge = grp.entities
  circle = ge.add_circle([144.mm,2270.mm,293.mm], [1,0,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper axle Ø8 BL 2270
  grp = ents.add_group
  grp.name = "Keeper axle Ø8 BL 2270"
  ge = grp.entities
  circle = ge.add_circle([144.mm,2270.mm,293.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal roller Ø32 (wide face) BL 2310
  grp = ents.add_group
  grp.name = "Acetal roller Ø32 (wide face) BL 2310"
  ge = grp.entities
  circle = ge.add_circle([140.mm,2310.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel axle Ø10 BL 2310
  grp = ents.add_group
  grp.name = "Wheel axle Ø10 BL 2310"
  ge = grp.entities
  circle = ge.add_circle([140.mm,2310.mm,253.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper roller Ø20 (anti-lift / anti-tip) BL 2310
  grp = ents.add_group
  grp.name = "Keeper roller Ø20 (anti-lift / anti-tip) BL 2310"
  ge = grp.entities
  circle = ge.add_circle([144.mm,2310.mm,293.mm], [1,0,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper axle Ø8 BL 2310
  grp = ents.add_group
  grp.name = "Keeper axle Ø8 BL 2310"
  ge = grp.entities
  circle = ge.add_circle([144.mm,2310.mm,293.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (bolted to skate axles) BL
  grp = ents.add_group
  grp.name = "Carriage plate (bolted to skate axles) BL"
  face = grp.entities.add_face([177.mm,2263.mm,154.mm], [191.mm,2263.mm,154.mm], [191.mm,2349.mm,154.mm], [177.mm,2349.mm,154.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(157.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) BL 2270
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) BL 2270"
  ge = grp.entities
  circle = ge.add_circle([183.mm,2270.mm,231.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) BL 2310
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) BL 2310"
  ge = grp.entities
  circle = ge.add_circle([183.mm,2310.mm,231.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake base (5128A63) BL
  grp = ents.add_group
  grp.name = "Cam-brake base (5128A63) BL"
  face = grp.entities.add_face([175.mm,2295.mm,311.mm], [185.mm,2295.mm,311.mm], [185.mm,2317.mm,311.mm], [175.mm,2317.mm,311.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Cam-brake base (5128A63) BL"] || model.materials.add("Cam-brake base (5128A63) BL")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake hold-down arm BL
  grp = ents.add_group
  grp.name = "Cam-brake hold-down arm BL"
  face = grp.entities.add_face([158.mm,2302.mm,312.mm], [180.mm,2302.mm,312.mm], [180.mm,2310.mm,312.mm], [158.mm,2310.mm,312.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Cam-brake base (5128A63) BL"] || model.materials.add("Cam-brake base (5128A63) BL")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake UHMW pad BL
  grp = ents.add_group
  grp.name = "Cam-brake UHMW pad BL"
  face = grp.entities.add_face([152.mm,2301.mm,308.mm], [164.mm,2301.mm,308.mm], [164.mm,2311.mm,308.mm], [152.mm,2311.mm,308.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Cam-brake UHMW pad BL"] || model.materials.add("Cam-brake UHMW pad BL")
  mat.color = Sketchup::Color.new(216, 212, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake lever BL
  grp = ents.add_group
  grp.name = "Cam-brake lever BL"
  ge = grp.entities
  circle = ge.add_circle([158.mm,2306.mm,312.mm], [0,0,1], 2.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Cam-brake base (5128A63) BL"] || model.materials.add("Cam-brake base (5128A63) BL")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z slide rail (TILT, green) BL
  grp = ents.add_group
  grp.name = "Vertical Z slide rail (TILT, green) BL"
  face = grp.entities.add_face([171.mm,2263.mm,140.mm], [181.mm,2263.mm,140.mm], [181.mm,2281.mm,140.mm], [171.mm,2281.mm,140.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(250.mm)
  mat = model.materials["Vertical Z cross-slide (TILT, green ~250) (Movement BL)"] || model.materials.add("Vertical Z cross-slide (TILT, green ~250) (Movement BL)")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X slide rail (SWING, purple) BL
  grp = ents.add_group
  grp.name = "Horizontal X slide rail (SWING, purple) BL"
  face = grp.entities.add_face([130.mm,2263.mm,142.mm], [390.mm,2263.mm,142.mm], [390.mm,2277.mm,142.mm], [130.mm,2277.mm,142.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X cross-slide (SWING, purple ~260) (Movement BL)"] || model.materials.add("Horizontal X cross-slide (SWING, purple ~260) (Movement BL)")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint (Belden UJ-SS750x375, setscrew) BL
  grp = ents.add_group
  grp.name = "U-joint (Belden UJ-SS750x375, setscrew) BL"
  face = grp.entities.add_face([138.mm,2258.mm,146.mm], [162.mm,2258.mm,146.mm], [162.mm,2282.mm,146.mm], [138.mm,2282.mm,146.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Input stub 3/8 (X slide → U-joint) BL
  grp = ents.add_group
  grp.name = "Input stub 3/8 (X slide → U-joint) BL"
  ge = grp.entities
  circle = ge.add_circle([155.mm,2270.mm,160.mm], [1,0,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(46.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 4040N12 304 shaft support (clamps input stub → X slide) BL
  grp = ents.add_group
  grp.name = "4040N12 304 shaft support (clamps input stub → X slide) BL"
  face = grp.entities.add_face([176.mm,2261.mm,149.mm], [199.mm,2261.mm,149.mm], [199.mm,2279.mm,149.mm], [176.mm,2279.mm,149.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Output stub 3/8 (U-joint → corner plate) BL
  grp = ents.add_group
  grp.name = "Output stub 3/8 (U-joint → corner plate) BL"
  ge = grp.entities
  circle = ge.add_circle([150.mm,2248.mm,160.mm], [0,1,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Corner plate 304 SS (U-joint mount — angle frame → U-joint) BL
  grp = ents.add_group
  grp.name = "Corner plate 304 SS (U-joint mount — angle frame → U-joint) BL"
  face = grp.entities.add_face([136.mm,2254.mm,165.mm], [170.mm,2254.mm,165.mm], [170.mm,2270.mm,165.mm], [136.mm,2270.mm,165.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
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
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) web BR
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) web BR"
  face = grp.entities.add_face([4638.mm,0.mm,232.mm], [4643.mm,0.mm,232.mm], [4643.mm,2362.mm,232.mm], [4638.mm,2362.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) flange BR 303
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) flange BR 303"
  face = grp.entities.add_face([4605.mm,0.mm,303.mm], [4643.mm,0.mm,303.mm], [4643.mm,2362.mm,303.mm], [4605.mm,2362.mm,303.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) flange BR 232
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) flange BR 232"
  face = grp.entities.add_face([4605.mm,0.mm,232.mm], [4643.mm,0.mm,232.mm], [4643.mm,2362.mm,232.mm], [4605.mm,2362.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) bottom-flange lip BR
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) bottom-flange lip BR"
  face = grp.entities.add_face([4605.mm,0.mm,237.mm], [4610.mm,0.mm,237.mm], [4610.mm,2362.mm,237.mm], [4605.mm,2362.mm,237.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Rail end flange (outboard-trimmed) BR 0
  grp = ents.add_group
  grp.name = "Rail end flange (outboard-trimmed) BR 0"
  face = grp.entities.add_face([4569.mm,0.mm,227.mm], [4644.mm,0.mm,227.mm], [4644.mm,12.mm,227.mm], [4569.mm,12.mm,227.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(86.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Rail end flange (outboard-trimmed) BR 2350
  grp = ents.add_group
  grp.name = "Rail end flange (outboard-trimmed) BR 2350"
  face = grp.entities.add_face([4569.mm,2350.mm,227.mm], [4644.mm,2350.mm,227.mm], [4644.mm,2362.mm,227.mm], [4569.mm,2362.mm,227.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(86.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal roller Ø32 (wide face) BR 2270
  grp = ents.add_group
  grp.name = "Acetal roller Ø32 (wide face) BR 2270"
  ge = grp.entities
  circle = ge.add_circle([4614.mm,2270.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel axle Ø10 BR 2270
  grp = ents.add_group
  grp.name = "Wheel axle Ø10 BR 2270"
  ge = grp.entities
  circle = ge.add_circle([4585.mm,2270.mm,253.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper roller Ø20 (anti-lift / anti-tip) BR 2270
  grp = ents.add_group
  grp.name = "Keeper roller Ø20 (anti-lift / anti-tip) BR 2270"
  ge = grp.entities
  circle = ge.add_circle([4618.mm,2270.mm,293.mm], [1,0,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper axle Ø8 BR 2270
  grp = ents.add_group
  grp.name = "Keeper axle Ø8 BR 2270"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2270.mm,293.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(37.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal roller Ø32 (wide face) BR 2310
  grp = ents.add_group
  grp.name = "Acetal roller Ø32 (wide face) BR 2310"
  ge = grp.entities
  circle = ge.add_circle([4614.mm,2310.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel axle Ø10 BR 2310
  grp = ents.add_group
  grp.name = "Wheel axle Ø10 BR 2310"
  ge = grp.entities
  circle = ge.add_circle([4585.mm,2310.mm,253.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper roller Ø20 (anti-lift / anti-tip) BR 2310
  grp = ents.add_group
  grp.name = "Keeper roller Ø20 (anti-lift / anti-tip) BR 2310"
  ge = grp.entities
  circle = ge.add_circle([4618.mm,2310.mm,293.mm], [1,0,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper axle Ø8 BR 2310
  grp = ents.add_group
  grp.name = "Keeper axle Ø8 BR 2310"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2310.mm,293.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(37.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (bolted to skate axles) BR
  grp = ents.add_group
  grp.name = "Carriage plate (bolted to skate axles) BR"
  face = grp.entities.add_face([4585.mm,2263.mm,154.mm], [4599.mm,2263.mm,154.mm], [4599.mm,2349.mm,154.mm], [4585.mm,2349.mm,154.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(157.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) BR 2270
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) BR 2270"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2270.mm,231.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) BR 2310
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) BR 2310"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2310.mm,231.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake base (5128A63) BR
  grp = ents.add_group
  grp.name = "Cam-brake base (5128A63) BR"
  face = grp.entities.add_face([4589.mm,2295.mm,311.mm], [4599.mm,2295.mm,311.mm], [4599.mm,2317.mm,311.mm], [4589.mm,2317.mm,311.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Cam-brake base (5128A63) BL"] || model.materials.add("Cam-brake base (5128A63) BL")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake hold-down arm BR
  grp = ents.add_group
  grp.name = "Cam-brake hold-down arm BR"
  face = grp.entities.add_face([4594.mm,2302.mm,312.mm], [4616.mm,2302.mm,312.mm], [4616.mm,2310.mm,312.mm], [4594.mm,2310.mm,312.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Cam-brake base (5128A63) BL"] || model.materials.add("Cam-brake base (5128A63) BL")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake UHMW pad BR
  grp = ents.add_group
  grp.name = "Cam-brake UHMW pad BR"
  face = grp.entities.add_face([4610.mm,2301.mm,308.mm], [4622.mm,2301.mm,308.mm], [4622.mm,2311.mm,308.mm], [4610.mm,2311.mm,308.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Cam-brake UHMW pad BL"] || model.materials.add("Cam-brake UHMW pad BL")
  mat.color = Sketchup::Color.new(216, 212, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake lever BR
  grp = ents.add_group
  grp.name = "Cam-brake lever BR"
  ge = grp.entities
  circle = ge.add_circle([4616.mm,2306.mm,312.mm], [0,0,1], 2.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Cam-brake base (5128A63) BL"] || model.materials.add("Cam-brake base (5128A63) BL")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z slide rail (TILT, green) BR
  grp = ents.add_group
  grp.name = "Vertical Z slide rail (TILT, green) BR"
  face = grp.entities.add_face([4593.mm,2263.mm,140.mm], [4603.mm,2263.mm,140.mm], [4603.mm,2281.mm,140.mm], [4593.mm,2281.mm,140.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(250.mm)
  mat = model.materials["Vertical Z cross-slide (TILT, green ~250) (Movement BL)"] || model.materials.add("Vertical Z cross-slide (TILT, green ~250) (Movement BL)")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X slide rail (SWING, purple) BR
  grp = ents.add_group
  grp.name = "Horizontal X slide rail (SWING, purple) BR"
  face = grp.entities.add_face([4384.mm,2263.mm,142.mm], [4644.mm,2263.mm,142.mm], [4644.mm,2277.mm,142.mm], [4384.mm,2277.mm,142.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X cross-slide (SWING, purple ~260) (Movement BL)"] || model.materials.add("Horizontal X cross-slide (SWING, purple ~260) (Movement BL)")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint (Belden UJ-SS750x375, setscrew) BR
  grp = ents.add_group
  grp.name = "U-joint (Belden UJ-SS750x375, setscrew) BR"
  face = grp.entities.add_face([4612.mm,2258.mm,146.mm], [4636.mm,2258.mm,146.mm], [4636.mm,2282.mm,146.mm], [4612.mm,2282.mm,146.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Input stub 3/8 (X slide → U-joint) BR
  grp = ents.add_group
  grp.name = "Input stub 3/8 (X slide → U-joint) BR"
  ge = grp.entities
  circle = ge.add_circle([4573.mm,2270.mm,160.mm], [1,0,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(46.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 4040N12 304 shaft support (clamps input stub → X slide) BR
  grp = ents.add_group
  grp.name = "4040N12 304 shaft support (clamps input stub → X slide) BR"
  face = grp.entities.add_face([4575.mm,2261.mm,149.mm], [4598.mm,2261.mm,149.mm], [4598.mm,2279.mm,149.mm], [4575.mm,2279.mm,149.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Output stub 3/8 (U-joint → corner plate) BR
  grp = ents.add_group
  grp.name = "Output stub 3/8 (U-joint → corner plate) BR"
  ge = grp.entities
  circle = ge.add_circle([4624.mm,2248.mm,160.mm], [0,1,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Corner plate 304 SS (U-joint mount — angle frame → U-joint) BR
  grp = ents.add_group
  grp.name = "Corner plate 304 SS (U-joint mount — angle frame → U-joint) BR"
  face = grp.entities.add_face([4604.mm,2254.mm,165.mm], [4638.mm,2254.mm,165.mm], [4638.mm,2270.mm,165.mm], [4604.mm,2270.mm,165.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
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
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail STUB (fixed, parks corner) web TL
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) web TL"
  face = grp.entities.add_face([131.mm,2090.mm,2262.mm], [136.mm,2090.mm,2262.mm], [136.mm,2362.mm,2262.mm], [131.mm,2362.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail STUB (fixed, parks corner) flange TL 2333
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) flange TL 2333"
  face = grp.entities.add_face([131.mm,2090.mm,2333.mm], [169.mm,2090.mm,2333.mm], [169.mm,2362.mm,2333.mm], [131.mm,2362.mm,2333.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail STUB (fixed, parks corner) flange TL 2262
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) flange TL 2262"
  face = grp.entities.add_face([131.mm,2090.mm,2262.mm], [169.mm,2090.mm,2262.mm], [169.mm,2362.mm,2262.mm], [131.mm,2362.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail STUB (fixed, parks corner) bottom-flange lip TL
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) bottom-flange lip TL"
  face = grp.entities.add_face([164.mm,2090.mm,2267.mm], [169.mm,2090.mm,2267.mm], [169.mm,2362.mm,2267.mm], [164.mm,2362.mm,2267.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail REMOVABLE (out for transport) web TL
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) web TL"
  face = grp.entities.add_face([131.mm,0.mm,2262.mm], [136.mm,0.mm,2262.mm], [136.mm,2090.mm,2262.mm], [131.mm,2090.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.3
  grp.material = mat

  # U-rail REMOVABLE (out for transport) flange TL 2333
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) flange TL 2333"
  face = grp.entities.add_face([131.mm,0.mm,2333.mm], [169.mm,0.mm,2333.mm], [169.mm,2090.mm,2333.mm], [131.mm,2090.mm,2333.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.3
  grp.material = mat

  # U-rail REMOVABLE (out for transport) flange TL 2262
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) flange TL 2262"
  face = grp.entities.add_face([131.mm,0.mm,2262.mm], [169.mm,0.mm,2262.mm], [169.mm,2090.mm,2262.mm], [131.mm,2090.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.3
  grp.material = mat

  # U-rail REMOVABLE (out for transport) bottom-flange lip TL
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) bottom-flange lip TL"
  face = grp.entities.add_face([164.mm,0.mm,2267.mm], [169.mm,0.mm,2267.mm], [169.mm,2090.mm,2267.mm], [164.mm,2090.mm,2267.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.3
  grp.material = mat

  # Welded bridge (welded to REMOVABLE, bears on stub, ON TOP) TL
  grp = ents.add_group
  grp.name = "Welded bridge (welded to REMOVABLE, bears on stub, ON TOP) TL"
  face = grp.entities.add_face([131.mm,2030.mm,2338.mm], [169.mm,2030.mm,2338.mm], [169.mm,2180.mm,2338.mm], [131.mm,2180.mm,2338.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Locating pin (bridge↔STUB, flush to inner-rail top) TL
  grp = ents.add_group
  grp.name = "Locating pin (bridge↔STUB, flush to inner-rail top) TL"
  ge = grp.entities
  circle = ge.add_circle([150.mm,2135.mm,2333.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(17.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Bottom support bridge (STUB → beam underside) TL
  grp = ents.add_group
  grp.name = "Bottom support bridge (STUB → beam underside) TL"
  face = grp.entities.add_face([131.mm,2058.mm,2250.mm], [169.mm,2058.mm,2250.mm], [169.mm,2122.mm,2250.mm], [131.mm,2122.mm,2250.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Rail far flange (pivot post) TL
  grp = ents.add_group
  grp.name = "Rail far flange (pivot post) TL"
  face = grp.entities.add_face([95.mm,2350.mm,2257.mm], [205.mm,2350.mm,2257.mm], [205.mm,2362.mm,2257.mm], [95.mm,2362.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(86.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Pinhole-wall gusset/seat TL
  grp = ents.add_group
  grp.name = "Pinhole-wall gusset/seat TL"
  face = grp.entities.add_face([94.mm,0.mm,2232.mm], [206.mm,0.mm,2232.mm], [206.mm,45.mm,2232.mm], [94.mm,45.mm,2232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(131.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Length splice (pinhole end, outboard web) TL
  grp = ents.add_group
  grp.name = "Length splice (pinhole end, outboard web) TL"
  face = grp.entities.add_face([119.mm,205.mm,2262.mm], [131.mm,205.mm,2262.mm], [131.mm,315.mm,2262.mm], [119.mm,315.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal roller Ø32 (wide face) TL 2270
  grp = ents.add_group
  grp.name = "Acetal roller Ø32 (wide face) TL 2270"
  ge = grp.entities
  circle = ge.add_circle([140.mm,2270.mm,2283.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel axle Ø10 TL 2270
  grp = ents.add_group
  grp.name = "Wheel axle Ø10 TL 2270"
  ge = grp.entities
  circle = ge.add_circle([140.mm,2270.mm,2283.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper roller Ø20 (anti-lift / anti-tip) TL 2270
  grp = ents.add_group
  grp.name = "Keeper roller Ø20 (anti-lift / anti-tip) TL 2270"
  ge = grp.entities
  circle = ge.add_circle([144.mm,2270.mm,2323.mm], [1,0,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper axle Ø8 TL 2270
  grp = ents.add_group
  grp.name = "Keeper axle Ø8 TL 2270"
  ge = grp.entities
  circle = ge.add_circle([144.mm,2270.mm,2323.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal roller Ø32 (wide face) TL 2310
  grp = ents.add_group
  grp.name = "Acetal roller Ø32 (wide face) TL 2310"
  ge = grp.entities
  circle = ge.add_circle([140.mm,2310.mm,2283.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel axle Ø10 TL 2310
  grp = ents.add_group
  grp.name = "Wheel axle Ø10 TL 2310"
  ge = grp.entities
  circle = ge.add_circle([140.mm,2310.mm,2283.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper roller Ø20 (anti-lift / anti-tip) TL 2310
  grp = ents.add_group
  grp.name = "Keeper roller Ø20 (anti-lift / anti-tip) TL 2310"
  ge = grp.entities
  circle = ge.add_circle([144.mm,2310.mm,2323.mm], [1,0,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper axle Ø8 TL 2310
  grp = ents.add_group
  grp.name = "Keeper axle Ø8 TL 2310"
  ge = grp.entities
  circle = ge.add_circle([144.mm,2310.mm,2323.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (bolted to skate axles) TL
  grp = ents.add_group
  grp.name = "Carriage plate (bolted to skate axles) TL"
  face = grp.entities.add_face([177.mm,2263.mm,2246.mm], [191.mm,2263.mm,2246.mm], [191.mm,2349.mm,2246.mm], [177.mm,2349.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(95.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) TL 2270
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) TL 2270"
  ge = grp.entities
  circle = ge.add_circle([183.mm,2270.mm,2261.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) TL 2310
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) TL 2310"
  ge = grp.entities
  circle = ge.add_circle([183.mm,2310.mm,2261.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake base (5128A63) TL
  grp = ents.add_group
  grp.name = "Cam-brake base (5128A63) TL"
  face = grp.entities.add_face([175.mm,2295.mm,2341.mm], [185.mm,2295.mm,2341.mm], [185.mm,2317.mm,2341.mm], [175.mm,2317.mm,2341.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Cam-brake base (5128A63) BL"] || model.materials.add("Cam-brake base (5128A63) BL")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake hold-down arm TL
  grp = ents.add_group
  grp.name = "Cam-brake hold-down arm TL"
  face = grp.entities.add_face([158.mm,2302.mm,2342.mm], [180.mm,2302.mm,2342.mm], [180.mm,2310.mm,2342.mm], [158.mm,2310.mm,2342.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Cam-brake base (5128A63) BL"] || model.materials.add("Cam-brake base (5128A63) BL")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake UHMW pad TL
  grp = ents.add_group
  grp.name = "Cam-brake UHMW pad TL"
  face = grp.entities.add_face([152.mm,2301.mm,2338.mm], [164.mm,2301.mm,2338.mm], [164.mm,2311.mm,2338.mm], [152.mm,2311.mm,2338.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Cam-brake UHMW pad BL"] || model.materials.add("Cam-brake UHMW pad BL")
  mat.color = Sketchup::Color.new(216, 212, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake lever TL
  grp = ents.add_group
  grp.name = "Cam-brake lever TL"
  ge = grp.entities
  circle = ge.add_circle([158.mm,2306.mm,2342.mm], [0,0,1], 2.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Cam-brake base (5128A63) BL"] || model.materials.add("Cam-brake base (5128A63) BL")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z slide rail (TILT, green) TL
  grp = ents.add_group
  grp.name = "Vertical Z slide rail (TILT, green) TL"
  face = grp.entities.add_face([163.mm,2263.mm,1998.mm], [173.mm,2263.mm,1998.mm], [173.mm,2281.mm,1998.mm], [163.mm,2281.mm,1998.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(250.mm)
  mat = model.materials["Vertical Z cross-slide (TILT, green ~250) (Movement BL)"] || model.materials.add("Vertical Z cross-slide (TILT, green ~250) (Movement BL)")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X slide rail (SWING, purple) TL
  grp = ents.add_group
  grp.name = "Horizontal X slide rail (SWING, purple) TL"
  face = grp.entities.add_face([130.mm,2263.mm,2256.mm], [390.mm,2263.mm,2256.mm], [390.mm,2277.mm,2256.mm], [130.mm,2277.mm,2256.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X cross-slide (SWING, purple ~260) (Movement BL)"] || model.materials.add("Horizontal X cross-slide (SWING, purple ~260) (Movement BL)")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint (Belden UJ-SS750x375, setscrew) TL
  grp = ents.add_group
  grp.name = "U-joint (Belden UJ-SS750x375, setscrew) TL"
  face = grp.entities.add_face([138.mm,2258.mm,2238.mm], [162.mm,2258.mm,2238.mm], [162.mm,2282.mm,2238.mm], [138.mm,2282.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Input stub 3/8 (X slide → U-joint) TL
  grp = ents.add_group
  grp.name = "Input stub 3/8 (X slide → U-joint) TL"
  ge = grp.entities
  circle = ge.add_circle([155.mm,2270.mm,2252.mm], [1,0,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(46.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 4040N12 304 shaft support (clamps input stub → X slide) TL
  grp = ents.add_group
  grp.name = "4040N12 304 shaft support (clamps input stub → X slide) TL"
  face = grp.entities.add_face([176.mm,2261.mm,2241.mm], [199.mm,2261.mm,2241.mm], [199.mm,2279.mm,2241.mm], [176.mm,2279.mm,2241.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Output stub 3/8 (U-joint → corner plate) TL
  grp = ents.add_group
  grp.name = "Output stub 3/8 (U-joint → corner plate) TL"
  ge = grp.entities
  circle = ge.add_circle([150.mm,2248.mm,2252.mm], [0,1,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Corner plate 304 SS (U-joint mount — angle frame → U-joint) TL
  grp = ents.add_group
  grp.name = "Corner plate 304 SS (U-joint mount — angle frame → U-joint) TL"
  face = grp.entities.add_face([136.mm,2254.mm,2207.mm], [170.mm,2254.mm,2207.mm], [170.mm,2270.mm,2207.mm], [136.mm,2270.mm,2207.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (angle frame → bracket) TL
  grp = ents.add_group
  grp.name = "Frame-corner bolt (angle frame → bracket) TL"
  ge = grp.entities
  circle = ge.add_circle([183.mm,2256.mm,2252.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) web TR
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) web TR"
  face = grp.entities.add_face([4638.mm,0.mm,2262.mm], [4643.mm,0.mm,2262.mm], [4643.mm,2362.mm,2262.mm], [4638.mm,2362.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) flange TR 2333
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) flange TR 2333"
  face = grp.entities.add_face([4605.mm,0.mm,2333.mm], [4643.mm,0.mm,2333.mm], [4643.mm,2362.mm,2333.mm], [4605.mm,2362.mm,2333.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) flange TR 2262
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) flange TR 2262"
  face = grp.entities.add_face([4605.mm,0.mm,2262.mm], [4643.mm,0.mm,2262.mm], [4643.mm,2362.mm,2262.mm], [4605.mm,2362.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) bottom-flange lip TR
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) bottom-flange lip TR"
  face = grp.entities.add_face([4605.mm,0.mm,2267.mm], [4610.mm,0.mm,2267.mm], [4610.mm,2362.mm,2267.mm], [4605.mm,2362.mm,2267.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Rail end flange (outboard-trimmed) TR 0
  grp = ents.add_group
  grp.name = "Rail end flange (outboard-trimmed) TR 0"
  face = grp.entities.add_face([4569.mm,0.mm,2257.mm], [4644.mm,0.mm,2257.mm], [4644.mm,12.mm,2257.mm], [4569.mm,12.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(86.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Rail end flange (outboard-trimmed) TR 2350
  grp = ents.add_group
  grp.name = "Rail end flange (outboard-trimmed) TR 2350"
  face = grp.entities.add_face([4569.mm,2350.mm,2257.mm], [4644.mm,2350.mm,2257.mm], [4644.mm,2362.mm,2257.mm], [4569.mm,2362.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(86.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal roller Ø32 (wide face) TR 2270
  grp = ents.add_group
  grp.name = "Acetal roller Ø32 (wide face) TR 2270"
  ge = grp.entities
  circle = ge.add_circle([4614.mm,2270.mm,2283.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel axle Ø10 TR 2270
  grp = ents.add_group
  grp.name = "Wheel axle Ø10 TR 2270"
  ge = grp.entities
  circle = ge.add_circle([4585.mm,2270.mm,2283.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper roller Ø20 (anti-lift / anti-tip) TR 2270
  grp = ents.add_group
  grp.name = "Keeper roller Ø20 (anti-lift / anti-tip) TR 2270"
  ge = grp.entities
  circle = ge.add_circle([4618.mm,2270.mm,2323.mm], [1,0,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper axle Ø8 TR 2270
  grp = ents.add_group
  grp.name = "Keeper axle Ø8 TR 2270"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2270.mm,2323.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(37.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal roller Ø32 (wide face) TR 2310
  grp = ents.add_group
  grp.name = "Acetal roller Ø32 (wide face) TR 2310"
  ge = grp.entities
  circle = ge.add_circle([4614.mm,2310.mm,2283.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel axle Ø10 TR 2310
  grp = ents.add_group
  grp.name = "Wheel axle Ø10 TR 2310"
  ge = grp.entities
  circle = ge.add_circle([4585.mm,2310.mm,2283.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper roller Ø20 (anti-lift / anti-tip) TR 2310
  grp = ents.add_group
  grp.name = "Keeper roller Ø20 (anti-lift / anti-tip) TR 2310"
  ge = grp.entities
  circle = ge.add_circle([4618.mm,2310.mm,2323.mm], [1,0,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper axle Ø8 TR 2310
  grp = ents.add_group
  grp.name = "Keeper axle Ø8 TR 2310"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2310.mm,2323.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(37.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (bolted to skate axles) TR
  grp = ents.add_group
  grp.name = "Carriage plate (bolted to skate axles) TR"
  face = grp.entities.add_face([4585.mm,2263.mm,2246.mm], [4599.mm,2263.mm,2246.mm], [4599.mm,2349.mm,2246.mm], [4585.mm,2349.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(95.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) TR 2270
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) TR 2270"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2270.mm,2261.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) TR 2310
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) TR 2310"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2310.mm,2261.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake base (5128A63) TR
  grp = ents.add_group
  grp.name = "Cam-brake base (5128A63) TR"
  face = grp.entities.add_face([4589.mm,2295.mm,2341.mm], [4599.mm,2295.mm,2341.mm], [4599.mm,2317.mm,2341.mm], [4589.mm,2317.mm,2341.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Cam-brake base (5128A63) BL"] || model.materials.add("Cam-brake base (5128A63) BL")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake hold-down arm TR
  grp = ents.add_group
  grp.name = "Cam-brake hold-down arm TR"
  face = grp.entities.add_face([4594.mm,2302.mm,2342.mm], [4616.mm,2302.mm,2342.mm], [4616.mm,2310.mm,2342.mm], [4594.mm,2310.mm,2342.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Cam-brake base (5128A63) BL"] || model.materials.add("Cam-brake base (5128A63) BL")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake UHMW pad TR
  grp = ents.add_group
  grp.name = "Cam-brake UHMW pad TR"
  face = grp.entities.add_face([4610.mm,2301.mm,2338.mm], [4622.mm,2301.mm,2338.mm], [4622.mm,2311.mm,2338.mm], [4610.mm,2311.mm,2338.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Cam-brake UHMW pad BL"] || model.materials.add("Cam-brake UHMW pad BL")
  mat.color = Sketchup::Color.new(216, 212, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake lever TR
  grp = ents.add_group
  grp.name = "Cam-brake lever TR"
  ge = grp.entities
  circle = ge.add_circle([4616.mm,2306.mm,2342.mm], [0,0,1], 2.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Cam-brake base (5128A63) BL"] || model.materials.add("Cam-brake base (5128A63) BL")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z slide rail (TILT, green) TR
  grp = ents.add_group
  grp.name = "Vertical Z slide rail (TILT, green) TR"
  face = grp.entities.add_face([4595.mm,2263.mm,1998.mm], [4605.mm,2263.mm,1998.mm], [4605.mm,2281.mm,1998.mm], [4595.mm,2281.mm,1998.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(250.mm)
  mat = model.materials["Vertical Z cross-slide (TILT, green ~250) (Movement BL)"] || model.materials.add("Vertical Z cross-slide (TILT, green ~250) (Movement BL)")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X slide rail (SWING, purple) TR
  grp = ents.add_group
  grp.name = "Horizontal X slide rail (SWING, purple) TR"
  face = grp.entities.add_face([4384.mm,2263.mm,2256.mm], [4644.mm,2263.mm,2256.mm], [4644.mm,2277.mm,2256.mm], [4384.mm,2277.mm,2256.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X cross-slide (SWING, purple ~260) (Movement BL)"] || model.materials.add("Horizontal X cross-slide (SWING, purple ~260) (Movement BL)")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint (Belden UJ-SS750x375, setscrew) TR
  grp = ents.add_group
  grp.name = "U-joint (Belden UJ-SS750x375, setscrew) TR"
  face = grp.entities.add_face([4612.mm,2258.mm,2238.mm], [4636.mm,2258.mm,2238.mm], [4636.mm,2282.mm,2238.mm], [4612.mm,2282.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Input stub 3/8 (X slide → U-joint) TR
  grp = ents.add_group
  grp.name = "Input stub 3/8 (X slide → U-joint) TR"
  ge = grp.entities
  circle = ge.add_circle([4573.mm,2270.mm,2252.mm], [1,0,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(46.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 4040N12 304 shaft support (clamps input stub → X slide) TR
  grp = ents.add_group
  grp.name = "4040N12 304 shaft support (clamps input stub → X slide) TR"
  face = grp.entities.add_face([4575.mm,2261.mm,2241.mm], [4598.mm,2261.mm,2241.mm], [4598.mm,2279.mm,2241.mm], [4575.mm,2279.mm,2241.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Output stub 3/8 (U-joint → corner plate) TR
  grp = ents.add_group
  grp.name = "Output stub 3/8 (U-joint → corner plate) TR"
  ge = grp.entities
  circle = ge.add_circle([4624.mm,2248.mm,2252.mm], [0,1,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Corner plate 304 SS (U-joint mount — angle frame → U-joint) TR
  grp = ents.add_group
  grp.name = "Corner plate 304 SS (U-joint mount — angle frame → U-joint) TR"
  face = grp.entities.add_face([4604.mm,2254.mm,2207.mm], [4638.mm,2254.mm,2207.mm], [4638.mm,2270.mm,2207.mm], [4604.mm,2270.mm,2207.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (angle frame → bracket) TR
  grp = ents.add_group
  grp.name = "Frame-corner bolt (angle frame → bracket) TR"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2256.mm,2252.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
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
  face.pushpull(2092.mm)
  mat = model.materials["Film-plane ACM backing (ghost)"] || model.materials.add("Film-plane ACM backing (ghost)")
  mat.color = Sketchup::Color.new(31, 59, 102)
  mat.alpha = 0.14
  grp.material = mat

  # Film frame 2x2 6061 Al angle — top (upstand / muslin spring clip)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 Al angle — top (upstand / muslin spring clip)"
  face = grp.entities.add_face([183.mm,2212.mm,2249.mm], [4591.mm,2212.mm,2249.mm], [4591.mm,2262.mm,2249.mm], [183.mm,2262.mm,2249.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 6061 Al angle — top (in-plane leg / ACM seat)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 Al angle — top (in-plane leg / ACM seat)"
  face = grp.entities.add_face([183.mm,2259.mm,2202.mm], [4591.mm,2259.mm,2202.mm], [4591.mm,2262.mm,2202.mm], [183.mm,2262.mm,2202.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 6061 Al angle — bottom (upstand / muslin spring clip)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 Al angle — bottom (upstand / muslin spring clip)"
  face = grp.entities.add_face([183.mm,2212.mm,160.mm], [4591.mm,2212.mm,160.mm], [4591.mm,2262.mm,160.mm], [183.mm,2262.mm,160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 6061 Al angle — bottom (in-plane leg / ACM seat)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 Al angle — bottom (in-plane leg / ACM seat)"
  face = grp.entities.add_face([183.mm,2259.mm,160.mm], [4591.mm,2259.mm,160.mm], [4591.mm,2262.mm,160.mm], [183.mm,2262.mm,160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 6061 Al angle — left (upstand / muslin spring clip)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 Al angle — left (upstand / muslin spring clip)"
  face = grp.entities.add_face([183.mm,2212.mm,160.mm], [186.mm,2212.mm,160.mm], [186.mm,2262.mm,160.mm], [183.mm,2262.mm,160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2092.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 6061 Al angle — left (in-plane leg / ACM seat)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 Al angle — left (in-plane leg / ACM seat)"
  face = grp.entities.add_face([183.mm,2259.mm,160.mm], [233.mm,2259.mm,160.mm], [233.mm,2262.mm,160.mm], [183.mm,2262.mm,160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2092.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 6061 Al angle — right (upstand / muslin spring clip)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 Al angle — right (upstand / muslin spring clip)"
  face = grp.entities.add_face([4588.mm,2212.mm,160.mm], [4591.mm,2212.mm,160.mm], [4591.mm,2262.mm,160.mm], [4588.mm,2262.mm,160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2092.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 6061 Al angle — right (in-plane leg / ACM seat)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 Al angle — right (in-plane leg / ACM seat)"
  face = grp.entities.add_face([4541.mm,2259.mm,160.mm], [4591.mm,2259.mm,160.mm], [4591.mm,2262.mm,160.mm], [4541.mm,2262.mm,160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2092.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Film Plane"
  inst.layer = model.layers["Film Plane"]

  # ═══ Pinhole ═══
  defn = model.definitions.add("Pinhole")
  ents = defn.entities
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
  ents.add_edges(Geom::Point3d.new(2399.mm, 0.mm, 1194.mm), Geom::Point3d.new(183.mm, 2262.mm, 2252.mm))
  ents.add_edges(Geom::Point3d.new(2399.mm, 0.mm, 1194.mm), Geom::Point3d.new(4591.mm, 2262.mm, 2252.mm))
  ents.add_edges(Geom::Point3d.new(2399.mm, 0.mm, 1194.mm), Geom::Point3d.new(183.mm, 2262.mm, 160.mm))
  ents.add_edges(Geom::Point3d.new(2399.mm, 0.mm, 1194.mm), Geom::Point3d.new(4591.mm, 2262.mm, 160.mm))

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Pinhole"
  inst.layer = model.layers["Pinhole"]

  # ═══ Context (walkway + IBC cantilever/beams) ═══
  defn = model.definitions.add("Context (walkway + IBC cantilever/beams)")
  ents = defn.entities
  # Walkway Near (fixed, bump integral)
  grp = ents.add_group
  grp.name = "Walkway Near (fixed, bump integral)"
  face = grp.entities.add_face([470.mm,8.mm,115.mm], [4329.mm,8.mm,115.mm], [4329.mm,300.mm,115.mm], [3083.mm,300.mm,115.mm], [3083.mm,500.mm,115.mm], [1055.mm,500.mm,115.mm], [1055.mm,300.mm,115.mm], [470.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (fixed, bump integral)"] || model.materials.add("Walkway Near (fixed, bump integral)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far
  grp = ents.add_group
  grp.name = "Walkway Far"
  face = grp.entities.add_face([470.mm,2062.mm,115.mm], [4329.mm,2062.mm,115.mm], [4329.mm,2354.mm,115.mm], [470.mm,2354.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (fixed, bump integral)"] || model.materials.add("Walkway Near (fixed, bump integral)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Right (IBC end)
  grp = ents.add_group
  grp.name = "Walkway Right (IBC end)"
  face = grp.entities.add_face([4329.mm,0.mm,115.mm], [4629.mm,0.mm,115.mm], [4629.mm,2362.mm,115.mm], [4329.mm,2362.mm,115.mm], [4329.mm,2062.mm,115.mm], [4429.mm,2062.mm,115.mm], [4429.mm,1912.mm,115.mm], [4329.mm,1912.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (fixed, bump integral)"] || model.materials.add("Walkway Near (fixed, bump integral)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Left (REMOVABLE — transport)
  grp = ents.add_group
  grp.name = "Walkway Left (REMOVABLE — transport)"
  face = grp.entities.add_face([170.mm,0.mm,115.mm], [170.mm,2362.mm,115.mm], [470.mm,2362.mm,115.mm], [470.mm,2062.mm,115.mm], [370.mm,2062.mm,115.mm], [370.mm,1912.mm,115.mm], [470.mm,1912.mm,115.mm], [470.mm,1560.mm,115.mm], [770.mm,1560.mm,115.mm], [770.mm,800.mm,115.mm], [470.mm,800.mm,115.mm], [470.mm,0.mm,115.mm])
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
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
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
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 1 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 gusset"
  ge = grp.entities
  f = ge.add_face([694.mm,8.mm,0.mm], [694.mm,8.mm,105.mm], [694.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) plate"
  face = grp.entities.add_face([1095.mm,0.mm,0.mm], [1215.mm,0.mm,0.mm], [1215.mm,10.mm,0.mm], [1095.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
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
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([1150.mm,10.mm,0.mm], [1150.mm,10.mm,103.mm], [1150.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) plate"
  face = grp.entities.add_face([1552.mm,0.mm,0.mm], [1672.mm,0.mm,0.mm], [1672.mm,10.mm,0.mm], [1552.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
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
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([1607.mm,10.mm,0.mm], [1607.mm,10.mm,103.mm], [1607.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) plate"
  face = grp.entities.add_face([2009.mm,0.mm,0.mm], [2129.mm,0.mm,0.mm], [2129.mm,10.mm,0.mm], [2009.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
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
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([2064.mm,10.mm,0.mm], [2064.mm,10.mm,103.mm], [2064.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) plate"
  face = grp.entities.add_face([2466.mm,0.mm,0.mm], [2586.mm,0.mm,0.mm], [2586.mm,10.mm,0.mm], [2466.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2491.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2561.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2491.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2561.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) arm"
  face = grp.entities.add_face([2521.mm,10.mm,103.mm], [2531.mm,10.mm,103.mm], [2531.mm,500.mm,103.mm], [2521.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([2521.mm,10.mm,0.mm], [2521.mm,10.mm,103.mm], [2521.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 (widened) plate"
  face = grp.entities.add_face([2923.mm,0.mm,0.mm], [3043.mm,0.mm,0.mm], [3043.mm,10.mm,0.mm], [2923.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2948.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3018.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2948.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3018.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 (widened) arm"
  face = grp.entities.add_face([2978.mm,10.mm,103.mm], [2988.mm,10.mm,103.mm], [2988.mm,500.mm,103.mm], [2978.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([2978.mm,10.mm,0.mm], [2978.mm,10.mm,103.mm], [2978.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 7 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 plate"
  face = grp.entities.add_face([3380.mm,0.mm,0.mm], [3500.mm,0.mm,0.mm], [3500.mm,8.mm,0.mm], [3380.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
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
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 7 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 gusset"
  ge = grp.entities
  f = ge.add_face([3436.mm,8.mm,0.mm], [3436.mm,8.mm,105.mm], [3436.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 8 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 plate"
  face = grp.entities.add_face([3837.mm,0.mm,0.mm], [3957.mm,0.mm,0.mm], [3957.mm,8.mm,0.mm], [3837.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
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
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 8 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 gusset"
  ge = grp.entities
  f = ge.add_face([3893.mm,8.mm,0.mm], [3893.mm,8.mm,105.mm], [3893.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 1 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 plate"
  face = grp.entities.add_face([638.mm,2354.mm,0.mm], [758.mm,2354.mm,0.mm], [758.mm,2362.mm,0.mm], [638.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
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
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 1 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 gusset"
  ge = grp.entities
  f = ge.add_face([694.mm,2354.mm,0.mm], [694.mm,2354.mm,105.mm], [694.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 2 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 plate"
  face = grp.entities.add_face([1095.mm,2354.mm,0.mm], [1215.mm,2354.mm,0.mm], [1215.mm,2362.mm,0.mm], [1095.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
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
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 2 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 gusset"
  ge = grp.entities
  f = ge.add_face([1151.mm,2354.mm,0.mm], [1151.mm,2354.mm,105.mm], [1151.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 3 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 plate"
  face = grp.entities.add_face([1552.mm,2354.mm,0.mm], [1672.mm,2354.mm,0.mm], [1672.mm,2362.mm,0.mm], [1552.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
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
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 3 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 gusset"
  ge = grp.entities
  f = ge.add_face([1608.mm,2354.mm,0.mm], [1608.mm,2354.mm,105.mm], [1608.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 4 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 plate"
  face = grp.entities.add_face([2009.mm,2354.mm,0.mm], [2129.mm,2354.mm,0.mm], [2129.mm,2362.mm,0.mm], [2009.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
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
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 4 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 gusset"
  ge = grp.entities
  f = ge.add_face([2065.mm,2354.mm,0.mm], [2065.mm,2354.mm,105.mm], [2065.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 5 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 plate"
  face = grp.entities.add_face([2466.mm,2354.mm,0.mm], [2586.mm,2354.mm,0.mm], [2586.mm,2362.mm,0.mm], [2466.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
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
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 5 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 gusset"
  ge = grp.entities
  f = ge.add_face([2522.mm,2354.mm,0.mm], [2522.mm,2354.mm,105.mm], [2522.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 6 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 plate"
  face = grp.entities.add_face([2923.mm,2354.mm,0.mm], [3043.mm,2354.mm,0.mm], [3043.mm,2362.mm,0.mm], [2923.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
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
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 6 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 gusset"
  ge = grp.entities
  f = ge.add_face([2979.mm,2354.mm,0.mm], [2979.mm,2354.mm,105.mm], [2979.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 7 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 plate"
  face = grp.entities.add_face([3380.mm,2354.mm,0.mm], [3500.mm,2354.mm,0.mm], [3500.mm,2362.mm,0.mm], [3380.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
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
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 7 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 gusset"
  ge = grp.entities
  f = ge.add_face([3436.mm,2354.mm,0.mm], [3436.mm,2354.mm,105.mm], [3436.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 8 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 plate"
  face = grp.entities.add_face([3837.mm,2354.mm,0.mm], [3957.mm,2354.mm,0.mm], [3957.mm,2362.mm,0.mm], [3837.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
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
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 8 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 gusset"
  ge = grp.entities
  f = ge.add_face([3893.mm,2354.mm,0.mm], [3893.mm,2354.mm,105.mm], [3893.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 1 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 1 foot plate"
  face = grp.entities.add_face([38.mm,220.mm,0.mm], [166.mm,220.mm,0.mm], [166.mm,280.mm,0.mm], [38.mm,280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 1 post (2x2x0.120 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 1 post (2x2x0.120 SHS)"
  face = grp.entities.add_face([114.6.mm,220.mm,0.mm], [165.39999999999998.mm,220.mm,0.mm], [165.39999999999998.mm,280.mm,0.mm], [114.6.mm,280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 1 arm (to X470)
  grp = ents.add_group
  grp.name = "Left cantilever 1 arm (to X470)"
  face = grp.entities.add_face([165.4.mm,224.6.mm,89.6.mm], [470.mm,224.6.mm,89.6.mm], [470.mm,275.4.mm,89.6.mm], [165.4.mm,275.4.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.400000000000006.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 2 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 2 foot plate"
  face = grp.entities.add_face([38.mm,770.mm,0.mm], [166.mm,770.mm,0.mm], [166.mm,830.mm,0.mm], [38.mm,830.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 2 post (2x2x0.120 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 2 post (2x2x0.120 SHS)"
  face = grp.entities.add_face([114.6.mm,770.mm,0.mm], [165.39999999999998.mm,770.mm,0.mm], [165.39999999999998.mm,830.mm,0.mm], [114.6.mm,830.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 2 arm (to X770)
  grp = ents.add_group
  grp.name = "Left cantilever 2 arm (to X770)"
  face = grp.entities.add_face([165.4.mm,774.6.mm,89.6.mm], [770.mm,774.6.mm,89.6.mm], [770.mm,825.4.mm,89.6.mm], [165.4.mm,825.4.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.400000000000006.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 3 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 3 foot plate"
  face = grp.entities.add_face([38.mm,1150.mm,0.mm], [166.mm,1150.mm,0.mm], [166.mm,1210.mm,0.mm], [38.mm,1210.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 3 post (2x2x0.120 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 3 post (2x2x0.120 SHS)"
  face = grp.entities.add_face([114.6.mm,1150.mm,0.mm], [165.39999999999998.mm,1150.mm,0.mm], [165.39999999999998.mm,1210.mm,0.mm], [114.6.mm,1210.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 3 arm (to X770)
  grp = ents.add_group
  grp.name = "Left cantilever 3 arm (to X770)"
  face = grp.entities.add_face([165.4.mm,1154.6.mm,89.6.mm], [770.mm,1154.6.mm,89.6.mm], [770.mm,1205.3999999999999.mm,89.6.mm], [165.4.mm,1205.3999999999999.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.400000000000006.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 4 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 4 foot plate"
  face = grp.entities.add_face([38.mm,1530.mm,0.mm], [166.mm,1530.mm,0.mm], [166.mm,1590.mm,0.mm], [38.mm,1590.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 4 post (2x2x0.120 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 4 post (2x2x0.120 SHS)"
  face = grp.entities.add_face([114.6.mm,1530.mm,0.mm], [165.39999999999998.mm,1530.mm,0.mm], [165.39999999999998.mm,1590.mm,0.mm], [114.6.mm,1590.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 4 arm (to X770)
  grp = ents.add_group
  grp.name = "Left cantilever 4 arm (to X770)"
  face = grp.entities.add_face([165.4.mm,1534.6.mm,89.6.mm], [770.mm,1534.6.mm,89.6.mm], [770.mm,1585.3999999999999.mm,89.6.mm], [165.4.mm,1585.3999999999999.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.400000000000006.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 5 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 5 foot plate"
  face = grp.entities.add_face([38.mm,2080.mm,0.mm], [166.mm,2080.mm,0.mm], [166.mm,2140.mm,0.mm], [38.mm,2140.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 5 post (2x2x0.120 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 5 post (2x2x0.120 SHS)"
  face = grp.entities.add_face([114.6.mm,2080.mm,0.mm], [165.39999999999998.mm,2080.mm,0.mm], [165.39999999999998.mm,2140.mm,0.mm], [114.6.mm,2140.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 5 arm (to X470)
  grp = ents.add_group
  grp.name = "Left cantilever 5 arm (to X470)"
  face = grp.entities.add_face([165.4.mm,2084.6.mm,89.6.mm], [470.mm,2084.6.mm,89.6.mm], [470.mm,2135.4.mm,89.6.mm], [165.4.mm,2135.4.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.400000000000006.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner plate (near)
  grp = ents.add_group
  grp.name = "FP combined corner plate (near)"
  face = grp.entities.add_face([4574.mm,0.mm,77.6.mm], [4724.mm,0.mm,77.6.mm], [4724.mm,10.mm,77.6.mm], [4574.mm,10.mm,77.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(157.4.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner ext plate (near)
  grp = ents.add_group
  grp.name = "FP combined corner ext plate (near)"
  face = grp.entities.add_face([4574.mm,-50.mm,77.6.mm], [4724.mm,-50.mm,77.6.mm], [4724.mm,-40.mm,77.6.mm], [4574.mm,-40.mm,77.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(157.4.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined right-beam seat (near)
  grp = ents.add_group
  grp.name = "FP combined right-beam seat (near)"
  face = grp.entities.add_face([4574.mm,0.mm,77.6.mm], [4724.mm,0.mm,77.6.mm], [4724.mm,55.mm,77.6.mm], [4574.mm,55.mm,77.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined BR rail seat (near)
  grp = ents.add_group
  grp.name = "FP combined BR rail seat (near)"
  face = grp.entities.add_face([4619.mm,0.mm,148.mm], [4679.mm,0.mm,148.mm], [4679.mm,55.mm,148.mm], [4619.mm,55.mm,148.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X4599 Z103
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X4599 Z103"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,-50.mm,103.6.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
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
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X4699 Z103
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X4699 Z103"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,-50.mm,103.6.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
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
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner plate (far)
  grp = ents.add_group
  grp.name = "FP combined corner plate (far)"
  face = grp.entities.add_face([4574.mm,2352.mm,77.6.mm], [4724.mm,2352.mm,77.6.mm], [4724.mm,2362.mm,77.6.mm], [4574.mm,2362.mm,77.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(157.4.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner ext plate (far)
  grp = ents.add_group
  grp.name = "FP combined corner ext plate (far)"
  face = grp.entities.add_face([4574.mm,2402.mm,77.6.mm], [4724.mm,2402.mm,77.6.mm], [4724.mm,2412.mm,77.6.mm], [4574.mm,2412.mm,77.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(157.4.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined right-beam seat (far)
  grp = ents.add_group
  grp.name = "FP combined right-beam seat (far)"
  face = grp.entities.add_face([4574.mm,2307.mm,77.6.mm], [4724.mm,2307.mm,77.6.mm], [4724.mm,2362.mm,77.6.mm], [4574.mm,2362.mm,77.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined BR rail seat (far)
  grp = ents.add_group
  grp.name = "FP combined BR rail seat (far)"
  face = grp.entities.add_face([4619.mm,2307.mm,148.mm], [4679.mm,2307.mm,148.mm], [4679.mm,2362.mm,148.mm], [4619.mm,2362.mm,148.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (far) X4599 Z103
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (far) X4599 Z103"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,2352.mm,103.6.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
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
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (far) X4699 Z103
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (far) X4699 Z103"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,2352.mm,103.6.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
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
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([4654.mm,1046.mm,0.mm], [4704.8.mm,1046.mm,0.mm], [4704.8.mm,1096.8.mm,0.mm], [4654.mm,1096.8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([4654.mm,1265.2.mm,0.mm], [4704.8.mm,1265.2.mm,0.mm], [4704.8.mm,1316.mm,0.mm], [4654.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([5104.mm,1046.mm,0.mm], [5154.8.mm,1046.mm,0.mm], [5154.8.mm,1096.8.mm,0.mm], [5104.mm,1096.8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([5104.mm,1265.2.mm,0.mm], [5154.8.mm,1265.2.mm,0.mm], [5154.8.mm,1316.mm,0.mm], [5104.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([4654.mm,1096.8.mm,0.mm], [4704.8.mm,1096.8.mm,0.mm], [4704.8.mm,1265.2.mm,0.mm], [4654.mm,1265.2.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([5104.mm,1096.8.mm,0.mm], [5154.8.mm,1096.8.mm,0.mm], [5154.8.mm,1265.2.mm,0.mm], [5104.mm,1265.2.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.8.mm,1046.mm,0.mm], [5104.mm,1046.mm,0.mm], [5104.mm,1096.8.mm,0.mm], [4704.8.mm,1096.8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.8.mm,1265.2.mm,0.mm], [5104.mm,1265.2.mm,0.mm], [5104.mm,1316.mm,0.mm], [4704.8.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([4654.mm,1096.8.mm,2245.2.mm], [4704.8.mm,1096.8.mm,2245.2.mm], [4704.8.mm,1265.2.mm,2245.2.mm], [4654.mm,1265.2.mm,2245.2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([5104.mm,1096.8.mm,2245.2.mm], [5154.8.mm,1096.8.mm,2245.2.mm], [5154.8.mm,1265.2.mm,2245.2.mm], [5104.mm,1265.2.mm,2245.2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.8.mm,1046.mm,2245.2.mm], [5104.mm,1046.mm,2245.2.mm], [5104.mm,1096.8.mm,2245.2.mm], [4704.8.mm,1096.8.mm,2245.2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.8.mm,1265.2.mm,2245.2.mm], [5104.mm,1265.2.mm,2245.2.mm], [5104.mm,1316.mm,2245.2.mm], [4704.8.mm,1316.mm,2245.2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot plate
  grp = ents.add_group
  grp.name = "Foot plate"
  face = grp.entities.add_face([4604.4.mm,996.4000000000001.mm,0.mm], [4754.4.mm,996.4000000000001.mm,0.mm], [4754.4.mm,1146.4.mm,0.mm], [4604.4.mm,1146.4.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4629.4.mm,1021.4000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([4629.4.mm,1121.4.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([4729.4.mm,1021.4000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([4729.4.mm,1121.4.mm,0.mm], [0,0,1], 7.mm, 24)
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
  face = grp.entities.add_face([4604.4.mm,1215.6000000000001.mm,0.mm], [4754.4.mm,1215.6000000000001.mm,0.mm], [4754.4.mm,1365.6000000000001.mm,0.mm], [4604.4.mm,1365.6000000000001.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4629.4.mm,1240.6000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([4629.4.mm,1340.6000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([4729.4.mm,1240.6000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([4729.4.mm,1340.6000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
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
  face = grp.entities.add_face([5054.4.mm,996.4000000000001.mm,0.mm], [5204.4.mm,996.4000000000001.mm,0.mm], [5204.4.mm,1146.4.mm,0.mm], [5054.4.mm,1146.4.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5079.4.mm,1021.4000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5079.4.mm,1121.4.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5179.4.mm,1021.4000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5179.4.mm,1121.4.mm,0.mm], [0,0,1], 7.mm, 24)
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
  face = grp.entities.add_face([5054.4.mm,1215.6000000000001.mm,0.mm], [5204.4.mm,1215.6000000000001.mm,0.mm], [5204.4.mm,1365.6000000000001.mm,0.mm], [5054.4.mm,1365.6000000000001.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5079.4.mm,1240.6000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5079.4.mm,1340.6000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5179.4.mm,1240.6000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5179.4.mm,1340.6000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
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
  face = grp.entities.add_face([5122.mm,1096.8.mm,90.mm], [5152.mm,1096.8.mm,90.mm], [5152.mm,1136.8.mm,90.mm], [5122.mm,1136.8.mm,90.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1096.8.mm,1118.mm], [5152.mm,1096.8.mm,1118.mm], [5152.mm,1136.8.mm,1118.mm], [5122.mm,1136.8.mm,1118.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1096.8.mm,2146.mm], [5152.mm,1096.8.mm,2146.mm], [5152.mm,1136.8.mm,2146.mm], [5122.mm,1136.8.mm,2146.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1225.2.mm,90.mm], [5152.mm,1225.2.mm,90.mm], [5152.mm,1265.2.mm,90.mm], [5122.mm,1265.2.mm,90.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1225.2.mm,1118.mm], [5152.mm,1225.2.mm,1118.mm], [5152.mm,1265.2.mm,1118.mm], [5122.mm,1265.2.mm,1118.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1225.2.mm,2146.mm], [5152.mm,1225.2.mm,2146.mm], [5152.mm,1265.2.mm,2146.mm], [5122.mm,1265.2.mm,2146.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,0.mm,560.mm], [4674.mm,0.mm,560.mm], [4674.mm,1096.8.mm,560.mm], [4654.mm,1096.8.mm,560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,0.mm,1760.mm], [4674.mm,0.mm,1760.mm], [4674.mm,1096.8.mm,1760.mm], [4654.mm,1096.8.mm,1760.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,1265.2.mm,560.mm], [4674.mm,1265.2.mm,560.mm], [4674.mm,2362.mm,560.mm], [4654.mm,2362.mm,560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,1265.2.mm,1760.mm], [4674.mm,1265.2.mm,1760.mm], [4674.mm,2362.mm,1760.mm], [4654.mm,2362.mm,1760.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,520.mm,585.4.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,520.mm,1785.4.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,940.mm,585.4.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,940.mm,1785.4.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,1422.mm,585.4.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,1422.mm,1785.4.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,1842.mm,585.4.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,1842.mm,1785.4.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4646.mm,0.mm,530.mm], [4712.8.mm,0.mm,530.mm], [4712.8.mm,4.mm,530.mm], [4646.mm,4.mm,530.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,0.mm,556.mm], [4708.8.mm,0.mm,556.mm], [4708.8.mm,70.mm,556.mm], [4650.mm,70.mm,556.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.4.mm,-48.mm,517.9.mm], [4729.4.mm,-48.mm,517.9.mm], [4729.4.mm,-40.mm,517.9.mm], [4629.4.mm,-40.mm,517.9.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4647.4.mm,-48.mm,539.9.mm], [0,1,0], 7.mm, 24)
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
  circle = ge.add_circle([4647.4.mm,-48.mm,630.9.mm], [0,1,0], 7.mm, 24)
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
  circle = ge.add_circle([4711.4.mm,-48.mm,539.9.mm], [0,1,0], 7.mm, 24)
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
  circle = ge.add_circle([4711.4.mm,-48.mm,630.9.mm], [0,1,0], 7.mm, 24)
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
  face = grp.entities.add_face([4646.mm,0.mm,1730.mm], [4712.8.mm,0.mm,1730.mm], [4712.8.mm,4.mm,1730.mm], [4646.mm,4.mm,1730.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,0.mm,1756.mm], [4708.8.mm,0.mm,1756.mm], [4708.8.mm,70.mm,1756.mm], [4650.mm,70.mm,1756.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.4.mm,-48.mm,1717.9.mm], [4729.4.mm,-48.mm,1717.9.mm], [4729.4.mm,-40.mm,1717.9.mm], [4629.4.mm,-40.mm,1717.9.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4647.4.mm,-48.mm,1739.9.mm], [0,1,0], 7.mm, 24)
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
  circle = ge.add_circle([4647.4.mm,-48.mm,1830.9.mm], [0,1,0], 7.mm, 24)
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
  circle = ge.add_circle([4711.4.mm,-48.mm,1739.9.mm], [0,1,0], 7.mm, 24)
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
  circle = ge.add_circle([4711.4.mm,-48.mm,1830.9.mm], [0,1,0], 7.mm, 24)
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
  face = grp.entities.add_face([4646.mm,2358.mm,530.mm], [4712.8.mm,2358.mm,530.mm], [4712.8.mm,2362.mm,530.mm], [4646.mm,2362.mm,530.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,2292.mm,556.mm], [4708.8.mm,2292.mm,556.mm], [4708.8.mm,2362.mm,556.mm], [4650.mm,2362.mm,556.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.4.mm,2402.mm,517.9.mm], [4729.4.mm,2402.mm,517.9.mm], [4729.4.mm,2410.mm,517.9.mm], [4629.4.mm,2410.mm,517.9.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4647.4.mm,2352.mm,539.9.mm], [0,1,0], 7.mm, 24)
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
  circle = ge.add_circle([4647.4.mm,2352.mm,630.9.mm], [0,1,0], 7.mm, 24)
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
  circle = ge.add_circle([4711.4.mm,2352.mm,539.9.mm], [0,1,0], 7.mm, 24)
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
  circle = ge.add_circle([4711.4.mm,2352.mm,630.9.mm], [0,1,0], 7.mm, 24)
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
  face = grp.entities.add_face([4646.mm,2358.mm,1730.mm], [4712.8.mm,2358.mm,1730.mm], [4712.8.mm,2362.mm,1730.mm], [4646.mm,2362.mm,1730.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.8.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,2292.mm,1756.mm], [4708.8.mm,2292.mm,1756.mm], [4708.8.mm,2362.mm,1756.mm], [4650.mm,2362.mm,1756.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.4.mm,2402.mm,1717.9.mm], [4729.4.mm,2402.mm,1717.9.mm], [4729.4.mm,2410.mm,1717.9.mm], [4629.4.mm,2410.mm,1717.9.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4647.4.mm,2352.mm,1739.9.mm], [0,1,0], 7.mm, 24)
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
  circle = ge.add_circle([4647.4.mm,2352.mm,1830.9.mm], [0,1,0], 7.mm, 24)
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
  circle = ge.add_circle([4711.4.mm,2352.mm,1739.9.mm], [0,1,0], 7.mm, 24)
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
  circle = ge.add_circle([4711.4.mm,2352.mm,1830.9.mm], [0,1,0], 7.mm, 24)
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

  # ═══ Movement base (BL corner) ═══
  defn = model.definitions.add("Movement base (BL corner)")
  ents = defn.entities
  # U-channel rail (Movement BL) web MoveBL
  grp = ents.add_group
  grp.name = "U-channel rail (Movement BL) web MoveBL"
  face = grp.entities.add_face([131.mm,1742.mm,232.mm], [136.mm,1742.mm,232.mm], [136.mm,3062.mm,232.mm], [131.mm,3062.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-channel rail (Movement BL) flange MoveBL 303
  grp = ents.add_group
  grp.name = "U-channel rail (Movement BL) flange MoveBL 303"
  face = grp.entities.add_face([131.mm,1742.mm,303.mm], [169.mm,1742.mm,303.mm], [169.mm,3062.mm,303.mm], [131.mm,3062.mm,303.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-channel rail (Movement BL) flange MoveBL 232
  grp = ents.add_group
  grp.name = "U-channel rail (Movement BL) flange MoveBL 232"
  face = grp.entities.add_face([131.mm,1742.mm,232.mm], [169.mm,1742.mm,232.mm], [169.mm,3062.mm,232.mm], [131.mm,3062.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-channel rail (Movement BL) bottom-flange lip MoveBL
  grp = ents.add_group
  grp.name = "U-channel rail (Movement BL) bottom-flange lip MoveBL"
  face = grp.entities.add_face([164.mm,1742.mm,237.mm], [169.mm,1742.mm,237.mm], [169.mm,3062.mm,237.mm], [164.mm,3062.mm,237.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Movement base (BL corner)"
  inst.layer = model.layers["Movement"]

  # ═══ Movement base (TL corner) ═══
  defn = model.definitions.add("Movement base (TL corner)")
  ents = defn.entities
  # U-channel rail (Movement TL) web MoveTL
  grp = ents.add_group
  grp.name = "U-channel rail (Movement TL) web MoveTL"
  face = grp.entities.add_face([131.mm,1742.mm,2262.mm], [136.mm,1742.mm,2262.mm], [136.mm,3062.mm,2262.mm], [131.mm,3062.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-channel rail (Movement TL) flange MoveTL 2333
  grp = ents.add_group
  grp.name = "U-channel rail (Movement TL) flange MoveTL 2333"
  face = grp.entities.add_face([131.mm,1742.mm,2333.mm], [169.mm,1742.mm,2333.mm], [169.mm,3062.mm,2333.mm], [131.mm,3062.mm,2333.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-channel rail (Movement TL) flange MoveTL 2262
  grp = ents.add_group
  grp.name = "U-channel rail (Movement TL) flange MoveTL 2262"
  face = grp.entities.add_face([131.mm,1742.mm,2262.mm], [169.mm,1742.mm,2262.mm], [169.mm,3062.mm,2262.mm], [131.mm,3062.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-channel rail (Movement TL) bottom-flange lip MoveTL
  grp = ents.add_group
  grp.name = "U-channel rail (Movement TL) bottom-flange lip MoveTL"
  face = grp.entities.add_face([164.mm,1742.mm,2267.mm], [169.mm,1742.mm,2267.mm], [169.mm,3062.mm,2267.mm], [164.mm,3062.mm,2267.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Movement base (TL corner)"
  inst.layer = model.layers["Movement"]

  # ═══ Movement base (BR corner) ═══
  defn = model.definitions.add("Movement base (BR corner)")
  ents = defn.entities
  # U-channel rail (Movement BR) web MoveBR
  grp = ents.add_group
  grp.name = "U-channel rail (Movement BR) web MoveBR"
  face = grp.entities.add_face([2214.mm,1742.mm,232.mm], [2219.mm,1742.mm,232.mm], [2219.mm,3062.mm,232.mm], [2214.mm,3062.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-channel rail (Movement BR) flange MoveBR 303
  grp = ents.add_group
  grp.name = "U-channel rail (Movement BR) flange MoveBR 303"
  face = grp.entities.add_face([2181.mm,1742.mm,303.mm], [2219.mm,1742.mm,303.mm], [2219.mm,3062.mm,303.mm], [2181.mm,3062.mm,303.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-channel rail (Movement BR) flange MoveBR 232
  grp = ents.add_group
  grp.name = "U-channel rail (Movement BR) flange MoveBR 232"
  face = grp.entities.add_face([2181.mm,1742.mm,232.mm], [2219.mm,1742.mm,232.mm], [2219.mm,3062.mm,232.mm], [2181.mm,3062.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-channel rail (Movement BR) bottom-flange lip MoveBR
  grp = ents.add_group
  grp.name = "U-channel rail (Movement BR) bottom-flange lip MoveBR"
  face = grp.entities.add_face([2181.mm,1742.mm,237.mm], [2186.mm,1742.mm,237.mm], [2186.mm,3062.mm,237.mm], [2181.mm,3062.mm,237.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Movement base (BR corner)"
  inst.layer = model.layers["Movement"]

  # ═══ Movement base (TR corner) ═══
  defn = model.definitions.add("Movement base (TR corner)")
  ents = defn.entities
  # U-channel rail (Movement TR) web MoveTR
  grp = ents.add_group
  grp.name = "U-channel rail (Movement TR) web MoveTR"
  face = grp.entities.add_face([2214.mm,1742.mm,2262.mm], [2219.mm,1742.mm,2262.mm], [2219.mm,3062.mm,2262.mm], [2214.mm,3062.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-channel rail (Movement TR) flange MoveTR 2333
  grp = ents.add_group
  grp.name = "U-channel rail (Movement TR) flange MoveTR 2333"
  face = grp.entities.add_face([2181.mm,1742.mm,2333.mm], [2219.mm,1742.mm,2333.mm], [2219.mm,3062.mm,2333.mm], [2181.mm,3062.mm,2333.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-channel rail (Movement TR) flange MoveTR 2262
  grp = ents.add_group
  grp.name = "U-channel rail (Movement TR) flange MoveTR 2262"
  face = grp.entities.add_face([2181.mm,1742.mm,2262.mm], [2219.mm,1742.mm,2262.mm], [2219.mm,3062.mm,2262.mm], [2181.mm,3062.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-channel rail (Movement TR) bottom-flange lip MoveTR
  grp = ents.add_group
  grp.name = "U-channel rail (Movement TR) bottom-flange lip MoveTR"
  face = grp.entities.add_face([2181.mm,1742.mm,2267.mm], [2186.mm,1742.mm,2267.mm], [2186.mm,3062.mm,2267.mm], [2181.mm,3062.mm,2267.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Movement base (TR corner)"
  inst.layer = model.layers["Movement"]

  # ═══ Container shell (no ceiling) ═══
  defn = model.definitions.add("Container shell (no ceiling)")
  ents = defn.entities
  # Floor (reference)
  grp = ents.add_group
  grp.name = "Floor (reference)"
  face = grp.entities.add_face([-300.mm,0.mm,-12.mm], [4974.mm,0.mm,-12.mm], [4974.mm,2362.mm,-12.mm], [-300.mm,2362.mm,-12.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Floor (reference)"] || model.materials.add("Floor (reference)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.08
  grp.material = mat

  # Depth rail BL web rBL
  grp = ents.add_group
  grp.name = "Depth rail BL web rBL"
  face = grp.entities.add_face([131.mm,0.mm,232.mm], [136.mm,0.mm,232.mm], [136.mm,2362.mm,232.mm], [131.mm,2362.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Depth rail BL flange rBL 303
  grp = ents.add_group
  grp.name = "Depth rail BL flange rBL 303"
  face = grp.entities.add_face([131.mm,0.mm,303.mm], [169.mm,0.mm,303.mm], [169.mm,2362.mm,303.mm], [131.mm,2362.mm,303.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Depth rail BL flange rBL 232
  grp = ents.add_group
  grp.name = "Depth rail BL flange rBL 232"
  face = grp.entities.add_face([131.mm,0.mm,232.mm], [169.mm,0.mm,232.mm], [169.mm,2362.mm,232.mm], [131.mm,2362.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Depth rail BL bottom-flange lip rBL
  grp = ents.add_group
  grp.name = "Depth rail BL bottom-flange lip rBL"
  face = grp.entities.add_face([164.mm,0.mm,237.mm], [169.mm,0.mm,237.mm], [169.mm,2362.mm,237.mm], [164.mm,2362.mm,237.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Depth rail BR web rBR
  grp = ents.add_group
  grp.name = "Depth rail BR web rBR"
  face = grp.entities.add_face([4638.mm,0.mm,232.mm], [4643.mm,0.mm,232.mm], [4643.mm,2362.mm,232.mm], [4638.mm,2362.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Depth rail BR flange rBR 303
  grp = ents.add_group
  grp.name = "Depth rail BR flange rBR 303"
  face = grp.entities.add_face([4605.mm,0.mm,303.mm], [4643.mm,0.mm,303.mm], [4643.mm,2362.mm,303.mm], [4605.mm,2362.mm,303.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Depth rail BR flange rBR 232
  grp = ents.add_group
  grp.name = "Depth rail BR flange rBR 232"
  face = grp.entities.add_face([4605.mm,0.mm,232.mm], [4643.mm,0.mm,232.mm], [4643.mm,2362.mm,232.mm], [4605.mm,2362.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Depth rail BR bottom-flange lip rBR
  grp = ents.add_group
  grp.name = "Depth rail BR bottom-flange lip rBR"
  face = grp.entities.add_face([4605.mm,0.mm,237.mm], [4610.mm,0.mm,237.mm], [4610.mm,2362.mm,237.mm], [4605.mm,2362.mm,237.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Depth rail TL web rTL
  grp = ents.add_group
  grp.name = "Depth rail TL web rTL"
  face = grp.entities.add_face([131.mm,0.mm,2262.mm], [136.mm,0.mm,2262.mm], [136.mm,2362.mm,2262.mm], [131.mm,2362.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Depth rail TL flange rTL 2333
  grp = ents.add_group
  grp.name = "Depth rail TL flange rTL 2333"
  face = grp.entities.add_face([131.mm,0.mm,2333.mm], [169.mm,0.mm,2333.mm], [169.mm,2362.mm,2333.mm], [131.mm,2362.mm,2333.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Depth rail TL flange rTL 2262
  grp = ents.add_group
  grp.name = "Depth rail TL flange rTL 2262"
  face = grp.entities.add_face([131.mm,0.mm,2262.mm], [169.mm,0.mm,2262.mm], [169.mm,2362.mm,2262.mm], [131.mm,2362.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Depth rail TL bottom-flange lip rTL
  grp = ents.add_group
  grp.name = "Depth rail TL bottom-flange lip rTL"
  face = grp.entities.add_face([164.mm,0.mm,2267.mm], [169.mm,0.mm,2267.mm], [169.mm,2362.mm,2267.mm], [164.mm,2362.mm,2267.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Depth rail TR web rTR
  grp = ents.add_group
  grp.name = "Depth rail TR web rTR"
  face = grp.entities.add_face([4638.mm,0.mm,2262.mm], [4643.mm,0.mm,2262.mm], [4643.mm,2362.mm,2262.mm], [4638.mm,2362.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Depth rail TR flange rTR 2333
  grp = ents.add_group
  grp.name = "Depth rail TR flange rTR 2333"
  face = grp.entities.add_face([4605.mm,0.mm,2333.mm], [4643.mm,0.mm,2333.mm], [4643.mm,2362.mm,2333.mm], [4605.mm,2362.mm,2333.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Depth rail TR flange rTR 2262
  grp = ents.add_group
  grp.name = "Depth rail TR flange rTR 2262"
  face = grp.entities.add_face([4605.mm,0.mm,2262.mm], [4643.mm,0.mm,2262.mm], [4643.mm,2362.mm,2262.mm], [4605.mm,2362.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Depth rail TR bottom-flange lip rTR
  grp = ents.add_group
  grp.name = "Depth rail TR bottom-flange lip rTR"
  face = grp.entities.add_face([4605.mm,0.mm,2267.mm], [4610.mm,0.mm,2267.mm], [4610.mm,2362.mm,2267.mm], [4605.mm,2362.mm,2267.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-channel rail (Movement BL) web MoveBL"] || model.materials.add("U-channel rail (Movement BL) web MoveBL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Container shell (no ceiling)"
  inst.layer = model.layers["Shell"]


# ═══ Movement — BL corner (Sheet 3 model): ONE click — the depth-rail ROLL drives the tilt;
# the green Z cross-slide takes up the small foreshortening. One coordinated motion. ═══
mvpan_BL = model.definitions.add("Panel tilt BL")
ents = mvpan_BL.entities
  # 304 SS corner plate (Movement BL)
  grp = ents.add_group
  grp.name = "304 SS corner plate (Movement BL)"
  face = grp.entities.add_face([-14.mm,-16.mm,7.mm], [20.mm,-16.mm,7.mm], [20.mm,0.mm,7.mm], [-14.mm,0.mm,7.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # ACM film-panel corner — partial ghost (Movement BL)
  grp = ents.add_group
  grp.name = "ACM film-panel corner — partial ghost (Movement BL)"
  face = grp.entities.add_face([33.mm,-8.mm,2.mm], [753.mm,-8.mm,2.mm], [753.mm,-4.mm,2.mm], [33.mm,-4.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(720.mm)
  mat = model.materials["ACM film-panel corner — partial ghost (Movement BL)"] || model.materials.add("ACM film-panel corner — partial ghost (Movement BL)")
  mat.color = Sketchup::Color.new(31, 59, 102)
  mat.alpha = 0.3
  grp.material = mat

  # Film frame 2x2 6061 — bottom upstand (Movement BL)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 — bottom upstand (Movement BL)"
  face = grp.entities.add_face([33.mm,-58.mm,2.mm], [753.mm,-58.mm,2.mm], [753.mm,-8.mm,2.mm], [33.mm,-8.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 6061 — bottom in-plane leg (Movement BL)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 — bottom in-plane leg (Movement BL)"
  face = grp.entities.add_face([33.mm,-11.mm,2.mm], [753.mm,-11.mm,2.mm], [753.mm,-8.mm,2.mm], [33.mm,-8.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 6061 — left upstand (Movement BL)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 — left upstand (Movement BL)"
  face = grp.entities.add_face([33.mm,-58.mm,2.mm], [36.mm,-58.mm,2.mm], [36.mm,-8.mm,2.mm], [33.mm,-8.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(720.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 6061 — left in-plane leg (Movement BL)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 — left in-plane leg (Movement BL)"
  face = grp.entities.add_face([33.mm,-11.mm,2.mm], [83.mm,-11.mm,2.mm], [83.mm,-8.mm,2.mm], [33.mm,-8.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(720.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (angle frame → corner plate) (Movement BL)
  grp = ents.add_group
  grp.name = "Frame-corner bolt (angle frame → corner plate) (Movement BL)"
  ge = grp.entities
  circle = ge.add_circle([33.mm,-14.mm,2.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

mvfl_BL = model.definitions.add("Float BL")
ents = mvfl_BL.entities
  # Horizontal X cross-slide (SWING, purple ~260) (Movement BL)
  grp = ents.add_group
  grp.name = "Horizontal X cross-slide (SWING, purple ~260) (Movement BL)"
  face = grp.entities.add_face([130.mm,2263.mm,142.mm], [390.mm,2263.mm,142.mm], [390.mm,2277.mm,142.mm], [130.mm,2277.mm,142.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X cross-slide (SWING, purple ~260) (Movement BL)"] || model.materials.add("Horizontal X cross-slide (SWING, purple ~260) (Movement BL)")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint (Belden UJ-SS750x375) (Movement BL)
  grp = ents.add_group
  grp.name = "U-joint (Belden UJ-SS750x375) (Movement BL)"
  face = grp.entities.add_face([138.mm,2258.mm,146.mm], [162.mm,2258.mm,146.mm], [162.mm,2282.mm,146.mm], [138.mm,2282.mm,146.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Input stub 3/8 (X slide → U-joint) (Movement BL)
  grp = ents.add_group
  grp.name = "Input stub 3/8 (X slide → U-joint) (Movement BL)"
  ge = grp.entities
  circle = ge.add_circle([155.mm,2270.mm,160.mm], [1,0,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(46.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 4040N12 304 shaft support (clamps stub → carrier) (Movement BL)
  grp = ents.add_group
  grp.name = "4040N12 304 shaft support (clamps stub → carrier) (Movement BL)"
  face = grp.entities.add_face([176.mm,2261.mm,149.mm], [199.mm,2261.mm,149.mm], [199.mm,2279.mm,149.mm], [176.mm,2279.mm,149.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Output stub 3/8 (U-joint → corner plate) (Movement BL)
  grp = ents.add_group
  grp.name = "Output stub 3/8 (U-joint → corner plate) (Movement BL)"
  ge = grp.entities
  circle = ge.add_circle([150.mm,2248.mm,160.mm], [0,1,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

mvpan_BL_inst = mvfl_BL.entities.add_instance(mvpan_BL, Geom::Transformation.translation([150.mm, 2270.mm, 158.mm]))
mvpan_BL_inst.name = "Panel tilt BL"; mvpan_BL_inst.layer = model.layers["Movement"]
mvo_BL = model.definitions.add("Carriage BL")
ents = mvo_BL.entities
  # Acetal skate wheel Ø32 (Movement BL) 2270
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (Movement BL) 2270"
  ge = grp.entities
  circle = ge.add_circle([140.mm,2270.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal skate wheel Ø32 (Movement BL) 2310
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (Movement BL) 2310"
  ge = grp.entities
  circle = ge.add_circle([140.mm,2310.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (Movement BL)
  grp = ents.add_group
  grp.name = "Carriage plate (Movement BL)"
  face = grp.entities.add_face([177.mm,2263.mm,154.mm], [191.mm,2263.mm,154.mm], [191.mm,2349.mm,154.mm], [177.mm,2349.mm,154.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(145.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z cross-slide (TILT, green ~250) (Movement BL)
  grp = ents.add_group
  grp.name = "Vertical Z cross-slide (TILT, green ~250) (Movement BL)"
  face = grp.entities.add_face([171.mm,2263.mm,140.mm], [181.mm,2263.mm,140.mm], [181.mm,2281.mm,140.mm], [171.mm,2281.mm,140.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(250.mm)
  mat = model.materials["Vertical Z cross-slide (TILT, green ~250) (Movement BL)"] || model.materials.add("Vertical Z cross-slide (TILT, green ~250) (Movement BL)")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

mvfl_BL_inst = mvo_BL.entities.add_instance(mvfl_BL, Geom::Transformation.new)
mvfl_BL_inst.name = "Float BL"; mvfl_BL_inst.layer = model.layers["Movement"]
mvp_BL = model.definitions.add("Movement BL")
mvo_BL_inst = mvp_BL.entities.add_instance(mvo_BL, Geom::Transformation.new)
mvo_BL_inst.name = "Carriage BL"; mvo_BL_inst.layer = model.layers["Movement"]
mvp_BL_inst = entities.add_instance(mvp_BL, Geom::Transformation.new)
mvp_BL_inst.name = "Movement BL"; mvp_BL_inst.layer = model.layers["Movement"]
da = "dynamic_attributes"
[mvp_BL, mvp_BL_inst].each do |e|
  e.set_attribute(da, "_name", "MovementBL"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "move", 0.0)
end
mvp_BL_inst.set_attribute(da, "_move_access", "VIEW")
mvp_BL_inst.set_attribute(da, "_move_label", "BL: depth-roll drives the tilt (green Z cross-slide absorbs foreshortening)")
mvp_BL_inst.set_attribute(da, "onclick", 'ANIMATE("move", 0, 1, -1)')
mvp_BL_inst.set_attribute(da, "_onclick_access", "NONE")
# carriage ROLLS along the depth rail (Y) — the DRIVER of tilt (Sheet 3); one coordinated motion
[mvo_BL, mvo_BL_inst].each do |e|
  e.set_attribute(da, "_name", "CarriageBL"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "drive", 0.0); e.set_attribute(da, "y", 0.0)
end
mvo_BL_inst.set_attribute(da, "_drive_formula", "MovementBL!move")
mvo_BL_inst.set_attribute(da, "_y_formula", "drive * 320")
# float (U-joint + panel) — the cross-slide takes up a SMALL foreshortening along the green Z way
[mvfl_BL, mvfl_BL_inst].each do |e|
  e.set_attribute(da, "_name", "FloatBL"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "drive", 0.0); e.set_attribute(da, "z", 0.0)
end
mvfl_BL_inst.set_attribute(da, "_drive_formula", "CarriageBL!drive")
mvfl_BL_inst.set_attribute(da, "_z_formula", "ABS(drive) * 50")
# panel tiltS about the U-joint (rotx=tilt / rotz=swing) — the DOF the depth-roll produces
[mvpan_BL, mvpan_BL_inst].each do |e|
  e.set_attribute(da, "_name", "PanelTiltBL"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "drive", 0.0); e.set_attribute(da, "rotx", 0.0)
end
mvpan_BL_inst.set_attribute(da, "_drive_formula", "FloatBL!drive")
mvpan_BL_inst.set_attribute(da, "_rotx_formula", "drive * 30")
mvtxt_BL = entities.add_text("CLICK BL: 1st click tilts toward the PINHOLE, 2nd toward the FAR WALL — the green Z slider foreshortens the SAME both ways", Geom::Point3d.new(570.mm, 2762.mm, 680.mm), Geom::Vector3d.new(300.mm, -400.mm, 300.mm))
mvtxt_BL.layer = model.layers["Movement"] rescue nil

# ═══ Movement — TL corner (Sheet 3 model): ONE click — the depth-rail ROLL drives the tilt;
# the green Z cross-slide takes up the small foreshortening. One coordinated motion. ═══
mvpan_TL = model.definitions.add("Panel tilt TL")
ents = mvpan_TL.entities
  # 304 SS corner plate (Movement TL)
  grp = ents.add_group
  grp.name = "304 SS corner plate (Movement TL)"
  face = grp.entities.add_face([-14.mm,-16.mm,-43.mm], [20.mm,-16.mm,-43.mm], [20.mm,0.mm,-43.mm], [-14.mm,0.mm,-43.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # ACM film-panel corner — partial ghost (Movement TL)
  grp = ents.add_group
  grp.name = "ACM film-panel corner — partial ghost (Movement TL)"
  face = grp.entities.add_face([33.mm,-8.mm,-718.mm], [753.mm,-8.mm,-718.mm], [753.mm,-4.mm,-718.mm], [33.mm,-4.mm,-718.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(720.mm)
  mat = model.materials["ACM film-panel corner — partial ghost (Movement BL)"] || model.materials.add("ACM film-panel corner — partial ghost (Movement BL)")
  mat.color = Sketchup::Color.new(31, 59, 102)
  mat.alpha = 0.3
  grp.material = mat

  # Film frame 2x2 6061 — top upstand (Movement TL)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 — top upstand (Movement TL)"
  face = grp.entities.add_face([33.mm,-58.mm,-1.mm], [753.mm,-58.mm,-1.mm], [753.mm,-8.mm,-1.mm], [33.mm,-8.mm,-1.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 6061 — top in-plane leg (Movement TL)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 — top in-plane leg (Movement TL)"
  face = grp.entities.add_face([33.mm,-11.mm,-48.mm], [753.mm,-11.mm,-48.mm], [753.mm,-8.mm,-48.mm], [33.mm,-8.mm,-48.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 6061 — left upstand (Movement TL)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 — left upstand (Movement TL)"
  face = grp.entities.add_face([33.mm,-58.mm,-718.mm], [36.mm,-58.mm,-718.mm], [36.mm,-8.mm,-718.mm], [33.mm,-8.mm,-718.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(720.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 6061 — left in-plane leg (Movement TL)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 — left in-plane leg (Movement TL)"
  face = grp.entities.add_face([33.mm,-11.mm,-718.mm], [83.mm,-11.mm,-718.mm], [83.mm,-8.mm,-718.mm], [33.mm,-8.mm,-718.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(720.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (angle frame → corner plate) (Movement TL)
  grp = ents.add_group
  grp.name = "Frame-corner bolt (angle frame → corner plate) (Movement TL)"
  ge = grp.entities
  circle = ge.add_circle([33.mm,-14.mm,2.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

mvfl_TL = model.definitions.add("Float TL")
ents = mvfl_TL.entities
  # Horizontal X cross-slide (SWING, purple ~260) (Movement TL)
  grp = ents.add_group
  grp.name = "Horizontal X cross-slide (SWING, purple ~260) (Movement TL)"
  face = grp.entities.add_face([130.mm,2263.mm,2256.mm], [390.mm,2263.mm,2256.mm], [390.mm,2277.mm,2256.mm], [130.mm,2277.mm,2256.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X cross-slide (SWING, purple ~260) (Movement BL)"] || model.materials.add("Horizontal X cross-slide (SWING, purple ~260) (Movement BL)")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint (Belden UJ-SS750x375) (Movement TL)
  grp = ents.add_group
  grp.name = "U-joint (Belden UJ-SS750x375) (Movement TL)"
  face = grp.entities.add_face([138.mm,2258.mm,2238.mm], [162.mm,2258.mm,2238.mm], [162.mm,2282.mm,2238.mm], [138.mm,2282.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Input stub 3/8 (X slide → U-joint) (Movement TL)
  grp = ents.add_group
  grp.name = "Input stub 3/8 (X slide → U-joint) (Movement TL)"
  ge = grp.entities
  circle = ge.add_circle([155.mm,2270.mm,2252.mm], [1,0,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(46.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 4040N12 304 shaft support (clamps stub → carrier) (Movement TL)
  grp = ents.add_group
  grp.name = "4040N12 304 shaft support (clamps stub → carrier) (Movement TL)"
  face = grp.entities.add_face([176.mm,2261.mm,2241.mm], [199.mm,2261.mm,2241.mm], [199.mm,2279.mm,2241.mm], [176.mm,2279.mm,2241.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Output stub 3/8 (U-joint → corner plate) (Movement TL)
  grp = ents.add_group
  grp.name = "Output stub 3/8 (U-joint → corner plate) (Movement TL)"
  ge = grp.entities
  circle = ge.add_circle([150.mm,2248.mm,2252.mm], [0,1,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

mvpan_TL_inst = mvfl_TL.entities.add_instance(mvpan_TL, Geom::Transformation.translation([150.mm, 2270.mm, 2250.mm]))
mvpan_TL_inst.name = "Panel tilt TL"; mvpan_TL_inst.layer = model.layers["Movement"]
mvo_TL = model.definitions.add("Carriage TL")
ents = mvo_TL.entities
  # Acetal skate wheel Ø32 (Movement TL) 2270
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (Movement TL) 2270"
  ge = grp.entities
  circle = ge.add_circle([140.mm,2270.mm,2283.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal skate wheel Ø32 (Movement TL) 2310
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (Movement TL) 2310"
  ge = grp.entities
  circle = ge.add_circle([140.mm,2310.mm,2283.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (Movement TL)
  grp = ents.add_group
  grp.name = "Carriage plate (Movement TL)"
  face = grp.entities.add_face([177.mm,2263.mm,2246.mm], [191.mm,2263.mm,2246.mm], [191.mm,2349.mm,2246.mm], [177.mm,2349.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(83.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z cross-slide (TILT, green ~250) (Movement TL)
  grp = ents.add_group
  grp.name = "Vertical Z cross-slide (TILT, green ~250) (Movement TL)"
  face = grp.entities.add_face([163.mm,2263.mm,1998.mm], [173.mm,2263.mm,1998.mm], [173.mm,2281.mm,1998.mm], [163.mm,2281.mm,1998.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(250.mm)
  mat = model.materials["Vertical Z cross-slide (TILT, green ~250) (Movement BL)"] || model.materials.add("Vertical Z cross-slide (TILT, green ~250) (Movement BL)")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

mvfl_TL_inst = mvo_TL.entities.add_instance(mvfl_TL, Geom::Transformation.new)
mvfl_TL_inst.name = "Float TL"; mvfl_TL_inst.layer = model.layers["Movement"]
mvp_TL = model.definitions.add("Movement TL")
mvo_TL_inst = mvp_TL.entities.add_instance(mvo_TL, Geom::Transformation.new)
mvo_TL_inst.name = "Carriage TL"; mvo_TL_inst.layer = model.layers["Movement"]
mvp_TL_inst = entities.add_instance(mvp_TL, Geom::Transformation.new)
mvp_TL_inst.name = "Movement TL"; mvp_TL_inst.layer = model.layers["Movement"]
da = "dynamic_attributes"
[mvp_TL, mvp_TL_inst].each do |e|
  e.set_attribute(da, "_name", "MovementTL"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "move", 0.0)
end
mvp_TL_inst.set_attribute(da, "_move_access", "VIEW")
mvp_TL_inst.set_attribute(da, "_move_label", "TL: depth-roll drives the tilt (green Z cross-slide absorbs foreshortening)")
mvp_TL_inst.set_attribute(da, "onclick", 'ANIMATE("move", 0, 1, -1)')
mvp_TL_inst.set_attribute(da, "_onclick_access", "NONE")
# carriage ROLLS along the depth rail (Y) — the DRIVER of tilt (Sheet 3); one coordinated motion
[mvo_TL, mvo_TL_inst].each do |e|
  e.set_attribute(da, "_name", "CarriageTL"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "drive", 0.0); e.set_attribute(da, "y", 0.0)
end
mvo_TL_inst.set_attribute(da, "_drive_formula", "MovementTL!move")
mvo_TL_inst.set_attribute(da, "_y_formula", "drive * 320")
# float (U-joint + panel) — the cross-slide takes up a SMALL foreshortening along the green Z way
[mvfl_TL, mvfl_TL_inst].each do |e|
  e.set_attribute(da, "_name", "FloatTL"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "drive", 0.0); e.set_attribute(da, "z", 0.0)
end
mvfl_TL_inst.set_attribute(da, "_drive_formula", "CarriageTL!drive")
mvfl_TL_inst.set_attribute(da, "_z_formula", "ABS(drive) * -50")
# panel tiltS about the U-joint (rotx=tilt / rotz=swing) — the DOF the depth-roll produces
[mvpan_TL, mvpan_TL_inst].each do |e|
  e.set_attribute(da, "_name", "PanelTiltTL"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "drive", 0.0); e.set_attribute(da, "rotx", 0.0)
end
mvpan_TL_inst.set_attribute(da, "_drive_formula", "FloatTL!drive")
mvpan_TL_inst.set_attribute(da, "_rotx_formula", "drive * -30")
mvtxt_TL = entities.add_text("CLICK TL: 1st click tilts toward the PINHOLE, 2nd toward the FAR WALL — the green Z slider foreshortens the SAME both ways", Geom::Point3d.new(570.mm, 2762.mm, 1732.mm), Geom::Vector3d.new(300.mm, -400.mm, -300.mm))
mvtxt_TL.layer = model.layers["Movement"] rescue nil

# ═══ Movement — BR corner (Sheet 3 model): ONE click — the depth-rail ROLL drives the swing;
# the purple X cross-slide takes up the small foreshortening. One coordinated motion. ═══
mvpan_BR = model.definitions.add("Panel tilt BR")
ents = mvpan_BR.entities
  # 304 SS corner plate (Movement BR)
  grp = ents.add_group
  grp.name = "304 SS corner plate (Movement BR)"
  face = grp.entities.add_face([-20.mm,-16.mm,7.mm], [14.mm,-16.mm,7.mm], [14.mm,0.mm,7.mm], [-20.mm,0.mm,7.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # ACM film-panel corner — partial ghost (Movement BR)
  grp = ents.add_group
  grp.name = "ACM film-panel corner — partial ghost (Movement BR)"
  face = grp.entities.add_face([-753.mm,-8.mm,2.mm], [-33.mm,-8.mm,2.mm], [-33.mm,-4.mm,2.mm], [-753.mm,-4.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(720.mm)
  mat = model.materials["ACM film-panel corner — partial ghost (Movement BL)"] || model.materials.add("ACM film-panel corner — partial ghost (Movement BL)")
  mat.color = Sketchup::Color.new(31, 59, 102)
  mat.alpha = 0.3
  grp.material = mat

  # Film frame 2x2 6061 — bottom upstand (Movement BR)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 — bottom upstand (Movement BR)"
  face = grp.entities.add_face([-753.mm,-58.mm,2.mm], [-33.mm,-58.mm,2.mm], [-33.mm,-8.mm,2.mm], [-753.mm,-8.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 6061 — bottom in-plane leg (Movement BR)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 — bottom in-plane leg (Movement BR)"
  face = grp.entities.add_face([-753.mm,-11.mm,2.mm], [-33.mm,-11.mm,2.mm], [-33.mm,-8.mm,2.mm], [-753.mm,-8.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 6061 — right upstand (Movement BR)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 — right upstand (Movement BR)"
  face = grp.entities.add_face([-36.mm,-58.mm,2.mm], [-33.mm,-58.mm,2.mm], [-33.mm,-8.mm,2.mm], [-36.mm,-8.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(720.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 6061 — right in-plane leg (Movement BR)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 — right in-plane leg (Movement BR)"
  face = grp.entities.add_face([-83.mm,-11.mm,2.mm], [-33.mm,-11.mm,2.mm], [-33.mm,-8.mm,2.mm], [-83.mm,-8.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(720.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (angle frame → corner plate) (Movement BR)
  grp = ents.add_group
  grp.name = "Frame-corner bolt (angle frame → corner plate) (Movement BR)"
  ge = grp.entities
  circle = ge.add_circle([-33.mm,-14.mm,2.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

mvfl_BR = model.definitions.add("Float BR")
ents = mvfl_BR.entities
  # Vertical Z cross-slide (TILT, green ~250) (Movement BR)
  grp = ents.add_group
  grp.name = "Vertical Z cross-slide (TILT, green ~250) (Movement BR)"
  face = grp.entities.add_face([2169.mm,2263.mm,140.mm], [2179.mm,2263.mm,140.mm], [2179.mm,2281.mm,140.mm], [2169.mm,2281.mm,140.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(250.mm)
  mat = model.materials["Vertical Z cross-slide (TILT, green ~250) (Movement BL)"] || model.materials.add("Vertical Z cross-slide (TILT, green ~250) (Movement BL)")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint (Belden UJ-SS750x375) (Movement BR)
  grp = ents.add_group
  grp.name = "U-joint (Belden UJ-SS750x375) (Movement BR)"
  face = grp.entities.add_face([2188.mm,2258.mm,146.mm], [2212.mm,2258.mm,146.mm], [2212.mm,2282.mm,146.mm], [2188.mm,2282.mm,146.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Input stub 3/8 (X slide → U-joint) (Movement BR)
  grp = ents.add_group
  grp.name = "Input stub 3/8 (X slide → U-joint) (Movement BR)"
  ge = grp.entities
  circle = ge.add_circle([2149.mm,2270.mm,160.mm], [1,0,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(46.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 4040N12 304 shaft support (clamps stub → carrier) (Movement BR)
  grp = ents.add_group
  grp.name = "4040N12 304 shaft support (clamps stub → carrier) (Movement BR)"
  face = grp.entities.add_face([2151.mm,2261.mm,149.mm], [2174.mm,2261.mm,149.mm], [2174.mm,2279.mm,149.mm], [2151.mm,2279.mm,149.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Output stub 3/8 (U-joint → corner plate) (Movement BR)
  grp = ents.add_group
  grp.name = "Output stub 3/8 (U-joint → corner plate) (Movement BR)"
  ge = grp.entities
  circle = ge.add_circle([2200.mm,2248.mm,160.mm], [0,1,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

mvpan_BR_inst = mvfl_BR.entities.add_instance(mvpan_BR, Geom::Transformation.translation([2200.mm, 2270.mm, 158.mm]))
mvpan_BR_inst.name = "Panel tilt BR"; mvpan_BR_inst.layer = model.layers["Movement"]
mvo_BR = model.definitions.add("Carriage BR")
ents = mvo_BR.entities
  # Acetal skate wheel Ø32 (Movement BR) 2270
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (Movement BR) 2270"
  ge = grp.entities
  circle = ge.add_circle([2190.mm,2270.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal skate wheel Ø32 (Movement BR) 2310
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (Movement BR) 2310"
  ge = grp.entities
  circle = ge.add_circle([2190.mm,2310.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (Movement BR)
  grp = ents.add_group
  grp.name = "Carriage plate (Movement BR)"
  face = grp.entities.add_face([2159.mm,2263.mm,154.mm], [2173.mm,2263.mm,154.mm], [2173.mm,2349.mm,154.mm], [2159.mm,2349.mm,154.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(145.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X cross-slide (SWING, purple ~260) (Movement BR)
  grp = ents.add_group
  grp.name = "Horizontal X cross-slide (SWING, purple ~260) (Movement BR)"
  face = grp.entities.add_face([1960.mm,2263.mm,142.mm], [2220.mm,2263.mm,142.mm], [2220.mm,2277.mm,142.mm], [1960.mm,2277.mm,142.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X cross-slide (SWING, purple ~260) (Movement BL)"] || model.materials.add("Horizontal X cross-slide (SWING, purple ~260) (Movement BL)")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

mvfl_BR_inst = mvo_BR.entities.add_instance(mvfl_BR, Geom::Transformation.new)
mvfl_BR_inst.name = "Float BR"; mvfl_BR_inst.layer = model.layers["Movement"]
mvp_BR = model.definitions.add("Movement BR")
mvo_BR_inst = mvp_BR.entities.add_instance(mvo_BR, Geom::Transformation.new)
mvo_BR_inst.name = "Carriage BR"; mvo_BR_inst.layer = model.layers["Movement"]
mvp_BR_inst = entities.add_instance(mvp_BR, Geom::Transformation.new)
mvp_BR_inst.name = "Movement BR"; mvp_BR_inst.layer = model.layers["Movement"]
da = "dynamic_attributes"
[mvp_BR, mvp_BR_inst].each do |e|
  e.set_attribute(da, "_name", "MovementBR"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "move", 0.0)
end
mvp_BR_inst.set_attribute(da, "_move_access", "VIEW")
mvp_BR_inst.set_attribute(da, "_move_label", "BR: depth-roll drives the swing (purple X cross-slide absorbs foreshortening)")
mvp_BR_inst.set_attribute(da, "onclick", 'ANIMATE("move", 0, 1, -1)')
mvp_BR_inst.set_attribute(da, "_onclick_access", "NONE")
# carriage ROLLS along the depth rail (Y) — the DRIVER of swing (Sheet 3); one coordinated motion
[mvo_BR, mvo_BR_inst].each do |e|
  e.set_attribute(da, "_name", "CarriageBR"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "drive", 0.0); e.set_attribute(da, "y", 0.0)
end
mvo_BR_inst.set_attribute(da, "_drive_formula", "MovementBR!move")
mvo_BR_inst.set_attribute(da, "_y_formula", "drive * 320")
# float (U-joint + panel) — the cross-slide takes up a SMALL foreshortening along the purple X way
[mvfl_BR, mvfl_BR_inst].each do |e|
  e.set_attribute(da, "_name", "FloatBR"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "drive", 0.0); e.set_attribute(da, "x", 0.0)
end
mvfl_BR_inst.set_attribute(da, "_drive_formula", "CarriageBR!drive")
mvfl_BR_inst.set_attribute(da, "_x_formula", "ABS(drive) * -50")
# panel swingS about the U-joint (rotx=tilt / rotz=swing) — the DOF the depth-roll produces
[mvpan_BR, mvpan_BR_inst].each do |e|
  e.set_attribute(da, "_name", "PanelTiltBR"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "drive", 0.0); e.set_attribute(da, "rotz", 0.0)
end
mvpan_BR_inst.set_attribute(da, "_drive_formula", "FloatBR!drive")
mvpan_BR_inst.set_attribute(da, "_rotz_formula", "drive * 30")
mvtxt_BR = entities.add_text("CLICK BR: 1st click swings toward the PINHOLE, 2nd toward the FAR WALL — the purple X slider foreshortens the SAME both ways", Geom::Point3d.new(1780.mm, 2762.mm, 680.mm), Geom::Vector3d.new(-300.mm, -400.mm, 300.mm))
mvtxt_BR.layer = model.layers["Movement"] rescue nil

# ═══ Movement — TR corner (Sheet 3 model): ONE click — the depth-rail ROLL drives the swing;
# the purple X cross-slide takes up the small foreshortening. One coordinated motion. ═══
mvpan_TR = model.definitions.add("Panel tilt TR")
ents = mvpan_TR.entities
  # 304 SS corner plate (Movement TR)
  grp = ents.add_group
  grp.name = "304 SS corner plate (Movement TR)"
  face = grp.entities.add_face([-20.mm,-16.mm,-43.mm], [14.mm,-16.mm,-43.mm], [14.mm,0.mm,-43.mm], [-20.mm,0.mm,-43.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # ACM film-panel corner — partial ghost (Movement TR)
  grp = ents.add_group
  grp.name = "ACM film-panel corner — partial ghost (Movement TR)"
  face = grp.entities.add_face([-753.mm,-8.mm,-718.mm], [-33.mm,-8.mm,-718.mm], [-33.mm,-4.mm,-718.mm], [-753.mm,-4.mm,-718.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(720.mm)
  mat = model.materials["ACM film-panel corner — partial ghost (Movement BL)"] || model.materials.add("ACM film-panel corner — partial ghost (Movement BL)")
  mat.color = Sketchup::Color.new(31, 59, 102)
  mat.alpha = 0.3
  grp.material = mat

  # Film frame 2x2 6061 — top upstand (Movement TR)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 — top upstand (Movement TR)"
  face = grp.entities.add_face([-753.mm,-58.mm,-1.mm], [-33.mm,-58.mm,-1.mm], [-33.mm,-8.mm,-1.mm], [-753.mm,-8.mm,-1.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 6061 — top in-plane leg (Movement TR)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 — top in-plane leg (Movement TR)"
  face = grp.entities.add_face([-753.mm,-11.mm,-48.mm], [-33.mm,-11.mm,-48.mm], [-33.mm,-8.mm,-48.mm], [-753.mm,-8.mm,-48.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 6061 — right upstand (Movement TR)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 — right upstand (Movement TR)"
  face = grp.entities.add_face([-36.mm,-58.mm,-718.mm], [-33.mm,-58.mm,-718.mm], [-33.mm,-8.mm,-718.mm], [-36.mm,-8.mm,-718.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(720.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame 2x2 6061 — right in-plane leg (Movement TR)
  grp = ents.add_group
  grp.name = "Film frame 2x2 6061 — right in-plane leg (Movement TR)"
  face = grp.entities.add_face([-83.mm,-11.mm,-718.mm], [-33.mm,-11.mm,-718.mm], [-33.mm,-8.mm,-718.mm], [-83.mm,-8.mm,-718.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(720.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (angle frame → corner plate) (Movement TR)
  grp = ents.add_group
  grp.name = "Frame-corner bolt (angle frame → corner plate) (Movement TR)"
  ge = grp.entities
  circle = ge.add_circle([-33.mm,-14.mm,2.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

mvfl_TR = model.definitions.add("Float TR")
ents = mvfl_TR.entities
  # Vertical Z cross-slide (TILT, green ~250) (Movement TR)
  grp = ents.add_group
  grp.name = "Vertical Z cross-slide (TILT, green ~250) (Movement TR)"
  face = grp.entities.add_face([2171.mm,2263.mm,1998.mm], [2181.mm,2263.mm,1998.mm], [2181.mm,2281.mm,1998.mm], [2171.mm,2281.mm,1998.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(250.mm)
  mat = model.materials["Vertical Z cross-slide (TILT, green ~250) (Movement BL)"] || model.materials.add("Vertical Z cross-slide (TILT, green ~250) (Movement BL)")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint (Belden UJ-SS750x375) (Movement TR)
  grp = ents.add_group
  grp.name = "U-joint (Belden UJ-SS750x375) (Movement TR)"
  face = grp.entities.add_face([2188.mm,2258.mm,2238.mm], [2212.mm,2258.mm,2238.mm], [2212.mm,2282.mm,2238.mm], [2188.mm,2282.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Input stub 3/8 (X slide → U-joint) (Movement TR)
  grp = ents.add_group
  grp.name = "Input stub 3/8 (X slide → U-joint) (Movement TR)"
  ge = grp.entities
  circle = ge.add_circle([2149.mm,2270.mm,2252.mm], [1,0,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(46.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 4040N12 304 shaft support (clamps stub → carrier) (Movement TR)
  grp = ents.add_group
  grp.name = "4040N12 304 shaft support (clamps stub → carrier) (Movement TR)"
  face = grp.entities.add_face([2151.mm,2261.mm,2241.mm], [2174.mm,2261.mm,2241.mm], [2174.mm,2279.mm,2241.mm], [2151.mm,2279.mm,2241.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Output stub 3/8 (U-joint → corner plate) (Movement TR)
  grp = ents.add_group
  grp.name = "Output stub 3/8 (U-joint → corner plate) (Movement TR)"
  ge = grp.entities
  circle = ge.add_circle([2200.mm,2248.mm,2252.mm], [0,1,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

mvpan_TR_inst = mvfl_TR.entities.add_instance(mvpan_TR, Geom::Transformation.translation([2200.mm, 2270.mm, 2250.mm]))
mvpan_TR_inst.name = "Panel tilt TR"; mvpan_TR_inst.layer = model.layers["Movement"]
mvo_TR = model.definitions.add("Carriage TR")
ents = mvo_TR.entities
  # Acetal skate wheel Ø32 (Movement TR) 2270
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (Movement TR) 2270"
  ge = grp.entities
  circle = ge.add_circle([2190.mm,2270.mm,2283.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal skate wheel Ø32 (Movement TR) 2310
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (Movement TR) 2310"
  ge = grp.entities
  circle = ge.add_circle([2190.mm,2310.mm,2283.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (Movement TR)
  grp = ents.add_group
  grp.name = "Carriage plate (Movement TR)"
  face = grp.entities.add_face([2159.mm,2263.mm,2246.mm], [2173.mm,2263.mm,2246.mm], [2173.mm,2349.mm,2246.mm], [2159.mm,2349.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(83.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X cross-slide (SWING, purple ~260) (Movement TR)
  grp = ents.add_group
  grp.name = "Horizontal X cross-slide (SWING, purple ~260) (Movement TR)"
  face = grp.entities.add_face([1960.mm,2263.mm,2256.mm], [2220.mm,2263.mm,2256.mm], [2220.mm,2277.mm,2256.mm], [1960.mm,2277.mm,2256.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X cross-slide (SWING, purple ~260) (Movement BL)"] || model.materials.add("Horizontal X cross-slide (SWING, purple ~260) (Movement BL)")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

mvfl_TR_inst = mvo_TR.entities.add_instance(mvfl_TR, Geom::Transformation.new)
mvfl_TR_inst.name = "Float TR"; mvfl_TR_inst.layer = model.layers["Movement"]
mvp_TR = model.definitions.add("Movement TR")
mvo_TR_inst = mvp_TR.entities.add_instance(mvo_TR, Geom::Transformation.new)
mvo_TR_inst.name = "Carriage TR"; mvo_TR_inst.layer = model.layers["Movement"]
mvp_TR_inst = entities.add_instance(mvp_TR, Geom::Transformation.new)
mvp_TR_inst.name = "Movement TR"; mvp_TR_inst.layer = model.layers["Movement"]
da = "dynamic_attributes"
[mvp_TR, mvp_TR_inst].each do |e|
  e.set_attribute(da, "_name", "MovementTR"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "move", 0.0)
end
mvp_TR_inst.set_attribute(da, "_move_access", "VIEW")
mvp_TR_inst.set_attribute(da, "_move_label", "TR: depth-roll drives the swing (purple X cross-slide absorbs foreshortening)")
mvp_TR_inst.set_attribute(da, "onclick", 'ANIMATE("move", 0, 1, -1)')
mvp_TR_inst.set_attribute(da, "_onclick_access", "NONE")
# carriage ROLLS along the depth rail (Y) — the DRIVER of swing (Sheet 3); one coordinated motion
[mvo_TR, mvo_TR_inst].each do |e|
  e.set_attribute(da, "_name", "CarriageTR"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "drive", 0.0); e.set_attribute(da, "y", 0.0)
end
mvo_TR_inst.set_attribute(da, "_drive_formula", "MovementTR!move")
mvo_TR_inst.set_attribute(da, "_y_formula", "drive * 320")
# float (U-joint + panel) — the cross-slide takes up a SMALL foreshortening along the purple X way
[mvfl_TR, mvfl_TR_inst].each do |e|
  e.set_attribute(da, "_name", "FloatTR"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "drive", 0.0); e.set_attribute(da, "x", 0.0)
end
mvfl_TR_inst.set_attribute(da, "_drive_formula", "CarriageTR!drive")
mvfl_TR_inst.set_attribute(da, "_x_formula", "ABS(drive) * -50")
# panel swingS about the U-joint (rotx=tilt / rotz=swing) — the DOF the depth-roll produces
[mvpan_TR, mvpan_TR_inst].each do |e|
  e.set_attribute(da, "_name", "PanelTiltTR"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "drive", 0.0); e.set_attribute(da, "rotz", 0.0)
end
mvpan_TR_inst.set_attribute(da, "_drive_formula", "FloatTR!drive")
mvpan_TR_inst.set_attribute(da, "_rotz_formula", "drive * 30")
mvtxt_TR = entities.add_text("CLICK TR: 1st click swings toward the PINHOLE, 2nd toward the FAR WALL — the purple X slider foreshortens the SAME both ways", Geom::Point3d.new(1780.mm, 2762.mm, 1732.mm), Geom::Vector3d.new(-300.mm, -400.mm, -300.mm))
mvtxt_TR.layer = model.layers["Movement"] rescue nil

# ═══ Whole plane — Tilt: FRAME rotates rotx about the centre; each CARRIAGE stays on its rail and
# only ROLLS in Y (the cross-slide absorbs the perpendicular offset) — same rules as the Movement scene. ═══
plwTilt = model.definitions.add("Whole plane Tilt")
da = "dynamic_attributes"
frmTilt = model.definitions.add("Plane frame Tilt")
ents = frmTilt.entities
  # Film panel (near-invisible, clickable fill) — whole plane
  grp = ents.add_group
  grp.name = "Film panel (near-invisible, clickable fill) — whole plane"
  face = grp.entities.add_face([-2204.mm,0.mm,-1046.mm], [2204.mm,0.mm,-1046.mm], [2204.mm,4.mm,-1046.mm], [-2204.mm,4.mm,-1046.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2092.mm)
  mat = model.materials["Film panel (near-invisible, clickable fill) — whole plane"] || model.materials.add("Film panel (near-invisible, clickable fill) — whole plane")
  mat.color = Sketchup::Color.new(31, 59, 102)
  mat.alpha = 0.04
  grp.material = mat

  # Film frame — top upstand
  grp = ents.add_group
  grp.name = "Film frame — top upstand"
  face = grp.entities.add_face([-2204.mm,-50.mm,1043.mm], [2204.mm,-50.mm,1043.mm], [2204.mm,0.mm,1043.mm], [-2204.mm,0.mm,1043.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame — top in-plane
  grp = ents.add_group
  grp.name = "Film frame — top in-plane"
  face = grp.entities.add_face([-2204.mm,-3.mm,996.mm], [2204.mm,-3.mm,996.mm], [2204.mm,0.mm,996.mm], [-2204.mm,0.mm,996.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame — bottom upstand
  grp = ents.add_group
  grp.name = "Film frame — bottom upstand"
  face = grp.entities.add_face([-2204.mm,-50.mm,-1046.mm], [2204.mm,-50.mm,-1046.mm], [2204.mm,0.mm,-1046.mm], [-2204.mm,0.mm,-1046.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame — bottom in-plane
  grp = ents.add_group
  grp.name = "Film frame — bottom in-plane"
  face = grp.entities.add_face([-2204.mm,-3.mm,-1046.mm], [2204.mm,-3.mm,-1046.mm], [2204.mm,0.mm,-1046.mm], [-2204.mm,0.mm,-1046.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame — left upstand
  grp = ents.add_group
  grp.name = "Film frame — left upstand"
  face = grp.entities.add_face([-2204.mm,-50.mm,-1046.mm], [-2201.mm,-50.mm,-1046.mm], [-2201.mm,0.mm,-1046.mm], [-2204.mm,0.mm,-1046.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2092.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame — left in-plane
  grp = ents.add_group
  grp.name = "Film frame — left in-plane"
  face = grp.entities.add_face([-2204.mm,-3.mm,-1046.mm], [-2154.mm,-3.mm,-1046.mm], [-2154.mm,0.mm,-1046.mm], [-2204.mm,0.mm,-1046.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2092.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame — right upstand
  grp = ents.add_group
  grp.name = "Film frame — right upstand"
  face = grp.entities.add_face([2201.mm,-50.mm,-1046.mm], [2204.mm,-50.mm,-1046.mm], [2204.mm,0.mm,-1046.mm], [2201.mm,0.mm,-1046.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2092.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame — right in-plane
  grp = ents.add_group
  grp.name = "Film frame — right in-plane"
  face = grp.entities.add_face([2154.mm,-3.mm,-1046.mm], [2204.mm,-3.mm,-1046.mm], [2204.mm,0.mm,-1046.mm], [2154.mm,0.mm,-1046.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2092.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint (Belden UJ-SS750x375) (183,160)
  grp = ents.add_group
  grp.name = "U-joint (Belden UJ-SS750x375) (183,160)"
  face = grp.entities.add_face([-2249.mm,-4.mm,-1060.mm], [-2225.mm,-4.mm,-1060.mm], [-2225.mm,20.mm,-1060.mm], [-2249.mm,20.mm,-1060.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Input stub 3/8 (183,160)
  grp = ents.add_group
  grp.name = "Input stub 3/8 (183,160)"
  ge = grp.entities
  circle = ge.add_circle([-2232.mm,8.mm,-1046.mm], [1,0,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(46.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 4040N12 304 shaft support (183,160)
  grp = ents.add_group
  grp.name = "4040N12 304 shaft support (183,160)"
  face = grp.entities.add_face([-2211.mm,-1.mm,-1057.mm], [-2188.mm,-1.mm,-1057.mm], [-2188.mm,17.mm,-1057.mm], [-2211.mm,17.mm,-1057.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Output stub 3/8 (183,160)
  grp = ents.add_group
  grp.name = "Output stub 3/8 (183,160)"
  ge = grp.entities
  circle = ge.add_circle([-2237.mm,-14.mm,-1046.mm], [0,1,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (183,160)
  grp = ents.add_group
  grp.name = "Frame-corner bolt (183,160)"
  ge = grp.entities
  circle = ge.add_circle([-2204.mm,-6.mm,-1046.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 304 SS corner plate (183,160)
  grp = ents.add_group
  grp.name = "304 SS corner plate (183,160)"
  face = grp.entities.add_face([-2251.mm,-8.mm,-1041.mm], [-2217.mm,-8.mm,-1041.mm], [-2217.mm,8.mm,-1041.mm], [-2251.mm,8.mm,-1041.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint (Belden UJ-SS750x375) (4591,160)
  grp = ents.add_group
  grp.name = "U-joint (Belden UJ-SS750x375) (4591,160)"
  face = grp.entities.add_face([2225.mm,-4.mm,-1060.mm], [2249.mm,-4.mm,-1060.mm], [2249.mm,20.mm,-1060.mm], [2225.mm,20.mm,-1060.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Input stub 3/8 (4591,160)
  grp = ents.add_group
  grp.name = "Input stub 3/8 (4591,160)"
  ge = grp.entities
  circle = ge.add_circle([2186.mm,8.mm,-1046.mm], [1,0,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(46.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 4040N12 304 shaft support (4591,160)
  grp = ents.add_group
  grp.name = "4040N12 304 shaft support (4591,160)"
  face = grp.entities.add_face([2188.mm,-1.mm,-1057.mm], [2211.mm,-1.mm,-1057.mm], [2211.mm,17.mm,-1057.mm], [2188.mm,17.mm,-1057.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Output stub 3/8 (4591,160)
  grp = ents.add_group
  grp.name = "Output stub 3/8 (4591,160)"
  ge = grp.entities
  circle = ge.add_circle([2237.mm,-14.mm,-1046.mm], [0,1,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (4591,160)
  grp = ents.add_group
  grp.name = "Frame-corner bolt (4591,160)"
  ge = grp.entities
  circle = ge.add_circle([2204.mm,-6.mm,-1046.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 304 SS corner plate (4591,160)
  grp = ents.add_group
  grp.name = "304 SS corner plate (4591,160)"
  face = grp.entities.add_face([2217.mm,-8.mm,-1041.mm], [2251.mm,-8.mm,-1041.mm], [2251.mm,8.mm,-1041.mm], [2217.mm,8.mm,-1041.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint (Belden UJ-SS750x375) (183,2252)
  grp = ents.add_group
  grp.name = "U-joint (Belden UJ-SS750x375) (183,2252)"
  face = grp.entities.add_face([-2249.mm,-4.mm,1032.mm], [-2225.mm,-4.mm,1032.mm], [-2225.mm,20.mm,1032.mm], [-2249.mm,20.mm,1032.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Input stub 3/8 (183,2252)
  grp = ents.add_group
  grp.name = "Input stub 3/8 (183,2252)"
  ge = grp.entities
  circle = ge.add_circle([-2232.mm,8.mm,1046.mm], [1,0,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(46.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 4040N12 304 shaft support (183,2252)
  grp = ents.add_group
  grp.name = "4040N12 304 shaft support (183,2252)"
  face = grp.entities.add_face([-2211.mm,-1.mm,1035.mm], [-2188.mm,-1.mm,1035.mm], [-2188.mm,17.mm,1035.mm], [-2211.mm,17.mm,1035.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Output stub 3/8 (183,2252)
  grp = ents.add_group
  grp.name = "Output stub 3/8 (183,2252)"
  ge = grp.entities
  circle = ge.add_circle([-2237.mm,-14.mm,1046.mm], [0,1,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (183,2252)
  grp = ents.add_group
  grp.name = "Frame-corner bolt (183,2252)"
  ge = grp.entities
  circle = ge.add_circle([-2204.mm,-6.mm,1046.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 304 SS corner plate (183,2252)
  grp = ents.add_group
  grp.name = "304 SS corner plate (183,2252)"
  face = grp.entities.add_face([-2251.mm,-8.mm,1001.mm], [-2217.mm,-8.mm,1001.mm], [-2217.mm,8.mm,1001.mm], [-2251.mm,8.mm,1001.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint (Belden UJ-SS750x375) (4591,2252)
  grp = ents.add_group
  grp.name = "U-joint (Belden UJ-SS750x375) (4591,2252)"
  face = grp.entities.add_face([2225.mm,-4.mm,1032.mm], [2249.mm,-4.mm,1032.mm], [2249.mm,20.mm,1032.mm], [2225.mm,20.mm,1032.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Input stub 3/8 (4591,2252)
  grp = ents.add_group
  grp.name = "Input stub 3/8 (4591,2252)"
  ge = grp.entities
  circle = ge.add_circle([2186.mm,8.mm,1046.mm], [1,0,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(46.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 4040N12 304 shaft support (4591,2252)
  grp = ents.add_group
  grp.name = "4040N12 304 shaft support (4591,2252)"
  face = grp.entities.add_face([2188.mm,-1.mm,1035.mm], [2211.mm,-1.mm,1035.mm], [2211.mm,17.mm,1035.mm], [2188.mm,17.mm,1035.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Output stub 3/8 (4591,2252)
  grp = ents.add_group
  grp.name = "Output stub 3/8 (4591,2252)"
  ge = grp.entities
  circle = ge.add_circle([2237.mm,-14.mm,1046.mm], [0,1,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (4591,2252)
  grp = ents.add_group
  grp.name = "Frame-corner bolt (4591,2252)"
  ge = grp.entities
  circle = ge.add_circle([2204.mm,-6.mm,1046.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 304 SS corner plate (4591,2252)
  grp = ents.add_group
  grp.name = "304 SS corner plate (4591,2252)"
  face = grp.entities.add_face([2217.mm,-8.mm,1001.mm], [2251.mm,-8.mm,1001.mm], [2251.mm,8.mm,1001.mm], [2217.mm,8.mm,1001.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

frmTilt_inst = plwTilt.entities.add_instance(frmTilt, Geom::Transformation.translation([2387.mm, 1181.mm, 1206.mm]))
frmTilt_inst.name = "Plane frame Tilt"; frmTilt_inst.layer = model.layers["Plane Tilt"]
[frmTilt, frmTilt_inst].each { |e| e.set_attribute(da, "_name", "PlaneFrameTilt"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "rotx", 0.0) }
frmTilt_inst.set_attribute(da, "_rotx_formula", "WholePlaneTilt!move * 15")

carTilt0 = model.definitions.add("Plane carriage Tilt 0")
ents = carTilt0.entities
  # Acetal skate wheel Ø32 (150,160) 1189
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (150,160) 1189"
  ge = grp.entities
  circle = ge.add_circle([142.mm,1189.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(16.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal skate wheel Ø32 (150,160) 1229
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (150,160) 1229"
  ge = grp.entities
  circle = ge.add_circle([142.mm,1229.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(16.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (150,160)
  grp = ents.add_group
  grp.name = "Carriage plate (150,160)"
  face = grp.entities.add_face([177.mm,1182.mm,154.mm], [191.mm,1182.mm,154.mm], [191.mm,1268.mm,154.mm], [177.mm,1268.mm,154.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(145.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z cross-slide way (green) (150,160)
  grp = ents.add_group
  grp.name = "Vertical Z cross-slide way (green) (150,160)"
  face = grp.entities.add_face([171.mm,1182.mm,140.mm], [181.mm,1182.mm,140.mm], [181.mm,1200.mm,140.mm], [171.mm,1200.mm,140.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(250.mm)
  mat = model.materials["Vertical Z cross-slide (TILT, green ~250) (Movement BL)"] || model.materials.add("Vertical Z cross-slide (TILT, green ~250) (Movement BL)")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X cross-slide way (purple) (150,160)
  grp = ents.add_group
  grp.name = "Horizontal X cross-slide way (purple) (150,160)"
  face = grp.entities.add_face([130.mm,1182.mm,142.mm], [390.mm,1182.mm,142.mm], [390.mm,1196.mm,142.mm], [130.mm,1196.mm,142.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X cross-slide (SWING, purple ~260) (Movement BL)"] || model.materials.add("Horizontal X cross-slide (SWING, purple ~260) (Movement BL)")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

carTilt0_inst = plwTilt.entities.add_instance(carTilt0, Geom::Transformation.new)
carTilt0_inst.name = "Plane carriage Tilt 0"; carTilt0_inst.layer = model.layers["Plane Tilt"]
[carTilt0, carTilt0_inst].each { |e| e.set_attribute(da, "_name", "PlaneCarTilt0"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "y", 0.0) }
carTilt0_inst.set_attribute(da, "_y_formula", "WholePlaneTilt!move * 270.72")

carTilt1 = model.definitions.add("Plane carriage Tilt 1")
ents = carTilt1.entities
  # Acetal skate wheel Ø32 (4624,160) 1189
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (4624,160) 1189"
  ge = grp.entities
  circle = ge.add_circle([4616.mm,1189.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(16.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal skate wheel Ø32 (4624,160) 1229
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (4624,160) 1229"
  ge = grp.entities
  circle = ge.add_circle([4616.mm,1229.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(16.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (4624,160)
  grp = ents.add_group
  grp.name = "Carriage plate (4624,160)"
  face = grp.entities.add_face([4583.mm,1182.mm,154.mm], [4597.mm,1182.mm,154.mm], [4597.mm,1268.mm,154.mm], [4583.mm,1268.mm,154.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(145.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z cross-slide way (green) (4624,160)
  grp = ents.add_group
  grp.name = "Vertical Z cross-slide way (green) (4624,160)"
  face = grp.entities.add_face([4593.mm,1182.mm,140.mm], [4603.mm,1182.mm,140.mm], [4603.mm,1200.mm,140.mm], [4593.mm,1200.mm,140.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(250.mm)
  mat = model.materials["Vertical Z cross-slide (TILT, green ~250) (Movement BL)"] || model.materials.add("Vertical Z cross-slide (TILT, green ~250) (Movement BL)")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X cross-slide way (purple) (4624,160)
  grp = ents.add_group
  grp.name = "Horizontal X cross-slide way (purple) (4624,160)"
  face = grp.entities.add_face([4384.mm,1182.mm,142.mm], [4644.mm,1182.mm,142.mm], [4644.mm,1196.mm,142.mm], [4384.mm,1196.mm,142.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X cross-slide (SWING, purple ~260) (Movement BL)"] || model.materials.add("Horizontal X cross-slide (SWING, purple ~260) (Movement BL)")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

carTilt1_inst = plwTilt.entities.add_instance(carTilt1, Geom::Transformation.new)
carTilt1_inst.name = "Plane carriage Tilt 1"; carTilt1_inst.layer = model.layers["Plane Tilt"]
[carTilt1, carTilt1_inst].each { |e| e.set_attribute(da, "_name", "PlaneCarTilt1"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "y", 0.0) }
carTilt1_inst.set_attribute(da, "_y_formula", "WholePlaneTilt!move * 270.72")

carTilt2 = model.definitions.add("Plane carriage Tilt 2")
ents = carTilt2.entities
  # Acetal skate wheel Ø32 (150,2252) 1189
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (150,2252) 1189"
  ge = grp.entities
  circle = ge.add_circle([142.mm,1189.mm,2283.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(16.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal skate wheel Ø32 (150,2252) 1229
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (150,2252) 1229"
  ge = grp.entities
  circle = ge.add_circle([142.mm,1229.mm,2283.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(16.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (150,2252)
  grp = ents.add_group
  grp.name = "Carriage plate (150,2252)"
  face = grp.entities.add_face([177.mm,1182.mm,2246.mm], [191.mm,1182.mm,2246.mm], [191.mm,1268.mm,2246.mm], [177.mm,1268.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(83.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z cross-slide way (green) (150,2252)
  grp = ents.add_group
  grp.name = "Vertical Z cross-slide way (green) (150,2252)"
  face = grp.entities.add_face([163.mm,1182.mm,1998.mm], [173.mm,1182.mm,1998.mm], [173.mm,1200.mm,1998.mm], [163.mm,1200.mm,1998.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(250.mm)
  mat = model.materials["Vertical Z cross-slide (TILT, green ~250) (Movement BL)"] || model.materials.add("Vertical Z cross-slide (TILT, green ~250) (Movement BL)")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X cross-slide way (purple) (150,2252)
  grp = ents.add_group
  grp.name = "Horizontal X cross-slide way (purple) (150,2252)"
  face = grp.entities.add_face([130.mm,1182.mm,2256.mm], [390.mm,1182.mm,2256.mm], [390.mm,1196.mm,2256.mm], [130.mm,1196.mm,2256.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X cross-slide (SWING, purple ~260) (Movement BL)"] || model.materials.add("Horizontal X cross-slide (SWING, purple ~260) (Movement BL)")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

carTilt2_inst = plwTilt.entities.add_instance(carTilt2, Geom::Transformation.new)
carTilt2_inst.name = "Plane carriage Tilt 2"; carTilt2_inst.layer = model.layers["Plane Tilt"]
[carTilt2, carTilt2_inst].each { |e| e.set_attribute(da, "_name", "PlaneCarTilt2"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "y", 0.0) }
carTilt2_inst.set_attribute(da, "_y_formula", "WholePlaneTilt!move * -270.72")

carTilt3 = model.definitions.add("Plane carriage Tilt 3")
ents = carTilt3.entities
  # Acetal skate wheel Ø32 (4624,2252) 1189
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (4624,2252) 1189"
  ge = grp.entities
  circle = ge.add_circle([4616.mm,1189.mm,2283.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(16.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal skate wheel Ø32 (4624,2252) 1229
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (4624,2252) 1229"
  ge = grp.entities
  circle = ge.add_circle([4616.mm,1229.mm,2283.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(16.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (4624,2252)
  grp = ents.add_group
  grp.name = "Carriage plate (4624,2252)"
  face = grp.entities.add_face([4583.mm,1182.mm,2246.mm], [4597.mm,1182.mm,2246.mm], [4597.mm,1268.mm,2246.mm], [4583.mm,1268.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(83.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z cross-slide way (green) (4624,2252)
  grp = ents.add_group
  grp.name = "Vertical Z cross-slide way (green) (4624,2252)"
  face = grp.entities.add_face([4595.mm,1182.mm,1998.mm], [4605.mm,1182.mm,1998.mm], [4605.mm,1200.mm,1998.mm], [4595.mm,1200.mm,1998.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(250.mm)
  mat = model.materials["Vertical Z cross-slide (TILT, green ~250) (Movement BL)"] || model.materials.add("Vertical Z cross-slide (TILT, green ~250) (Movement BL)")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X cross-slide way (purple) (4624,2252)
  grp = ents.add_group
  grp.name = "Horizontal X cross-slide way (purple) (4624,2252)"
  face = grp.entities.add_face([4384.mm,1182.mm,2256.mm], [4644.mm,1182.mm,2256.mm], [4644.mm,1196.mm,2256.mm], [4384.mm,1196.mm,2256.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X cross-slide (SWING, purple ~260) (Movement BL)"] || model.materials.add("Horizontal X cross-slide (SWING, purple ~260) (Movement BL)")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

carTilt3_inst = plwTilt.entities.add_instance(carTilt3, Geom::Transformation.new)
carTilt3_inst.name = "Plane carriage Tilt 3"; carTilt3_inst.layer = model.layers["Plane Tilt"]
[carTilt3, carTilt3_inst].each { |e| e.set_attribute(da, "_name", "PlaneCarTilt3"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "y", 0.0) }
carTilt3_inst.set_attribute(da, "_y_formula", "WholePlaneTilt!move * -270.72")

plwTilt_inst = entities.add_instance(plwTilt, Geom::Transformation.new)
plwTilt_inst.name = "Whole plane Tilt"; plwTilt_inst.layer = model.layers["Plane Tilt"]
[plwTilt, plwTilt_inst].each do |e|
  e.set_attribute(da, "_name", "WholePlaneTilt"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "move", 0.0)
end
plwTilt_inst.set_attribute(da, "_move_access", "VIEW")
plwTilt_inst.set_attribute(da, "_move_label", "Tilt: click — frame rotxs, carriages roll on the rails")
plwTilt_inst.set_attribute(da, "onclick", 'ANIMATE("move", 0, 1)')
plwTilt_inst.set_attribute(da, "_onclick_access", "NONE")
pltxtTilt = entities.add_text("CLICK: Tilt — the frame rotxs; each carriage stays on its rail and rolls in Y", Geom::Point3d.new(2387.mm, 1481.mm, 2402.mm), Geom::Vector3d.new(300.mm, -300.mm, 300.mm))
pltxtTilt.layer = model.layers["Plane Tilt"] rescue nil

# ═══ Whole plane — Swing: FRAME rotates rotz about the centre; each CARRIAGE stays on its rail and
# only ROLLS in Y (the cross-slide absorbs the perpendicular offset) — same rules as the Movement scene. ═══
plwSwing = model.definitions.add("Whole plane Swing")
da = "dynamic_attributes"
frmSwing = model.definitions.add("Plane frame Swing")
ents = frmSwing.entities
  # Film panel (near-invisible, clickable fill) — whole plane
  grp = ents.add_group
  grp.name = "Film panel (near-invisible, clickable fill) — whole plane"
  face = grp.entities.add_face([-2204.mm,0.mm,-1046.mm], [2204.mm,0.mm,-1046.mm], [2204.mm,4.mm,-1046.mm], [-2204.mm,4.mm,-1046.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2092.mm)
  mat = model.materials["Film panel (near-invisible, clickable fill) — whole plane"] || model.materials.add("Film panel (near-invisible, clickable fill) — whole plane")
  mat.color = Sketchup::Color.new(31, 59, 102)
  mat.alpha = 0.04
  grp.material = mat

  # Film frame — top upstand
  grp = ents.add_group
  grp.name = "Film frame — top upstand"
  face = grp.entities.add_face([-2204.mm,-50.mm,1043.mm], [2204.mm,-50.mm,1043.mm], [2204.mm,0.mm,1043.mm], [-2204.mm,0.mm,1043.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame — top in-plane
  grp = ents.add_group
  grp.name = "Film frame — top in-plane"
  face = grp.entities.add_face([-2204.mm,-3.mm,996.mm], [2204.mm,-3.mm,996.mm], [2204.mm,0.mm,996.mm], [-2204.mm,0.mm,996.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame — bottom upstand
  grp = ents.add_group
  grp.name = "Film frame — bottom upstand"
  face = grp.entities.add_face([-2204.mm,-50.mm,-1046.mm], [2204.mm,-50.mm,-1046.mm], [2204.mm,0.mm,-1046.mm], [-2204.mm,0.mm,-1046.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame — bottom in-plane
  grp = ents.add_group
  grp.name = "Film frame — bottom in-plane"
  face = grp.entities.add_face([-2204.mm,-3.mm,-1046.mm], [2204.mm,-3.mm,-1046.mm], [2204.mm,0.mm,-1046.mm], [-2204.mm,0.mm,-1046.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame — left upstand
  grp = ents.add_group
  grp.name = "Film frame — left upstand"
  face = grp.entities.add_face([-2204.mm,-50.mm,-1046.mm], [-2201.mm,-50.mm,-1046.mm], [-2201.mm,0.mm,-1046.mm], [-2204.mm,0.mm,-1046.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2092.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame — left in-plane
  grp = ents.add_group
  grp.name = "Film frame — left in-plane"
  face = grp.entities.add_face([-2204.mm,-3.mm,-1046.mm], [-2154.mm,-3.mm,-1046.mm], [-2154.mm,0.mm,-1046.mm], [-2204.mm,0.mm,-1046.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2092.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame — right upstand
  grp = ents.add_group
  grp.name = "Film frame — right upstand"
  face = grp.entities.add_face([2201.mm,-50.mm,-1046.mm], [2204.mm,-50.mm,-1046.mm], [2204.mm,0.mm,-1046.mm], [2201.mm,0.mm,-1046.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2092.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Film frame — right in-plane
  grp = ents.add_group
  grp.name = "Film frame — right in-plane"
  face = grp.entities.add_face([2154.mm,-3.mm,-1046.mm], [2204.mm,-3.mm,-1046.mm], [2204.mm,0.mm,-1046.mm], [2154.mm,0.mm,-1046.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2092.mm)
  mat = model.materials["Film frame 2x2 6061 — bottom upstand (Movement BL)"] || model.materials.add("Film frame 2x2 6061 — bottom upstand (Movement BL)")
  mat.color = Sketchup::Color.new(143, 176, 200)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint (Belden UJ-SS750x375) (183,160)
  grp = ents.add_group
  grp.name = "U-joint (Belden UJ-SS750x375) (183,160)"
  face = grp.entities.add_face([-2249.mm,-4.mm,-1060.mm], [-2225.mm,-4.mm,-1060.mm], [-2225.mm,20.mm,-1060.mm], [-2249.mm,20.mm,-1060.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Input stub 3/8 (183,160)
  grp = ents.add_group
  grp.name = "Input stub 3/8 (183,160)"
  ge = grp.entities
  circle = ge.add_circle([-2232.mm,8.mm,-1046.mm], [1,0,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(46.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 4040N12 304 shaft support (183,160)
  grp = ents.add_group
  grp.name = "4040N12 304 shaft support (183,160)"
  face = grp.entities.add_face([-2211.mm,-1.mm,-1057.mm], [-2188.mm,-1.mm,-1057.mm], [-2188.mm,17.mm,-1057.mm], [-2211.mm,17.mm,-1057.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Output stub 3/8 (183,160)
  grp = ents.add_group
  grp.name = "Output stub 3/8 (183,160)"
  ge = grp.entities
  circle = ge.add_circle([-2237.mm,-14.mm,-1046.mm], [0,1,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (183,160)
  grp = ents.add_group
  grp.name = "Frame-corner bolt (183,160)"
  ge = grp.entities
  circle = ge.add_circle([-2204.mm,-6.mm,-1046.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 304 SS corner plate (183,160)
  grp = ents.add_group
  grp.name = "304 SS corner plate (183,160)"
  face = grp.entities.add_face([-2251.mm,-8.mm,-1041.mm], [-2217.mm,-8.mm,-1041.mm], [-2217.mm,8.mm,-1041.mm], [-2251.mm,8.mm,-1041.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint (Belden UJ-SS750x375) (4591,160)
  grp = ents.add_group
  grp.name = "U-joint (Belden UJ-SS750x375) (4591,160)"
  face = grp.entities.add_face([2225.mm,-4.mm,-1060.mm], [2249.mm,-4.mm,-1060.mm], [2249.mm,20.mm,-1060.mm], [2225.mm,20.mm,-1060.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Input stub 3/8 (4591,160)
  grp = ents.add_group
  grp.name = "Input stub 3/8 (4591,160)"
  ge = grp.entities
  circle = ge.add_circle([2186.mm,8.mm,-1046.mm], [1,0,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(46.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 4040N12 304 shaft support (4591,160)
  grp = ents.add_group
  grp.name = "4040N12 304 shaft support (4591,160)"
  face = grp.entities.add_face([2188.mm,-1.mm,-1057.mm], [2211.mm,-1.mm,-1057.mm], [2211.mm,17.mm,-1057.mm], [2188.mm,17.mm,-1057.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Output stub 3/8 (4591,160)
  grp = ents.add_group
  grp.name = "Output stub 3/8 (4591,160)"
  ge = grp.entities
  circle = ge.add_circle([2237.mm,-14.mm,-1046.mm], [0,1,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (4591,160)
  grp = ents.add_group
  grp.name = "Frame-corner bolt (4591,160)"
  ge = grp.entities
  circle = ge.add_circle([2204.mm,-6.mm,-1046.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 304 SS corner plate (4591,160)
  grp = ents.add_group
  grp.name = "304 SS corner plate (4591,160)"
  face = grp.entities.add_face([2217.mm,-8.mm,-1041.mm], [2251.mm,-8.mm,-1041.mm], [2251.mm,8.mm,-1041.mm], [2217.mm,8.mm,-1041.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint (Belden UJ-SS750x375) (183,2252)
  grp = ents.add_group
  grp.name = "U-joint (Belden UJ-SS750x375) (183,2252)"
  face = grp.entities.add_face([-2249.mm,-4.mm,1032.mm], [-2225.mm,-4.mm,1032.mm], [-2225.mm,20.mm,1032.mm], [-2249.mm,20.mm,1032.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Input stub 3/8 (183,2252)
  grp = ents.add_group
  grp.name = "Input stub 3/8 (183,2252)"
  ge = grp.entities
  circle = ge.add_circle([-2232.mm,8.mm,1046.mm], [1,0,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(46.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 4040N12 304 shaft support (183,2252)
  grp = ents.add_group
  grp.name = "4040N12 304 shaft support (183,2252)"
  face = grp.entities.add_face([-2211.mm,-1.mm,1035.mm], [-2188.mm,-1.mm,1035.mm], [-2188.mm,17.mm,1035.mm], [-2211.mm,17.mm,1035.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Output stub 3/8 (183,2252)
  grp = ents.add_group
  grp.name = "Output stub 3/8 (183,2252)"
  ge = grp.entities
  circle = ge.add_circle([-2237.mm,-14.mm,1046.mm], [0,1,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (183,2252)
  grp = ents.add_group
  grp.name = "Frame-corner bolt (183,2252)"
  ge = grp.entities
  circle = ge.add_circle([-2204.mm,-6.mm,1046.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 304 SS corner plate (183,2252)
  grp = ents.add_group
  grp.name = "304 SS corner plate (183,2252)"
  face = grp.entities.add_face([-2251.mm,-8.mm,1001.mm], [-2217.mm,-8.mm,1001.mm], [-2217.mm,8.mm,1001.mm], [-2251.mm,8.mm,1001.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint (Belden UJ-SS750x375) (4591,2252)
  grp = ents.add_group
  grp.name = "U-joint (Belden UJ-SS750x375) (4591,2252)"
  face = grp.entities.add_face([2225.mm,-4.mm,1032.mm], [2249.mm,-4.mm,1032.mm], [2249.mm,20.mm,1032.mm], [2225.mm,20.mm,1032.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["U-joint (Belden UJ-SS750x375) (Movement BL)"] || model.materials.add("U-joint (Belden UJ-SS750x375) (Movement BL)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Input stub 3/8 (4591,2252)
  grp = ents.add_group
  grp.name = "Input stub 3/8 (4591,2252)"
  ge = grp.entities
  circle = ge.add_circle([2186.mm,8.mm,1046.mm], [1,0,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(46.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 4040N12 304 shaft support (4591,2252)
  grp = ents.add_group
  grp.name = "4040N12 304 shaft support (4591,2252)"
  face = grp.entities.add_face([2188.mm,-1.mm,1035.mm], [2211.mm,-1.mm,1035.mm], [2211.mm,17.mm,1035.mm], [2188.mm,17.mm,1035.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Output stub 3/8 (4591,2252)
  grp = ents.add_group
  grp.name = "Output stub 3/8 (4591,2252)"
  ge = grp.entities
  circle = ge.add_circle([2237.mm,-14.mm,1046.mm], [0,1,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (4591,2252)
  grp = ents.add_group
  grp.name = "Frame-corner bolt (4591,2252)"
  ge = grp.entities
  circle = ge.add_circle([2204.mm,-6.mm,1046.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 304 SS corner plate (4591,2252)
  grp = ents.add_group
  grp.name = "304 SS corner plate (4591,2252)"
  face = grp.entities.add_face([2217.mm,-8.mm,1001.mm], [2251.mm,-8.mm,1001.mm], [2251.mm,8.mm,1001.mm], [2217.mm,8.mm,1001.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Input stub 3/8 (X slide → U-joint) (Movement BL)"] || model.materials.add("Input stub 3/8 (X slide → U-joint) (Movement BL)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

frmSwing_inst = plwSwing.entities.add_instance(frmSwing, Geom::Transformation.translation([2387.mm, 1181.mm, 1206.mm]))
frmSwing_inst.name = "Plane frame Swing"; frmSwing_inst.layer = model.layers["Plane Swing"]
[frmSwing, frmSwing_inst].each { |e| e.set_attribute(da, "_name", "PlaneFrameSwing"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "rotz", 0.0) }
frmSwing_inst.set_attribute(da, "_rotz_formula", "WholePlaneSwing!move * 15")

carSwing0 = model.definitions.add("Plane carriage Swing 0")
ents = carSwing0.entities
  # Acetal skate wheel Ø32 (150,160) 1189
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (150,160) 1189"
  ge = grp.entities
  circle = ge.add_circle([142.mm,1189.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(16.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal skate wheel Ø32 (150,160) 1229
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (150,160) 1229"
  ge = grp.entities
  circle = ge.add_circle([142.mm,1229.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(16.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (150,160)
  grp = ents.add_group
  grp.name = "Carriage plate (150,160)"
  face = grp.entities.add_face([177.mm,1182.mm,154.mm], [191.mm,1182.mm,154.mm], [191.mm,1268.mm,154.mm], [177.mm,1268.mm,154.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(145.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z cross-slide way (green) (150,160)
  grp = ents.add_group
  grp.name = "Vertical Z cross-slide way (green) (150,160)"
  face = grp.entities.add_face([171.mm,1182.mm,140.mm], [181.mm,1182.mm,140.mm], [181.mm,1200.mm,140.mm], [171.mm,1200.mm,140.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(250.mm)
  mat = model.materials["Vertical Z cross-slide (TILT, green ~250) (Movement BL)"] || model.materials.add("Vertical Z cross-slide (TILT, green ~250) (Movement BL)")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X cross-slide way (purple) (150,160)
  grp = ents.add_group
  grp.name = "Horizontal X cross-slide way (purple) (150,160)"
  face = grp.entities.add_face([130.mm,1182.mm,142.mm], [390.mm,1182.mm,142.mm], [390.mm,1196.mm,142.mm], [130.mm,1196.mm,142.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X cross-slide (SWING, purple ~260) (Movement BL)"] || model.materials.add("Horizontal X cross-slide (SWING, purple ~260) (Movement BL)")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

carSwing0_inst = plwSwing.entities.add_instance(carSwing0, Geom::Transformation.new)
carSwing0_inst.name = "Plane carriage Swing 0"; carSwing0_inst.layer = model.layers["Plane Swing"]
[carSwing0, carSwing0_inst].each { |e| e.set_attribute(da, "_name", "PlaneCarSwing0"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "y", 0.0) }
carSwing0_inst.set_attribute(da, "_y_formula", "WholePlaneSwing!move * -570.44")

carSwing1 = model.definitions.add("Plane carriage Swing 1")
ents = carSwing1.entities
  # Acetal skate wheel Ø32 (4624,160) 1189
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (4624,160) 1189"
  ge = grp.entities
  circle = ge.add_circle([4616.mm,1189.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(16.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal skate wheel Ø32 (4624,160) 1229
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (4624,160) 1229"
  ge = grp.entities
  circle = ge.add_circle([4616.mm,1229.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(16.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (4624,160)
  grp = ents.add_group
  grp.name = "Carriage plate (4624,160)"
  face = grp.entities.add_face([4583.mm,1182.mm,154.mm], [4597.mm,1182.mm,154.mm], [4597.mm,1268.mm,154.mm], [4583.mm,1268.mm,154.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(145.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z cross-slide way (green) (4624,160)
  grp = ents.add_group
  grp.name = "Vertical Z cross-slide way (green) (4624,160)"
  face = grp.entities.add_face([4593.mm,1182.mm,140.mm], [4603.mm,1182.mm,140.mm], [4603.mm,1200.mm,140.mm], [4593.mm,1200.mm,140.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(250.mm)
  mat = model.materials["Vertical Z cross-slide (TILT, green ~250) (Movement BL)"] || model.materials.add("Vertical Z cross-slide (TILT, green ~250) (Movement BL)")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X cross-slide way (purple) (4624,160)
  grp = ents.add_group
  grp.name = "Horizontal X cross-slide way (purple) (4624,160)"
  face = grp.entities.add_face([4384.mm,1182.mm,142.mm], [4644.mm,1182.mm,142.mm], [4644.mm,1196.mm,142.mm], [4384.mm,1196.mm,142.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X cross-slide (SWING, purple ~260) (Movement BL)"] || model.materials.add("Horizontal X cross-slide (SWING, purple ~260) (Movement BL)")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

carSwing1_inst = plwSwing.entities.add_instance(carSwing1, Geom::Transformation.new)
carSwing1_inst.name = "Plane carriage Swing 1"; carSwing1_inst.layer = model.layers["Plane Swing"]
[carSwing1, carSwing1_inst].each { |e| e.set_attribute(da, "_name", "PlaneCarSwing1"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "y", 0.0) }
carSwing1_inst.set_attribute(da, "_y_formula", "WholePlaneSwing!move * 570.44")

carSwing2 = model.definitions.add("Plane carriage Swing 2")
ents = carSwing2.entities
  # Acetal skate wheel Ø32 (150,2252) 1189
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (150,2252) 1189"
  ge = grp.entities
  circle = ge.add_circle([142.mm,1189.mm,2283.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(16.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal skate wheel Ø32 (150,2252) 1229
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (150,2252) 1229"
  ge = grp.entities
  circle = ge.add_circle([142.mm,1229.mm,2283.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(16.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (150,2252)
  grp = ents.add_group
  grp.name = "Carriage plate (150,2252)"
  face = grp.entities.add_face([177.mm,1182.mm,2246.mm], [191.mm,1182.mm,2246.mm], [191.mm,1268.mm,2246.mm], [177.mm,1268.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(83.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z cross-slide way (green) (150,2252)
  grp = ents.add_group
  grp.name = "Vertical Z cross-slide way (green) (150,2252)"
  face = grp.entities.add_face([163.mm,1182.mm,1998.mm], [173.mm,1182.mm,1998.mm], [173.mm,1200.mm,1998.mm], [163.mm,1200.mm,1998.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(250.mm)
  mat = model.materials["Vertical Z cross-slide (TILT, green ~250) (Movement BL)"] || model.materials.add("Vertical Z cross-slide (TILT, green ~250) (Movement BL)")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X cross-slide way (purple) (150,2252)
  grp = ents.add_group
  grp.name = "Horizontal X cross-slide way (purple) (150,2252)"
  face = grp.entities.add_face([130.mm,1182.mm,2256.mm], [390.mm,1182.mm,2256.mm], [390.mm,1196.mm,2256.mm], [130.mm,1196.mm,2256.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X cross-slide (SWING, purple ~260) (Movement BL)"] || model.materials.add("Horizontal X cross-slide (SWING, purple ~260) (Movement BL)")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

carSwing2_inst = plwSwing.entities.add_instance(carSwing2, Geom::Transformation.new)
carSwing2_inst.name = "Plane carriage Swing 2"; carSwing2_inst.layer = model.layers["Plane Swing"]
[carSwing2, carSwing2_inst].each { |e| e.set_attribute(da, "_name", "PlaneCarSwing2"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "y", 0.0) }
carSwing2_inst.set_attribute(da, "_y_formula", "WholePlaneSwing!move * -570.44")

carSwing3 = model.definitions.add("Plane carriage Swing 3")
ents = carSwing3.entities
  # Acetal skate wheel Ø32 (4624,2252) 1189
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (4624,2252) 1189"
  ge = grp.entities
  circle = ge.add_circle([4616.mm,1189.mm,2283.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(16.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal skate wheel Ø32 (4624,2252) 1229
  grp = ents.add_group
  grp.name = "Acetal skate wheel Ø32 (4624,2252) 1229"
  ge = grp.entities
  circle = ge.add_circle([4616.mm,1229.mm,2283.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(16.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (4624,2252)
  grp = ents.add_group
  grp.name = "Carriage plate (4624,2252)"
  face = grp.entities.add_face([4583.mm,1182.mm,2246.mm], [4597.mm,1182.mm,2246.mm], [4597.mm,1268.mm,2246.mm], [4583.mm,1268.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(83.mm)
  mat = model.materials["Acetal skate wheel Ø32 (Movement BL) 2270"] || model.materials.add("Acetal skate wheel Ø32 (Movement BL) 2270")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z cross-slide way (green) (4624,2252)
  grp = ents.add_group
  grp.name = "Vertical Z cross-slide way (green) (4624,2252)"
  face = grp.entities.add_face([4595.mm,1182.mm,1998.mm], [4605.mm,1182.mm,1998.mm], [4605.mm,1200.mm,1998.mm], [4595.mm,1200.mm,1998.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(250.mm)
  mat = model.materials["Vertical Z cross-slide (TILT, green ~250) (Movement BL)"] || model.materials.add("Vertical Z cross-slide (TILT, green ~250) (Movement BL)")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X cross-slide way (purple) (4624,2252)
  grp = ents.add_group
  grp.name = "Horizontal X cross-slide way (purple) (4624,2252)"
  face = grp.entities.add_face([4384.mm,1182.mm,2256.mm], [4644.mm,1182.mm,2256.mm], [4644.mm,1196.mm,2256.mm], [4384.mm,1196.mm,2256.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X cross-slide (SWING, purple ~260) (Movement BL)"] || model.materials.add("Horizontal X cross-slide (SWING, purple ~260) (Movement BL)")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

carSwing3_inst = plwSwing.entities.add_instance(carSwing3, Geom::Transformation.new)
carSwing3_inst.name = "Plane carriage Swing 3"; carSwing3_inst.layer = model.layers["Plane Swing"]
[carSwing3, carSwing3_inst].each { |e| e.set_attribute(da, "_name", "PlaneCarSwing3"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "y", 0.0) }
carSwing3_inst.set_attribute(da, "_y_formula", "WholePlaneSwing!move * 570.44")

plwSwing_inst = entities.add_instance(plwSwing, Geom::Transformation.new)
plwSwing_inst.name = "Whole plane Swing"; plwSwing_inst.layer = model.layers["Plane Swing"]
[plwSwing, plwSwing_inst].each do |e|
  e.set_attribute(da, "_name", "WholePlaneSwing"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "move", 0.0)
end
plwSwing_inst.set_attribute(da, "_move_access", "VIEW")
plwSwing_inst.set_attribute(da, "_move_label", "Swing: click — frame rotzs, carriages roll on the rails")
plwSwing_inst.set_attribute(da, "onclick", 'ANIMATE("move", 0, 1)')
plwSwing_inst.set_attribute(da, "_onclick_access", "NONE")
pltxtSwing = entities.add_text("CLICK: Swing — the frame rotzs; each carriage stays on its rail and rolls in Y", Geom::Point3d.new(2387.mm, 1481.mm, 2402.mm), Geom::Vector3d.new(300.mm, -300.mm, 300.mm))
pltxtSwing.layer = model.layers["Plane Swing"] rescue nil


# ── "Labeled" callouts (Labels tag) ──

tt = entities.add_text("PINHOLE (far wall) — the film plane faces it across the throw", Geom::Point3d.new(2399.mm, 0.mm, 1194.mm), Geom::Vector3d.new(60.mm, -50.mm, 30.mm))
tt.layer = model.layers["Labels"] rescue nil

tt = entities.add_text("Film plane 4408.0 x 2092 (edges seated in the carriers; bottom @Z160 above walkway, weight on the bottom rail; top = light guide only)", Geom::Point3d.new(2400.mm, 2262.mm, 1194.mm), Geom::Vector3d.new(60.mm, 45.mm, 20.mm))
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

tt = entities.add_text("4040N12 304 shaft support — clamps the input stub to the X (swing) slide", Geom::Point3d.new(190.mm, 2270.mm, 152.mm), Geom::Vector3d.new(55.mm, 45.mm, -14.mm))
tt.layer = model.layers["Labels"] rescue nil

# ── In-model © + license credit (default layer → shown in every scene) ──
lbb = model.bounds
lanc = Geom::Point3d.new(lbb.min.x, lbb.min.y - 400.mm, lbb.min.z)
entities.add_text("© 2026 Alvin Richards
Licensed under GNU AGPLv3
alvinr.github.io/tbs", lanc)

model.definitions.purge_unused
model.materials.purge_unused

keep_tags = ["Corners", "Film Plane", "Pinhole", "Context", "Movement", "Shell", "Plane Tilt", "Plane Swing", "Labels"]
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

# ── Movement + the two Whole-plane scenes (iso), AFTER Swing (top) ──
[["Movement", ["Movement"], [1175.mm, 2512.mm, 1194.mm, 4400.mm]], ["Whole plane — tilt", ["Shell", "Plane Tilt"], [2400.mm, 1181.mm, 1194.mm, 6800.mm]], ["Whole plane — swing", ["Shell", "Plane Swing"], [2400.mm, 1181.mm, 1194.mm, 6800.mm]]].each { |name, tags, tgt|
  model.layers.each { |l| l.visible = (l == default_layer || tags.include?(l.name)) }
  t = Geom::Point3d.new(tgt[0], tgt[1], tgt[2])
  cdir = Geom::Vector3d.new(0.5, -0.7, 0.4); cdir.normalize!
  model.active_view.camera = Sketchup::Camera.new(t.offset(cdir, tgt[3]), t, Z_AXIS)
  page = model.pages.add(name)
  page.use_camera = true
}

# ── Labeled (Labels tag) — LAST scene ──
model.layers.each { |l| l.visible = (l == default_layer || ["Corners", "Film Plane", "Pinhole", "Labels"].include?(l.name)) }
lc = Geom::Point3d.new(2400.mm, 1862.mm, 1194.mm)
ldir = Geom::Vector3d.new(0.5, -0.7, 0.4); ldir.normalize!
model.active_view.camera = Sketchup::Camera.new(lc.offset(ldir, 7200.mm), lc, Z_AXIS)
pl = model.pages.add("Labeled"); pl.use_camera = true

# Land on the Overview scene (which hides Movement/Context) so the post-regen view matches a real
# scene rather than an ad-hoc all-visible state (else the 4 Movement demos appear to "leak" into
# whatever scene tab is selected until it is re-clicked).
model.pages.selected_page = model.pages[0] if model.pages.count > 0

model.commit_operation
{ success: true, model: "Film-Plane Corner Mechanism",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
