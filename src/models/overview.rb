model = Sketchup.active_model
model.start_operation("TBS-001 Overview", true)
entities = model.active_entities

# Display in millimeters (LengthUnit 2 = mm, LengthFormat 0 = decimal).
# SketchUp stores geometry in inches internally; this only sets the UI readout.
opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# ── Idempotent rebuild: erase prior generated instances (keep 'Sree'), then
# purge their now-unused definitions so names don't collide on re-add.
to_erase = entities.to_a.select { |e|
  (e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance)) &&
  !(e.is_a?(Sketchup::ComponentInstance) && e.definition.name == "Sree")
}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each { |p| model.pages.erase(p) }

# ── Tags (layers) ──
  model.layers.add("Shell") unless model.layers["Shell"]
  model.layers.add("Walkways") unless model.layers["Walkways"]
  model.layers.add("Processing Tray") unless model.layers["Processing Tray"]
  model.layers.add("Pinhole") unless model.layers["Pinhole"]
  model.layers.add("Optical Cone") unless model.layers["Optical Cone"]
  model.layers.add("Film Plane") unless model.layers["Film Plane"]
  model.layers.add("Ceiling Rail") unless model.layers["Ceiling Rail"]
  model.layers.add("Spray Bar") unless model.layers["Spray Bar"]
  model.layers.add("Equipment Panel") unless model.layers["Equipment Panel"]
  model.layers.add("IBC Stack") unless model.layers["IBC Stack"]
  model.layers.add("IBC Rack") unless model.layers["IBC Rack"]
  model.layers.add("Light Trap") unless model.layers["Light Trap"]
  model.layers.add("Electrical") unless model.layers["Electrical"]
  model.layers.add("Shelf") unless model.layers["Shelf"]
  model.layers.add("Light Seal") unless model.layers["Light Seal"]
  model.layers.add("Lighting") unless model.layers["Lighting"]
  model.layers.add("Evap Cooler") unless model.layers["Evap Cooler"]
  model.layers.add("Water Hookups") unless model.layers["Water Hookups"]
  model.layers.add("Fans") unless model.layers["Fans"]
  model.layers.add("Water Plumbing") unless model.layers["Water Plumbing"]

# Dashed line style for the optical cone wireframe (guidance, not a solid).
begin
  ds = model.line_styles["Dash"] || model.line_styles["Dot"]
  model.layers["Optical Cone"].line_style = ds if ds
rescue StandardError
end

# ── Subsystems (each a component on its tag) ──
  # ═══ Container Shell ═══
  defn = model.definitions.add("Container Shell")
  ents = defn.entities
  # Container Floor
  grp = ents.add_group
  grp.name = "Container Floor"
  face = grp.entities.add_face([0.mm,0.mm,-40.mm], [5893.mm,0.mm,-40.mm], [5893.mm,2362.mm,-40.mm], [0.mm,2362.mm,-40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Container Floor"] || model.materials.add("Container Floor")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 1.0
  grp.material = mat
  grp.entities.grep(Sketchup::Face).each { |f| f.material = mat; f.back_material = mat }

  # Container Ceiling
  grp = ents.add_group
  grp.name = "Container Ceiling"
  face = grp.entities.add_face([0.mm,0.mm,2388.mm], [5893.mm,0.mm,2388.mm], [5893.mm,2362.mm,2388.mm], [0.mm,2362.mm,2388.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Container Ceiling"] || model.materials.add("Container Ceiling")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.2
  grp.material = mat
  grp.entities.grep(Sketchup::Face).each { |f| f.material = mat; f.back_material = mat }

  # Pinhole Wall (Yd=0)
  grp = ents.add_group
  grp.name = "Pinhole Wall (Yd=0)"
  face = grp.entities.add_face([0.mm,-40.mm,0.mm], [5893.mm,-40.mm,0.mm], [5893.mm,0.mm,0.mm], [0.mm,0.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Container Ceiling"] || model.materials.add("Container Ceiling")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.2
  grp.material = mat
  grp.entities.grep(Sketchup::Face).each { |f| f.material = mat; f.back_material = mat }

  # Film Plane Wall (Yd=max)
  grp = ents.add_group
  grp.name = "Film Plane Wall (Yd=max)"
  face = grp.entities.add_face([0.mm,2362.mm,0.mm], [5893.mm,2362.mm,0.mm], [5893.mm,2402.mm,0.mm], [0.mm,2402.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Container Ceiling"] || model.materials.add("Container Ceiling")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.2
  grp.material = mat
  grp.entities.grep(Sketchup::Face).each { |f| f.material = mat; f.back_material = mat }

  # Far End Wall (IBC end)
  grp = ents.add_group
  grp.name = "Far End Wall (IBC end)"
  face = grp.entities.add_face([5893.mm,0.mm,0.mm], [5933.mm,0.mm,0.mm], [5933.mm,2362.mm,0.mm], [5893.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Container Ceiling"] || model.materials.add("Container Ceiling")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.2
  grp.material = mat
  grp.entities.grep(Sketchup::Face).each { |f| f.material = mat; f.back_material = mat }

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Container Shell"
  inst.layer = model.layers["Shell"]

  # ═══ Walkways ═══
  defn = model.definitions.add("Walkways")
  ents = defn.entities
  # Walkway Near (left section)
  grp = ents.add_group
  grp.name = "Walkway Near (left section)"
  face = grp.entities.add_face([470.mm,0.mm,65.mm], [1155.mm,0.mm,65.mm], [1155.mm,300.mm,65.mm], [470.mm,300.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near (widened)
  grp = ents.add_group
  grp.name = "Walkway Near (widened)"
  face = grp.entities.add_face([1155.mm,0.mm,65.mm], [2629.mm,0.mm,65.mm], [2629.mm,500.mm,65.mm], [1155.mm,500.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near (right section)
  grp = ents.add_group
  grp.name = "Walkway Near (right section)"
  face = grp.entities.add_face([2629.mm,0.mm,65.mm], [4329.mm,0.mm,65.mm], [4329.mm,300.mm,65.mm], [2629.mm,300.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far
  grp = ents.add_group
  grp.name = "Walkway Far"
  face = grp.entities.add_face([470.mm,2062.mm,65.mm], [4329.mm,2062.mm,65.mm], [4329.mm,2362.mm,65.mm], [470.mm,2362.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Right (IBC end)
  grp = ents.add_group
  grp.name = "Walkway Right (IBC end)"
  face = grp.entities.add_face([4329.mm,0.mm,65.mm], [4629.mm,0.mm,65.mm], [4629.mm,2362.mm,65.mm], [4329.mm,2362.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Left (REMOVABLE — transport)
  grp = ents.add_group
  grp.name = "Walkway Left (REMOVABLE — transport)"
  face = grp.entities.add_face([170.mm,0.mm,65.mm], [470.mm,0.mm,65.mm], [470.mm,2362.mm,65.mm], [170.mm,2362.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Left (REMOVABLE — transport)"] || model.materials.add("Walkway Left (REMOVABLE — transport)")
  mat.color = Sketchup::Color.new(192, 96, 0)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Walkways"
  inst.layer = model.layers["Walkways"]

  # ═══ Processing Tray ═══
  defn = model.definitions.add("Processing Tray")
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
  mat.alpha = 0.45
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Processing Tray"
  inst.layer = model.layers["Processing Tray"]

  # ═══ Pinhole Assembly ═══
  defn = model.definitions.add("Pinhole Assembly")
  ents = defn.entities
  # Pinhole Mount Plate
  grp = ents.add_group
  grp.name = "Pinhole Mount Plate"
  face = grp.entities.add_face([2349.mm,0.mm,1144.mm], [2449.mm,0.mm,1144.mm], [2449.mm,3.mm,1144.mm], [2349.mm,3.mm,1144.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Pinhole Aperture (Ø2.17)
  grp = ents.add_group
  grp.name = "Pinhole Aperture (Ø2.17)"
  face = grp.entities.add_face([2397.915.mm,3.mm,1192.915.mm], [2400.085.mm,3.mm,1192.915.mm], [2400.085.mm,4.mm,1192.915.mm], [2397.915.mm,4.mm,1192.915.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.17.mm)
  mat = model.materials["Pinhole Aperture (Ø2.17)"] || model.materials.add("Pinhole Aperture (Ø2.17)")
  mat.color = Sketchup::Color.new(204, 102, 0)
  mat.alpha = 1.0
  grp.material = mat

  # TS Base Plate (wall mount)
  grp = ents.add_group
  grp.name = "TS Base Plate (wall mount)"
  face = grp.entities.add_face([2229.mm,-52.mm,1024.mm], [2569.mm,-52.mm,1024.mm], [2569.mm,-40.mm,1024.mm], [2229.mm,-40.mm,1024.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(340.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Pinhole Tilt-Swing Board
  grp = ents.add_group
  grp.name = "Pinhole Tilt-Swing Board"
  face = grp.entities.add_face([2259.mm,-80.mm,1054.mm], [2539.mm,-80.mm,1054.mm], [2539.mm,-64.mm,1054.mm], [2259.mm,-64.mm,1054.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(280.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # TS Tilt Knob
  grp = ents.add_group
  grp.name = "TS Tilt Knob"
  face = grp.entities.add_face([2384.mm,-100.mm,1029.mm], [2414.mm,-100.mm,1029.mm], [2414.mm,-75.mm,1029.mm], [2384.mm,-75.mm,1029.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # TS Swing Knob
  grp = ents.add_group
  grp.name = "TS Swing Knob"
  face = grp.entities.add_face([2539.mm,-100.mm,1179.mm], [2564.mm,-100.mm,1179.mm], [2564.mm,-75.mm,1179.mm], [2539.mm,-75.mm,1179.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Pinhole Assembly"
  inst.layer = model.layers["Pinhole"]

  # ═══ Optical Cone ═══
  defn = model.definitions.add("Optical Cone")
  ents = defn.entities
  # Optical Cone
  grp = ents.add_group
  grp.name = "Optical Cone"
  ge = grp.entities
  apex = [2399.mm,0.mm,1194.mm]
  b0 = [150.mm,2262.mm,0.mm]; b1 = [4649.mm,2262.mm,0.mm]; b2 = [4649.mm,2262.mm,2388.mm]; b3 = [150.mm,2262.mm,2388.mm]
  edges = []
  edges.concat(ge.add_edges(b0, b1, b2, b3, b0))
  edges << ge.add_line(apex, b0)
  edges << ge.add_line(apex, b1)
  edges << ge.add_line(apex, b2)
  edges << ge.add_line(apex, b3)
  lyr = model.layers["Optical Cone"]
  edges.each { |e| e.layer = lyr if e.is_a?(Sketchup::Edge) }

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Optical Cone"
  inst.layer = model.layers["Optical Cone"]

  # ═══ Film Plane Mechanism ═══
  defn = model.definitions.add("Film Plane Mechanism")
  ents = defn.entities
  # FP Rail BR
  grp = ents.add_group
  grp.name = "FP Rail BR"
  face = grp.entities.add_face([4609.mm,100.mm,100.mm], [4649.mm,100.mm,100.mm], [4649.mm,2300.mm,100.mm], [4609.mm,2300.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Rail TR
  grp = ents.add_group
  grp.name = "FP Rail TR"
  face = grp.entities.add_face([4609.mm,100.mm,2248.mm], [4649.mm,100.mm,2248.mm], [4649.mm,2300.mm,2248.mm], [4609.mm,2300.mm,2248.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Rail BL (fixed near)
  grp = ents.add_group
  grp.name = "FP Rail BL (fixed near)"
  face = grp.entities.add_face([150.mm,100.mm,100.mm], [190.mm,100.mm,100.mm], [190.mm,806.mm,100.mm], [150.mm,806.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Rail BL (DEMOUNTABLE — drum mode)
  grp = ents.add_group
  grp.name = "FP Rail BL (DEMOUNTABLE — drum mode)"
  face = grp.entities.add_face([150.mm,806.mm,100.mm], [190.mm,806.mm,100.mm], [190.mm,1556.mm,100.mm], [150.mm,1556.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["FP Rail BL (DEMOUNTABLE — drum mode)"] || model.materials.add("FP Rail BL (DEMOUNTABLE — drum mode)")
  mat.color = Sketchup::Color.new(224, 144, 42)
  mat.alpha = 1.0
  grp.material = mat

  # FP Rail BL (fixed far)
  grp = ents.add_group
  grp.name = "FP Rail BL (fixed far)"
  face = grp.entities.add_face([150.mm,1556.mm,100.mm], [190.mm,1556.mm,100.mm], [190.mm,2300.mm,100.mm], [150.mm,2300.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Rail TL (fixed near)
  grp = ents.add_group
  grp.name = "FP Rail TL (fixed near)"
  face = grp.entities.add_face([150.mm,100.mm,2248.mm], [190.mm,100.mm,2248.mm], [190.mm,806.mm,2248.mm], [150.mm,806.mm,2248.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Rail TL (DEMOUNTABLE — drum mode)
  grp = ents.add_group
  grp.name = "FP Rail TL (DEMOUNTABLE — drum mode)"
  face = grp.entities.add_face([150.mm,806.mm,2248.mm], [190.mm,806.mm,2248.mm], [190.mm,1556.mm,2248.mm], [150.mm,1556.mm,2248.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["FP Rail BL (DEMOUNTABLE — drum mode)"] || model.materials.add("FP Rail BL (DEMOUNTABLE — drum mode)")
  mat.color = Sketchup::Color.new(224, 144, 42)
  mat.alpha = 1.0
  grp.material = mat

  # FP Rail TL (fixed far)
  grp = ents.add_group
  grp.name = "FP Rail TL (fixed far)"
  face = grp.entities.add_face([150.mm,1556.mm,2248.mm], [190.mm,1556.mm,2248.mm], [190.mm,2300.mm,2248.mm], [150.mm,2300.mm,2248.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Brace Vert L (pinhole)
  grp = ents.add_group
  grp.name = "FP Brace Vert L (pinhole)"
  face = grp.entities.add_face([150.mm,100.mm,100.mm], [200.mm,100.mm,100.mm], [200.mm,150.mm,100.mm], [150.mm,150.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2188.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Brace Vert R (pinhole)
  grp = ents.add_group
  grp.name = "FP Brace Vert R (pinhole)"
  face = grp.entities.add_face([4599.mm,100.mm,100.mm], [4649.mm,100.mm,100.mm], [4649.mm,150.mm,100.mm], [4599.mm,150.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2188.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Brace Beam Bottom (pinhole)
  grp = ents.add_group
  grp.name = "FP Brace Beam Bottom (pinhole)"
  face = grp.entities.add_face([150.mm,100.mm,100.mm], [4649.mm,100.mm,100.mm], [4649.mm,150.mm,100.mm], [150.mm,150.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Brace Beam Top (pinhole)
  grp = ents.add_group
  grp.name = "FP Brace Beam Top (pinhole)"
  face = grp.entities.add_face([150.mm,100.mm,2238.mm], [4649.mm,100.mm,2238.mm], [4649.mm,150.mm,2238.mm], [150.mm,150.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Brace Vert L (film)
  grp = ents.add_group
  grp.name = "FP Brace Vert L (film)"
  face = grp.entities.add_face([150.mm,2262.mm,100.mm], [200.mm,2262.mm,100.mm], [200.mm,2312.mm,100.mm], [150.mm,2312.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2188.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Brace Vert R (film)
  grp = ents.add_group
  grp.name = "FP Brace Vert R (film)"
  face = grp.entities.add_face([4599.mm,2262.mm,100.mm], [4649.mm,2262.mm,100.mm], [4649.mm,2312.mm,100.mm], [4599.mm,2312.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2188.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Brace Beam Bottom (film)
  grp = ents.add_group
  grp.name = "FP Brace Beam Bottom (film)"
  face = grp.entities.add_face([150.mm,2262.mm,100.mm], [4649.mm,2262.mm,100.mm], [4649.mm,2312.mm,100.mm], [150.mm,2312.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Brace Beam Top (film)
  grp = ents.add_group
  grp.name = "FP Brace Beam Top (film)"
  face = grp.entities.add_face([150.mm,2262.mm,2238.mm], [4649.mm,2262.mm,2238.mm], [4649.mm,2312.mm,2238.mm], [150.mm,2312.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Film Plane Screen (muslin)
  grp = ents.add_group
  grp.name = "Film Plane Screen (muslin)"
  face = grp.entities.add_face([150.mm,2262.mm,0.mm], [4649.mm,2262.mm,0.mm], [4649.mm,2282.mm,0.mm], [150.mm,2282.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Film Plane Screen (muslin)"] || model.materials.add("Film Plane Screen (muslin)")
  mat.color = Sketchup::Color.new(32, 96, 160)
  mat.alpha = 0.3
  grp.material = mat

  # FP Frame Bottom
  grp = ents.add_group
  grp.name = "FP Frame Bottom"
  face = grp.entities.add_face([150.mm,2211.2.mm,0.mm], [4649.mm,2211.2.mm,0.mm], [4649.mm,2262.mm,0.mm], [150.mm,2262.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Frame Top
  grp = ents.add_group
  grp.name = "FP Frame Top"
  face = grp.entities.add_face([150.mm,2211.2.mm,2337.2.mm], [4649.mm,2211.2.mm,2337.2.mm], [4649.mm,2262.mm,2337.2.mm], [150.mm,2262.mm,2337.2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Frame Left
  grp = ents.add_group
  grp.name = "FP Frame Left"
  face = grp.entities.add_face([150.mm,2211.2.mm,0.mm], [200.8.mm,2211.2.mm,0.mm], [200.8.mm,2262.mm,0.mm], [150.mm,2262.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Frame Right
  grp = ents.add_group
  grp.name = "FP Frame Right"
  face = grp.entities.add_face([4598.2.mm,2211.2.mm,0.mm], [4649.mm,2211.2.mm,0.mm], [4649.mm,2262.mm,0.mm], [4598.2.mm,2262.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Film Plane Mechanism"
  inst.layer = model.layers["Film Plane"]

  # ═══ Ceiling Rail ═══
  defn = model.definitions.add("Ceiling Rail")
  ents = defn.entities
  # HGR20 Rail L
  grp = ents.add_group
  grp.name = "HGR20 Rail L"
  face = grp.entities.add_face([-30.mm,746.mm,2358.mm], [480.mm,746.mm,2358.mm], [480.mm,766.mm,2358.mm], [-30.mm,766.mm,2358.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["HGR20 Rail L"] || model.materials.add("HGR20 Rail L")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage L (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage L (HGH20CA)"
  face = grp.entities.add_face([38.mm,734.mm,2330.mm], [82.mm,734.mm,2330.mm], [82.mm,778.mm,2330.mm], [38.mm,778.mm,2330.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Carriage L (HGH20CA)"] || model.materials.add("Carriage L (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Suspension Bracket L
  grp = ents.add_group
  grp.name = "Suspension Bracket L"
  face = grp.entities.add_face([30.mm,736.mm,2290.mm], [90.mm,736.mm,2290.mm], [90.mm,776.mm,2290.mm], [30.mm,776.mm,2290.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # HGR20 Rail R
  grp = ents.add_group
  grp.name = "HGR20 Rail R"
  face = grp.entities.add_face([-30.mm,1596.mm,2358.mm], [480.mm,1596.mm,2358.mm], [480.mm,1616.mm,2358.mm], [-30.mm,1616.mm,2358.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["HGR20 Rail L"] || model.materials.add("HGR20 Rail L")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage R (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage R (HGH20CA)"
  face = grp.entities.add_face([38.mm,1584.mm,2330.mm], [82.mm,1584.mm,2330.mm], [82.mm,1628.mm,2330.mm], [38.mm,1628.mm,2330.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Carriage L (HGH20CA)"] || model.materials.add("Carriage L (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Suspension Bracket R
  grp = ents.add_group
  grp.name = "Suspension Bracket R"
  face = grp.entities.add_face([30.mm,1586.mm,2290.mm], [90.mm,1586.mm,2290.mm], [90.mm,1626.mm,2290.mm], [30.mm,1626.mm,2290.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cargo Door Panel
  grp = ents.add_group
  grp.name = "Cargo Door Panel"
  face = grp.entities.add_face([0.mm,0.mm,80.mm], [120.mm,0.mm,80.mm], [120.mm,2362.mm,80.mm], [0.mm,2362.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2210.mm)
  mat = model.materials["Cargo Door Panel"] || model.materials.add("Cargo Door Panel")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.6
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Ceiling Rail"
  inst.layer = model.layers["Ceiling Rail"]

  # ═══ Spray Bar ═══
  defn = model.definitions.add("Spray Bar")
  ents = defn.entities
  # Spray Bar Beam
  grp = ents.add_group
  grp.name = "Spray Bar Beam"
  face = grp.entities.add_face([200.mm,1160.mm,20.mm], [4599.mm,1160.mm,20.mm], [4599.mm,1200.mm,20.mm], [200.mm,1200.mm,20.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Spray Bar Carriage
  grp = ents.add_group
  grp.name = "Spray Bar Carriage"
  face = grp.entities.add_face([200.mm,1135.mm,15.mm], [250.mm,1135.mm,15.mm], [250.mm,1225.mm,15.mm], [200.mm,1225.mm,15.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(55.mm)
  mat = model.materials["Carriage L (HGH20CA)"] || model.materials.add("Carriage L (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Spray Bar Carriage
  grp = ents.add_group
  grp.name = "Spray Bar Carriage"
  face = grp.entities.add_face([4549.mm,1135.mm,15.mm], [4599.mm,1135.mm,15.mm], [4599.mm,1225.mm,15.mm], [4549.mm,1225.mm,15.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(55.mm)
  mat = model.materials["Carriage L (HGH20CA)"] || model.materials.add("Carriage L (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Spray Bar"
  inst.layer = model.layers["Spray Bar"]

  # ═══ Equipment Panel ═══
  defn = model.definitions.add("Equipment Panel")
  ents = defn.entities
  # Equipment Panel (ply)
  grp = ents.add_group
  grp.name = "Equipment Panel (ply)"
  face = grp.entities.add_face([5240.mm,1046.mm,200.mm], [5258.mm,1046.mm,200.mm], [5258.mm,1316.mm,200.mm], [5240.mm,1316.mm,200.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2060.mm)
  mat = model.materials["Equipment Panel (ply)"] || model.materials.add("Equipment Panel (ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-01 (Blue)
  grp = ents.add_group
  grp.name = "Pump P-01 (Blue)"
  face = grp.entities.add_face([5140.mm,1045.5.mm,1320.mm], [5240.mm,1045.5.mm,1320.mm], [5240.mm,1172.5.mm,1320.mm], [5140.mm,1172.5.mm,1320.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-02 (Brown)
  grp = ents.add_group
  grp.name = "Pump P-02 (Brown)"
  face = grp.entities.add_face([5140.mm,1189.5.mm,1320.mm], [5240.mm,1189.5.mm,1320.mm], [5240.mm,1316.5.mm,1320.mm], [5140.mm,1316.5.mm,1320.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-04 (Tray drain)
  grp = ents.add_group
  grp.name = "Pump P-04 (Tray drain)"
  face = grp.entities.add_face([5140.mm,1045.5.mm,1578.mm], [5240.mm,1045.5.mm,1578.mm], [5240.mm,1172.5.mm,1578.mm], [5140.mm,1172.5.mm,1578.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-03 (Waste evac)
  grp = ents.add_group
  grp.name = "Pump P-03 (Waste evac)"
  face = grp.entities.add_face([5140.mm,1189.5.mm,1578.mm], [5240.mm,1189.5.mm,1578.mm], [5240.mm,1316.5.mm,1578.mm], [5140.mm,1316.5.mm,1578.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-05 (Brown drain)
  grp = ents.add_group
  grp.name = "Pump P-05 (Brown drain)"
  face = grp.entities.add_face([5140.mm,1189.5.mm,1946.mm], [5240.mm,1189.5.mm,1946.mm], [5240.mm,1316.5.mm,1946.mm], [5140.mm,1316.5.mm,1946.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # ACC-01 Accumulator
  grp = ents.add_group
  grp.name = "ACC-01 Accumulator"
  ge = grp.entities
  circle = ge.add_circle([5177.mm,1109.mm,1946.mm], [0,0,1], 63.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(150.mm)
  mat = model.materials["ACC-01 Accumulator"] || model.materials.add("ACC-01 Accumulator")
  mat.color = Sketchup::Color.new(90, 154, 204)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F1 (50µ)
  grp = ents.add_group
  grp.name = "Filter F1 (50µ)"
  ge = grp.entities
  circle = ge.add_circle([5175.mm,1181.mm,200.mm], [0,0,1], 65.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(340.mm)
  mat = model.materials["Filter F1 (50µ)"] || model.materials.add("Filter F1 (50µ)")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F2 (5µ)
  grp = ents.add_group
  grp.name = "Filter F2 (5µ)"
  ge = grp.entities
  circle = ge.add_circle([5175.mm,1181.mm,570.mm], [0,0,1], 65.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(340.mm)
  mat = model.materials["Filter F1 (50µ)"] || model.materials.add("Filter F1 (50µ)")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F3 (GAC)
  grp = ents.add_group
  grp.name = "Filter F3 (GAC)"
  ge = grp.entities
  circle = ge.add_circle([5175.mm,1181.mm,940.mm], [0,0,1], 65.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(340.mm)
  mat = model.materials["Filter F1 (50µ)"] || model.materials.add("Filter F1 (50µ)")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Equipment Panel"
  inst.layer = model.layers["Equipment Panel"]

  # ═══ IBC Stack ═══
  defn = model.definitions.add("IBC Stack")
  ents = defn.entities
  # IBC Brown (developer) pallet
  grp = ents.add_group
  grp.name = "IBC Brown (developer) pallet"
  face = grp.entities.add_face([4674.mm,30.mm,0.mm], [5893.mm,30.mm,0.mm], [5893.mm,1046.mm,0.mm], [4674.mm,1046.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(168.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Brown (developer) bottle
  grp = ents.add_group
  grp.name = "IBC Brown (developer) bottle"
  face = grp.entities.add_face([4704.mm,60.mm,168.mm], [5863.mm,60.mm,168.mm], [5863.mm,1016.mm,168.mm], [4704.mm,1016.mm,168.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(822.mm)
  mat = model.materials["IBC Brown (developer) bottle"] || model.materials.add("IBC Brown (developer) bottle")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 0.55
  grp.material = mat

  # IBC Blue #1 pallet
  grp = ents.add_group
  grp.name = "IBC Blue #1 pallet"
  face = grp.entities.add_face([4674.mm,30.mm,1010.mm], [5893.mm,30.mm,1010.mm], [5893.mm,1046.mm,1010.mm], [4674.mm,1046.mm,1010.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(168.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Blue #1 bottle
  grp = ents.add_group
  grp.name = "IBC Blue #1 bottle"
  face = grp.entities.add_face([4704.mm,60.mm,1178.mm], [5863.mm,60.mm,1178.mm], [5863.mm,1016.mm,1178.mm], [4704.mm,1016.mm,1178.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(822.mm)
  mat = model.materials["IBC Blue #1 bottle"] || model.materials.add("IBC Blue #1 bottle")
  mat.color = Sketchup::Color.new(46, 109, 180)
  mat.alpha = 0.55
  grp.material = mat

  # IBC Waste pallet
  grp = ents.add_group
  grp.name = "IBC Waste pallet"
  face = grp.entities.add_face([4674.mm,1316.mm,0.mm], [5893.mm,1316.mm,0.mm], [5893.mm,2332.mm,0.mm], [4674.mm,2332.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(168.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Waste bottle
  grp = ents.add_group
  grp.name = "IBC Waste bottle"
  face = grp.entities.add_face([4704.mm,1346.mm,168.mm], [5863.mm,1346.mm,168.mm], [5863.mm,2302.mm,168.mm], [4704.mm,2302.mm,168.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(822.mm)
  mat = model.materials["IBC Waste bottle"] || model.materials.add("IBC Waste bottle")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 0.55
  grp.material = mat

  # IBC Blue #2 pallet
  grp = ents.add_group
  grp.name = "IBC Blue #2 pallet"
  face = grp.entities.add_face([4674.mm,1316.mm,1010.mm], [5893.mm,1316.mm,1010.mm], [5893.mm,2332.mm,1010.mm], [4674.mm,2332.mm,1010.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(168.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Blue #2 bottle
  grp = ents.add_group
  grp.name = "IBC Blue #2 bottle"
  face = grp.entities.add_face([4704.mm,1346.mm,1178.mm], [5863.mm,1346.mm,1178.mm], [5863.mm,2302.mm,1178.mm], [4704.mm,2302.mm,1178.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(822.mm)
  mat = model.materials["IBC Blue #1 bottle"] || model.materials.add("IBC Blue #1 bottle")
  mat.color = Sketchup::Color.new(46, 109, 180)
  mat.alpha = 0.55
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "IBC Stack"
  inst.layer = model.layers["IBC Stack"]

  # ═══ IBC Rack ═══
  defn = model.definitions.add("IBC Rack")
  ents = defn.entities
  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([4734.mm,1046.mm,0.mm], [4784.mm,1046.mm,0.mm], [4784.mm,1096.mm,0.mm], [4734.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([4734.mm,1266.mm,0.mm], [4784.mm,1266.mm,0.mm], [4784.mm,1316.mm,0.mm], [4734.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([5258.5.mm,1046.mm,0.mm], [5308.5.mm,1046.mm,0.mm], [5308.5.mm,1096.mm,0.mm], [5258.5.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([5258.5.mm,1266.mm,0.mm], [5308.5.mm,1266.mm,0.mm], [5308.5.mm,1316.mm,0.mm], [5258.5.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([5783.mm,1046.mm,0.mm], [5833.mm,1046.mm,0.mm], [5833.mm,1096.mm,0.mm], [5783.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([5783.mm,1266.mm,0.mm], [5833.mm,1266.mm,0.mm], [5833.mm,1316.mm,0.mm], [5783.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Spine
  grp = ents.add_group
  grp.name = "Rack Spine"
  face = grp.entities.add_face([4734.mm,1046.mm,960.mm], [5833.mm,1046.mm,960.mm], [5833.mm,1096.mm,960.mm], [4734.mm,1096.mm,960.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Spine
  grp = ents.add_group
  grp.name = "Rack Spine"
  face = grp.entities.add_face([4734.mm,1266.mm,960.mm], [5833.mm,1266.mm,960.mm], [5833.mm,1316.mm,960.mm], [4734.mm,1316.mm,960.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Platform Beam
  grp = ents.add_group
  grp.name = "Rack Platform Beam"
  face = grp.entities.add_face([4734.mm,30.mm,960.mm], [4784.mm,30.mm,960.mm], [4784.mm,2332.mm,960.mm], [4734.mm,2332.mm,960.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Platform Beam
  grp = ents.add_group
  grp.name = "Rack Platform Beam"
  face = grp.entities.add_face([5258.5.mm,30.mm,960.mm], [5308.5.mm,30.mm,960.mm], [5308.5.mm,2332.mm,960.mm], [5258.5.mm,2332.mm,960.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Platform Beam
  grp = ents.add_group
  grp.name = "Rack Platform Beam"
  face = grp.entities.add_face([5783.mm,30.mm,960.mm], [5833.mm,30.mm,960.mm], [5833.mm,2332.mm,960.mm], [5783.mm,2332.mm,960.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Panel Frame Upright
  grp = ents.add_group
  grp.name = "Panel Frame Upright"
  face = grp.entities.add_face([5258.5.mm,1046.mm,1010.mm], [5308.5.mm,1046.mm,1010.mm], [5308.5.mm,1096.mm,1010.mm], [5258.5.mm,1096.mm,1010.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1250.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Panel Frame Upright
  grp = ents.add_group
  grp.name = "Panel Frame Upright"
  face = grp.entities.add_face([5258.5.mm,1266.mm,1010.mm], [5308.5.mm,1266.mm,1010.mm], [5308.5.mm,1316.mm,1010.mm], [5258.5.mm,1316.mm,1010.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1250.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Panel Frame Top Rail
  grp = ents.add_group
  grp.name = "Panel Frame Top Rail"
  face = grp.entities.add_face([5258.5.mm,1046.mm,2210.mm], [5308.5.mm,1046.mm,2210.mm], [5308.5.mm,1316.mm,2210.mm], [5258.5.mm,1316.mm,2210.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Panel Frame Floor Beam
  grp = ents.add_group
  grp.name = "Panel Frame Floor Beam"
  face = grp.entities.add_face([5258.5.mm,1046.mm,0.mm], [5308.5.mm,1046.mm,0.mm], [5308.5.mm,1316.mm,0.mm], [5258.5.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Flange Plate
  grp = ents.add_group
  grp.name = "Foot Flange Plate"
  face = grp.entities.add_face([4684.mm,996.mm,-12.mm], [4834.mm,996.mm,-12.mm], [4834.mm,1146.mm,-12.mm], [4684.mm,1146.mm,-12.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4709.mm,1021.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4709.mm,1121.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4809.mm,1021.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4809.mm,1121.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Flange Plate
  grp = ents.add_group
  grp.name = "Foot Flange Plate"
  face = grp.entities.add_face([4684.mm,1216.mm,-12.mm], [4834.mm,1216.mm,-12.mm], [4834.mm,1366.mm,-12.mm], [4684.mm,1366.mm,-12.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4709.mm,1241.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4709.mm,1341.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4809.mm,1241.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4809.mm,1341.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Flange Plate
  grp = ents.add_group
  grp.name = "Foot Flange Plate"
  face = grp.entities.add_face([5208.5.mm,996.mm,-12.mm], [5358.5.mm,996.mm,-12.mm], [5358.5.mm,1146.mm,-12.mm], [5208.5.mm,1146.mm,-12.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5233.5.mm,1021.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5233.5.mm,1121.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5333.5.mm,1021.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5333.5.mm,1121.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Flange Plate
  grp = ents.add_group
  grp.name = "Foot Flange Plate"
  face = grp.entities.add_face([5208.5.mm,1216.mm,-12.mm], [5358.5.mm,1216.mm,-12.mm], [5358.5.mm,1366.mm,-12.mm], [5208.5.mm,1366.mm,-12.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5233.5.mm,1241.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5233.5.mm,1341.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5333.5.mm,1241.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5333.5.mm,1341.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Flange Plate
  grp = ents.add_group
  grp.name = "Foot Flange Plate"
  face = grp.entities.add_face([5733.mm,996.mm,-12.mm], [5883.mm,996.mm,-12.mm], [5883.mm,1146.mm,-12.mm], [5733.mm,1146.mm,-12.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5758.mm,1021.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5758.mm,1121.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5858.mm,1021.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5858.mm,1121.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Flange Plate
  grp = ents.add_group
  grp.name = "Foot Flange Plate"
  face = grp.entities.add_face([5733.mm,1216.mm,-12.mm], [5883.mm,1216.mm,-12.mm], [5883.mm,1366.mm,-12.mm], [5733.mm,1366.mm,-12.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5758.mm,1241.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5758.mm,1341.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5858.mm,1241.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5858.mm,1341.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Plate
  grp = ents.add_group
  grp.name = "Wall Bracket Plate"
  face = grp.entities.add_face([4684.mm,0.mm,750.mm], [4834.mm,0.mm,750.mm], [4834.mm,8.mm,750.mm], [4684.mm,8.mm,750.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(270.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Seat
  grp = ents.add_group
  grp.name = "Wall Bracket Seat"
  face = grp.entities.add_face([4724.mm,0.mm,950.mm], [4794.mm,0.mm,950.mm], [4794.mm,110.mm,950.mm], [4724.mm,110.mm,950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Gusset
  grp = ents.add_group
  grp.name = "Wall Bracket Gusset"
  ge = grp.entities
  f = ge.add_face([4755.mm,110.mm,950.mm], [4755.mm,0.mm,950.mm], [4755.mm,0.mm,750.mm])
  f.pushpull(8.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4704.mm,-10.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4704.mm,-10.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4814.mm,-10.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4814.mm,-10.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Plate
  grp = ents.add_group
  grp.name = "Wall Bracket Plate"
  face = grp.entities.add_face([4684.mm,2354.mm,750.mm], [4834.mm,2354.mm,750.mm], [4834.mm,2362.mm,750.mm], [4684.mm,2362.mm,750.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(270.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Seat
  grp = ents.add_group
  grp.name = "Wall Bracket Seat"
  face = grp.entities.add_face([4724.mm,2252.mm,950.mm], [4794.mm,2252.mm,950.mm], [4794.mm,2362.mm,950.mm], [4724.mm,2362.mm,950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Gusset
  grp = ents.add_group
  grp.name = "Wall Bracket Gusset"
  ge = grp.entities
  f = ge.add_face([4755.mm,2252.mm,950.mm], [4755.mm,2362.mm,950.mm], [4755.mm,2362.mm,750.mm])
  f.pushpull(8.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4704.mm,2344.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4704.mm,2344.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4814.mm,2344.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4814.mm,2344.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Plate
  grp = ents.add_group
  grp.name = "Wall Bracket Plate"
  face = grp.entities.add_face([5208.5.mm,0.mm,750.mm], [5358.5.mm,0.mm,750.mm], [5358.5.mm,8.mm,750.mm], [5208.5.mm,8.mm,750.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(270.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Seat
  grp = ents.add_group
  grp.name = "Wall Bracket Seat"
  face = grp.entities.add_face([5248.5.mm,0.mm,950.mm], [5318.5.mm,0.mm,950.mm], [5318.5.mm,110.mm,950.mm], [5248.5.mm,110.mm,950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Gusset
  grp = ents.add_group
  grp.name = "Wall Bracket Gusset"
  ge = grp.entities
  f = ge.add_face([5279.5.mm,110.mm,950.mm], [5279.5.mm,0.mm,950.mm], [5279.5.mm,0.mm,750.mm])
  f.pushpull(8.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5228.5.mm,-10.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5228.5.mm,-10.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5338.5.mm,-10.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5338.5.mm,-10.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Plate
  grp = ents.add_group
  grp.name = "Wall Bracket Plate"
  face = grp.entities.add_face([5208.5.mm,2354.mm,750.mm], [5358.5.mm,2354.mm,750.mm], [5358.5.mm,2362.mm,750.mm], [5208.5.mm,2362.mm,750.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(270.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Seat
  grp = ents.add_group
  grp.name = "Wall Bracket Seat"
  face = grp.entities.add_face([5248.5.mm,2252.mm,950.mm], [5318.5.mm,2252.mm,950.mm], [5318.5.mm,2362.mm,950.mm], [5248.5.mm,2362.mm,950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Gusset
  grp = ents.add_group
  grp.name = "Wall Bracket Gusset"
  ge = grp.entities
  f = ge.add_face([5279.5.mm,2252.mm,950.mm], [5279.5.mm,2362.mm,950.mm], [5279.5.mm,2362.mm,750.mm])
  f.pushpull(8.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5228.5.mm,2344.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5228.5.mm,2344.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5338.5.mm,2344.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5338.5.mm,2344.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Plate
  grp = ents.add_group
  grp.name = "Wall Bracket Plate"
  face = grp.entities.add_face([5733.mm,0.mm,750.mm], [5883.mm,0.mm,750.mm], [5883.mm,8.mm,750.mm], [5733.mm,8.mm,750.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(270.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Seat
  grp = ents.add_group
  grp.name = "Wall Bracket Seat"
  face = grp.entities.add_face([5773.mm,0.mm,950.mm], [5843.mm,0.mm,950.mm], [5843.mm,110.mm,950.mm], [5773.mm,110.mm,950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Gusset
  grp = ents.add_group
  grp.name = "Wall Bracket Gusset"
  ge = grp.entities
  f = ge.add_face([5804.mm,110.mm,950.mm], [5804.mm,0.mm,950.mm], [5804.mm,0.mm,750.mm])
  f.pushpull(8.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5753.mm,-10.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5753.mm,-10.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5863.mm,-10.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5863.mm,-10.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Plate
  grp = ents.add_group
  grp.name = "Wall Bracket Plate"
  face = grp.entities.add_face([5733.mm,2354.mm,750.mm], [5883.mm,2354.mm,750.mm], [5883.mm,2362.mm,750.mm], [5733.mm,2362.mm,750.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(270.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Seat
  grp = ents.add_group
  grp.name = "Wall Bracket Seat"
  face = grp.entities.add_face([5773.mm,2252.mm,950.mm], [5843.mm,2252.mm,950.mm], [5843.mm,2362.mm,950.mm], [5773.mm,2362.mm,950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Gusset
  grp = ents.add_group
  grp.name = "Wall Bracket Gusset"
  ge = grp.entities
  f = ge.add_face([5804.mm,2252.mm,950.mm], [5804.mm,2362.mm,950.mm], [5804.mm,2362.mm,750.mm])
  f.pushpull(8.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5753.mm,2344.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5753.mm,2344.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5863.mm,2344.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5863.mm,2344.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "IBC Rack"
  inst.layer = model.layers["IBC Rack"]

  # ═══ Light-Trap Drum ═══
  defn = model.definitions.add("Light-Trap Drum")
  ents = defn.entities
  # LT Drum Shell (3 segments walled)
  grp = ents.add_group
  grp.name = "LT Drum Shell (3 segments walled)"
  ge = grp.entities
  face = ge.add_face([[-265.17.mm,915.83.mm,0], [-237.9.mm,891.12.mm,0], [-208.34.mm,869.2.mm,0], [-176.77.mm,850.28.mm,0], [-143.51.mm,834.55.mm,0], [-108.86.mm,822.15.mm,0], [-73.16.mm,813.21.mm,0], [-36.76.mm,807.81.mm,0], [0.mm,806.mm,0], [36.76.mm,807.81.mm,0], [73.16.mm,813.21.mm,0], [108.86.mm,822.15.mm,0], [143.51.mm,834.55.mm,0], [176.77.mm,850.28.mm,0], [208.34.mm,869.2.mm,0], [237.9.mm,891.12.mm,0], [265.17.mm,915.83.mm,0], [289.88.mm,943.1.mm,0], [311.8.mm,972.66.mm,0], [330.72.mm,1004.23.mm,0], [346.45.mm,1037.49.mm,0], [358.85.mm,1072.14.mm,0], [367.79.mm,1107.84.mm,0], [373.19.mm,1144.24.mm,0], [375.mm,1181.mm,0], [373.19.mm,1217.76.mm,0], [367.79.mm,1254.16.mm,0], [358.85.mm,1289.86.mm,0], [346.45.mm,1324.51.mm,0], [330.72.mm,1357.77.mm,0], [311.8.mm,1389.34.mm,0], [289.88.mm,1418.9.mm,0], [265.17.mm,1446.17.mm,0], [237.9.mm,1470.88.mm,0], [208.34.mm,1492.8.mm,0], [176.77.mm,1511.72.mm,0], [143.51.mm,1527.45.mm,0], [108.86.mm,1539.85.mm,0], [73.16.mm,1548.79.mm,0], [36.76.mm,1554.19.mm,0], [0.mm,1556.mm,0], [-36.76.mm,1554.19.mm,0], [-73.16.mm,1548.79.mm,0], [-108.86.mm,1539.85.mm,0], [-143.51.mm,1527.45.mm,0], [-176.77.mm,1511.72.mm,0], [-208.34.mm,1492.8.mm,0], [-237.9.mm,1470.88.mm,0], [-265.17.mm,1446.17.mm,0], [-256.68.mm,1437.68.mm,0], [-230.28.mm,1461.6.mm,0], [-201.67.mm,1482.82.mm,0], [-171.12.mm,1501.14.mm,0], [-138.91.mm,1516.37.mm,0], [-105.37.mm,1528.37.mm,0], [-70.82.mm,1537.03.mm,0], [-35.58.mm,1542.25.mm,0], [0.mm,1544.mm,0], [35.58.mm,1542.25.mm,0], [70.82.mm,1537.03.mm,0], [105.37.mm,1528.37.mm,0], [138.91.mm,1516.37.mm,0], [171.12.mm,1501.14.mm,0], [201.67.mm,1482.82.mm,0], [230.28.mm,1461.6.mm,0], [256.68.mm,1437.68.mm,0], [280.6.mm,1411.28.mm,0], [301.82.mm,1382.67.mm,0], [320.14.mm,1352.12.mm,0], [335.37.mm,1319.91.mm,0], [347.37.mm,1286.37.mm,0], [356.03.mm,1251.82.mm,0], [361.25.mm,1216.58.mm,0], [363.mm,1181.mm,0], [361.25.mm,1145.42.mm,0], [356.03.mm,1110.18.mm,0], [347.37.mm,1075.63.mm,0], [335.37.mm,1042.09.mm,0], [320.14.mm,1009.88.mm,0], [301.82.mm,979.33.mm,0], [280.6.mm,950.72.mm,0], [256.68.mm,924.32.mm,0], [230.28.mm,900.4.mm,0], [201.67.mm,879.18.mm,0], [171.12.mm,860.86.mm,0], [138.91.mm,845.63.mm,0], [105.37.mm,833.63.mm,0], [70.82.mm,824.97.mm,0], [35.58.mm,819.75.mm,0], [0.mm,818.mm,0], [-35.58.mm,819.75.mm,0], [-70.82.mm,824.97.mm,0], [-105.37.mm,833.63.mm,0], [-138.91.mm,845.63.mm,0], [-171.12.mm,860.86.mm,0], [-201.67.mm,879.18.mm,0], [-230.28.mm,900.4.mm,0], [-256.68.mm,924.32.mm,0]])
  face.reverse! if face.normal.z < 0
  face.pushpull(2200.mm)
  mat = model.materials["LT Drum Shell (3 segments walled)"] || model.materials.add("LT Drum Shell (3 segments walled)")
  mat.color = Sketchup::Color.new(232, 224, 208)
  mat.alpha = 0.18
  grp.material = mat

  # LT Drum Vane A
  grp = ents.add_group
  grp.name = "LT Drum Vane A"
  ge = grp.entities
  face = ge.add_face([[267.29.mm,1444.04.mm,0], [-263.04.mm,913.71.mm,0], [-267.29.mm,917.96.mm,0], [263.04.mm,1448.29.mm,0]])
  face.reverse! if face.normal.z < 0
  face.pushpull(2200.mm)
  mat = model.materials["LT Drum Vane A"] || model.materials.add("LT Drum Vane A")
  mat.color = Sketchup::Color.new(119, 128, 136)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum Vane B
  grp = ents.add_group
  grp.name = "LT Drum Vane B"
  ge = grp.entities
  face = ge.add_face([[-263.04.mm,1448.29.mm,0], [267.29.mm,917.96.mm,0], [263.04.mm,913.71.mm,0], [-267.29.mm,1444.04.mm,0]])
  face.reverse! if face.normal.z < 0
  face.pushpull(2200.mm)
  mat = model.materials["LT Drum Vane A"] || model.materials.add("LT Drum Vane A")
  mat.color = Sketchup::Color.new(119, 128, 136)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Light-Trap Drum"
  inst.layer = model.layers["Light Trap"]

  # ═══ Electrical ═══
  defn = model.definitions.add("Electrical")
  ents = defn.entities
  # Electrical Panel (EP)
  grp = ents.add_group
  grp.name = "Electrical Panel (EP)"
  face = grp.entities.add_face([1600.mm,0.mm,1600.mm], [1900.mm,0.mm,1600.mm], [1900.mm,160.mm,1600.mm], [1600.mm,160.mm,1600.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(600.mm)
  mat = model.materials["Electrical Panel (EP)"] || model.materials.add("Electrical Panel (EP)")
  mat.color = Sketchup::Color.new(245, 197, 24)
  mat.alpha = 1.0
  grp.material = mat

  # Battery 1 (12V 100Ah LiFePO4)
  grp = ents.add_group
  grp.name = "Battery 1 (12V 100Ah LiFePO4)"
  face = grp.entities.add_face([1810.mm,0.mm,100.mm], [2050.mm,0.mm,100.mm], [2050.mm,120.mm,100.mm], [1810.mm,120.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(500.mm)
  mat = model.materials["Battery 1 (12V 100Ah LiFePO4)"] || model.materials.add("Battery 1 (12V 100Ah LiFePO4)")
  mat.color = Sketchup::Color.new(106, 90, 205)
  mat.alpha = 1.0
  grp.material = mat

  # Battery 2 (12V 100Ah LiFePO4)
  grp = ents.add_group
  grp.name = "Battery 2 (12V 100Ah LiFePO4)"
  face = grp.entities.add_face([2070.mm,0.mm,100.mm], [2310.mm,0.mm,100.mm], [2310.mm,120.mm,100.mm], [2070.mm,120.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(500.mm)
  mat = model.materials["Battery 1 (12V 100Ah LiFePO4)"] || model.materials.add("Battery 1 (12V 100Ah LiFePO4)")
  mat.color = Sketchup::Color.new(106, 90, 205)
  mat.alpha = 1.0
  grp.material = mat

  # Ext. Power Panel (exterior)
  grp = ents.add_group
  grp.name = "Ext. Power Panel (exterior)"
  face = grp.entities.add_face([1250.mm,-65.mm,1780.mm], [1590.mm,-65.mm,1780.mm], [1590.mm,-40.mm,1780.mm], [1250.mm,-40.mm,1780.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(240.mm)
  mat = model.materials["Ext. Power Panel (exterior)"] || model.materials.add("Ext. Power Panel (exterior)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.5
  grp.material = mat

  # Ext. Power Panel (interior face)
  grp = ents.add_group
  grp.name = "Ext. Power Panel (interior face)"
  face = grp.entities.add_face([1250.mm,0.mm,1780.mm], [1590.mm,0.mm,1780.mm], [1590.mm,20.mm,1780.mm], [1250.mm,20.mm,1780.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(240.mm)
  mat = model.materials["Electrical Panel (EP)"] || model.materials.add("Electrical Panel (EP)")
  mat.color = Sketchup::Color.new(245, 197, 24)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Electrical"
  inst.layer = model.layers["Electrical"]

  # ═══ Chemistry Shelf ═══
  defn = model.definitions.add("Chemistry Shelf")
  ents = defn.entities
  # Chem Shelf
  grp = ents.add_group
  grp.name = "Chem Shelf"
  face = grp.entities.add_face([3729.mm,300.mm,1003.mm], [4329.mm,300.mm,1003.mm], [4329.mm,600.mm,1003.mm], [3729.mm,600.mm,1003.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Chem Shelf"] || model.materials.add("Chem Shelf")
  mat.color = Sketchup::Color.new(200, 176, 106)
  mat.alpha = 1.0
  grp.material = mat

  # Shelf Hanger Rod
  grp = ents.add_group
  grp.name = "Shelf Hanger Rod"
  ge = grp.entities
  circle = ge.add_circle([3749.mm,320.mm,1025.mm], [0,0,1], 5.mm, 12)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(1363.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Shelf Hanger Rod
  grp = ents.add_group
  grp.name = "Shelf Hanger Rod"
  ge = grp.entities
  circle = ge.add_circle([3749.mm,580.mm,1025.mm], [0,0,1], 5.mm, 12)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(1363.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Shelf Hanger Rod
  grp = ents.add_group
  grp.name = "Shelf Hanger Rod"
  ge = grp.entities
  circle = ge.add_circle([4309.mm,320.mm,1025.mm], [0,0,1], 5.mm, 12)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(1363.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Shelf Hanger Rod
  grp = ents.add_group
  grp.name = "Shelf Hanger Rod"
  ge = grp.entities
  circle = ge.add_circle([4309.mm,580.mm,1025.mm], [0,0,1], 5.mm, 12)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(1363.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Chemistry Shelf"
  inst.layer = model.layers["Shelf"]

  # ═══ Light Seal & Hinges ═══
  defn = model.definitions.add("Light Seal & Hinges")
  ents = defn.entities
  # EPDM Seal Bottom
  grp = ents.add_group
  grp.name = "EPDM Seal Bottom"
  face = grp.entities.add_face([120.mm,0.mm,80.mm], [140.mm,0.mm,80.mm], [140.mm,2362.mm,80.mm], [120.mm,2362.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["EPDM Seal Bottom"] || model.materials.add("EPDM Seal Bottom")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM Seal Top
  grp = ents.add_group
  grp.name = "EPDM Seal Top"
  face = grp.entities.add_face([120.mm,0.mm,2348.mm], [140.mm,0.mm,2348.mm], [140.mm,2362.mm,2348.mm], [120.mm,2362.mm,2348.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["EPDM Seal Bottom"] || model.materials.add("EPDM Seal Bottom")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM Seal Left
  grp = ents.add_group
  grp.name = "EPDM Seal Left"
  face = grp.entities.add_face([120.mm,0.mm,80.mm], [140.mm,0.mm,80.mm], [140.mm,40.mm,80.mm], [120.mm,40.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2308.mm)
  mat = model.materials["EPDM Seal Bottom"] || model.materials.add("EPDM Seal Bottom")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM Seal Right
  grp = ents.add_group
  grp.name = "EPDM Seal Right"
  face = grp.entities.add_face([120.mm,2322.mm,80.mm], [140.mm,2322.mm,80.mm], [140.mm,2362.mm,80.mm], [120.mm,2362.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2308.mm)
  mat = model.materials["EPDM Seal Bottom"] || model.materials.add("EPDM Seal Bottom")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Hinge
  grp = ents.add_group
  grp.name = "Hinge"
  face = grp.entities.add_face([-30.mm,0.mm,300.mm], [30.mm,0.mm,300.mm], [30.mm,30.mm,300.mm], [-30.mm,30.mm,300.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Hinge
  grp = ents.add_group
  grp.name = "Hinge"
  face = grp.entities.add_face([-30.mm,0.mm,1184.mm], [30.mm,0.mm,1184.mm], [30.mm,30.mm,1184.mm], [-30.mm,30.mm,1184.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Hinge
  grp = ents.add_group
  grp.name = "Hinge"
  face = grp.entities.add_face([-30.mm,0.mm,2050.mm], [30.mm,0.mm,2050.mm], [30.mm,30.mm,2050.mm], [-30.mm,30.mm,2050.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Light Seal & Hinges"
  inst.layer = model.layers["Light Seal"]

  # ═══ Lighting & Wiring ═══
  defn = model.definitions.add("Lighting & Wiring")
  ents = defn.entities
  # Cable Trunking (40x25 PVC)
  grp = ents.add_group
  grp.name = "Cable Trunking (40x25 PVC)"
  face = grp.entities.add_face([0.mm,0.mm,2363.mm], [5893.mm,0.mm,2363.mm], [5893.mm,40.mm,2363.mm], [0.mm,40.mm,2363.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Cable Trunking (40x25 PVC)"] || model.materials.add("Cable Trunking (40x25 PVC)")
  mat.color = Sketchup::Color.new(154, 160, 160)
  mat.alpha = 1.0
  grp.material = mat

  # White LED Panel (Cct G)
  grp = ents.add_group
  grp.name = "White LED Panel (Cct G)"
  face = grp.entities.add_face([1000.mm,1031.mm,2348.mm], [1600.mm,1031.mm,2348.mm], [1600.mm,1331.mm,2348.mm], [1000.mm,1331.mm,2348.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["White LED Panel (Cct G)"] || model.materials.add("White LED Panel (Cct G)")
  mat.color = Sketchup::Color.new(255, 255, 224)
  mat.alpha = 0.4
  grp.material = mat

  # White LED Panel (Cct G)
  grp = ents.add_group
  grp.name = "White LED Panel (Cct G)"
  face = grp.entities.add_face([2900.mm,1031.mm,2348.mm], [3500.mm,1031.mm,2348.mm], [3500.mm,1331.mm,2348.mm], [2900.mm,1331.mm,2348.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["White LED Panel (Cct G)"] || model.materials.add("White LED Panel (Cct G)")
  mat.color = Sketchup::Color.new(255, 255, 224)
  mat.alpha = 0.4
  grp.material = mat

  # White LED Panel (Cct G)
  grp = ents.add_group
  grp.name = "White LED Panel (Cct G)"
  face = grp.entities.add_face([4790.mm,881.mm,2348.mm], [5090.mm,881.mm,2348.mm], [5090.mm,1481.mm,2348.mm], [4790.mm,1481.mm,2348.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["White LED Panel (Cct G)"] || model.materials.add("White LED Panel (Cct G)")
  mat.color = Sketchup::Color.new(255, 255, 224)
  mat.alpha = 0.4
  grp.material = mat

  # Safelight Strip (Cct D)
  grp = ents.add_group
  grp.name = "Safelight Strip (Cct D)"
  face = grp.entities.add_face([500.mm,100.mm,2363.mm], [540.mm,100.mm,2363.mm], [540.mm,2262.mm,2363.mm], [500.mm,2262.mm,2363.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Safelight Strip (Cct D)"] || model.materials.add("Safelight Strip (Cct D)")
  mat.color = Sketchup::Color.new(204, 34, 34)
  mat.alpha = 0.4
  grp.material = mat

  # Safelight Strip (Cct D)
  grp = ents.add_group
  grp.name = "Safelight Strip (Cct D)"
  face = grp.entities.add_face([2250.mm,100.mm,2363.mm], [2290.mm,100.mm,2363.mm], [2290.mm,2262.mm,2363.mm], [2250.mm,2262.mm,2363.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Safelight Strip (Cct D)"] || model.materials.add("Safelight Strip (Cct D)")
  mat.color = Sketchup::Color.new(204, 34, 34)
  mat.alpha = 0.4
  grp.material = mat

  # Safelight Strip (Cct D)
  grp = ents.add_group
  grp.name = "Safelight Strip (Cct D)"
  face = grp.entities.add_face([4150.mm,100.mm,2363.mm], [4190.mm,100.mm,2363.mm], [4190.mm,2262.mm,2363.mm], [4150.mm,2262.mm,2363.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Safelight Strip (Cct D)"] || model.materials.add("Safelight Strip (Cct D)")
  mat.color = Sketchup::Color.new(204, 34, 34)
  mat.alpha = 0.4
  grp.material = mat

  # Pull Switch (ceiling)
  grp = ents.add_group
  grp.name = "Pull Switch (ceiling)"
  face = grp.entities.add_face([1450.mm,45.mm,2348.mm], [1490.mm,45.mm,2348.mm], [1490.mm,85.mm,2348.mm], [1450.mm,85.mm,2348.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Pull Switch (ceiling)"] || model.materials.add("Pull Switch (ceiling)")
  mat.color = Sketchup::Color.new(216, 216, 240)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  face = grp.entities.add_face([1467.mm,62.mm,900.mm], [1473.mm,62.mm,900.mm], [1473.mm,68.mm,900.mm], [1467.mm,68.mm,900.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1448.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Switch (ceiling)
  grp = ents.add_group
  grp.name = "Pull Switch (ceiling)"
  face = grp.entities.add_face([1530.mm,45.mm,2348.mm], [1570.mm,45.mm,2348.mm], [1570.mm,85.mm,2348.mm], [1530.mm,85.mm,2348.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Pull Switch (ceiling)"] || model.materials.add("Pull Switch (ceiling)")
  mat.color = Sketchup::Color.new(216, 216, 240)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  face = grp.entities.add_face([1547.mm,62.mm,900.mm], [1553.mm,62.mm,900.mm], [1553.mm,68.mm,900.mm], [1547.mm,68.mm,900.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1448.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Conduit Drop (10mm)
  grp = ents.add_group
  grp.name = "Conduit Drop (10mm)"
  face = grp.entities.add_face([1750.mm,8.mm,2200.mm], [1760.mm,8.mm,2200.mm], [1760.mm,18.mm,2200.mm], [1750.mm,18.mm,2200.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(163.mm)
  mat = model.materials["Cable Trunking (40x25 PVC)"] || model.materials.add("Cable Trunking (40x25 PVC)")
  mat.color = Sketchup::Color.new(154, 160, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Conduit Drop (10mm)
  grp = ents.add_group
  grp.name = "Conduit Drop (10mm)"
  face = grp.entities.add_face([2060.mm,8.mm,600.mm], [2070.mm,8.mm,600.mm], [2070.mm,18.mm,600.mm], [2060.mm,18.mm,600.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1763.mm)
  mat = model.materials["Cable Trunking (40x25 PVC)"] || model.materials.add("Cable Trunking (40x25 PVC)")
  mat.color = Sketchup::Color.new(154, 160, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Conduit to LED Panel (Cct G)
  grp = ents.add_group
  grp.name = "Conduit to LED Panel (Cct G)"
  ge = grp.entities
  circle = ge.add_circle([1300.mm,40.mm,2350.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(991.mm)
  mat = model.materials["Cable Trunking (40x25 PVC)"] || model.materials.add("Cable Trunking (40x25 PVC)")
  mat.color = Sketchup::Color.new(154, 160, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Conduit to LED Panel (Cct G)
  grp = ents.add_group
  grp.name = "Conduit to LED Panel (Cct G)"
  ge = grp.entities
  circle = ge.add_circle([3200.mm,40.mm,2350.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(991.mm)
  mat = model.materials["Cable Trunking (40x25 PVC)"] || model.materials.add("Cable Trunking (40x25 PVC)")
  mat.color = Sketchup::Color.new(154, 160, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Conduit to LED Panel (Cct G)
  grp = ents.add_group
  grp.name = "Conduit to LED Panel (Cct G)"
  ge = grp.entities
  circle = ge.add_circle([4940.mm,40.mm,2350.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(841.mm)
  mat = model.materials["Cable Trunking (40x25 PVC)"] || model.materials.add("Cable Trunking (40x25 PVC)")
  mat.color = Sketchup::Color.new(154, 160, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Conduit to Safelight (Cct D)
  grp = ents.add_group
  grp.name = "Conduit to Safelight (Cct D)"
  ge = grp.entities
  circle = ge.add_circle([520.mm,40.mm,2350.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cable Trunking (40x25 PVC)"] || model.materials.add("Cable Trunking (40x25 PVC)")
  mat.color = Sketchup::Color.new(154, 160, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Conduit to Safelight (Cct D)
  grp = ents.add_group
  grp.name = "Conduit to Safelight (Cct D)"
  ge = grp.entities
  circle = ge.add_circle([2270.mm,40.mm,2350.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cable Trunking (40x25 PVC)"] || model.materials.add("Cable Trunking (40x25 PVC)")
  mat.color = Sketchup::Color.new(154, 160, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Conduit to Safelight (Cct D)
  grp = ents.add_group
  grp.name = "Conduit to Safelight (Cct D)"
  ge = grp.entities
  circle = ge.add_circle([4170.mm,40.mm,2350.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cable Trunking (40x25 PVC)"] || model.materials.add("Cable Trunking (40x25 PVC)")
  mat.color = Sketchup::Color.new(154, 160, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Conduit to Equipment Panel (Cct C)
  grp = ents.add_group
  grp.name = "Conduit to Equipment Panel (Cct C)"
  ge = grp.entities
  circle = ge.add_circle([5240.mm,40.mm,2350.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(1141.mm)
  mat = model.materials["Cable Trunking (40x25 PVC)"] || model.materials.add("Cable Trunking (40x25 PVC)")
  mat.color = Sketchup::Color.new(154, 160, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Conduit Drop to Pumps (Cct C)
  grp = ents.add_group
  grp.name = "Conduit Drop to Pumps (Cct C)"
  face = grp.entities.add_face([5235.mm,1176.mm,2220.mm], [5245.mm,1176.mm,2220.mm], [5245.mm,1186.mm,2220.mm], [5235.mm,1186.mm,2220.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(143.mm)
  mat = model.materials["Cable Trunking (40x25 PVC)"] || model.materials.add("Cable Trunking (40x25 PVC)")
  mat.color = Sketchup::Color.new(154, 160, 160)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Lighting & Wiring"
  inst.layer = model.layers["Lighting"]

  # ═══ Evap Cooler & Duct ═══
  defn = model.definitions.add("Evap Cooler & Duct")
  ents = defn.entities
  # Evap Cooler (on ground)
  grp = ents.add_group
  grp.name = "Evap Cooler (on ground)"
  face = grp.entities.add_face([700.mm,-490.mm,0.mm], [1300.mm,-490.mm,0.mm], [1300.mm,-140.mm,0.mm], [700.mm,-140.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(800.mm)
  mat = model.materials["Evap Cooler (on ground)"] || model.materials.add("Evap Cooler (on ground)")
  mat.color = Sketchup::Color.new(61, 170, 150)
  mat.alpha = 1.0
  grp.material = mat

  # Cold-Air Duct Inlet (Ø200)
  grp = ents.add_group
  grp.name = "Cold-Air Duct Inlet (Ø200)"
  ge = grp.entities
  circle = ge.add_circle([1000.mm,-45.mm,1900.mm], [0,1,0], 100.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(50.mm)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Evap Cooler & Duct"
  inst.layer = model.layers["Evap Cooler"]

  # ═══ Water/Waste Hookups ═══
  defn = model.definitions.add("Water/Waste Hookups")
  ents = defn.entities
  # Water Fill Hookup (2in NPT)
  grp = ents.add_group
  grp.name = "Water Fill Hookup (2in NPT)"
  ge = grp.entities
  circle = ge.add_circle([5893.mm,1181.mm,2250.mm], [1,0,0], 30.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(120.mm)
  mat = model.materials["Water Fill Hookup (2in NPT)"] || model.materials.add("Water Fill Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(46, 109, 180)
  mat.alpha = 1.0
  grp.material = mat

  # Waste Drain Hookup (2in NPT)
  grp = ents.add_group
  grp.name = "Waste Drain Hookup (2in NPT)"
  ge = grp.entities
  circle = ge.add_circle([5893.mm,1181.mm,400.mm], [1,0,0], 30.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(120.mm)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Waste Drain Hookup (2in NPT)
  grp = ents.add_group
  grp.name = "Waste Drain Hookup (2in NPT)"
  ge = grp.entities
  circle = ge.add_circle([5893.mm,1181.mm,200.mm], [1,0,0], 30.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(120.mm)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Water/Waste Hookups"
  inst.layer = model.layers["Water Hookups"]

  # ═══ Fans A & B ═══
  defn = model.definitions.add("Fans A & B")
  ents = defn.entities
  # Fan A (exhaust) baffle duct
  grp = ents.add_group
  grp.name = "Fan A (exhaust) baffle duct"
  face = grp.entities.add_face([5593.mm,200.mm,2100.mm], [5893.mm,200.mm,2100.mm], [5893.mm,400.mm,2100.mm], [5593.mm,400.mm,2100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan A (exhaust) baffle duct"] || model.materials.add("Fan A (exhaust) baffle duct")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 0.5
  grp.material = mat

  # Fan A (exhaust) baffle plate 1
  grp = ents.add_group
  grp.name = "Fan A (exhaust) baffle plate 1"
  face = grp.entities.add_face([5689.mm,225.mm,2100.mm], [5697.mm,225.mm,2100.mm], [5697.mm,375.mm,2100.mm], [5689.mm,375.mm,2100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) baffle plate 2
  grp = ents.add_group
  grp.name = "Fan A (exhaust) baffle plate 2"
  face = grp.entities.add_face([5789.mm,225.mm,2150.mm], [5797.mm,225.mm,2150.mm], [5797.mm,375.mm,2150.mm], [5789.mm,375.mm,2150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust)
  grp = ents.add_group
  grp.name = "Fan A (exhaust)"
  ge = grp.entities
  circle = ge.add_circle([5593.mm,300.mm,2200.mm], [1,0,0], 75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(50.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) baffle duct
  grp = ents.add_group
  grp.name = "Fan B (intake) baffle duct"
  face = grp.entities.add_face([0.mm,1859.mm,500.mm], [300.mm,1859.mm,500.mm], [300.mm,2059.mm,500.mm], [0.mm,2059.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan A (exhaust) baffle duct"] || model.materials.add("Fan A (exhaust) baffle duct")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 0.5
  grp.material = mat

  # Fan B (intake) baffle plate 1
  grp = ents.add_group
  grp.name = "Fan B (intake) baffle plate 1"
  face = grp.entities.add_face([96.mm,1884.mm,500.mm], [104.mm,1884.mm,500.mm], [104.mm,2034.mm,500.mm], [96.mm,2034.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) baffle plate 2
  grp = ents.add_group
  grp.name = "Fan B (intake) baffle plate 2"
  face = grp.entities.add_face([196.mm,1884.mm,550.mm], [204.mm,1884.mm,550.mm], [204.mm,2034.mm,550.mm], [196.mm,2034.mm,550.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake)
  grp = ents.add_group
  grp.name = "Fan B (intake)"
  ge = grp.entities
  circle = ge.add_circle([250.mm,1959.mm,600.mm], [1,0,0], 75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(50.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Fans A & B"
  inst.layer = model.layers["Fans"]

  # ═══ Spray Bar Plumbing ═══
  defn = model.definitions.add("Spray Bar Plumbing")
  ents = defn.entities
  # Blue Supply Trunk (1/2in HDPE)
  grp = ents.add_group
  grp.name = "Blue Supply Trunk (1/2in HDPE)"
  ge = grp.entities
  circle = ge.add_circle([470.mm,12.mm,40.mm], [1,0,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(4179.mm)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # BV-02 Riser
  grp = ents.add_group
  grp.name = "BV-02 Riser"
  ge = grp.entities
  circle = ge.add_circle([2399.mm,12.mm,40.mm], [0,0,1], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(860.mm)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # BV-02 (ball valve)
  grp = ents.add_group
  grp.name = "BV-02 (ball valve)"
  face = grp.entities.add_face([2374.mm,-13.mm,875.mm], [2424.mm,-13.mm,875.mm], [2424.mm,37.mm,875.mm], [2374.mm,37.mm,875.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["BV-02 (ball valve)"] || model.materials.add("BV-02 (ball valve)")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # TAP-01 Riser (3/4in)
  grp = ents.add_group
  grp.name = "TAP-01 Riser (3/4in)"
  ge = grp.entities
  circle = ge.add_circle([3729.mm,12.mm,40.mm], [0,0,1], 12.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(1110.mm)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # TAP-01 (chem tap)
  grp = ents.add_group
  grp.name = "TAP-01 (chem tap)"
  face = grp.entities.add_face([3714.mm,12.mm,1150.mm], [3744.mm,12.mm,1150.mm], [3744.mm,142.mm,1150.mm], [3714.mm,142.mm,1150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["BV-02 (ball valve)"] || model.materials.add("BV-02 (ball valve)")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Spray Bar Plumbing"
  inst.layer = model.layers["Spray Bar"]

  # ═══ Water Plumbing ═══
  defn = model.definitions.add("Water Plumbing")
  ents = defn.entities
  # Fill Trunk
  grp = ents.add_group
  grp.name = "Fill Trunk"
  ge = grp.entities
  vec = Geom::Vector3d.new(-485.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5893.mm,1181.mm,2250.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill Tee
  grp = ents.add_group
  grp.name = "Fill Tee"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 45.59999999999991.mm, 0.mm)
  circle = ge.add_circle([5408.mm,1158.2.mm,2250.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill Tee
  grp = ents.add_group
  grp.name = "Fill Tee"
  ge = grp.entities
  vec = Geom::Vector3d.new(22.800000000000182.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5408.mm,1181.mm,2250.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill → Blue #1
  grp = ents.add_group
  grp.name = "Fill → Blue #1"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -619.mm, 0.mm)
  circle = ge.add_circle([5408.mm,1181.mm,2250.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill → Blue #1 elbow
  grp = ents.add_group
  grp.name = "Fill → Blue #1 elbow"
  ge = grp.entities
  arc = ge.add_arc([5408.mm,562.mm,2226.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5408.mm,562.mm,2250.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill → Blue #1
  grp = ents.add_group
  grp.name = "Fill → Blue #1"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -186.mm)
  circle = ge.add_circle([5408.mm,538.mm,2226.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill → Blue #2
  grp = ents.add_group
  grp.name = "Fill → Blue #2"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 619.mm, 0.mm)
  circle = ge.add_circle([5408.mm,1181.mm,2250.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill → Blue #2 elbow
  grp = ents.add_group
  grp.name = "Fill → Blue #2 elbow"
  ge = grp.entities
  arc = ge.add_arc([5408.mm,1800.mm,2226.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5408.mm,1800.mm,2250.mm], [0.000000,1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill → Blue #2
  grp = ents.add_group
  grp.name = "Fill → Blue #2"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -186.mm)
  circle = ge.add_circle([5408.mm,1824.mm,2226.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Drain → Brown IBC
  grp = ents.add_group
  grp.name = "Drain → Brown IBC"
  ge = grp.entities
  vec = Geom::Vector3d.new(-469.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5893.mm,1181.mm,400.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Drain → Brown IBC elbow
  grp = ents.add_group
  grp.name = "Drain → Brown IBC elbow"
  ge = grp.entities
  arc = ge.add_arc([5424.mm,1157.mm,400.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5424.mm,1181.mm,400.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Drain → Brown IBC
  grp = ents.add_group
  grp.name = "Drain → Brown IBC"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -87.mm, 0.mm)
  circle = ge.add_circle([5400.mm,1157.mm,400.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Drain → Brown IBC elbow
  grp = ents.add_group
  grp.name = "Drain → Brown IBC elbow"
  ge = grp.entities
  arc = ge.add_arc([5400.mm,1070.mm,376.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5400.mm,1070.mm,400.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Drain → Brown IBC
  grp = ents.add_group
  grp.name = "Drain → Brown IBC"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -76.mm)
  circle = ge.add_circle([5400.mm,1046.mm,376.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Drain → Waste IBC
  grp = ents.add_group
  grp.name = "Drain → Waste IBC"
  ge = grp.entities
  vec = Geom::Vector3d.new(-469.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5893.mm,1181.mm,200.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Drain → Waste IBC elbow
  grp = ents.add_group
  grp.name = "Drain → Waste IBC elbow"
  ge = grp.entities
  arc = ge.add_arc([5424.mm,1205.mm,200.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,-1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5424.mm,1181.mm,200.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Drain → Waste IBC
  grp = ents.add_group
  grp.name = "Drain → Waste IBC"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 87.mm, 0.mm)
  circle = ge.add_circle([5400.mm,1205.mm,200.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Drain → Waste IBC elbow
  grp = ents.add_group
  grp.name = "Drain → Waste IBC elbow"
  ge = grp.entities
  arc = ge.add_arc([5400.mm,1292.mm,224.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5400.mm,1292.mm,200.mm], [0.000000,1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Drain → Waste IBC
  grp = ents.add_group
  grp.name = "Drain → Waste IBC"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 76.mm)
  circle = ge.add_circle([5400.mm,1316.mm,224.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Blue Suction Manifold
  grp = ents.add_group
  grp.name = "Blue Suction Manifold"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 430.mm, 0.mm)
  circle = ge.add_circle([5533.5.mm,966.mm,1195.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue Manifold Tee
  grp = ents.add_group
  grp.name = "Blue Manifold Tee"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 45.59999999999991.mm, 0.mm)
  circle = ge.add_circle([5533.5.mm,1158.2.mm,1195.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue Manifold Tee
  grp = ents.add_group
  grp.name = "Blue Manifold Tee"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.800000000000182.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5533.5.mm,1181.mm,1195.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Manifold → P-01
  grp = ents.add_group
  grp.name = "Manifold → P-01"
  ge = grp.entities
  vec = Geom::Vector3d.new(-329.5.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5533.5.mm,1181.mm,1195.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Manifold → P-01 elbow
  grp = ents.add_group
  grp.name = "Manifold → P-01 elbow"
  ge = grp.entities
  arc = ge.add_arc([5204.mm,1157.mm,1195.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5204.mm,1181.mm,1195.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Manifold → P-01
  grp = ents.add_group
  grp.name = "Manifold → P-01"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -24.480000000000018.mm, 0.mm)
  circle = ge.add_circle([5180.mm,1157.mm,1195.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Manifold → P-01 elbow
  grp = ents.add_group
  grp.name = "Manifold → P-01 elbow"
  ge = grp.entities
  arc = ge.add_arc([5180.mm,1132.52.mm,1218.52.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 23.520000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5180.mm,1132.52.mm,1195.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Manifold → P-01
  grp = ents.add_group
  grp.name = "Manifold → P-01"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 101.48000000000002.mm)
  circle = ge.add_circle([5180.mm,1109.mm,1218.52.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Brown → P-02
  grp = ents.add_group
  grp.name = "Brown → P-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(-79.5.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5283.5.mm,1046.mm,185.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown → P-02 elbow
  grp = ents.add_group
  grp.name = "Brown → P-02 elbow"
  ge = grp.entities
  arc = ge.add_arc([5204.mm,1070.mm,185.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,-1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5204.mm,1046.mm,185.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown → P-02
  grp = ents.add_group
  grp.name = "Brown → P-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 159.mm, 0.mm)
  circle = ge.add_circle([5180.mm,1070.mm,185.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown → P-02 elbow
  grp = ents.add_group
  grp.name = "Brown → P-02 elbow"
  ge = grp.entities
  arc = ge.add_arc([5180.mm,1229.mm,209.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5180.mm,1229.mm,185.mm], [0.000000,1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown → P-02
  grp = ents.add_group
  grp.name = "Brown → P-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1111.mm)
  circle = ge.add_circle([5180.mm,1253.mm,209.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Waste → P-03
  grp = ents.add_group
  grp.name = "Waste → P-03"
  ge = grp.entities
  vec = Geom::Vector3d.new(-39.5.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5283.5.mm,1316.mm,185.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste → P-03 elbow
  grp = ents.add_group
  grp.name = "Waste → P-03 elbow"
  ge = grp.entities
  arc = ge.add_arc([5244.mm,1292.mm,185.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5244.mm,1316.mm,185.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste → P-03
  grp = ents.add_group
  grp.name = "Waste → P-03"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -19.8900000000001.mm, 0.mm)
  circle = ge.add_circle([5220.mm,1292.mm,185.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste → P-03 elbow
  grp = ents.add_group
  grp.name = "Waste → P-03 elbow"
  ge = grp.entities
  arc = ge.add_arc([5220.mm,1272.11.mm,204.11.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 19.110000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5220.mm,1272.11.mm,185.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste → P-03
  grp = ents.add_group
  grp.name = "Waste → P-03"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1373.8899999999999.mm)
  circle = ge.add_circle([5220.mm,1253.mm,204.11.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 101.mm)
  circle = ge.add_circle([4550.mm,80.mm,20.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4574.mm,80.mm,121.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4550.mm,80.mm,121.mm], [0.000000,0.000000,1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(23.460000000000036.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4574.mm,80.mm,145.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4597.46.mm,80.mm,122.46.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 22.540000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4597.46.mm,80.mm,145.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -77.025.mm)
  circle = ge.add_circle([4620.mm,80.mm,122.46000000000001.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4635.435.mm,80.mm,45.435.mm], [-1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 15.435000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4620.mm,80.mm,45.435.mm], [0.000000,0.000000,-1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.19315000000006.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4635.435.mm,80.mm,30.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4643.6281500000005.mm,87.87184999999981.mm,30.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 7.871849999999805.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4643.6281500000005.mm,80.mm,30.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 1069.1281500000002.mm, 0.mm)
  circle = ge.add_circle([4651.5.mm,87.87184999999981.mm,30.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4675.5.mm,1157.mm,30.mm], [-1.000000,0.000000,0.000000], [0.000000,0.000000,-1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4651.5.mm,1157.mm,30.mm], [0.000000,1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(520.5.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4675.5.mm,1181.mm,30.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([5196.mm,1157.mm,30.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,-1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5196.mm,1181.mm,30.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -24.480000000000018.mm, 0.mm)
  circle = ge.add_circle([5220.mm,1157.mm,30.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([5220.mm,1132.52.mm,53.52.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 23.520000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5220.mm,1132.52.mm,30.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1524.48.mm)
  circle = ge.add_circle([5220.mm,1109.mm,53.519999999999996.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Pump → Filters
  grp = ents.add_group
  grp.name = "Pump → Filters"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -620.mm)
  circle = ge.add_circle([5190.mm,1181.mm,1320.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Filters → Spray Trunk
  grp = ents.add_group
  grp.name = "Filters → Spray Trunk"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -616.mm)
  circle = ge.add_circle([5190.mm,1181.mm,700.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Filters → Spray Trunk elbow
  grp = ents.add_group
  grp.name = "Filters → Spray Trunk elbow"
  ge = grp.entities
  arc = ge.add_arc([5166.mm,1181.mm,84.mm], [1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5190.mm,1181.mm,84.mm], [0.000000,0.000000,-1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Filters → Spray Trunk
  grp = ents.add_group
  grp.name = "Filters → Spray Trunk"
  ge = grp.entities
  vec = Geom::Vector3d.new(-493.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5166.mm,1181.mm,60.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Filters → Spray Trunk elbow
  grp = ents.add_group
  grp.name = "Filters → Spray Trunk elbow"
  ge = grp.entities
  arc = ge.add_arc([4673.mm,1157.mm,60.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4673.mm,1181.mm,60.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Filters → Spray Trunk
  grp = ents.add_group
  grp.name = "Filters → Spray Trunk"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -1135.2.mm, 0.mm)
  circle = ge.add_circle([4649.mm,1157.mm,60.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Filters → Spray Trunk elbow
  grp = ents.add_group
  grp.name = "Filters → Spray Trunk elbow"
  ge = grp.entities
  arc = ge.add_arc([4649.mm,21.8.mm,50.199999999999996.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 9.800000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4649.mm,21.8.mm,60.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Filters → Spray Trunk
  grp = ents.add_group
  grp.name = "Filters → Spray Trunk"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -10.200000000000003.mm)
  circle = ge.add_circle([4649.mm,12.mm,50.2.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Water Plumbing"
  inst.layer = model.layers["Water Plumbing"]


model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags from earlier generator versions ──
keep_tags = ["Shell", "Walkways", "Processing Tray", "Pinhole", "Optical Cone", "Film Plane", "Ceiling Rail", "Spray Bar", "Equipment Panel", "IBC Stack", "IBC Rack", "Light Trap", "Electrical", "Shelf", "Light Seal", "Lighting", "Evap Cooler", "Water Hookups", "Fans", "Water Plumbing"]
default_layer = model.layers[0]
model.layers.to_a.each { |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}

# ── Scenes ──
# One consistent iso camera, shared by every scene — switching scenes only
# toggles visibility, never the viewpoint.
model.layers.each { |l| l.visible = true }
bb = model.bounds
ctr = bb.center
dir = Geom::Vector3d.new(0.72, -0.7, 0.5); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.5)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

# Overview — everything visible.
model.pages.add("Overview")

# Grouped scenes — translucent Shell (context) + the group's subsystems.
[["Film Plane & Pinhole", ["Pinhole", "Optical Cone", "Film Plane"]], ["Water Systems", ["Processing Tray", "Spray Bar", "Equipment Panel", "IBC Stack", "IBC Rack", "Shelf", "Water Hookups", "Water Plumbing"]], ["Electrical Systems", ["Electrical", "Lighting"]], ["Hinge Panel & Drum", ["Light Trap", "Light Seal", "Ceiling Rail"]], ["Ventilation", ["Evap Cooler", "Fans"]], ["Walkways", ["Walkways"]]].each { |name, tags|
  model.layers.each { |l| l.visible = (l == default_layer || l.name == "Shell" || tags.include?(l.name)) }
  page = model.pages.add(name)
  page.use_camera = true
}
model.layers.each { |l| l.visible = true }

model.commit_operation
{ success: true, model: "Overview",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
