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
  model.layers.add("Optical Axis") unless model.layers["Optical Axis"]
  model.layers.add("Film Plane") unless model.layers["Film Plane"]

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
  # Walkway Near (left section)
  grp = ents.add_group
  grp.name = "Walkway Near (left section)"
  face = grp.entities.add_face([470.mm,0.mm,75.mm], [1155.mm,0.mm,75.mm], [1155.mm,300.mm,75.mm], [470.mm,300.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  grp.material = mat

  # Walkway Near (widened)
  grp = ents.add_group
  grp.name = "Walkway Near (widened)"
  face = grp.entities.add_face([1155.mm,0.mm,75.mm], [2629.mm,0.mm,75.mm], [2629.mm,500.mm,75.mm], [1155.mm,500.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (widened)"] || model.materials.add("Walkway Near (widened)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  grp.material = mat

  # Walkway Near (right section)
  grp = ents.add_group
  grp.name = "Walkway Near (right section)"
  face = grp.entities.add_face([2629.mm,0.mm,75.mm], [4329.mm,0.mm,75.mm], [4329.mm,300.mm,75.mm], [2629.mm,300.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (right section)"] || model.materials.add("Walkway Near (right section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  grp.material = mat

  # Walkway Far
  grp = ents.add_group
  grp.name = "Walkway Far"
  face = grp.entities.add_face([470.mm,2062.mm,75.mm], [4329.mm,2062.mm,75.mm], [4329.mm,2362.mm,75.mm], [470.mm,2362.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Far"] || model.materials.add("Walkway Far")
  mat.color = Sketchup::Color.new(128, 128, 128)
  grp.material = mat

  # Walkway Right (IBC end)
  grp = ents.add_group
  grp.name = "Walkway Right (IBC end)"
  face = grp.entities.add_face([4329.mm,0.mm,75.mm], [4629.mm,0.mm,75.mm], [4629.mm,2362.mm,75.mm], [4329.mm,2362.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Right (IBC end)"] || model.materials.add("Walkway Right (IBC end)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  grp.material = mat

  # Walkway Left (cargo door)
  grp = ents.add_group
  grp.name = "Walkway Left (cargo door)"
  face = grp.entities.add_face([170.mm,0.mm,75.mm], [470.mm,0.mm,75.mm], [470.mm,2362.mm,75.mm], [170.mm,2362.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Left (cargo door)"] || model.materials.add("Walkway Left (cargo door)")
  mat.color = Sketchup::Color.new(128, 128, 128)
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

  # ═══ Optical Axis ═══
  defn = model.definitions.add("Optical Axis")
  ents = defn.entities
  # Optical Axis (pinhole → film plane)
  grp = ents.add_group
  grp.name = "Optical Axis (pinhole → film plane)"
  face = grp.entities.add_face([2396.mm,0.mm,1191.mm], [2402.mm,0.mm,1191.mm], [2402.mm,2262.mm,1191.mm], [2396.mm,2262.mm,1191.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Optical Axis (pinhole → film plane)"] || model.materials.add("Optical Axis (pinhole → film plane)")
  mat.color = Sketchup::Color.new(204, 102, 0)
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Optical Axis"
  inst.layer = model.layers["Optical Axis"]

  # ═══ Film Plane Mechanism ═══
  defn = model.definitions.add("Film Plane Mechanism")
  ents = defn.entities
  # FP Rail BL
  grp = ents.add_group
  grp.name = "FP Rail BL"
  face = grp.entities.add_face([150.mm,100.mm,100.mm], [190.mm,100.mm,100.mm], [190.mm,2300.mm,100.mm], [150.mm,2300.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["FP Rail BL"] || model.materials.add("FP Rail BL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # FP Rail BR
  grp = ents.add_group
  grp.name = "FP Rail BR"
  face = grp.entities.add_face([4609.mm,100.mm,100.mm], [4649.mm,100.mm,100.mm], [4649.mm,2300.mm,100.mm], [4609.mm,2300.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["FP Rail BR"] || model.materials.add("FP Rail BR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # FP Rail TL
  grp = ents.add_group
  grp.name = "FP Rail TL"
  face = grp.entities.add_face([150.mm,100.mm,2248.mm], [190.mm,100.mm,2248.mm], [190.mm,2300.mm,2248.mm], [150.mm,2300.mm,2248.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["FP Rail TL"] || model.materials.add("FP Rail TL")
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


model.definitions.purge_unused
model.materials.purge_unused

# ── Scenes ──
model.layers.each { |l| l.visible = true }
model.pages.add("Overview")

# Optical Core: hide circulation/processing, keep shell + optical train.
["Walkways", "Processing Tray"].each { |n| model.layers[n].visible = false }
model.pages.add("Optical Core")
model.layers.each { |l| l.visible = true }

model.commit_operation
Sketchup.active_model.active_view.zoom_extents
{ success: true, model: "Overview",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
