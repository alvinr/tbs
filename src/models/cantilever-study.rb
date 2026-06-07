model = Sketchup.active_model
# Clear pages BEFORE start_operation — erase applies immediately here (inside an
# operation it is deferred, so a count-loop would spin forever). Bounded to_a.each.
model.pages.to_a.each { |p| model.pages.erase(p) }
model.start_operation("TBS-001 Cantilever Study", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# Idempotent rebuild.
to_erase = entities.to_a.select { |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text)
}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused

# ── Tags ──
  model.layers.add("Context") unless model.layers["Context"]
  model.layers.add("Processing Tray") unless model.layers["Processing Tray"]
  model.layers.add("Film Plane Rails") unless model.layers["Film Plane Rails"]
  model.layers.add("Spray Bar") unless model.layers["Spray Bar"]
  model.layers.add("Cantilevers") unless model.layers["Cantilevers"]
  model.layers.add("Grate (lift-out)") unless model.layers["Grate (lift-out)"]
  model.layers.add("Hinge Panel (transport)") unless model.layers["Hinge Panel (transport)"]
  model.layers.add("Light-trap Drum") unless model.layers["Light-trap Drum"]
  model.layers.add("Labels") unless model.layers["Labels"]

# ── Subsystems ──
  # ═══ Container (ghost) ═══
  defn = model.definitions.add("Container (ghost)")
  ents = defn.entities
  # Floor (context)
  grp = ents.add_group
  grp.name = "Floor (context)"
  face = grp.entities.add_face([-890.mm,0.mm,-40.mm], [4629.mm,0.mm,-40.mm], [4629.mm,2362.mm,-40.mm], [-890.mm,2362.mm,-40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Floor (context)"] || model.materials.add("Floor (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.25
  grp.material = mat

  # Ceiling / aperture top (context)
  grp = ents.add_group
  grp.name = "Ceiling / aperture top (context)"
  face = grp.entities.add_face([-890.mm,0.mm,2388.mm], [4629.mm,0.mm,2388.mm], [4629.mm,2362.mm,2388.mm], [-890.mm,2362.mm,2388.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Ceiling / aperture top (context)"] || model.materials.add("Ceiling / aperture top (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.08
  grp.material = mat

  # Side Wall near (context)
  grp = ents.add_group
  grp.name = "Side Wall near (context)"
  face = grp.entities.add_face([0.mm,-40.mm,0.mm], [4629.mm,-40.mm,0.mm], [4629.mm,0.mm,0.mm], [0.mm,0.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Side Wall near (context)"] || model.materials.add("Side Wall near (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.14
  grp.material = mat

  # Side Wall far (context)
  grp = ents.add_group
  grp.name = "Side Wall far (context)"
  face = grp.entities.add_face([0.mm,2362.mm,0.mm], [4629.mm,2362.mm,0.mm], [4629.mm,2402.mm,0.mm], [0.mm,2402.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Side Wall near (context)"] || model.materials.add("Side Wall near (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.14
  grp.material = mat

  # Door plane (context)
  grp = ents.add_group
  grp.name = "Door plane (context)"
  face = grp.entities.add_face([-40.mm,0.mm,0.mm], [0.mm,0.mm,0.mm], [0.mm,2362.mm,0.mm], [-40.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Door plane (context)"] || model.materials.add("Door plane (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.1
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Container (ghost)"
  inst.layer = model.layers["Context"]

  # ═══ Processing Tray (partial) ═══
  defn = model.definitions.add("Processing Tray (partial)")
  ents = defn.entities
  # Processing Tray Floor
  grp = ents.add_group
  grp.name = "Processing Tray Floor"
  face = grp.entities.add_face([170.mm,80.mm,0.mm], [4629.mm,80.mm,0.mm], [4629.mm,2280.mm,0.mm], [170.mm,2280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Processing Tray Floor"] || model.materials.add("Processing Tray Floor")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Near
  grp = ents.add_group
  grp.name = "Tray Rim Near"
  face = grp.entities.add_face([170.mm,80.mm,2.mm], [4629.mm,80.mm,2.mm], [4629.mm,82.mm,2.mm], [170.mm,82.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Processing Tray Floor"] || model.materials.add("Processing Tray Floor")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Far
  grp = ents.add_group
  grp.name = "Tray Rim Far"
  face = grp.entities.add_face([170.mm,2278.mm,2.mm], [4629.mm,2278.mm,2.mm], [4629.mm,2280.mm,2.mm], [170.mm,2280.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Processing Tray Floor"] || model.materials.add("Processing Tray Floor")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Left
  grp = ents.add_group
  grp.name = "Tray Rim Left"
  face = grp.entities.add_face([170.mm,80.mm,2.mm], [172.mm,80.mm,2.mm], [172.mm,2280.mm,2.mm], [170.mm,2280.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Processing Tray Floor"] || model.materials.add("Processing Tray Floor")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Right
  grp = ents.add_group
  grp.name = "Tray Rim Right"
  face = grp.entities.add_face([4627.mm,80.mm,2.mm], [4629.mm,80.mm,2.mm], [4629.mm,2280.mm,2.mm], [4627.mm,2280.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Processing Tray Floor"] || model.materials.add("Processing Tray Floor")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Chemistry Bath
  grp = ents.add_group
  grp.name = "Chemistry Bath"
  face = grp.entities.add_face([172.mm,82.mm,2.mm], [4627.mm,82.mm,2.mm], [4627.mm,2278.mm,2.mm], [172.mm,2278.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Chemistry Bath"] || model.materials.add("Chemistry Bath")
  mat.color = Sketchup::Color.new(46, 111, 160)
  mat.alpha = 0.4
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Processing Tray (partial)"
  inst.layer = model.layers["Processing Tray"]

  # ═══ Film-Plane Rails (left) ═══
  defn = model.definitions.add("Film-Plane Rails (left)")
  ents = defn.entities
  # Film rail left (bottom, Yd-run)
  grp = ents.add_group
  grp.name = "Film rail left (bottom, Yd-run)"
  face = grp.entities.add_face([150.mm,80.mm,150.mm], [190.mm,80.mm,150.mm], [190.mm,2280.mm,150.mm], [150.mm,2280.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Film rail left (bottom, Yd-run)"] || model.materials.add("Film rail left (bottom, Yd-run)")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Film plane left edge (ghost)
  grp = ents.add_group
  grp.name = "Film plane left edge (ghost)"
  face = grp.entities.add_face([150.mm,600.mm,150.mm], [162.mm,600.mm,150.mm], [162.mm,1762.mm,150.mm], [150.mm,1762.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2138.mm)
  mat = model.materials["Film plane left edge (ghost)"] || model.materials.add("Film plane left edge (ghost)")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 0.18
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Film-Plane Rails (left)"
  inst.layer = model.layers["Film Plane Rails"]

  # ═══ Spray Bar (at drum Yd) ═══
  defn = model.definitions.add("Spray Bar (at drum Yd)")
  ents = defn.entities
  # Spray Bar beam (40x40, Z20-60)
  grp = ents.add_group
  grp.name = "Spray Bar beam (40x40, Z20-60)"
  face = grp.entities.add_face([170.mm,1160.mm,20.mm], [4629.mm,1160.mm,20.mm], [4629.mm,1200.mm,20.mm], [170.mm,1200.mm,20.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Spray Bar beam (40x40, Z20-60)"] || model.materials.add("Spray Bar beam (40x40, Z20-60)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Spray Bar wheel (left, on rim)
  grp = ents.add_group
  grp.name = "Spray Bar wheel (left, on rim)"
  ge = grp.entities
  circle = ge.add_circle([174.mm,1150.mm,27.mm], [0,1,0], 25.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Spray Bar wheel (left, on rim)"] || model.materials.add("Spray Bar wheel (left, on rim)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray Bar wheel (right, on rim)
  grp = ents.add_group
  grp.name = "Spray Bar wheel (right, on rim)"
  ge = grp.entities
  circle = ge.add_circle([4605.mm,1150.mm,27.mm], [0,1,0], 25.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Spray Bar wheel (left, on rim)"] || model.materials.add("Spray Bar wheel (left, on rim)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Spray Bar (at drum Yd)"
  inst.layer = model.layers["Spray Bar"]

  # ═══ Cantilever Brackets ═══
  defn = model.definitions.add("Cantilever Brackets")
  ents = defn.entities
  # Cantilever 1 foot plate
  grp = ents.add_group
  grp.name = "Cantilever 1 foot plate"
  face = grp.entities.add_face([38.mm,167.mm,0.mm], [166.mm,167.mm,0.mm], [166.mm,227.mm,0.mm], [38.mm,227.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Spray Bar wheel (left, on rim)"] || model.materials.add("Spray Bar wheel (left, on rim)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever 1 post (50x50 SHS)
  grp = ents.add_group
  grp.name = "Cantilever 1 post (50x50 SHS)"
  face = grp.entities.add_face([115.mm,167.mm,0.mm], [165.mm,167.mm,0.mm], [165.mm,227.mm,0.mm], [115.mm,227.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Cantilever 1 post (50x50 SHS)"] || model.materials.add("Cantilever 1 post (50x50 SHS)")
  mat.color = Sketchup::Color.new(200, 120, 30)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever 1 arm (to X470, ~50mm deep)
  grp = ents.add_group
  grp.name = "Cantilever 1 arm (to X470, ~50mm deep)"
  face = grp.entities.add_face([165.mm,177.mm,65.mm], [470.mm,177.mm,65.mm], [470.mm,217.mm,65.mm], [165.mm,217.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Cantilever 1 post (50x50 SHS)"] || model.materials.add("Cantilever 1 post (50x50 SHS)")
  mat.color = Sketchup::Color.new(200, 120, 30)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever 2 foot plate
  grp = ents.add_group
  grp.name = "Cantilever 2 foot plate"
  face = grp.entities.add_face([38.mm,560.mm,0.mm], [166.mm,560.mm,0.mm], [166.mm,620.mm,0.mm], [38.mm,620.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Spray Bar wheel (left, on rim)"] || model.materials.add("Spray Bar wheel (left, on rim)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever 2 post (50x50 SHS)
  grp = ents.add_group
  grp.name = "Cantilever 2 post (50x50 SHS)"
  face = grp.entities.add_face([115.mm,560.mm,0.mm], [165.mm,560.mm,0.mm], [165.mm,620.mm,0.mm], [115.mm,620.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Cantilever 1 post (50x50 SHS)"] || model.materials.add("Cantilever 1 post (50x50 SHS)")
  mat.color = Sketchup::Color.new(200, 120, 30)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever 2 arm (to X470, ~50mm deep)
  grp = ents.add_group
  grp.name = "Cantilever 2 arm (to X470, ~50mm deep)"
  face = grp.entities.add_face([165.mm,570.mm,65.mm], [470.mm,570.mm,65.mm], [470.mm,610.mm,65.mm], [165.mm,610.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Cantilever 1 post (50x50 SHS)"] || model.materials.add("Cantilever 1 post (50x50 SHS)")
  mat.color = Sketchup::Color.new(200, 120, 30)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever 3 foot plate
  grp = ents.add_group
  grp.name = "Cantilever 3 foot plate"
  face = grp.entities.add_face([38.mm,954.mm,0.mm], [166.mm,954.mm,0.mm], [166.mm,1014.mm,0.mm], [38.mm,1014.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Spray Bar wheel (left, on rim)"] || model.materials.add("Spray Bar wheel (left, on rim)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever 3 post (50x50 SHS)
  grp = ents.add_group
  grp.name = "Cantilever 3 post (50x50 SHS)"
  face = grp.entities.add_face([115.mm,954.mm,0.mm], [165.mm,954.mm,0.mm], [165.mm,1014.mm,0.mm], [115.mm,1014.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Cantilever 1 post (50x50 SHS)"] || model.materials.add("Cantilever 1 post (50x50 SHS)")
  mat.color = Sketchup::Color.new(200, 120, 30)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever 3 arm (to X470, ~50mm deep)
  grp = ents.add_group
  grp.name = "Cantilever 3 arm (to X470, ~50mm deep)"
  face = grp.entities.add_face([165.mm,964.mm,65.mm], [470.mm,964.mm,65.mm], [470.mm,1004.mm,65.mm], [165.mm,1004.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Cantilever 1 post (50x50 SHS)"] || model.materials.add("Cantilever 1 post (50x50 SHS)")
  mat.color = Sketchup::Color.new(200, 120, 30)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever 4 foot plate
  grp = ents.add_group
  grp.name = "Cantilever 4 foot plate"
  face = grp.entities.add_face([38.mm,1348.mm,0.mm], [166.mm,1348.mm,0.mm], [166.mm,1408.mm,0.mm], [38.mm,1408.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Spray Bar wheel (left, on rim)"] || model.materials.add("Spray Bar wheel (left, on rim)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever 4 post (50x50 SHS)
  grp = ents.add_group
  grp.name = "Cantilever 4 post (50x50 SHS)"
  face = grp.entities.add_face([115.mm,1348.mm,0.mm], [165.mm,1348.mm,0.mm], [165.mm,1408.mm,0.mm], [115.mm,1408.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Cantilever 1 post (50x50 SHS)"] || model.materials.add("Cantilever 1 post (50x50 SHS)")
  mat.color = Sketchup::Color.new(200, 120, 30)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever 4 arm (to X470, ~50mm deep)
  grp = ents.add_group
  grp.name = "Cantilever 4 arm (to X470, ~50mm deep)"
  face = grp.entities.add_face([165.mm,1358.mm,65.mm], [470.mm,1358.mm,65.mm], [470.mm,1398.mm,65.mm], [165.mm,1398.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Cantilever 1 post (50x50 SHS)"] || model.materials.add("Cantilever 1 post (50x50 SHS)")
  mat.color = Sketchup::Color.new(200, 120, 30)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever 5 foot plate
  grp = ents.add_group
  grp.name = "Cantilever 5 foot plate"
  face = grp.entities.add_face([38.mm,1742.mm,0.mm], [166.mm,1742.mm,0.mm], [166.mm,1802.mm,0.mm], [38.mm,1802.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Spray Bar wheel (left, on rim)"] || model.materials.add("Spray Bar wheel (left, on rim)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever 5 post (50x50 SHS)
  grp = ents.add_group
  grp.name = "Cantilever 5 post (50x50 SHS)"
  face = grp.entities.add_face([115.mm,1742.mm,0.mm], [165.mm,1742.mm,0.mm], [165.mm,1802.mm,0.mm], [115.mm,1802.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Cantilever 1 post (50x50 SHS)"] || model.materials.add("Cantilever 1 post (50x50 SHS)")
  mat.color = Sketchup::Color.new(200, 120, 30)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever 5 arm (to X470, ~50mm deep)
  grp = ents.add_group
  grp.name = "Cantilever 5 arm (to X470, ~50mm deep)"
  face = grp.entities.add_face([165.mm,1752.mm,65.mm], [470.mm,1752.mm,65.mm], [470.mm,1792.mm,65.mm], [165.mm,1792.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Cantilever 1 post (50x50 SHS)"] || model.materials.add("Cantilever 1 post (50x50 SHS)")
  mat.color = Sketchup::Color.new(200, 120, 30)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever 6 foot plate
  grp = ents.add_group
  grp.name = "Cantilever 6 foot plate"
  face = grp.entities.add_face([38.mm,2135.mm,0.mm], [166.mm,2135.mm,0.mm], [166.mm,2195.mm,0.mm], [38.mm,2195.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Spray Bar wheel (left, on rim)"] || model.materials.add("Spray Bar wheel (left, on rim)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever 6 post (50x50 SHS)
  grp = ents.add_group
  grp.name = "Cantilever 6 post (50x50 SHS)"
  face = grp.entities.add_face([115.mm,2135.mm,0.mm], [165.mm,2135.mm,0.mm], [165.mm,2195.mm,0.mm], [115.mm,2195.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Cantilever 1 post (50x50 SHS)"] || model.materials.add("Cantilever 1 post (50x50 SHS)")
  mat.color = Sketchup::Color.new(200, 120, 30)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever 6 arm (to X470, ~50mm deep)
  grp = ents.add_group
  grp.name = "Cantilever 6 arm (to X470, ~50mm deep)"
  face = grp.entities.add_face([165.mm,2145.mm,65.mm], [470.mm,2145.mm,65.mm], [470.mm,2185.mm,65.mm], [165.mm,2185.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Cantilever 1 post (50x50 SHS)"] || model.materials.add("Cantilever 1 post (50x50 SHS)")
  mat.color = Sketchup::Color.new(200, 120, 30)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Cantilever Brackets"
  inst.layer = model.layers["Cantilevers"]

  # ═══ Grate (lift-out) ═══
  defn = model.definitions.add("Grate (lift-out)")
  ents = defn.entities
  # Walkway Left (removable)
  grp = ents.add_group
  grp.name = "Walkway Left (removable)"
  face = grp.entities.add_face([170.mm,0.mm,115.mm], [470.mm,0.mm,115.mm], [470.mm,2362.mm,115.mm], [170.mm,2362.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Left (removable)"] || model.materials.add("Walkway Left (removable)")
  mat.color = Sketchup::Color.new(192, 96, 0)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Left punch-out (cantilevered)
  grp = ents.add_group
  grp.name = "Walkway Left punch-out (cantilevered)"
  face = grp.entities.add_face([470.mm,800.mm,115.mm], [770.mm,800.mm,115.mm], [770.mm,1560.mm,115.mm], [470.mm,1560.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Left (removable)"] || model.materials.add("Walkway Left (removable)")
  mat.color = Sketchup::Color.new(192, 96, 0)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Grate (lift-out)"
  inst.layer = model.layers["Grate (lift-out)"]

  # ═══ Hinge Panel (transport) ═══
  defn = model.definitions.add("Hinge Panel (transport)")
  ents = defn.entities
  # Panel corner near (40mm)
  grp = ents.add_group
  grp.name = "Panel corner near (40mm)"
  face = grp.entities.add_face([880.mm,0.mm,130.mm], [920.mm,0.mm,130.mm], [920.mm,653.mm,130.mm], [880.mm,653.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2220.mm)
  mat = model.materials["Panel corner near (40mm)"] || model.materials.add("Panel corner near (40mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Panel centre (120mm)
  grp = ents.add_group
  grp.name = "Panel centre (120mm)"
  face = grp.entities.add_face([880.mm,653.mm,130.mm], [1000.mm,653.mm,130.mm], [1000.mm,1709.mm,130.mm], [880.mm,1709.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2220.mm)
  mat = model.materials["Panel corner near (40mm)"] || model.materials.add("Panel corner near (40mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Panel corner far (40mm)
  grp = ents.add_group
  grp.name = "Panel corner far (40mm)"
  face = grp.entities.add_face([880.mm,1709.mm,130.mm], [920.mm,1709.mm,130.mm], [920.mm,2362.mm,130.mm], [880.mm,2362.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2220.mm)
  mat = model.materials["Panel corner near (40mm)"] || model.materials.add("Panel corner near (40mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Panel swept path (clearance band)
  grp = ents.add_group
  grp.name = "Panel swept path (clearance band)"
  face = grp.entities.add_face([0.mm,0.mm,130.mm], [1000.mm,0.mm,130.mm], [1000.mm,2362.mm,130.mm], [0.mm,2362.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Panel swept path (clearance band)"] || model.materials.add("Panel swept path (clearance band)")
  mat.color = Sketchup::Color.new(48, 112, 192)
  mat.alpha = 0.12
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Hinge Panel (transport)"
  inst.layer = model.layers["Hinge Panel (transport)"]

  # ═══ Light-trap Drum (lifted) ═══
  defn = model.definitions.add("Light-trap Drum (lifted)")
  ents = defn.entities
  # Light-trap drum (lifted +50mm)
  grp = ents.add_group
  grp.name = "Light-trap drum (lifted +50mm)"
  ge = grp.entities
  circle = ge.add_circle([-400.mm,1181.mm,130.mm], [0,0,1], 450.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2120.mm)
  mat = model.materials["Light-trap drum (lifted +50mm)"] || model.materials.add("Light-trap drum (lifted +50mm)")
  mat.color = Sketchup::Color.new(232, 224, 208)
  mat.alpha = 0.3
  grp.material = mat

  # Drum base disc
  grp = ents.add_group
  grp.name = "Drum base disc"
  ge = grp.entities
  circle = ge.add_circle([-400.mm,1181.mm,130.mm], [0,0,1], 450.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Spray Bar wheel (left, on rim)"] || model.materials.add("Spray Bar wheel (left, on rim)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Light-trap Drum (lifted)"
  inst.layer = model.layers["Light-trap Drum"]


# ── Labels (Labels tag; visible only in "Labeled") ──
anc = Geom::Point3d.new(140.mm, 197.mm, 115.mm)
txt = entities.add_text("FLOOR-LEG CANTILEVER
bolted to bare floor (X<170,
outside tray) — replaces edge beam", anc, Geom::Vector3d.new(-700.mm, -700.mm, 500.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(470.mm, 984.mm, 65.mm)
txt = entities.add_text("ARM now ~50mm deep (was 13)
bottom Z65 clears spray bar (Z60)", anc, Geom::Vector3d.new(520.mm, -650.mm, 320.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(770.mm, 1180.mm, 115.mm)
txt = entities.add_text("PUNCH-OUT cantilevers 300mm;
grate underside Z115 now clears
spray bar (Z60) by 55mm", anc, Geom::Vector3d.new(650.mm, -300.mm, 450.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(470.mm, 1180.mm, 60.mm)
txt = entities.add_text("SPRAY BAR fixed at Z20-60
(does NOT rise) — gap opens up", anc, Geom::Vector3d.new(-300.mm, 600.mm, -250.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1000.mm, 1180.mm, 130.mm)
txt = entities.add_text("PANEL lifted +50mm (rides Z130)
still clears brackets by 15mm", anc, Geom::Vector3d.new(500.mm, -500.mm, 700.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(-400.mm, 1181.mm, 2250.mm)
txt = entities.add_text("DRUM LIFTED +50mm -> top Z2250
interior height PRESERVED;
138mm spare to aperture top", anc, Geom::Vector3d.new(-300.mm, -250.mm, 250.mm))
txt.layer = model.layers["Labels"] rescue nil

model.definitions.purge_unused
model.materials.purge_unused

keep_tags = ["Context", "Processing Tray", "Film Plane Rails", "Spray Bar", "Cantilevers", "Grate (lift-out)", "Hinge Panel (transport)", "Light-trap Drum", "Labels"]
default_layer = model.layers[0]
model.layers.to_a.each { |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}

# ── Scenes — shared iso camera framed on the CARGO-DOOR END (the study focus). The
# tray + spray bar now run the full length toward the IBC end, so a bounds/zoom_extents
# camera would shrink the detail; use a fixed cargo-door-end framing instead. ──
model.layers.each { |l| l.visible = (l.name != "Labels") }
ctr = Geom::Point3d.new(700.mm, 1100.mm, 500.mm)
dir = Geom::Vector3d.new(0.58, -0.80, 0.48); dir.normalize!
eye = ctr.offset(dir, 4600.mm)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)

[["Operating", ["Processing Tray", "Film Plane Rails", "Spray Bar", "Cantilevers", "Grate (lift-out)"]], ["Transport clearance", ["Processing Tray", "Film Plane Rails", "Cantilevers", "Hinge Panel (transport)", "Light-trap Drum"]], ["Spray-bar clearance", ["Processing Tray", "Spray Bar", "Cantilevers", "Grate (lift-out)"]], ["Drum lift", ["Processing Tray", "Cantilevers", "Hinge Panel (transport)", "Light-trap Drum"]], ["Combined", ["Context", "Processing Tray", "Film Plane Rails", "Spray Bar", "Cantilevers", "Grate (lift-out)", "Hinge Panel (transport)", "Light-trap Drum"]], ["Labeled", ["Context", "Processing Tray", "Film Plane Rails", "Spray Bar", "Cantilevers", "Grate (lift-out)", "Hinge Panel (transport)", "Light-trap Drum", "Labels"]]].each { |name, tags|
  model.layers.each { |l| l.visible = (l == default_layer || l.name == "Context" || tags.include?(l.name)) }
  page = model.pages.add(name)
  page.use_camera = true
}
model.layers.each { |l| l.visible = true }

model.commit_operation
{ success: true, model: "Cantilever Study",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
