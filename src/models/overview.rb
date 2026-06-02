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
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Container Ceiling
  grp = ents.add_group
  grp.name = "Container Ceiling"
  face = grp.entities.add_face([0.mm,0.mm,2388.mm], [5893.mm,0.mm,2388.mm], [5893.mm,2362.mm,2388.mm], [0.mm,2362.mm,2388.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Container Ceiling"] || model.materials.add("Container Ceiling")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.2
  grp.material = mat

  # Pinhole Wall (Yd=0)
  grp = ents.add_group
  grp.name = "Pinhole Wall (Yd=0)"
  face = grp.entities.add_face([0.mm,-40.mm,0.mm], [5893.mm,-40.mm,0.mm], [5893.mm,0.mm,0.mm], [0.mm,0.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Pinhole Wall (Yd=0)"] || model.materials.add("Pinhole Wall (Yd=0)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Film Plane Wall (Yd=max)
  grp = ents.add_group
  grp.name = "Film Plane Wall (Yd=max)"
  face = grp.entities.add_face([0.mm,2362.mm,0.mm], [5893.mm,2362.mm,0.mm], [5893.mm,2402.mm,0.mm], [0.mm,2402.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Film Plane Wall (Yd=max)"] || model.materials.add("Film Plane Wall (Yd=max)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Far End Wall (IBC end)
  grp = ents.add_group
  grp.name = "Far End Wall (IBC end)"
  face = grp.entities.add_face([5893.mm,0.mm,0.mm], [5933.mm,0.mm,0.mm], [5933.mm,2362.mm,0.mm], [5893.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Far End Wall (IBC end)"] || model.materials.add("Far End Wall (IBC end)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Container Shell"
  inst.layer = model.layers["Shell"]

  # ═══ Walkways ═══
  defn = model.definitions.add("Walkways")
  ents = defn.entities
  # Walkway Near left (DROPPED)
  grp = ents.add_group
  grp.name = "Walkway Near left (DROPPED)"
  face = grp.entities.add_face([470.mm,0.mm,75.mm], [1155.mm,0.mm,75.mm], [1155.mm,300.mm,75.mm], [470.mm,300.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near left (DROPPED)"] || model.materials.add("Walkway Near left (DROPPED)")
  mat.color = Sketchup::Color.new(204, 68, 34)
  mat.alpha = 0.3
  grp.material = mat

  # Walkway Near widened (DROPPED)
  grp = ents.add_group
  grp.name = "Walkway Near widened (DROPPED)"
  face = grp.entities.add_face([1155.mm,0.mm,75.mm], [2629.mm,0.mm,75.mm], [2629.mm,500.mm,75.mm], [1155.mm,500.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near widened (DROPPED)"] || model.materials.add("Walkway Near widened (DROPPED)")
  mat.color = Sketchup::Color.new(204, 68, 34)
  mat.alpha = 0.3
  grp.material = mat

  # Walkway Near right (DROPPED)
  grp = ents.add_group
  grp.name = "Walkway Near right (DROPPED)"
  face = grp.entities.add_face([2629.mm,0.mm,75.mm], [4329.mm,0.mm,75.mm], [4329.mm,300.mm,75.mm], [2629.mm,300.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near right (DROPPED)"] || model.materials.add("Walkway Near right (DROPPED)")
  mat.color = Sketchup::Color.new(204, 68, 34)
  mat.alpha = 0.3
  grp.material = mat

  # Walkway Far (DROPPED)
  grp = ents.add_group
  grp.name = "Walkway Far (DROPPED)"
  face = grp.entities.add_face([470.mm,2062.mm,75.mm], [4329.mm,2062.mm,75.mm], [4329.mm,2362.mm,75.mm], [470.mm,2362.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Far (DROPPED)"] || model.materials.add("Walkway Far (DROPPED)")
  mat.color = Sketchup::Color.new(204, 68, 34)
  mat.alpha = 0.3
  grp.material = mat

  # Walkway Right IBC end (DROPPED)
  grp = ents.add_group
  grp.name = "Walkway Right IBC end (DROPPED)"
  face = grp.entities.add_face([4329.mm,0.mm,75.mm], [4629.mm,0.mm,75.mm], [4629.mm,2362.mm,75.mm], [4329.mm,2362.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Right IBC end (DROPPED)"] || model.materials.add("Walkway Right IBC end (DROPPED)")
  mat.color = Sketchup::Color.new(204, 68, 34)
  mat.alpha = 0.3
  grp.material = mat

  # Walkway Left cargo door (DROPPED)
  grp = ents.add_group
  grp.name = "Walkway Left cargo door (DROPPED)"
  face = grp.entities.add_face([170.mm,0.mm,75.mm], [470.mm,0.mm,75.mm], [470.mm,2362.mm,75.mm], [170.mm,2362.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Left cargo door (DROPPED)"] || model.materials.add("Walkway Left cargo door (DROPPED)")
  mat.color = Sketchup::Color.new(204, 68, 34)
  mat.alpha = 0.3
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
  mat.color = Sketchup::Color.new(232, 245, 233)
  mat.alpha = 0.5
  grp.material = mat

  # Tray Rim Near
  grp = ents.add_group
  grp.name = "Tray Rim Near"
  face = grp.entities.add_face([170.mm,80.mm,2.mm], [4629.mm,80.mm,2.mm], [4629.mm,82.mm,2.mm], [170.mm,82.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Tray Rim Near"] || model.materials.add("Tray Rim Near")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Tray Rim Far
  grp = ents.add_group
  grp.name = "Tray Rim Far"
  face = grp.entities.add_face([170.mm,2278.mm,2.mm], [4629.mm,2278.mm,2.mm], [4629.mm,2280.mm,2.mm], [170.mm,2280.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Tray Rim Far"] || model.materials.add("Tray Rim Far")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Tray Rim Left
  grp = ents.add_group
  grp.name = "Tray Rim Left"
  face = grp.entities.add_face([170.mm,80.mm,2.mm], [172.mm,80.mm,2.mm], [172.mm,2280.mm,2.mm], [170.mm,2280.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Tray Rim Left"] || model.materials.add("Tray Rim Left")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Tray Rim Right
  grp = ents.add_group
  grp.name = "Tray Rim Right"
  face = grp.entities.add_face([4627.mm,80.mm,2.mm], [4629.mm,80.mm,2.mm], [4629.mm,2280.mm,2.mm], [4627.mm,2280.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Tray Rim Right"] || model.materials.add("Tray Rim Right")
  mat.color = Sketchup::Color.new(176, 176, 184)
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
  grp.material = mat

  # Pinhole Aperture (Ø2.17)
  grp = ents.add_group
  grp.name = "Pinhole Aperture (Ø2.17)"
  face = grp.entities.add_face([2397.915.mm,3.mm,1192.915.mm], [2400.085.mm,3.mm,1192.915.mm], [2400.085.mm,4.mm,1192.915.mm], [2397.915.mm,4.mm,1192.915.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.17.mm)
  mat = model.materials["Pinhole Aperture (Ø2.17)"] || model.materials.add("Pinhole Aperture (Ø2.17)")
  mat.color = Sketchup::Color.new(204, 102, 0)
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
  mat = model.materials["FP Rail BR"] || model.materials.add("FP Rail BR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # FP Rail TR
  grp = ents.add_group
  grp.name = "FP Rail TR"
  face = grp.entities.add_face([4609.mm,100.mm,2248.mm], [4649.mm,100.mm,2248.mm], [4649.mm,2300.mm,2248.mm], [4609.mm,2300.mm,2248.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["FP Rail TR"] || model.materials.add("FP Rail TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # FP Rail BL (fixed near)
  grp = ents.add_group
  grp.name = "FP Rail BL (fixed near)"
  face = grp.entities.add_face([150.mm,100.mm,100.mm], [190.mm,100.mm,100.mm], [190.mm,806.mm,100.mm], [150.mm,806.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["FP Rail BL (fixed near)"] || model.materials.add("FP Rail BL (fixed near)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # FP Rail BL (DEMOUNTABLE — drum mode)
  grp = ents.add_group
  grp.name = "FP Rail BL (DEMOUNTABLE — drum mode)"
  face = grp.entities.add_face([150.mm,806.mm,100.mm], [190.mm,806.mm,100.mm], [190.mm,1556.mm,100.mm], [150.mm,1556.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["FP Rail BL (DEMOUNTABLE — drum mode)"] || model.materials.add("FP Rail BL (DEMOUNTABLE — drum mode)")
  mat.color = Sketchup::Color.new(224, 144, 42)
  grp.material = mat

  # FP Rail BL (fixed far)
  grp = ents.add_group
  grp.name = "FP Rail BL (fixed far)"
  face = grp.entities.add_face([150.mm,1556.mm,100.mm], [190.mm,1556.mm,100.mm], [190.mm,2300.mm,100.mm], [150.mm,2300.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["FP Rail BL (fixed far)"] || model.materials.add("FP Rail BL (fixed far)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # FP Rail TL (fixed near)
  grp = ents.add_group
  grp.name = "FP Rail TL (fixed near)"
  face = grp.entities.add_face([150.mm,100.mm,2248.mm], [190.mm,100.mm,2248.mm], [190.mm,806.mm,2248.mm], [150.mm,806.mm,2248.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["FP Rail TL (fixed near)"] || model.materials.add("FP Rail TL (fixed near)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # FP Rail TL (DEMOUNTABLE — drum mode)
  grp = ents.add_group
  grp.name = "FP Rail TL (DEMOUNTABLE — drum mode)"
  face = grp.entities.add_face([150.mm,806.mm,2248.mm], [190.mm,806.mm,2248.mm], [190.mm,1556.mm,2248.mm], [150.mm,1556.mm,2248.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["FP Rail TL (DEMOUNTABLE — drum mode)"] || model.materials.add("FP Rail TL (DEMOUNTABLE — drum mode)")
  mat.color = Sketchup::Color.new(224, 144, 42)
  grp.material = mat

  # FP Rail TL (fixed far)
  grp = ents.add_group
  grp.name = "FP Rail TL (fixed far)"
  face = grp.entities.add_face([150.mm,1556.mm,2248.mm], [190.mm,1556.mm,2248.mm], [190.mm,2300.mm,2248.mm], [150.mm,2300.mm,2248.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["FP Rail TL (fixed far)"] || model.materials.add("FP Rail TL (fixed far)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # FP Brace Vert L (pinhole)
  grp = ents.add_group
  grp.name = "FP Brace Vert L (pinhole)"
  face = grp.entities.add_face([150.mm,100.mm,100.mm], [200.mm,100.mm,100.mm], [200.mm,150.mm,100.mm], [150.mm,150.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2188.mm)
  mat = model.materials["FP Brace Vert L (pinhole)"] || model.materials.add("FP Brace Vert L (pinhole)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # FP Brace Vert R (pinhole)
  grp = ents.add_group
  grp.name = "FP Brace Vert R (pinhole)"
  face = grp.entities.add_face([4599.mm,100.mm,100.mm], [4649.mm,100.mm,100.mm], [4649.mm,150.mm,100.mm], [4599.mm,150.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2188.mm)
  mat = model.materials["FP Brace Vert R (pinhole)"] || model.materials.add("FP Brace Vert R (pinhole)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # FP Brace Beam Bottom (pinhole)
  grp = ents.add_group
  grp.name = "FP Brace Beam Bottom (pinhole)"
  face = grp.entities.add_face([150.mm,100.mm,100.mm], [4649.mm,100.mm,100.mm], [4649.mm,150.mm,100.mm], [150.mm,150.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["FP Brace Beam Bottom (pinhole)"] || model.materials.add("FP Brace Beam Bottom (pinhole)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # FP Brace Beam Top (pinhole)
  grp = ents.add_group
  grp.name = "FP Brace Beam Top (pinhole)"
  face = grp.entities.add_face([150.mm,100.mm,2238.mm], [4649.mm,100.mm,2238.mm], [4649.mm,150.mm,2238.mm], [150.mm,150.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["FP Brace Beam Top (pinhole)"] || model.materials.add("FP Brace Beam Top (pinhole)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # FP Brace Vert L (film)
  grp = ents.add_group
  grp.name = "FP Brace Vert L (film)"
  face = grp.entities.add_face([150.mm,2262.mm,100.mm], [200.mm,2262.mm,100.mm], [200.mm,2312.mm,100.mm], [150.mm,2312.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2188.mm)
  mat = model.materials["FP Brace Vert L (film)"] || model.materials.add("FP Brace Vert L (film)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # FP Brace Vert R (film)
  grp = ents.add_group
  grp.name = "FP Brace Vert R (film)"
  face = grp.entities.add_face([4599.mm,2262.mm,100.mm], [4649.mm,2262.mm,100.mm], [4649.mm,2312.mm,100.mm], [4599.mm,2312.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2188.mm)
  mat = model.materials["FP Brace Vert R (film)"] || model.materials.add("FP Brace Vert R (film)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # FP Brace Beam Bottom (film)
  grp = ents.add_group
  grp.name = "FP Brace Beam Bottom (film)"
  face = grp.entities.add_face([150.mm,2262.mm,100.mm], [4649.mm,2262.mm,100.mm], [4649.mm,2312.mm,100.mm], [150.mm,2312.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["FP Brace Beam Bottom (film)"] || model.materials.add("FP Brace Beam Bottom (film)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # FP Brace Beam Top (film)
  grp = ents.add_group
  grp.name = "FP Brace Beam Top (film)"
  face = grp.entities.add_face([150.mm,2262.mm,2238.mm], [4649.mm,2262.mm,2238.mm], [4649.mm,2312.mm,2238.mm], [150.mm,2312.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["FP Brace Beam Top (film)"] || model.materials.add("FP Brace Beam Top (film)")
  mat.color = Sketchup::Color.new(176, 176, 184)
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
  mat = model.materials["FP Frame Bottom"] || model.materials.add("FP Frame Bottom")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # FP Frame Top
  grp = ents.add_group
  grp.name = "FP Frame Top"
  face = grp.entities.add_face([150.mm,2211.2.mm,2337.2.mm], [4649.mm,2211.2.mm,2337.2.mm], [4649.mm,2262.mm,2337.2.mm], [150.mm,2262.mm,2337.2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["FP Frame Top"] || model.materials.add("FP Frame Top")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # FP Frame Left
  grp = ents.add_group
  grp.name = "FP Frame Left"
  face = grp.entities.add_face([150.mm,2211.2.mm,0.mm], [200.8.mm,2211.2.mm,0.mm], [200.8.mm,2262.mm,0.mm], [150.mm,2262.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["FP Frame Left"] || model.materials.add("FP Frame Left")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # FP Frame Right
  grp = ents.add_group
  grp.name = "FP Frame Right"
  face = grp.entities.add_face([4598.2.mm,2211.2.mm,0.mm], [4649.mm,2211.2.mm,0.mm], [4649.mm,2262.mm,0.mm], [4598.2.mm,2262.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["FP Frame Right"] || model.materials.add("FP Frame Right")
  mat.color = Sketchup::Color.new(176, 176, 184)
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
  grp.material = mat

  # Carriage L (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage L (HGH20CA)"
  face = grp.entities.add_face([38.mm,734.mm,2330.mm], [82.mm,734.mm,2330.mm], [82.mm,778.mm,2330.mm], [38.mm,778.mm,2330.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Carriage L (HGH20CA)"] || model.materials.add("Carriage L (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  grp.material = mat

  # Suspension Bracket L
  grp = ents.add_group
  grp.name = "Suspension Bracket L"
  face = grp.entities.add_face([30.mm,736.mm,2290.mm], [90.mm,736.mm,2290.mm], [90.mm,776.mm,2290.mm], [30.mm,776.mm,2290.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Suspension Bracket L"] || model.materials.add("Suspension Bracket L")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # HGR20 Rail R
  grp = ents.add_group
  grp.name = "HGR20 Rail R"
  face = grp.entities.add_face([-30.mm,1596.mm,2358.mm], [480.mm,1596.mm,2358.mm], [480.mm,1616.mm,2358.mm], [-30.mm,1616.mm,2358.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["HGR20 Rail R"] || model.materials.add("HGR20 Rail R")
  mat.color = Sketchup::Color.new(96, 96, 104)
  grp.material = mat

  # Carriage R (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage R (HGH20CA)"
  face = grp.entities.add_face([38.mm,1584.mm,2330.mm], [82.mm,1584.mm,2330.mm], [82.mm,1628.mm,2330.mm], [38.mm,1628.mm,2330.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Carriage R (HGH20CA)"] || model.materials.add("Carriage R (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  grp.material = mat

  # Suspension Bracket R
  grp = ents.add_group
  grp.name = "Suspension Bracket R"
  face = grp.entities.add_face([30.mm,1586.mm,2290.mm], [90.mm,1586.mm,2290.mm], [90.mm,1626.mm,2290.mm], [30.mm,1626.mm,2290.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Suspension Bracket R"] || model.materials.add("Suspension Bracket R")
  mat.color = Sketchup::Color.new(176, 176, 184)
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
  face = grp.entities.add_face([200.mm,1160.mm,10.mm], [4599.mm,1160.mm,10.mm], [4599.mm,1200.mm,10.mm], [200.mm,1200.mm,10.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Spray Bar Beam"] || model.materials.add("Spray Bar Beam")
  mat.color = Sketchup::Color.new(200, 216, 232)
  grp.material = mat

  # Spray Bar Carriage
  grp = ents.add_group
  grp.name = "Spray Bar Carriage"
  face = grp.entities.add_face([200.mm,1135.mm,5.mm], [250.mm,1135.mm,5.mm], [250.mm,1225.mm,5.mm], [200.mm,1225.mm,5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(55.mm)
  mat = model.materials["Spray Bar Carriage"] || model.materials.add("Spray Bar Carriage")
  mat.color = Sketchup::Color.new(192, 64, 16)
  grp.material = mat

  # Spray Bar Carriage
  grp = ents.add_group
  grp.name = "Spray Bar Carriage"
  face = grp.entities.add_face([4549.mm,1135.mm,5.mm], [4599.mm,1135.mm,5.mm], [4599.mm,1225.mm,5.mm], [4549.mm,1225.mm,5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(55.mm)
  mat = model.materials["Spray Bar Carriage"] || model.materials.add("Spray Bar Carriage")
  mat.color = Sketchup::Color.new(192, 64, 16)
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
  face = grp.entities.add_face([5000.mm,1046.mm,200.mm], [5018.mm,1046.mm,200.mm], [5018.mm,1316.mm,200.mm], [5000.mm,1316.mm,200.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2060.mm)
  mat = model.materials["Equipment Panel (ply)"] || model.materials.add("Equipment Panel (ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  grp.material = mat

  # Pump P-01 (Blue)
  grp = ents.add_group
  grp.name = "Pump P-01 (Blue)"
  face = grp.entities.add_face([4900.mm,1045.5.mm,1320.mm], [5000.mm,1045.5.mm,1320.mm], [5000.mm,1172.5.mm,1320.mm], [4900.mm,1172.5.mm,1320.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  grp.material = mat

  # Pump P-02 (Brown)
  grp = ents.add_group
  grp.name = "Pump P-02 (Brown)"
  face = grp.entities.add_face([4900.mm,1189.5.mm,1320.mm], [5000.mm,1189.5.mm,1320.mm], [5000.mm,1316.5.mm,1320.mm], [4900.mm,1316.5.mm,1320.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-02 (Brown)"] || model.materials.add("Pump P-02 (Brown)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  grp.material = mat

  # Pump P-04 (Tray drain)
  grp = ents.add_group
  grp.name = "Pump P-04 (Tray drain)"
  face = grp.entities.add_face([4900.mm,1045.5.mm,1578.mm], [5000.mm,1045.5.mm,1578.mm], [5000.mm,1172.5.mm,1578.mm], [4900.mm,1172.5.mm,1578.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-04 (Tray drain)"] || model.materials.add("Pump P-04 (Tray drain)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  grp.material = mat

  # Pump P-03 (Waste evac)
  grp = ents.add_group
  grp.name = "Pump P-03 (Waste evac)"
  face = grp.entities.add_face([4900.mm,1189.5.mm,1578.mm], [5000.mm,1189.5.mm,1578.mm], [5000.mm,1316.5.mm,1578.mm], [4900.mm,1316.5.mm,1578.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-03 (Waste evac)"] || model.materials.add("Pump P-03 (Waste evac)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  grp.material = mat

  # Pump P-05 (Brown drain)
  grp = ents.add_group
  grp.name = "Pump P-05 (Brown drain)"
  face = grp.entities.add_face([4900.mm,1189.5.mm,1946.mm], [5000.mm,1189.5.mm,1946.mm], [5000.mm,1316.5.mm,1946.mm], [4900.mm,1316.5.mm,1946.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-05 (Brown drain)"] || model.materials.add("Pump P-05 (Brown drain)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  grp.material = mat

  # ACC-01 Accumulator
  grp = ents.add_group
  grp.name = "ACC-01 Accumulator"
  ge = grp.entities
  circle = ge.add_circle([4937.mm,1109.mm,1946.mm], [0,0,1], 63.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(150.mm)
  mat = model.materials["ACC-01 Accumulator"] || model.materials.add("ACC-01 Accumulator")
  mat.color = Sketchup::Color.new(90, 154, 204)
  grp.material = mat

  # Filter F1 (50µ)
  grp = ents.add_group
  grp.name = "Filter F1 (50µ)"
  ge = grp.entities
  circle = ge.add_circle([4935.mm,1181.mm,200.mm], [0,0,1], 65.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(340.mm)
  mat = model.materials["Filter F1 (50µ)"] || model.materials.add("Filter F1 (50µ)")
  mat.color = Sketchup::Color.new(58, 110, 165)
  grp.material = mat

  # Filter F2 (5µ)
  grp = ents.add_group
  grp.name = "Filter F2 (5µ)"
  ge = grp.entities
  circle = ge.add_circle([4935.mm,1181.mm,570.mm], [0,0,1], 65.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(340.mm)
  mat = model.materials["Filter F2 (5µ)"] || model.materials.add("Filter F2 (5µ)")
  mat.color = Sketchup::Color.new(58, 110, 165)
  grp.material = mat

  # Filter F3 (GAC)
  grp = ents.add_group
  grp.name = "Filter F3 (GAC)"
  ge = grp.entities
  circle = ge.add_circle([4935.mm,1181.mm,940.mm], [0,0,1], 65.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(340.mm)
  mat = model.materials["Filter F3 (GAC)"] || model.materials.add("Filter F3 (GAC)")
  mat.color = Sketchup::Color.new(58, 110, 165)
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
  mat = model.materials["IBC Blue #1 pallet"] || model.materials.add("IBC Blue #1 pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
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
  mat = model.materials["IBC Waste pallet"] || model.materials.add("IBC Waste pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
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
  mat = model.materials["IBC Blue #2 pallet"] || model.materials.add("IBC Blue #2 pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  grp.material = mat

  # IBC Blue #2 bottle
  grp = ents.add_group
  grp.name = "IBC Blue #2 bottle"
  face = grp.entities.add_face([4704.mm,1346.mm,1178.mm], [5863.mm,1346.mm,1178.mm], [5863.mm,2302.mm,1178.mm], [4704.mm,2302.mm,1178.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(822.mm)
  mat = model.materials["IBC Blue #2 bottle"] || model.materials.add("IBC Blue #2 bottle")
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
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([4734.mm,1266.mm,0.mm], [4784.mm,1266.mm,0.mm], [4784.mm,1316.mm,0.mm], [4734.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([5258.5.mm,1046.mm,0.mm], [5308.5.mm,1046.mm,0.mm], [5308.5.mm,1096.mm,0.mm], [5258.5.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([5258.5.mm,1266.mm,0.mm], [5308.5.mm,1266.mm,0.mm], [5308.5.mm,1316.mm,0.mm], [5258.5.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([5783.mm,1046.mm,0.mm], [5833.mm,1046.mm,0.mm], [5833.mm,1096.mm,0.mm], [5783.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([5783.mm,1266.mm,0.mm], [5833.mm,1266.mm,0.mm], [5833.mm,1316.mm,0.mm], [5783.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Rack Spine
  grp = ents.add_group
  grp.name = "Rack Spine"
  face = grp.entities.add_face([4734.mm,1046.mm,960.mm], [5833.mm,1046.mm,960.mm], [5833.mm,1096.mm,960.mm], [4734.mm,1096.mm,960.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Rack Spine"] || model.materials.add("Rack Spine")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Rack Spine
  grp = ents.add_group
  grp.name = "Rack Spine"
  face = grp.entities.add_face([4734.mm,1266.mm,960.mm], [5833.mm,1266.mm,960.mm], [5833.mm,1316.mm,960.mm], [4734.mm,1316.mm,960.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Rack Spine"] || model.materials.add("Rack Spine")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Rack Platform Beam
  grp = ents.add_group
  grp.name = "Rack Platform Beam"
  face = grp.entities.add_face([4734.mm,30.mm,960.mm], [4784.mm,30.mm,960.mm], [4784.mm,2332.mm,960.mm], [4734.mm,2332.mm,960.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Rack Platform Beam"] || model.materials.add("Rack Platform Beam")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Rack Platform Beam
  grp = ents.add_group
  grp.name = "Rack Platform Beam"
  face = grp.entities.add_face([5258.5.mm,30.mm,960.mm], [5308.5.mm,30.mm,960.mm], [5308.5.mm,2332.mm,960.mm], [5258.5.mm,2332.mm,960.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Rack Platform Beam"] || model.materials.add("Rack Platform Beam")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Rack Platform Beam
  grp = ents.add_group
  grp.name = "Rack Platform Beam"
  face = grp.entities.add_face([5783.mm,30.mm,960.mm], [5833.mm,30.mm,960.mm], [5833.mm,2332.mm,960.mm], [5783.mm,2332.mm,960.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Rack Platform Beam"] || model.materials.add("Rack Platform Beam")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "IBC Rack"
  inst.layer = model.layers["IBC Rack"]


model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags from earlier generator versions ──
keep_tags = ["Shell", "Walkways", "Processing Tray", "Pinhole", "Optical Cone", "Film Plane", "Ceiling Rail", "Spray Bar", "Equipment Panel", "IBC Stack", "IBC Rack"]
default_layer = model.layers[0]
model.layers.to_a.each { |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}

# ── Scenes ──
model.layers.each { |l| l.visible = true }
model.pages.add("Overview")

# Optical Core: hide circulation/processing/structure, keep the optical train.
["Walkways", "Processing Tray", "Ceiling Rail", "Spray Bar", "Equipment Panel", "IBC Stack", "IBC Rack"].each { |n| model.layers[n].visible = false }
model.pages.add("Optical Core")
model.layers.each { |l| l.visible = true }

model.commit_operation
Sketchup.active_model.active_view.zoom_extents
{ success: true, model: "Overview",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
