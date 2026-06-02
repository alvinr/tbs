model = Sketchup.active_model
model.start_operation("TBS-001 Phase 1", true)
entities = model.active_entities

# Display in millimeters (LengthUnit 2 = mm, LengthFormat 0 = decimal).
# SketchUp stores geometry in inches internally; this only sets the UI readout.
opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

  # Container Floor
  grp = entities.add_group
  grp.name = "Container Floor"
  face = grp.entities.add_face([0.mm,0.mm,-40.mm], [5893.mm,0.mm,-40.mm], [5893.mm,2362.mm,-40.mm], [0.mm,2362.mm,-40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials.add("Container Floor")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Container Ceiling
  grp = entities.add_group
  grp.name = "Container Ceiling"
  face = grp.entities.add_face([0.mm,0.mm,2388.mm], [5893.mm,0.mm,2388.mm], [5893.mm,2362.mm,2388.mm], [0.mm,2362.mm,2388.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials.add("Container Ceiling")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.2
  grp.material = mat

  # Pinhole Wall (Yd=0)
  grp = entities.add_group
  grp.name = "Pinhole Wall (Yd=0)"
  face = grp.entities.add_face([0.mm,-40.mm,0.mm], [5893.mm,-40.mm,0.mm], [5893.mm,0.mm,0.mm], [0.mm,0.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials.add("Pinhole Wall (Yd=0)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Film Plane Wall (Yd=max)
  grp = entities.add_group
  grp.name = "Film Plane Wall (Yd=max)"
  face = grp.entities.add_face([0.mm,2362.mm,0.mm], [5893.mm,2362.mm,0.mm], [5893.mm,2402.mm,0.mm], [0.mm,2402.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials.add("Film Plane Wall (Yd=max)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Far End Wall (IBC end)
  grp = entities.add_group
  grp.name = "Far End Wall (IBC end)"
  face = grp.entities.add_face([5893.mm,0.mm,0.mm], [5933.mm,0.mm,0.mm], [5933.mm,2362.mm,0.mm], [5893.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials.add("Far End Wall (IBC end)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Processing Tray Floor
  grp = entities.add_group
  grp.name = "Processing Tray Floor"
  face = grp.entities.add_face([170.mm,80.mm,0.mm], [4629.mm,80.mm,0.mm], [4629.mm,2280.mm,0.mm], [170.mm,2280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials.add("Processing Tray Floor")
  mat.color = Sketchup::Color.new(232, 245, 233)
  mat.alpha = 0.5
  grp.material = mat

  # Tray Rim Near
  grp = entities.add_group
  grp.name = "Tray Rim Near"
  face = grp.entities.add_face([170.mm,80.mm,2.mm], [4629.mm,80.mm,2.mm], [4629.mm,82.mm,2.mm], [170.mm,82.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials.add("Tray Rim Near")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Tray Rim Far
  grp = entities.add_group
  grp.name = "Tray Rim Far"
  face = grp.entities.add_face([170.mm,2278.mm,2.mm], [4629.mm,2278.mm,2.mm], [4629.mm,2280.mm,2.mm], [170.mm,2280.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials.add("Tray Rim Far")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Tray Rim Left
  grp = entities.add_group
  grp.name = "Tray Rim Left"
  face = grp.entities.add_face([170.mm,80.mm,2.mm], [172.mm,80.mm,2.mm], [172.mm,2280.mm,2.mm], [170.mm,2280.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials.add("Tray Rim Left")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Tray Rim Right
  grp = entities.add_group
  grp.name = "Tray Rim Right"
  face = grp.entities.add_face([4627.mm,80.mm,2.mm], [4629.mm,80.mm,2.mm], [4629.mm,2280.mm,2.mm], [4627.mm,2280.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials.add("Tray Rim Right")
  mat.color = Sketchup::Color.new(176, 176, 184)
  grp.material = mat

  # Walkway Near (left section)
  grp = entities.add_group
  grp.name = "Walkway Near (left section)"
  face = grp.entities.add_face([470.mm,0.mm,75.mm], [1155.mm,0.mm,75.mm], [1155.mm,300.mm,75.mm], [470.mm,300.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  grp.material = mat

  # Walkway Near (widened)
  grp = entities.add_group
  grp.name = "Walkway Near (widened)"
  face = grp.entities.add_face([1155.mm,0.mm,75.mm], [2629.mm,0.mm,75.mm], [2629.mm,500.mm,75.mm], [1155.mm,500.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials.add("Walkway Near (widened)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  grp.material = mat

  # Walkway Near (right section)
  grp = entities.add_group
  grp.name = "Walkway Near (right section)"
  face = grp.entities.add_face([2629.mm,0.mm,75.mm], [4329.mm,0.mm,75.mm], [4329.mm,300.mm,75.mm], [2629.mm,300.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials.add("Walkway Near (right section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  grp.material = mat

  # Walkway Far
  grp = entities.add_group
  grp.name = "Walkway Far"
  face = grp.entities.add_face([470.mm,2062.mm,75.mm], [4329.mm,2062.mm,75.mm], [4329.mm,2362.mm,75.mm], [470.mm,2362.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials.add("Walkway Far")
  mat.color = Sketchup::Color.new(128, 128, 128)
  grp.material = mat

  # Walkway Right (IBC end)
  grp = entities.add_group
  grp.name = "Walkway Right (IBC end)"
  face = grp.entities.add_face([4329.mm,0.mm,75.mm], [4629.mm,0.mm,75.mm], [4629.mm,2362.mm,75.mm], [4329.mm,2362.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials.add("Walkway Right (IBC end)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  grp.material = mat

  # Walkway Left (cargo door)
  grp = entities.add_group
  grp.name = "Walkway Left (cargo door)"
  face = grp.entities.add_face([170.mm,0.mm,75.mm], [470.mm,0.mm,75.mm], [470.mm,2362.mm,75.mm], [170.mm,2362.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials.add("Walkway Left (cargo door)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  grp.material = mat


model.commit_operation
Sketchup.active_model.active_view.zoom_extents
{ success: true, phase: "Phase 1 — Container + Walkways + Tray" }.to_json
