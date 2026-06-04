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

  # Walkway Left punch-out (drum exit)
  grp = ents.add_group
  grp.name = "Walkway Left punch-out (drum exit)"
  face = grp.entities.add_face([470.mm,800.mm,65.mm], [770.mm,800.mm,65.mm], [770.mm,1560.mm,65.mm], [470.mm,1560.mm,65.mm])
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
  face = grp.entities.add_face([150.mm,100.mm,100.mm], [190.mm,100.mm,100.mm], [190.mm,731.mm,100.mm], [150.mm,731.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Rail BL (DEMOUNTABLE — drum mode)
  grp = ents.add_group
  grp.name = "FP Rail BL (DEMOUNTABLE — drum mode)"
  face = grp.entities.add_face([150.mm,731.mm,100.mm], [190.mm,731.mm,100.mm], [190.mm,1631.mm,100.mm], [150.mm,1631.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["FP Rail BL (DEMOUNTABLE — drum mode)"] || model.materials.add("FP Rail BL (DEMOUNTABLE — drum mode)")
  mat.color = Sketchup::Color.new(224, 144, 42)
  mat.alpha = 1.0
  grp.material = mat

  # FP Rail BL (fixed far)
  grp = ents.add_group
  grp.name = "FP Rail BL (fixed far)"
  face = grp.entities.add_face([150.mm,1631.mm,100.mm], [190.mm,1631.mm,100.mm], [190.mm,2300.mm,100.mm], [150.mm,2300.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Rail TL (fixed near)
  grp = ents.add_group
  grp.name = "FP Rail TL (fixed near)"
  face = grp.entities.add_face([150.mm,100.mm,2248.mm], [190.mm,100.mm,2248.mm], [190.mm,731.mm,2248.mm], [150.mm,731.mm,2248.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Rail TL (DEMOUNTABLE — drum mode)
  grp = ents.add_group
  grp.name = "FP Rail TL (DEMOUNTABLE — drum mode)"
  face = grp.entities.add_face([150.mm,731.mm,2248.mm], [190.mm,731.mm,2248.mm], [190.mm,1631.mm,2248.mm], [150.mm,1631.mm,2248.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["FP Rail BL (DEMOUNTABLE — drum mode)"] || model.materials.add("FP Rail BL (DEMOUNTABLE — drum mode)")
  mat.color = Sketchup::Color.new(224, 144, 42)
  mat.alpha = 1.0
  grp.material = mat

  # FP Rail TL (fixed far)
  grp = ents.add_group
  grp.name = "FP Rail TL (fixed far)"
  face = grp.entities.add_face([150.mm,1631.mm,2248.mm], [190.mm,1631.mm,2248.mm], [190.mm,2300.mm,2248.mm], [150.mm,2300.mm,2248.mm])
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
  face = grp.entities.add_face([-30.mm,643.mm,2358.mm], [480.mm,643.mm,2358.mm], [480.mm,663.mm,2358.mm], [-30.mm,663.mm,2358.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["HGR20 Rail L"] || model.materials.add("HGR20 Rail L")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage L (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage L (HGH20CA)"
  face = grp.entities.add_face([38.mm,631.mm,2330.mm], [82.mm,631.mm,2330.mm], [82.mm,675.mm,2330.mm], [38.mm,675.mm,2330.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Carriage L (HGH20CA)"] || model.materials.add("Carriage L (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Suspension Bracket L
  grp = ents.add_group
  grp.name = "Suspension Bracket L"
  face = grp.entities.add_face([30.mm,633.mm,2290.mm], [90.mm,633.mm,2290.mm], [90.mm,673.mm,2290.mm], [30.mm,673.mm,2290.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # HGR20 Rail R
  grp = ents.add_group
  grp.name = "HGR20 Rail R"
  face = grp.entities.add_face([-30.mm,1699.mm,2358.mm], [480.mm,1699.mm,2358.mm], [480.mm,1719.mm,2358.mm], [-30.mm,1719.mm,2358.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["HGR20 Rail L"] || model.materials.add("HGR20 Rail L")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage R (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage R (HGH20CA)"
  face = grp.entities.add_face([38.mm,1687.mm,2330.mm], [82.mm,1687.mm,2330.mm], [82.mm,1731.mm,2330.mm], [38.mm,1731.mm,2330.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Carriage L (HGH20CA)"] || model.materials.add("Carriage L (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Suspension Bracket R
  grp = ents.add_group
  grp.name = "Suspension Bracket R"
  face = grp.entities.add_face([30.mm,1689.mm,2290.mm], [90.mm,1689.mm,2290.mm], [90.mm,1729.mm,2290.mm], [30.mm,1729.mm,2290.mm])
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
  # Spray Beam 40x40x3 Al SHS
  grp = ents.add_group
  grp.name = "Spray Beam 40x40x3 Al SHS"
  face = grp.entities.add_face([470.mm,1160.mm,20.mm], [4329.mm,1160.mm,20.mm], [4329.mm,1200.mm,20.mm], [470.mm,1200.mm,20.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Spray Beam 40x40x3 Al SHS"] || model.materials.add("Spray Beam 40x40x3 Al SHS")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.45
  grp.material = mat

  # Beam End Cap (feed)
  grp = ents.add_group
  grp.name = "Beam End Cap (feed)"
  face = grp.entities.add_face([466.mm,1160.mm,20.mm], [470.mm,1160.mm,20.mm], [470.mm,1200.mm,20.mm], [466.mm,1200.mm,20.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Beam End Cap (feed)"] || model.materials.add("Beam End Cap (feed)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Beam End Cap
  grp = ents.add_group
  grp.name = "Beam End Cap"
  face = grp.entities.add_face([4329.mm,1160.mm,20.mm], [4333.mm,1160.mm,20.mm], [4333.mm,1200.mm,20.mm], [4329.mm,1200.mm,20.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Beam End Cap (feed)"] || model.materials.add("Beam End Cap (feed)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Irrigation Poly Pipe (3/4 LDPE)
  grp = ents.add_group
  grp.name = "Irrigation Poly Pipe (3/4 LDPE)"
  ge = grp.entities
  circle = ge.add_circle([470.mm,1180.mm,40.mm], [1,0,0], 12.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(3859.mm)
  mat = model.materials["Irrigation Poly Pipe (3/4 LDPE)"] || model.materials.add("Irrigation Poly Pipe (3/4 LDPE)")
  mat.color = Sketchup::Color.new(42, 42, 42)
  mat.alpha = 1.0
  grp.material = mat

  # Water in Pipe
  grp = ents.add_group
  grp.name = "Water in Pipe"
  ge = grp.entities
  circle = ge.add_circle([470.mm,1180.mm,40.mm], [1,0,0], 9.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(3859.mm)
  mat = model.materials["Water in Pipe"] || model.materials.add("Water in Pipe")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 0.55
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([524.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([524.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([674.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([674.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([824.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([824.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([974.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([974.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1124.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1124.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1274.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1274.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1424.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1424.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1574.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1574.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1724.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1724.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1874.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1874.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2024.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2024.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2174.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2174.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2324.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2324.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2474.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2474.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2624.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2624.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2774.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2774.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2924.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2924.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3074.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3074.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3224.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3224.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3374.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3374.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3524.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3524.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3674.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3674.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3824.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3824.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3974.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3974.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([4124.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([4124.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([4274.5.mm,1180.mm,20.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([4274.5.mm,1180.mm,14.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage Plate L L
  grp = ents.add_group
  grp.name = "Carriage Plate L L"
  face = grp.entities.add_face([470.mm,1062.mm,29.mm], [510.mm,1062.mm,29.mm], [510.mm,1160.mm,29.mm], [470.mm,1160.mm,29.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["Beam End Cap (feed)"] || model.materials.add("Beam End Cap (feed)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage Plate R L
  grp = ents.add_group
  grp.name = "Carriage Plate R L"
  face = grp.entities.add_face([470.mm,1200.mm,29.mm], [510.mm,1200.mm,29.mm], [510.mm,1298.mm,29.mm], [470.mm,1298.mm,29.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["Beam End Cap (feed)"] || model.materials.add("Beam End Cap (feed)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel L
  grp = ents.add_group
  grp.name = "Wheel L"
  ge = grp.entities
  circle = ge.add_circle([480.mm,1080.mm,27.mm], [1,0,0], 25.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Pin 10mm L
  grp = ents.add_group
  grp.name = "Axle Pin 10mm L"
  ge = grp.entities
  circle = ge.add_circle([466.mm,1080.mm,27.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(48.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle L
  grp = ents.add_group
  grp.name = "Axle Saddle L"
  ge = grp.entities
  face = ge.add_face([[471.mm,1072.mm,27.mm], [471.mm,1072.07.mm,25.96.mm], [471.mm,1072.27.mm,24.93.mm], [471.mm,1072.61.mm,23.94.mm], [471.mm,1073.07.mm,23.mm], [471.mm,1073.65.mm,22.13.mm], [471.mm,1074.34.mm,21.34.mm], [471.mm,1075.13.mm,20.65.mm], [471.mm,1076.mm,20.07.mm], [471.mm,1076.94.mm,19.61.mm], [471.mm,1077.93.mm,19.27.mm], [471.mm,1078.96.mm,19.07.mm], [471.mm,1080.mm,19.mm], [471.mm,1081.04.mm,19.07.mm], [471.mm,1082.07.mm,19.27.mm], [471.mm,1083.06.mm,19.61.mm], [471.mm,1084.mm,20.07.mm], [471.mm,1084.87.mm,20.65.mm], [471.mm,1085.66.mm,21.34.mm], [471.mm,1086.35.mm,22.13.mm], [471.mm,1086.93.mm,23.mm], [471.mm,1087.39.mm,23.94.mm], [471.mm,1087.73.mm,24.93.mm], [471.mm,1087.93.mm,25.96.mm], [471.mm,1088.mm,27.mm], [471.mm,1086.mm,27.mm], [471.mm,1085.95.mm,26.22.mm], [471.mm,1085.8.mm,25.45.mm], [471.mm,1085.54.mm,24.7.mm], [471.mm,1085.2.mm,24.mm], [471.mm,1084.76.mm,23.35.mm], [471.mm,1084.24.mm,22.76.mm], [471.mm,1083.65.mm,22.24.mm], [471.mm,1083.mm,21.8.mm], [471.mm,1082.3.mm,21.46.mm], [471.mm,1081.55.mm,21.2.mm], [471.mm,1080.78.mm,21.05.mm], [471.mm,1080.mm,21.mm], [471.mm,1079.22.mm,21.05.mm], [471.mm,1078.45.mm,21.2.mm], [471.mm,1077.7.mm,21.46.mm], [471.mm,1077.mm,21.8.mm], [471.mm,1076.35.mm,22.24.mm], [471.mm,1075.76.mm,22.76.mm], [471.mm,1075.24.mm,23.35.mm], [471.mm,1074.8.mm,24.mm], [471.mm,1074.46.mm,24.7.mm], [471.mm,1074.2.mm,25.45.mm], [471.mm,1074.05.mm,26.22.mm], [471.mm,1074.mm,27.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([471.mm,1064.mm,27.mm], [477.mm,1064.mm,27.mm], [477.mm,1074.mm,27.mm], [471.mm,1074.mm,27.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([474.mm,1069.mm,25.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([471.mm,1086.mm,27.mm], [477.mm,1086.mm,27.mm], [477.mm,1096.mm,27.mm], [471.mm,1096.mm,27.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([474.mm,1091.mm,25.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle L
  grp = ents.add_group
  grp.name = "Axle Saddle L"
  ge = grp.entities
  face = ge.add_face([[503.mm,1072.mm,27.mm], [503.mm,1072.07.mm,25.96.mm], [503.mm,1072.27.mm,24.93.mm], [503.mm,1072.61.mm,23.94.mm], [503.mm,1073.07.mm,23.mm], [503.mm,1073.65.mm,22.13.mm], [503.mm,1074.34.mm,21.34.mm], [503.mm,1075.13.mm,20.65.mm], [503.mm,1076.mm,20.07.mm], [503.mm,1076.94.mm,19.61.mm], [503.mm,1077.93.mm,19.27.mm], [503.mm,1078.96.mm,19.07.mm], [503.mm,1080.mm,19.mm], [503.mm,1081.04.mm,19.07.mm], [503.mm,1082.07.mm,19.27.mm], [503.mm,1083.06.mm,19.61.mm], [503.mm,1084.mm,20.07.mm], [503.mm,1084.87.mm,20.65.mm], [503.mm,1085.66.mm,21.34.mm], [503.mm,1086.35.mm,22.13.mm], [503.mm,1086.93.mm,23.mm], [503.mm,1087.39.mm,23.94.mm], [503.mm,1087.73.mm,24.93.mm], [503.mm,1087.93.mm,25.96.mm], [503.mm,1088.mm,27.mm], [503.mm,1086.mm,27.mm], [503.mm,1085.95.mm,26.22.mm], [503.mm,1085.8.mm,25.45.mm], [503.mm,1085.54.mm,24.7.mm], [503.mm,1085.2.mm,24.mm], [503.mm,1084.76.mm,23.35.mm], [503.mm,1084.24.mm,22.76.mm], [503.mm,1083.65.mm,22.24.mm], [503.mm,1083.mm,21.8.mm], [503.mm,1082.3.mm,21.46.mm], [503.mm,1081.55.mm,21.2.mm], [503.mm,1080.78.mm,21.05.mm], [503.mm,1080.mm,21.mm], [503.mm,1079.22.mm,21.05.mm], [503.mm,1078.45.mm,21.2.mm], [503.mm,1077.7.mm,21.46.mm], [503.mm,1077.mm,21.8.mm], [503.mm,1076.35.mm,22.24.mm], [503.mm,1075.76.mm,22.76.mm], [503.mm,1075.24.mm,23.35.mm], [503.mm,1074.8.mm,24.mm], [503.mm,1074.46.mm,24.7.mm], [503.mm,1074.2.mm,25.45.mm], [503.mm,1074.05.mm,26.22.mm], [503.mm,1074.mm,27.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([503.mm,1064.mm,27.mm], [509.mm,1064.mm,27.mm], [509.mm,1074.mm,27.mm], [503.mm,1074.mm,27.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([506.mm,1069.mm,25.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([503.mm,1086.mm,27.mm], [509.mm,1086.mm,27.mm], [509.mm,1096.mm,27.mm], [503.mm,1096.mm,27.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([506.mm,1091.mm,25.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel L
  grp = ents.add_group
  grp.name = "Wheel L"
  ge = grp.entities
  circle = ge.add_circle([480.mm,1280.mm,27.mm], [1,0,0], 25.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Pin 10mm L
  grp = ents.add_group
  grp.name = "Axle Pin 10mm L"
  ge = grp.entities
  circle = ge.add_circle([466.mm,1280.mm,27.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(48.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle L
  grp = ents.add_group
  grp.name = "Axle Saddle L"
  ge = grp.entities
  face = ge.add_face([[471.mm,1272.mm,27.mm], [471.mm,1272.07.mm,25.96.mm], [471.mm,1272.27.mm,24.93.mm], [471.mm,1272.61.mm,23.94.mm], [471.mm,1273.07.mm,23.mm], [471.mm,1273.65.mm,22.13.mm], [471.mm,1274.34.mm,21.34.mm], [471.mm,1275.13.mm,20.65.mm], [471.mm,1276.mm,20.07.mm], [471.mm,1276.94.mm,19.61.mm], [471.mm,1277.93.mm,19.27.mm], [471.mm,1278.96.mm,19.07.mm], [471.mm,1280.mm,19.mm], [471.mm,1281.04.mm,19.07.mm], [471.mm,1282.07.mm,19.27.mm], [471.mm,1283.06.mm,19.61.mm], [471.mm,1284.mm,20.07.mm], [471.mm,1284.87.mm,20.65.mm], [471.mm,1285.66.mm,21.34.mm], [471.mm,1286.35.mm,22.13.mm], [471.mm,1286.93.mm,23.mm], [471.mm,1287.39.mm,23.94.mm], [471.mm,1287.73.mm,24.93.mm], [471.mm,1287.93.mm,25.96.mm], [471.mm,1288.mm,27.mm], [471.mm,1286.mm,27.mm], [471.mm,1285.95.mm,26.22.mm], [471.mm,1285.8.mm,25.45.mm], [471.mm,1285.54.mm,24.7.mm], [471.mm,1285.2.mm,24.mm], [471.mm,1284.76.mm,23.35.mm], [471.mm,1284.24.mm,22.76.mm], [471.mm,1283.65.mm,22.24.mm], [471.mm,1283.mm,21.8.mm], [471.mm,1282.3.mm,21.46.mm], [471.mm,1281.55.mm,21.2.mm], [471.mm,1280.78.mm,21.05.mm], [471.mm,1280.mm,21.mm], [471.mm,1279.22.mm,21.05.mm], [471.mm,1278.45.mm,21.2.mm], [471.mm,1277.7.mm,21.46.mm], [471.mm,1277.mm,21.8.mm], [471.mm,1276.35.mm,22.24.mm], [471.mm,1275.76.mm,22.76.mm], [471.mm,1275.24.mm,23.35.mm], [471.mm,1274.8.mm,24.mm], [471.mm,1274.46.mm,24.7.mm], [471.mm,1274.2.mm,25.45.mm], [471.mm,1274.05.mm,26.22.mm], [471.mm,1274.mm,27.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([471.mm,1264.mm,27.mm], [477.mm,1264.mm,27.mm], [477.mm,1274.mm,27.mm], [471.mm,1274.mm,27.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([474.mm,1269.mm,25.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([471.mm,1286.mm,27.mm], [477.mm,1286.mm,27.mm], [477.mm,1296.mm,27.mm], [471.mm,1296.mm,27.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([474.mm,1291.mm,25.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle L
  grp = ents.add_group
  grp.name = "Axle Saddle L"
  ge = grp.entities
  face = ge.add_face([[503.mm,1272.mm,27.mm], [503.mm,1272.07.mm,25.96.mm], [503.mm,1272.27.mm,24.93.mm], [503.mm,1272.61.mm,23.94.mm], [503.mm,1273.07.mm,23.mm], [503.mm,1273.65.mm,22.13.mm], [503.mm,1274.34.mm,21.34.mm], [503.mm,1275.13.mm,20.65.mm], [503.mm,1276.mm,20.07.mm], [503.mm,1276.94.mm,19.61.mm], [503.mm,1277.93.mm,19.27.mm], [503.mm,1278.96.mm,19.07.mm], [503.mm,1280.mm,19.mm], [503.mm,1281.04.mm,19.07.mm], [503.mm,1282.07.mm,19.27.mm], [503.mm,1283.06.mm,19.61.mm], [503.mm,1284.mm,20.07.mm], [503.mm,1284.87.mm,20.65.mm], [503.mm,1285.66.mm,21.34.mm], [503.mm,1286.35.mm,22.13.mm], [503.mm,1286.93.mm,23.mm], [503.mm,1287.39.mm,23.94.mm], [503.mm,1287.73.mm,24.93.mm], [503.mm,1287.93.mm,25.96.mm], [503.mm,1288.mm,27.mm], [503.mm,1286.mm,27.mm], [503.mm,1285.95.mm,26.22.mm], [503.mm,1285.8.mm,25.45.mm], [503.mm,1285.54.mm,24.7.mm], [503.mm,1285.2.mm,24.mm], [503.mm,1284.76.mm,23.35.mm], [503.mm,1284.24.mm,22.76.mm], [503.mm,1283.65.mm,22.24.mm], [503.mm,1283.mm,21.8.mm], [503.mm,1282.3.mm,21.46.mm], [503.mm,1281.55.mm,21.2.mm], [503.mm,1280.78.mm,21.05.mm], [503.mm,1280.mm,21.mm], [503.mm,1279.22.mm,21.05.mm], [503.mm,1278.45.mm,21.2.mm], [503.mm,1277.7.mm,21.46.mm], [503.mm,1277.mm,21.8.mm], [503.mm,1276.35.mm,22.24.mm], [503.mm,1275.76.mm,22.76.mm], [503.mm,1275.24.mm,23.35.mm], [503.mm,1274.8.mm,24.mm], [503.mm,1274.46.mm,24.7.mm], [503.mm,1274.2.mm,25.45.mm], [503.mm,1274.05.mm,26.22.mm], [503.mm,1274.mm,27.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([503.mm,1264.mm,27.mm], [509.mm,1264.mm,27.mm], [509.mm,1274.mm,27.mm], [503.mm,1274.mm,27.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([506.mm,1269.mm,25.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([503.mm,1286.mm,27.mm], [509.mm,1286.mm,27.mm], [509.mm,1296.mm,27.mm], [503.mm,1296.mm,27.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([506.mm,1291.mm,25.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Bottom Clamp L
  grp = ents.add_group
  grp.name = "Bottom Clamp L"
  face = grp.entities.add_face([470.mm,1148.mm,17.mm], [510.mm,1148.mm,17.mm], [510.mm,1212.mm,17.mm], [470.mm,1212.mm,17.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Top Clamp L
  grp = ents.add_group
  grp.name = "Top Clamp L"
  face = grp.entities.add_face([470.mm,1148.mm,60.mm], [510.mm,1148.mm,60.mm], [510.mm,1212.mm,60.mm], [470.mm,1212.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Spacer L
  grp = ents.add_group
  grp.name = "Clamp Spacer L"
  face = grp.entities.add_face([474.mm,1152.mm,20.mm], [506.mm,1152.mm,20.mm], [506.mm,1160.mm,20.mm], [474.mm,1160.mm,20.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Beam End Cap (feed)"] || model.materials.add("Beam End Cap (feed)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt L
  grp = ents.add_group
  grp.name = "Clamp Bolt L"
  ge = grp.entities
  circle = ge.add_circle([479.mm,1156.mm,13.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(54.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt L
  grp = ents.add_group
  grp.name = "Clamp Bolt L"
  ge = grp.entities
  circle = ge.add_circle([501.mm,1156.mm,13.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(54.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Spacer L
  grp = ents.add_group
  grp.name = "Clamp Spacer L"
  face = grp.entities.add_face([474.mm,1200.mm,20.mm], [506.mm,1200.mm,20.mm], [506.mm,1208.mm,20.mm], [474.mm,1208.mm,20.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Beam End Cap (feed)"] || model.materials.add("Beam End Cap (feed)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt L
  grp = ents.add_group
  grp.name = "Clamp Bolt L"
  ge = grp.entities
  circle = ge.add_circle([479.mm,1204.mm,13.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(54.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt L
  grp = ents.add_group
  grp.name = "Clamp Bolt L"
  ge = grp.entities
  circle = ge.add_circle([501.mm,1204.mm,13.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(54.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage Plate L R
  grp = ents.add_group
  grp.name = "Carriage Plate L R"
  face = grp.entities.add_face([4289.mm,1062.mm,29.mm], [4329.mm,1062.mm,29.mm], [4329.mm,1160.mm,29.mm], [4289.mm,1160.mm,29.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["Beam End Cap (feed)"] || model.materials.add("Beam End Cap (feed)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage Plate R R
  grp = ents.add_group
  grp.name = "Carriage Plate R R"
  face = grp.entities.add_face([4289.mm,1200.mm,29.mm], [4329.mm,1200.mm,29.mm], [4329.mm,1298.mm,29.mm], [4289.mm,1298.mm,29.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["Beam End Cap (feed)"] || model.materials.add("Beam End Cap (feed)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel R
  grp = ents.add_group
  grp.name = "Wheel R"
  ge = grp.entities
  circle = ge.add_circle([4299.mm,1080.mm,27.mm], [1,0,0], 25.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Pin 10mm R
  grp = ents.add_group
  grp.name = "Axle Pin 10mm R"
  ge = grp.entities
  circle = ge.add_circle([4285.mm,1080.mm,27.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(48.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle R
  grp = ents.add_group
  grp.name = "Axle Saddle R"
  ge = grp.entities
  face = ge.add_face([[4290.mm,1072.mm,27.mm], [4290.mm,1072.07.mm,25.96.mm], [4290.mm,1072.27.mm,24.93.mm], [4290.mm,1072.61.mm,23.94.mm], [4290.mm,1073.07.mm,23.mm], [4290.mm,1073.65.mm,22.13.mm], [4290.mm,1074.34.mm,21.34.mm], [4290.mm,1075.13.mm,20.65.mm], [4290.mm,1076.mm,20.07.mm], [4290.mm,1076.94.mm,19.61.mm], [4290.mm,1077.93.mm,19.27.mm], [4290.mm,1078.96.mm,19.07.mm], [4290.mm,1080.mm,19.mm], [4290.mm,1081.04.mm,19.07.mm], [4290.mm,1082.07.mm,19.27.mm], [4290.mm,1083.06.mm,19.61.mm], [4290.mm,1084.mm,20.07.mm], [4290.mm,1084.87.mm,20.65.mm], [4290.mm,1085.66.mm,21.34.mm], [4290.mm,1086.35.mm,22.13.mm], [4290.mm,1086.93.mm,23.mm], [4290.mm,1087.39.mm,23.94.mm], [4290.mm,1087.73.mm,24.93.mm], [4290.mm,1087.93.mm,25.96.mm], [4290.mm,1088.mm,27.mm], [4290.mm,1086.mm,27.mm], [4290.mm,1085.95.mm,26.22.mm], [4290.mm,1085.8.mm,25.45.mm], [4290.mm,1085.54.mm,24.7.mm], [4290.mm,1085.2.mm,24.mm], [4290.mm,1084.76.mm,23.35.mm], [4290.mm,1084.24.mm,22.76.mm], [4290.mm,1083.65.mm,22.24.mm], [4290.mm,1083.mm,21.8.mm], [4290.mm,1082.3.mm,21.46.mm], [4290.mm,1081.55.mm,21.2.mm], [4290.mm,1080.78.mm,21.05.mm], [4290.mm,1080.mm,21.mm], [4290.mm,1079.22.mm,21.05.mm], [4290.mm,1078.45.mm,21.2.mm], [4290.mm,1077.7.mm,21.46.mm], [4290.mm,1077.mm,21.8.mm], [4290.mm,1076.35.mm,22.24.mm], [4290.mm,1075.76.mm,22.76.mm], [4290.mm,1075.24.mm,23.35.mm], [4290.mm,1074.8.mm,24.mm], [4290.mm,1074.46.mm,24.7.mm], [4290.mm,1074.2.mm,25.45.mm], [4290.mm,1074.05.mm,26.22.mm], [4290.mm,1074.mm,27.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4290.mm,1064.mm,27.mm], [4296.mm,1064.mm,27.mm], [4296.mm,1074.mm,27.mm], [4290.mm,1074.mm,27.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4293.mm,1069.mm,25.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4290.mm,1086.mm,27.mm], [4296.mm,1086.mm,27.mm], [4296.mm,1096.mm,27.mm], [4290.mm,1096.mm,27.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4293.mm,1091.mm,25.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle R
  grp = ents.add_group
  grp.name = "Axle Saddle R"
  ge = grp.entities
  face = ge.add_face([[4322.mm,1072.mm,27.mm], [4322.mm,1072.07.mm,25.96.mm], [4322.mm,1072.27.mm,24.93.mm], [4322.mm,1072.61.mm,23.94.mm], [4322.mm,1073.07.mm,23.mm], [4322.mm,1073.65.mm,22.13.mm], [4322.mm,1074.34.mm,21.34.mm], [4322.mm,1075.13.mm,20.65.mm], [4322.mm,1076.mm,20.07.mm], [4322.mm,1076.94.mm,19.61.mm], [4322.mm,1077.93.mm,19.27.mm], [4322.mm,1078.96.mm,19.07.mm], [4322.mm,1080.mm,19.mm], [4322.mm,1081.04.mm,19.07.mm], [4322.mm,1082.07.mm,19.27.mm], [4322.mm,1083.06.mm,19.61.mm], [4322.mm,1084.mm,20.07.mm], [4322.mm,1084.87.mm,20.65.mm], [4322.mm,1085.66.mm,21.34.mm], [4322.mm,1086.35.mm,22.13.mm], [4322.mm,1086.93.mm,23.mm], [4322.mm,1087.39.mm,23.94.mm], [4322.mm,1087.73.mm,24.93.mm], [4322.mm,1087.93.mm,25.96.mm], [4322.mm,1088.mm,27.mm], [4322.mm,1086.mm,27.mm], [4322.mm,1085.95.mm,26.22.mm], [4322.mm,1085.8.mm,25.45.mm], [4322.mm,1085.54.mm,24.7.mm], [4322.mm,1085.2.mm,24.mm], [4322.mm,1084.76.mm,23.35.mm], [4322.mm,1084.24.mm,22.76.mm], [4322.mm,1083.65.mm,22.24.mm], [4322.mm,1083.mm,21.8.mm], [4322.mm,1082.3.mm,21.46.mm], [4322.mm,1081.55.mm,21.2.mm], [4322.mm,1080.78.mm,21.05.mm], [4322.mm,1080.mm,21.mm], [4322.mm,1079.22.mm,21.05.mm], [4322.mm,1078.45.mm,21.2.mm], [4322.mm,1077.7.mm,21.46.mm], [4322.mm,1077.mm,21.8.mm], [4322.mm,1076.35.mm,22.24.mm], [4322.mm,1075.76.mm,22.76.mm], [4322.mm,1075.24.mm,23.35.mm], [4322.mm,1074.8.mm,24.mm], [4322.mm,1074.46.mm,24.7.mm], [4322.mm,1074.2.mm,25.45.mm], [4322.mm,1074.05.mm,26.22.mm], [4322.mm,1074.mm,27.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4322.mm,1064.mm,27.mm], [4328.mm,1064.mm,27.mm], [4328.mm,1074.mm,27.mm], [4322.mm,1074.mm,27.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4325.mm,1069.mm,25.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4322.mm,1086.mm,27.mm], [4328.mm,1086.mm,27.mm], [4328.mm,1096.mm,27.mm], [4322.mm,1096.mm,27.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4325.mm,1091.mm,25.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel R
  grp = ents.add_group
  grp.name = "Wheel R"
  ge = grp.entities
  circle = ge.add_circle([4299.mm,1280.mm,27.mm], [1,0,0], 25.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Pin 10mm R
  grp = ents.add_group
  grp.name = "Axle Pin 10mm R"
  ge = grp.entities
  circle = ge.add_circle([4285.mm,1280.mm,27.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(48.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle R
  grp = ents.add_group
  grp.name = "Axle Saddle R"
  ge = grp.entities
  face = ge.add_face([[4290.mm,1272.mm,27.mm], [4290.mm,1272.07.mm,25.96.mm], [4290.mm,1272.27.mm,24.93.mm], [4290.mm,1272.61.mm,23.94.mm], [4290.mm,1273.07.mm,23.mm], [4290.mm,1273.65.mm,22.13.mm], [4290.mm,1274.34.mm,21.34.mm], [4290.mm,1275.13.mm,20.65.mm], [4290.mm,1276.mm,20.07.mm], [4290.mm,1276.94.mm,19.61.mm], [4290.mm,1277.93.mm,19.27.mm], [4290.mm,1278.96.mm,19.07.mm], [4290.mm,1280.mm,19.mm], [4290.mm,1281.04.mm,19.07.mm], [4290.mm,1282.07.mm,19.27.mm], [4290.mm,1283.06.mm,19.61.mm], [4290.mm,1284.mm,20.07.mm], [4290.mm,1284.87.mm,20.65.mm], [4290.mm,1285.66.mm,21.34.mm], [4290.mm,1286.35.mm,22.13.mm], [4290.mm,1286.93.mm,23.mm], [4290.mm,1287.39.mm,23.94.mm], [4290.mm,1287.73.mm,24.93.mm], [4290.mm,1287.93.mm,25.96.mm], [4290.mm,1288.mm,27.mm], [4290.mm,1286.mm,27.mm], [4290.mm,1285.95.mm,26.22.mm], [4290.mm,1285.8.mm,25.45.mm], [4290.mm,1285.54.mm,24.7.mm], [4290.mm,1285.2.mm,24.mm], [4290.mm,1284.76.mm,23.35.mm], [4290.mm,1284.24.mm,22.76.mm], [4290.mm,1283.65.mm,22.24.mm], [4290.mm,1283.mm,21.8.mm], [4290.mm,1282.3.mm,21.46.mm], [4290.mm,1281.55.mm,21.2.mm], [4290.mm,1280.78.mm,21.05.mm], [4290.mm,1280.mm,21.mm], [4290.mm,1279.22.mm,21.05.mm], [4290.mm,1278.45.mm,21.2.mm], [4290.mm,1277.7.mm,21.46.mm], [4290.mm,1277.mm,21.8.mm], [4290.mm,1276.35.mm,22.24.mm], [4290.mm,1275.76.mm,22.76.mm], [4290.mm,1275.24.mm,23.35.mm], [4290.mm,1274.8.mm,24.mm], [4290.mm,1274.46.mm,24.7.mm], [4290.mm,1274.2.mm,25.45.mm], [4290.mm,1274.05.mm,26.22.mm], [4290.mm,1274.mm,27.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4290.mm,1264.mm,27.mm], [4296.mm,1264.mm,27.mm], [4296.mm,1274.mm,27.mm], [4290.mm,1274.mm,27.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4293.mm,1269.mm,25.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4290.mm,1286.mm,27.mm], [4296.mm,1286.mm,27.mm], [4296.mm,1296.mm,27.mm], [4290.mm,1296.mm,27.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4293.mm,1291.mm,25.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle R
  grp = ents.add_group
  grp.name = "Axle Saddle R"
  ge = grp.entities
  face = ge.add_face([[4322.mm,1272.mm,27.mm], [4322.mm,1272.07.mm,25.96.mm], [4322.mm,1272.27.mm,24.93.mm], [4322.mm,1272.61.mm,23.94.mm], [4322.mm,1273.07.mm,23.mm], [4322.mm,1273.65.mm,22.13.mm], [4322.mm,1274.34.mm,21.34.mm], [4322.mm,1275.13.mm,20.65.mm], [4322.mm,1276.mm,20.07.mm], [4322.mm,1276.94.mm,19.61.mm], [4322.mm,1277.93.mm,19.27.mm], [4322.mm,1278.96.mm,19.07.mm], [4322.mm,1280.mm,19.mm], [4322.mm,1281.04.mm,19.07.mm], [4322.mm,1282.07.mm,19.27.mm], [4322.mm,1283.06.mm,19.61.mm], [4322.mm,1284.mm,20.07.mm], [4322.mm,1284.87.mm,20.65.mm], [4322.mm,1285.66.mm,21.34.mm], [4322.mm,1286.35.mm,22.13.mm], [4322.mm,1286.93.mm,23.mm], [4322.mm,1287.39.mm,23.94.mm], [4322.mm,1287.73.mm,24.93.mm], [4322.mm,1287.93.mm,25.96.mm], [4322.mm,1288.mm,27.mm], [4322.mm,1286.mm,27.mm], [4322.mm,1285.95.mm,26.22.mm], [4322.mm,1285.8.mm,25.45.mm], [4322.mm,1285.54.mm,24.7.mm], [4322.mm,1285.2.mm,24.mm], [4322.mm,1284.76.mm,23.35.mm], [4322.mm,1284.24.mm,22.76.mm], [4322.mm,1283.65.mm,22.24.mm], [4322.mm,1283.mm,21.8.mm], [4322.mm,1282.3.mm,21.46.mm], [4322.mm,1281.55.mm,21.2.mm], [4322.mm,1280.78.mm,21.05.mm], [4322.mm,1280.mm,21.mm], [4322.mm,1279.22.mm,21.05.mm], [4322.mm,1278.45.mm,21.2.mm], [4322.mm,1277.7.mm,21.46.mm], [4322.mm,1277.mm,21.8.mm], [4322.mm,1276.35.mm,22.24.mm], [4322.mm,1275.76.mm,22.76.mm], [4322.mm,1275.24.mm,23.35.mm], [4322.mm,1274.8.mm,24.mm], [4322.mm,1274.46.mm,24.7.mm], [4322.mm,1274.2.mm,25.45.mm], [4322.mm,1274.05.mm,26.22.mm], [4322.mm,1274.mm,27.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4322.mm,1264.mm,27.mm], [4328.mm,1264.mm,27.mm], [4328.mm,1274.mm,27.mm], [4322.mm,1274.mm,27.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4325.mm,1269.mm,25.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4322.mm,1286.mm,27.mm], [4328.mm,1286.mm,27.mm], [4328.mm,1296.mm,27.mm], [4322.mm,1296.mm,27.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4325.mm,1291.mm,25.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Bottom Clamp R
  grp = ents.add_group
  grp.name = "Bottom Clamp R"
  face = grp.entities.add_face([4289.mm,1148.mm,17.mm], [4329.mm,1148.mm,17.mm], [4329.mm,1212.mm,17.mm], [4289.mm,1212.mm,17.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Top Clamp R
  grp = ents.add_group
  grp.name = "Top Clamp R"
  face = grp.entities.add_face([4289.mm,1148.mm,60.mm], [4329.mm,1148.mm,60.mm], [4329.mm,1212.mm,60.mm], [4289.mm,1212.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Spacer R
  grp = ents.add_group
  grp.name = "Clamp Spacer R"
  face = grp.entities.add_face([4293.mm,1152.mm,20.mm], [4325.mm,1152.mm,20.mm], [4325.mm,1160.mm,20.mm], [4293.mm,1160.mm,20.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Beam End Cap (feed)"] || model.materials.add("Beam End Cap (feed)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt R
  grp = ents.add_group
  grp.name = "Clamp Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4298.mm,1156.mm,13.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(54.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt R
  grp = ents.add_group
  grp.name = "Clamp Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4320.mm,1156.mm,13.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(54.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Spacer R
  grp = ents.add_group
  grp.name = "Clamp Spacer R"
  face = grp.entities.add_face([4293.mm,1200.mm,20.mm], [4325.mm,1200.mm,20.mm], [4325.mm,1208.mm,20.mm], [4293.mm,1208.mm,20.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Beam End Cap (feed)"] || model.materials.add("Beam End Cap (feed)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt R
  grp = ents.add_group
  grp.name = "Clamp Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4298.mm,1204.mm,13.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(54.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt R
  grp = ents.add_group
  grp.name = "Clamp Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4320.mm,1204.mm,13.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(54.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Pole Mount Flange
  grp = ents.add_group
  grp.name = "Pole Mount Flange"
  face = grp.entities.add_face([2377.5.mm,1158.mm,60.mm], [2421.5.mm,1158.mm,60.mm], [2421.5.mm,1202.mm,60.mm], [2377.5.mm,1202.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Flange Self-Tapping Screw
  grp = ents.add_group
  grp.name = "Flange Self-Tapping Screw"
  ge = grp.entities
  circle = ge.add_circle([2383.5.mm,1164.mm,56.mm], [0,0,1], 1.8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(9.mm)
  mat = model.materials["Flange Self-Tapping Screw"] || model.materials.add("Flange Self-Tapping Screw")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Flange Screw Head
  grp = ents.add_group
  grp.name = "Flange Screw Head"
  ge = grp.entities
  circle = ge.add_circle([2383.5.mm,1164.mm,65.mm], [0,0,1], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2.5.mm)
  mat = model.materials["Flange Self-Tapping Screw"] || model.materials.add("Flange Self-Tapping Screw")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Flange Self-Tapping Screw
  grp = ents.add_group
  grp.name = "Flange Self-Tapping Screw"
  ge = grp.entities
  circle = ge.add_circle([2383.5.mm,1196.mm,56.mm], [0,0,1], 1.8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(9.mm)
  mat = model.materials["Flange Self-Tapping Screw"] || model.materials.add("Flange Self-Tapping Screw")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Flange Screw Head
  grp = ents.add_group
  grp.name = "Flange Screw Head"
  ge = grp.entities
  circle = ge.add_circle([2383.5.mm,1196.mm,65.mm], [0,0,1], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2.5.mm)
  mat = model.materials["Flange Self-Tapping Screw"] || model.materials.add("Flange Self-Tapping Screw")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Flange Self-Tapping Screw
  grp = ents.add_group
  grp.name = "Flange Self-Tapping Screw"
  ge = grp.entities
  circle = ge.add_circle([2415.5.mm,1164.mm,56.mm], [0,0,1], 1.8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(9.mm)
  mat = model.materials["Flange Self-Tapping Screw"] || model.materials.add("Flange Self-Tapping Screw")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Flange Screw Head
  grp = ents.add_group
  grp.name = "Flange Screw Head"
  ge = grp.entities
  circle = ge.add_circle([2415.5.mm,1164.mm,65.mm], [0,0,1], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2.5.mm)
  mat = model.materials["Flange Self-Tapping Screw"] || model.materials.add("Flange Self-Tapping Screw")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Flange Self-Tapping Screw
  grp = ents.add_group
  grp.name = "Flange Self-Tapping Screw"
  ge = grp.entities
  circle = ge.add_circle([2415.5.mm,1196.mm,56.mm], [0,0,1], 1.8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(9.mm)
  mat = model.materials["Flange Self-Tapping Screw"] || model.materials.add("Flange Self-Tapping Screw")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Flange Screw Head
  grp = ents.add_group
  grp.name = "Flange Screw Head"
  ge = grp.entities
  circle = ge.add_circle([2415.5.mm,1196.mm,65.mm], [0,0,1], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2.5.mm)
  mat = model.materials["Flange Self-Tapping Screw"] || model.materials.add("Flange Self-Tapping Screw")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Ball-Joint Socket (20mm)
  grp = ents.add_group
  grp.name = "Ball-Joint Socket (20mm)"
  ge = grp.entities
  circle = ge.add_circle([2399.5.mm,1180.mm,65.mm], [0,0,1], 18.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(28.mm)
  mat = model.materials["Ball-Joint Socket (20mm)"] || model.materials.add("Ball-Joint Socket (20mm)")
  mat.color = Sketchup::Color.new(200, 176, 112)
  mat.alpha = 1.0
  grp.material = mat

  # Ball-Joint Stud (M12)
  grp = ents.add_group
  grp.name = "Ball-Joint Stud (M12)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -28.mm, 24.mm)
  circle = ge.add_circle([2399.5.mm,1180.mm,81.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Ball-Joint Stud (M12)"] || model.materials.add("Ball-Joint Stud (M12)")
  mat.color = Sketchup::Color.new(216, 208, 188)
  mat.alpha = 1.0
  grp.material = mat

  # Arm Tube (25 OD Al)
  grp = ents.add_group
  grp.name = "Arm Tube (25 OD Al)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -476.mm, 424.5.mm)
  circle = ge.add_circle([2399.5.mm,1156.mm,101.mm], vec, 12.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Beam End Cap (feed)"] || model.materials.add("Beam End Cap (feed)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Pinch Bolt
  grp = ents.add_group
  grp.name = "Pinch Bolt"
  ge = grp.entities
  circle = ge.add_circle([2381.5.mm,1154.mm,107.mm], [1,0,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(36.mm)
  mat = model.materials["Flange Self-Tapping Screw"] || model.materials.add("Flange Self-Tapping Screw")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Telescoping Pole
  grp = ents.add_group
  grp.name = "Telescoping Pole"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -500.mm, 444.5.mm)
  circle = ge.add_circle([2399.5.mm,680.mm,525.5.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Beam End Cap (feed)"] || model.materials.add("Beam End Cap (feed)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Pole Handle
  grp = ents.add_group
  grp.name = "Pole Handle"
  ge = grp.entities
  circle = ge.add_circle([2309.5.mm,180.mm,970.mm], [1,0,0], 9.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(180.mm)
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Manifold
  grp = ents.add_group
  grp.name = "Feed Manifold"
  face = grp.entities.add_face([2419.5.mm,1166.mm,64.mm], [2455.5.mm,1166.mm,64.mm], [2455.5.mm,1194.mm,64.mm], [2419.5.mm,1194.mm,64.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Hose (upper)
  grp = ents.add_group
  grp.name = "Feed Hose (upper)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 500.mm, -444.5.mm)
  circle = ge.add_circle([2419.5.mm,180.mm,970.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Hose (lower)
  grp = ents.add_group
  grp.name = "Feed Hose (lower)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 476.mm, -424.5.mm)
  circle = ge.add_circle([2419.5.mm,680.mm,525.5.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.1475000000000364.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2419.5.mm,1156.mm,101.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.1475000000000364.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2420.6475.mm,1156.mm,101.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.1475000000000364.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2421.795.mm,1156.mm,101.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.1475000000000364.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2422.9425.mm,1156.mm,101.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.1474999999995816.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2424.09.mm,1156.mm,101.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.1475000000000364.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2425.2374999999997.mm,1156.mm,101.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.1475000000000364.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2426.3849999999998.mm,1156.mm,101.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.1475000000000364.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2427.5325.mm,1156.mm,101.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector elbow
  grp = ents.add_group
  grp.name = "Feed Flex Connector elbow"
  ge = grp.entities
  arc = ge.add_arc([2428.68.mm,1164.82.mm,101.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 8.820000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2428.68.mm,1156.mm,101.mm], [1.000000,0.000000,0.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.9677249999999731.mm, 0.mm)
  circle = ge.add_circle([2437.5.mm,1164.82.mm,101.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.9677249999999731.mm, 0.mm)
  circle = ge.add_circle([2437.5.mm,1165.787725.mm,101.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.9677249999999731.mm, 0.mm)
  circle = ge.add_circle([2437.5.mm,1166.7554499999999.mm,101.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.9677250000002005.mm, 0.mm)
  circle = ge.add_circle([2437.5.mm,1167.7231749999999.mm,101.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.9677249999999731.mm, 0.mm)
  circle = ge.add_circle([2437.5.mm,1168.6909.mm,101.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.9677249999999731.mm, 0.mm)
  circle = ge.add_circle([2437.5.mm,1169.658625.mm,101.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.9677249999999731.mm, 0.mm)
  circle = ge.add_circle([2437.5.mm,1170.62635.mm,101.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.9677249999999731.mm, 0.mm)
  circle = ge.add_circle([2437.5.mm,1171.594075.mm,101.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector elbow
  grp = ents.add_group
  grp.name = "Feed Flex Connector elbow"
  ge = grp.entities
  arc = ge.add_arc([2437.5.mm,1172.5618.mm,93.56179999999996.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 7.438200000000032.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2437.5.mm,1172.5618.mm,101.mm], [0.000000,1.000000,0.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1.4452249999999935.mm)
  circle = ge.add_circle([2437.5.mm,1180.mm,93.56179999999996.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1.4452249999999935.mm)
  circle = ge.add_circle([2437.5.mm,1180.mm,92.11657499999997.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1.4452249999999935.mm)
  circle = ge.add_circle([2437.5.mm,1180.mm,90.67134999999998.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1.4452250000000078.mm)
  circle = ge.add_circle([2437.5.mm,1180.mm,89.22612499999998.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1.4452249999999935.mm)
  circle = ge.add_circle([2437.5.mm,1180.mm,87.78089999999997.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1.4452249999999935.mm)
  circle = ge.add_circle([2437.5.mm,1180.mm,86.33567499999998.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1.4452249999999935.mm)
  circle = ge.add_circle([2437.5.mm,1180.mm,84.89044999999999.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1.4452249999999935.mm)
  circle = ge.add_circle([2437.5.mm,1180.mm,83.445225.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -6.443753782366116.mm, -7.248316965541221.mm)
  circle = ge.add_circle([2430.5.mm,263.3333333333333.mm,895.9166666666666.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, -3.98245885263799.mm, -4.479706245936995.mm)
  circle = ge.add_circle([2426.107390870624.mm,256.8895795509672.mm,888.6683497011254.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2414.607390870624.mm,252.9071206983292.mm,884.1886434551884.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, 3.98245885263799.mm, 4.479706245936995.mm)
  circle = ge.add_circle([2400.392609129376.mm,252.9071206983292.mm,884.1886434551884.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 6.443753782366116.mm, 7.248316965541221.mm)
  circle = ge.add_circle([2388.892609129376.mm,256.8895795509672.mm,888.6683497011254.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, 6.443753782366116.mm, 7.248316965541221.mm)
  circle = ge.add_circle([2384.5.mm,263.3333333333333.mm,895.9166666666666.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, 3.98245885263799.mm, 4.479706245936995.mm)
  circle = ge.add_circle([2388.892609129376.mm,269.77708711569943.mm,903.1649836322078.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2400.392609129376.mm,273.7595459683374.mm,907.6446898781448.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, -3.98245885263799.mm, -4.479706245936995.mm)
  circle = ge.add_circle([2414.607390870624.mm,273.7595459683374.mm,907.6446898781448.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, -6.443753782366116.mm, -7.248316965541221.mm)
  circle = ge.add_circle([2426.107390870624.mm,269.77708711569943.mm,903.1649836322078.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -6.443753782366116.mm, -7.248316965541221.mm)
  circle = ge.add_circle([2430.5.mm,430.mm,747.75.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, -3.98245885263799.mm, -4.479706245936995.mm)
  circle = ge.add_circle([2426.107390870624.mm,423.5562462176339.mm,740.5016830344588.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2414.607390870624.mm,419.5737873649959.mm,736.0219767885218.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, 3.98245885263799.mm, 4.479706245936995.mm)
  circle = ge.add_circle([2400.392609129376.mm,419.5737873649959.mm,736.0219767885218.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 6.443753782366116.mm, 7.248316965541221.mm)
  circle = ge.add_circle([2388.892609129376.mm,423.5562462176339.mm,740.5016830344588.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, 6.443753782366116.mm, 7.248316965541221.mm)
  circle = ge.add_circle([2384.5.mm,430.mm,747.75.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, 3.98245885263799.mm, 4.479706245936995.mm)
  circle = ge.add_circle([2388.892609129376.mm,436.4437537823661.mm,754.9983169655412.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2400.392609129376.mm,440.4262126350041.mm,759.4780232114782.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, -3.98245885263799.mm, -4.479706245936995.mm)
  circle = ge.add_circle([2414.607390870624.mm,440.4262126350041.mm,759.4780232114782.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, -6.443753782366116.mm, -7.248316965541221.mm)
  circle = ge.add_circle([2426.107390870624.mm,436.4437537823661.mm,754.9983169655412.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -6.443753782366116.mm, -7.248316965541221.mm)
  circle = ge.add_circle([2430.5.mm,596.6666666666667.mm,599.5833333333333.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, -3.982458852637933.mm, -4.479706245936995.mm)
  circle = ge.add_circle([2426.107390870624.mm,590.2229128843006.mm,592.335016367792.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2414.607390870624.mm,586.2404540316627.mm,587.855310121855.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, 3.982458852637933.mm, 4.479706245936995.mm)
  circle = ge.add_circle([2400.392609129376.mm,586.2404540316627.mm,587.855310121855.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 6.443753782366116.mm, 7.248316965541221.mm)
  circle = ge.add_circle([2388.892609129376.mm,590.2229128843006.mm,592.335016367792.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, 6.443753782366116.mm, 7.248316965541221.mm)
  circle = ge.add_circle([2384.5.mm,596.6666666666667.mm,599.5833333333333.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, 3.982458852637933.mm, 4.479706245936995.mm)
  circle = ge.add_circle([2388.892609129376.mm,603.1104204490329.mm,606.8316502988745.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2400.392609129376.mm,607.0928793016708.mm,611.3113565448115.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, -3.982458852637933.mm, -4.479706245936995.mm)
  circle = ge.add_circle([2414.607390870624.mm,607.0928793016708.mm,611.3113565448115.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, -6.443753782366116.mm, -7.248316965541221.mm)
  circle = ge.add_circle([2426.107390870624.mm,603.1104204490329.mm,606.8316502988745.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -6.455093390975094.mm, -7.238220151010921.mm)
  circle = ge.add_circle([2430.5.mm,759.3333333333334.mm,454.75.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, -3.989467116177366.mm, -4.473466071379107.mm)
  circle = ge.add_circle([2426.107390870624.mm,752.8782399423583.mm,447.5117798489891.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2414.607390870624.mm,748.8887728261809.mm,443.03831377760997.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, 3.989467116177366.mm, 4.473466071379107.mm)
  circle = ge.add_circle([2400.392609129376.mm,748.8887728261809.mm,443.03831377760997.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 6.455093390975094.mm, 7.238220151010921.mm)
  circle = ge.add_circle([2388.892609129376.mm,752.8782399423583.mm,447.5117798489891.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, 6.455093390975094.mm, 7.238220151010921.mm)
  circle = ge.add_circle([2384.5.mm,759.3333333333334.mm,454.75.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, 3.989467116177366.mm, 4.473466071379107.mm)
  circle = ge.add_circle([2388.892609129376.mm,765.7884267243085.mm,461.9882201510109.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2400.392609129376.mm,769.7778938404858.mm,466.46168622239003.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, -3.989467116177366.mm, -4.473466071379107.mm)
  circle = ge.add_circle([2414.607390870624.mm,769.7778938404858.mm,466.46168622239003.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, -6.455093390975094.mm, -7.238220151010921.mm)
  circle = ge.add_circle([2426.107390870624.mm,765.7884267243085.mm,461.9882201510109.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -6.455093390975094.mm, -7.238220151010921.mm)
  circle = ge.add_circle([2430.5.mm,918.mm,313.25.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, -3.989467116177366.mm, -4.473466071379107.mm)
  circle = ge.add_circle([2426.107390870624.mm,911.5449066090249.mm,306.0117798489891.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2414.607390870624.mm,907.5554394928475.mm,301.53831377760997.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, 3.989467116177366.mm, 4.473466071379107.mm)
  circle = ge.add_circle([2400.392609129376.mm,907.5554394928475.mm,301.53831377760997.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 6.455093390975094.mm, 7.238220151010921.mm)
  circle = ge.add_circle([2388.892609129376.mm,911.5449066090249.mm,306.0117798489891.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, 6.455093390975094.mm, 7.238220151010921.mm)
  circle = ge.add_circle([2384.5.mm,918.mm,313.25.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, 3.989467116177366.mm, 4.473466071379107.mm)
  circle = ge.add_circle([2388.892609129376.mm,924.4550933909751.mm,320.4882201510109.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2400.392609129376.mm,928.4445605071525.mm,324.96168622239003.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, -3.989467116177366.mm, -4.473466071379107.mm)
  circle = ge.add_circle([2414.607390870624.mm,928.4445605071525.mm,324.96168622239003.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, -6.455093390975094.mm, -7.238220151010921.mm)
  circle = ge.add_circle([2426.107390870624.mm,924.4550933909751.mm,320.4882201510109.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -6.45509339097498.mm, -7.238220151010921.mm)
  circle = ge.add_circle([2430.5.mm,1076.6666666666667.mm,171.75.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, -3.989467116177593.mm, -4.473466071379107.mm)
  circle = ge.add_circle([2426.107390870624.mm,1070.2115732756918.mm,164.51177984898908.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-14.214781741247862.mm, 0.mm, -2.842170943040401e-14.mm)
  circle = ge.add_circle([2414.607390870624.mm,1066.2221061595142.mm,160.03831377760997.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, 3.989467116177593.mm, 4.473466071379136.mm)
  circle = ge.add_circle([2400.392609129376.mm,1066.2221061595142.mm,160.03831377760994.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 6.45509339097498.mm, 7.238220151010921.mm)
  circle = ge.add_circle([2388.892609129376.mm,1070.2115732756918.mm,164.51177984898908.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, 6.45509339097498.mm, 7.238220151010893.mm)
  circle = ge.add_circle([2384.5.mm,1076.6666666666667.mm,171.75.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, 3.989467116177593.mm, 4.473466071379136.mm)
  circle = ge.add_circle([2388.892609129376.mm,1083.1217600576417.mm,178.9882201510109.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(14.214781741247862.mm, 0.mm, 2.842170943040401e-14.mm)
  circle = ge.add_circle([2400.392609129376.mm,1087.1112271738193.mm,183.46168622239003.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, -3.989467116177593.mm, -4.473466071379136.mm)
  circle = ge.add_circle([2414.607390870624.mm,1087.1112271738193.mm,183.46168622239006.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, -6.45509339097498.mm, -7.238220151010921.mm)
  circle = ge.add_circle([2426.107390870624.mm,1083.1217600576417.mm,178.98822015101092.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 13.mm, 0.mm)
  circle = ge.add_circle([2437.5.mm,1192.mm,73.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube elbow
  grp = ents.add_group
  grp.name = "Feed Tube elbow"
  ge = grp.entities
  arc = ge.add_arc([2432.5.mm,1205.mm,73.mm], [1.000000,0.000000,0.000000], [0.000000,-0.000000,1.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2437.5.mm,1205.mm,73.mm], [0.000000,1.000000,0.000000], 3.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1681.857142857143.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2432.5.mm,1210.mm,73.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube elbow
  grp = ents.add_group
  grp.name = "Feed Tube elbow"
  ge = grp.entities
  arc = ge.add_arc([750.6428571428571.mm,1205.mm,73.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([750.6428571428571.mm,1210.mm,73.mm], [-1.000000,0.000000,0.000000], 3.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -21.569999999999936.mm, 0.mm)
  circle = ge.add_circle([745.6428571428571.mm,1205.mm,73.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube elbow
  grp = ents.add_group
  grp.name = "Feed Tube elbow"
  ge = grp.entities
  arc = ge.add_arc([745.6428571428571.mm,1183.43.mm,69.57.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 3.43.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([745.6428571428571.mm,1183.43.mm,73.mm], [0.000000,-1.000000,0.000000], 3.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -3.569999999999993.mm)
  circle = ge.add_circle([745.6428571428571.mm,1180.mm,69.57.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Barb Fitting
  grp = ents.add_group
  grp.name = "Feed Barb Fitting"
  ge = grp.entities
  circle = ge.add_circle([745.6428571428571.mm,1180.mm,38.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(28.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 13.mm, 0.mm)
  circle = ge.add_circle([2437.5.mm,1192.mm,73.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube elbow
  grp = ents.add_group
  grp.name = "Feed Tube elbow"
  ge = grp.entities
  arc = ge.add_arc([2432.5.mm,1205.mm,73.mm], [1.000000,0.000000,0.000000], [0.000000,-0.000000,1.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2437.5.mm,1205.mm,73.mm], [0.000000,1.000000,0.000000], 3.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1130.5714285714287.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2432.5.mm,1210.mm,73.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube elbow
  grp = ents.add_group
  grp.name = "Feed Tube elbow"
  ge = grp.entities
  arc = ge.add_arc([1301.9285714285713.mm,1205.mm,73.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1301.9285714285713.mm,1210.mm,73.mm], [-1.000000,0.000000,0.000000], 3.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -21.569999999999936.mm, 0.mm)
  circle = ge.add_circle([1296.9285714285713.mm,1205.mm,73.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube elbow
  grp = ents.add_group
  grp.name = "Feed Tube elbow"
  ge = grp.entities
  arc = ge.add_arc([1296.9285714285713.mm,1183.43.mm,69.57.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 3.43.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1296.9285714285713.mm,1183.43.mm,73.mm], [0.000000,-1.000000,0.000000], 3.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -3.569999999999993.mm)
  circle = ge.add_circle([1296.9285714285713.mm,1180.mm,69.57.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Barb Fitting
  grp = ents.add_group
  grp.name = "Feed Barb Fitting"
  ge = grp.entities
  circle = ge.add_circle([1296.9285714285713.mm,1180.mm,38.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(28.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 13.mm, 0.mm)
  circle = ge.add_circle([2437.5.mm,1192.mm,73.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube elbow
  grp = ents.add_group
  grp.name = "Feed Tube elbow"
  ge = grp.entities
  arc = ge.add_arc([2432.5.mm,1205.mm,73.mm], [1.000000,0.000000,0.000000], [0.000000,-0.000000,1.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2437.5.mm,1205.mm,73.mm], [0.000000,1.000000,0.000000], 3.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(-579.2857142857142.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2432.5.mm,1210.mm,73.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube elbow
  grp = ents.add_group
  grp.name = "Feed Tube elbow"
  ge = grp.entities
  arc = ge.add_arc([1853.2142857142858.mm,1205.mm,73.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1853.2142857142858.mm,1210.mm,73.mm], [-1.000000,0.000000,0.000000], 3.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -21.569999999999936.mm, 0.mm)
  circle = ge.add_circle([1848.2142857142858.mm,1205.mm,73.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube elbow
  grp = ents.add_group
  grp.name = "Feed Tube elbow"
  ge = grp.entities
  arc = ge.add_arc([1848.2142857142858.mm,1183.43.mm,69.57.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 3.43.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1848.2142857142858.mm,1183.43.mm,73.mm], [0.000000,-1.000000,0.000000], 3.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -3.569999999999993.mm)
  circle = ge.add_circle([1848.2142857142858.mm,1180.mm,69.57.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Barb Fitting
  grp = ents.add_group
  grp.name = "Feed Barb Fitting"
  ge = grp.entities
  circle = ge.add_circle([1848.2142857142858.mm,1180.mm,38.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(28.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(24.570000000000164.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2451.5.mm,1180.mm,73.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube elbow
  grp = ents.add_group
  grp.name = "Feed Tube elbow"
  ge = grp.entities
  arc = ge.add_arc([2476.07.mm,1180.mm,69.57.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 3.43.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2476.07.mm,1180.mm,73.mm], [1.000000,0.000000,0.000000], 3.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -3.569999999999993.mm)
  circle = ge.add_circle([2479.5.mm,1180.mm,69.57.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Barb Fitting
  grp = ents.add_group
  grp.name = "Feed Barb Fitting"
  ge = grp.entities
  circle = ge.add_circle([2479.5.mm,1180.mm,38.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(28.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(495.85571428571484.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2451.5.mm,1180.mm,73.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube elbow
  grp = ents.add_group
  grp.name = "Feed Tube elbow"
  ge = grp.entities
  arc = ge.add_arc([2947.355714285715.mm,1180.mm,69.57.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 3.43.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2947.355714285715.mm,1180.mm,73.mm], [1.000000,0.000000,0.000000], 3.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -3.569999999999993.mm)
  circle = ge.add_circle([2950.7857142857147.mm,1180.mm,69.57.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Barb Fitting
  grp = ents.add_group
  grp.name = "Feed Barb Fitting"
  ge = grp.entities
  circle = ge.add_circle([2950.7857142857147.mm,1180.mm,38.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(28.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(1047.1414285714286.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2451.5.mm,1180.mm,73.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube elbow
  grp = ents.add_group
  grp.name = "Feed Tube elbow"
  ge = grp.entities
  arc = ge.add_arc([3498.6414285714286.mm,1180.mm,69.57.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 3.43.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([3498.6414285714286.mm,1180.mm,73.mm], [1.000000,0.000000,0.000000], 3.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -3.569999999999993.mm)
  circle = ge.add_circle([3502.0714285714284.mm,1180.mm,69.57.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Barb Fitting
  grp = ents.add_group
  grp.name = "Feed Barb Fitting"
  ge = grp.entities
  circle = ge.add_circle([3502.0714285714284.mm,1180.mm,38.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(28.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(1598.4271428571433.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2451.5.mm,1180.mm,73.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube elbow
  grp = ents.add_group
  grp.name = "Feed Tube elbow"
  ge = grp.entities
  arc = ge.add_arc([4049.9271428571433.mm,1180.mm,69.57.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 3.43.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4049.9271428571433.mm,1180.mm,73.mm], [1.000000,0.000000,0.000000], 3.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -3.569999999999993.mm)
  circle = ge.add_circle([4053.357142857143.mm,1180.mm,69.57.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Barb Fitting
  grp = ents.add_group
  grp.name = "Feed Barb Fitting"
  ge = grp.entities
  circle = ge.add_circle([4053.357142857143.mm,1180.mm,38.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(28.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
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
  # LT Housing arc (near Yd)
  grp = ents.add_group
  grp.name = "LT Housing arc (near Yd)"
  ge = grp.entities
  face = ge.add_face([[344.72.mm,1470.25.mm,80.mm], [333.98.mm,1482.59.mm,80.mm], [322.79.mm,1494.54.mm,80.mm], [311.18.mm,1506.06.mm,80.mm], [299.16.mm,1517.16.mm,80.mm], [286.74.mm,1527.81.mm,80.mm], [273.94.mm,1538.01.mm,80.mm], [260.78.mm,1547.73.mm,80.mm], [247.28.mm,1556.97.mm,80.mm], [233.45.mm,1565.71.mm,80.mm], [219.31.mm,1573.94.mm,80.mm], [204.88.mm,1581.66.mm,80.mm], [190.18.mm,1588.84.mm,80.mm], [175.23.mm,1595.48.mm,80.mm], [160.04.mm,1601.58.mm,80.mm], [144.65.mm,1607.12.mm,80.mm], [129.06.mm,1612.1.mm,80.mm], [113.3.mm,1616.5.mm,80.mm], [97.4.mm,1620.33.mm,80.mm], [81.36.mm,1623.58.mm,80.mm], [65.22.mm,1626.25.mm,80.mm], [48.99.mm,1628.33.mm,80.mm], [32.7.mm,1629.81.mm,80.mm], [16.36.mm,1630.7.mm,80.mm], [0.mm,1631.mm,80.mm], [-16.36.mm,1630.7.mm,80.mm], [-32.7.mm,1629.81.mm,80.mm], [-48.99.mm,1628.33.mm,80.mm], [-65.22.mm,1626.25.mm,80.mm], [-81.36.mm,1623.58.mm,80.mm], [-97.4.mm,1620.33.mm,80.mm], [-113.3.mm,1616.5.mm,80.mm], [-129.06.mm,1612.1.mm,80.mm], [-144.65.mm,1607.12.mm,80.mm], [-160.04.mm,1601.58.mm,80.mm], [-175.23.mm,1595.48.mm,80.mm], [-190.18.mm,1588.84.mm,80.mm], [-204.88.mm,1581.66.mm,80.mm], [-219.31.mm,1573.94.mm,80.mm], [-233.45.mm,1565.71.mm,80.mm], [-247.28.mm,1556.97.mm,80.mm], [-260.78.mm,1547.73.mm,80.mm], [-273.94.mm,1538.01.mm,80.mm], [-286.74.mm,1527.81.mm,80.mm], [-299.16.mm,1517.16.mm,80.mm], [-311.18.mm,1506.06.mm,80.mm], [-322.79.mm,1494.54.mm,80.mm], [-333.98.mm,1482.59.mm,80.mm], [-344.72.mm,1470.25.mm,80.mm], [-342.42.mm,1468.33.mm,80.mm], [-331.75.mm,1480.58.mm,80.mm], [-320.64.mm,1492.45.mm,80.mm], [-309.11.mm,1503.9.mm,80.mm], [-297.16.mm,1514.92.mm,80.mm], [-284.83.mm,1525.5.mm,80.mm], [-272.12.mm,1535.63.mm,80.mm], [-259.04.mm,1545.29.mm,80.mm], [-245.63.mm,1554.46.mm,80.mm], [-231.89.mm,1563.15.mm,80.mm], [-217.85.mm,1571.32.mm,80.mm], [-203.51.mm,1578.98.mm,80.mm], [-188.91.mm,1586.12.mm,80.mm], [-174.06.mm,1592.72.mm,80.mm], [-158.98.mm,1598.77.mm,80.mm], [-143.68.mm,1604.28.mm,80.mm], [-128.2.mm,1609.22.mm,80.mm], [-112.55.mm,1613.6.mm,80.mm], [-96.75.mm,1617.4.mm,80.mm], [-80.82.mm,1620.63.mm,80.mm], [-64.78.mm,1623.28.mm,80.mm], [-48.66.mm,1625.34.mm,80.mm], [-32.48.mm,1626.82.mm,80.mm], [-16.25.mm,1627.7.mm,80.mm], [0.mm,1628.mm,80.mm], [16.25.mm,1627.7.mm,80.mm], [32.48.mm,1626.82.mm,80.mm], [48.66.mm,1625.34.mm,80.mm], [64.78.mm,1623.28.mm,80.mm], [80.82.mm,1620.63.mm,80.mm], [96.75.mm,1617.4.mm,80.mm], [112.55.mm,1613.6.mm,80.mm], [128.2.mm,1609.22.mm,80.mm], [143.68.mm,1604.28.mm,80.mm], [158.98.mm,1598.77.mm,80.mm], [174.06.mm,1592.72.mm,80.mm], [188.91.mm,1586.12.mm,80.mm], [203.51.mm,1578.98.mm,80.mm], [217.85.mm,1571.32.mm,80.mm], [231.89.mm,1563.15.mm,80.mm], [245.63.mm,1554.46.mm,80.mm], [259.04.mm,1545.29.mm,80.mm], [272.12.mm,1535.63.mm,80.mm], [284.83.mm,1525.5.mm,80.mm], [297.16.mm,1514.92.mm,80.mm], [309.11.mm,1503.9.mm,80.mm], [320.64.mm,1492.45.mm,80.mm], [331.75.mm,1480.58.mm,80.mm], [342.42.mm,1468.33.mm,80.mm]])
  face.reverse! if face.normal.z < 0
  face.pushpull(2120.mm)
  mat = model.materials["LT Housing arc (near Yd)"] || model.materials.add("LT Housing arc (near Yd)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.42
  grp.material = mat

  # LT Housing arc (far Yd)
  grp = ents.add_group
  grp.name = "LT Housing arc (far Yd)"
  ge = grp.entities
  face = ge.add_face([[-344.72.mm,891.75.mm,80.mm], [-333.98.mm,879.41.mm,80.mm], [-322.79.mm,867.46.mm,80.mm], [-311.18.mm,855.94.mm,80.mm], [-299.16.mm,844.84.mm,80.mm], [-286.74.mm,834.19.mm,80.mm], [-273.94.mm,823.99.mm,80.mm], [-260.78.mm,814.27.mm,80.mm], [-247.28.mm,805.03.mm,80.mm], [-233.45.mm,796.29.mm,80.mm], [-219.31.mm,788.06.mm,80.mm], [-204.88.mm,780.34.mm,80.mm], [-190.18.mm,773.16.mm,80.mm], [-175.23.mm,766.52.mm,80.mm], [-160.04.mm,760.42.mm,80.mm], [-144.65.mm,754.88.mm,80.mm], [-129.06.mm,749.9.mm,80.mm], [-113.3.mm,745.5.mm,80.mm], [-97.4.mm,741.67.mm,80.mm], [-81.36.mm,738.42.mm,80.mm], [-65.22.mm,735.75.mm,80.mm], [-48.99.mm,733.67.mm,80.mm], [-32.7.mm,732.19.mm,80.mm], [-16.36.mm,731.3.mm,80.mm], [0.mm,731.mm,80.mm], [16.36.mm,731.3.mm,80.mm], [32.7.mm,732.19.mm,80.mm], [48.99.mm,733.67.mm,80.mm], [65.22.mm,735.75.mm,80.mm], [81.36.mm,738.42.mm,80.mm], [97.4.mm,741.67.mm,80.mm], [113.3.mm,745.5.mm,80.mm], [129.06.mm,749.9.mm,80.mm], [144.65.mm,754.88.mm,80.mm], [160.04.mm,760.42.mm,80.mm], [175.23.mm,766.52.mm,80.mm], [190.18.mm,773.16.mm,80.mm], [204.88.mm,780.34.mm,80.mm], [219.31.mm,788.06.mm,80.mm], [233.45.mm,796.29.mm,80.mm], [247.28.mm,805.03.mm,80.mm], [260.78.mm,814.27.mm,80.mm], [273.94.mm,823.99.mm,80.mm], [286.74.mm,834.19.mm,80.mm], [299.16.mm,844.84.mm,80.mm], [311.18.mm,855.94.mm,80.mm], [322.79.mm,867.46.mm,80.mm], [333.98.mm,879.41.mm,80.mm], [344.72.mm,891.75.mm,80.mm], [342.42.mm,893.67.mm,80.mm], [331.75.mm,881.42.mm,80.mm], [320.64.mm,869.55.mm,80.mm], [309.11.mm,858.1.mm,80.mm], [297.16.mm,847.08.mm,80.mm], [284.83.mm,836.5.mm,80.mm], [272.12.mm,826.37.mm,80.mm], [259.04.mm,816.71.mm,80.mm], [245.63.mm,807.54.mm,80.mm], [231.89.mm,798.85.mm,80.mm], [217.85.mm,790.68.mm,80.mm], [203.51.mm,783.02.mm,80.mm], [188.91.mm,775.88.mm,80.mm], [174.06.mm,769.28.mm,80.mm], [158.98.mm,763.23.mm,80.mm], [143.68.mm,757.72.mm,80.mm], [128.2.mm,752.78.mm,80.mm], [112.55.mm,748.4.mm,80.mm], [96.75.mm,744.6.mm,80.mm], [80.82.mm,741.37.mm,80.mm], [64.78.mm,738.72.mm,80.mm], [48.66.mm,736.66.mm,80.mm], [32.48.mm,735.18.mm,80.mm], [16.25.mm,734.3.mm,80.mm], [0.mm,734.mm,80.mm], [-16.25.mm,734.3.mm,80.mm], [-32.48.mm,735.18.mm,80.mm], [-48.66.mm,736.66.mm,80.mm], [-64.78.mm,738.72.mm,80.mm], [-80.82.mm,741.37.mm,80.mm], [-96.75.mm,744.6.mm,80.mm], [-112.55.mm,748.4.mm,80.mm], [-128.2.mm,752.78.mm,80.mm], [-143.68.mm,757.72.mm,80.mm], [-158.98.mm,763.23.mm,80.mm], [-174.06.mm,769.28.mm,80.mm], [-188.91.mm,775.88.mm,80.mm], [-203.51.mm,783.02.mm,80.mm], [-217.85.mm,790.68.mm,80.mm], [-231.89.mm,798.85.mm,80.mm], [-245.63.mm,807.54.mm,80.mm], [-259.04.mm,816.71.mm,80.mm], [-272.12.mm,826.37.mm,80.mm], [-284.83.mm,836.5.mm,80.mm], [-297.16.mm,847.08.mm,80.mm], [-309.11.mm,858.1.mm,80.mm], [-320.64.mm,869.55.mm,80.mm], [-331.75.mm,881.42.mm,80.mm], [-342.42.mm,893.67.mm,80.mm]])
  face.reverse! if face.normal.z < 0
  face.pushpull(2120.mm)
  mat = model.materials["LT Housing arc (near Yd)"] || model.materials.add("LT Housing arc (near Yd)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.42
  grp.material = mat

  # LT Drum C-shell
  grp = ents.add_group
  grp.name = "LT Drum C-shell"
  ge = grp.entities
  face = ge.add_face([[-330.93.mm,903.32.mm,80.mm], [-301.mm,871.12.mm,80.mm], [-267.94.mm,842.13.mm,80.mm], [-232.11.mm,816.65.mm,80.mm], [-193.88.mm,794.95.mm,80.mm], [-153.64.mm,777.24.mm,80.mm], [-111.81.mm,763.72.mm,80.mm], [-68.82.mm,754.52.mm,80.mm], [-25.12.mm,749.73.mm,80.mm], [18.84.mm,749.41.mm,80.mm], [62.61.mm,753.56.mm,80.mm], [105.73.mm,762.14.mm,80.mm], [147.75.mm,775.05.mm,80.mm], [188.25.mm,792.17.mm,80.mm], [226.79.mm,813.32.mm,80.mm], [262.98.mm,838.27.mm,80.mm], [296.46.mm,866.77.mm,80.mm], [326.86.mm,898.53.mm,80.mm], [353.87.mm,933.21.mm,80.mm], [377.22.mm,970.46.mm,80.mm], [396.67.mm,1009.89.mm,80.mm], [412.01.mm,1051.1.mm,80.mm], [423.08.mm,1093.64.mm,80.mm], [429.76.mm,1137.09.mm,80.mm], [432.mm,1181.mm,80.mm], [429.76.mm,1224.91.mm,80.mm], [423.08.mm,1268.36.mm,80.mm], [412.01.mm,1310.9.mm,80.mm], [396.67.mm,1352.11.mm,80.mm], [377.22.mm,1391.54.mm,80.mm], [353.87.mm,1428.79.mm,80.mm], [326.86.mm,1463.47.mm,80.mm], [296.46.mm,1495.23.mm,80.mm], [262.98.mm,1523.73.mm,80.mm], [226.79.mm,1548.68.mm,80.mm], [188.25.mm,1569.83.mm,80.mm], [147.75.mm,1586.95.mm,80.mm], [105.73.mm,1599.86.mm,80.mm], [62.61.mm,1608.44.mm,80.mm], [18.84.mm,1612.59.mm,80.mm], [-25.12.mm,1612.27.mm,80.mm], [-68.82.mm,1607.48.mm,80.mm], [-111.81.mm,1598.28.mm,80.mm], [-153.64.mm,1584.76.mm,80.mm], [-193.88.mm,1567.05.mm,80.mm], [-232.11.mm,1545.35.mm,80.mm], [-267.94.mm,1519.87.mm,80.mm], [-301.mm,1490.88.mm,80.mm], [-330.93.mm,1458.68.mm,80.mm], [-328.63.mm,1456.76.mm,80.mm], [-298.9.mm,1488.73.mm,80.mm], [-266.08.mm,1517.51.mm,80.mm], [-230.5.mm,1542.81.mm,80.mm], [-192.53.mm,1564.37.mm,80.mm], [-152.57.mm,1581.95.mm,80.mm], [-111.03.mm,1595.38.mm,80.mm], [-68.34.mm,1604.52.mm,80.mm], [-24.94.mm,1609.27.mm,80.mm], [18.71.mm,1609.59.mm,80.mm], [62.18.mm,1605.47.mm,80.mm], [104.99.mm,1596.95.mm,80.mm], [146.73.mm,1584.13.mm,80.mm], [186.94.mm,1567.13.mm,80.mm], [225.21.mm,1546.13.mm,80.mm], [261.16.mm,1521.35.mm,80.mm], [294.4.mm,1493.04.mm,80.mm], [324.59.mm,1461.51.mm,80.mm], [351.42.mm,1427.06.mm,80.mm], [374.61.mm,1390.07.mm,80.mm], [393.91.mm,1350.92.mm,80.mm], [409.14.mm,1310.mm,80.mm], [420.14.mm,1267.75.mm,80.mm], [426.78.mm,1224.6.mm,80.mm], [429.mm,1181.mm,80.mm], [426.78.mm,1137.4.mm,80.mm], [420.14.mm,1094.25.mm,80.mm], [409.14.mm,1052.mm,80.mm], [393.91.mm,1011.08.mm,80.mm], [374.61.mm,971.93.mm,80.mm], [351.42.mm,934.94.mm,80.mm], [324.59.mm,900.49.mm,80.mm], [294.4.mm,868.96.mm,80.mm], [261.16.mm,840.65.mm,80.mm], [225.21.mm,815.87.mm,80.mm], [186.94.mm,794.87.mm,80.mm], [146.73.mm,777.87.mm,80.mm], [104.99.mm,765.05.mm,80.mm], [62.18.mm,756.53.mm,80.mm], [18.71.mm,752.41.mm,80.mm], [-24.94.mm,752.73.mm,80.mm], [-68.34.mm,757.48.mm,80.mm], [-111.03.mm,766.62.mm,80.mm], [-152.57.mm,780.05.mm,80.mm], [-192.53.mm,797.63.mm,80.mm], [-230.5.mm,819.19.mm,80.mm], [-266.08.mm,844.49.mm,80.mm], [-298.9.mm,873.27.mm,80.mm], [-328.63.mm,905.24.mm,80.mm]])
  face.reverse! if face.normal.z < 0
  face.pushpull(2120.mm)
  mat = model.materials["LT Drum C-shell"] || model.materials.add("LT Drum C-shell")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.85
  grp.material = mat

  # LT Drum top cap
  grp = ents.add_group
  grp.name = "LT Drum top cap"
  ge = grp.entities
  circle = ge.add_circle([0.mm,1181.mm,2195.mm], [0,0,1], 432.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Beam End Cap (feed)"] || model.materials.add("Beam End Cap (feed)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum bottom cap
  grp = ents.add_group
  grp.name = "LT Drum bottom cap"
  ge = grp.entities
  circle = ge.add_circle([0.mm,1181.mm,80.mm], [0,0,1], 432.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Beam End Cap (feed)"] || model.materials.add("Beam End Cap (feed)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum top shaft
  grp = ents.add_group
  grp.name = "LT Drum top shaft"
  ge = grp.entities
  circle = ge.add_circle([0.mm,1181.mm,2200.mm], [0,0,1], 37.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(65.mm)
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Upper bearing (SKF 6215)
  grp = ents.add_group
  grp.name = "LT Upper bearing (SKF 6215)"
  ge = grp.entities
  circle = ge.add_circle([0.mm,1181.mm,2200.mm], [0,0,1], 65.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(45.mm)
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Lower bearing collar
  grp = ents.add_group
  grp.name = "LT Lower bearing collar"
  ge = grp.entities
  circle = ge.add_circle([0.mm,1181.mm,80.mm], [0,0,1], 75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(45.mm)
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Lower bearing mount plate
  grp = ents.add_group
  grp.name = "LT Lower bearing mount plate"
  face = grp.entities.add_face([-120.mm,1061.mm,80.mm], [120.mm,1061.mm,80.mm], [120.mm,1301.mm,80.mm], [-120.mm,1301.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Grab rail
  grp = ents.add_group
  grp.name = "LT Grab rail"
  ge = grp.entities
  circle = ge.add_circle([357.mm,1181.mm,700.mm], [0,0,1], 15.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(400.mm)
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Grab rail standoff
  grp = ents.add_group
  grp.name = "LT Grab rail standoff"
  face = grp.entities.add_face([357.mm,1175.mm,720.mm], [429.mm,1175.mm,720.mm], [429.mm,1187.mm,720.mm], [357.mm,1187.mm,720.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Grab rail standoff
  grp = ents.add_group
  grp.name = "LT Grab rail standoff"
  face = grp.entities.add_face([357.mm,1175.mm,1080.mm], [429.mm,1175.mm,1080.mm], [429.mm,1187.mm,1080.mm], [357.mm,1187.mm,1080.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum opening brush seal
  grp = ents.add_group
  grp.name = "LT Drum opening brush seal"
  ge = grp.entities
  circle = ge.add_circle([-336.6765327507908.mm,1463.505154457234.mm,80.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2120.mm)
  mat = model.materials["LT Drum opening brush seal"] || model.materials.add("LT Drum opening brush seal")
  mat.color = Sketchup::Color.new(126, 126, 118)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum opening brush seal
  grp = ents.add_group
  grp.name = "LT Drum opening brush seal"
  ge = grp.entities
  circle = ge.add_circle([-336.6765327507909.mm,898.4948455427659.mm,80.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2120.mm)
  mat = model.materials["LT Drum opening brush seal"] || model.materials.add("LT Drum opening brush seal")
  mat.color = Sketchup::Color.new(126, 126, 118)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum top felt seal
  grp = ents.add_group
  grp.name = "LT Drum top felt seal"
  ge = grp.entities
  circle = ge.add_circle([0.mm,1181.mm,2192.mm], [0,0,1], 446.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(8.mm)
  mat = model.materials["LT Drum opening brush seal"] || model.materials.add("LT Drum opening brush seal")
  mat.color = Sketchup::Color.new(126, 126, 118)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum bottom felt seal
  grp = ents.add_group
  grp.name = "LT Drum bottom felt seal"
  ge = grp.entities
  circle = ge.add_circle([0.mm,1181.mm,80.mm], [0,0,1], 446.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(8.mm)
  mat = model.materials["LT Drum opening brush seal"] || model.materials.add("LT Drum opening brush seal")
  mat.color = Sketchup::Color.new(126, 126, 118)
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
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,900.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,920.1111111111111.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,940.2222222222222.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,960.3333333333334.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,980.4444444444445.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1000.5555555555555.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1020.6666666666666.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1040.7777777777778.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1060.888888888889.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1081.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1101.111111111111.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1121.2222222222222.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1141.3333333333333.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1161.4444444444443.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1181.5555555555557.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1201.6666666666667.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1221.7777777777778.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1241.888888888889.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1262.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1282.111111111111.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1302.2222222222222.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1322.3333333333333.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1342.4444444444443.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1362.5555555555557.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1382.6666666666665.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1402.7777777777778.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1422.888888888889.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1443.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1463.111111111111.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1483.2222222222222.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1503.3333333333335.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1523.4444444444443.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1543.5555555555557.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1563.6666666666665.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1583.7777777777778.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1603.888888888889.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1624.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1644.111111111111.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1664.2222222222222.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1684.3333333333335.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1704.4444444444443.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1724.5555555555557.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1744.6666666666665.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1764.7777777777778.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1784.888888888889.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1805.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1825.111111111111.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1845.2222222222222.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1865.3333333333333.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1885.4444444444443.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1905.5555555555557.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1925.6666666666667.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1945.7777777777778.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1965.888888888889.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1986.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2006.111111111111.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2026.2222222222222.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2046.3333333333333.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2066.4444444444443.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2086.5555555555557.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2106.666666666667.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2126.777777777778.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2146.8888888888887.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2167.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2187.1111111111113.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2207.222222222222.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2227.333333333333.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2247.4444444444443.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2267.5555555555557.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2287.666666666667.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2307.777777777778.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2327.8888888888887.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord Knob
  grp = ents.add_group
  grp.name = "Pull Cord Knob"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,884.mm], [0,0,1], 6.mm, 10)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
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
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,900.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,920.1111111111111.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,940.2222222222222.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,960.3333333333334.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,980.4444444444445.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1000.5555555555555.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1020.6666666666666.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1040.7777777777778.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1060.888888888889.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1081.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1101.111111111111.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1121.2222222222222.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1141.3333333333333.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1161.4444444444443.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1181.5555555555557.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1201.6666666666667.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1221.7777777777778.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1241.888888888889.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1262.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1282.111111111111.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1302.2222222222222.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1322.3333333333333.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1342.4444444444443.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1362.5555555555557.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1382.6666666666665.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1402.7777777777778.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1422.888888888889.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1443.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1463.111111111111.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1483.2222222222222.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1503.3333333333335.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1523.4444444444443.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1543.5555555555557.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1563.6666666666665.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1583.7777777777778.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1603.888888888889.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1624.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1644.111111111111.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1664.2222222222222.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1684.3333333333335.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1704.4444444444443.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1724.5555555555557.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1744.6666666666665.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1764.7777777777778.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1784.888888888889.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1805.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1825.111111111111.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1845.2222222222222.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1865.3333333333333.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1885.4444444444443.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1905.5555555555557.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1925.6666666666667.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1945.7777777777778.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1965.888888888889.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1986.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2006.111111111111.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2026.2222222222222.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2046.3333333333333.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2066.4444444444443.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2086.5555555555557.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2106.666666666667.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2126.777777777778.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2146.8888888888887.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2167.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2187.1111111111113.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2207.222222222222.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2227.333333333333.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2247.4444444444443.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2267.5555555555557.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2287.666666666667.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2307.777777777778.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2327.8888888888887.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.11111111111111.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord Knob
  grp = ents.add_group
  grp.name = "Pull Cord Knob"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,884.mm], [0,0,1], 6.mm, 10)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
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

  # Evap Flex Duct
  grp = ents.add_group
  grp.name = "Evap Flex Duct"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 74.43846153846152.mm)
  circle = ge.add_circle([1000.mm,-315.mm,800.mm], vec, 100.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Flex Duct
  grp = ents.add_group
  grp.name = "Evap Flex Duct"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 74.43846153846152.mm)
  circle = ge.add_circle([1000.mm,-315.mm,874.4384615384615.mm], vec, 80.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Flex Duct
  grp = ents.add_group
  grp.name = "Evap Flex Duct"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 74.43846153846152.mm)
  circle = ge.add_circle([1000.mm,-315.mm,948.876923076923.mm], vec, 100.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Flex Duct
  grp = ents.add_group
  grp.name = "Evap Flex Duct"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 74.43846153846152.mm)
  circle = ge.add_circle([1000.mm,-315.mm,1023.3153846153846.mm], vec, 80.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Flex Duct
  grp = ents.add_group
  grp.name = "Evap Flex Duct"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 74.43846153846152.mm)
  circle = ge.add_circle([1000.mm,-315.mm,1097.753846153846.mm], vec, 100.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Flex Duct
  grp = ents.add_group
  grp.name = "Evap Flex Duct"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 74.43846153846152.mm)
  circle = ge.add_circle([1000.mm,-315.mm,1172.1923076923076.mm], vec, 80.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Flex Duct
  grp = ents.add_group
  grp.name = "Evap Flex Duct"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 74.43846153846152.mm)
  circle = ge.add_circle([1000.mm,-315.mm,1246.6307692307691.mm], vec, 100.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Flex Duct
  grp = ents.add_group
  grp.name = "Evap Flex Duct"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 74.43846153846175.mm)
  circle = ge.add_circle([1000.mm,-315.mm,1321.0692307692307.mm], vec, 80.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Flex Duct
  grp = ents.add_group
  grp.name = "Evap Flex Duct"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 74.4384615384613.mm)
  circle = ge.add_circle([1000.mm,-315.mm,1395.5076923076924.mm], vec, 100.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Flex Duct
  grp = ents.add_group
  grp.name = "Evap Flex Duct"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 74.43846153846175.mm)
  circle = ge.add_circle([1000.mm,-315.mm,1469.9461538461537.mm], vec, 80.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Flex Duct
  grp = ents.add_group
  grp.name = "Evap Flex Duct"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 74.43846153846152.mm)
  circle = ge.add_circle([1000.mm,-315.mm,1544.3846153846155.mm], vec, 100.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Flex Duct
  grp = ents.add_group
  grp.name = "Evap Flex Duct"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 74.43846153846152.mm)
  circle = ge.add_circle([1000.mm,-315.mm,1618.823076923077.mm], vec, 80.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Flex Duct
  grp = ents.add_group
  grp.name = "Evap Flex Duct"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 74.43846153846152.mm)
  circle = ge.add_circle([1000.mm,-315.mm,1693.2615384615385.mm], vec, 100.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Flex Duct elbow
  grp = ents.add_group
  grp.name = "Evap Flex Duct elbow"
  ge = grp.entities
  arc = ge.add_arc([1000.mm,-182.69999999999996.mm,1767.7.mm], [0.000000,-1.000000,0.000000], [-1.000000,0.000000,0.000000], 132.30000000000004.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1000.mm,-315.mm,1767.7.mm], [0.000000,0.000000,1.000000], 100.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Flex Duct
  grp = ents.add_group
  grp.name = "Evap Flex Duct"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 17.212500000000006.mm, 0.mm)
  circle = ge.add_circle([1000.mm,-182.7.mm,1900.mm], vec, 100.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Flex Duct
  grp = ents.add_group
  grp.name = "Evap Flex Duct"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 17.212500000000006.mm, 0.mm)
  circle = ge.add_circle([1000.mm,-165.48749999999998.mm,1900.mm], vec, 80.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Flex Duct
  grp = ents.add_group
  grp.name = "Evap Flex Duct"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 17.212499999999977.mm, 0.mm)
  circle = ge.add_circle([1000.mm,-148.27499999999998.mm,1900.mm], vec, 100.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Flex Duct
  grp = ents.add_group
  grp.name = "Evap Flex Duct"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 17.212500000000006.mm, 0.mm)
  circle = ge.add_circle([1000.mm,-131.0625.mm,1900.mm], vec, 80.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Flex Duct
  grp = ents.add_group
  grp.name = "Evap Flex Duct"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 17.212500000000006.mm, 0.mm)
  circle = ge.add_circle([1000.mm,-113.85.mm,1900.mm], vec, 100.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Flex Duct
  grp = ents.add_group
  grp.name = "Evap Flex Duct"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 17.21249999999999.mm, 0.mm)
  circle = ge.add_circle([1000.mm,-96.63749999999999.mm,1900.mm], vec, 80.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Flex Duct
  grp = ents.add_group
  grp.name = "Evap Flex Duct"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 17.21249999999999.mm, 0.mm)
  circle = ge.add_circle([1000.mm,-79.425.mm,1900.mm], vec, 100.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cold-Air Duct Inlet (Ø200)"] || model.materials.add("Cold-Air Duct Inlet (Ø200)")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Flex Duct
  grp = ents.add_group
  grp.name = "Evap Flex Duct"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 17.212500000000006.mm, 0.mm)
  circle = ge.add_circle([1000.mm,-62.212500000000006.mm,1900.mm], vec, 80.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
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
  face = grp.entities.add_face([5689.mm,200.mm,2100.mm], [5697.mm,200.mm,2100.mm], [5697.mm,325.mm,2100.mm], [5689.mm,325.mm,2100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) baffle plate 2
  grp = ents.add_group
  grp.name = "Fan A (exhaust) baffle plate 2"
  face = grp.entities.add_face([5789.mm,275.mm,2100.mm], [5797.mm,275.mm,2100.mm], [5797.mm,400.mm,2100.mm], [5789.mm,400.mm,2100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan frame top
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan frame top"
  face = grp.entities.add_face([5593.mm,200.mm,2275.mm], [5643.mm,200.mm,2275.mm], [5643.mm,400.mm,2275.mm], [5593.mm,400.mm,2275.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan frame bottom
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan frame bottom"
  face = grp.entities.add_face([5593.mm,200.mm,2100.mm], [5643.mm,200.mm,2100.mm], [5643.mm,400.mm,2100.mm], [5593.mm,400.mm,2100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan frame left
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan frame left"
  face = grp.entities.add_face([5593.mm,200.mm,2125.mm], [5643.mm,200.mm,2125.mm], [5643.mm,225.mm,2125.mm], [5593.mm,225.mm,2125.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan frame right
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan frame right"
  face = grp.entities.add_face([5593.mm,375.mm,2125.mm], [5643.mm,375.mm,2125.mm], [5643.mm,400.mm,2125.mm], [5593.mm,400.mm,2125.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan hub
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan hub"
  ge = grp.entities
  circle = ge.add_circle([5593.mm,300.mm,2200.mm], [1,0,0], 19.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(50.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan blade up
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan blade up"
  face = grp.entities.add_face([5615.5.mm,285.mm,2219.5.mm], [5621.5.mm,285.mm,2219.5.mm], [5621.5.mm,315.mm,2219.5.mm], [5615.5.mm,315.mm,2219.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.5.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan blade down
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan blade down"
  face = grp.entities.add_face([5615.5.mm,285.mm,2134.mm], [5621.5.mm,285.mm,2134.mm], [5621.5.mm,315.mm,2134.mm], [5615.5.mm,315.mm,2134.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.5.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan blade left
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan blade left"
  face = grp.entities.add_face([5615.5.mm,234.mm,2185.mm], [5621.5.mm,234.mm,2185.mm], [5621.5.mm,280.5.mm,2185.mm], [5615.5.mm,280.5.mm,2185.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan blade right
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan blade right"
  face = grp.entities.add_face([5615.5.mm,319.5.mm,2185.mm], [5621.5.mm,319.5.mm,2185.mm], [5621.5.mm,366.mm,2185.mm], [5615.5.mm,366.mm,2185.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) wall flange
  grp = ents.add_group
  grp.name = "Fan A (exhaust) wall flange"
  face = grp.entities.add_face([5888.mm,170.mm,2070.mm], [5893.mm,170.mm,2070.mm], [5893.mm,430.mm,2070.mm], [5888.mm,430.mm,2070.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(260.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) flange bolt M10
  grp = ents.add_group
  grp.name = "Fan A (exhaust) flange bolt M10"
  ge = grp.entities
  circle = ge.add_circle([5886.5.mm,185.mm,2085.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(13.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) flange bolt M10
  grp = ents.add_group
  grp.name = "Fan A (exhaust) flange bolt M10"
  ge = grp.entities
  circle = ge.add_circle([5886.5.mm,185.mm,2315.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(13.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) flange bolt M10
  grp = ents.add_group
  grp.name = "Fan A (exhaust) flange bolt M10"
  ge = grp.entities
  circle = ge.add_circle([5886.5.mm,415.mm,2085.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(13.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) flange bolt M10
  grp = ents.add_group
  grp.name = "Fan A (exhaust) flange bolt M10"
  ge = grp.entities
  circle = ge.add_circle([5886.5.mm,415.mm,2315.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(13.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) louvre grille
  grp = ents.add_group
  grp.name = "Fan A (exhaust) louvre grille"
  face = grp.entities.add_face([5893.mm,200.mm,2135.mm], [5933.mm,200.mm,2135.mm], [5933.mm,400.mm,2135.mm], [5893.mm,400.mm,2135.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(130.mm)
  mat = model.materials["Fan A (exhaust) louvre grille"] || model.materials.add("Fan A (exhaust) louvre grille")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 0.55
  grp.material = mat

  # Fan A (exhaust) louvre slat
  grp = ents.add_group
  grp.name = "Fan A (exhaust) louvre slat"
  face = grp.entities.add_face([5895.mm,204.mm,2146.5.mm], [5931.mm,204.mm,2146.5.mm], [5931.mm,396.mm,2146.5.mm], [5895.mm,396.mm,2146.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) louvre slat
  grp = ents.add_group
  grp.name = "Fan A (exhaust) louvre slat"
  face = grp.entities.add_face([5895.mm,204.mm,2172.5.mm], [5931.mm,204.mm,2172.5.mm], [5931.mm,396.mm,2172.5.mm], [5895.mm,396.mm,2172.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) louvre slat
  grp = ents.add_group
  grp.name = "Fan A (exhaust) louvre slat"
  face = grp.entities.add_face([5895.mm,204.mm,2198.5.mm], [5931.mm,204.mm,2198.5.mm], [5931.mm,396.mm,2198.5.mm], [5895.mm,396.mm,2198.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) louvre slat
  grp = ents.add_group
  grp.name = "Fan A (exhaust) louvre slat"
  face = grp.entities.add_face([5895.mm,204.mm,2224.5.mm], [5931.mm,204.mm,2224.5.mm], [5931.mm,396.mm,2224.5.mm], [5895.mm,396.mm,2224.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) louvre slat
  grp = ents.add_group
  grp.name = "Fan A (exhaust) louvre slat"
  face = grp.entities.add_face([5895.mm,204.mm,2250.5.mm], [5931.mm,204.mm,2250.5.mm], [5931.mm,396.mm,2250.5.mm], [5895.mm,396.mm,2250.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) baffle duct
  grp = ents.add_group
  grp.name = "Fan B (intake) baffle duct"
  face = grp.entities.add_face([0.mm,1896.mm,500.mm], [300.mm,1896.mm,500.mm], [300.mm,2096.mm,500.mm], [0.mm,2096.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan A (exhaust) baffle duct"] || model.materials.add("Fan A (exhaust) baffle duct")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 0.5
  grp.material = mat

  # Fan B (intake) baffle plate 1
  grp = ents.add_group
  grp.name = "Fan B (intake) baffle plate 1"
  face = grp.entities.add_face([96.mm,1896.mm,500.mm], [104.mm,1896.mm,500.mm], [104.mm,2021.mm,500.mm], [96.mm,2021.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) baffle plate 2
  grp = ents.add_group
  grp.name = "Fan B (intake) baffle plate 2"
  face = grp.entities.add_face([196.mm,1971.mm,500.mm], [204.mm,1971.mm,500.mm], [204.mm,2096.mm,500.mm], [196.mm,2096.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan frame top
  grp = ents.add_group
  grp.name = "Fan B (intake) fan frame top"
  face = grp.entities.add_face([250.mm,1896.mm,675.mm], [300.mm,1896.mm,675.mm], [300.mm,2096.mm,675.mm], [250.mm,2096.mm,675.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan frame bottom
  grp = ents.add_group
  grp.name = "Fan B (intake) fan frame bottom"
  face = grp.entities.add_face([250.mm,1896.mm,500.mm], [300.mm,1896.mm,500.mm], [300.mm,2096.mm,500.mm], [250.mm,2096.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan frame left
  grp = ents.add_group
  grp.name = "Fan B (intake) fan frame left"
  face = grp.entities.add_face([250.mm,1896.mm,525.mm], [300.mm,1896.mm,525.mm], [300.mm,1921.mm,525.mm], [250.mm,1921.mm,525.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan frame right
  grp = ents.add_group
  grp.name = "Fan B (intake) fan frame right"
  face = grp.entities.add_face([250.mm,2071.mm,525.mm], [300.mm,2071.mm,525.mm], [300.mm,2096.mm,525.mm], [250.mm,2096.mm,525.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan hub
  grp = ents.add_group
  grp.name = "Fan B (intake) fan hub"
  ge = grp.entities
  circle = ge.add_circle([250.mm,1996.mm,600.mm], [1,0,0], 19.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(50.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade up
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade up"
  face = grp.entities.add_face([272.5.mm,1981.mm,619.5.mm], [278.5.mm,1981.mm,619.5.mm], [278.5.mm,2011.mm,619.5.mm], [272.5.mm,2011.mm,619.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.5.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade down
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade down"
  face = grp.entities.add_face([272.5.mm,1981.mm,534.mm], [278.5.mm,1981.mm,534.mm], [278.5.mm,2011.mm,534.mm], [272.5.mm,2011.mm,534.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.5.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade left
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade left"
  face = grp.entities.add_face([272.5.mm,1930.mm,585.mm], [278.5.mm,1930.mm,585.mm], [278.5.mm,1976.5.mm,585.mm], [272.5.mm,1976.5.mm,585.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade right
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade right"
  face = grp.entities.add_face([272.5.mm,2015.5.mm,585.mm], [278.5.mm,2015.5.mm,585.mm], [278.5.mm,2062.mm,585.mm], [272.5.mm,2062.mm,585.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) wall flange
  grp = ents.add_group
  grp.name = "Fan B (intake) wall flange"
  face = grp.entities.add_face([0.mm,1866.mm,470.mm], [5.mm,1866.mm,470.mm], [5.mm,2126.mm,470.mm], [0.mm,2126.mm,470.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(260.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) flange bolt M10
  grp = ents.add_group
  grp.name = "Fan B (intake) flange bolt M10"
  ge = grp.entities
  circle = ge.add_circle([-6.5.mm,1881.mm,485.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(13.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) flange bolt M10
  grp = ents.add_group
  grp.name = "Fan B (intake) flange bolt M10"
  ge = grp.entities
  circle = ge.add_circle([-6.5.mm,1881.mm,715.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(13.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) flange bolt M10
  grp = ents.add_group
  grp.name = "Fan B (intake) flange bolt M10"
  ge = grp.entities
  circle = ge.add_circle([-6.5.mm,2111.mm,485.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(13.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) flange bolt M10
  grp = ents.add_group
  grp.name = "Fan B (intake) flange bolt M10"
  ge = grp.entities
  circle = ge.add_circle([-6.5.mm,2111.mm,715.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(13.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre grille
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre grille"
  face = grp.entities.add_face([-40.mm,1896.mm,535.mm], [0.mm,1896.mm,535.mm], [0.mm,2096.mm,535.mm], [-40.mm,2096.mm,535.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(130.mm)
  mat = model.materials["Fan A (exhaust) louvre grille"] || model.materials.add("Fan A (exhaust) louvre grille")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 0.55
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,1900.mm,546.5.mm], [-2.mm,1900.mm,546.5.mm], [-2.mm,2092.mm,546.5.mm], [-38.mm,2092.mm,546.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,1900.mm,572.5.mm], [-2.mm,1900.mm,572.5.mm], [-2.mm,2092.mm,572.5.mm], [-38.mm,2092.mm,572.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,1900.mm,598.5.mm], [-2.mm,1900.mm,598.5.mm], [-2.mm,2092.mm,598.5.mm], [-38.mm,2092.mm,598.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,1900.mm,624.5.mm], [-2.mm,1900.mm,624.5.mm], [-2.mm,2092.mm,624.5.mm], [-38.mm,2092.mm,624.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,1900.mm,650.5.mm], [-2.mm,1900.mm,650.5.mm], [-2.mm,2092.mm,650.5.mm], [-38.mm,2092.mm,650.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Pinhole Mount Plate"] || model.materials.add("Pinhole Mount Plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
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

  # P-05 → X3 (Brown drain-out)
  grp = ents.add_group
  grp.name = "P-05 → X3 (Brown drain-out)"
  ge = grp.entities
  vec = Geom::Vector3d.new(156.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5220.mm,1253.mm,1946.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 → X3 (Brown drain-out) elbow
  grp = ents.add_group
  grp.name = "P-05 → X3 (Brown drain-out) elbow"
  ge = grp.entities
  arc = ge.add_arc([5376.mm,1253.mm,1922.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5376.mm,1253.mm,1946.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 → X3 (Brown drain-out)
  grp = ents.add_group
  grp.name = "P-05 → X3 (Brown drain-out)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1498.mm)
  circle = ge.add_circle([5400.mm,1253.mm,1922.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 → X3 (Brown drain-out) elbow
  grp = ents.add_group
  grp.name = "P-05 → X3 (Brown drain-out) elbow"
  ge = grp.entities
  arc = ge.add_arc([5400.mm,1229.mm,424.mm], [0.000000,1.000000,0.000000], [-1.000000,-0.000000,-0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5400.mm,1253.mm,424.mm], [0.000000,0.000000,-1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 → X3 (Brown drain-out)
  grp = ents.add_group
  grp.name = "P-05 → X3 (Brown drain-out)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -24.480000000000018.mm, 0.mm)
  circle = ge.add_circle([5400.mm,1229.mm,400.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 → X3 (Brown drain-out) elbow
  grp = ents.add_group
  grp.name = "P-05 → X3 (Brown drain-out) elbow"
  ge = grp.entities
  arc = ge.add_arc([5423.52.mm,1204.52.mm,400.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.000000,1.000000], 23.520000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5400.mm,1204.52.mm,400.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 → X3 (Brown drain-out)
  grp = ents.add_group
  grp.name = "P-05 → X3 (Brown drain-out)"
  ge = grp.entities
  vec = Geom::Vector3d.new(469.47999999999956.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5423.52.mm,1181.mm,400.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 → X4 (Waste drain-out)
  grp = ents.add_group
  grp.name = "P-03 → X4 (Waste drain-out)"
  ge = grp.entities
  vec = Geom::Vector3d.new(96.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5220.mm,1253.mm,1578.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 → X4 (Waste drain-out) elbow
  grp = ents.add_group
  grp.name = "P-03 → X4 (Waste drain-out) elbow"
  ge = grp.entities
  arc = ge.add_arc([5316.mm,1253.mm,1554.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5316.mm,1253.mm,1578.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 → X4 (Waste drain-out)
  grp = ents.add_group
  grp.name = "P-03 → X4 (Waste drain-out)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1330.mm)
  circle = ge.add_circle([5340.mm,1253.mm,1554.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 → X4 (Waste drain-out) elbow
  grp = ents.add_group
  grp.name = "P-03 → X4 (Waste drain-out) elbow"
  ge = grp.entities
  arc = ge.add_arc([5340.mm,1229.mm,224.mm], [0.000000,1.000000,0.000000], [-1.000000,-0.000000,-0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5340.mm,1253.mm,224.mm], [0.000000,0.000000,-1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 → X4 (Waste drain-out)
  grp = ents.add_group
  grp.name = "P-03 → X4 (Waste drain-out)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -24.480000000000018.mm, 0.mm)
  circle = ge.add_circle([5340.mm,1229.mm,200.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 → X4 (Waste drain-out) elbow
  grp = ents.add_group
  grp.name = "P-03 → X4 (Waste drain-out) elbow"
  ge = grp.entities
  arc = ge.add_arc([5363.52.mm,1204.52.mm,200.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.000000,1.000000], 23.520000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5340.mm,1204.52.mm,200.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 → X4 (Waste drain-out)
  grp = ents.add_group
  grp.name = "P-03 → X4 (Waste drain-out)"
  ge = grp.entities
  vec = Geom::Vector3d.new(529.4799999999996.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5363.52.mm,1181.mm,200.mm], vec, 12.mm, 16)
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
