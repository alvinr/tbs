model = Sketchup.active_model
model.start_operation("TBS-001 Overview", true)
entities = model.active_entities

# Display in millimeters (LengthUnit 2 = mm, LengthFormat 0 = decimal).
# SketchUp stores geometry in inches internally; this only sets the UI readout.
opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# ── Idempotent rebuild: erase ALL prior instances (incl. any 'Sree' scale figure —
# the person is no longer kept), then purge unused definitions so names don't collide.
to_erase = entities.to_a.select { |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text)
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
  model.layers.add("Combined Plate") unless model.layers["Combined Plate"]
  model.layers.add("Pivot Axle") unless model.layers["Pivot Axle"]
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
  model.layers.add("Solar Array") unless model.layers["Solar Array"]
  model.layers.add("Labels") unless model.layers["Labels"]

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
  face = grp.entities.add_face([470.mm,8.mm,115.mm], [1155.mm,8.mm,115.mm], [1155.mm,300.mm,115.mm], [470.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near (widened)
  grp = ents.add_group
  grp.name = "Walkway Near (widened)"
  face = grp.entities.add_face([1155.mm,10.mm,115.mm], [2629.mm,10.mm,115.mm], [2629.mm,500.mm,115.mm], [1155.mm,500.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near (right section)
  grp = ents.add_group
  grp.name = "Walkway Near (right section)"
  face = grp.entities.add_face([2629.mm,8.mm,115.mm], [4329.mm,8.mm,115.mm], [4329.mm,300.mm,115.mm], [2629.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far
  grp = ents.add_group
  grp.name = "Walkway Far"
  face = grp.entities.add_face([470.mm,2062.mm,115.mm], [4329.mm,2062.mm,115.mm], [4329.mm,2354.mm,115.mm], [470.mm,2354.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4329 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 upper"
  face = grp.entities.add_face([4329.mm,0.mm,95.mm], [4369.mm,0.mm,95.mm], [4369.mm,2362.mm,95.mm], [4329.mm,2362.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4329 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 lower"
  face = grp.entities.add_face([4329.mm,0.mm,80.mm], [4369.mm,0.mm,80.mm], [4369.mm,1046.mm,80.mm], [4329.mm,1046.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4329 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 lower"
  face = grp.entities.add_face([4329.mm,1086.mm,80.mm], [4369.mm,1086.mm,80.mm], [4369.mm,1266.mm,80.mm], [4329.mm,1266.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4329 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 lower"
  face = grp.entities.add_face([4329.mm,1306.mm,80.mm], [4369.mm,1306.mm,80.mm], [4369.mm,2362.mm,80.mm], [4329.mm,2362.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 upper"
  face = grp.entities.add_face([4589.mm,0.mm,95.mm], [4629.mm,0.mm,95.mm], [4629.mm,2362.mm,95.mm], [4589.mm,2362.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 lower"
  face = grp.entities.add_face([4589.mm,0.mm,80.mm], [4629.mm,0.mm,80.mm], [4629.mm,1046.mm,80.mm], [4589.mm,1046.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 lower"
  face = grp.entities.add_face([4589.mm,1086.mm,80.mm], [4629.mm,1086.mm,80.mm], [4629.mm,1266.mm,80.mm], [4589.mm,1266.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 lower"
  face = grp.entities.add_face([4589.mm,1306.mm,80.mm], [4629.mm,1306.mm,80.mm], [4629.mm,2362.mm,80.mm], [4589.mm,2362.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk end beam Yd0
  grp = ents.add_group
  grp.name = "RWk end beam Yd0"
  face = grp.entities.add_face([4329.mm,0.mm,80.mm], [4629.mm,0.mm,80.mm], [4629.mm,40.mm,80.mm], [4329.mm,40.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(35.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk end beam Yd2322
  grp = ents.add_group
  grp.name = "RWk end beam Yd2322"
  face = grp.entities.add_face([4329.mm,2322.mm,80.mm], [4629.mm,2322.mm,80.mm], [4629.mm,2362.mm,80.mm], [4329.mm,2362.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(35.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1046 lower
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 lower"
  face = grp.entities.add_face([4329.mm,1046.mm,70.mm], [4734.mm,1046.mm,70.mm], [4734.mm,1086.mm,70.mm], [4329.mm,1086.mm,70.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1046 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 upper"
  face = grp.entities.add_face([4369.mm,1046.mm,95.mm], [4589.mm,1046.mm,95.mm], [4589.mm,1086.mm,95.mm], [4369.mm,1086.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1046 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 upper"
  face = grp.entities.add_face([4629.mm,1046.mm,95.mm], [4734.mm,1046.mm,95.mm], [4734.mm,1086.mm,95.mm], [4629.mm,1086.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1046 Y1038
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1046 Y1038"
  face = grp.entities.add_face([4730.mm,1038.mm,45.mm], [4788.mm,1038.mm,45.mm], [4788.mm,1046.mm,45.mm], [4730.mm,1046.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1046 Y1086
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1046 Y1086"
  face = grp.entities.add_face([4730.mm,1086.mm,45.mm], [4788.mm,1086.mm,45.mm], [4788.mm,1094.mm,45.mm], [4730.mm,1094.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1046 Z76
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1046 Z76"
  ge = grp.entities
  circle = ge.add_circle([4759.mm,1034.mm,76.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(64.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1046 Z133
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1046 Z133"
  ge = grp.entities
  circle = ge.add_circle([4759.mm,1034.mm,133.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(64.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1266 lower
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 lower"
  face = grp.entities.add_face([4329.mm,1266.mm,70.mm], [4734.mm,1266.mm,70.mm], [4734.mm,1306.mm,70.mm], [4329.mm,1306.mm,70.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1266 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 upper"
  face = grp.entities.add_face([4369.mm,1266.mm,95.mm], [4589.mm,1266.mm,95.mm], [4589.mm,1306.mm,95.mm], [4369.mm,1306.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1266 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 upper"
  face = grp.entities.add_face([4629.mm,1266.mm,95.mm], [4734.mm,1266.mm,95.mm], [4734.mm,1306.mm,95.mm], [4629.mm,1306.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1266 Y1258
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1266 Y1258"
  face = grp.entities.add_face([4730.mm,1258.mm,45.mm], [4788.mm,1258.mm,45.mm], [4788.mm,1266.mm,45.mm], [4730.mm,1266.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1266 Y1306
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1266 Y1306"
  face = grp.entities.add_face([4730.mm,1306.mm,45.mm], [4788.mm,1306.mm,45.mm], [4788.mm,1314.mm,45.mm], [4730.mm,1314.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1266 Z76
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1266 Z76"
  ge = grp.entities
  circle = ge.add_circle([4759.mm,1254.mm,76.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(64.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1266 Z133
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1266 Z133"
  ge = grp.entities
  circle = ge.add_circle([4759.mm,1254.mm,133.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(64.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat plate (near)
  grp = ents.add_group
  grp.name = "RWk wall cleat plate (near)"
  face = grp.entities.add_face([4304.mm,0.mm,60.mm], [4394.mm,0.mm,60.mm], [4394.mm,8.mm,60.mm], [4304.mm,8.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(65.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat ext plate (near)
  grp = ents.add_group
  grp.name = "RWk wall cleat ext plate (near)"
  face = grp.entities.add_face([4304.mm,-48.mm,60.mm], [4394.mm,-48.mm,60.mm], [4394.mm,-40.mm,60.mm], [4304.mm,-40.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(65.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat shelf (near)
  grp = ents.add_group
  grp.name = "RWk wall cleat shelf (near)"
  face = grp.entities.add_face([4304.mm,0.mm,60.mm], [4394.mm,0.mm,60.mm], [4394.mm,55.mm,60.mm], [4304.mm,55.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall bolt (near) Z76
  grp = ents.add_group
  grp.name = "RWk wall bolt (near) Z76"
  ge = grp.entities
  circle = ge.add_circle([4349.mm,-48.mm,76.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall bolt (near) Z109
  grp = ents.add_group
  grp.name = "RWk wall bolt (near) Z109"
  ge = grp.entities
  circle = ge.add_circle([4349.mm,-48.mm,109.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat plate (far)
  grp = ents.add_group
  grp.name = "RWk wall cleat plate (far)"
  face = grp.entities.add_face([4304.mm,2354.mm,60.mm], [4394.mm,2354.mm,60.mm], [4394.mm,2362.mm,60.mm], [4304.mm,2362.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(65.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat ext plate (far)
  grp = ents.add_group
  grp.name = "RWk wall cleat ext plate (far)"
  face = grp.entities.add_face([4304.mm,2402.mm,60.mm], [4394.mm,2402.mm,60.mm], [4394.mm,2410.mm,60.mm], [4304.mm,2410.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(65.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat shelf (far)
  grp = ents.add_group
  grp.name = "RWk wall cleat shelf (far)"
  face = grp.entities.add_face([4304.mm,2307.mm,60.mm], [4394.mm,2307.mm,60.mm], [4394.mm,2362.mm,60.mm], [4304.mm,2362.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall bolt (far) Z76
  grp = ents.add_group
  grp.name = "RWk wall bolt (far) Z76"
  ge = grp.entities
  circle = ge.add_circle([4349.mm,2354.mm,76.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall bolt (far) Z109
  grp = ents.add_group
  grp.name = "RWk wall bolt (far) Z109"
  ge = grp.entities
  circle = ge.add_circle([4349.mm,2354.mm,109.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right walkway grate (cantilevered)
  grp = ents.add_group
  grp.name = "Right walkway grate (cantilevered)"
  face = grp.entities.add_face([4329.mm,0.mm,115.mm], [4629.mm,0.mm,115.mm], [4629.mm,2362.mm,115.mm], [4329.mm,2362.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Left (REMOVABLE — transport)
  grp = ents.add_group
  grp.name = "Walkway Left (REMOVABLE — transport)"
  face = grp.entities.add_face([170.mm,0.mm,115.mm], [470.mm,0.mm,115.mm], [470.mm,2362.mm,115.mm], [170.mm,2362.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Left (REMOVABLE — transport)"] || model.materials.add("Walkway Left (REMOVABLE — transport)")
  mat.color = Sketchup::Color.new(192, 96, 0)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Left punch-out (drum exit)
  grp = ents.add_group
  grp.name = "Walkway Left punch-out (drum exit)"
  face = grp.entities.add_face([470.mm,800.mm,115.mm], [770.mm,800.mm,115.mm], [770.mm,1560.mm,115.mm], [470.mm,1560.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
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
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 1 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 arm"
  face = grp.entities.add_face([694.mm,8.mm,105.mm], [702.mm,8.mm,105.mm], [702.mm,300.mm,105.mm], [694.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 1 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 gusset"
  ge = grp.entities
  f = ge.add_face([694.mm,8.mm,0.mm], [694.mm,8.mm,105.mm], [694.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) plate"
  face = grp.entities.add_face([1095.mm,0.mm,0.mm], [1215.mm,0.mm,0.mm], [1215.mm,10.mm,0.mm], [1095.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) arm"
  face = grp.entities.add_face([1150.mm,10.mm,103.mm], [1160.mm,10.mm,103.mm], [1160.mm,500.mm,103.mm], [1150.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([1150.mm,10.mm,0.mm], [1150.mm,10.mm,103.mm], [1150.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) plate"
  face = grp.entities.add_face([1552.mm,0.mm,0.mm], [1672.mm,0.mm,0.mm], [1672.mm,10.mm,0.mm], [1552.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) arm"
  face = grp.entities.add_face([1607.mm,10.mm,103.mm], [1617.mm,10.mm,103.mm], [1617.mm,500.mm,103.mm], [1607.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([1607.mm,10.mm,0.mm], [1607.mm,10.mm,103.mm], [1607.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) plate"
  face = grp.entities.add_face([2009.mm,0.mm,0.mm], [2129.mm,0.mm,0.mm], [2129.mm,10.mm,0.mm], [2009.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) arm"
  face = grp.entities.add_face([2064.mm,10.mm,103.mm], [2074.mm,10.mm,103.mm], [2074.mm,500.mm,103.mm], [2064.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([2064.mm,10.mm,0.mm], [2064.mm,10.mm,103.mm], [2064.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) plate"
  face = grp.entities.add_face([2466.mm,0.mm,0.mm], [2586.mm,0.mm,0.mm], [2586.mm,10.mm,0.mm], [2466.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) arm"
  face = grp.entities.add_face([2521.mm,10.mm,103.mm], [2531.mm,10.mm,103.mm], [2531.mm,500.mm,103.mm], [2521.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([2521.mm,10.mm,0.mm], [2521.mm,10.mm,103.mm], [2521.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 plate"
  face = grp.entities.add_face([2923.mm,0.mm,0.mm], [3043.mm,0.mm,0.mm], [3043.mm,8.mm,0.mm], [2923.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 arm"
  face = grp.entities.add_face([2979.mm,8.mm,105.mm], [2987.mm,8.mm,105.mm], [2987.mm,300.mm,105.mm], [2979.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 gusset"
  ge = grp.entities
  f = ge.add_face([2979.mm,8.mm,0.mm], [2979.mm,8.mm,105.mm], [2979.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 7 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 plate"
  face = grp.entities.add_face([3380.mm,0.mm,0.mm], [3500.mm,0.mm,0.mm], [3500.mm,8.mm,0.mm], [3380.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 7 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 arm"
  face = grp.entities.add_face([3436.mm,8.mm,105.mm], [3444.mm,8.mm,105.mm], [3444.mm,300.mm,105.mm], [3436.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 7 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 gusset"
  ge = grp.entities
  f = ge.add_face([3436.mm,8.mm,0.mm], [3436.mm,8.mm,105.mm], [3436.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 8 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 plate"
  face = grp.entities.add_face([3837.mm,0.mm,0.mm], [3957.mm,0.mm,0.mm], [3957.mm,8.mm,0.mm], [3837.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 8 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 arm"
  face = grp.entities.add_face([3893.mm,8.mm,105.mm], [3901.mm,8.mm,105.mm], [3901.mm,300.mm,105.mm], [3893.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 8 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 gusset"
  ge = grp.entities
  f = ge.add_face([3893.mm,8.mm,0.mm], [3893.mm,8.mm,105.mm], [3893.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 1 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 plate"
  face = grp.entities.add_face([638.mm,2354.mm,0.mm], [758.mm,2354.mm,0.mm], [758.mm,2362.mm,0.mm], [638.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 1 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 arm"
  face = grp.entities.add_face([694.mm,2062.mm,105.mm], [702.mm,2062.mm,105.mm], [702.mm,2354.mm,105.mm], [694.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 1 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 gusset"
  ge = grp.entities
  f = ge.add_face([694.mm,2354.mm,0.mm], [694.mm,2354.mm,105.mm], [694.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 2 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 plate"
  face = grp.entities.add_face([1095.mm,2354.mm,0.mm], [1215.mm,2354.mm,0.mm], [1215.mm,2362.mm,0.mm], [1095.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 2 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 arm"
  face = grp.entities.add_face([1151.mm,2062.mm,105.mm], [1159.mm,2062.mm,105.mm], [1159.mm,2354.mm,105.mm], [1151.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 2 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 gusset"
  ge = grp.entities
  f = ge.add_face([1151.mm,2354.mm,0.mm], [1151.mm,2354.mm,105.mm], [1151.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 3 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 plate"
  face = grp.entities.add_face([1552.mm,2354.mm,0.mm], [1672.mm,2354.mm,0.mm], [1672.mm,2362.mm,0.mm], [1552.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 3 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 arm"
  face = grp.entities.add_face([1608.mm,2062.mm,105.mm], [1616.mm,2062.mm,105.mm], [1616.mm,2354.mm,105.mm], [1608.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 3 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 gusset"
  ge = grp.entities
  f = ge.add_face([1608.mm,2354.mm,0.mm], [1608.mm,2354.mm,105.mm], [1608.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 4 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 plate"
  face = grp.entities.add_face([2009.mm,2354.mm,0.mm], [2129.mm,2354.mm,0.mm], [2129.mm,2362.mm,0.mm], [2009.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 4 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 arm"
  face = grp.entities.add_face([2065.mm,2062.mm,105.mm], [2073.mm,2062.mm,105.mm], [2073.mm,2354.mm,105.mm], [2065.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 4 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 gusset"
  ge = grp.entities
  f = ge.add_face([2065.mm,2354.mm,0.mm], [2065.mm,2354.mm,105.mm], [2065.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 5 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 plate"
  face = grp.entities.add_face([2466.mm,2354.mm,0.mm], [2586.mm,2354.mm,0.mm], [2586.mm,2362.mm,0.mm], [2466.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 5 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 arm"
  face = grp.entities.add_face([2522.mm,2062.mm,105.mm], [2530.mm,2062.mm,105.mm], [2530.mm,2354.mm,105.mm], [2522.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 5 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 gusset"
  ge = grp.entities
  f = ge.add_face([2522.mm,2354.mm,0.mm], [2522.mm,2354.mm,105.mm], [2522.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 6 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 plate"
  face = grp.entities.add_face([2923.mm,2354.mm,0.mm], [3043.mm,2354.mm,0.mm], [3043.mm,2362.mm,0.mm], [2923.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 6 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 arm"
  face = grp.entities.add_face([2979.mm,2062.mm,105.mm], [2987.mm,2062.mm,105.mm], [2987.mm,2354.mm,105.mm], [2979.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 6 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 gusset"
  ge = grp.entities
  f = ge.add_face([2979.mm,2354.mm,0.mm], [2979.mm,2354.mm,105.mm], [2979.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 7 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 plate"
  face = grp.entities.add_face([3380.mm,2354.mm,0.mm], [3500.mm,2354.mm,0.mm], [3500.mm,2362.mm,0.mm], [3380.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 7 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 arm"
  face = grp.entities.add_face([3436.mm,2062.mm,105.mm], [3444.mm,2062.mm,105.mm], [3444.mm,2354.mm,105.mm], [3436.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 7 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 gusset"
  ge = grp.entities
  f = ge.add_face([3436.mm,2354.mm,0.mm], [3436.mm,2354.mm,105.mm], [3436.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 8 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 plate"
  face = grp.entities.add_face([3837.mm,2354.mm,0.mm], [3957.mm,2354.mm,0.mm], [3957.mm,2362.mm,0.mm], [3837.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 8 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 arm"
  face = grp.entities.add_face([3893.mm,2062.mm,105.mm], [3901.mm,2062.mm,105.mm], [3901.mm,2354.mm,105.mm], [3893.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 8 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 gusset"
  ge = grp.entities
  f = ge.add_face([3893.mm,2354.mm,0.mm], [3893.mm,2354.mm,105.mm], [3893.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 1 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 1 foot plate"
  face = grp.entities.add_face([38.mm,220.mm,0.mm], [166.mm,220.mm,0.mm], [166.mm,280.mm,0.mm], [38.mm,280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 1 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 1 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,220.mm,0.mm], [165.mm,220.mm,0.mm], [165.mm,280.mm,0.mm], [115.mm,280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 1 arm (to X470)
  grp = ents.add_group
  grp.name = "Left cantilever 1 arm (to X470)"
  face = grp.entities.add_face([165.mm,230.mm,75.mm], [470.mm,230.mm,75.mm], [470.mm,270.mm,75.mm], [165.mm,270.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 2 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 2 foot plate"
  face = grp.entities.add_face([38.mm,770.mm,0.mm], [166.mm,770.mm,0.mm], [166.mm,830.mm,0.mm], [38.mm,830.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 2 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 2 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,770.mm,0.mm], [165.mm,770.mm,0.mm], [165.mm,830.mm,0.mm], [115.mm,830.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 2 arm (to X770)
  grp = ents.add_group
  grp.name = "Left cantilever 2 arm (to X770)"
  face = grp.entities.add_face([165.mm,770.mm,75.mm], [770.mm,770.mm,75.mm], [770.mm,830.mm,75.mm], [165.mm,830.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 3 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 3 foot plate"
  face = grp.entities.add_face([38.mm,1150.mm,0.mm], [166.mm,1150.mm,0.mm], [166.mm,1210.mm,0.mm], [38.mm,1210.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 3 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 3 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,1150.mm,0.mm], [165.mm,1150.mm,0.mm], [165.mm,1210.mm,0.mm], [115.mm,1210.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 3 arm (to X770)
  grp = ents.add_group
  grp.name = "Left cantilever 3 arm (to X770)"
  face = grp.entities.add_face([165.mm,1150.mm,75.mm], [770.mm,1150.mm,75.mm], [770.mm,1210.mm,75.mm], [165.mm,1210.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 4 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 4 foot plate"
  face = grp.entities.add_face([38.mm,1530.mm,0.mm], [166.mm,1530.mm,0.mm], [166.mm,1590.mm,0.mm], [38.mm,1590.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 4 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 4 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,1530.mm,0.mm], [165.mm,1530.mm,0.mm], [165.mm,1590.mm,0.mm], [115.mm,1590.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 4 arm (to X770)
  grp = ents.add_group
  grp.name = "Left cantilever 4 arm (to X770)"
  face = grp.entities.add_face([165.mm,1530.mm,75.mm], [770.mm,1530.mm,75.mm], [770.mm,1590.mm,75.mm], [165.mm,1590.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 5 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 5 foot plate"
  face = grp.entities.add_face([38.mm,2080.mm,0.mm], [166.mm,2080.mm,0.mm], [166.mm,2140.mm,0.mm], [38.mm,2140.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 5 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 5 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,2080.mm,0.mm], [165.mm,2080.mm,0.mm], [165.mm,2140.mm,0.mm], [115.mm,2140.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 5 arm (to X470)
  grp = ents.add_group
  grp.name = "Left cantilever 5 arm (to X470)"
  face = grp.entities.add_face([165.mm,2090.mm,75.mm], [470.mm,2090.mm,75.mm], [470.mm,2130.mm,75.mm], [165.mm,2130.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
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
  face = grp.entities.add_face([170.mm,80.mm,0.mm], [4629.mm,80.mm,0.mm], [4629.mm,2281.mm,0.mm], [170.mm,2281.mm,0.mm])
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
  face = grp.entities.add_face([170.mm,2279.mm,2.mm], [4629.mm,2279.mm,2.mm], [4629.mm,2281.mm,2.mm], [170.mm,2281.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Processing Tray Floor"] || model.materials.add("Processing Tray Floor")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Left
  grp = ents.add_group
  grp.name = "Tray Rim Left"
  face = grp.entities.add_face([170.mm,80.mm,2.mm], [172.mm,80.mm,2.mm], [172.mm,2281.mm,2.mm], [170.mm,2281.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Processing Tray Floor"] || model.materials.add("Processing Tray Floor")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Right
  grp = ents.add_group
  grp.name = "Tray Rim Right"
  face = grp.entities.add_face([4627.mm,80.mm,2.mm], [4629.mm,80.mm,2.mm], [4629.mm,2281.mm,2.mm], [4627.mm,2281.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Processing Tray Floor"] || model.materials.add("Processing Tray Floor")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Chemistry Bath
  grp = ents.add_group
  grp.name = "Chemistry Bath"
  face = grp.entities.add_face([172.mm,82.mm,2.mm], [4627.mm,82.mm,2.mm], [4627.mm,2279.mm,2.mm], [172.mm,2279.mm,2.mm])
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
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # TS Swing Knob
  grp = ents.add_group
  grp.name = "TS Swing Knob"
  face = grp.entities.add_face([2539.mm,-100.mm,1179.mm], [2564.mm,-100.mm,1179.mm], [2564.mm,-75.mm,1179.mm], [2539.mm,-75.mm,1179.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  face = grp.entities.add_face([4609.mm,0.mm,150.mm], [4649.mm,0.mm,150.mm], [4649.mm,2362.mm,150.mm], [4609.mm,2362.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Rail TR
  grp = ents.add_group
  grp.name = "FP Rail TR"
  face = grp.entities.add_face([4609.mm,0.mm,2248.mm], [4649.mm,0.mm,2248.mm], [4649.mm,2362.mm,2248.mm], [4609.mm,2362.mm,2248.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Rail BL
  grp = ents.add_group
  grp.name = "FP Rail BL"
  face = grp.entities.add_face([150.mm,0.mm,150.mm], [190.mm,0.mm,150.mm], [190.mm,2362.mm,150.mm], [150.mm,2362.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Rail TL
  grp = ents.add_group
  grp.name = "FP Rail TL"
  face = grp.entities.add_face([150.mm,0.mm,2248.mm], [190.mm,0.mm,2248.mm], [190.mm,2362.mm,2248.mm], [150.mm,2362.mm,2248.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle back-plate TL near
  grp = ents.add_group
  grp.name = "Saddle back-plate TL near"
  face = grp.entities.add_face([75.mm,0.mm,2173.mm], [225.mm,0.mm,2173.mm], [225.mm,8.mm,2173.mm], [75.mm,8.mm,2173.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle OUTSIDE plate TL near
  grp = ents.add_group
  grp.name = "Saddle OUTSIDE plate TL near"
  face = grp.entities.add_face([75.mm,-48.mm,2173.mm], [225.mm,-48.mm,2173.mm], [225.mm,-40.mm,2173.mm], [75.mm,-40.mm,2173.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle seat TL near
  grp = ents.add_group
  grp.name = "Saddle seat TL near"
  face = grp.entities.add_face([126.mm,0.mm,2238.mm], [174.mm,0.mm,2238.mm], [174.mm,110.mm,2238.mm], [126.mm,110.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle gusset TL near
  grp = ents.add_group
  grp.name = "Saddle gusset TL near"
  ge = grp.entities
  f = ge.add_face([150.mm,110.mm,2238.mm], [150.mm,0.mm,2238.mm], [150.mm,0.mm,2118.mm])
  f.pushpull(8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TL near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TL near"
  ge = grp.entities
  circle = ge.add_circle([100.mm,-48.mm,2198.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TL near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TL near"
  ge = grp.entities
  circle = ge.add_circle([100.mm,-48.mm,2298.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TL near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TL near"
  ge = grp.entities
  circle = ge.add_circle([200.mm,-48.mm,2198.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TL near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TL near"
  ge = grp.entities
  circle = ge.add_circle([200.mm,-48.mm,2298.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Thumb screw TL near
  grp = ents.add_group
  grp.name = "Thumb screw TL near"
  ge = grp.entities
  circle = ge.add_circle([150.mm,25.mm,2248.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Thumb screw TL near
  grp = ents.add_group
  grp.name = "Thumb screw TL near"
  ge = grp.entities
  circle = ge.add_circle([150.mm,85.mm,2248.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle back-plate TL far
  grp = ents.add_group
  grp.name = "Saddle back-plate TL far"
  face = grp.entities.add_face([75.mm,2354.mm,2173.mm], [225.mm,2354.mm,2173.mm], [225.mm,2362.mm,2173.mm], [75.mm,2362.mm,2173.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle OUTSIDE plate TL far
  grp = ents.add_group
  grp.name = "Saddle OUTSIDE plate TL far"
  face = grp.entities.add_face([75.mm,2402.mm,2173.mm], [225.mm,2402.mm,2173.mm], [225.mm,2410.mm,2173.mm], [75.mm,2410.mm,2173.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle seat TL far
  grp = ents.add_group
  grp.name = "Saddle seat TL far"
  face = grp.entities.add_face([126.mm,2252.mm,2238.mm], [174.mm,2252.mm,2238.mm], [174.mm,2362.mm,2238.mm], [126.mm,2362.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle gusset TL far
  grp = ents.add_group
  grp.name = "Saddle gusset TL far"
  ge = grp.entities
  f = ge.add_face([150.mm,2252.mm,2238.mm], [150.mm,2362.mm,2238.mm], [150.mm,2362.mm,2118.mm])
  f.pushpull(8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TL far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TL far"
  ge = grp.entities
  circle = ge.add_circle([100.mm,2354.mm,2198.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TL far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TL far"
  ge = grp.entities
  circle = ge.add_circle([100.mm,2354.mm,2298.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TL far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TL far"
  ge = grp.entities
  circle = ge.add_circle([200.mm,2354.mm,2198.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TL far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TL far"
  ge = grp.entities
  circle = ge.add_circle([200.mm,2354.mm,2298.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Thumb screw TL far
  grp = ents.add_group
  grp.name = "Thumb screw TL far"
  ge = grp.entities
  circle = ge.add_circle([150.mm,2277.mm,2248.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Thumb screw TL far
  grp = ents.add_group
  grp.name = "Thumb screw TL far"
  ge = grp.entities
  circle = ge.add_circle([150.mm,2337.mm,2248.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle back-plate TR near
  grp = ents.add_group
  grp.name = "Saddle back-plate TR near"
  face = grp.entities.add_face([4534.mm,0.mm,2173.mm], [4684.mm,0.mm,2173.mm], [4684.mm,8.mm,2173.mm], [4534.mm,8.mm,2173.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle OUTSIDE plate TR near
  grp = ents.add_group
  grp.name = "Saddle OUTSIDE plate TR near"
  face = grp.entities.add_face([4534.mm,-48.mm,2173.mm], [4684.mm,-48.mm,2173.mm], [4684.mm,-40.mm,2173.mm], [4534.mm,-40.mm,2173.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle seat TR near
  grp = ents.add_group
  grp.name = "Saddle seat TR near"
  face = grp.entities.add_face([4585.mm,0.mm,2238.mm], [4633.mm,0.mm,2238.mm], [4633.mm,110.mm,2238.mm], [4585.mm,110.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle gusset TR near
  grp = ents.add_group
  grp.name = "Saddle gusset TR near"
  ge = grp.entities
  f = ge.add_face([4609.mm,110.mm,2238.mm], [4609.mm,0.mm,2238.mm], [4609.mm,0.mm,2118.mm])
  f.pushpull(8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TR near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR near"
  ge = grp.entities
  circle = ge.add_circle([4559.mm,-48.mm,2198.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TR near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR near"
  ge = grp.entities
  circle = ge.add_circle([4559.mm,-48.mm,2298.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TR near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR near"
  ge = grp.entities
  circle = ge.add_circle([4659.mm,-48.mm,2198.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TR near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR near"
  ge = grp.entities
  circle = ge.add_circle([4659.mm,-48.mm,2298.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail fixing bolt TR near
  grp = ents.add_group
  grp.name = "Rail fixing bolt TR near"
  ge = grp.entities
  circle = ge.add_circle([4609.mm,25.mm,2248.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail fixing bolt TR near
  grp = ents.add_group
  grp.name = "Rail fixing bolt TR near"
  ge = grp.entities
  circle = ge.add_circle([4609.mm,85.mm,2248.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle back-plate TR far
  grp = ents.add_group
  grp.name = "Saddle back-plate TR far"
  face = grp.entities.add_face([4534.mm,2354.mm,2173.mm], [4684.mm,2354.mm,2173.mm], [4684.mm,2362.mm,2173.mm], [4534.mm,2362.mm,2173.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle OUTSIDE plate TR far
  grp = ents.add_group
  grp.name = "Saddle OUTSIDE plate TR far"
  face = grp.entities.add_face([4534.mm,2402.mm,2173.mm], [4684.mm,2402.mm,2173.mm], [4684.mm,2410.mm,2173.mm], [4534.mm,2410.mm,2173.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle seat TR far
  grp = ents.add_group
  grp.name = "Saddle seat TR far"
  face = grp.entities.add_face([4585.mm,2252.mm,2238.mm], [4633.mm,2252.mm,2238.mm], [4633.mm,2362.mm,2238.mm], [4585.mm,2362.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle gusset TR far
  grp = ents.add_group
  grp.name = "Saddle gusset TR far"
  ge = grp.entities
  f = ge.add_face([4609.mm,2252.mm,2238.mm], [4609.mm,2362.mm,2238.mm], [4609.mm,2362.mm,2118.mm])
  f.pushpull(8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TR far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR far"
  ge = grp.entities
  circle = ge.add_circle([4559.mm,2354.mm,2198.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TR far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR far"
  ge = grp.entities
  circle = ge.add_circle([4559.mm,2354.mm,2298.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TR far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR far"
  ge = grp.entities
  circle = ge.add_circle([4659.mm,2354.mm,2198.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TR far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR far"
  ge = grp.entities
  circle = ge.add_circle([4659.mm,2354.mm,2298.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail fixing bolt TR far
  grp = ents.add_group
  grp.name = "Rail fixing bolt TR far"
  ge = grp.entities
  circle = ge.add_circle([4609.mm,2277.mm,2248.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail fixing bolt TR far
  grp = ents.add_group
  grp.name = "Rail fixing bolt TR far"
  ge = grp.entities
  circle = ge.add_circle([4609.mm,2337.mm,2248.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle back-plate BL near
  grp = ents.add_group
  grp.name = "Saddle back-plate BL near"
  face = grp.entities.add_face([75.mm,0.mm,75.mm], [225.mm,0.mm,75.mm], [225.mm,8.mm,75.mm], [75.mm,8.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle OUTSIDE plate BL near
  grp = ents.add_group
  grp.name = "Saddle OUTSIDE plate BL near"
  face = grp.entities.add_face([75.mm,-48.mm,75.mm], [225.mm,-48.mm,75.mm], [225.mm,-40.mm,75.mm], [75.mm,-40.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle seat BL near
  grp = ents.add_group
  grp.name = "Saddle seat BL near"
  face = grp.entities.add_face([126.mm,0.mm,140.mm], [174.mm,0.mm,140.mm], [174.mm,110.mm,140.mm], [126.mm,110.mm,140.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle gusset BL near
  grp = ents.add_group
  grp.name = "Saddle gusset BL near"
  ge = grp.entities
  f = ge.add_face([150.mm,110.mm,140.mm], [150.mm,0.mm,140.mm], [150.mm,0.mm,20.mm])
  f.pushpull(8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BL near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BL near"
  ge = grp.entities
  circle = ge.add_circle([100.mm,-48.mm,100.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BL near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BL near"
  ge = grp.entities
  circle = ge.add_circle([100.mm,-48.mm,200.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BL near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BL near"
  ge = grp.entities
  circle = ge.add_circle([200.mm,-48.mm,100.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BL near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BL near"
  ge = grp.entities
  circle = ge.add_circle([200.mm,-48.mm,200.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Thumb screw BL near
  grp = ents.add_group
  grp.name = "Thumb screw BL near"
  ge = grp.entities
  circle = ge.add_circle([150.mm,25.mm,150.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Thumb screw BL near
  grp = ents.add_group
  grp.name = "Thumb screw BL near"
  ge = grp.entities
  circle = ge.add_circle([150.mm,85.mm,150.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle back-plate BL far
  grp = ents.add_group
  grp.name = "Saddle back-plate BL far"
  face = grp.entities.add_face([75.mm,2354.mm,75.mm], [225.mm,2354.mm,75.mm], [225.mm,2362.mm,75.mm], [75.mm,2362.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle OUTSIDE plate BL far
  grp = ents.add_group
  grp.name = "Saddle OUTSIDE plate BL far"
  face = grp.entities.add_face([75.mm,2402.mm,75.mm], [225.mm,2402.mm,75.mm], [225.mm,2410.mm,75.mm], [75.mm,2410.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle seat BL far
  grp = ents.add_group
  grp.name = "Saddle seat BL far"
  face = grp.entities.add_face([126.mm,2252.mm,140.mm], [174.mm,2252.mm,140.mm], [174.mm,2362.mm,140.mm], [126.mm,2362.mm,140.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle gusset BL far
  grp = ents.add_group
  grp.name = "Saddle gusset BL far"
  ge = grp.entities
  f = ge.add_face([150.mm,2252.mm,140.mm], [150.mm,2362.mm,140.mm], [150.mm,2362.mm,20.mm])
  f.pushpull(8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BL far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BL far"
  ge = grp.entities
  circle = ge.add_circle([100.mm,2354.mm,100.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BL far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BL far"
  ge = grp.entities
  circle = ge.add_circle([100.mm,2354.mm,200.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BL far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BL far"
  ge = grp.entities
  circle = ge.add_circle([200.mm,2354.mm,100.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BL far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BL far"
  ge = grp.entities
  circle = ge.add_circle([200.mm,2354.mm,200.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Thumb screw BL far
  grp = ents.add_group
  grp.name = "Thumb screw BL far"
  ge = grp.entities
  circle = ge.add_circle([150.mm,2277.mm,150.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Thumb screw BL far
  grp = ents.add_group
  grp.name = "Thumb screw BL far"
  ge = grp.entities
  circle = ge.add_circle([150.mm,2337.mm,150.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
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
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Frame Top
  grp = ents.add_group
  grp.name = "FP Frame Top"
  face = grp.entities.add_face([150.mm,2211.2.mm,2337.2.mm], [4649.mm,2211.2.mm,2337.2.mm], [4649.mm,2262.mm,2337.2.mm], [150.mm,2262.mm,2337.2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Frame Left
  grp = ents.add_group
  grp.name = "FP Frame Left"
  face = grp.entities.add_face([150.mm,2211.2.mm,0.mm], [200.8.mm,2211.2.mm,0.mm], [200.8.mm,2262.mm,0.mm], [150.mm,2262.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Frame Right
  grp = ents.add_group
  grp.name = "FP Frame Right"
  face = grp.entities.add_face([4598.2.mm,2211.2.mm,0.mm], [4649.mm,2211.2.mm,0.mm], [4649.mm,2262.mm,0.mm], [4598.2.mm,2262.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Film Plane Mechanism"
  inst.layer = model.layers["Film Plane"]

  # ═══ FP Combined Corner Plates ═══
  defn = model.definitions.add("FP Combined Corner Plates")
  ents = defn.entities
  # FP combined corner plate (near)
  grp = ents.add_group
  grp.name = "FP combined corner plate (near)"
  face = grp.entities.add_face([4574.mm,0.mm,58.mm], [4724.mm,0.mm,58.mm], [4724.mm,10.mm,58.mm], [4574.mm,10.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(167.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner ext plate (near)
  grp = ents.add_group
  grp.name = "FP combined corner ext plate (near)"
  face = grp.entities.add_face([4574.mm,-50.mm,58.mm], [4724.mm,-50.mm,58.mm], [4724.mm,-40.mm,58.mm], [4574.mm,-40.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(167.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined right-beam seat (near)
  grp = ents.add_group
  grp.name = "FP combined right-beam seat (near)"
  face = grp.entities.add_face([4574.mm,0.mm,58.mm], [4724.mm,0.mm,58.mm], [4724.mm,55.mm,58.mm], [4574.mm,55.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined BR rail seat (near)
  grp = ents.add_group
  grp.name = "FP combined BR rail seat (near)"
  face = grp.entities.add_face([4619.mm,0.mm,138.mm], [4679.mm,0.mm,138.mm], [4679.mm,55.mm,138.mm], [4619.mm,55.mm,138.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X4599 Z178
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X4599 Z178"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,-50.mm,178.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X4699 Z178
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X4699 Z178"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,-50.mm,178.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner plate (far)
  grp = ents.add_group
  grp.name = "FP combined corner plate (far)"
  face = grp.entities.add_face([4574.mm,2352.mm,58.mm], [4724.mm,2352.mm,58.mm], [4724.mm,2362.mm,58.mm], [4574.mm,2362.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(167.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner ext plate (far)
  grp = ents.add_group
  grp.name = "FP combined corner ext plate (far)"
  face = grp.entities.add_face([4574.mm,2402.mm,58.mm], [4724.mm,2402.mm,58.mm], [4724.mm,2412.mm,58.mm], [4574.mm,2412.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(167.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined right-beam seat (far)
  grp = ents.add_group
  grp.name = "FP combined right-beam seat (far)"
  face = grp.entities.add_face([4574.mm,2307.mm,58.mm], [4724.mm,2307.mm,58.mm], [4724.mm,2362.mm,58.mm], [4574.mm,2362.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined BR rail seat (far)
  grp = ents.add_group
  grp.name = "FP combined BR rail seat (far)"
  face = grp.entities.add_face([4619.mm,2307.mm,138.mm], [4679.mm,2307.mm,138.mm], [4679.mm,2362.mm,138.mm], [4619.mm,2362.mm,138.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (far) X4599 Z178
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (far) X4599 Z178"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,2352.mm,178.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (far) X4699 Z178
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (far) X4699 Z178"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,2352.mm,178.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "FP Combined Corner Plates"
  inst.layer = model.layers["Combined Plate"]

  # ═══ Panel & Pivot Axle ═══
  defn = model.definitions.add("Panel & Pivot Axle")
  ents = defn.entities
  # Pivot post (Ø89 CHS)
  grp = ents.add_group
  grp.name = "Pivot post (Ø89 CHS)"
  ge = grp.entities
  circle = ge.add_circle([175.mm,2287.mm,0.mm], [0,0,1], 44.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2388.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Pivot floor mount plate
  grp = ents.add_group
  grp.name = "Pivot floor mount plate"
  ge = grp.entities
  circle = ge.add_circle([175.mm,2287.mm,0.mm], [0,0,1], 110.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Pivot roof mount plate
  grp = ents.add_group
  grp.name = "Pivot roof mount plate"
  ge = grp.entities
  circle = ge.add_circle([175.mm,2287.mm,2368.mm], [0,0,1], 110.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Pivot thrust collar
  grp = ents.add_group
  grp.name = "Pivot thrust collar"
  ge = grp.entities
  circle = ge.add_circle([175.mm,2287.mm,130.mm], [0,0,1], 75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(25.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cargo Door Panel
  grp = ents.add_group
  grp.name = "Cargo Door Panel"
  face = grp.entities.add_face([0.mm,0.mm,130.mm], [120.mm,0.mm,130.mm], [120.mm,2362.mm,130.mm], [0.mm,2362.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2170.mm)
  mat = model.materials["Cargo Door Panel"] || model.materials.add("Cargo Door Panel")
  mat.color = Sketchup::Color.new(110, 140, 160)
  mat.alpha = 0.6
  grp.material = mat

  # Fan B mount band (18mm ply)
  grp = ents.add_group
  grp.name = "Fan B mount band (18mm ply)"
  face = grp.entities.add_face([0.mm,0.mm,130.mm], [120.mm,0.mm,130.mm], [120.mm,653.mm,130.mm], [0.mm,653.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(995.mm)
  mat = model.materials["Fan B mount band (18mm ply)"] || model.materials.add("Fan B mount band (18mm ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 0.6
  grp.material = mat

  # Stay inside plate
  grp = ents.add_group
  grp.name = "Stay inside plate"
  face = grp.entities.add_face([1695.mm,0.mm,400.mm], [1895.mm,0.mm,400.mm], [1895.mm,12.mm,400.mm], [1695.mm,12.mm,400.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay outside plate
  grp = ents.add_group
  grp.name = "Stay outside plate"
  face = grp.entities.add_face([1695.mm,-52.mm,400.mm], [1895.mm,-52.mm,400.mm], [1895.mm,-40.mm,400.mm], [1695.mm,-40.mm,400.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay eye
  grp = ents.add_group
  grp.name = "Stay eye"
  face = grp.entities.add_face([1780.mm,12.mm,485.mm], [1810.mm,12.mm,485.mm], [1810.mm,67.mm,485.mm], [1780.mm,67.mm,485.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1717.mm,-58.mm,422.mm], [1733.mm,-58.mm,422.mm], [1733.mm,18.mm,422.mm], [1717.mm,18.mm,422.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1717.mm,-58.mm,562.mm], [1733.mm,-58.mm,562.mm], [1733.mm,18.mm,562.mm], [1717.mm,18.mm,562.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1857.mm,-58.mm,422.mm], [1873.mm,-58.mm,422.mm], [1873.mm,18.mm,422.mm], [1857.mm,18.mm,422.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1857.mm,-58.mm,562.mm], [1873.mm,-58.mm,562.mm], [1873.mm,18.mm,562.mm], [1857.mm,18.mm,562.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay inside plate
  grp = ents.add_group
  grp.name = "Stay inside plate"
  face = grp.entities.add_face([1695.mm,0.mm,1950.mm], [1895.mm,0.mm,1950.mm], [1895.mm,12.mm,1950.mm], [1695.mm,12.mm,1950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay outside plate
  grp = ents.add_group
  grp.name = "Stay outside plate"
  face = grp.entities.add_face([1695.mm,-52.mm,1950.mm], [1895.mm,-52.mm,1950.mm], [1895.mm,-40.mm,1950.mm], [1695.mm,-40.mm,1950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay eye
  grp = ents.add_group
  grp.name = "Stay eye"
  face = grp.entities.add_face([1780.mm,12.mm,2035.mm], [1810.mm,12.mm,2035.mm], [1810.mm,67.mm,2035.mm], [1780.mm,67.mm,2035.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1717.mm,-58.mm,1972.mm], [1733.mm,-58.mm,1972.mm], [1733.mm,18.mm,1972.mm], [1717.mm,18.mm,1972.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1717.mm,-58.mm,2112.mm], [1733.mm,-58.mm,2112.mm], [1733.mm,18.mm,2112.mm], [1717.mm,18.mm,2112.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1857.mm,-58.mm,1972.mm], [1873.mm,-58.mm,1972.mm], [1873.mm,18.mm,1972.mm], [1857.mm,18.mm,1972.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1857.mm,-58.mm,2112.mm], [1873.mm,-58.mm,2112.mm], [1873.mm,18.mm,2112.mm], [1857.mm,18.mm,2112.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay hook (frame)
  grp = ents.add_group
  grp.name = "Stay hook (frame)"
  face = grp.entities.add_face([-10.mm,175.mm,465.mm], [50.mm,175.mm,465.mm], [50.mm,235.mm,465.mm], [-10.mm,235.mm,465.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay hook (frame)
  grp = ents.add_group
  grp.name = "Stay hook (frame)"
  face = grp.entities.add_face([-10.mm,175.mm,2015.mm], [50.mm,175.mm,2015.mm], [50.mm,235.mm,2015.mm], [-10.mm,235.mm,2015.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Panel & Pivot Axle"
  inst.layer = model.layers["Pivot Axle"]

  # ═══ Spray Bar ═══
  defn = model.definitions.add("Spray Bar")
  ents = defn.entities
  # Spray Beam 40x40x3 Al SHS
  grp = ents.add_group
  grp.name = "Spray Beam 40x40x3 Al SHS"
  face = grp.entities.add_face([200.mm,1160.mm,20.mm], [4599.mm,1160.mm,20.mm], [4599.mm,1200.mm,20.mm], [200.mm,1200.mm,20.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Spray Beam 40x40x3 Al SHS"] || model.materials.add("Spray Beam 40x40x3 Al SHS")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.45
  grp.material = mat

  # Beam End Cap (feed)
  grp = ents.add_group
  grp.name = "Beam End Cap (feed)"
  face = grp.entities.add_face([196.mm,1160.mm,20.mm], [200.mm,1160.mm,20.mm], [200.mm,1200.mm,20.mm], [196.mm,1200.mm,20.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Beam End Cap (feed)"] || model.materials.add("Beam End Cap (feed)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Beam End Cap
  grp = ents.add_group
  grp.name = "Beam End Cap"
  face = grp.entities.add_face([4599.mm,1160.mm,20.mm], [4603.mm,1160.mm,20.mm], [4603.mm,1200.mm,20.mm], [4599.mm,1200.mm,20.mm])
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
  circle = ge.add_circle([200.mm,1180.mm,40.mm], [1,0,0], 12.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(4399.mm)
  mat = model.materials["Irrigation Poly Pipe (3/4 LDPE)"] || model.materials.add("Irrigation Poly Pipe (3/4 LDPE)")
  mat.color = Sketchup::Color.new(42, 42, 42)
  mat.alpha = 1.0
  grp.material = mat

  # Water in Pipe
  grp = ents.add_group
  grp.name = "Water in Pipe"
  ge = grp.entities
  circle = ge.add_circle([200.mm,1180.mm,40.mm], [1,0,0], 9.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(4399.mm)
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
  face = grp.entities.add_face([200.mm,1062.mm,29.mm], [240.mm,1062.mm,29.mm], [240.mm,1160.mm,29.mm], [200.mm,1160.mm,29.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["Beam End Cap (feed)"] || model.materials.add("Beam End Cap (feed)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage Plate R L
  grp = ents.add_group
  grp.name = "Carriage Plate R L"
  face = grp.entities.add_face([200.mm,1200.mm,29.mm], [240.mm,1200.mm,29.mm], [240.mm,1298.mm,29.mm], [200.mm,1298.mm,29.mm])
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
  circle = ge.add_circle([210.mm,1080.mm,27.mm], [1,0,0], 25.mm, 24)
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
  circle = ge.add_circle([196.mm,1080.mm,27.mm], [1,0,0], 5.mm, 24)
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
  face = ge.add_face([[201.mm,1072.mm,27.mm], [201.mm,1072.07.mm,25.96.mm], [201.mm,1072.27.mm,24.93.mm], [201.mm,1072.61.mm,23.94.mm], [201.mm,1073.07.mm,23.mm], [201.mm,1073.65.mm,22.13.mm], [201.mm,1074.34.mm,21.34.mm], [201.mm,1075.13.mm,20.65.mm], [201.mm,1076.mm,20.07.mm], [201.mm,1076.94.mm,19.61.mm], [201.mm,1077.93.mm,19.27.mm], [201.mm,1078.96.mm,19.07.mm], [201.mm,1080.mm,19.mm], [201.mm,1081.04.mm,19.07.mm], [201.mm,1082.07.mm,19.27.mm], [201.mm,1083.06.mm,19.61.mm], [201.mm,1084.mm,20.07.mm], [201.mm,1084.87.mm,20.65.mm], [201.mm,1085.66.mm,21.34.mm], [201.mm,1086.35.mm,22.13.mm], [201.mm,1086.93.mm,23.mm], [201.mm,1087.39.mm,23.94.mm], [201.mm,1087.73.mm,24.93.mm], [201.mm,1087.93.mm,25.96.mm], [201.mm,1088.mm,27.mm], [201.mm,1086.mm,27.mm], [201.mm,1085.95.mm,26.22.mm], [201.mm,1085.8.mm,25.45.mm], [201.mm,1085.54.mm,24.7.mm], [201.mm,1085.2.mm,24.mm], [201.mm,1084.76.mm,23.35.mm], [201.mm,1084.24.mm,22.76.mm], [201.mm,1083.65.mm,22.24.mm], [201.mm,1083.mm,21.8.mm], [201.mm,1082.3.mm,21.46.mm], [201.mm,1081.55.mm,21.2.mm], [201.mm,1080.78.mm,21.05.mm], [201.mm,1080.mm,21.mm], [201.mm,1079.22.mm,21.05.mm], [201.mm,1078.45.mm,21.2.mm], [201.mm,1077.7.mm,21.46.mm], [201.mm,1077.mm,21.8.mm], [201.mm,1076.35.mm,22.24.mm], [201.mm,1075.76.mm,22.76.mm], [201.mm,1075.24.mm,23.35.mm], [201.mm,1074.8.mm,24.mm], [201.mm,1074.46.mm,24.7.mm], [201.mm,1074.2.mm,25.45.mm], [201.mm,1074.05.mm,26.22.mm], [201.mm,1074.mm,27.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([201.mm,1064.mm,27.mm], [207.mm,1064.mm,27.mm], [207.mm,1074.mm,27.mm], [201.mm,1074.mm,27.mm])
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
  circle = ge.add_circle([204.mm,1069.mm,25.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([201.mm,1086.mm,27.mm], [207.mm,1086.mm,27.mm], [207.mm,1096.mm,27.mm], [201.mm,1096.mm,27.mm])
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
  circle = ge.add_circle([204.mm,1091.mm,25.mm], [0,0,1], 2.5.mm, 24)
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
  face = ge.add_face([[233.mm,1072.mm,27.mm], [233.mm,1072.07.mm,25.96.mm], [233.mm,1072.27.mm,24.93.mm], [233.mm,1072.61.mm,23.94.mm], [233.mm,1073.07.mm,23.mm], [233.mm,1073.65.mm,22.13.mm], [233.mm,1074.34.mm,21.34.mm], [233.mm,1075.13.mm,20.65.mm], [233.mm,1076.mm,20.07.mm], [233.mm,1076.94.mm,19.61.mm], [233.mm,1077.93.mm,19.27.mm], [233.mm,1078.96.mm,19.07.mm], [233.mm,1080.mm,19.mm], [233.mm,1081.04.mm,19.07.mm], [233.mm,1082.07.mm,19.27.mm], [233.mm,1083.06.mm,19.61.mm], [233.mm,1084.mm,20.07.mm], [233.mm,1084.87.mm,20.65.mm], [233.mm,1085.66.mm,21.34.mm], [233.mm,1086.35.mm,22.13.mm], [233.mm,1086.93.mm,23.mm], [233.mm,1087.39.mm,23.94.mm], [233.mm,1087.73.mm,24.93.mm], [233.mm,1087.93.mm,25.96.mm], [233.mm,1088.mm,27.mm], [233.mm,1086.mm,27.mm], [233.mm,1085.95.mm,26.22.mm], [233.mm,1085.8.mm,25.45.mm], [233.mm,1085.54.mm,24.7.mm], [233.mm,1085.2.mm,24.mm], [233.mm,1084.76.mm,23.35.mm], [233.mm,1084.24.mm,22.76.mm], [233.mm,1083.65.mm,22.24.mm], [233.mm,1083.mm,21.8.mm], [233.mm,1082.3.mm,21.46.mm], [233.mm,1081.55.mm,21.2.mm], [233.mm,1080.78.mm,21.05.mm], [233.mm,1080.mm,21.mm], [233.mm,1079.22.mm,21.05.mm], [233.mm,1078.45.mm,21.2.mm], [233.mm,1077.7.mm,21.46.mm], [233.mm,1077.mm,21.8.mm], [233.mm,1076.35.mm,22.24.mm], [233.mm,1075.76.mm,22.76.mm], [233.mm,1075.24.mm,23.35.mm], [233.mm,1074.8.mm,24.mm], [233.mm,1074.46.mm,24.7.mm], [233.mm,1074.2.mm,25.45.mm], [233.mm,1074.05.mm,26.22.mm], [233.mm,1074.mm,27.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([233.mm,1064.mm,27.mm], [239.mm,1064.mm,27.mm], [239.mm,1074.mm,27.mm], [233.mm,1074.mm,27.mm])
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
  circle = ge.add_circle([236.mm,1069.mm,25.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([233.mm,1086.mm,27.mm], [239.mm,1086.mm,27.mm], [239.mm,1096.mm,27.mm], [233.mm,1096.mm,27.mm])
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
  circle = ge.add_circle([236.mm,1091.mm,25.mm], [0,0,1], 2.5.mm, 24)
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
  circle = ge.add_circle([210.mm,1280.mm,27.mm], [1,0,0], 25.mm, 24)
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
  circle = ge.add_circle([196.mm,1280.mm,27.mm], [1,0,0], 5.mm, 24)
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
  face = ge.add_face([[201.mm,1272.mm,27.mm], [201.mm,1272.07.mm,25.96.mm], [201.mm,1272.27.mm,24.93.mm], [201.mm,1272.61.mm,23.94.mm], [201.mm,1273.07.mm,23.mm], [201.mm,1273.65.mm,22.13.mm], [201.mm,1274.34.mm,21.34.mm], [201.mm,1275.13.mm,20.65.mm], [201.mm,1276.mm,20.07.mm], [201.mm,1276.94.mm,19.61.mm], [201.mm,1277.93.mm,19.27.mm], [201.mm,1278.96.mm,19.07.mm], [201.mm,1280.mm,19.mm], [201.mm,1281.04.mm,19.07.mm], [201.mm,1282.07.mm,19.27.mm], [201.mm,1283.06.mm,19.61.mm], [201.mm,1284.mm,20.07.mm], [201.mm,1284.87.mm,20.65.mm], [201.mm,1285.66.mm,21.34.mm], [201.mm,1286.35.mm,22.13.mm], [201.mm,1286.93.mm,23.mm], [201.mm,1287.39.mm,23.94.mm], [201.mm,1287.73.mm,24.93.mm], [201.mm,1287.93.mm,25.96.mm], [201.mm,1288.mm,27.mm], [201.mm,1286.mm,27.mm], [201.mm,1285.95.mm,26.22.mm], [201.mm,1285.8.mm,25.45.mm], [201.mm,1285.54.mm,24.7.mm], [201.mm,1285.2.mm,24.mm], [201.mm,1284.76.mm,23.35.mm], [201.mm,1284.24.mm,22.76.mm], [201.mm,1283.65.mm,22.24.mm], [201.mm,1283.mm,21.8.mm], [201.mm,1282.3.mm,21.46.mm], [201.mm,1281.55.mm,21.2.mm], [201.mm,1280.78.mm,21.05.mm], [201.mm,1280.mm,21.mm], [201.mm,1279.22.mm,21.05.mm], [201.mm,1278.45.mm,21.2.mm], [201.mm,1277.7.mm,21.46.mm], [201.mm,1277.mm,21.8.mm], [201.mm,1276.35.mm,22.24.mm], [201.mm,1275.76.mm,22.76.mm], [201.mm,1275.24.mm,23.35.mm], [201.mm,1274.8.mm,24.mm], [201.mm,1274.46.mm,24.7.mm], [201.mm,1274.2.mm,25.45.mm], [201.mm,1274.05.mm,26.22.mm], [201.mm,1274.mm,27.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([201.mm,1264.mm,27.mm], [207.mm,1264.mm,27.mm], [207.mm,1274.mm,27.mm], [201.mm,1274.mm,27.mm])
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
  circle = ge.add_circle([204.mm,1269.mm,25.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([201.mm,1286.mm,27.mm], [207.mm,1286.mm,27.mm], [207.mm,1296.mm,27.mm], [201.mm,1296.mm,27.mm])
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
  circle = ge.add_circle([204.mm,1291.mm,25.mm], [0,0,1], 2.5.mm, 24)
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
  face = ge.add_face([[233.mm,1272.mm,27.mm], [233.mm,1272.07.mm,25.96.mm], [233.mm,1272.27.mm,24.93.mm], [233.mm,1272.61.mm,23.94.mm], [233.mm,1273.07.mm,23.mm], [233.mm,1273.65.mm,22.13.mm], [233.mm,1274.34.mm,21.34.mm], [233.mm,1275.13.mm,20.65.mm], [233.mm,1276.mm,20.07.mm], [233.mm,1276.94.mm,19.61.mm], [233.mm,1277.93.mm,19.27.mm], [233.mm,1278.96.mm,19.07.mm], [233.mm,1280.mm,19.mm], [233.mm,1281.04.mm,19.07.mm], [233.mm,1282.07.mm,19.27.mm], [233.mm,1283.06.mm,19.61.mm], [233.mm,1284.mm,20.07.mm], [233.mm,1284.87.mm,20.65.mm], [233.mm,1285.66.mm,21.34.mm], [233.mm,1286.35.mm,22.13.mm], [233.mm,1286.93.mm,23.mm], [233.mm,1287.39.mm,23.94.mm], [233.mm,1287.73.mm,24.93.mm], [233.mm,1287.93.mm,25.96.mm], [233.mm,1288.mm,27.mm], [233.mm,1286.mm,27.mm], [233.mm,1285.95.mm,26.22.mm], [233.mm,1285.8.mm,25.45.mm], [233.mm,1285.54.mm,24.7.mm], [233.mm,1285.2.mm,24.mm], [233.mm,1284.76.mm,23.35.mm], [233.mm,1284.24.mm,22.76.mm], [233.mm,1283.65.mm,22.24.mm], [233.mm,1283.mm,21.8.mm], [233.mm,1282.3.mm,21.46.mm], [233.mm,1281.55.mm,21.2.mm], [233.mm,1280.78.mm,21.05.mm], [233.mm,1280.mm,21.mm], [233.mm,1279.22.mm,21.05.mm], [233.mm,1278.45.mm,21.2.mm], [233.mm,1277.7.mm,21.46.mm], [233.mm,1277.mm,21.8.mm], [233.mm,1276.35.mm,22.24.mm], [233.mm,1275.76.mm,22.76.mm], [233.mm,1275.24.mm,23.35.mm], [233.mm,1274.8.mm,24.mm], [233.mm,1274.46.mm,24.7.mm], [233.mm,1274.2.mm,25.45.mm], [233.mm,1274.05.mm,26.22.mm], [233.mm,1274.mm,27.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([233.mm,1264.mm,27.mm], [239.mm,1264.mm,27.mm], [239.mm,1274.mm,27.mm], [233.mm,1274.mm,27.mm])
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
  circle = ge.add_circle([236.mm,1269.mm,25.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([233.mm,1286.mm,27.mm], [239.mm,1286.mm,27.mm], [239.mm,1296.mm,27.mm], [233.mm,1296.mm,27.mm])
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
  circle = ge.add_circle([236.mm,1291.mm,25.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([200.mm,1148.mm,17.mm], [240.mm,1148.mm,17.mm], [240.mm,1212.mm,17.mm], [200.mm,1212.mm,17.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Top Clamp L
  grp = ents.add_group
  grp.name = "Top Clamp L"
  face = grp.entities.add_face([200.mm,1148.mm,60.mm], [240.mm,1148.mm,60.mm], [240.mm,1212.mm,60.mm], [200.mm,1212.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Spacer L
  grp = ents.add_group
  grp.name = "Clamp Spacer L"
  face = grp.entities.add_face([204.mm,1152.mm,20.mm], [236.mm,1152.mm,20.mm], [236.mm,1160.mm,20.mm], [204.mm,1160.mm,20.mm])
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
  circle = ge.add_circle([209.mm,1156.mm,13.mm], [0,0,1], 2.5.mm, 24)
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
  circle = ge.add_circle([231.mm,1156.mm,13.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([204.mm,1200.mm,20.mm], [236.mm,1200.mm,20.mm], [236.mm,1208.mm,20.mm], [204.mm,1208.mm,20.mm])
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
  circle = ge.add_circle([209.mm,1204.mm,13.mm], [0,0,1], 2.5.mm, 24)
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
  circle = ge.add_circle([231.mm,1204.mm,13.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([4559.mm,1062.mm,29.mm], [4599.mm,1062.mm,29.mm], [4599.mm,1160.mm,29.mm], [4559.mm,1160.mm,29.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["Beam End Cap (feed)"] || model.materials.add("Beam End Cap (feed)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage Plate R R
  grp = ents.add_group
  grp.name = "Carriage Plate R R"
  face = grp.entities.add_face([4559.mm,1200.mm,29.mm], [4599.mm,1200.mm,29.mm], [4599.mm,1298.mm,29.mm], [4559.mm,1298.mm,29.mm])
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
  circle = ge.add_circle([4569.mm,1080.mm,27.mm], [1,0,0], 25.mm, 24)
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
  circle = ge.add_circle([4555.mm,1080.mm,27.mm], [1,0,0], 5.mm, 24)
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
  face = ge.add_face([[4560.mm,1072.mm,27.mm], [4560.mm,1072.07.mm,25.96.mm], [4560.mm,1072.27.mm,24.93.mm], [4560.mm,1072.61.mm,23.94.mm], [4560.mm,1073.07.mm,23.mm], [4560.mm,1073.65.mm,22.13.mm], [4560.mm,1074.34.mm,21.34.mm], [4560.mm,1075.13.mm,20.65.mm], [4560.mm,1076.mm,20.07.mm], [4560.mm,1076.94.mm,19.61.mm], [4560.mm,1077.93.mm,19.27.mm], [4560.mm,1078.96.mm,19.07.mm], [4560.mm,1080.mm,19.mm], [4560.mm,1081.04.mm,19.07.mm], [4560.mm,1082.07.mm,19.27.mm], [4560.mm,1083.06.mm,19.61.mm], [4560.mm,1084.mm,20.07.mm], [4560.mm,1084.87.mm,20.65.mm], [4560.mm,1085.66.mm,21.34.mm], [4560.mm,1086.35.mm,22.13.mm], [4560.mm,1086.93.mm,23.mm], [4560.mm,1087.39.mm,23.94.mm], [4560.mm,1087.73.mm,24.93.mm], [4560.mm,1087.93.mm,25.96.mm], [4560.mm,1088.mm,27.mm], [4560.mm,1086.mm,27.mm], [4560.mm,1085.95.mm,26.22.mm], [4560.mm,1085.8.mm,25.45.mm], [4560.mm,1085.54.mm,24.7.mm], [4560.mm,1085.2.mm,24.mm], [4560.mm,1084.76.mm,23.35.mm], [4560.mm,1084.24.mm,22.76.mm], [4560.mm,1083.65.mm,22.24.mm], [4560.mm,1083.mm,21.8.mm], [4560.mm,1082.3.mm,21.46.mm], [4560.mm,1081.55.mm,21.2.mm], [4560.mm,1080.78.mm,21.05.mm], [4560.mm,1080.mm,21.mm], [4560.mm,1079.22.mm,21.05.mm], [4560.mm,1078.45.mm,21.2.mm], [4560.mm,1077.7.mm,21.46.mm], [4560.mm,1077.mm,21.8.mm], [4560.mm,1076.35.mm,22.24.mm], [4560.mm,1075.76.mm,22.76.mm], [4560.mm,1075.24.mm,23.35.mm], [4560.mm,1074.8.mm,24.mm], [4560.mm,1074.46.mm,24.7.mm], [4560.mm,1074.2.mm,25.45.mm], [4560.mm,1074.05.mm,26.22.mm], [4560.mm,1074.mm,27.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4560.mm,1064.mm,27.mm], [4566.mm,1064.mm,27.mm], [4566.mm,1074.mm,27.mm], [4560.mm,1074.mm,27.mm])
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
  circle = ge.add_circle([4563.mm,1069.mm,25.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([4560.mm,1086.mm,27.mm], [4566.mm,1086.mm,27.mm], [4566.mm,1096.mm,27.mm], [4560.mm,1096.mm,27.mm])
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
  circle = ge.add_circle([4563.mm,1091.mm,25.mm], [0,0,1], 2.5.mm, 24)
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
  face = ge.add_face([[4592.mm,1072.mm,27.mm], [4592.mm,1072.07.mm,25.96.mm], [4592.mm,1072.27.mm,24.93.mm], [4592.mm,1072.61.mm,23.94.mm], [4592.mm,1073.07.mm,23.mm], [4592.mm,1073.65.mm,22.13.mm], [4592.mm,1074.34.mm,21.34.mm], [4592.mm,1075.13.mm,20.65.mm], [4592.mm,1076.mm,20.07.mm], [4592.mm,1076.94.mm,19.61.mm], [4592.mm,1077.93.mm,19.27.mm], [4592.mm,1078.96.mm,19.07.mm], [4592.mm,1080.mm,19.mm], [4592.mm,1081.04.mm,19.07.mm], [4592.mm,1082.07.mm,19.27.mm], [4592.mm,1083.06.mm,19.61.mm], [4592.mm,1084.mm,20.07.mm], [4592.mm,1084.87.mm,20.65.mm], [4592.mm,1085.66.mm,21.34.mm], [4592.mm,1086.35.mm,22.13.mm], [4592.mm,1086.93.mm,23.mm], [4592.mm,1087.39.mm,23.94.mm], [4592.mm,1087.73.mm,24.93.mm], [4592.mm,1087.93.mm,25.96.mm], [4592.mm,1088.mm,27.mm], [4592.mm,1086.mm,27.mm], [4592.mm,1085.95.mm,26.22.mm], [4592.mm,1085.8.mm,25.45.mm], [4592.mm,1085.54.mm,24.7.mm], [4592.mm,1085.2.mm,24.mm], [4592.mm,1084.76.mm,23.35.mm], [4592.mm,1084.24.mm,22.76.mm], [4592.mm,1083.65.mm,22.24.mm], [4592.mm,1083.mm,21.8.mm], [4592.mm,1082.3.mm,21.46.mm], [4592.mm,1081.55.mm,21.2.mm], [4592.mm,1080.78.mm,21.05.mm], [4592.mm,1080.mm,21.mm], [4592.mm,1079.22.mm,21.05.mm], [4592.mm,1078.45.mm,21.2.mm], [4592.mm,1077.7.mm,21.46.mm], [4592.mm,1077.mm,21.8.mm], [4592.mm,1076.35.mm,22.24.mm], [4592.mm,1075.76.mm,22.76.mm], [4592.mm,1075.24.mm,23.35.mm], [4592.mm,1074.8.mm,24.mm], [4592.mm,1074.46.mm,24.7.mm], [4592.mm,1074.2.mm,25.45.mm], [4592.mm,1074.05.mm,26.22.mm], [4592.mm,1074.mm,27.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4592.mm,1064.mm,27.mm], [4598.mm,1064.mm,27.mm], [4598.mm,1074.mm,27.mm], [4592.mm,1074.mm,27.mm])
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
  circle = ge.add_circle([4595.mm,1069.mm,25.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([4592.mm,1086.mm,27.mm], [4598.mm,1086.mm,27.mm], [4598.mm,1096.mm,27.mm], [4592.mm,1096.mm,27.mm])
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
  circle = ge.add_circle([4595.mm,1091.mm,25.mm], [0,0,1], 2.5.mm, 24)
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
  circle = ge.add_circle([4569.mm,1280.mm,27.mm], [1,0,0], 25.mm, 24)
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
  circle = ge.add_circle([4555.mm,1280.mm,27.mm], [1,0,0], 5.mm, 24)
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
  face = ge.add_face([[4560.mm,1272.mm,27.mm], [4560.mm,1272.07.mm,25.96.mm], [4560.mm,1272.27.mm,24.93.mm], [4560.mm,1272.61.mm,23.94.mm], [4560.mm,1273.07.mm,23.mm], [4560.mm,1273.65.mm,22.13.mm], [4560.mm,1274.34.mm,21.34.mm], [4560.mm,1275.13.mm,20.65.mm], [4560.mm,1276.mm,20.07.mm], [4560.mm,1276.94.mm,19.61.mm], [4560.mm,1277.93.mm,19.27.mm], [4560.mm,1278.96.mm,19.07.mm], [4560.mm,1280.mm,19.mm], [4560.mm,1281.04.mm,19.07.mm], [4560.mm,1282.07.mm,19.27.mm], [4560.mm,1283.06.mm,19.61.mm], [4560.mm,1284.mm,20.07.mm], [4560.mm,1284.87.mm,20.65.mm], [4560.mm,1285.66.mm,21.34.mm], [4560.mm,1286.35.mm,22.13.mm], [4560.mm,1286.93.mm,23.mm], [4560.mm,1287.39.mm,23.94.mm], [4560.mm,1287.73.mm,24.93.mm], [4560.mm,1287.93.mm,25.96.mm], [4560.mm,1288.mm,27.mm], [4560.mm,1286.mm,27.mm], [4560.mm,1285.95.mm,26.22.mm], [4560.mm,1285.8.mm,25.45.mm], [4560.mm,1285.54.mm,24.7.mm], [4560.mm,1285.2.mm,24.mm], [4560.mm,1284.76.mm,23.35.mm], [4560.mm,1284.24.mm,22.76.mm], [4560.mm,1283.65.mm,22.24.mm], [4560.mm,1283.mm,21.8.mm], [4560.mm,1282.3.mm,21.46.mm], [4560.mm,1281.55.mm,21.2.mm], [4560.mm,1280.78.mm,21.05.mm], [4560.mm,1280.mm,21.mm], [4560.mm,1279.22.mm,21.05.mm], [4560.mm,1278.45.mm,21.2.mm], [4560.mm,1277.7.mm,21.46.mm], [4560.mm,1277.mm,21.8.mm], [4560.mm,1276.35.mm,22.24.mm], [4560.mm,1275.76.mm,22.76.mm], [4560.mm,1275.24.mm,23.35.mm], [4560.mm,1274.8.mm,24.mm], [4560.mm,1274.46.mm,24.7.mm], [4560.mm,1274.2.mm,25.45.mm], [4560.mm,1274.05.mm,26.22.mm], [4560.mm,1274.mm,27.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4560.mm,1264.mm,27.mm], [4566.mm,1264.mm,27.mm], [4566.mm,1274.mm,27.mm], [4560.mm,1274.mm,27.mm])
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
  circle = ge.add_circle([4563.mm,1269.mm,25.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([4560.mm,1286.mm,27.mm], [4566.mm,1286.mm,27.mm], [4566.mm,1296.mm,27.mm], [4560.mm,1296.mm,27.mm])
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
  circle = ge.add_circle([4563.mm,1291.mm,25.mm], [0,0,1], 2.5.mm, 24)
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
  face = ge.add_face([[4592.mm,1272.mm,27.mm], [4592.mm,1272.07.mm,25.96.mm], [4592.mm,1272.27.mm,24.93.mm], [4592.mm,1272.61.mm,23.94.mm], [4592.mm,1273.07.mm,23.mm], [4592.mm,1273.65.mm,22.13.mm], [4592.mm,1274.34.mm,21.34.mm], [4592.mm,1275.13.mm,20.65.mm], [4592.mm,1276.mm,20.07.mm], [4592.mm,1276.94.mm,19.61.mm], [4592.mm,1277.93.mm,19.27.mm], [4592.mm,1278.96.mm,19.07.mm], [4592.mm,1280.mm,19.mm], [4592.mm,1281.04.mm,19.07.mm], [4592.mm,1282.07.mm,19.27.mm], [4592.mm,1283.06.mm,19.61.mm], [4592.mm,1284.mm,20.07.mm], [4592.mm,1284.87.mm,20.65.mm], [4592.mm,1285.66.mm,21.34.mm], [4592.mm,1286.35.mm,22.13.mm], [4592.mm,1286.93.mm,23.mm], [4592.mm,1287.39.mm,23.94.mm], [4592.mm,1287.73.mm,24.93.mm], [4592.mm,1287.93.mm,25.96.mm], [4592.mm,1288.mm,27.mm], [4592.mm,1286.mm,27.mm], [4592.mm,1285.95.mm,26.22.mm], [4592.mm,1285.8.mm,25.45.mm], [4592.mm,1285.54.mm,24.7.mm], [4592.mm,1285.2.mm,24.mm], [4592.mm,1284.76.mm,23.35.mm], [4592.mm,1284.24.mm,22.76.mm], [4592.mm,1283.65.mm,22.24.mm], [4592.mm,1283.mm,21.8.mm], [4592.mm,1282.3.mm,21.46.mm], [4592.mm,1281.55.mm,21.2.mm], [4592.mm,1280.78.mm,21.05.mm], [4592.mm,1280.mm,21.mm], [4592.mm,1279.22.mm,21.05.mm], [4592.mm,1278.45.mm,21.2.mm], [4592.mm,1277.7.mm,21.46.mm], [4592.mm,1277.mm,21.8.mm], [4592.mm,1276.35.mm,22.24.mm], [4592.mm,1275.76.mm,22.76.mm], [4592.mm,1275.24.mm,23.35.mm], [4592.mm,1274.8.mm,24.mm], [4592.mm,1274.46.mm,24.7.mm], [4592.mm,1274.2.mm,25.45.mm], [4592.mm,1274.05.mm,26.22.mm], [4592.mm,1274.mm,27.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4592.mm,1264.mm,27.mm], [4598.mm,1264.mm,27.mm], [4598.mm,1274.mm,27.mm], [4592.mm,1274.mm,27.mm])
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
  circle = ge.add_circle([4595.mm,1269.mm,25.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([4592.mm,1286.mm,27.mm], [4598.mm,1286.mm,27.mm], [4598.mm,1296.mm,27.mm], [4592.mm,1296.mm,27.mm])
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
  circle = ge.add_circle([4595.mm,1291.mm,25.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([4559.mm,1148.mm,17.mm], [4599.mm,1148.mm,17.mm], [4599.mm,1212.mm,17.mm], [4559.mm,1212.mm,17.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Top Clamp R
  grp = ents.add_group
  grp.name = "Top Clamp R"
  face = grp.entities.add_face([4559.mm,1148.mm,60.mm], [4599.mm,1148.mm,60.mm], [4599.mm,1212.mm,60.mm], [4559.mm,1212.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Spacer R
  grp = ents.add_group
  grp.name = "Clamp Spacer R"
  face = grp.entities.add_face([4563.mm,1152.mm,20.mm], [4595.mm,1152.mm,20.mm], [4595.mm,1160.mm,20.mm], [4563.mm,1160.mm,20.mm])
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
  circle = ge.add_circle([4568.mm,1156.mm,13.mm], [0,0,1], 2.5.mm, 24)
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
  circle = ge.add_circle([4590.mm,1156.mm,13.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([4563.mm,1200.mm,20.mm], [4595.mm,1200.mm,20.mm], [4595.mm,1208.mm,20.mm], [4563.mm,1208.mm,20.mm])
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
  circle = ge.add_circle([4568.mm,1204.mm,13.mm], [0,0,1], 2.5.mm, 24)
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
  circle = ge.add_circle([4590.mm,1204.mm,13.mm], [0,0,1], 2.5.mm, 24)
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
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
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
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
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
  vec = Geom::Vector3d.new(-1913.2857142857142.mm, 0.mm, 0.mm)
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
  arc = ge.add_arc([519.2142857142858.mm,1205.mm,73.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([519.2142857142858.mm,1210.mm,73.mm], [-1.000000,0.000000,0.000000], 3.mm, 16)
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
  circle = ge.add_circle([514.2142857142858.mm,1205.mm,73.mm], vec, 3.mm, 16)
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
  arc = ge.add_arc([514.2142857142858.mm,1183.43.mm,69.57.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 3.43.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([514.2142857142858.mm,1183.43.mm,73.mm], [0.000000,-1.000000,0.000000], 3.mm, 16)
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
  circle = ge.add_circle([514.2142857142858.mm,1180.mm,69.57.mm], vec, 3.mm, 16)
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
  circle = ge.add_circle([514.2142857142858.mm,1180.mm,38.mm], [0,0,1], 4.mm, 24)
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
  vec = Geom::Vector3d.new(-1284.857142857143.mm, 0.mm, 0.mm)
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
  arc = ge.add_arc([1147.642857142857.mm,1205.mm,73.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1147.642857142857.mm,1210.mm,73.mm], [-1.000000,0.000000,0.000000], 3.mm, 16)
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
  circle = ge.add_circle([1142.642857142857.mm,1205.mm,73.mm], vec, 3.mm, 16)
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
  arc = ge.add_arc([1142.642857142857.mm,1183.43.mm,69.57.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 3.43.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1142.642857142857.mm,1183.43.mm,73.mm], [0.000000,-1.000000,0.000000], 3.mm, 16)
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
  circle = ge.add_circle([1142.642857142857.mm,1180.mm,69.57.mm], vec, 3.mm, 16)
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
  circle = ge.add_circle([1142.642857142857.mm,1180.mm,38.mm], [0,0,1], 4.mm, 24)
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
  vec = Geom::Vector3d.new(-656.4285714285713.mm, 0.mm, 0.mm)
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
  arc = ge.add_arc([1776.0714285714287.mm,1205.mm,73.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1776.0714285714287.mm,1210.mm,73.mm], [-1.000000,0.000000,0.000000], 3.mm, 16)
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
  circle = ge.add_circle([1771.0714285714287.mm,1205.mm,73.mm], vec, 3.mm, 16)
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
  arc = ge.add_arc([1771.0714285714287.mm,1183.43.mm,69.57.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 3.43.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1771.0714285714287.mm,1183.43.mm,73.mm], [0.000000,-1.000000,0.000000], 3.mm, 16)
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
  circle = ge.add_circle([1771.0714285714287.mm,1180.mm,69.57.mm], vec, 3.mm, 16)
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
  circle = ge.add_circle([1771.0714285714287.mm,1180.mm,38.mm], [0,0,1], 4.mm, 24)
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
  vec = Geom::Vector3d.new(572.9985714285717.mm, 0.mm, 0.mm)
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
  arc = ge.add_arc([3024.4985714285717.mm,1180.mm,69.57.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 3.43.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([3024.4985714285717.mm,1180.mm,73.mm], [1.000000,0.000000,0.000000], 3.mm, 16)
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
  circle = ge.add_circle([3027.9285714285716.mm,1180.mm,69.57.mm], vec, 3.mm, 16)
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
  circle = ge.add_circle([3027.9285714285716.mm,1180.mm,38.mm], [0,0,1], 4.mm, 24)
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
  vec = Geom::Vector3d.new(1201.4271428571428.mm, 0.mm, 0.mm)
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
  arc = ge.add_arc([3652.927142857143.mm,1180.mm,69.57.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 3.43.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([3652.927142857143.mm,1180.mm,73.mm], [1.000000,0.000000,0.000000], 3.mm, 16)
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
  circle = ge.add_circle([3656.3571428571427.mm,1180.mm,69.57.mm], vec, 3.mm, 16)
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
  circle = ge.add_circle([3656.3571428571427.mm,1180.mm,38.mm], [0,0,1], 4.mm, 24)
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
  vec = Geom::Vector3d.new(1829.8557142857135.mm, 0.mm, 0.mm)
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
  arc = ge.add_arc([4281.3557142857135.mm,1180.mm,69.57.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 3.43.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4281.3557142857135.mm,1180.mm,73.mm], [1.000000,0.000000,0.000000], 3.mm, 16)
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
  circle = ge.add_circle([4284.785714285714.mm,1180.mm,69.57.mm], vec, 3.mm, 16)
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
  circle = ge.add_circle([4284.785714285714.mm,1180.mm,38.mm], [0,0,1], 4.mm, 24)
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
  face = grp.entities.add_face([4874.mm,1046.mm,250.mm], [4892.mm,1046.mm,250.mm], [4892.mm,1316.mm,250.mm], [4874.mm,1316.mm,250.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2060.mm)
  mat = model.materials["Equipment Panel (ply)"] || model.materials.add("Equipment Panel (ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-01 (Blue)
  grp = ents.add_group
  grp.name = "Pump P-01 (Blue)"
  face = grp.entities.add_face([4760.mm,1045.5.mm,1370.mm], [4874.mm,1045.5.mm,1370.mm], [4874.mm,1172.5.mm,1370.mm], [4760.mm,1172.5.mm,1370.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-02 (Brown)
  grp = ents.add_group
  grp.name = "Pump P-02 (Brown)"
  face = grp.entities.add_face([4760.mm,1189.5.mm,1370.mm], [4874.mm,1189.5.mm,1370.mm], [4874.mm,1316.5.mm,1370.mm], [4760.mm,1316.5.mm,1370.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-04 (Tray drain)
  grp = ents.add_group
  grp.name = "Pump P-04 (Tray drain)"
  face = grp.entities.add_face([4760.mm,1045.5.mm,1628.mm], [4874.mm,1045.5.mm,1628.mm], [4874.mm,1172.5.mm,1628.mm], [4760.mm,1172.5.mm,1628.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-03 (Waste evac)
  grp = ents.add_group
  grp.name = "Pump P-03 (Waste evac)"
  face = grp.entities.add_face([4760.mm,1189.5.mm,1628.mm], [4874.mm,1189.5.mm,1628.mm], [4874.mm,1316.5.mm,1628.mm], [4760.mm,1316.5.mm,1628.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-05 (Brown drain)
  grp = ents.add_group
  grp.name = "Pump P-05 (Brown drain)"
  face = grp.entities.add_face([4760.mm,1189.5.mm,1996.mm], [4874.mm,1189.5.mm,1996.mm], [4874.mm,1316.5.mm,1996.mm], [4760.mm,1316.5.mm,1996.mm])
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
  circle = ge.add_circle([4811.mm,1109.mm,1996.mm], [0,0,1], 63.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(200.mm)
  mat = model.materials["ACC-01 Accumulator"] || model.materials.add("ACC-01 Accumulator")
  mat.color = Sketchup::Color.new(90, 154, 204)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F1 (50µ)
  grp = ents.add_group
  grp.name = "Filter F1 (50µ)"
  ge = grp.entities
  circle = ge.add_circle([4782.mm,1181.mm,250.mm], [0,0,1], 92.mm, 24)
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
  circle = ge.add_circle([4782.mm,1181.mm,620.mm], [0,0,1], 92.mm, 24)
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
  circle = ge.add_circle([4782.mm,1181.mm,990.mm], [0,0,1], 92.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(340.mm)
  mat = model.materials["Filter F1 (50µ)"] || model.materials.add("Filter F1 (50µ)")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # Drain-riser spine (ply)
  grp = ents.add_group
  grp.name = "Drain-riser spine (ply)"
  face = grp.entities.add_face([4874.mm,1223.mm,250.mm], [5420.mm,1223.mm,250.mm], [5420.mm,1241.mm,250.mm], [4874.mm,1241.mm,250.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2060.mm)
  mat = model.materials["Equipment Panel (ply)"] || model.materials.add("Equipment Panel (ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Drain-riser spine flange (ply)
  grp = ents.add_group
  grp.name = "Drain-riser spine flange (ply)"
  face = grp.entities.add_face([5402.mm,1226.mm,250.mm], [5420.mm,1226.mm,250.mm], [5420.mm,1280.mm,250.mm], [5402.mm,1280.mm,250.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2060.mm)
  mat = model.materials["Equipment Panel (ply)"] || model.materials.add("Equipment Panel (ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Riser pipe clamp
  grp = ents.add_group
  grp.name = "Riser pipe clamp"
  face = grp.entities.add_face([5324.mm,1241.mm,500.mm], [5356.mm,1241.mm,500.mm], [5356.mm,1271.mm,500.mm], [5324.mm,1271.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Riser pipe clamp
  grp = ents.add_group
  grp.name = "Riser pipe clamp"
  face = grp.entities.add_face([5324.mm,1241.mm,900.mm], [5356.mm,1241.mm,900.mm], [5356.mm,1271.mm,900.mm], [5324.mm,1271.mm,900.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Riser pipe clamp
  grp = ents.add_group
  grp.name = "Riser pipe clamp"
  face = grp.entities.add_face([5324.mm,1241.mm,1300.mm], [5356.mm,1241.mm,1300.mm], [5356.mm,1271.mm,1300.mm], [5324.mm,1271.mm,1300.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Riser pipe clamp
  grp = ents.add_group
  grp.name = "Riser pipe clamp"
  face = grp.entities.add_face([5384.mm,1241.mm,500.mm], [5416.mm,1241.mm,500.mm], [5416.mm,1271.mm,500.mm], [5384.mm,1271.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Riser pipe clamp
  grp = ents.add_group
  grp.name = "Riser pipe clamp"
  face = grp.entities.add_face([5384.mm,1241.mm,900.mm], [5416.mm,1241.mm,900.mm], [5416.mm,1271.mm,900.mm], [5384.mm,1271.mm,900.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Riser pipe clamp
  grp = ents.add_group
  grp.name = "Riser pipe clamp"
  face = grp.entities.add_face([5384.mm,1241.mm,1300.mm], [5416.mm,1241.mm,1300.mm], [5416.mm,1271.mm,1300.mm], [5384.mm,1271.mm,1300.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Riser pipe clamp
  grp = ents.add_group
  grp.name = "Riser pipe clamp"
  face = grp.entities.add_face([5384.mm,1241.mm,1700.mm], [5416.mm,1241.mm,1700.mm], [5416.mm,1271.mm,1700.mm], [5384.mm,1271.mm,1700.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
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
  face.pushpull(980.mm)
  mat = model.materials["IBC Brown (developer) bottle"] || model.materials.add("IBC Brown (developer) bottle")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 0.55
  grp.material = mat

  # IBC Blue #1 pallet
  grp = ents.add_group
  grp.name = "IBC Blue #1 pallet"
  face = grp.entities.add_face([4674.mm,30.mm,1168.mm], [5893.mm,30.mm,1168.mm], [5893.mm,1046.mm,1168.mm], [4674.mm,1046.mm,1168.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(168.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Blue #1 bottle
  grp = ents.add_group
  grp.name = "IBC Blue #1 bottle"
  face = grp.entities.add_face([4704.mm,60.mm,1336.mm], [5863.mm,60.mm,1336.mm], [5863.mm,1016.mm,1336.mm], [4704.mm,1016.mm,1336.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(980.mm)
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
  face.pushpull(980.mm)
  mat = model.materials["IBC Waste bottle"] || model.materials.add("IBC Waste bottle")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 0.55
  grp.material = mat

  # IBC Blue #2 pallet
  grp = ents.add_group
  grp.name = "IBC Blue #2 pallet"
  face = grp.entities.add_face([4674.mm,1316.mm,1168.mm], [5893.mm,1316.mm,1168.mm], [5893.mm,2332.mm,1168.mm], [4674.mm,2332.mm,1168.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(168.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Blue #2 bottle
  grp = ents.add_group
  grp.name = "IBC Blue #2 bottle"
  face = grp.entities.add_face([4704.mm,1346.mm,1336.mm], [5863.mm,1346.mm,1336.mm], [5863.mm,2302.mm,1336.mm], [4704.mm,2302.mm,1336.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(980.mm)
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
  # Front Portal Upright
  grp = ents.add_group
  grp.name = "Front Portal Upright"
  face = grp.entities.add_face([4734.mm,1046.mm,0.mm], [4784.mm,1046.mm,0.mm], [4784.mm,1096.mm,0.mm], [4734.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Portal Upright
  grp = ents.add_group
  grp.name = "Front Portal Upright"
  face = grp.entities.add_face([4734.mm,1266.mm,0.mm], [4784.mm,1266.mm,0.mm], [4784.mm,1316.mm,0.mm], [4734.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Portal Top Tie
  grp = ents.add_group
  grp.name = "Front Portal Top Tie"
  face = grp.entities.add_face([4734.mm,1046.mm,2246.mm], [4784.mm,1046.mm,2246.mm], [4784.mm,1316.mm,2246.mm], [4734.mm,1316.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Portal Floor Beam
  grp = ents.add_group
  grp.name = "Front Portal Floor Beam"
  face = grp.entities.add_face([4734.mm,1046.mm,0.mm], [4784.mm,1046.mm,0.mm], [4784.mm,1316.mm,0.mm], [4734.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Panel Mount Rail
  grp = ents.add_group
  grp.name = "Panel Mount Rail"
  face = grp.entities.add_face([4734.mm,1046.mm,2260.mm], [4892.mm,1046.mm,2260.mm], [4892.mm,1316.mm,2260.mm], [4734.mm,1316.mm,2260.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Flange Plate
  grp = ents.add_group
  grp.name = "Foot Flange Plate"
  face = grp.entities.add_face([4684.mm,996.mm,0.mm], [4834.mm,996.mm,0.mm], [4834.mm,1146.mm,0.mm], [4684.mm,1146.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4709.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4709.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4809.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4809.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Flange Plate
  grp = ents.add_group
  grp.name = "Foot Flange Plate"
  face = grp.entities.add_face([4684.mm,1216.mm,0.mm], [4834.mm,1216.mm,0.mm], [4834.mm,1366.mm,0.mm], [4684.mm,1366.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4709.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4709.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4809.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4809.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,0.mm,560.mm], [4674.mm,0.mm,560.mm], [4674.mm,1096.mm,560.mm], [4654.mm,1096.mm,560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,0.mm,1760.mm], [4674.mm,0.mm,1760.mm], [4674.mm,1096.mm,1760.mm], [4654.mm,1096.mm,1760.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,1266.mm,560.mm], [4674.mm,1266.mm,560.mm], [4674.mm,2362.mm,560.mm], [4654.mm,2362.mm,560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,1266.mm,1760.mm], [4674.mm,1266.mm,1760.mm], [4674.mm,2362.mm,1760.mm], [4654.mm,2362.mm,1760.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Bar Stub
  grp = ents.add_group
  grp.name = "Front Bar Stub"
  face = grp.entities.add_face([4654.mm,1046.mm,560.mm], [4784.mm,1046.mm,560.mm], [4784.mm,1096.mm,560.mm], [4654.mm,1096.mm,560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Bar Stub
  grp = ents.add_group
  grp.name = "Front Bar Stub"
  face = grp.entities.add_face([4654.mm,1046.mm,1760.mm], [4784.mm,1046.mm,1760.mm], [4784.mm,1096.mm,1760.mm], [4654.mm,1096.mm,1760.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Bar Stub
  grp = ents.add_group
  grp.name = "Front Bar Stub"
  face = grp.entities.add_face([4654.mm,1266.mm,560.mm], [4784.mm,1266.mm,560.mm], [4784.mm,1316.mm,560.mm], [4654.mm,1316.mm,560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Bar Stub
  grp = ents.add_group
  grp.name = "Front Bar Stub"
  face = grp.entities.add_face([4654.mm,1266.mm,1760.mm], [4784.mm,1266.mm,1760.mm], [4784.mm,1316.mm,1760.mm], [4654.mm,1316.mm,1760.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4646.mm,0.mm,530.mm], [4712.mm,0.mm,530.mm], [4712.mm,4.mm,530.mm], [4646.mm,4.mm,530.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,0.mm,556.mm], [4708.mm,0.mm,556.mm], [4708.mm,70.mm,556.mm], [4650.mm,70.mm,556.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.mm,-48.mm,517.5.mm], [4729.mm,-48.mm,517.5.mm], [4729.mm,-40.mm,517.5.mm], [4629.mm,-40.mm,517.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4646.mm,0.mm,1730.mm], [4712.mm,0.mm,1730.mm], [4712.mm,4.mm,1730.mm], [4646.mm,4.mm,1730.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,0.mm,1756.mm], [4708.mm,0.mm,1756.mm], [4708.mm,70.mm,1756.mm], [4650.mm,70.mm,1756.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.mm,-48.mm,1717.5.mm], [4729.mm,-48.mm,1717.5.mm], [4729.mm,-40.mm,1717.5.mm], [4629.mm,-40.mm,1717.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4646.mm,2358.mm,530.mm], [4712.mm,2358.mm,530.mm], [4712.mm,2362.mm,530.mm], [4646.mm,2362.mm,530.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,2292.mm,556.mm], [4708.mm,2292.mm,556.mm], [4708.mm,2362.mm,556.mm], [4650.mm,2362.mm,556.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.mm,2402.mm,517.5.mm], [4729.mm,2402.mm,517.5.mm], [4729.mm,2410.mm,517.5.mm], [4629.mm,2410.mm,517.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4646.mm,2358.mm,1730.mm], [4712.mm,2358.mm,1730.mm], [4712.mm,2362.mm,1730.mm], [4646.mm,2362.mm,1730.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,2292.mm,1756.mm], [4708.mm,2292.mm,1756.mm], [4708.mm,2362.mm,1756.mm], [4650.mm,2362.mm,1756.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.mm,2402.mm,1717.5.mm], [4729.mm,2402.mm,1717.5.mm], [4729.mm,2410.mm,1717.5.mm], [4629.mm,2410.mm,1717.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
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
  face = ge.add_face([[-55.28.mm,1470.25.mm,130.mm], [-66.02.mm,1482.59.mm,130.mm], [-77.21.mm,1494.54.mm,130.mm], [-88.82.mm,1506.06.mm,130.mm], [-100.84.mm,1517.16.mm,130.mm], [-113.26.mm,1527.81.mm,130.mm], [-126.06.mm,1538.01.mm,130.mm], [-139.22.mm,1547.73.mm,130.mm], [-152.72.mm,1556.97.mm,130.mm], [-166.55.mm,1565.71.mm,130.mm], [-180.69.mm,1573.94.mm,130.mm], [-195.12.mm,1581.66.mm,130.mm], [-209.82.mm,1588.84.mm,130.mm], [-224.77.mm,1595.48.mm,130.mm], [-239.96.mm,1601.58.mm,130.mm], [-255.35.mm,1607.12.mm,130.mm], [-270.94.mm,1612.1.mm,130.mm], [-286.7.mm,1616.5.mm,130.mm], [-302.6.mm,1620.33.mm,130.mm], [-318.64.mm,1623.58.mm,130.mm], [-334.78.mm,1626.25.mm,130.mm], [-351.01.mm,1628.33.mm,130.mm], [-367.3.mm,1629.81.mm,130.mm], [-383.64.mm,1630.7.mm,130.mm], [-400.mm,1631.mm,130.mm], [-416.36.mm,1630.7.mm,130.mm], [-432.7.mm,1629.81.mm,130.mm], [-448.99.mm,1628.33.mm,130.mm], [-465.22.mm,1626.25.mm,130.mm], [-481.36.mm,1623.58.mm,130.mm], [-497.4.mm,1620.33.mm,130.mm], [-513.3.mm,1616.5.mm,130.mm], [-529.06.mm,1612.1.mm,130.mm], [-544.65.mm,1607.12.mm,130.mm], [-560.04.mm,1601.58.mm,130.mm], [-575.23.mm,1595.48.mm,130.mm], [-590.18.mm,1588.84.mm,130.mm], [-604.88.mm,1581.66.mm,130.mm], [-619.31.mm,1573.94.mm,130.mm], [-633.45.mm,1565.71.mm,130.mm], [-647.28.mm,1556.97.mm,130.mm], [-660.78.mm,1547.73.mm,130.mm], [-673.94.mm,1538.01.mm,130.mm], [-686.74.mm,1527.81.mm,130.mm], [-699.16.mm,1517.16.mm,130.mm], [-711.18.mm,1506.06.mm,130.mm], [-722.79.mm,1494.54.mm,130.mm], [-733.98.mm,1482.59.mm,130.mm], [-744.72.mm,1470.25.mm,130.mm], [-740.89.mm,1467.04.mm,130.mm], [-730.27.mm,1479.24.mm,130.mm], [-719.21.mm,1491.05.mm,130.mm], [-707.72.mm,1502.45.mm,130.mm], [-695.83.mm,1513.43.mm,130.mm], [-683.55.mm,1523.96.mm,130.mm], [-670.9.mm,1534.04.mm,130.mm], [-657.89.mm,1543.66.mm,130.mm], [-644.53.mm,1552.79.mm,130.mm], [-630.85.mm,1561.44.mm,130.mm], [-616.87.mm,1569.58.mm,130.mm], [-602.6.mm,1577.2.mm,130.mm], [-588.07.mm,1584.31.mm,130.mm], [-573.28.mm,1590.88.mm,130.mm], [-558.26.mm,1596.91.mm,130.mm], [-543.04.mm,1602.38.mm,130.mm], [-527.63.mm,1607.31.mm,130.mm], [-512.05.mm,1611.66.mm,130.mm], [-496.32.mm,1615.45.mm,130.mm], [-480.46.mm,1618.67.mm,130.mm], [-464.49.mm,1621.3.mm,130.mm], [-448.45.mm,1623.36.mm,130.mm], [-432.33.mm,1624.82.mm,130.mm], [-416.18.mm,1625.71.mm,130.mm], [-400.mm,1626.mm,130.mm], [-383.82.mm,1625.71.mm,130.mm], [-367.67.mm,1624.82.mm,130.mm], [-351.55.mm,1623.36.mm,130.mm], [-335.51.mm,1621.3.mm,130.mm], [-319.54.mm,1618.67.mm,130.mm], [-303.68.mm,1615.45.mm,130.mm], [-287.95.mm,1611.66.mm,130.mm], [-272.37.mm,1607.31.mm,130.mm], [-256.96.mm,1602.38.mm,130.mm], [-241.74.mm,1596.91.mm,130.mm], [-226.72.mm,1590.88.mm,130.mm], [-211.93.mm,1584.31.mm,130.mm], [-197.4.mm,1577.2.mm,130.mm], [-183.13.mm,1569.58.mm,130.mm], [-169.15.mm,1561.44.mm,130.mm], [-155.47.mm,1552.79.mm,130.mm], [-142.11.mm,1543.66.mm,130.mm], [-129.1.mm,1534.04.mm,130.mm], [-116.45.mm,1523.96.mm,130.mm], [-104.17.mm,1513.43.mm,130.mm], [-92.28.mm,1502.45.mm,130.mm], [-80.79.mm,1491.05.mm,130.mm], [-69.73.mm,1479.24.mm,130.mm], [-59.11.mm,1467.04.mm,130.mm]])
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
  face = ge.add_face([[-744.72.mm,891.75.mm,130.mm], [-733.98.mm,879.41.mm,130.mm], [-722.79.mm,867.46.mm,130.mm], [-711.18.mm,855.94.mm,130.mm], [-699.16.mm,844.84.mm,130.mm], [-686.74.mm,834.19.mm,130.mm], [-673.94.mm,823.99.mm,130.mm], [-660.78.mm,814.27.mm,130.mm], [-647.28.mm,805.03.mm,130.mm], [-633.45.mm,796.29.mm,130.mm], [-619.31.mm,788.06.mm,130.mm], [-604.88.mm,780.34.mm,130.mm], [-590.18.mm,773.16.mm,130.mm], [-575.23.mm,766.52.mm,130.mm], [-560.04.mm,760.42.mm,130.mm], [-544.65.mm,754.88.mm,130.mm], [-529.06.mm,749.9.mm,130.mm], [-513.3.mm,745.5.mm,130.mm], [-497.4.mm,741.67.mm,130.mm], [-481.36.mm,738.42.mm,130.mm], [-465.22.mm,735.75.mm,130.mm], [-448.99.mm,733.67.mm,130.mm], [-432.7.mm,732.19.mm,130.mm], [-416.36.mm,731.3.mm,130.mm], [-400.mm,731.mm,130.mm], [-383.64.mm,731.3.mm,130.mm], [-367.3.mm,732.19.mm,130.mm], [-351.01.mm,733.67.mm,130.mm], [-334.78.mm,735.75.mm,130.mm], [-318.64.mm,738.42.mm,130.mm], [-302.6.mm,741.67.mm,130.mm], [-286.7.mm,745.5.mm,130.mm], [-270.94.mm,749.9.mm,130.mm], [-255.35.mm,754.88.mm,130.mm], [-239.96.mm,760.42.mm,130.mm], [-224.77.mm,766.52.mm,130.mm], [-209.82.mm,773.16.mm,130.mm], [-195.12.mm,780.34.mm,130.mm], [-180.69.mm,788.06.mm,130.mm], [-166.55.mm,796.29.mm,130.mm], [-152.72.mm,805.03.mm,130.mm], [-139.22.mm,814.27.mm,130.mm], [-126.06.mm,823.99.mm,130.mm], [-113.26.mm,834.19.mm,130.mm], [-100.84.mm,844.84.mm,130.mm], [-88.82.mm,855.94.mm,130.mm], [-77.21.mm,867.46.mm,130.mm], [-66.02.mm,879.41.mm,130.mm], [-55.28.mm,891.75.mm,130.mm], [-59.11.mm,894.96.mm,130.mm], [-69.73.mm,882.76.mm,130.mm], [-80.79.mm,870.95.mm,130.mm], [-92.28.mm,859.55.mm,130.mm], [-104.17.mm,848.57.mm,130.mm], [-116.45.mm,838.04.mm,130.mm], [-129.1.mm,827.96.mm,130.mm], [-142.11.mm,818.34.mm,130.mm], [-155.47.mm,809.21.mm,130.mm], [-169.15.mm,800.56.mm,130.mm], [-183.13.mm,792.42.mm,130.mm], [-197.4.mm,784.8.mm,130.mm], [-211.93.mm,777.69.mm,130.mm], [-226.72.mm,771.12.mm,130.mm], [-241.74.mm,765.09.mm,130.mm], [-256.96.mm,759.62.mm,130.mm], [-272.37.mm,754.69.mm,130.mm], [-287.95.mm,750.34.mm,130.mm], [-303.68.mm,746.55.mm,130.mm], [-319.54.mm,743.33.mm,130.mm], [-335.51.mm,740.7.mm,130.mm], [-351.55.mm,738.64.mm,130.mm], [-367.67.mm,737.18.mm,130.mm], [-383.82.mm,736.29.mm,130.mm], [-400.mm,736.mm,130.mm], [-416.18.mm,736.29.mm,130.mm], [-432.33.mm,737.18.mm,130.mm], [-448.45.mm,738.64.mm,130.mm], [-464.49.mm,740.7.mm,130.mm], [-480.46.mm,743.33.mm,130.mm], [-496.32.mm,746.55.mm,130.mm], [-512.05.mm,750.34.mm,130.mm], [-527.63.mm,754.69.mm,130.mm], [-543.04.mm,759.62.mm,130.mm], [-558.26.mm,765.09.mm,130.mm], [-573.28.mm,771.12.mm,130.mm], [-588.07.mm,777.69.mm,130.mm], [-602.6.mm,784.8.mm,130.mm], [-616.87.mm,792.42.mm,130.mm], [-630.85.mm,800.56.mm,130.mm], [-644.53.mm,809.21.mm,130.mm], [-657.89.mm,818.34.mm,130.mm], [-670.9.mm,827.96.mm,130.mm], [-683.55.mm,838.04.mm,130.mm], [-695.83.mm,848.57.mm,130.mm], [-707.72.mm,859.55.mm,130.mm], [-719.21.mm,870.95.mm,130.mm], [-730.27.mm,882.76.mm,130.mm], [-740.89.mm,894.96.mm,130.mm]])
  face.reverse! if face.normal.z < 0
  face.pushpull(2120.mm)
  mat = model.materials["LT Housing arc (near Yd)"] || model.materials.add("LT Housing arc (near Yd)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.42
  grp.material = mat

  # LT Upper bearing (SKF 6215)
  grp = ents.add_group
  grp.name = "LT Upper bearing (SKF 6215)"
  ge = grp.entities
  circle = ge.add_circle([-400.mm,1181.mm,2250.mm], [0,0,1], 65.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(45.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum C-shell
  grp = ents.add_group
  grp.name = "LT Drum C-shell"
  ge = grp.entities
  face = ge.add_face([[-730.93.mm,903.32.mm,130.mm], [-701.mm,871.12.mm,130.mm], [-667.94.mm,842.13.mm,130.mm], [-632.11.mm,816.65.mm,130.mm], [-593.88.mm,794.95.mm,130.mm], [-553.64.mm,777.24.mm,130.mm], [-511.81.mm,763.72.mm,130.mm], [-468.82.mm,754.52.mm,130.mm], [-425.12.mm,749.73.mm,130.mm], [-381.16.mm,749.41.mm,130.mm], [-337.39.mm,753.56.mm,130.mm], [-294.27.mm,762.14.mm,130.mm], [-252.25.mm,775.05.mm,130.mm], [-211.75.mm,792.17.mm,130.mm], [-173.21.mm,813.32.mm,130.mm], [-137.02.mm,838.27.mm,130.mm], [-103.54.mm,866.77.mm,130.mm], [-73.14.mm,898.53.mm,130.mm], [-46.13.mm,933.21.mm,130.mm], [-22.78.mm,970.46.mm,130.mm], [-3.33.mm,1009.89.mm,130.mm], [12.01.mm,1051.1.mm,130.mm], [23.08.mm,1093.64.mm,130.mm], [29.76.mm,1137.09.mm,130.mm], [32.mm,1181.mm,130.mm], [29.76.mm,1224.91.mm,130.mm], [23.08.mm,1268.36.mm,130.mm], [12.01.mm,1310.9.mm,130.mm], [-3.33.mm,1352.11.mm,130.mm], [-22.78.mm,1391.54.mm,130.mm], [-46.13.mm,1428.79.mm,130.mm], [-73.14.mm,1463.47.mm,130.mm], [-103.54.mm,1495.23.mm,130.mm], [-137.02.mm,1523.73.mm,130.mm], [-173.21.mm,1548.68.mm,130.mm], [-211.75.mm,1569.83.mm,130.mm], [-252.25.mm,1586.95.mm,130.mm], [-294.27.mm,1599.86.mm,130.mm], [-337.39.mm,1608.44.mm,130.mm], [-381.16.mm,1612.59.mm,130.mm], [-425.12.mm,1612.27.mm,130.mm], [-468.82.mm,1607.48.mm,130.mm], [-511.81.mm,1598.28.mm,130.mm], [-553.64.mm,1584.76.mm,130.mm], [-593.88.mm,1567.05.mm,130.mm], [-632.11.mm,1545.35.mm,130.mm], [-667.94.mm,1519.87.mm,130.mm], [-701.mm,1490.88.mm,130.mm], [-730.93.mm,1458.68.mm,130.mm], [-727.87.mm,1456.11.mm,130.mm], [-698.21.mm,1488.01.mm,130.mm], [-665.46.mm,1516.73.mm,130.mm], [-629.96.mm,1541.97.mm,130.mm], [-592.09.mm,1563.47.mm,130.mm], [-552.22.mm,1581.02.mm,130.mm], [-510.77.mm,1594.42.mm,130.mm], [-468.18.mm,1603.53.mm,130.mm], [-424.89.mm,1608.28.mm,130.mm], [-381.33.mm,1608.59.mm,130.mm], [-337.97.mm,1604.48.mm,130.mm], [-295.25.mm,1595.98.mm,130.mm], [-253.62.mm,1583.19.mm,130.mm], [-213.5.mm,1566.23.mm,130.mm], [-175.31.mm,1545.28.mm,130.mm], [-139.45.mm,1520.56.mm,130.mm], [-106.29.mm,1492.32.mm,130.mm], [-76.17.mm,1460.85.mm,130.mm], [-49.4.mm,1426.49.mm,130.mm], [-26.27.mm,1389.59.mm,130.mm], [-7.mm,1350.52.mm,130.mm], [8.19.mm,1309.7.mm,130.mm], [19.16.mm,1267.55.mm,130.mm], [25.78.mm,1224.5.mm,130.mm], [28.mm,1181.mm,130.mm], [25.78.mm,1137.5.mm,130.mm], [19.16.mm,1094.45.mm,130.mm], [8.19.mm,1052.3.mm,130.mm], [-7.mm,1011.48.mm,130.mm], [-26.27.mm,972.41.mm,130.mm], [-49.4.mm,935.51.mm,130.mm], [-76.17.mm,901.15.mm,130.mm], [-106.29.mm,869.68.mm,130.mm], [-139.45.mm,841.44.mm,130.mm], [-175.31.mm,816.72.mm,130.mm], [-213.5.mm,795.77.mm,130.mm], [-253.62.mm,778.81.mm,130.mm], [-295.25.mm,766.02.mm,130.mm], [-337.97.mm,757.52.mm,130.mm], [-381.33.mm,753.41.mm,130.mm], [-424.89.mm,753.72.mm,130.mm], [-468.18.mm,758.47.mm,130.mm], [-510.77.mm,767.58.mm,130.mm], [-552.22.mm,780.98.mm,130.mm], [-592.09.mm,798.53.mm,130.mm], [-629.96.mm,820.03.mm,130.mm], [-665.46.mm,845.27.mm,130.mm], [-698.21.mm,873.99.mm,130.mm], [-727.87.mm,905.89.mm,130.mm]])
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
  circle = ge.add_circle([-400.mm,1181.mm,2245.mm], [0,0,1], 432.mm, 24)
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
  circle = ge.add_circle([-400.mm,1181.mm,130.mm], [0,0,1], 432.mm, 24)
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
  circle = ge.add_circle([-400.mm,1181.mm,2250.mm], [0,0,1], 37.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(65.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Grab rail
  grp = ents.add_group
  grp.name = "LT Grab rail"
  ge = grp.entities
  circle = ge.add_circle([-43.mm,1181.mm,700.mm], [0,0,1], 15.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(400.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Grab rail standoff
  grp = ents.add_group
  grp.name = "LT Grab rail standoff"
  face = grp.entities.add_face([-43.mm,1175.mm,720.mm], [28.mm,1175.mm,720.mm], [28.mm,1187.mm,720.mm], [-43.mm,1187.mm,720.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Grab rail standoff
  grp = ents.add_group
  grp.name = "LT Grab rail standoff"
  face = grp.entities.add_face([-43.mm,1175.mm,1080.mm], [28.mm,1175.mm,1080.mm], [28.mm,1187.mm,1080.mm], [-43.mm,1187.mm,1080.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum opening brush seal
  grp = ents.add_group
  grp.name = "LT Drum opening brush seal"
  ge = grp.entities
  circle = ge.add_circle([-735.9104883076718.mm,1462.8623668475475.mm,130.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([-735.9104883076719.mm,899.1376331524525.mm,130.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2120.mm)
  mat = model.materials["LT Drum opening brush seal"] || model.materials.add("LT Drum opening brush seal")
  mat.color = Sketchup::Color.new(126, 126, 118)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Light-Trap Drum"
  inst.layer = model.layers["Light Trap"]

  # ═══ Light-Trap Bay ═══
  defn = model.definitions.add("Light-Trap Bay")
  ents = defn.entities
  # Bay wall near (Yd)
  grp = ents.add_group
  grp.name = "Bay wall near (Yd)"
  face = grp.entities.add_face([-890.mm,653.mm,130.mm], [0.mm,653.mm,130.mm], [0.mm,659.mm,130.mm], [-890.mm,659.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2170.mm)
  mat = model.materials["Bay wall near (Yd)"] || model.materials.add("Bay wall near (Yd)")
  mat.color = Sketchup::Color.new(110, 140, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Bay wall far (Yd)
  grp = ents.add_group
  grp.name = "Bay wall far (Yd)"
  face = grp.entities.add_face([-890.mm,1703.mm,130.mm], [0.mm,1703.mm,130.mm], [0.mm,1709.mm,130.mm], [-890.mm,1709.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2170.mm)
  mat = model.materials["Bay wall near (Yd)"] || model.materials.add("Bay wall near (Yd)")
  mat.color = Sketchup::Color.new(110, 140, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Bay wall top
  grp = ents.add_group
  grp.name = "Bay wall top"
  face = grp.entities.add_face([-890.mm,653.mm,2294.mm], [0.mm,653.mm,2294.mm], [0.mm,1709.mm,2294.mm], [-890.mm,1709.mm,2294.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Bay wall near (Yd)"] || model.materials.add("Bay wall near (Yd)")
  mat.color = Sketchup::Color.new(110, 140, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Bay wall bottom
  grp = ents.add_group
  grp.name = "Bay wall bottom"
  face = grp.entities.add_face([-890.mm,653.mm,130.mm], [0.mm,653.mm,130.mm], [0.mm,1709.mm,130.mm], [-890.mm,1709.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Bay wall near (Yd)"] || model.materials.add("Bay wall near (Yd)")
  mat.color = Sketchup::Color.new(110, 140, 160)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Light-Trap Bay"
  inst.layer = model.layers["Light Trap"]

  # ═══ Electrical ═══
  defn = model.definitions.add("Electrical")
  ents = defn.entities
  # Electrical Panel (EP enclosure, IP65)
  grp = ents.add_group
  grp.name = "Electrical Panel (EP enclosure, IP65)"
  face = grp.entities.add_face([1898.mm,0.mm,1488.mm], [2222.mm,0.mm,1488.mm], [2222.mm,171.mm,1488.mm], [1898.mm,171.mm,1488.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(624.mm)
  mat = model.materials["Electrical Panel (EP enclosure, IP65)"] || model.materials.add("Electrical Panel (EP enclosure, IP65)")
  mat.color = Sketchup::Color.new(245, 197, 24)
  mat.alpha = 0.14
  grp.material = mat

  # MPPT Controller (Victron 100/50)
  grp = ents.add_group
  grp.name = "MPPT Controller (Victron 100/50)"
  face = grp.entities.add_face([1925.mm,25.mm,1970.mm], [2110.mm,25.mm,1970.mm], [2110.mm,95.mm,1970.mm], [1925.mm,95.mm,1970.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["MPPT Controller (Victron 100/50)"] || model.materials.add("MPPT Controller (Victron 100/50)")
  mat.color = Sketchup::Color.new(58, 91, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse Block base (Blue Sea 5026)
  grp = ents.add_group
  grp.name = "Fuse Block base (Blue Sea 5026)"
  face = grp.entities.add_face([1925.mm,25.mm,1770.mm], [2075.mm,25.mm,1770.mm], [2075.mm,70.mm,1770.mm], [1925.mm,70.mm,1770.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Fuse Block base (Blue Sea 5026)"] || model.materials.add("Fuse Block base (Blue Sea 5026)")
  mat.color = Sketchup::Color.new(43, 43, 48)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse A (5A — exhaust fan)
  grp = ents.add_group
  grp.name = "Fuse A (5A — exhaust fan)"
  face = grp.entities.add_face([1929.2142857142858.mm,43.mm,1798.mm], [1942.2142857142858.mm,43.mm,1798.mm], [1942.2142857142858.mm,52.mm,1798.mm], [1929.2142857142858.mm,52.mm,1798.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse B (5A — intake fan)
  grp = ents.add_group
  grp.name = "Fuse B (5A — intake fan)"
  face = grp.entities.add_face([1950.642857142857.mm,43.mm,1798.mm], [1963.642857142857.mm,43.mm,1798.mm], [1963.642857142857.mm,52.mm,1798.mm], [1950.642857142857.mm,52.mm,1798.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse C (15A — water pumps)
  grp = ents.add_group
  grp.name = "Fuse C (15A — water pumps)"
  face = grp.entities.add_face([1972.0714285714287.mm,43.mm,1798.mm], [1985.0714285714287.mm,43.mm,1798.mm], [1985.0714285714287.mm,52.mm,1798.mm], [1972.0714285714287.mm,52.mm,1798.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse D (5A — safelight)
  grp = ents.add_group
  grp.name = "Fuse D (5A — safelight)"
  face = grp.entities.add_face([1993.5.mm,43.mm,1798.mm], [2006.5.mm,43.mm,1798.mm], [2006.5.mm,52.mm,1798.mm], [1993.5.mm,52.mm,1798.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse D (5A — safelight)"] || model.materials.add("Fuse D (5A — safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse E (40A — cooler / inverter)
  grp = ents.add_group
  grp.name = "Fuse E (40A — cooler / inverter)"
  face = grp.entities.add_face([2014.9285714285713.mm,43.mm,1798.mm], [2027.9285714285713.mm,43.mm,1798.mm], [2027.9285714285713.mm,52.mm,1798.mm], [2014.9285714285713.mm,52.mm,1798.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse E (40A — cooler / inverter)"] || model.materials.add("Fuse E (40A — cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse F (20A — actuators (spare))
  grp = ents.add_group
  grp.name = "Fuse F (20A — actuators (spare))"
  face = grp.entities.add_face([2036.357142857143.mm,43.mm,1798.mm], [2049.357142857143.mm,43.mm,1798.mm], [2049.357142857143.mm,52.mm,1798.mm], [2036.357142857143.mm,52.mm,1798.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse F (20A — actuators (spare))"] || model.materials.add("Fuse F (20A — actuators (spare))")
  mat.color = Sketchup::Color.new(127, 140, 141)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse G (10A — white LED)
  grp = ents.add_group
  grp.name = "Fuse G (10A — white LED)"
  face = grp.entities.add_face([2057.785714285714.mm,43.mm,1798.mm], [2070.785714285714.mm,43.mm,1798.mm], [2070.785714285714.mm,52.mm,1798.mm], [2057.785714285714.mm,52.mm,1798.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse G (10A — white LED)"] || model.materials.add("Fuse G (10A — white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Busbar (+)
  grp = ents.add_group
  grp.name = "Busbar (+)"
  face = grp.entities.add_face([1925.mm,30.mm,1705.mm], [2045.mm,30.mm,1705.mm], [2045.mm,50.mm,1705.mm], [1925.mm,50.mm,1705.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Busbar (-)
  grp = ents.add_group
  grp.name = "Busbar (-)"
  face = grp.entities.add_face([1925.mm,30.mm,1675.mm], [2045.mm,30.mm,1675.mm], [2045.mm,50.mm,1675.mm], [1925.mm,50.mm,1675.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Busbar (-)"] || model.materials.add("Busbar (-)")
  mat.color = Sketchup::Color.new(44, 44, 44)
  mat.alpha = 1.0
  grp.material = mat

  # Main Disconnect (Blue Sea m-Series)
  grp = ents.add_group
  grp.name = "Main Disconnect (Blue Sea m-Series)"
  ge = grp.entities
  circle = ge.add_circle([2150.mm,165.mm,1620.mm], [0,1,0], 35.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Main Disconnect (Blue Sea m-Series)"] || model.materials.add("Main Disconnect (Blue Sea m-Series)")
  mat.color = Sketchup::Color.new(212, 58, 47)
  mat.alpha = 1.0
  grp.material = mat

  # Main feed (disconnect -> busbar +)
  grp = ents.add_group
  grp.name = "Main feed (disconnect -> busbar +)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -63.mm, 0.mm)
  circle = ge.add_circle([2150.mm,130.mm,1655.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect -> busbar +)"] || model.materials.add("Main feed (disconnect -> busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Main feed (disconnect -> busbar +) elbow
  grp = ents.add_group
  grp.name = "Main feed (disconnect -> busbar +) elbow"
  ge = grp.entities
  arc = ge.add_arc([2150.mm,67.mm,1677.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 22.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2150.mm,67.mm,1655.mm], [0.000000,-1.000000,0.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Main feed (disconnect -> busbar +)"] || model.materials.add("Main feed (disconnect -> busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Main feed (disconnect -> busbar +)
  grp = ents.add_group
  grp.name = "Main feed (disconnect -> busbar +)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 14.279999999999973.mm)
  circle = ge.add_circle([2150.mm,45.mm,1677.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect -> busbar +)"] || model.materials.add("Main feed (disconnect -> busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Main feed (disconnect -> busbar +) elbow
  grp = ents.add_group
  grp.name = "Main feed (disconnect -> busbar +) elbow"
  ge = grp.entities
  arc = ge.add_arc([2136.28.mm,45.mm,1691.28.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 13.72.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2150.mm,45.mm,1691.28.mm], [0.000000,0.000000,1.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Main feed (disconnect -> busbar +)"] || model.materials.add("Main feed (disconnect -> busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Main feed (disconnect -> busbar +)
  grp = ents.add_group
  grp.name = "Main feed (disconnect -> busbar +)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-91.2800000000002.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2136.28.mm,45.mm,1705.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect -> busbar +)"] || model.materials.add("Main feed (disconnect -> busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery 1 (12V 100Ah LiFePO4)
  grp = ents.add_group
  grp.name = "Battery 1 (12V 100Ah LiFePO4)"
  face = grp.entities.add_face([1540.mm,0.mm,150.mm], [1870.mm,0.mm,150.mm], [1870.mm,172.mm,150.mm], [1540.mm,172.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(214.mm)
  mat = model.materials["Battery 1 (12V 100Ah LiFePO4)"] || model.materials.add("Battery 1 (12V 100Ah LiFePO4)")
  mat.color = Sketchup::Color.new(106, 90, 205)
  mat.alpha = 1.0
  grp.material = mat

  # Battery 2 (optional 2nd pack — plug-in, ghosted)
  grp = ents.add_group
  grp.name = "Battery 2 (optional 2nd pack — plug-in, ghosted)"
  face = grp.entities.add_face([1890.mm,0.mm,150.mm], [2220.mm,0.mm,150.mm], [2220.mm,172.mm,150.mm], [1890.mm,172.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(214.mm)
  mat = model.materials["Battery 2 (optional 2nd pack — plug-in, ghosted)"] || model.materials.add("Battery 2 (optional 2nd pack — plug-in, ghosted)")
  mat.color = Sketchup::Color.new(106, 90, 205)
  mat.alpha = 0.28
  grp.material = mat

  # Ext. Power Panel (exterior)
  grp = ents.add_group
  grp.name = "Ext. Power Panel (exterior)"
  face = grp.entities.add_face([1250.mm,-65.mm,1830.mm], [1590.mm,-65.mm,1830.mm], [1590.mm,-40.mm,1830.mm], [1250.mm,-40.mm,1830.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(240.mm)
  mat = model.materials["Ext. Power Panel (exterior)"] || model.materials.add("Ext. Power Panel (exterior)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.5
  grp.material = mat

  # Ext. Power Panel (interior face)
  grp = ents.add_group
  grp.name = "Ext. Power Panel (interior face)"
  face = grp.entities.add_face([1250.mm,0.mm,1830.mm], [1590.mm,0.mm,1830.mm], [1590.mm,20.mm,1830.mm], [1250.mm,20.mm,1830.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(240.mm)
  mat = model.materials["Ext. Power Panel (interior face)"] || model.materials.add("Ext. Power Panel (interior face)")
  mat.color = Sketchup::Color.new(245, 197, 24)
  mat.alpha = 1.0
  grp.material = mat

  # Battery Contactor (ML-RBS, in + feed)
  grp = ents.add_group
  grp.name = "Battery Contactor (ML-RBS, in + feed)"
  face = grp.entities.add_face([1560.mm,15.mm,364.mm], [1680.mm,15.mm,364.mm], [1680.mm,105.mm,364.mm], [1560.mm,105.mm,364.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Battery Contactor (ML-RBS, in + feed)"] || model.materials.add("Battery Contactor (ML-RBS, in + feed)")
  mat.color = Sketchup::Color.new(196, 43, 28)
  mat.alpha = 1.0
  grp.material = mat

  # MRBF Main Fuse (on + post)
  grp = ents.add_group
  grp.name = "MRBF Main Fuse (on + post)"
  face = grp.entities.add_face([1695.mm,20.mm,364.mm], [1735.mm,20.mm,364.mm], [1735.mm,60.mm,364.mm], [1695.mm,60.mm,364.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(38.mm)
  mat = model.materials["MRBF Main Fuse (on + post)"] || model.materials.add("MRBF Main Fuse (on + post)")
  mat.color = Sketchup::Color.new(34, 34, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF -> main disconnect)
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF -> main disconnect)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1161.mm)
  circle = ge.add_circle([1715.mm,45.mm,402.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect -> busbar +)"] || model.materials.add("Main feed (disconnect -> busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF -> main disconnect) elbow
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF -> main disconnect) elbow"
  ge = grp.entities
  arc = ge.add_arc([1737.mm,45.mm,1563.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 22.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1715.mm,45.mm,1563.mm], [0.000000,0.000000,1.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Main feed (disconnect -> busbar +)"] || model.materials.add("Main feed (disconnect -> busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF -> main disconnect)
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF -> main disconnect)"
  ge = grp.entities
  vec = Geom::Vector3d.new(391.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1737.mm,45.mm,1585.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect -> busbar +)"] || model.materials.add("Main feed (disconnect -> busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF -> main disconnect) elbow
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF -> main disconnect) elbow"
  ge = grp.entities
  arc = ge.add_arc([2128.mm,67.mm,1585.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 22.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2128.mm,45.mm,1585.mm], [1.000000,0.000000,0.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Main feed (disconnect -> busbar +)"] || model.materials.add("Main feed (disconnect -> busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF -> main disconnect)
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF -> main disconnect)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 63.mm, 0.mm)
  circle = ge.add_circle([2150.mm,67.mm,1585.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect -> busbar +)"] || model.materials.add("Main feed (disconnect -> busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery - cable (2/0 AWG -> busbar -)
  grp = ents.add_group
  grp.name = "Battery - cable (2/0 AWG -> busbar -)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1300.mm)
  circle = ge.add_circle([1760.mm,60.mm,364.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Battery - cable (2/0 AWG -> busbar -)"] || model.materials.add("Battery - cable (2/0 AWG -> busbar -)")
  mat.color = Sketchup::Color.new(32, 32, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Battery - cable (2/0 AWG -> busbar -) elbow
  grp = ents.add_group
  grp.name = "Battery - cable (2/0 AWG -> busbar -) elbow"
  ge = grp.entities
  arc = ge.add_arc([1782.mm,60.mm,1664.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 22.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1760.mm,60.mm,1664.mm], [0.000000,0.000000,1.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Battery - cable (2/0 AWG -> busbar -)"] || model.materials.add("Battery - cable (2/0 AWG -> busbar -)")
  mat.color = Sketchup::Color.new(32, 32, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Battery - cable (2/0 AWG -> busbar -)
  grp = ents.add_group
  grp.name = "Battery - cable (2/0 AWG -> busbar -)"
  ge = grp.entities
  vec = Geom::Vector3d.new(163.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1782.mm,60.mm,1686.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Battery - cable (2/0 AWG -> busbar -)"] || model.materials.add("Battery - cable (2/0 AWG -> busbar -)")
  mat.color = Sketchup::Color.new(32, 32, 32)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop collar (safety yellow)
  grp = ents.add_group
  grp.name = "E-stop collar (safety yellow)"
  ge = grp.entities
  circle = ge.add_circle([1420.mm,-77.mm,1950.mm], [0,1,0], 35.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(12.mm)
  mat = model.materials["E-stop collar (safety yellow)"] || model.materials.add("E-stop collar (safety yellow)")
  mat.color = Sketchup::Color.new(242, 194, 0)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop button (red mushroom)
  grp = ents.add_group
  grp.name = "E-stop button (red mushroom)"
  ge = grp.entities
  circle = ge.add_circle([1420.mm,-105.mm,1950.mm], [0,1,0], 26.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Battery Contactor (ML-RBS, in + feed)"] || model.materials.add("Battery Contactor (ML-RBS, in + feed)")
  mat.color = Sketchup::Color.new(196, 43, 28)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop control wire (2x 18 AWG)
  grp = ents.add_group
  grp.name = "E-stop control wire (2x 18 AWG)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-490.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1620.mm,60.mm,464.mm], vec, 5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["E-stop control wire (2x 18 AWG)"] || model.materials.add("E-stop control wire (2x 18 AWG)")
  mat.color = Sketchup::Color.new(106, 61, 168)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop control wire (2x 18 AWG) elbow
  grp = ents.add_group
  grp.name = "E-stop control wire (2x 18 AWG) elbow"
  ge = grp.entities
  arc = ge.add_arc([1130.mm,60.mm,474.mm], [0.000000,0.000000,-1.000000], [0.000000,1.000000,-0.000000], 10.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1130.mm,60.mm,464.mm], [-1.000000,0.000000,0.000000], 5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["E-stop control wire (2x 18 AWG)"] || model.materials.add("E-stop control wire (2x 18 AWG)")
  mat.color = Sketchup::Color.new(106, 61, 168)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop control wire (2x 18 AWG)
  grp = ents.add_group
  grp.name = "E-stop control wire (2x 18 AWG)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1466.mm)
  circle = ge.add_circle([1120.mm,60.mm,474.mm], vec, 5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["E-stop control wire (2x 18 AWG)"] || model.materials.add("E-stop control wire (2x 18 AWG)")
  mat.color = Sketchup::Color.new(106, 61, 168)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop control wire (2x 18 AWG) elbow
  grp = ents.add_group
  grp.name = "E-stop control wire (2x 18 AWG) elbow"
  ge = grp.entities
  arc = ge.add_arc([1130.mm,60.mm,1940.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 10.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1120.mm,60.mm,1940.mm], [0.000000,0.000000,1.000000], 5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["E-stop control wire (2x 18 AWG)"] || model.materials.add("E-stop control wire (2x 18 AWG)")
  mat.color = Sketchup::Color.new(106, 61, 168)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop control wire (2x 18 AWG)
  grp = ents.add_group
  grp.name = "E-stop control wire (2x 18 AWG)"
  ge = grp.entities
  vec = Geom::Vector3d.new(280.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1130.mm,60.mm,1950.mm], vec, 5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["E-stop control wire (2x 18 AWG)"] || model.materials.add("E-stop control wire (2x 18 AWG)")
  mat.color = Sketchup::Color.new(106, 61, 168)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop control wire (2x 18 AWG) elbow
  grp = ents.add_group
  grp.name = "E-stop control wire (2x 18 AWG) elbow"
  ge = grp.entities
  arc = ge.add_arc([1410.mm,50.mm,1950.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,-1.000000], 10.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1410.mm,60.mm,1950.mm], [1.000000,0.000000,0.000000], 5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["E-stop control wire (2x 18 AWG)"] || model.materials.add("E-stop control wire (2x 18 AWG)")
  mat.color = Sketchup::Color.new(106, 61, 168)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop control wire (2x 18 AWG)
  grp = ents.add_group
  grp.name = "E-stop control wire (2x 18 AWG)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -40.mm, 0.mm)
  circle = ge.add_circle([1420.mm,50.mm,1950.mm], vec, 5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["E-stop control wire (2x 18 AWG)"] || model.materials.add("E-stop control wire (2x 18 AWG)")
  mat.color = Sketchup::Color.new(106, 61, 168)
  mat.alpha = 1.0
  grp.material = mat

  # MC4 PV1 (+)
  grp = ents.add_group
  grp.name = "MC4 PV1 (+)"
  ge = grp.entities
  circle = ge.add_circle([1315.28.mm,-85.mm,1884.mm], [0,1,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # MC4 PV1 (-)
  grp = ents.add_group
  grp.name = "MC4 PV1 (-)"
  ge = grp.entities
  circle = ge.add_circle([1343.5.mm,-85.mm,1884.mm], [0,1,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["MC4 PV1 (-)"] || model.materials.add("MC4 PV1 (-)")
  mat.color = Sketchup::Color.new(154, 160, 166)
  mat.alpha = 1.0
  grp.material = mat

  # MC4 PV2 (+)
  grp = ents.add_group
  grp.name = "MC4 PV2 (+)"
  ge = grp.entities
  circle = ge.add_circle([1315.28.mm,-85.mm,1950.mm], [0,1,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # MC4 PV2 (-)
  grp = ents.add_group
  grp.name = "MC4 PV2 (-)"
  ge = grp.entities
  circle = ge.add_circle([1343.5.mm,-85.mm,1950.mm], [0,1,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["MC4 PV1 (-)"] || model.materials.add("MC4 PV1 (-)")
  mat.color = Sketchup::Color.new(154, 160, 166)
  mat.alpha = 1.0
  grp.material = mat

  # MC4 PV3 (+)
  grp = ents.add_group
  grp.name = "MC4 PV3 (+)"
  ge = grp.entities
  circle = ge.add_circle([1315.28.mm,-85.mm,2016.mm], [0,1,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # MC4 PV3 (-)
  grp = ents.add_group
  grp.name = "MC4 PV3 (-)"
  ge = grp.entities
  circle = ge.add_circle([1343.5.mm,-85.mm,2016.mm], [0,1,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["MC4 PV1 (-)"] || model.materials.add("MC4 PV1 (-)")
  mat.color = Sketchup::Color.new(154, 160, 166)
  mat.alpha = 1.0
  grp.material = mat

  # NEMA 5-15R inlet (panel)
  grp = ents.add_group
  grp.name = "NEMA 5-15R inlet (panel)"
  face = grp.entities.add_face([1472.28.mm,-95.mm,2018.72.mm], [1532.28.mm,-95.mm,2018.72.mm], [1532.28.mm,-65.mm,2018.72.mm], [1472.28.mm,-65.mm,2018.72.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(45.mm)
  mat = model.materials["NEMA 5-15R inlet (panel)"] || model.materials.add("NEMA 5-15R inlet (panel)")
  mat.color = Sketchup::Color.new(255, 240, 204)
  mat.alpha = 1.0
  grp.material = mat

  # GFCI AC outlet (Cct E cooler)
  grp = ents.add_group
  grp.name = "GFCI AC outlet (Cct E cooler)"
  ge = grp.entities
  circle = ge.add_circle([1510.78.mm,-85.mm,1908.mm], [0,1,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # PV feed (MC4 bulkheads -> MPPT)
  grp = ents.add_group
  grp.name = "PV feed (MC4 bulkheads -> MPPT)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 45.mm, 0.mm)
  circle = ge.add_circle([1328.2.mm,22.mm,1884.mm], vec, 9.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV feed (MC4 bulkheads -> MPPT) elbow
  grp = ents.add_group
  grp.name = "PV feed (MC4 bulkheads -> MPPT) elbow"
  ge = grp.entities
  arc = ge.add_arc([1346.2.mm,67.mm,1884.mm], [-1.000000,0.000000,0.000000], [0.000000,0.000000,-1.000000], 18.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1328.2.mm,67.mm,1884.mm], [0.000000,1.000000,0.000000], 9.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV feed (MC4 bulkheads -> MPPT)
  grp = ents.add_group
  grp.name = "PV feed (MC4 bulkheads -> MPPT)"
  ge = grp.entities
  vec = Geom::Vector3d.new(585.8.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1346.2.mm,85.mm,1884.mm], vec, 9.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV feed (MC4 bulkheads -> MPPT) elbow
  grp = ents.add_group
  grp.name = "PV feed (MC4 bulkheads -> MPPT) elbow"
  ge = grp.entities
  arc = ge.add_arc([1932.mm,85.mm,1902.mm], [0.000000,0.000000,-1.000000], [0.000000,-1.000000,0.000000], 18.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1932.mm,85.mm,1884.mm], [1.000000,0.000000,0.000000], 9.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV feed (MC4 bulkheads -> MPPT)
  grp = ents.add_group
  grp.name = "PV feed (MC4 bulkheads -> MPPT)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 66.mm)
  circle = ge.add_circle([1950.mm,85.mm,1902.mm], vec, 9.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Electrical"
  inst.layer = model.layers["Electrical"]

  # ═══ Solar Array ═══
  defn = model.definitions.add("Solar Array")
  ents = defn.entities
  # Solar Panel 1 (200W)
  grp = ents.add_group
  grp.name = "Solar Panel 1 (200W)"
  face = grp.entities.add_face([250.mm,-900.mm,120.mm], [930.mm,-900.mm,120.mm], [930.mm,-2181.7175976009694.mm,859.9999999999999.mm], [250.mm,-2181.7175976009694.mm,859.9999999999999.mm])
  face.pushpull(35.mm)
  mat = model.materials["Solar Panel 1 (200W)"] || model.materials.add("Solar Panel 1 (200W)")
  mat.color = Sketchup::Color.new(27, 58, 107)
  mat.alpha = 1.0
  grp.material = mat

  # Solar Panel 2 (200W)
  grp = ents.add_group
  grp.name = "Solar Panel 2 (200W)"
  face = grp.entities.add_face([960.mm,-900.mm,120.mm], [1640.mm,-900.mm,120.mm], [1640.mm,-2181.7175976009694.mm,859.9999999999999.mm], [960.mm,-2181.7175976009694.mm,859.9999999999999.mm])
  face.pushpull(35.mm)
  mat = model.materials["Solar Panel 1 (200W)"] || model.materials.add("Solar Panel 1 (200W)")
  mat.color = Sketchup::Color.new(27, 58, 107)
  mat.alpha = 1.0
  grp.material = mat

  # Solar Panel 3 (200W)
  grp = ents.add_group
  grp.name = "Solar Panel 3 (200W)"
  face = grp.entities.add_face([1670.mm,-900.mm,120.mm], [2350.mm,-900.mm,120.mm], [2350.mm,-2181.7175976009694.mm,859.9999999999999.mm], [1670.mm,-2181.7175976009694.mm,859.9999999999999.mm])
  face.pushpull(35.mm)
  mat = model.materials["Solar Panel 1 (200W)"] || model.materials.add("Solar Panel 1 (200W)")
  mat.color = Sketchup::Color.new(27, 58, 107)
  mat.alpha = 1.0
  grp.material = mat

  # Tilt Frame front rail
  grp = ents.add_group
  grp.name = "Tilt Frame front rail"
  face = grp.entities.add_face([250.mm,-920.mm,0.mm], [2350.mm,-920.mm,0.mm], [2350.mm,-880.mm,0.mm], [250.mm,-880.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Tilt Frame back rail
  grp = ents.add_group
  grp.name = "Tilt Frame back rail"
  face = grp.entities.add_face([250.mm,-2201.7175976009694.mm,0.mm], [2350.mm,-2201.7175976009694.mm,0.mm], [2350.mm,-2161.7175976009694.mm,0.mm], [250.mm,-2161.7175976009694.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Tilt Frame back leg
  grp = ents.add_group
  grp.name = "Tilt Frame back leg"
  face = grp.entities.add_face([250.mm,-2201.7175976009694.mm,0.mm], [290.mm,-2201.7175976009694.mm,0.mm], [290.mm,-2161.7175976009694.mm,0.mm], [250.mm,-2161.7175976009694.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(859.9999999999999.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Tilt Frame back leg
  grp = ents.add_group
  grp.name = "Tilt Frame back leg"
  face = grp.entities.add_face([2310.mm,-2201.7175976009694.mm,0.mm], [2350.mm,-2201.7175976009694.mm,0.mm], [2350.mm,-2161.7175976009694.mm,0.mm], [2310.mm,-2161.7175976009694.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(859.9999999999999.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.mm, -9.mm, 0.mm)
  circle = ge.add_circle([1282.mm,-920.mm,60.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(7.mm, -21.mm, 0.mm)
  circle = ge.add_circle([1285.mm,-929.mm,60.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 88.mm, 0.mm)
  circle = ge.add_circle([1292.mm,-950.mm,60.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.240646482510101.mm, 11.174603174603135.mm, -9.143875140511966.mm)
  circle = ge.add_circle([1292.mm,-862.mm,60.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.103793034090586.mm, 11.174603174603249.mm, -3.8554044985163287.mm)
  circle = ge.add_circle([1301.24064648251.mm,-850.8253968253969.mm,50.856124859488034.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.182943879120785.mm, 11.174603174603135.mm, 3.6628859069936794.mm)
  circle = ge.add_circle([1292.1368534484195.mm,-839.6507936507936.mm,47.000720360971705.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.951028205245848.mm, 11.174603174603135.mm, 9.062702001946683.mm)
  circle = ge.add_circle([1282.9539095692987.mm,-828.4761904761905.mm,50.663606267965385.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.5660123580282743.mm, 11.174603174603249.mm, 9.220994920133435.mm)
  circle = ge.add_circle([1279.0028813640529.mm,-817.3015873015873.mm,59.72630826991207.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.02060659798417.mm, 11.174603174603135.mm, 4.046214040203338.mm)
  circle = ge.add_circle([1282.5688937220812.mm,-806.1269841269841.mm,68.9473031900455.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.25802404655201.mm, 11.174603174603135.mm, -3.4687436065814126.mm)
  circle = ge.add_circle([1291.5895003200653.mm,-794.952380952381.mm,72.99351723024884.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.140951454441392.mm, 11.174603174603249.mm, -8.977511487416585.mm)
  circle = ge.add_circle([1300.8475243666173.mm,-783.7777777777778.mm,69.52477362366743.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.3710904324400417.mm, 11.174603174603135.mm, -9.294027154632523.mm)
  circle = ge.add_circle([1304.9884758210587.mm,-772.6031746031746.mm,60.54726213625084.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.933421446249213.mm, 11.174603174603249.mm, -4.235229948707868.mm)
  circle = ge.add_circle([1301.6173853886187.mm,-761.4285714285714.mm,51.25323498161832.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.32900025433878.mm, 11.174603174603135.mm, 3.2730636579942143.mm)
  circle = ge.add_circle([1292.6839639423695.mm,-750.2539682539682.mm,47.01800503291045.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.3290390746112735.mm, 11.174603174603135.mm, 8.888341360750331.mm)
  circle = ge.add_circle([1283.3549636880307.mm,-739.0793650793651.mm,50.291068690904666.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.174674147038104.mm, 11.174603174603135.mm, 9.36293946978536.mm)
  circle = ge.add_circle([1279.0259246134194.mm,-727.9047619047619.mm,59.179410051655.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.842276226910144.mm, 11.174603174603249.mm, 4.42236843577696.mm)
  circle = ge.add_circle([1282.2005987604575.mm,-716.7301587301588.mm,68.54234952144036.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.395841039666493.mm, 11.174603174603135.mm, -3.075932803565891.mm)
  circle = ge.add_circle([1291.0428749873677.mm,-705.5555555555555.mm,72.96471795721732.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.51520768900059.mm, 11.174603174603249.mm, -8.795231149886035.mm)
  circle = ge.add_circle([1300.4387160270342.mm,-694.3809523809524.mm,69.88878515365143.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.976850570564011.mm, 11.174603174603135.mm, -9.427701317673794.mm)
  circle = ge.add_circle([1304.9539237160348.mm,-683.2063492063492.mm,61.09355400376539.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.747211343437812.mm, 11.174603174603135.mm, -4.607546545393788.mm)
  circle = ge.add_circle([1301.9770731454707.mm,-672.031746031746.mm,51.6658526860916.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.458516772898975.mm, 11.174603174603135.mm, 2.87743842879766.mm)
  circle = ge.add_circle([1293.229861802033.mm,-660.8571428571429.mm,47.05830614069781.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.69937477152439.mm, 11.174603174603249.mm, 8.698222129348956.mm)
  circle = ge.add_circle([1283.771345029134.mm,-649.6825396825398.mm,49.93574456949547.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.7777073955937794.mm, 11.174603174603135.mm, 9.488283990227039.mm)
  circle = ge.add_circle([1279.0719702576096.mm,-638.5079365079365.mm,58.633966698844425.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.648268936837894.mm, 11.174603174603249.mm, 4.790682190550868.mm)
  circle = ge.add_circle([1281.8496776532033.mm,-627.3333333333334.mm,68.12225068907146.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.516999670712721.mm, 11.174603174603135.mm, -2.6776685236212074.mm)
  circle = ge.add_circle([1290.4979465900412.mm,-616.1587301587301.mm,72.91293287962233.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.88145868334982.mm, 11.174603174603135.mm, -8.597357301955228.mm)
  circle = ge.add_circle([1300.014946260754.mm,-604.984126984127.mm,70.23526435600112.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.5773328996638156.mm, 11.174603174603135.mm, -9.544660631947359.mm)
  circle = ge.add_circle([1304.8964049441038.mm,-593.8095238095239.mm,61.6379070540459.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.545492866971017.mm, 11.174603174603249.mm, -4.9716941896382565.mm)
  circle = ge.add_circle([1302.31907204444.mm,-582.6349206349207.mm,52.09324642209854.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.571263808411913.mm, 11.174603174603249.mm, 2.476711643394019.mm)
  circle = ge.add_circle([1293.773579177469.mm,-571.4603174603175.mm,47.12155223246028.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.061378709086739.mm, 11.174603174603135.mm, 8.492681379749136.mm)
  circle = ge.add_circle([1284.202315369057.mm,-560.2857142857142.mm,49.5982638758543.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.3758159061385413.mm, 11.174603174603135.mm, 9.59680625181496.mm)
  circle = ge.add_circle([1279.1409366599703.mm,-549.1111111111111.mm,58.09094525560344.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.438928693110029.mm, 11.174603174603135.mm, 5.150502302430169.mm)
  circle = ge.add_circle([1281.5167525661088.mm,-537.936507936508.mm,67.6877515074184.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.621285131421928.mm, 11.174603174603135.mm, -2.274656869643934.mm)
  circle = ge.add_circle([1289.9556812592189.mm,-526.7619047619048.mm,72.83825380984857.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.239055092566787.mm, 11.174603174603249.mm, -8.384240764182898.mm)
  circle = ge.add_circle([1299.5769663906408.mm,-515.5873015873017.mm,70.56359694020463.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.1732457448365494.mm, 11.174603174603192.mm, -9.644697734366083.mm)
  circle = ge.add_circle([1304.8160214832076.mm,-504.41269841269843.mm,62.179356176021734.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.328623653744444.mm, 11.174603174603135.mm, -5.327027265654515.mm)
  circle = ge.add_circle([1302.642775738371.mm,-493.23809523809524.mm,52.53465844165565.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.66704146595157.mm, 11.174603174603249.mm, 2.0715937705804706.mm)
  circle = ge.add_circle([1294.3141520846266.mm,-482.0634920634921.mm,47.20763117600114.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.414409072198168.mm, 11.174603174603135.mm, 8.272083525547465.mm)
  circle = ge.add_circle([1284.647110618675.mm,-470.88888888888886.mm,49.27922494658161.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.9697122124318867.mm, 11.174603174603192.mm, 9.68831384993971.mm)
  circle = ge.add_circle([1279.2327015464768.mm,-459.7142857142857.mm,57.55130847212907.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.214626645638873.mm, 11.174603174603135.mm, 5.5011908281293245.mm)
  circle = ge.add_circle([1281.2024137589087.mm,-448.53968253968253.mm,67.23962232206878.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.708512528823348.mm, 11.174603174603249.mm, -1.8676123613903997.mm)
  circle = ge.add_circle([1289.4170404045476.mm,-437.3650793650794.mm,72.74081315019811.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.587362915880476.mm, 11.174603174603135.mm, -8.15625938166383.mm)
  circle = ge.add_circle([1299.125552933371.mm,-426.19047619047615.mm,70.87320078880771.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.765305532648199.mm, 11.174603174603192.mm, -9.727635264088526.mm)
  circle = ge.add_circle([1304.7129158492514.mm,-415.015873015873.mm,62.71694140714388.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.096988202160446.mm, 11.174603174603135.mm, -5.6729157854501295.mm)
  circle = ge.add_circle([1302.9476103166032.mm,-403.8412698412698.mm,52.98930614305535.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.745679936462693.mm, 11.174603174603192.mm, 1.6628030643352218.mm)
  circle = ge.add_circle([1294.8506221144428.mm,-392.6666666666667.mm,47.31639035760522.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.7578399554618045.mm, 11.174603174603135.mm, 8.036819675843432.mm)
  circle = ge.add_circle([1285.10494217798.mm,-381.4920634920635.mm,48.979193421940444.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.5601163162637022.mm, 11.174603174603249.mm, 9.762644546149552.mm)
  circle = ge.add_circle([1279.3471022225183.mm,-370.31746031746036.mm,57.016013097783876.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(7.975760470875457.mm, 11.174603174603135.mm, 5.842126014214088.mm)
  circle = ge.add_circle([1280.907218538782.mm,-359.1428571428571.mm,66.77865764393343.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.778527213049983.mm, 11.174603174603135.mm, -1.457256668668279.mm)
  circle = ge.add_circle([1288.8829790096574.mm,-347.968253968254.mm,72.62078365814752.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.925764620724294.mm, 11.174603174603135.mm, -7.913817354128447.mm)
  circle = ge.add_circle([1298.6615062227074.mm,-336.79365079365084.mm,71.16352698947924.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.354235520945167.mm, 11.174603174603249.mm, -9.793326176971128.mm)
  circle = ge.add_circle([1304.5872708434317.mm,-325.6190476190477.mm,63.24970963535079.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-7.850997190433873.mm, 11.174603174603135.mm, -6.008746505764073.mm)
  circle = ge.add_circle([1303.2330353224866.mm,-314.44444444444446.mm,53.45638345837966.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.80703979782129.mm, 11.174603174603249.mm, 1.2510642903888183.mm)
  circle = ge.add_circle([1295.3820381320527.mm,-303.2698412698413.mm,47.44763695261559.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-6.091062472885142.mm, 11.174603174603135.mm, 7.787306941821903.mm)
  circle = ge.add_circle([1285.5749983342314.mm,-292.0952380952381.mm,48.69870124300441.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.1477544109268365.mm, 11.174603174603249.mm, 9.819666555791706.mm)
  circle = ge.add_circle([1279.4839358613463.mm,-280.92063492063494.mm,56.48600818482631.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(7.722753666748758.mm, 11.174603174603135.mm, 6.172703399439527.mm)
  circle = ge.add_circle([1280.631690272273.mm,-269.7460317460317.mm,66.30567474061802.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.831205051525103.mm, 11.174603174603135.mm, -1.0443173318518006.mm)
  circle = ge.add_circle([1288.3544439390218.mm,-258.57142857142856.mm,72.47837814005754.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(6.253660237591021.mm, 11.174603174603135.mm, -7.65734451931656.mm)
  circle = ge.add_circle([1298.185648990547.mm,-247.39682539682542.mm,71.43406080820574.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-0.9407645165540544.mm, 11.174603174603249.mm, -9.841654006269906.mm)
  circle = ge.add_circle([1304.439309228138.mm,-236.22222222222229.mm,63.77671628888918.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-7.591086748478347.mm, 11.174603174603135.mm, -6.333924015317287.mm)
  circle = ge.add_circle([1303.498544711584.mm,-225.04761904761904.mm,53.93506228261928.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.851012262023687.mm, 11.174603174603249.mm, 0.837107441250204.mm)
  circle = ge.add_circle([1295.9074579631056.mm,-213.8730158730159.mm,47.60113826730199.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-6.413485837403641.mm, 11.174603174603135.mm, 7.52398769723591.mm)
  circle = ge.add_circle([1286.0564457010819.mm,-202.69841269841265.mm,48.438245708552195.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.7333575937109345.mm, 11.174603174603135.mm, 9.859278781659647.mm)
  circle = ge.add_circle([1279.6429598636782.mm,-191.52380952380952.mm,55.962233405788105.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(7.4560548018262125.mm, 11.174603174603135.mm, 6.492336886430067.mm)
  circle = ge.add_circle([1280.3763174573892.mm,-180.34920634920638.mm,65.82151218744775.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.866452649042685.mm, 11.174603174603249.mm, -0.6295264719886262.mm)
  circle = ge.add_circle([1287.8323722592154.mm,-169.17460317460325.mm,72.31384907387782.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.698824908258075.mm, 0.mm, -11.684322601889193.mm)
  circle = ge.add_circle([1297.698824908258.mm,-158.mm,71.68432260188919.mm], vec, 5.mm, 8)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 88.mm, 0.mm)
  circle = ge.add_circle([1292.mm,-158.mm,60.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.939000000000078.mm, 0.mm, 182.40000000000003.mm)
  circle = ge.add_circle([1292.mm,-70.mm,60.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.99496719611102.mm, 9.207730857270427.mm, 11.372464949587481.mm)
  circle = ge.add_circle([1294.939.mm,-70.mm,242.40000000000003.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.641549939327888.mm, -9.164298928050435.mm, 11.286205666047522.mm)
  circle = ge.add_circle([1285.944032803889.mm,-60.79226914272957.mm,253.77246494958752.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.941961640230147.mm, -9.189638245741236.mm, 11.164013009620362.mm)
  circle = ge.add_circle([1282.3024828645612.mm,-69.95656807078001.mm,265.05867061563504.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.331149549226211.mm, -3.85350347848248.mm, 11.077177355757726.mm)
  circle = ge.add_circle([1286.2444445047913.mm,-79.14620631652124.mm,276.2226836252554.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.381821324327575.mm, 3.7308654938301373.mm, 11.076360884556948.mm)
  circle = ge.add_circle([1295.5755940540175.mm,-82.99970979500372.mm,287.2998609810131.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.064413733362699.mm, 9.13855045261559.mm, 11.162039946562686.mm)
  circle = ge.add_circle([1304.957415378345.mm,-79.26884430117359.mm,298.3762218655701.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.518759265741437.mm, 9.214567274365436.mm, 11.284227147463753.mm)
  circle = ge.add_circle([1309.0218291117078.mm,-70.130293848558.mm,309.53826181213276.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.94347721629515.mm, 3.914565767164234.mm, 11.371635294704333.mm)
  circle = ge.add_circle([1305.5030698459664.mm,-60.91572657419256.mm,320.8224889595965.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.044818504160048.mm, -3.6692952732681263.mm, 11.373268200653058.mm)
  circle = ge.add_circle([1296.5595926296712.mm,-57.00116080702833.mm,332.19412425430085.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.763657984897236.mm, -9.112393969026904.mm, 11.288173185487892.mm)
  circle = ge.add_circle([1287.5147741255112.mm,-60.670456080296454.mm,343.5673924549539.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.818837868415585.mm, -9.239084900918641.mm, 11.16599689539538.mm)
  circle = ge.add_circle([1283.751116140614.mm,-69.78285004932336.mm,354.8555656404418.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.278843663565112.mm, -3.9754532825315323.mm, 11.078020157281628.mm)
  circle = ge.add_circle([1287.5699540090295.mm,-79.021934950242.mm,366.0215625358372.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.430849939616564.mm, 3.6075612299644035.mm, 11.075570889489313.mm)
  circle = ge.add_circle([1296.8487976725946.mm,-82.99738823277353.mm,377.0995826931188.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.18617227962045.mm, 9.085830645090851.mm, 11.160078058583224.mm)
  circle = ge.add_circle([1306.2796476122112.mm,-79.38982700280913.mm,388.1751535826081.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.395307892796609.mm, 9.263190030764278.mm, 11.282237983071923.mm)
  circle = ge.add_circle([1310.4658198918316.mm,-70.30399635771828.mm,399.33523164119134.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.890357760085635.mm, 4.036163306144211.mm, 11.370779384168145.mm)
  circle = ge.add_circle([1307.070511999035.mm,-61.040806326954.mm,410.61746962426326.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.093022237711466.mm, -3.54566612015401.mm, 11.374044904451864.mm)
  circle = ge.add_circle([1298.1801542389494.mm,-57.00464302080979.mm,421.9882490084314.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.8850615956996535.mm, -9.05886166677815.mm, 11.290129354414205.mm)
  circle = ge.add_circle([1289.087132001238.mm,-60.5503091409638.mm,433.3622939128833.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.695064406064148.mm, -9.286881587682458.mm, 11.167991249594081.mm)
  circle = ge.add_circle([1285.2020704055383.mm,-69.60917080774195.mm,444.6524232672975.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.22491300842762.mm, -4.096693127486546.mm, 11.078889138616319.mm)
  circle = ge.add_circle([1288.8971348116024.mm,-78.8960523954244.mm,455.82041451689156.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.478226639282411.mm, 3.4836127072631626.mm, 11.07480751163672.mm)
  circle = ge.add_circle([1298.12204782003.mm,-82.99274552291095.mm,466.8993036555079.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.307215534669922.mm, 9.031488238170581.mm, 11.158127696047075.mm)
  circle = ge.add_circle([1307.6002744593125.mm,-79.50913281564779.mm,477.9741111671446.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.271217867142468.mm, 9.310158513918111.mm, 11.280238528108043.mm)
  circle = ge.add_circle([1311.9074899939824.mm,-70.47764457747721.mm,489.1322388631917.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.835618313858731.mm, 4.157040044088305.mm, 11.369897370832405.mm)
  circle = ge.add_circle([1308.63627212684.mm,-61.167486063559096.mm,500.4124773912997.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.139569788267636.mm, -3.4214037617857045.mm, 11.374794922275669.mm)
  circle = ge.add_circle([1299.8006538129812.mm,-57.01044601947079.mm,511.7823747621321.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.005739090786619.mm, -9.003711581407579.mm, 11.292073823482497.mm)
  circle = ge.add_circle([1290.6610840247135.mm,-60.431849781256496.mm,523.1571696844078.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.5706633573449835.mm, -9.333019770228091.mm, 11.16999571605345.mm)
  circle = ge.add_circle([1286.655344933927.mm,-69.43556136266407.mm,534.4492435078903.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.1693672150584.mm, -4.21720136164538.mm, 11.079784144574205.mm)
  circle = ge.add_circle([1290.226008291272.mm,-78.76858113289217.mm,545.6192392239437.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.523942962524416.mm, 3.3590420611596414.mm, 11.07407088732748.mm)
  circle = ge.add_circle([1299.3953755063303.mm,-82.98578249453755.mm,556.6990233685179.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.427521881915709.mm, 8.975532936631367.mm, 11.15618920726115.mm)
  circle = ge.add_circle([1308.9193184688547.mm,-79.6267404333779.mm,567.7730942558454.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.14651134948258.mm, 9.355464335927678.mm, 11.278229139646442.mm)
  circle = ge.add_circle([1313.3468403507704.mm,-70.65120749674654.mm,578.9292834631066.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.779268653295503.mm, 4.2771743941400615.mm, 11.368989412211704.mm)
  circle = ge.add_circle([1310.2003290012879.mm,-61.29574316081886.mm,590.207512602753.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.184452843102463.mm, -3.296530389643003.mm, 11.375518120182392.mm)
  circle = ge.add_circle([1301.4210603479924.mm,-57.0185687666788.mm,601.5765020149647.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.125668918883548.mm, -8.946953561931686.mm, 11.294006245438482.mm)
  circle = ge.add_circle([1292.23660750489.mm,-60.3150991563218.mm,612.9520201351471.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.4456569385067723.mm, -9.377491208936064.mm, 11.17200993680433.mm)
  circle = ge.add_circle([1288.1109385860063.mm,-69.26205271825349.mm,624.2460263805856.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.112216203140633.mm, -4.336956463961059.mm, 11.08070501531995.mm)
  circle = ge.add_circle([1291.556595524513.mm,-78.63954392718955.mm,635.4180363173899.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.567990745061024.mm, 3.2338715381895327.mm, 11.073361148112099.mm)
  circle = ge.add_circle([1300.6688117276537.mm,-82.97650039115061.mm,646.4987413327099.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.547069836366063.mm, 8.917974733289725.mm, 11.154262938411762.mm)
  circle = ge.add_circle([1310.2368024727148.mm,-79.74262885296108.mm,657.572102480822.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.0212106106175725.mm, 9.399099405821133.mm, 11.276210176535074.mm)
  circle = ge.add_circle([1314.7838723090808.mm,-70.82465411967135.mm,668.7263654192337.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.721318841639913.mm, 4.396544902022889.mm, 11.36805567045485.mm)
  circle = ge.add_circle([1311.7626616984633.mm,-61.42555471385022.mm,680.0025755957688.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.227663386743643.mm, -3.171068304324052.mm, 11.37621436901884.mm)
  circle = ge.add_circle([1303.0413428568233.mm,-57.02900981182733.mm,691.3706312662237.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.244829662238772.mm, -8.888597744520972.mm, 11.295926275179227.mm)
  circle = ge.add_circle([1293.8136794700797.mm,-60.20007811615138.mm,702.7468456352425.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.3200674739075566.mm, -9.4202879618435.mm, 11.174033552135825.mm)
  circle = ge.add_circle([1289.568849807841.mm,-69.08867586067235.mm,714.0427719104217.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.053470179027954.mm, -4.455937047885172.mm, 11.081651586399289.mm)
  circle = ge.add_circle([1292.8889172817485.mm,-78.50896382251585.mm,725.2168054625575.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.610362120588889.mm, 3.108123492017853.mm, 11.072678420739976.mm)
  circle = ge.add_circle([1301.9423874607764.mm,-82.96490087040102.mm,736.2984570489568.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.665838048465275.mm, 8.858823907217442.mm, 11.152349233502946.mm)
  circle = ge.add_circle([1311.5527495813653.mm,-79.85677737838317.mm,747.3711354696968.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.895338027466778.mm, 9.44105593099924.mm, 11.274181999331745.mm)
  circle = ge.add_circle([1316.2185876298306.mm,-70.99795347116573.mm,758.5234847031998.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.661779227899387.mm, 4.515130249871426.mm, 11.36709631231463.mm)
  circle = ge.add_circle([1313.3232496023638.mm,-61.55689754016649.mm,769.7976667025315.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.26919370240671.mm, -3.0450399115628954.mm, 11.376883544444922.mm)
  circle = ge.add_circle([1304.6614703744644.mm,-57.04176729029506.mm,781.1647630148461.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.363200040447055.mm, -8.828654550689528.mm, 11.297833569814998.mm)
  circle = ge.add_circle([1295.3922766720577.mm,-60.08680720185796.mm,792.541646559291.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.1939173920288795.mm, -9.461402386062474.mm, 11.17606620065908.mm)
  circle = ge.add_circle([1291.0290766316107.mm,-68.91546175254749.mm,803.839480129106.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.99313963392001.mm, -4.5741218651873226.mm, 11.08262368876808.mm)
  circle = ge.add_circle([1294.2229940236396.mm,-78.37686413860996.mm,815.0155463297651.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.65104952218644.mm, 2.9818203794469866.mm, 11.07202282713638.mm)
  circle = ge.add_circle([1303.2161336575596.mm,-82.95098600379728.mm,826.0981700185332.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.783805307909915.mm, 8.798091021906075.mm, 11.150448434295186.mm)
  circle = ge.add_circle([1312.867183179746.mm,-79.9691656243503.mm,837.1701928456696.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.7689160790737333.mm, 9.481326418626622.mm, 11.272144970240106.mm)
  circle = ge.add_circle([1317.650988487656.mm,-71.17107460244422.mm,848.3206412799648.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.600660444996947.mm, 4.63290926003878.mm, 11.366111509118582.mm)
  circle = ge.add_circle([1314.8820724085822.mm,-61.6897481838176.mm,859.5927862502049.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.3090363733711.mm, -2.9184677182276957.mm, 11.377525526955651.mm)
  circle = ge.add_circle([1306.2814119635852.mm,-57.05683892377882.mm,870.9588977593235.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.480758914252874.mm, -8.767134685434584.mm, 11.299727788730138.mm)
  circle = ge.add_circle([1296.9723755902141.mm,-59.975306642006515.mm,882.3364232862791.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.067229221471962.mm, -9.500827139144917.mm, 11.178107519372134.mm)
  circle = ge.add_circle([1292.4916166759613.mm,-68.7424413274411.mm,893.6361510750093.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.931235341988668.mm, -4.691489809749541.mm, 11.083621148822886.mm)
  circle = ge.add_circle([1295.5588458974332.mm,-78.24326846658602.mm,904.8142585943814.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.690045683665176.mm, 2.8549847564063526.mm, 11.071394484381017.mm)
  circle = ge.add_circle([1304.490081239422.mm,-82.93475827633556.mm,915.8978797432043.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.900950547435059.mm, 8.735786923380218.mm, 11.148560880243735.mm)
  circle = ge.add_circle([1314.180126923087.mm,-80.0797735199292.mm,926.9692742275853.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.641967342589851.mm, 9.519903676970202.mm, 11.270099453044168.mm)
  circle = ge.add_circle([1319.0810774705221.mm,-71.34398659654899.mm,938.117835107829.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.537973407873551.mm, 4.749860898878353.mm, 11.365101436738655.mm)
  circle = ge.add_circle([1316.4391101279323.mm,-61.824082919578785.mm,949.3879345608732.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.347184284305058.mm, -2.791374328301835.mm, 11.37814020190217.mm)
  circle = ge.add_circle([1307.9011367200587.mm,-57.07422202070043.mm,960.7530359976118.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.597485289323004.mm, -8.704049135324091.mm, 11.301608593644005.mm)
  circle = ge.add_circle([1298.5539524357537.mm,-59.86559634900227.mm,972.131176199514.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.9400255869313696.mm, -9.538555180393715.mm, 11.180157143724728.mm)
  circle = ge.add_circle([1293.9564671464307.mm,-68.56964548432636.mm,983.432784793158.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.867768358456487.mm, -4.808019921335756.mm, 11.084643788431663.mm)
  circle = ge.add_circle([1296.896492733362.mm,-78.10820066472007.mm,994.6129419368827.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.727343640867957.mm, 2.727639273923998.mm, 11.070793504686776.mm)
  circle = ge.add_circle([1305.7642610918185.mm,-82.91622058605583.mm,1005.6975857253144.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.017252846576184.mm, 8.671922738260733.mm, 11.146686908438937.mm)
  circle = ge.add_circle([1315.4916047326865.mm,-80.18858131213183.mm,1016.7683792300012.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.514514489243311.mm, 9.556780816683371.mm, 11.268045813044182.mm)
  circle = ge.add_circle([1320.5088575792627.mm,-71.5166585738711.mm,1027.9150661384401.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.473729311537227.mm, 4.8659642805003.mm, 11.36406627555948.mm)
  circle = ge.add_circle([1317.9943430900194.mm,-61.959877757187726.mm,1039.1831119514843.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.383630622538476.mm, -2.6637824388469085.mm, 11.37872745951222.mm)
  circle = ge.add_circle([1309.5206137784821.mm,-57.093913476687426.mm,1050.5471782270438.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.713358319995223.mm, -8.639409166534925.mm, 11.303475648672247.mm)
  circle = ge.add_circle([1300.1369831559437.mm,-59.757695915534335.mm,1061.925905686556.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.8123292051570843.mm, -9.57457977212053.mm, 11.182214707683215.mm)
  circle = ge.add_circle([1295.4236248359484.mm,-68.39710508206926.mm,1073.2293813352283.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.802750017616972.mm, -4.923691389334692.mm, 11.085691424965262.mm)
  circle = ge.add_circle([1298.2359540411055.mm,-77.97168485418979.mm,1084.4115960429115.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.762936732914568.mm, 2.599806674081691.mm, 11.070219995380057.mm)
  circle = ge.add_circle([1307.0387040587225.mm,-82.89537624352448.mm,1095.4972874678767.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.1326914354062865.mm, 8.606509871777604.mm, 11.14482685354551.mm)
  circle = ge.add_circle([1316.801640791637.mm,-80.29556956944279.mm,1106.5675074632568.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.3865802802918097.mm, 9.591951252036644.mm, 11.265984416990932.mm)
  circle = ge.add_circle([1321.9343322270433.mm,-71.68905969766519.mm,1117.7123343168023.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.40793962906423.mm, 4.981198670501122.mm, 11.36300621044552.mm)
  circle = ge.add_circle([1319.5477519467515.mm,-62.09710844562854.mm,1128.9783187337932.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.418368879275704.mm, -2.5357148359493635.mm, 11.37928719490992.mm)
  circle = ge.add_circle([1311.1398123176873.mm,-57.11590977512742.mm,1140.3413249442387.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.828357313004972.mm, -8.57322632284091.mm, 11.305328620385353.mm)
  circle = ge.add_circle([1301.7214434384116.mm,-59.651624611076784.mm,1151.7206121391487.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.6841628808961104.mm, -9.60889448084859.mm, 11.184279843796048.mm)
  circle = ge.add_circle([1296.8930861254066.mm,-68.2248509339177.mm,1163.025940759534.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.736191930817768.mm, -5.038483556476592.mm, 11.086763871330959.mm)
  circle = ge.add_circle([1299.5772490063027.mm,-77.83374541476628.mm,1174.21022060333.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.796818603386555.mm, 2.4715097859532733.mm, 11.069674058881446.mm)
  circle = ge.add_circle([1308.3134409371205.mm,-82.87222897124288.mm,1185.296984474661.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.2472456982441145.mm, 8.539560005733222.mm, 11.142981047742751.mm)
  circle = ge.add_circle([1318.110259540507.mm,-80.4007191852896.mm,1196.3666585335425.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.258187562953708.mm, 9.62540870209304.mm, 11.263915633020133.mm)
  circle = ge.add_circle([1323.3575052387512.mm,-71.86115917955638.mm,1207.5096395812852.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.340616109551547.mm, 5.0955434896672.mm, 11.361921430709344.mm)
  circle = ge.add_circle([1321.0993176757975.mm,-62.23575047746334.mm,1218.7735552143054.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.451392850761522.mm, -2.4071943906512985.mm, 11.379819308134756.mm)
  circle = ge.add_circle([1312.758701566246.mm,-57.14020698779614.mm,1230.1354766450147.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.942461731176081.mm, -8.5055124235516.mm, 11.307167177868905.mm)
  circle = ge.add_circle([1303.3073087154844.mm,-59.54740137844744.mm,1241.5152959531495.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.555549502820895.mm, -9.641493178461275.mm, 11.186352183259942.mm)
  circle = ge.add_circle([1298.3648469843083.mm,-68.05291380199904.mm,1252.8224631310184.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.668105984379508.mm, -5.152375922522495.mm, 11.087860936004745.mm)
  circle = ge.add_circle([1300.9203964871292.mm,-77.69440698046031.mm,1264.0088153142783.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.828983201467508.mm, 2.342771521527908.mm, 11.069155792688207.mm)
  circle = ge.add_circle([1309.5885024715087.mm,-82.84678290298281.mm,1275.096676250283.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.36089517733717.mm, 8.471085096415933.mm, 11.141149820664168.mm)
  circle = ge.add_circle([1319.4174856729762.mm,-80.5040113814549.mm,1286.1658320429713.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.1293592663328127.mm, 9.65714719183076.mm, 11.261839830587405.mm)
  circle = ge.add_circle([1324.7783808503134.mm,-72.03292628503897.mm,1297.3069818636354.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.271770776016183.mm, 5.208978317649283.mm, 11.360812130077647.mm)
  circle = ge.add_circle([1322.6490215839806.mm,-62.37577909320821.mm,1308.5688216942228.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.482696639387086.mm, -2.278244054865965.mm, 11.3803237041584.mm)
  circle = ge.add_circle([1314.3772508079644.mm,-57.166800775558926.mm,1319.9296338243005.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.05565119709172.mm, -8.436279561400454.mm, 11.308990992783038.mm)
  circle = ge.add_circle([1304.8945541685773.mm,-59.44504483042489.mm,1331.3099575284589.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.4265120394416044.mm, -9.672370043297946.mm, 11.188431355983994.mm)
  circle = ge.add_circle([1299.8389029714856.mm,-67.88132439182534.mm,1342.618948521242.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.598504337479199.mm, -5.265348147924811.mm, 11.088982423067591.mm)
  circle = ge.add_circle([1302.2654150109272.mm,-77.55369443512329.mm,1353.807379877226.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.859424783019449.mm, 2.2136148716182618.mm, 11.068665289353476.mm)
  circle = ge.add_circle([1310.8639193484064.mm,-82.8190425830481.mm,1364.8963623002935.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.473619576514466.mm, 8.401097372465173.mm, 11.139333499342229.mm)
  circle = ge.add_circle([1320.7233441314258.mm,-80.60542771142984.mm,1375.965027589647.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.0001183973201933.mm, 9.687161053209408.mm, 11.259757380400742.mm)
  circle = ge.add_circle([1326.1969637079403.mm,-72.20433033896467.mm,1387.1043610889892.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.201415923250579.mm, 5.321482896609602.mm, 11.359678506654745.mm)
  circle = ge.add_circle([1324.1968453106201.mm,-62.51716928575526.mm,1398.36411846939.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.512274654742441.mm, -2.1488868572789173.mm, 11.380800292904041.mm)
  circle = ge.add_circle([1315.9954293873695.mm,-57.195686389145656.mm,1409.7237969760447.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.167905496733056.mm, -8.365540100386568.mm, 11.310799739420418.mm)
  circle = ge.add_circle([1306.483154732627.mm,-59.344573246424574.mm,1421.1045972689487.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.29707353500271.mm, -9.701519561192043.mm, 11.190516990657898.mm)
  circle = ge.add_circle([1301.315249235894.mm,-67.71011334681114.mm,1432.4153970083692.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.527399419975836.mm, -5.377380057459916.mm, 11.090128132237169.mm)
  circle = ge.add_circle([1303.6123227708968.mm,-77.41163290800318.mm,1443.605913999027.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.888137911611466.mm, 2.0840629017546064.mm, 11.06820263647569.mm)
  circle = ge.add_circle([1312.1397221908726.mm,-82.7890129654631.mm,1454.6960421312642.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.585398764810179.mm, 8.329609332687397.mm, 11.137532408144807.mm)
  circle = ge.add_circle([1322.027860102484.mm,-80.7049500637085.mm,1465.76424476774.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.870488036486222.mm, 9.715444926182656.mm, 11.257668654356394.mm)
  circle = ge.add_circle([1327.6132588672942.mm,-72.3753407310211.mm,1476.9017771758847.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.129564115624817.mm, 5.433037134839523.mm, 11.358520762890521.mm)
  circle = ge.add_circle([1325.742770830808.mm,-62.65989580483844.mm,1488.159445830241.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.540121614618556.mm, -2.019145899235511.mm, 11.381248989258438.mm)
  circle = ge.add_circle([1317.6132067151832.mm,-57.22685866999892.mm,1499.5179665931316.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.279204583086084.mm, -8.293306673565766.mm, 11.31259309476468.mm)
  circle = ge.add_circle([1308.0730851005646.mm,-59.24600456923443.mm,1510.89921558239.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.167257105370254.mm, -9.728936526456565.mm, 11.192608714817425.mm)
  circle = ge.add_circle([1302.7938805174786.mm,-67.5393112428002.mm,1522.2118086771547.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.454803930189655.mm, -5.488451643831226.mm, 11.0912978589065.mm)
  circle = ge.add_circle([1304.9611376228488.mm,-77.26824776925676.mm,1533.4044173919722.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.915117459490148.mm, 1.95413874806583.mm, 11.06776791667744.mm)
  circle = ge.add_circle([1313.4159415530385.mm,-82.75669941308799.mm,1544.4957152508787.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.6962127800597955.mm, 8.256633743823883.mm, 11.135746868721526.mm)
  circle = ge.add_circle([1323.3310590125286.mm,-80.80256066502216.mm,1555.5634831675561.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.740491333959426.mm, 9.741993759655351.mm, 11.255574025470878.mm)
  circle = ge.add_circle([1329.0272717925884.mm,-72.54592692119827.mm,1566.6992300362776.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.056228184843803.mm, 5.543621110347708.mm, 11.357339105540632.mm)
  circle = ge.add_circle([1327.286780458629.mm,-62.80393316154292.mm,1577.9548040617485.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.566232545945468.mm, -1.8890443506149097.mm, 11.381669713091696.mm)
  circle = ge.add_circle([1319.2305522737852.mm,-57.260312051195214.mm,1589.3121431672892.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.389528579727994.mm, -8.21959218079509.mm, 11.314370738548405.mm)
  circle = ge.add_circle([1309.6643197278397.mm,-59.149356401810124.mm,1600.6938128803808.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.0370859339018352.mm, -9.754616042813709.mm, 11.194706154910364.mm)
  circle = ge.add_circle([1304.2747911481117.mm,-67.36894858260521.mm,1612.0081836189293.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.380730832637482.mm, -5.598543071242105.mm, 11.092491394178978.mm)
  circle = ge.add_circle([1306.3118770820136.mm,-77.12356462541892.mm,1623.2028897738396.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.94035860849317.mm, 1.8238656131472624.mm, 11.067361207593422.mm)
  circle = ge.add_circle([1314.692607914651.mm,-82.72210769666103.mm,1634.2953811680186.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.806041832466008.mm, 8.182183638271212.mm, 11.133977199943729.mm)
  circle = ge.add_circle([1324.6329665231442.mm,-80.89824208351376.mm,1645.362742375612.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.6101515052912418.mm, 9.76680281238555.mm, 11.253473867815046.mm)
  circle = ge.add_circle([1330.4390083556102.mm,-72.71605844524255.mm,1656.4967195755557.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-7.981421227656256.mm, 5.653215074417858.mm, 11.356133745633088.mm)
  circle = ge.add_circle([1328.828856850319.mm,-62.949255632857.mm,1667.7501934433708.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.590602785685178.mm, -1.758605445692929.mm, 11.382062389268185.mm)
  circle = ge.add_circle([1320.8474356226627.mm,-57.296040558439145.mm,1679.1063271890039.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.498857784368965.mm, -8.144409786428518.mm, 11.316132353309285.mm)
  circle = ge.add_circle([1311.2568328369775.mm,-59.054646004132074.mm,1690.488389578272.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(12.693024947391677.mm, -2.8009442094394075.mm, -0.20452193158098453.mm)
  circle = ge.add_circle([1305.7579750526086.mm,-67.19905579056059.mm,1701.8045219315813.mm], vec, 5.mm, 8)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.938999999999851.mm, 0.mm, 182.39999999999964.mm)
  circle = ge.add_circle([1318.4510000000002.mm,-70.mm,1701.6000000000004.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.8330000000000837.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1321.39.mm,-70.mm,1884.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.277000000000044.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1319.557.mm,-70.mm,1884.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.mm, -9.mm, 0.mm)
  circle = ge.add_circle([1318.mm,-920.mm,60.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-7.mm, -21.mm, 0.mm)
  circle = ge.add_circle([1315.mm,-929.mm,60.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 88.mm, 0.mm)
  circle = ge.add_circle([1308.mm,-950.mm,60.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.240646482510101.mm, 11.174603174603135.mm, -9.143875140511966.mm)
  circle = ge.add_circle([1308.mm,-862.mm,60.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.103793034090586.mm, 11.174603174603249.mm, -3.8554044985163287.mm)
  circle = ge.add_circle([1317.24064648251.mm,-850.8253968253969.mm,50.856124859488034.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.182943879120785.mm, 11.174603174603135.mm, 3.6628859069936794.mm)
  circle = ge.add_circle([1308.1368534484195.mm,-839.6507936507936.mm,47.000720360971705.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.951028205245848.mm, 11.174603174603135.mm, 9.062702001946683.mm)
  circle = ge.add_circle([1298.9539095692987.mm,-828.4761904761905.mm,50.663606267965385.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.5660123580282743.mm, 11.174603174603249.mm, 9.220994920133435.mm)
  circle = ge.add_circle([1295.0028813640529.mm,-817.3015873015873.mm,59.72630826991207.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.02060659798417.mm, 11.174603174603135.mm, 4.046214040203338.mm)
  circle = ge.add_circle([1298.5688937220812.mm,-806.1269841269841.mm,68.9473031900455.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.25802404655201.mm, 11.174603174603135.mm, -3.4687436065814126.mm)
  circle = ge.add_circle([1307.5895003200653.mm,-794.952380952381.mm,72.99351723024884.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.140951454441392.mm, 11.174603174603249.mm, -8.977511487416585.mm)
  circle = ge.add_circle([1316.8475243666173.mm,-783.7777777777778.mm,69.52477362366743.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.3710904324400417.mm, 11.174603174603135.mm, -9.294027154632523.mm)
  circle = ge.add_circle([1320.9884758210587.mm,-772.6031746031746.mm,60.54726213625084.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.933421446249213.mm, 11.174603174603249.mm, -4.235229948707868.mm)
  circle = ge.add_circle([1317.6173853886187.mm,-761.4285714285714.mm,51.25323498161832.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.32900025433878.mm, 11.174603174603135.mm, 3.2730636579942143.mm)
  circle = ge.add_circle([1308.6839639423695.mm,-750.2539682539682.mm,47.01800503291045.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.3290390746112735.mm, 11.174603174603135.mm, 8.888341360750331.mm)
  circle = ge.add_circle([1299.3549636880307.mm,-739.0793650793651.mm,50.291068690904666.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.174674147038104.mm, 11.174603174603135.mm, 9.36293946978536.mm)
  circle = ge.add_circle([1295.0259246134194.mm,-727.9047619047619.mm,59.179410051655.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.842276226910144.mm, 11.174603174603249.mm, 4.42236843577696.mm)
  circle = ge.add_circle([1298.2005987604575.mm,-716.7301587301588.mm,68.54234952144036.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.395841039666493.mm, 11.174603174603135.mm, -3.075932803565891.mm)
  circle = ge.add_circle([1307.0428749873677.mm,-705.5555555555555.mm,72.96471795721732.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.51520768900059.mm, 11.174603174603249.mm, -8.795231149886035.mm)
  circle = ge.add_circle([1316.4387160270342.mm,-694.3809523809524.mm,69.88878515365143.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.976850570564011.mm, 11.174603174603135.mm, -9.427701317673794.mm)
  circle = ge.add_circle([1320.9539237160348.mm,-683.2063492063492.mm,61.09355400376539.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.747211343437812.mm, 11.174603174603135.mm, -4.607546545393788.mm)
  circle = ge.add_circle([1317.9770731454707.mm,-672.031746031746.mm,51.6658526860916.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.458516772898975.mm, 11.174603174603135.mm, 2.87743842879766.mm)
  circle = ge.add_circle([1309.229861802033.mm,-660.8571428571429.mm,47.05830614069781.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.69937477152439.mm, 11.174603174603249.mm, 8.698222129348956.mm)
  circle = ge.add_circle([1299.771345029134.mm,-649.6825396825398.mm,49.93574456949547.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.7777073955937794.mm, 11.174603174603135.mm, 9.488283990227039.mm)
  circle = ge.add_circle([1295.0719702576096.mm,-638.5079365079365.mm,58.633966698844425.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.648268936837894.mm, 11.174603174603249.mm, 4.790682190550868.mm)
  circle = ge.add_circle([1297.8496776532033.mm,-627.3333333333334.mm,68.12225068907146.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.516999670712721.mm, 11.174603174603135.mm, -2.6776685236212074.mm)
  circle = ge.add_circle([1306.4979465900412.mm,-616.1587301587301.mm,72.91293287962233.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.88145868334982.mm, 11.174603174603135.mm, -8.597357301955228.mm)
  circle = ge.add_circle([1316.014946260754.mm,-604.984126984127.mm,70.23526435600112.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.5773328996638156.mm, 11.174603174603135.mm, -9.544660631947359.mm)
  circle = ge.add_circle([1320.8964049441038.mm,-593.8095238095239.mm,61.6379070540459.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.545492866971017.mm, 11.174603174603249.mm, -4.9716941896382565.mm)
  circle = ge.add_circle([1318.31907204444.mm,-582.6349206349207.mm,52.09324642209854.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.571263808411913.mm, 11.174603174603249.mm, 2.476711643394019.mm)
  circle = ge.add_circle([1309.773579177469.mm,-571.4603174603175.mm,47.12155223246028.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.061378709086739.mm, 11.174603174603135.mm, 8.492681379749136.mm)
  circle = ge.add_circle([1300.202315369057.mm,-560.2857142857142.mm,49.5982638758543.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.3758159061385413.mm, 11.174603174603135.mm, 9.59680625181496.mm)
  circle = ge.add_circle([1295.1409366599703.mm,-549.1111111111111.mm,58.09094525560344.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.438928693110029.mm, 11.174603174603135.mm, 5.150502302430169.mm)
  circle = ge.add_circle([1297.5167525661088.mm,-537.936507936508.mm,67.6877515074184.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.621285131421928.mm, 11.174603174603135.mm, -2.274656869643934.mm)
  circle = ge.add_circle([1305.9556812592189.mm,-526.7619047619048.mm,72.83825380984857.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.239055092566787.mm, 11.174603174603249.mm, -8.384240764182898.mm)
  circle = ge.add_circle([1315.5769663906408.mm,-515.5873015873017.mm,70.56359694020463.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.1732457448365494.mm, 11.174603174603192.mm, -9.644697734366083.mm)
  circle = ge.add_circle([1320.8160214832076.mm,-504.41269841269843.mm,62.179356176021734.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.328623653744444.mm, 11.174603174603135.mm, -5.327027265654515.mm)
  circle = ge.add_circle([1318.642775738371.mm,-493.23809523809524.mm,52.53465844165565.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.66704146595157.mm, 11.174603174603249.mm, 2.0715937705804706.mm)
  circle = ge.add_circle([1310.3141520846266.mm,-482.0634920634921.mm,47.20763117600114.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.414409072198168.mm, 11.174603174603135.mm, 8.272083525547465.mm)
  circle = ge.add_circle([1300.647110618675.mm,-470.88888888888886.mm,49.27922494658161.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.9697122124318867.mm, 11.174603174603192.mm, 9.68831384993971.mm)
  circle = ge.add_circle([1295.2327015464768.mm,-459.7142857142857.mm,57.55130847212907.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.214626645638873.mm, 11.174603174603135.mm, 5.5011908281293245.mm)
  circle = ge.add_circle([1297.2024137589087.mm,-448.53968253968253.mm,67.23962232206878.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.708512528823348.mm, 11.174603174603249.mm, -1.8676123613903997.mm)
  circle = ge.add_circle([1305.4170404045476.mm,-437.3650793650794.mm,72.74081315019811.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.587362915880476.mm, 11.174603174603135.mm, -8.15625938166383.mm)
  circle = ge.add_circle([1315.125552933371.mm,-426.19047619047615.mm,70.87320078880771.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.765305532648199.mm, 11.174603174603192.mm, -9.727635264088526.mm)
  circle = ge.add_circle([1320.7129158492514.mm,-415.015873015873.mm,62.71694140714388.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.096988202160446.mm, 11.174603174603135.mm, -5.6729157854501295.mm)
  circle = ge.add_circle([1318.9476103166032.mm,-403.8412698412698.mm,52.98930614305535.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.745679936462693.mm, 11.174603174603192.mm, 1.6628030643352218.mm)
  circle = ge.add_circle([1310.8506221144428.mm,-392.6666666666667.mm,47.31639035760522.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.7578399554618045.mm, 11.174603174603135.mm, 8.036819675843432.mm)
  circle = ge.add_circle([1301.10494217798.mm,-381.4920634920635.mm,48.979193421940444.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.5601163162637022.mm, 11.174603174603249.mm, 9.762644546149552.mm)
  circle = ge.add_circle([1295.3471022225183.mm,-370.31746031746036.mm,57.016013097783876.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(7.975760470875457.mm, 11.174603174603135.mm, 5.842126014214088.mm)
  circle = ge.add_circle([1296.907218538782.mm,-359.1428571428571.mm,66.77865764393343.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.778527213049983.mm, 11.174603174603135.mm, -1.457256668668279.mm)
  circle = ge.add_circle([1304.8829790096574.mm,-347.968253968254.mm,72.62078365814752.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.925764620724294.mm, 11.174603174603135.mm, -7.913817354128447.mm)
  circle = ge.add_circle([1314.6615062227074.mm,-336.79365079365084.mm,71.16352698947924.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.354235520945167.mm, 11.174603174603249.mm, -9.793326176971128.mm)
  circle = ge.add_circle([1320.5872708434317.mm,-325.6190476190477.mm,63.24970963535079.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-7.850997190433873.mm, 11.174603174603135.mm, -6.008746505764073.mm)
  circle = ge.add_circle([1319.2330353224866.mm,-314.44444444444446.mm,53.45638345837966.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.80703979782129.mm, 11.174603174603249.mm, 1.2510642903888183.mm)
  circle = ge.add_circle([1311.3820381320527.mm,-303.2698412698413.mm,47.44763695261559.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-6.091062472885142.mm, 11.174603174603135.mm, 7.787306941821903.mm)
  circle = ge.add_circle([1301.5749983342314.mm,-292.0952380952381.mm,48.69870124300441.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.1477544109268365.mm, 11.174603174603249.mm, 9.819666555791706.mm)
  circle = ge.add_circle([1295.4839358613463.mm,-280.92063492063494.mm,56.48600818482631.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(7.722753666748758.mm, 11.174603174603135.mm, 6.172703399439527.mm)
  circle = ge.add_circle([1296.631690272273.mm,-269.7460317460317.mm,66.30567474061802.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.831205051525103.mm, 11.174603174603135.mm, -1.0443173318518006.mm)
  circle = ge.add_circle([1304.3544439390218.mm,-258.57142857142856.mm,72.47837814005754.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(6.253660237591021.mm, 11.174603174603135.mm, -7.65734451931656.mm)
  circle = ge.add_circle([1314.185648990547.mm,-247.39682539682542.mm,71.43406080820574.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-0.9407645165540544.mm, 11.174603174603249.mm, -9.841654006269906.mm)
  circle = ge.add_circle([1320.439309228138.mm,-236.22222222222229.mm,63.77671628888918.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-7.591086748478347.mm, 11.174603174603135.mm, -6.333924015317287.mm)
  circle = ge.add_circle([1319.498544711584.mm,-225.04761904761904.mm,53.93506228261928.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.851012262023687.mm, 11.174603174603249.mm, 0.837107441250204.mm)
  circle = ge.add_circle([1311.9074579631056.mm,-213.8730158730159.mm,47.60113826730199.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-6.413485837403641.mm, 11.174603174603135.mm, 7.52398769723591.mm)
  circle = ge.add_circle([1302.0564457010819.mm,-202.69841269841265.mm,48.438245708552195.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.7333575937109345.mm, 11.174603174603135.mm, 9.859278781659647.mm)
  circle = ge.add_circle([1295.6429598636782.mm,-191.52380952380952.mm,55.962233405788105.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(7.4560548018262125.mm, 11.174603174603135.mm, 6.492336886430067.mm)
  circle = ge.add_circle([1296.3763174573892.mm,-180.34920634920638.mm,65.82151218744775.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.866452649042685.mm, 11.174603174603249.mm, -0.6295264719886262.mm)
  circle = ge.add_circle([1303.8323722592154.mm,-169.17460317460325.mm,72.31384907387782.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.698824908258075.mm, 0.mm, -11.684322601889193.mm)
  circle = ge.add_circle([1313.698824908258.mm,-158.mm,71.68432260188919.mm], vec, 5.mm, 8)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 88.mm, 0.mm)
  circle = ge.add_circle([1308.mm,-158.mm,60.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.939000000000078.mm, 0.mm, 182.40000000000003.mm)
  circle = ge.add_circle([1308.mm,-70.mm,60.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.99496719611102.mm, 9.207730857270427.mm, 11.372464949587481.mm)
  circle = ge.add_circle([1310.939.mm,-70.mm,242.40000000000003.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.641549939327888.mm, -9.164298928050435.mm, 11.286205666047522.mm)
  circle = ge.add_circle([1301.944032803889.mm,-60.79226914272957.mm,253.77246494958752.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.941961640230147.mm, -9.189638245741236.mm, 11.164013009620362.mm)
  circle = ge.add_circle([1298.3024828645612.mm,-69.95656807078001.mm,265.05867061563504.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.331149549226211.mm, -3.85350347848248.mm, 11.077177355757726.mm)
  circle = ge.add_circle([1302.2444445047913.mm,-79.14620631652124.mm,276.2226836252554.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.381821324327575.mm, 3.7308654938301373.mm, 11.076360884556948.mm)
  circle = ge.add_circle([1311.5755940540175.mm,-82.99970979500372.mm,287.2998609810131.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.064413733362699.mm, 9.13855045261559.mm, 11.162039946562686.mm)
  circle = ge.add_circle([1320.957415378345.mm,-79.26884430117359.mm,298.3762218655701.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.518759265741437.mm, 9.214567274365436.mm, 11.284227147463753.mm)
  circle = ge.add_circle([1325.0218291117078.mm,-70.130293848558.mm,309.53826181213276.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.94347721629515.mm, 3.914565767164234.mm, 11.371635294704333.mm)
  circle = ge.add_circle([1321.5030698459664.mm,-60.91572657419256.mm,320.8224889595965.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.044818504160048.mm, -3.6692952732681263.mm, 11.373268200653058.mm)
  circle = ge.add_circle([1312.5595926296712.mm,-57.00116080702833.mm,332.19412425430085.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.763657984897236.mm, -9.112393969026904.mm, 11.288173185487892.mm)
  circle = ge.add_circle([1303.5147741255112.mm,-60.670456080296454.mm,343.5673924549539.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.818837868415585.mm, -9.239084900918641.mm, 11.16599689539538.mm)
  circle = ge.add_circle([1299.751116140614.mm,-69.78285004932336.mm,354.8555656404418.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.278843663565112.mm, -3.9754532825315323.mm, 11.078020157281628.mm)
  circle = ge.add_circle([1303.5699540090295.mm,-79.021934950242.mm,366.0215625358372.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.430849939616564.mm, 3.6075612299644035.mm, 11.075570889489313.mm)
  circle = ge.add_circle([1312.8487976725946.mm,-82.99738823277353.mm,377.0995826931188.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.18617227962045.mm, 9.085830645090851.mm, 11.160078058583224.mm)
  circle = ge.add_circle([1322.2796476122112.mm,-79.38982700280913.mm,388.1751535826081.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.395307892796609.mm, 9.263190030764278.mm, 11.282237983071923.mm)
  circle = ge.add_circle([1326.4658198918316.mm,-70.30399635771828.mm,399.33523164119134.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.890357760085635.mm, 4.036163306144211.mm, 11.370779384168145.mm)
  circle = ge.add_circle([1323.070511999035.mm,-61.040806326954.mm,410.61746962426326.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.093022237711466.mm, -3.54566612015401.mm, 11.374044904451864.mm)
  circle = ge.add_circle([1314.1801542389494.mm,-57.00464302080979.mm,421.9882490084314.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.8850615956996535.mm, -9.05886166677815.mm, 11.290129354414205.mm)
  circle = ge.add_circle([1305.087132001238.mm,-60.5503091409638.mm,433.3622939128833.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.695064406064148.mm, -9.286881587682458.mm, 11.167991249594081.mm)
  circle = ge.add_circle([1301.2020704055383.mm,-69.60917080774195.mm,444.6524232672975.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.22491300842762.mm, -4.096693127486546.mm, 11.078889138616319.mm)
  circle = ge.add_circle([1304.8971348116024.mm,-78.8960523954244.mm,455.82041451689156.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.478226639282411.mm, 3.4836127072631626.mm, 11.07480751163672.mm)
  circle = ge.add_circle([1314.12204782003.mm,-82.99274552291095.mm,466.8993036555079.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.307215534669922.mm, 9.031488238170581.mm, 11.158127696047075.mm)
  circle = ge.add_circle([1323.6002744593125.mm,-79.50913281564779.mm,477.9741111671446.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.271217867142468.mm, 9.310158513918111.mm, 11.280238528108043.mm)
  circle = ge.add_circle([1327.9074899939824.mm,-70.47764457747721.mm,489.1322388631917.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.835618313858731.mm, 4.157040044088305.mm, 11.369897370832405.mm)
  circle = ge.add_circle([1324.63627212684.mm,-61.167486063559096.mm,500.4124773912997.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.139569788267636.mm, -3.4214037617857045.mm, 11.374794922275669.mm)
  circle = ge.add_circle([1315.8006538129812.mm,-57.01044601947079.mm,511.7823747621321.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.005739090786619.mm, -9.003711581407579.mm, 11.292073823482497.mm)
  circle = ge.add_circle([1306.6610840247135.mm,-60.431849781256496.mm,523.1571696844078.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.5706633573449835.mm, -9.333019770228091.mm, 11.16999571605345.mm)
  circle = ge.add_circle([1302.655344933927.mm,-69.43556136266407.mm,534.4492435078903.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.1693672150584.mm, -4.21720136164538.mm, 11.079784144574205.mm)
  circle = ge.add_circle([1306.226008291272.mm,-78.76858113289217.mm,545.6192392239437.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.523942962524416.mm, 3.3590420611596414.mm, 11.07407088732748.mm)
  circle = ge.add_circle([1315.3953755063303.mm,-82.98578249453755.mm,556.6990233685179.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.427521881915709.mm, 8.975532936631367.mm, 11.15618920726115.mm)
  circle = ge.add_circle([1324.9193184688547.mm,-79.6267404333779.mm,567.7730942558454.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.14651134948258.mm, 9.355464335927678.mm, 11.278229139646442.mm)
  circle = ge.add_circle([1329.3468403507704.mm,-70.65120749674654.mm,578.9292834631066.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.779268653295503.mm, 4.2771743941400615.mm, 11.368989412211704.mm)
  circle = ge.add_circle([1326.2003290012879.mm,-61.29574316081886.mm,590.207512602753.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.184452843102463.mm, -3.296530389643003.mm, 11.375518120182392.mm)
  circle = ge.add_circle([1317.4210603479924.mm,-57.0185687666788.mm,601.5765020149647.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.125668918883548.mm, -8.946953561931686.mm, 11.294006245438482.mm)
  circle = ge.add_circle([1308.23660750489.mm,-60.3150991563218.mm,612.9520201351471.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.4456569385067723.mm, -9.377491208936064.mm, 11.17200993680433.mm)
  circle = ge.add_circle([1304.1109385860063.mm,-69.26205271825349.mm,624.2460263805856.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.112216203140633.mm, -4.336956463961059.mm, 11.08070501531995.mm)
  circle = ge.add_circle([1307.556595524513.mm,-78.63954392718955.mm,635.4180363173899.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.567990745061024.mm, 3.2338715381895327.mm, 11.073361148112099.mm)
  circle = ge.add_circle([1316.6688117276537.mm,-82.97650039115061.mm,646.4987413327099.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.547069836366063.mm, 8.917974733289725.mm, 11.154262938411762.mm)
  circle = ge.add_circle([1326.2368024727148.mm,-79.74262885296108.mm,657.572102480822.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.0212106106175725.mm, 9.399099405821133.mm, 11.276210176535074.mm)
  circle = ge.add_circle([1330.7838723090808.mm,-70.82465411967135.mm,668.7263654192337.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.721318841639913.mm, 4.396544902022889.mm, 11.36805567045485.mm)
  circle = ge.add_circle([1327.7626616984633.mm,-61.42555471385022.mm,680.0025755957688.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.227663386743643.mm, -3.171068304324052.mm, 11.37621436901884.mm)
  circle = ge.add_circle([1319.0413428568233.mm,-57.02900981182733.mm,691.3706312662237.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.244829662238772.mm, -8.888597744520972.mm, 11.295926275179227.mm)
  circle = ge.add_circle([1309.8136794700797.mm,-60.20007811615138.mm,702.7468456352425.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.3200674739075566.mm, -9.4202879618435.mm, 11.174033552135825.mm)
  circle = ge.add_circle([1305.568849807841.mm,-69.08867586067235.mm,714.0427719104217.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.053470179027954.mm, -4.455937047885172.mm, 11.081651586399289.mm)
  circle = ge.add_circle([1308.8889172817485.mm,-78.50896382251585.mm,725.2168054625575.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.610362120588889.mm, 3.108123492017853.mm, 11.072678420739976.mm)
  circle = ge.add_circle([1317.9423874607764.mm,-82.96490087040102.mm,736.2984570489568.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.665838048465275.mm, 8.858823907217442.mm, 11.152349233502946.mm)
  circle = ge.add_circle([1327.5527495813653.mm,-79.85677737838317.mm,747.3711354696968.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.895338027466778.mm, 9.44105593099924.mm, 11.274181999331745.mm)
  circle = ge.add_circle([1332.2185876298306.mm,-70.99795347116573.mm,758.5234847031998.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.661779227899387.mm, 4.515130249871426.mm, 11.36709631231463.mm)
  circle = ge.add_circle([1329.3232496023638.mm,-61.55689754016649.mm,769.7976667025315.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.26919370240671.mm, -3.0450399115628954.mm, 11.376883544444922.mm)
  circle = ge.add_circle([1320.6614703744644.mm,-57.04176729029506.mm,781.1647630148461.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.363200040447055.mm, -8.828654550689528.mm, 11.297833569814998.mm)
  circle = ge.add_circle([1311.3922766720577.mm,-60.08680720185796.mm,792.541646559291.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.1939173920288795.mm, -9.461402386062474.mm, 11.17606620065908.mm)
  circle = ge.add_circle([1307.0290766316107.mm,-68.91546175254749.mm,803.839480129106.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.99313963392001.mm, -4.5741218651873226.mm, 11.08262368876808.mm)
  circle = ge.add_circle([1310.2229940236396.mm,-78.37686413860996.mm,815.0155463297651.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.65104952218644.mm, 2.9818203794469866.mm, 11.07202282713638.mm)
  circle = ge.add_circle([1319.2161336575596.mm,-82.95098600379728.mm,826.0981700185332.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.783805307909915.mm, 8.798091021906075.mm, 11.150448434295186.mm)
  circle = ge.add_circle([1328.867183179746.mm,-79.9691656243503.mm,837.1701928456696.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.7689160790737333.mm, 9.481326418626622.mm, 11.272144970240106.mm)
  circle = ge.add_circle([1333.650988487656.mm,-71.17107460244422.mm,848.3206412799648.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.600660444996947.mm, 4.63290926003878.mm, 11.366111509118582.mm)
  circle = ge.add_circle([1330.8820724085822.mm,-61.6897481838176.mm,859.5927862502049.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.3090363733711.mm, -2.9184677182276957.mm, 11.377525526955651.mm)
  circle = ge.add_circle([1322.2814119635852.mm,-57.05683892377882.mm,870.9588977593235.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.480758914252874.mm, -8.767134685434584.mm, 11.299727788730138.mm)
  circle = ge.add_circle([1312.9723755902141.mm,-59.975306642006515.mm,882.3364232862791.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.067229221471962.mm, -9.500827139144917.mm, 11.178107519372134.mm)
  circle = ge.add_circle([1308.4916166759613.mm,-68.7424413274411.mm,893.6361510750093.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.931235341988668.mm, -4.691489809749541.mm, 11.083621148822886.mm)
  circle = ge.add_circle([1311.5588458974332.mm,-78.24326846658602.mm,904.8142585943814.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.690045683665176.mm, 2.8549847564063526.mm, 11.071394484381017.mm)
  circle = ge.add_circle([1320.490081239422.mm,-82.93475827633556.mm,915.8978797432043.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.900950547435059.mm, 8.735786923380218.mm, 11.148560880243735.mm)
  circle = ge.add_circle([1330.180126923087.mm,-80.0797735199292.mm,926.9692742275853.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.641967342589851.mm, 9.519903676970202.mm, 11.270099453044168.mm)
  circle = ge.add_circle([1335.0810774705221.mm,-71.34398659654899.mm,938.117835107829.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.537973407873551.mm, 4.749860898878353.mm, 11.365101436738655.mm)
  circle = ge.add_circle([1332.4391101279323.mm,-61.824082919578785.mm,949.3879345608732.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.347184284305058.mm, -2.791374328301835.mm, 11.37814020190217.mm)
  circle = ge.add_circle([1323.9011367200587.mm,-57.07422202070043.mm,960.7530359976118.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.597485289323004.mm, -8.704049135324091.mm, 11.301608593644005.mm)
  circle = ge.add_circle([1314.5539524357537.mm,-59.86559634900227.mm,972.131176199514.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.9400255869313696.mm, -9.538555180393715.mm, 11.180157143724728.mm)
  circle = ge.add_circle([1309.9564671464307.mm,-68.56964548432636.mm,983.432784793158.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.867768358456487.mm, -4.808019921335756.mm, 11.084643788431663.mm)
  circle = ge.add_circle([1312.896492733362.mm,-78.10820066472007.mm,994.6129419368827.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.727343640867957.mm, 2.727639273923998.mm, 11.070793504686776.mm)
  circle = ge.add_circle([1321.7642610918185.mm,-82.91622058605583.mm,1005.6975857253144.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.017252846576184.mm, 8.671922738260733.mm, 11.146686908438937.mm)
  circle = ge.add_circle([1331.4916047326865.mm,-80.18858131213183.mm,1016.7683792300012.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.514514489243311.mm, 9.556780816683371.mm, 11.268045813044182.mm)
  circle = ge.add_circle([1336.5088575792627.mm,-71.5166585738711.mm,1027.9150661384401.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.473729311537227.mm, 4.8659642805003.mm, 11.36406627555948.mm)
  circle = ge.add_circle([1333.9943430900194.mm,-61.959877757187726.mm,1039.1831119514843.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.383630622538476.mm, -2.6637824388469085.mm, 11.37872745951222.mm)
  circle = ge.add_circle([1325.5206137784821.mm,-57.093913476687426.mm,1050.5471782270438.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.713358319995223.mm, -8.639409166534925.mm, 11.303475648672247.mm)
  circle = ge.add_circle([1316.1369831559437.mm,-59.757695915534335.mm,1061.925905686556.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.8123292051570843.mm, -9.57457977212053.mm, 11.182214707683215.mm)
  circle = ge.add_circle([1311.4236248359484.mm,-68.39710508206926.mm,1073.2293813352283.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.802750017616972.mm, -4.923691389334692.mm, 11.085691424965262.mm)
  circle = ge.add_circle([1314.2359540411055.mm,-77.97168485418979.mm,1084.4115960429115.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.762936732914568.mm, 2.599806674081691.mm, 11.070219995380057.mm)
  circle = ge.add_circle([1323.0387040587225.mm,-82.89537624352448.mm,1095.4972874678767.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.1326914354062865.mm, 8.606509871777604.mm, 11.14482685354551.mm)
  circle = ge.add_circle([1332.801640791637.mm,-80.29556956944279.mm,1106.5675074632568.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.3865802802918097.mm, 9.591951252036644.mm, 11.265984416990932.mm)
  circle = ge.add_circle([1337.9343322270433.mm,-71.68905969766519.mm,1117.7123343168023.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.40793962906423.mm, 4.981198670501122.mm, 11.36300621044552.mm)
  circle = ge.add_circle([1335.5477519467515.mm,-62.09710844562854.mm,1128.9783187337932.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.418368879275704.mm, -2.5357148359493635.mm, 11.37928719490992.mm)
  circle = ge.add_circle([1327.1398123176873.mm,-57.11590977512742.mm,1140.3413249442387.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.828357313004972.mm, -8.57322632284091.mm, 11.305328620385353.mm)
  circle = ge.add_circle([1317.7214434384116.mm,-59.651624611076784.mm,1151.7206121391487.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.6841628808961104.mm, -9.60889448084859.mm, 11.184279843796048.mm)
  circle = ge.add_circle([1312.8930861254066.mm,-68.2248509339177.mm,1163.025940759534.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.736191930817768.mm, -5.038483556476592.mm, 11.086763871330959.mm)
  circle = ge.add_circle([1315.5772490063027.mm,-77.83374541476628.mm,1174.21022060333.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.796818603386555.mm, 2.4715097859532733.mm, 11.069674058881446.mm)
  circle = ge.add_circle([1324.3134409371205.mm,-82.87222897124288.mm,1185.296984474661.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.2472456982441145.mm, 8.539560005733222.mm, 11.142981047742751.mm)
  circle = ge.add_circle([1334.110259540507.mm,-80.4007191852896.mm,1196.3666585335425.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.258187562953708.mm, 9.62540870209304.mm, 11.263915633020133.mm)
  circle = ge.add_circle([1339.3575052387512.mm,-71.86115917955638.mm,1207.5096395812852.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.340616109551547.mm, 5.0955434896672.mm, 11.361921430709344.mm)
  circle = ge.add_circle([1337.0993176757975.mm,-62.23575047746334.mm,1218.7735552143054.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.451392850761522.mm, -2.4071943906512985.mm, 11.379819308134756.mm)
  circle = ge.add_circle([1328.758701566246.mm,-57.14020698779614.mm,1230.1354766450147.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.942461731176081.mm, -8.5055124235516.mm, 11.307167177868905.mm)
  circle = ge.add_circle([1319.3073087154844.mm,-59.54740137844744.mm,1241.5152959531495.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.555549502820895.mm, -9.641493178461275.mm, 11.186352183259942.mm)
  circle = ge.add_circle([1314.3648469843083.mm,-68.05291380199904.mm,1252.8224631310184.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.668105984379508.mm, -5.152375922522495.mm, 11.087860936004745.mm)
  circle = ge.add_circle([1316.9203964871292.mm,-77.69440698046031.mm,1264.0088153142783.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.828983201467508.mm, 2.342771521527908.mm, 11.069155792688207.mm)
  circle = ge.add_circle([1325.5885024715087.mm,-82.84678290298281.mm,1275.096676250283.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.36089517733717.mm, 8.471085096415933.mm, 11.141149820664168.mm)
  circle = ge.add_circle([1335.4174856729762.mm,-80.5040113814549.mm,1286.1658320429713.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.1293592663328127.mm, 9.65714719183076.mm, 11.261839830587405.mm)
  circle = ge.add_circle([1340.7783808503134.mm,-72.03292628503897.mm,1297.3069818636354.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.271770776016183.mm, 5.208978317649283.mm, 11.360812130077647.mm)
  circle = ge.add_circle([1338.6490215839806.mm,-62.37577909320821.mm,1308.5688216942228.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.482696639387086.mm, -2.278244054865965.mm, 11.3803237041584.mm)
  circle = ge.add_circle([1330.3772508079644.mm,-57.166800775558926.mm,1319.9296338243005.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.05565119709172.mm, -8.436279561400454.mm, 11.308990992783038.mm)
  circle = ge.add_circle([1320.8945541685773.mm,-59.44504483042489.mm,1331.3099575284589.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.4265120394416044.mm, -9.672370043297946.mm, 11.188431355983994.mm)
  circle = ge.add_circle([1315.8389029714856.mm,-67.88132439182534.mm,1342.618948521242.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.598504337479199.mm, -5.265348147924811.mm, 11.088982423067591.mm)
  circle = ge.add_circle([1318.2654150109272.mm,-77.55369443512329.mm,1353.807379877226.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.859424783019449.mm, 2.2136148716182618.mm, 11.068665289353476.mm)
  circle = ge.add_circle([1326.8639193484064.mm,-82.8190425830481.mm,1364.8963623002935.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.473619576514466.mm, 8.401097372465173.mm, 11.139333499342229.mm)
  circle = ge.add_circle([1336.7233441314258.mm,-80.60542771142984.mm,1375.965027589647.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.0001183973201933.mm, 9.687161053209408.mm, 11.259757380400742.mm)
  circle = ge.add_circle([1342.1969637079403.mm,-72.20433033896467.mm,1387.1043610889892.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.201415923250579.mm, 5.321482896609602.mm, 11.359678506654745.mm)
  circle = ge.add_circle([1340.1968453106201.mm,-62.51716928575526.mm,1398.36411846939.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.512274654742441.mm, -2.1488868572789173.mm, 11.380800292904041.mm)
  circle = ge.add_circle([1331.9954293873695.mm,-57.195686389145656.mm,1409.7237969760447.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.167905496733056.mm, -8.365540100386568.mm, 11.310799739420418.mm)
  circle = ge.add_circle([1322.483154732627.mm,-59.344573246424574.mm,1421.1045972689487.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.29707353500271.mm, -9.701519561192043.mm, 11.190516990657898.mm)
  circle = ge.add_circle([1317.315249235894.mm,-67.71011334681114.mm,1432.4153970083692.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.527399419975836.mm, -5.377380057459916.mm, 11.090128132237169.mm)
  circle = ge.add_circle([1319.6123227708968.mm,-77.41163290800318.mm,1443.605913999027.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.888137911611466.mm, 2.0840629017546064.mm, 11.06820263647569.mm)
  circle = ge.add_circle([1328.1397221908726.mm,-82.7890129654631.mm,1454.6960421312642.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.585398764810179.mm, 8.329609332687397.mm, 11.137532408144807.mm)
  circle = ge.add_circle([1338.027860102484.mm,-80.7049500637085.mm,1465.76424476774.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.870488036486222.mm, 9.715444926182656.mm, 11.257668654356394.mm)
  circle = ge.add_circle([1343.6132588672942.mm,-72.3753407310211.mm,1476.9017771758847.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.129564115624817.mm, 5.433037134839523.mm, 11.358520762890521.mm)
  circle = ge.add_circle([1341.742770830808.mm,-62.65989580483844.mm,1488.159445830241.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.540121614618556.mm, -2.019145899235511.mm, 11.381248989258438.mm)
  circle = ge.add_circle([1333.6132067151832.mm,-57.22685866999892.mm,1499.5179665931316.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.279204583086084.mm, -8.293306673565766.mm, 11.31259309476468.mm)
  circle = ge.add_circle([1324.0730851005646.mm,-59.24600456923443.mm,1510.89921558239.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.167257105370254.mm, -9.728936526456565.mm, 11.192608714817425.mm)
  circle = ge.add_circle([1318.7938805174786.mm,-67.5393112428002.mm,1522.2118086771547.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.454803930189655.mm, -5.488451643831226.mm, 11.0912978589065.mm)
  circle = ge.add_circle([1320.9611376228488.mm,-77.26824776925676.mm,1533.4044173919722.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.915117459490148.mm, 1.95413874806583.mm, 11.06776791667744.mm)
  circle = ge.add_circle([1329.4159415530385.mm,-82.75669941308799.mm,1544.4957152508787.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.6962127800597955.mm, 8.256633743823883.mm, 11.135746868721526.mm)
  circle = ge.add_circle([1339.3310590125286.mm,-80.80256066502216.mm,1555.5634831675561.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.740491333959426.mm, 9.741993759655351.mm, 11.255574025470878.mm)
  circle = ge.add_circle([1345.0272717925884.mm,-72.54592692119827.mm,1566.6992300362776.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.056228184843803.mm, 5.543621110347708.mm, 11.357339105540632.mm)
  circle = ge.add_circle([1343.286780458629.mm,-62.80393316154292.mm,1577.9548040617485.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.566232545945468.mm, -1.8890443506149097.mm, 11.381669713091696.mm)
  circle = ge.add_circle([1335.2305522737852.mm,-57.260312051195214.mm,1589.3121431672892.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.389528579727994.mm, -8.21959218079509.mm, 11.314370738548405.mm)
  circle = ge.add_circle([1325.6643197278397.mm,-59.149356401810124.mm,1600.6938128803808.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.0370859339018352.mm, -9.754616042813709.mm, 11.194706154910364.mm)
  circle = ge.add_circle([1320.2747911481117.mm,-67.36894858260521.mm,1612.0081836189293.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.380730832637482.mm, -5.598543071242105.mm, 11.092491394178978.mm)
  circle = ge.add_circle([1322.3118770820136.mm,-77.12356462541892.mm,1623.2028897738396.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.94035860849317.mm, 1.8238656131472624.mm, 11.067361207593422.mm)
  circle = ge.add_circle([1330.692607914651.mm,-82.72210769666103.mm,1634.2953811680186.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.806041832466008.mm, 8.182183638271212.mm, 11.133977199943729.mm)
  circle = ge.add_circle([1340.6329665231442.mm,-80.89824208351376.mm,1645.362742375612.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.6101515052912418.mm, 9.76680281238555.mm, 11.253473867815046.mm)
  circle = ge.add_circle([1346.4390083556102.mm,-72.71605844524255.mm,1656.4967195755557.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-7.981421227656256.mm, 5.653215074417858.mm, 11.356133745633088.mm)
  circle = ge.add_circle([1344.828856850319.mm,-62.949255632857.mm,1667.7501934433708.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.590602785685178.mm, -1.758605445692929.mm, 11.382062389268185.mm)
  circle = ge.add_circle([1336.8474356226627.mm,-57.296040558439145.mm,1679.1063271890039.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.498857784368965.mm, -8.144409786428518.mm, 11.316132353309285.mm)
  circle = ge.add_circle([1327.2568328369775.mm,-59.054646004132074.mm,1690.488389578272.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(12.693024947391677.mm, -2.8009442094394075.mm, -0.20452193158098453.mm)
  circle = ge.add_circle([1321.7579750526086.mm,-67.19905579056059.mm,1701.8045219315813.mm], vec, 5.mm, 8)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.938999999999851.mm, 0.mm, 182.39999999999964.mm)
  circle = ge.add_circle([1334.4510000000002.mm,-70.mm,1701.6000000000004.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.8329999999998563.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1337.39.mm,-70.mm,1884.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (-) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (-) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.277000000000044.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1339.223.mm,-70.mm,1884.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Solar Array"
  inst.layer = model.layers["Solar Array"]

  # ═══ Chemistry Shelf ═══
  defn = model.definitions.add("Chemistry Shelf")
  ents = defn.entities
  # Chem Shelf (board, deployed)
  grp = ents.add_group
  grp.name = "Chem Shelf (board, deployed)"
  face = grp.entities.add_face([1180.mm,0.mm,1053.mm], [1780.mm,0.mm,1053.mm], [1780.mm,300.mm,1053.mm], [1180.mm,300.mm,1053.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Chem Shelf (board, deployed)"] || model.materials.add("Chem Shelf (board, deployed)")
  mat.color = Sketchup::Color.new(200, 176, 106)
  mat.alpha = 1.0
  grp.material = mat

  # Chem Shelf lip (front)
  grp = ents.add_group
  grp.name = "Chem Shelf lip (front)"
  face = grp.entities.add_face([1180.mm,294.mm,1075.mm], [1780.mm,294.mm,1075.mm], [1780.mm,300.mm,1075.mm], [1180.mm,300.mm,1075.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Chem Shelf (board, deployed)"] || model.materials.add("Chem Shelf (board, deployed)")
  mat.color = Sketchup::Color.new(200, 176, 106)
  mat.alpha = 1.0
  grp.material = mat

  # Chem Shelf lip (end)
  grp = ents.add_group
  grp.name = "Chem Shelf lip (end)"
  face = grp.entities.add_face([1180.mm,0.mm,1075.mm], [1186.mm,0.mm,1075.mm], [1186.mm,300.mm,1075.mm], [1180.mm,300.mm,1075.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Chem Shelf (board, deployed)"] || model.materials.add("Chem Shelf (board, deployed)")
  mat.color = Sketchup::Color.new(200, 176, 106)
  mat.alpha = 1.0
  grp.material = mat

  # Chem Shelf lip (end)
  grp = ents.add_group
  grp.name = "Chem Shelf lip (end)"
  face = grp.entities.add_face([1774.mm,0.mm,1075.mm], [1780.mm,0.mm,1075.mm], [1780.mm,300.mm,1075.mm], [1774.mm,300.mm,1075.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Chem Shelf (board, deployed)"] || model.materials.add("Chem Shelf (board, deployed)")
  mat.color = Sketchup::Color.new(200, 176, 106)
  mat.alpha = 1.0
  grp.material = mat

  # Chem Shelf piano hinge
  grp = ents.add_group
  grp.name = "Chem Shelf piano hinge"
  ge = grp.entities
  circle = ge.add_circle([1180.mm,0.mm,1069.mm], [1,0,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(600.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Chem Shelf stay
  grp = ents.add_group
  grp.name = "Chem Shelf stay"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 290.mm, -230.mm)
  circle = ge.add_circle([1205.mm,0.mm,1305.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Chem Shelf stay anchor
  grp = ents.add_group
  grp.name = "Chem Shelf stay anchor"
  face = grp.entities.add_face([1193.mm,0.mm,1293.mm], [1217.mm,0.mm,1293.mm], [1217.mm,8.mm,1293.mm], [1193.mm,8.mm,1293.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Chem Shelf stay
  grp = ents.add_group
  grp.name = "Chem Shelf stay"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 290.mm, -230.mm)
  circle = ge.add_circle([1755.mm,0.mm,1305.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Chem Shelf stay anchor
  grp = ents.add_group
  grp.name = "Chem Shelf stay anchor"
  face = grp.entities.add_face([1743.mm,0.mm,1293.mm], [1767.mm,0.mm,1293.mm], [1767.mm,8.mm,1293.mm], [1743.mm,8.mm,1293.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Chemistry Shelf"
  inst.layer = model.layers["Shelf"]

  # ═══ Light-Trap Door Frame ═══
  defn = model.definitions.add("Light-Trap Door Frame")
  ents = defn.entities
  # Door Frame threshold
  grp = ents.add_group
  grp.name = "Door Frame threshold"
  face = grp.entities.add_face([-50.mm,0.mm,0.mm], [0.mm,0.mm,0.mm], [0.mm,2362.mm,0.mm], [-50.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Door Frame threshold"] || model.materials.add("Door Frame threshold")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame top
  grp = ents.add_group
  grp.name = "Door Frame top"
  face = grp.entities.add_face([-50.mm,0.mm,2338.mm], [0.mm,0.mm,2338.mm], [0.mm,2362.mm,2338.mm], [-50.mm,2362.mm,2338.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Door Frame threshold"] || model.materials.add("Door Frame threshold")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame left stile
  grp = ents.add_group
  grp.name = "Door Frame left stile"
  face = grp.entities.add_face([-50.mm,0.mm,0.mm], [0.mm,0.mm,0.mm], [0.mm,50.mm,0.mm], [-50.mm,50.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Door Frame threshold"] || model.materials.add("Door Frame threshold")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame right stile
  grp = ents.add_group
  grp.name = "Door Frame right stile"
  face = grp.entities.add_face([-50.mm,2312.mm,0.mm], [0.mm,2312.mm,0.mm], [0.mm,2362.mm,0.mm], [-50.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Door Frame threshold"] || model.materials.add("Door Frame threshold")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame bottom seal lip
  grp = ents.add_group
  grp.name = "Door Frame bottom seal lip"
  face = grp.entities.add_face([-32.mm,0.mm,0.mm], [-20.mm,0.mm,0.mm], [-20.mm,2362.mm,0.mm], [-32.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(110.mm)
  mat = model.materials["Door Frame threshold"] || model.materials.add("Door Frame threshold")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame top seal lip
  grp = ents.add_group
  grp.name = "Door Frame top seal lip"
  face = grp.entities.add_face([-32.mm,0.mm,2270.mm], [-20.mm,0.mm,2270.mm], [-20.mm,2362.mm,2270.mm], [-32.mm,2362.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(118.mm)
  mat = model.materials["Door Frame threshold"] || model.materials.add("Door Frame threshold")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Housing surround seal bottom
  grp = ents.add_group
  grp.name = "Housing surround seal bottom"
  face = grp.entities.add_face([-20.mm,713.mm,130.mm], [0.mm,713.mm,130.mm], [0.mm,1649.mm,130.mm], [-20.mm,1649.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Housing surround seal bottom"] || model.materials.add("Housing surround seal bottom")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Housing surround seal top
  grp = ents.add_group
  grp.name = "Housing surround seal top"
  face = grp.entities.add_face([-20.mm,713.mm,2210.mm], [0.mm,713.mm,2210.mm], [0.mm,1649.mm,2210.mm], [-20.mm,1649.mm,2210.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Housing surround seal bottom"] || model.materials.add("Housing surround seal bottom")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Housing surround seal left
  grp = ents.add_group
  grp.name = "Housing surround seal left"
  face = grp.entities.add_face([-20.mm,713.mm,130.mm], [0.mm,713.mm,130.mm], [0.mm,753.mm,130.mm], [-20.mm,753.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2120.mm)
  mat = model.materials["Housing surround seal bottom"] || model.materials.add("Housing surround seal bottom")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Housing surround seal right
  grp = ents.add_group
  grp.name = "Housing surround seal right"
  face = grp.entities.add_face([-20.mm,1609.mm,130.mm], [0.mm,1609.mm,130.mm], [0.mm,1649.mm,130.mm], [-20.mm,1649.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2120.mm)
  mat = model.materials["Housing surround seal bottom"] || model.materials.add("Housing surround seal bottom")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Light-Trap Door Frame"
  inst.layer = model.layers["Light Seal"]

  # ═══ Light Seal & Hinges ═══
  defn = model.definitions.add("Light Seal & Hinges")
  ents = defn.entities
  # EPDM Seal Bottom
  grp = ents.add_group
  grp.name = "EPDM Seal Bottom"
  face = grp.entities.add_face([-20.mm,0.mm,130.mm], [0.mm,0.mm,130.mm], [0.mm,2362.mm,130.mm], [-20.mm,2362.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["EPDM Seal Bottom"] || model.materials.add("EPDM Seal Bottom")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM Seal Top
  grp = ents.add_group
  grp.name = "EPDM Seal Top"
  face = grp.entities.add_face([-20.mm,0.mm,2348.mm], [0.mm,0.mm,2348.mm], [0.mm,2362.mm,2348.mm], [-20.mm,2362.mm,2348.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["EPDM Seal Bottom"] || model.materials.add("EPDM Seal Bottom")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM Seal Left
  grp = ents.add_group
  grp.name = "EPDM Seal Left"
  face = grp.entities.add_face([-20.mm,0.mm,130.mm], [0.mm,0.mm,130.mm], [0.mm,40.mm,130.mm], [-20.mm,40.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2258.mm)
  mat = model.materials["EPDM Seal Bottom"] || model.materials.add("EPDM Seal Bottom")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM Seal Right
  grp = ents.add_group
  grp.name = "EPDM Seal Right"
  face = grp.entities.add_face([-20.mm,2322.mm,130.mm], [0.mm,2322.mm,130.mm], [0.mm,2362.mm,130.mm], [-20.mm,2362.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2258.mm)
  mat = model.materials["EPDM Seal Bottom"] || model.materials.add("EPDM Seal Bottom")
  mat.color = Sketchup::Color.new(90, 48, 32)
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
  face = grp.entities.add_face([4424.mm,881.mm,2348.mm], [4724.mm,881.mm,2348.mm], [4724.mm,1481.mm,2348.mm], [4424.mm,1481.mm,2348.mm])
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
  circle = ge.add_circle([1470.mm,65.mm,1180.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1200.1379310344828.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1220.2758620689656.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1240.4137931034484.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1260.551724137931.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1280.6896551724137.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1300.8275862068965.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1320.9655172413793.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1341.103448275862.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1361.2413793103449.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1381.3793103448277.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1401.5172413793102.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1421.655172413793.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1441.7931034482758.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1461.9310344827586.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1482.0689655172414.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1502.2068965517242.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1522.344827586207.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1542.4827586206898.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1562.6206896551723.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1582.7586206896551.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1602.896551724138.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1623.0344827586207.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1643.1724137931035.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1663.310344827586.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1683.4482758620688.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1703.5862068965516.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1723.7241379310344.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1743.8620689655172.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1764.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1784.1379310344828.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1804.2758620689656.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1824.4137931034484.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1844.5517241379312.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1864.6896551724137.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1884.8275862068965.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1904.9655172413793.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1925.103448275862.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1945.2413793103447.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1965.3793103448274.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1985.5172413793102.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2005.655172413793.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2025.7931034482758.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2045.9310344827586.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2066.0689655172414.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2086.206896551724.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2106.344827586207.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2126.4827586206898.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2146.620689655172.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2166.758620689655.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2186.8965517241377.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2207.0344827586205.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2227.1724137931033.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2247.310344827586.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2267.448275862069.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2287.5862068965516.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2307.7241379310344.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,2327.862068965517.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord Knob
  grp = ents.add_group
  grp.name = "Pull Cord Knob"
  ge = grp.entities
  circle = ge.add_circle([1470.mm,65.mm,1164.mm], [0,0,1], 6.mm, 10)
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
  circle = ge.add_circle([1550.mm,65.mm,1180.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1200.1379310344828.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1220.2758620689656.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1240.4137931034484.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1260.551724137931.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1280.6896551724137.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1300.8275862068965.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1320.9655172413793.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1341.103448275862.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1361.2413793103449.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1381.3793103448277.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1401.5172413793102.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1421.655172413793.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1441.7931034482758.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1461.9310344827586.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1482.0689655172414.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1502.2068965517242.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1522.344827586207.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1542.4827586206898.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1562.6206896551723.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1582.7586206896551.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1602.896551724138.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1623.0344827586207.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1643.1724137931035.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1663.310344827586.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1683.4482758620688.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1703.5862068965516.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1723.7241379310344.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1743.8620689655172.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1764.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1784.1379310344828.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1804.2758620689656.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1824.4137931034484.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1844.5517241379312.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1864.6896551724137.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1884.8275862068965.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1904.9655172413793.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1925.103448275862.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1945.2413793103447.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1965.3793103448274.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1985.5172413793102.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2005.655172413793.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2025.7931034482758.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2045.9310344827586.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2066.0689655172414.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2086.206896551724.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2106.344827586207.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2126.4827586206898.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2146.620689655172.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2166.758620689655.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2186.8965517241377.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2207.0344827586205.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2227.1724137931033.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2247.310344827586.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2267.448275862069.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2287.5862068965516.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2307.7241379310344.mm], [0,0,1], 3.5.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord
  grp = ents.add_group
  grp.name = "Pull Cord"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,2327.862068965517.mm], [0,0,1], 2.mm, 8)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.137931034482758.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pull Cord Knob
  grp = ents.add_group
  grp.name = "Pull Cord Knob"
  ge = grp.entities
  circle = ge.add_circle([1550.mm,65.mm,1164.mm], [0,0,1], 6.mm, 10)
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
  circle = ge.add_circle([4574.mm,40.mm,2350.mm], [0,1,0], 7.mm, 24)
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
  circle = ge.add_circle([4874.mm,40.mm,2350.mm], [0,1,0], 7.mm, 24)
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
  face = grp.entities.add_face([4869.mm,1176.mm,2270.mm], [4879.mm,1176.mm,2270.mm], [4879.mm,1186.mm,2270.mm], [4869.mm,1186.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(93.mm)
  mat = model.materials["Cable Trunking (40x25 PVC)"] || model.materials.add("Cable Trunking (40x25 PVC)")
  mat.color = Sketchup::Color.new(154, 160, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Conduit to Fan A (exhaust, Cct A)
  grp = ents.add_group
  grp.name = "Conduit to Fan A (exhaust, Cct A)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 1147.mm, 0.mm)
  circle = ge.add_circle([5618.mm,20.mm,2358.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cable Trunking (40x25 PVC)"] || model.materials.add("Cable Trunking (40x25 PVC)")
  mat.color = Sketchup::Color.new(154, 160, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Conduit to Fan A (exhaust, Cct A) elbow
  grp = ents.add_group
  grp.name = "Conduit to Fan A (exhaust, Cct A) elbow"
  ge = grp.entities
  arc = ge.add_arc([5618.mm,1167.mm,2344.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 14.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5618.mm,1167.mm,2358.mm], [0.000000,1.000000,0.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Cable Trunking (40x25 PVC)"] || model.materials.add("Cable Trunking (40x25 PVC)")
  mat.color = Sketchup::Color.new(154, 160, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Conduit to Fan A (exhaust, Cct A)
  grp = ents.add_group
  grp.name = "Conduit to Fan A (exhaust, Cct A)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -244.mm)
  circle = ge.add_circle([5618.mm,1181.mm,2344.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cable Trunking (40x25 PVC)"] || model.materials.add("Cable Trunking (40x25 PVC)")
  mat.color = Sketchup::Color.new(154, 160, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Conduit to Fan B (intake, Cct B)
  grp = ents.add_group
  grp.name = "Conduit to Fan B (intake, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1713.mm)
  circle = ge.add_circle([300.mm,18.mm,2358.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cable Trunking (40x25 PVC)"] || model.materials.add("Cable Trunking (40x25 PVC)")
  mat.color = Sketchup::Color.new(154, 160, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B electrical box (Cct B — flex connector to fan, unplugged for swing)
  grp = ents.add_group
  grp.name = "Fan B electrical box (Cct B — flex connector to fan, unplugged for swing)"
  face = grp.entities.add_face([260.mm,0.mm,555.mm], [340.mm,0.mm,555.mm], [340.mm,60.mm,555.mm], [260.mm,60.mm,555.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Pull Switch (ceiling)"] || model.materials.add("Pull Switch (ceiling)")
  mat.color = Sketchup::Color.new(216, 216, 240)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-24.mm, 31.mm, 0.mm)
  circle = ge.add_circle([300.mm,55.mm,600.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.851511560266601.mm, 21.01868176094372.mm, -19.73157743024467.mm)
  circle = ge.add_circle([276.mm,86.mm,600.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.415285721407372.mm, -3.1878709732554427.mm, -8.26777556548791.mm)
  circle = ge.add_circle([284.8515115602666.mm,107.01868176094372.mm,580.2684225697553.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.50273106781765.mm, -3.2555705962828227.mm, 7.999501403076351.mm)
  circle = ge.add_circle([262.43622583885923.mm,103.83081078768828.mm,572.0006470042674.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-13.500283629993305.mm, 3.7140661297747783.mm, 19.61916723026559.mm)
  circle = ge.add_circle([239.93349477104158.mm,100.57524019140546.mm,580.0001484073438.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-0.6382537614751698.mm, 13.671766673143637.mm, 19.840340125280477.mm)
  circle = ge.add_circle([226.43321114104828.mm,104.28930632118023.mm,599.6193156376094.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.610678641132552.mm, 20.832230468710918.mm, 8.534521378108138.mm)
  circle = ge.add_circle([225.7949573795731.mm,117.96107299432387.mm,619.4596557628898.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.872998515546954.mm, 21.03531682309628.mm, -7.729748483022945.mm)
  circle = ge.add_circle([234.40563602070566.mm,138.7933034630348.mm,627.994177140998.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-0.003698733156397793.mm, 14.163035082164612.mm, -19.503130305068453.mm)
  circle = ge.add_circle([243.2786345362526.mm,159.82862028613107.mm,620.264428657975.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-12.862162052327875.mm, 4.2080957382899555.mm, -19.945435209911466.mm)
  circle = ge.add_circle([243.2749358030962.mm,173.99165536829568.mm,600.7612983529066.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.231783666317455.mm, -3.0458048660890995.mm, -8.799689531312879.mm)
  circle = ge.add_circle([230.41277375076834.mm,178.19975110658564.mm,580.8158631429951.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.668929577273758.mm, -3.3842404100552415.mm, 7.458566670834443.mm)
  circle = ge.add_circle([208.18099008445088.mm,175.15394624049654.mm,572.0161736116822.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-13.91962343044716.mm, 3.3894159616814363.mm, 19.38348810480136.mm)
  circle = ge.add_circle([185.51206050717713.mm,171.7697058304413.mm,579.4747402825167.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.0671036276280574.mm, 13.339753873541468.mm, 20.046843256656985.mm)
  circle = ge.add_circle([171.59243707672996.mm,175.15912179212273.mm,598.858228387318.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.421475164849738.mm, 20.68575035804028.mm, 9.063231007117906.mm)
  circle = ge.add_circle([170.5253334491019.mm,188.4988756656642.mm,618.905071643975.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.033366303204417.mm, 21.159472529669813.mm, -7.186006096157257.mm)
  circle = ge.add_circle([178.94680861395165.mm,209.18462602370448.mm,627.9683026510929.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.41306862197197347.mm, 14.48569367968338.mm, -19.26026274607011.mm)
  circle = ge.add_circle([187.98017491715606.mm,230.3440985533743.mm,620.7822965549357.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-12.431131796185184.mm, 4.5417965817552215.mm, -20.14454551960796.mm)
  circle = ge.add_circle([188.39324353912804.mm,244.82979223305767.mm,601.5220338088656.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.036913744282288.mm, -2.894937829674717.mm, -9.325097088240682.mm)
  circle = ge.add_circle([175.96211174294285.mm,249.3715888148129.mm,581.3774882892576.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.823436998148622.mm, -3.503859058474518.mm, 6.912117143510841.mm)
  circle = ge.add_circle([153.92519799866056.mm,246.47665098513818.mm,572.0523912010169.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-14.333741298209489.mm, 3.0688085801880334.mm, 19.13347700784925.mm)
  circle = ge.add_circle([131.10176100051194.mm,242.97279192666366.mm,578.9645083445278.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.5002345951338327.mm, 13.004426672891782.mm, 20.238523937893206.mm)
  circle = ge.add_circle([116.76801970230245.mm,246.0416005068517.mm,598.097985352377.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.220974819980398.mm, 20.530524284593128.mm, 9.585239367105373.mm)
  circle = ge.add_circle([115.26778510716862.mm,259.0460271797435.mm,618.3365092902702.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.181984795637973.mm, 21.27453200768275.mm, -6.636950442973102.mm)
  circle = ge.add_circle([123.48875992714902.mm,279.5765514643366.mm,627.9217486573756.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.8244604501020376.mm, 14.804190578880878.mm, -19.003154327272227.mm)
  circle = ge.add_circle([132.670744722787.mm,300.85108347201935.mm,621.2847982144025.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.995980184272383.mm, 4.878688152268467.mm, -20.328761139016706.mm)
  circle = ge.add_circle([133.49520517288903.mm,315.65527405090023.mm,602.2816438871303.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.83082004031614.mm, -2.7353814137009635.mm, -9.843609754792169.mm)
  circle = ge.add_circle([121.49922498861665.mm,320.5339622031687.mm,581.9528827481136.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.96613908908708.mm, -3.614338096620429.mm, 6.360556860822271.mm)
  circle = ge.add_circle([99.6684049483005.mm,317.79858078946774.mm,572.1092729933214.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-14.742331038366345.mm, 2.7524810394214114.mm, 18.869318795297772.mm)
  circle = ge.add_circle([76.70226585921343.mm,314.1842426928473.mm,578.4698298541437.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(22.04006517915292.mm, 17.063276267731283.mm, 2.6608513505585734.mm)
  circle = ge.add_circle([61.95993482084708.mm,316.9367237322687.mm,597.3391486494414.mm], vec, 5.mm, 8)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-24.mm, 31.mm, 0.mm)
  circle = ge.add_circle([84.mm,334.mm,600.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
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
  face = grp.entities.add_face([720.5.mm,-445.mm,0.mm], [1279.5.mm,-445.mm,0.mm], [1279.5.mm,-140.mm,0.mm], [720.5.mm,-140.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(711.mm)
  mat = model.materials["Evap Cooler (on ground)"] || model.materials.add("Evap Cooler (on ground)")
  mat.color = Sketchup::Color.new(61, 170, 150)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E Inverter (12->120V AC)
  grp = ents.add_group
  grp.name = "Cct E Inverter (12->120V AC)"
  face = grp.entities.add_face([1910.mm,0.mm,1180.mm], [2030.mm,0.mm,1180.mm], [2030.mm,72.mm,1180.mm], [1910.mm,72.mm,1180.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(235.mm)
  mat = model.materials["Cct E Inverter (12->120V AC)"] || model.materials.add("Cct E Inverter (12->120V AC)")
  mat.color = Sketchup::Color.new(64, 72, 72)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E AC line (inverter -> panel GFCI)
  grp = ents.add_group
  grp.name = "Cct E AC line (inverter -> panel GFCI)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-445.22.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1970.mm,30.mm,1415.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E AC line (inverter -> panel GFCI) elbow
  grp = ents.add_group
  grp.name = "Cct E AC line (inverter -> panel GFCI) elbow"
  ge = grp.entities
  arc = ge.add_arc([1524.78.mm,30.mm,1429.mm], [0.000000,0.000000,-1.000000], [0.000000,1.000000,-0.000000], 14.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1524.78.mm,30.mm,1415.mm], [-1.000000,0.000000,0.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E AC line (inverter -> panel GFCI)
  grp = ents.add_group
  grp.name = "Cct E AC line (inverter -> panel GFCI)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 473.1199999999999.mm)
  circle = ge.add_circle([1510.78.mm,30.mm,1429.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E AC line (inverter -> panel GFCI) elbow
  grp = ents.add_group
  grp.name = "Cct E AC line (inverter -> panel GFCI) elbow"
  ge = grp.entities
  arc = ge.add_arc([1510.78.mm,24.119999999999997.mm,1902.12.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 5.880000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1510.78.mm,30.mm,1902.12.mm], [0.000000,0.000000,1.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E AC line (inverter -> panel GFCI)
  grp = ents.add_group
  grp.name = "Cct E AC line (inverter -> panel GFCI)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -6.120000000000001.mm, 0.mm)
  circle = ge.add_circle([1510.78.mm,24.12.mm,1908.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-31.12799999999993.mm, -22.25.mm, -126.70000000000005.mm)
  circle = ge.add_circle([1510.78.mm,-70.mm,1908.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.911534316695224.mm, -20.5689858849434.mm, -2.7709411168864335.mm)
  circle = ge.add_circle([1479.652.mm,-92.25.mm,1781.3.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.601367115128369.mm, 17.974514822995275.mm, -12.318342659127666.mm)
  circle = ge.add_circle([1457.7404656833048.mm,-112.8189858849434.mm,1778.5290588831135.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.3780366767048235.mm, 17.274166539123.mm, -16.12121662847312.mm)
  circle = ge.add_circle([1447.1390985681765.mm,-94.84447106194813.mm,1766.2107162239859.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.644135678089242.mm, 5.319172914605446.mm, -16.78966589105835.mm)
  circle = ge.add_circle([1452.5171352448813.mm,-77.57030452282513.mm,1750.0894995955127.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.581874568015564.mm, -10.870916144349266.mm, -13.931200655098792.mm)
  circle = ge.add_circle([1469.1612709229705.mm,-72.25113160821968.mm,1733.2998337044544.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.227810870736903.mm, -21.78985231133329.mm, -9.224210722310318.mm)
  circle = ge.add_circle([1485.743145490986.mm,-83.12204775256895.mm,1719.3686330493556.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.75135033095512.mm, -21.02642201700951.mm, -5.4324742910744135.mm)
  circle = ge.add_circle([1490.970956361723.mm,-104.91190006390224.mm,1710.1444223270453.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.97321009670509.mm, -9.02888455947803.mm, -4.782365038050102.mm)
  circle = ge.add_circle([1480.2196060307679.mm,-125.93832208091175.mm,1704.7119480359709.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.84868882177011.mm, 7.158229919310372.mm, -7.655604149330429.mm)
  circle = ge.add_circle([1458.2463959340628.mm,-134.96720664038978.mm,1699.9295829979208.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.45090099966069.mm, 18.03041966133452.mm, -12.365127125547133.mm)
  circle = ge.add_circle([1436.3977071122927.mm,-127.8089767210794.mm,1692.2739788485903.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.527775025430628.mm, 17.203918946520048.mm, -16.145668454706083.mm)
  circle = ge.add_circle([1425.946806112632.mm,-109.77855705974488.mm,1679.9088517230432.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.705225191709133.mm, 5.164019795705698.mm, -16.77742782858354.mm)
  circle = ge.add_circle([1431.4745811380626.mm,-92.57463811322484.mm,1663.7631832683371.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.518445642323286.mm, -11.019874359430347.mm, -13.889458461850836.mm)
  circle = ge.add_circle([1448.1798063297717.mm,-87.41061831751914.mm,1646.9857554397536.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.077106730059995.mm, -21.845152621146923.mm, -9.17747393948207.mm)
  circle = ge.add_circle([1464.698251972095.mm,-98.43049267694948.mm,1633.0962969779027.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.900841539338444.mm, -20.95559403330148.mm, -5.408185106409292.mm)
  circle = ge.add_circle([1469.775358702155.mm,-120.2756452980964.mm,1623.9188230384207.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.033712416508934.mm, -8.873515972046334.mm, -4.794785202687308.mm)
  circle = ge.add_circle([1458.8745171628166.mm,-141.2312393313979.mm,1618.5106379320114.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.784677428252053.mm, 7.3069121648404405.mm, -7.6974409813783495.mm)
  circle = ge.add_circle([1436.8408047463076.mm,-150.10475530344422.mm,1613.715852729324.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.299961121678734.mm, 18.085114603084975.mm, -12.411815515253238.mm)
  circle = ge.add_circle([1415.0561273180556.mm,-142.79784313860378.mm,1606.0184117479457.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.67701682398183.mm, 17.132511646976653.mm, -16.169794629058515.mm)
  circle = ge.add_circle([1404.7561661963769.mm,-124.7127285355188.mm,1593.6065962326925.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.7651393991855.mm, 5.008438098458896.mm, -16.76482575034038.mm)
  circle = ge.add_circle([1410.4331830203587.mm,-107.58021688854215.mm,1577.436801603634.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.453852752764305.mm, -11.168278378200839.mm, -13.847527626145848.mm)
  circle = ge.add_circle([1427.1983224195442.mm,-102.57177879008326.mm,1560.6719758532936.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.925933406254671.mm, -21.899241364487068.mm, -9.130834651693931.mm)
  circle = ge.add_circle([1443.6521751723085.mm,-113.7400571682841.mm,1546.8244482271477.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.049831662354109.mm, -20.883608501987425.mm, -5.38422230863921.mm)
  circle = ge.add_circle([1448.5781085785632.mm,-135.63929853277116.mm,1537.6936135754538.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.09303760207422.mm, -8.717723526936396.mm, -4.807569003219214.mm)
  circle = ge.add_circle([1437.528276916209.mm,-156.5229070347586.mm,1532.3093912668146.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.719504023264108.mm, 7.455035703866656.mm, -7.739465184170967.mm)
  circle = ge.add_circle([1415.4352393141348.mm,-165.24063056169499.mm,1527.5018222635954.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.148556647077385.mm, 18.138596326870385.mm, -12.458404993071781.mm)
  circle = ge.add_circle([1393.7157352908707.mm,-157.78559485782833.mm,1519.7623570794244.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.825753009579557.mm, 17.059948976735157.mm, -16.193593686457234.mm)
  circle = ge.add_circle([1383.5671786437933.mm,-139.64699853095794.mm,1507.3039520863526.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.82387466219916.mm, 4.85243727063731.mm, -16.751860421595893.mm)
  circle = ge.add_circle([1389.392931653373.mm,-122.58704955422279.mm,1491.1103583998954.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.388099821771902.mm, -11.316119188756176.mm, -13.805410694253169.mm)
  circle = ge.add_circle([1406.216806315572.mm,-117.73461228358548.mm,1474.3584979782995.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.77430007939347.mm, -21.952115256788915.mm, -9.08429569113946.mm)
  circle = ge.add_circle([1422.604906137344.mm,-129.05073147234165.mm,1460.5530872840463.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.198311652505936.mm, -20.810469794423113.mm, -5.3605873529159.mm)
  circle = ge.add_circle([1427.3792062167374.mm,-151.00284672913057.mm,1451.4687915929069.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.151182050851958.mm, -8.561516684718384.mm, -4.82071566334389.mm)
  circle = ge.add_circle([1416.1808945642315.mm,-171.81331652355368.mm,1446.108204239991.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.653172564490887.mm, 7.6025915415168015.mm, -7.781674205768468.mm)
  circle = ge.add_circle([1394.0297125133795.mm,-180.37483320827207.mm,1441.287488576647.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.996696769965865.mm, 18.19086158498766.mm, -12.50489272983441.mm)
  circle = ge.add_circle([1372.3765399488886.mm,-172.77224166675526.mm,1433.5058143708786.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.9739745501478865.mm, 16.986235342197944.mm, -16.217064181692876.mm)
  circle = ge.add_circle([1362.3798431789228.mm,-154.5813800817676.mm,1421.0009216410442.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.8814274140243.mm, 4.696026785465477.mm, -16.738532629676.mm)
  circle = ge.add_circle([1368.3538177290707.mm,-137.59514473956966.mm,1404.7838574593513.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.321190842224723.mm, -11.463387813393098.mm, -13.763110223743979.mm)
  circle = ge.add_circle([1385.235245143095.mm,-132.89911795410418.mm,1388.0453248296753.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.622215957481103.mm, -22.003771087260276.mm, -9.0378598839186.mm)
  circle = ge.add_circle([1401.5564359853197.mm,-144.36250576749728.mm,1374.2822146059314.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.346272493276501.mm, -20.73618235199129.mm, -5.337281674483393.mm)
  circle = ge.add_circle([1406.1786519428008.mm,-166.36627685475756.mm,1365.2443547220128.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.20814223199136.mm, -8.404904931126936.mm, -4.8342243847243935.mm)
  circle = ge.add_circle([1394.8323794495243.mm,-187.10245920674885.mm,1359.9070730475294.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.585687079943227.mm, 7.749570717392601.mm, -7.824065483007871.mm)
  circle = ge.add_circle([1372.624237217533.mm,-195.50736413787578.mm,1355.072848662805.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.844390712106815.mm, 18.24190720360417.mm, -12.551275902551652.mm)
  circle = ge.add_circle([1351.0385501375897.mm,-187.75779342048318.mm,1347.248783179797.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(6.1216724448638615.mm, 16.91137521966067.mm, -16.240204689508573.mm)
  circle = ge.add_circle([1341.194159425483.mm,-169.515886216879.mm,1334.6975072772454.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.937794159741543.mm, 4.539216141044136.mm, -16.724843183916846.mm)
  circle = ge.add_circle([1347.3158318703468.mm,-152.60451099721834.mm,1318.4573025877369.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.253129877202127.mm, -11.610075309154297.mm, -13.720628783334178.mm)
  circle = ge.add_circle([1364.2536260300883.mm,-148.0652948561742.mm,1301.73245940382.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.469690275898529.mm, -22.054205719076435.mm, -8.991530049868288.mm)
  circle = ge.add_circle([1380.5067559072904.mm,-159.6753701653285.mm,1288.0118306204859.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.493705199672831.mm, -20.660750685832.mm, -5.3143066885900225.mm)
  circle = ge.add_circle([1384.976446183189.mm,-181.72957588440494.mm,1279.0203005706176.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.26391468655902.mm, -8.247897776485189.mm, -4.848094347036977.mm)
  circle = ge.add_circle([1373.4827409835161.mm,-202.39032657023694.mm,1273.7059938820275.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.51705166770853.mm, 7.895964306113797.mm, -7.866636441658784.mm)
  circle = ge.add_circle([1351.218826296957.mm,-210.63822434672213.mm,1268.8578995349906.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.691647722358312.mm, 18.291730082950295.mm, -12.597551694582762.mm)
  circle = ge.add_circle([1329.7017746292486.mm,-202.74226004060833.mm,1260.9912630933318.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(6.268837724702053.mm, 16.835373155039747.mm, -16.263013804686352.mm)
  circle = ge.add_circle([1320.0101269068903.mm,-184.45052995765803.mm,1248.393711398749.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.99297147645416.mm, 4.382014859774529.mm, -16.710792915616594.mm)
  circle = ge.add_circle([1326.2789646315923.mm,-167.6151568026183.mm,1232.1306975940627.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.18392105973885.mm, -11.756172768371812.mm, -13.67796895272977.mm)
  circle = ge.add_circle([1343.2719361080465.mm,-163.23314194284376.mm,1215.419904678446.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.316732296840428.mm, -22.103416089570572.mm, -8.945309002388967.mm)
  circle = ge.add_circle([1359.4558571677853.mm,-174.98931471121557.mm,1201.7419357257163.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.640600818774374.mm, -20.584179376569153.mm, -5.291663790403163.mm)
  circle = ge.add_circle([1363.7725894646258.mm,-197.09273080078614.mm,1192.7966267233273.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.318496027746278.mm, -8.090504755127114.mm, -4.862324708021333.mm)
  circle = ge.add_circle([1352.1319886458514.mm,-217.6769101773553.mm,1187.5049629329242.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.447270495704743.mm, 8.041763417860125.mm, -7.90938449658006.mm)
  circle = ge.add_circle([1329.813492618105.mm,-225.7674149324824.mm,1182.6426382249028.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.538477076110667.mm, 18.340327197508373.mm, -12.643717295808301.mm)
  circle = ge.add_circle([1308.3662221224004.mm,-217.72565151462229.mm,1174.7332537283228.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(6.415461452981617.mm, 16.75823376359665.mm, -16.285490142131266.mm)
  circle = ge.add_circle([1298.8277450462897.mm,-199.3853243171139.mm,1162.0895364325145.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(17.0469560134934.mm, 4.224432487778671.mm, -16.696382677984957.mm)
  circle = ge.add_circle([1305.2432064992713.mm,-182.62709055351726.mm,1145.8040462903832.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.113568592572392.mm, -11.901671319208333.mm, -13.635133322468619.mm)
  circle = ge.add_circle([1322.2901625127647.mm,-178.4026580657386.mm,1129.1076636123983.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.163351308752681.mm, -22.151399210419044.mm, -8.899199548276101.mm)
  circle = ge.add_circle([1338.403731105337.mm,-190.30432938494693.mm,1115.4725302899296.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.786950430275056.mm, -20.50647307403196.mm, -5.26935435492328.mm)
  circle = ge.add_circle([1342.5670824140898.mm,-212.45572859536597.mm,1106.5733307416535.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.371882941074773.mm, -7.932735424818674.mm, -4.876914603532441.mm)
  circle = ge.add_circle([1330.7801319838147.mm,-232.96220166939793.mm,1101.3039763867303.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.376347801427073.mm, 8.186959198911296.mm, -7.952307051875096.mm)
  circle = ge.add_circle([1308.40824904274.mm,-240.8949370942166.mm,1096.4270617831978.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.384888074724358.mm, 18.387695596195414.mm, -12.68976990280089.mm)
  circle = ge.add_circle([1287.0319012413129.mm,-232.7079778953053.mm,1088.4747547313227.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(6.561534725906768.mm, 16.679961729657464.mm, -16.30763233695734.mm)
  circle = ge.add_circle([1277.6470131665885.mm,-214.3202822991099.mm,1075.7849848285218.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(17.099744492622676.mm, 4.066478594321239.mm, -16.68161334608976.mm)
  circle = ge.add_circle([1284.2085478924953.mm,-197.64032056945243.mm,1059.4773524915645.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.042076747890178.mm, -12.046562126195198.mm, -13.592124493765368.mm)
  circle = ge.add_circle([1301.308292385118.mm,-193.5738419751312.mm,1042.7957391454747.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.009556625768482.mm, -22.19815216782456.mm, -8.85320448754851.mm)
  circle = ge.add_circle([1317.3503691330081.mm,-205.6204041013264.mm,1029.2036146517094.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.932745147024434.mm, -20.427636496972156.mm, -5.247379736901053.mm)
  circle = ge.add_circle([1321.3599257587766.mm,-227.81855626915095.mm,1020.3504101641608.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.424072184599936.mm, -7.774599366177483.mm, -4.891863147591835.mm)
  circle = ge.add_circle([1309.4271806117522.mm,-248.2461927661231.mm,1015.1030304272598.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.304287891689.mm, 8.331542832184454.mm, -7.995401501051219.mm)
  circle = ge.add_circle([1287.0031084271523.mm,-256.0207921323006.mm,1010.211167279668.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.23089004496478.mm, 18.433832402543004.mm, -12.73570671899381.mm)
  circle = ge.add_circle([1265.6988205354633.mm,-247.68924930011613.mm,1002.2157657786167.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(6.707048673109057.mm, 16.600561806328756.mm, -16.329439044569085.mm)
  circle = ge.add_circle([1256.4679304904985.mm,-229.25541689757313.mm,989.4800590596229.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(17.151333708236052.mm, 3.908162771227296.mm, -16.666485816806244.mm)
  circle = ge.add_circle([1263.1749791636075.mm,-212.65485509124437.mm,973.1506200150538.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(15.96944986706876.mm, -12.190836390769277.mm, -13.548945078351153.mm)
  circle = ge.add_circle([1280.3263128718436.mm,-208.74669232001708.mm,956.4841341982476.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.855357587142862.mm, -22.243672122691464.mm, -8.807326613277496.mm)
  circle = ge.add_circle([1296.2957627389123.mm,-220.93752871078635.mm,942.9351891198964.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-12.077976115569754.mm, -20.347674432778547.mm, -5.2257412707562025.mm)
  circle = ge.add_circle([1300.1511203260552.mm,-243.18120083347782.mm,934.127862506619.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.475060589104487.mm, -7.616106182090732.mm, -4.9071694324420605.mm)
  circle = ge.add_circle([1288.0731442104855.mm,-263.52887526625636.mm,928.9021212358628.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.231095142363074.mm, 8.475505537770175.mm, -8.038665227178058.mm)
  circle = ge.add_circle([1265.598083621381.mm,-271.1449814483471.mm,923.9949518034207.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.076492338434718.mm, 18.478734814871387.mm, -12.781524954851534.mm)
  circle = ge.add_circle([1244.366988479018.mm,-262.6694759105769.mm,915.9562865762426.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(6.851994458184208.mm, 16.520038815208522.mm, -16.35090894074426.mm)
  circle = ge.add_circle([1235.2904961405832.mm,-244.19074109570553.mm,903.1747616213911.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(17.20172052755447.mm, 3.749494632300298.mm, -16.651001008760772.mm)
  circle = ge.add_circle([1242.1424905987674.mm,-227.670702280497.mm,886.8238526806468.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(15.895692360409384.mm, -12.334485351807274.mm, -13.505597698316365.mm)
  circle = ge.add_circle([1259.3442111263219.mm,-223.9212076481967.mm,870.1728516718861.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.700763556685615.mm, -22.287956310799018.mm, -8.761568711419159.mm)
  circle = ge.add_circle([1275.2399034867312.mm,-236.255693000004.mm,856.6672539735697.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-12.222634516690732.mm, -20.266591737185024.mm, -5.204440270494501.mm)
  circle = ge.add_circle([1278.9406670434169.mm,-258.543649310803.mm,847.9056852621505.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.524845058293522.mm, -7.457265497132539.mm, -4.922832528601589.mm)
  circle = ge.add_circle([1266.7180325267261.mm,-278.81024104798803.mm,842.701244991656.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.156773998113977.mm, 8.618838573464359.mm, -8.082095603045445.mm)
  circle = ge.add_circle([1244.1931874684326.mm,-286.26750654512057.mm,837.7784124630545.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.921704331008641.mm, 18.522400106460793.mm, -12.827221828040365.mm)
  circle = ge.add_circle([1223.0364134703186.mm,-277.6486679716562.mm,829.696316860009.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(6.996363279230536.mm, 16.438397646093307.mm, -16.37204072171278.mm)
  circle = ge.add_circle([1214.11470913931.mm,-259.1262678651954.mm,816.8690950319686.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(17.250901890814475.mm, 3.5904838127386256.mm, -16.635159862275373.mm)
  circle = ge.add_circle([1221.1110724185405.mm,-242.6878702191021.mm,800.4970543102559.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(15.820808706871958.mm, -12.477500286157863.mm, -13.46208498595172.mm)
  circle = ge.add_circle([1238.361974309355.mm,-239.09738640636348.mm,783.8618944479805.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.5457839221933227.mm, -22.331002042968322.mm, -8.715933560643634.mm)
  circle = ge.add_circle([1254.182783016227.mm,-251.57488669252135.mm,770.3998094620288.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-27.100566938420116.mm, 3.6558887354896683.mm, 6.016124098614796.mm)
  circle = ge.add_circle([1257.7285669384203.mm,-273.90588873548967.mm,761.6838759013851.mm], vec, 5.mm, 8)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-31.128000000000156.mm, -22.25.mm, -126.69999999999993.mm)
  circle = ge.add_circle([1230.6280000000002.mm,-270.25.mm,767.6999999999999.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 71.18166666666662.mm)
  circle = ge.add_circle([1000.mm,-292.5.mm,711.mm], vec, 100.mm, 14)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 71.18166666666673.mm)
  circle = ge.add_circle([1000.mm,-292.5.mm,782.1816666666666.mm], vec, 80.mm, 14)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 71.18166666666662.mm)
  circle = ge.add_circle([1000.mm,-292.5.mm,853.3633333333333.mm], vec, 100.mm, 14)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 71.18166666666673.mm)
  circle = ge.add_circle([1000.mm,-292.5.mm,924.545.mm], vec, 80.mm, 14)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 71.18166666666662.mm)
  circle = ge.add_circle([1000.mm,-292.5.mm,995.7266666666667.mm], vec, 100.mm, 14)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 71.18166666666662.mm)
  circle = ge.add_circle([1000.mm,-292.5.mm,1066.9083333333333.mm], vec, 80.mm, 14)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 71.18166666666662.mm)
  circle = ge.add_circle([1000.mm,-292.5.mm,1138.09.mm], vec, 100.mm, 14)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 71.18166666666684.mm)
  circle = ge.add_circle([1000.mm,-292.5.mm,1209.2716666666665.mm], vec, 80.mm, 14)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 71.18166666666639.mm)
  circle = ge.add_circle([1000.mm,-292.5.mm,1280.4533333333334.mm], vec, 100.mm, 14)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 71.18166666666684.mm)
  circle = ge.add_circle([1000.mm,-292.5.mm,1351.6349999999998.mm], vec, 80.mm, 14)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 71.18166666666662.mm)
  circle = ge.add_circle([1000.mm,-292.5.mm,1422.8166666666666.mm], vec, 100.mm, 14)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 71.18166666666662.mm)
  circle = ge.add_circle([1000.mm,-292.5.mm,1493.9983333333332.mm], vec, 80.mm, 14)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 71.18166666666684.mm)
  circle = ge.add_circle([1000.mm,-292.5.mm,1565.1799999999998.mm], vec, 100.mm, 14)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 71.18166666666662.mm)
  circle = ge.add_circle([1000.mm,-292.5.mm,1636.3616666666667.mm], vec, 80.mm, 14)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 71.18166666666662.mm)
  circle = ge.add_circle([1000.mm,-292.5.mm,1707.5433333333333.mm], vec, 100.mm, 14)
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
  arc = ge.add_arc([1000.mm,-171.225.mm,1778.725.mm], [0.000000,-1.000000,0.000000], [-1.000000,0.000000,0.000000], 121.275.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1000.mm,-292.5.mm,1778.725.mm], [0.000000,0.000000,1.000000], 100.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 15.778124999999989.mm, 0.mm)
  circle = ge.add_circle([1000.mm,-171.22500000000002.mm,1900.mm], vec, 100.mm, 14)
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
  vec = Geom::Vector3d.new(0.mm, 15.778125000000017.mm, 0.mm)
  circle = ge.add_circle([1000.mm,-155.44687500000003.mm,1900.mm], vec, 80.mm, 14)
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
  vec = Geom::Vector3d.new(0.mm, 15.778125000000003.mm, 0.mm)
  circle = ge.add_circle([1000.mm,-139.66875000000002.mm,1900.mm], vec, 100.mm, 14)
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
  vec = Geom::Vector3d.new(0.mm, 15.778125000000003.mm, 0.mm)
  circle = ge.add_circle([1000.mm,-123.89062500000001.mm,1900.mm], vec, 80.mm, 14)
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
  vec = Geom::Vector3d.new(0.mm, 15.778125000000003.mm, 0.mm)
  circle = ge.add_circle([1000.mm,-108.11250000000001.mm,1900.mm], vec, 100.mm, 14)
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
  vec = Geom::Vector3d.new(0.mm, 15.778125000000003.mm, 0.mm)
  circle = ge.add_circle([1000.mm,-92.33437500000001.mm,1900.mm], vec, 80.mm, 14)
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
  vec = Geom::Vector3d.new(0.mm, 15.778125000000003.mm, 0.mm)
  circle = ge.add_circle([1000.mm,-76.55625.mm,1900.mm], vec, 100.mm, 14)
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
  vec = Geom::Vector3d.new(0.mm, 15.778125000000003.mm, 0.mm)
  circle = ge.add_circle([1000.mm,-60.778125.mm,1900.mm], vec, 80.mm, 14)
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
  face = grp.entities.add_face([5593.mm,1081.mm,1900.mm], [5893.mm,1081.mm,1900.mm], [5893.mm,1281.mm,1900.mm], [5593.mm,1281.mm,1900.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan A (exhaust) baffle duct"] || model.materials.add("Fan A (exhaust) baffle duct")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 0.5
  grp.material = mat

  # Fan A (exhaust) baffle plate 1
  grp = ents.add_group
  grp.name = "Fan A (exhaust) baffle plate 1"
  face = grp.entities.add_face([5689.mm,1081.mm,1900.mm], [5697.mm,1081.mm,1900.mm], [5697.mm,1206.mm,1900.mm], [5689.mm,1206.mm,1900.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) baffle plate 2
  grp = ents.add_group
  grp.name = "Fan A (exhaust) baffle plate 2"
  face = grp.entities.add_face([5789.mm,1156.mm,1900.mm], [5797.mm,1156.mm,1900.mm], [5797.mm,1281.mm,1900.mm], [5789.mm,1281.mm,1900.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan frame top
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan frame top"
  face = grp.entities.add_face([5593.mm,1081.mm,2075.mm], [5643.mm,1081.mm,2075.mm], [5643.mm,1281.mm,2075.mm], [5593.mm,1281.mm,2075.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan frame bottom
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan frame bottom"
  face = grp.entities.add_face([5593.mm,1081.mm,1900.mm], [5643.mm,1081.mm,1900.mm], [5643.mm,1281.mm,1900.mm], [5593.mm,1281.mm,1900.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan frame left
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan frame left"
  face = grp.entities.add_face([5593.mm,1081.mm,1925.mm], [5643.mm,1081.mm,1925.mm], [5643.mm,1106.mm,1925.mm], [5593.mm,1106.mm,1925.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan frame right
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan frame right"
  face = grp.entities.add_face([5593.mm,1256.mm,1925.mm], [5643.mm,1256.mm,1925.mm], [5643.mm,1281.mm,1925.mm], [5593.mm,1281.mm,1925.mm])
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
  circle = ge.add_circle([5593.mm,1181.mm,2000.mm], [1,0,0], 19.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan blade up
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan blade up"
  face = grp.entities.add_face([5615.5.mm,1166.mm,2019.5.mm], [5621.5.mm,1166.mm,2019.5.mm], [5621.5.mm,1196.mm,2019.5.mm], [5615.5.mm,1196.mm,2019.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.5.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan blade down
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan blade down"
  face = grp.entities.add_face([5615.5.mm,1166.mm,1934.mm], [5621.5.mm,1166.mm,1934.mm], [5621.5.mm,1196.mm,1934.mm], [5615.5.mm,1196.mm,1934.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.5.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan blade left
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan blade left"
  face = grp.entities.add_face([5615.5.mm,1115.mm,1985.mm], [5621.5.mm,1115.mm,1985.mm], [5621.5.mm,1161.5.mm,1985.mm], [5615.5.mm,1161.5.mm,1985.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan blade right
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan blade right"
  face = grp.entities.add_face([5615.5.mm,1200.5.mm,1985.mm], [5621.5.mm,1200.5.mm,1985.mm], [5621.5.mm,1247.mm,1985.mm], [5615.5.mm,1247.mm,1985.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) wall flange
  grp = ents.add_group
  grp.name = "Fan A (exhaust) wall flange"
  face = grp.entities.add_face([5888.mm,1051.mm,1870.mm], [5893.mm,1051.mm,1870.mm], [5893.mm,1311.mm,1870.mm], [5888.mm,1311.mm,1870.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(260.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) flange bolt M10
  grp = ents.add_group
  grp.name = "Fan A (exhaust) flange bolt M10"
  ge = grp.entities
  circle = ge.add_circle([5886.5.mm,1066.mm,1885.mm], [1,0,0], 5.mm, 24)
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
  circle = ge.add_circle([5886.5.mm,1066.mm,2115.mm], [1,0,0], 5.mm, 24)
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
  circle = ge.add_circle([5886.5.mm,1296.mm,1885.mm], [1,0,0], 5.mm, 24)
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
  circle = ge.add_circle([5886.5.mm,1296.mm,2115.mm], [1,0,0], 5.mm, 24)
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
  face = grp.entities.add_face([5893.mm,1081.mm,1935.mm], [5933.mm,1081.mm,1935.mm], [5933.mm,1281.mm,1935.mm], [5893.mm,1281.mm,1935.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(130.mm)
  mat = model.materials["Fan A (exhaust) louvre grille"] || model.materials.add("Fan A (exhaust) louvre grille")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 0.55
  grp.material = mat

  # Fan A (exhaust) louvre slat
  grp = ents.add_group
  grp.name = "Fan A (exhaust) louvre slat"
  face = grp.entities.add_face([5895.mm,1085.mm,1946.5.mm], [5931.mm,1085.mm,1946.5.mm], [5931.mm,1277.mm,1946.5.mm], [5895.mm,1277.mm,1946.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) louvre slat
  grp = ents.add_group
  grp.name = "Fan A (exhaust) louvre slat"
  face = grp.entities.add_face([5895.mm,1085.mm,1972.5.mm], [5931.mm,1085.mm,1972.5.mm], [5931.mm,1277.mm,1972.5.mm], [5895.mm,1277.mm,1972.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) louvre slat
  grp = ents.add_group
  grp.name = "Fan A (exhaust) louvre slat"
  face = grp.entities.add_face([5895.mm,1085.mm,1998.5.mm], [5931.mm,1085.mm,1998.5.mm], [5931.mm,1277.mm,1998.5.mm], [5895.mm,1277.mm,1998.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) louvre slat
  grp = ents.add_group
  grp.name = "Fan A (exhaust) louvre slat"
  face = grp.entities.add_face([5895.mm,1085.mm,2024.5.mm], [5931.mm,1085.mm,2024.5.mm], [5931.mm,1277.mm,2024.5.mm], [5895.mm,1277.mm,2024.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) louvre slat
  grp = ents.add_group
  grp.name = "Fan A (exhaust) louvre slat"
  face = grp.entities.add_face([5895.mm,1085.mm,2050.5.mm], [5931.mm,1085.mm,2050.5.mm], [5931.mm,1277.mm,2050.5.mm], [5895.mm,1277.mm,2050.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) baffle duct
  grp = ents.add_group
  grp.name = "Fan B (intake) baffle duct"
  face = grp.entities.add_face([0.mm,265.mm,500.mm], [300.mm,265.mm,500.mm], [300.mm,465.mm,500.mm], [0.mm,465.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan A (exhaust) baffle duct"] || model.materials.add("Fan A (exhaust) baffle duct")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 0.5
  grp.material = mat

  # Fan B (intake) baffle plate 1
  grp = ents.add_group
  grp.name = "Fan B (intake) baffle plate 1"
  face = grp.entities.add_face([96.mm,265.mm,500.mm], [104.mm,265.mm,500.mm], [104.mm,390.mm,500.mm], [96.mm,390.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) baffle plate 2
  grp = ents.add_group
  grp.name = "Fan B (intake) baffle plate 2"
  face = grp.entities.add_face([196.mm,340.mm,500.mm], [204.mm,340.mm,500.mm], [204.mm,465.mm,500.mm], [196.mm,465.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan frame top
  grp = ents.add_group
  grp.name = "Fan B (intake) fan frame top"
  face = grp.entities.add_face([250.mm,265.mm,675.mm], [300.mm,265.mm,675.mm], [300.mm,465.mm,675.mm], [250.mm,465.mm,675.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan frame bottom
  grp = ents.add_group
  grp.name = "Fan B (intake) fan frame bottom"
  face = grp.entities.add_face([250.mm,265.mm,500.mm], [300.mm,265.mm,500.mm], [300.mm,465.mm,500.mm], [250.mm,465.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan frame left
  grp = ents.add_group
  grp.name = "Fan B (intake) fan frame left"
  face = grp.entities.add_face([250.mm,265.mm,525.mm], [300.mm,265.mm,525.mm], [300.mm,290.mm,525.mm], [250.mm,290.mm,525.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan frame right
  grp = ents.add_group
  grp.name = "Fan B (intake) fan frame right"
  face = grp.entities.add_face([250.mm,440.mm,525.mm], [300.mm,440.mm,525.mm], [300.mm,465.mm,525.mm], [250.mm,465.mm,525.mm])
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
  circle = ge.add_circle([250.mm,365.mm,600.mm], [1,0,0], 19.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade up
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade up"
  face = grp.entities.add_face([272.5.mm,350.mm,619.5.mm], [278.5.mm,350.mm,619.5.mm], [278.5.mm,380.mm,619.5.mm], [272.5.mm,380.mm,619.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.5.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade down
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade down"
  face = grp.entities.add_face([272.5.mm,350.mm,534.mm], [278.5.mm,350.mm,534.mm], [278.5.mm,380.mm,534.mm], [272.5.mm,380.mm,534.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.5.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade left
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade left"
  face = grp.entities.add_face([272.5.mm,299.mm,585.mm], [278.5.mm,299.mm,585.mm], [278.5.mm,345.5.mm,585.mm], [272.5.mm,345.5.mm,585.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade right
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade right"
  face = grp.entities.add_face([272.5.mm,384.5.mm,585.mm], [278.5.mm,384.5.mm,585.mm], [278.5.mm,431.mm,585.mm], [272.5.mm,431.mm,585.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) wall flange
  grp = ents.add_group
  grp.name = "Fan B (intake) wall flange"
  face = grp.entities.add_face([0.mm,235.mm,470.mm], [5.mm,235.mm,470.mm], [5.mm,495.mm,470.mm], [0.mm,495.mm,470.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(260.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) flange bolt M10
  grp = ents.add_group
  grp.name = "Fan B (intake) flange bolt M10"
  ge = grp.entities
  circle = ge.add_circle([-6.5.mm,250.mm,485.mm], [1,0,0], 5.mm, 24)
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
  circle = ge.add_circle([-6.5.mm,250.mm,715.mm], [1,0,0], 5.mm, 24)
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
  circle = ge.add_circle([-6.5.mm,480.mm,485.mm], [1,0,0], 5.mm, 24)
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
  circle = ge.add_circle([-6.5.mm,480.mm,715.mm], [1,0,0], 5.mm, 24)
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
  face = grp.entities.add_face([-40.mm,265.mm,535.mm], [0.mm,265.mm,535.mm], [0.mm,465.mm,535.mm], [-40.mm,465.mm,535.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(130.mm)
  mat = model.materials["Fan A (exhaust) louvre grille"] || model.materials.add("Fan A (exhaust) louvre grille")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 0.55
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,269.mm,546.5.mm], [-2.mm,269.mm,546.5.mm], [-2.mm,461.mm,546.5.mm], [-38.mm,461.mm,546.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,269.mm,572.5.mm], [-2.mm,269.mm,572.5.mm], [-2.mm,461.mm,572.5.mm], [-38.mm,461.mm,572.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,269.mm,598.5.mm], [-2.mm,269.mm,598.5.mm], [-2.mm,461.mm,598.5.mm], [-38.mm,461.mm,598.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,269.mm,624.5.mm], [-2.mm,269.mm,624.5.mm], [-2.mm,461.mm,624.5.mm], [-38.mm,461.mm,624.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,269.mm,650.5.mm], [-2.mm,269.mm,650.5.mm], [-2.mm,461.mm,650.5.mm], [-38.mm,461.mm,650.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  circle = ge.add_circle([1130.mm,12.mm,40.mm], [1,0,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(3519.mm)
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
  cface.pushpull(910.mm)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # BV-02 (ball valve)
  grp = ents.add_group
  grp.name = "BV-02 (ball valve)"
  face = grp.entities.add_face([2374.mm,-13.mm,925.mm], [2424.mm,-13.mm,925.mm], [2424.mm,37.mm,925.mm], [2374.mm,37.mm,925.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # TAP-01 Branch (3/4in)
  grp = ents.add_group
  grp.name = "TAP-01 Branch (3/4in)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1310.mm)
  circle = ge.add_circle([1130.mm,12.mm,40.mm], vec, 12.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # TAP-01 Branch (3/4in) elbow
  grp = ents.add_group
  grp.name = "TAP-01 Branch (3/4in) elbow"
  ge = grp.entities
  arc = ge.add_arc([1130.mm,37.mm,1350.mm], [0.000000,-1.000000,0.000000], [-1.000000,0.000000,0.000000], 25.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1130.mm,12.mm,1350.mm], [0.000000,0.000000,1.000000], 12.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # TAP-01 Branch (3/4in)
  grp = ents.add_group
  grp.name = "TAP-01 Branch (3/4in)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 50.mm, 0.mm)
  circle = ge.add_circle([1130.mm,37.mm,1375.mm], vec, 12.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # TAP-01 Branch (3/4in) elbow
  grp = ents.add_group
  grp.name = "TAP-01 Branch (3/4in) elbow"
  ge = grp.entities
  arc = ge.add_arc([1130.mm,87.mm,1350.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 25.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1130.mm,87.mm,1375.mm], [0.000000,1.000000,0.000000], 12.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # TAP-01 Branch (3/4in)
  grp = ents.add_group
  grp.name = "TAP-01 Branch (3/4in)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -200.mm)
  circle = ge.add_circle([1130.mm,112.mm,1350.mm], vec, 12.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # BV-06 (chem tap isolation)
  grp = ents.add_group
  grp.name = "BV-06 (chem tap isolation)"
  face = grp.entities.add_face([1112.mm,4.mm,1010.mm], [1148.mm,4.mm,1010.mm], [1148.mm,40.mm,1010.mm], [1112.mm,40.mm,1010.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Spray Bar Plumbing"
  inst.layer = model.layers["Spray Bar"]

  # ═══ Water Plumbing ═══
  defn = model.definitions.add("Water Plumbing")
  ents = defn.entities
  # X1 Blue Fill Trunk
  grp = ents.add_group
  grp.name = "X1 Blue Fill Trunk"
  ge = grp.entities
  vec = Geom::Vector3d.new(-240.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5893.mm,1181.mm,2250.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue Fill Tee
  grp = ents.add_group
  grp.name = "Blue Fill Tee"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 45.59999999999991.mm, 0.mm)
  circle = ge.add_circle([5653.mm,1158.2.mm,2250.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue Fill Tee
  grp = ents.add_group
  grp.name = "Blue Fill Tee"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -22.800000000000182.mm)
  circle = ge.add_circle([5653.mm,1181.mm,2250.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill → Blue #1 side
  grp = ents.add_group
  grp.name = "Fill → Blue #1 side"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -70.mm)
  circle = ge.add_circle([5653.mm,1181.mm,2250.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill → Blue #1 side elbow
  grp = ents.add_group
  grp.name = "Fill → Blue #1 side elbow"
  ge = grp.entities
  arc = ge.add_arc([5653.mm,1157.mm,2180.mm], [0.000000,1.000000,0.000000], [-1.000000,-0.000000,-0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5653.mm,1181.mm,2180.mm], [0.000000,0.000000,-1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill → Blue #1 side
  grp = ents.add_group
  grp.name = "Fill → Blue #1 side"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -261.mm, 0.mm)
  circle = ge.add_circle([5653.mm,1157.mm,2156.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill → Blue #2 side
  grp = ents.add_group
  grp.name = "Fill → Blue #2 side"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 285.mm, 0.mm)
  circle = ge.add_circle([5653.mm,1181.mm,2156.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill Flange Blue #1
  grp = ents.add_group
  grp.name = "Fill Flange Blue #1"
  ge = grp.entities
  circle = ge.add_circle([5653.mm,1038.mm,2156.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(16.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill Flange Blue #2
  grp = ents.add_group
  grp.name = "Fill Flange Blue #2"
  ge = grp.entities
  circle = ge.add_circle([5653.mm,1308.mm,2156.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(16.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 → X3 (Brown drain-out)
  grp = ents.add_group
  grp.name = "P-05 → X3 (Brown drain-out)"
  ge = grp.entities
  vec = Geom::Vector3d.new(522.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4854.mm,1253.mm,1996.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([5376.mm,1253.mm,1972.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5376.mm,1253.mm,1996.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1548.mm)
  circle = ge.add_circle([5400.mm,1253.mm,1972.mm], vec, 12.mm, 16)
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
  vec = Geom::Vector3d.new(462.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4854.mm,1253.mm,1628.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([5316.mm,1253.mm,1604.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5316.mm,1253.mm,1628.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1380.mm)
  circle = ge.add_circle([5340.mm,1253.mm,1604.mm], vec, 12.mm, 16)
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

  # Blue Manifold Tee
  grp = ents.add_group
  grp.name = "Blue Manifold Tee"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 45.59999999999991.mm, 0.mm)
  circle = ge.add_circle([4814.mm,1158.2.mm,1353.mm], vec, 16.200000000000003.mm, 16)
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
  circle = ge.add_circle([4814.mm,1181.mm,1353.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 → manifold
  grp = ents.add_group
  grp.name = "Blue #1 → manifold"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 285.mm, 0.mm)
  circle = ge.add_circle([4814.mm,896.mm,1353.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #2 → manifold
  grp = ents.add_group
  grp.name = "Blue #2 → manifold"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -285.mm, 0.mm)
  circle = ge.add_circle([4814.mm,1466.mm,1353.mm], vec, 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, -63.67000000000007.mm, 0.mm)
  circle = ge.add_circle([4814.mm,1181.mm,1353.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([4814.mm,1117.33.mm,1361.33.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 8.330000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4814.mm,1117.33.mm,1353.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 8.670000000000073.mm)
  circle = ge.add_circle([4814.mm,1109.mm,1361.33.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 Suction Flange
  grp = ents.add_group
  grp.name = "Blue #1 Suction Flange"
  ge = grp.entities
  circle = ge.add_circle([4814.mm,1037.mm,1353.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #2 Suction Flange
  grp = ents.add_group
  grp.name = "Blue #2 Suction Flange"
  ge = grp.entities
  circle = ge.add_circle([4814.mm,1307.mm,1353.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Brown → P-02
  grp = ents.add_group
  grp.name = "Brown → P-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 333.mm, 0.mm)
  circle = ge.add_circle([4814.mm,896.mm,185.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([4814.mm,1229.mm,209.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4814.mm,1229.mm,185.mm], [0.000000,1.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1161.mm)
  circle = ge.add_circle([4814.mm,1253.mm,209.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown Suction Flange
  grp = ents.add_group
  grp.name = "Brown Suction Flange"
  ge = grp.entities
  circle = ge.add_circle([4814.mm,1037.mm,185.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Waste → P-03
  grp = ents.add_group
  grp.name = "Waste → P-03"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -189.mm, 0.mm)
  circle = ge.add_circle([4854.mm,1466.mm,185.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([4854.mm,1277.mm,209.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4854.mm,1277.mm,185.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1419.mm)
  circle = ge.add_circle([4854.mm,1253.mm,209.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste Suction Flange
  grp = ents.add_group
  grp.name = "Waste Suction Flange"
  ge = grp.entities
  circle = ge.add_circle([4854.mm,1307.mm,185.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 151.mm)
  circle = ge.add_circle([4550.mm,155.mm,20.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([4526.mm,155.mm,171.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4550.mm,155.mm,171.mm], [0.000000,0.000000,1.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(-23.460000000000036.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4526.mm,155.mm,195.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([4502.54.mm,132.46.mm,195.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 22.540000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4502.54.mm,155.mm,195.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, -58.46000000000001.mm, 0.mm)
  circle = ge.add_circle([4480.mm,132.46.mm,195.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([4480.mm,74.mm,171.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4480.mm,74.mm,195.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -117.mm)
  circle = ge.add_circle([4480.mm,50.mm,171.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([4504.mm,50.mm,54.mm], [-1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4480.mm,50.mm,54.mm], [0.000000,0.000000,-1.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(123.5.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4504.mm,50.mm,30.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([4627.5.mm,74.mm,30.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4627.5.mm,50.mm,30.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 1095.975.mm, 0.mm)
  circle = ge.add_circle([4651.5.mm,74.mm,30.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([4662.525.mm,1169.975.mm,30.mm], [-1.000000,0.000000,0.000000], [0.000000,0.000000,-1.000000], 11.025000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4651.5.mm,1169.975.mm,30.mm], [0.000000,1.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(5.852249999999913.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4662.525.mm,1181.mm,30.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([4668.37725.mm,1181.mm,35.62275000000018.mm], [0.000000,0.000000,-1.000000], [0.000000,-1.000000,0.000000], 5.622750000000179.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4668.37725.mm,1181.mm,30.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 30.37724999999982.mm)
  circle = ge.add_circle([4674.mm,1181.mm,35.62275000000018.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([4698.mm,1181.mm,66.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4674.mm,1181.mm,66.mm], [0.000000,0.000000,1.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(132.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4698.mm,1181.mm,90.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([4830.mm,1157.mm,90.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,-1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4830.mm,1181.mm,90.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
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
  circle = ge.add_circle([4854.mm,1157.mm,90.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([4854.mm,1132.52.mm,113.52000000000001.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 23.520000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4854.mm,1132.52.mm,90.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1514.48.mm)
  circle = ge.add_circle([4854.mm,1109.mm,113.52.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1096.mm)
  circle = ge.add_circle([4814.mm,1109.mm,1370.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar elbow
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar elbow"
  ge = grp.entities
  arc = ge.add_arc([4790.mm,1109.mm,274.mm], [1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4814.mm,1109.mm,274.mm], [0.000000,0.000000,-1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar"
  ge = grp.entities
  vec = Geom::Vector3d.new(-92.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4790.mm,1109.mm,250.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar elbow
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar elbow"
  ge = grp.entities
  arc = ge.add_arc([4698.mm,1109.mm,226.mm], [0.000000,0.000000,1.000000], [-0.000000,-1.000000,-0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4698.mm,1109.mm,250.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -153.75.mm)
  circle = ge.add_circle([4674.mm,1109.mm,226.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar elbow
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar elbow"
  ge = grp.entities
  arc = ge.add_arc([4661.75.mm,1109.mm,72.25.mm], [1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 12.250000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4674.mm,1109.mm,72.25.mm], [0.000000,0.000000,-1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar"
  ge = grp.entities
  vec = Geom::Vector3d.new(-6.5024999999996.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4661.75.mm,1109.mm,60.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar elbow
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar elbow"
  ge = grp.entities
  arc = ge.add_arc([4655.2475.mm,1102.7525.mm,60.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 6.2475000000000005.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4655.2475.mm,1109.mm,60.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -1080.9525.mm, 0.mm)
  circle = ge.add_circle([4649.mm,1102.7525.mm,60.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar elbow
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar elbow"
  ge = grp.entities
  arc = ge.add_arc([4649.mm,21.8.mm,50.199999999999996.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 9.800000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4649.mm,21.8.mm,60.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar"
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

  # 3W-DV-02 Diverter
  grp = ents.add_group
  grp.name = "3W-DV-02 Diverter"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -45.59999999999991.mm, 0.mm)
  circle = ge.add_circle([4854.mm,1081.8.mm,1088.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-02 Diverter
  grp = ents.add_group
  grp.name = "3W-DV-02 Diverter"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 22.799999999999955.mm)
  circle = ge.add_circle([4854.mm,1059.mm,1088.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # P-04 → DV-02
  grp = ents.add_group
  grp.name = "P-04 → DV-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -26.mm, 0.mm)
  circle = ge.add_circle([4854.mm,1109.mm,1628.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-04 → DV-02 elbow
  grp = ents.add_group
  grp.name = "P-04 → DV-02 elbow"
  ge = grp.entities
  arc = ge.add_arc([4854.mm,1083.mm,1604.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4854.mm,1083.mm,1628.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-04 → DV-02
  grp = ents.add_group
  grp.name = "P-04 → DV-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -516.mm)
  circle = ge.add_circle([4854.mm,1059.mm,1604.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 → IBC-3 side-entry
  grp = ents.add_group
  grp.name = "DV-02 → IBC-3 side-entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -163.mm, 0.mm)
  circle = ge.add_circle([4854.mm,1059.mm,1088.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 Recycle Flange
  grp = ents.add_group
  grp.name = "IBC-3 Recycle Flange"
  ge = grp.entities
  circle = ge.add_circle([4854.mm,1037.mm,1088.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 → Filters
  grp = ents.add_group
  grp.name = "P-02 → Filters"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.252676814717233.mm, -50.068522833113775.mm, 0.mm)
  circle = ge.add_circle([4814.mm,1253.mm,1370.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 → Filters elbow
  grp = ents.add_group
  grp.name = "P-02 → Filters elbow"
  ge = grp.entities
  arc = ge.add_arc([4791.747323185283.mm,1202.9314771668862.mm,1346.mm], [0.000000,0.000000,1.000000], [0.913812,-0.406138,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4791.747323185283.mm,1202.9314771668862.mm,1370.mm], [-0.406138,-0.913812,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 → Filters
  grp = ents.add_group
  grp.name = "P-02 → Filters"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1096.mm)
  circle = ge.add_circle([4782.mm,1181.mm,1346.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-01 Diverter
  grp = ents.add_group
  grp.name = "3W-DV-01 Diverter"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 45.59999999999991.mm, 0.mm)
  circle = ge.add_circle([4782.mm,1158.2.mm,2156.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-01 Diverter
  grp = ents.add_group
  grp.name = "3W-DV-01 Diverter"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -22.800000000000182.mm)
  circle = ge.add_circle([4782.mm,1181.mm,2156.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Thumb screw TL near"] || model.materials.add("Thumb screw TL near")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Filters → DV-01 → IBC-2 side-entry
  grp = ents.add_group
  grp.name = "Filters → DV-01 → IBC-2 side-entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 972.mm)
  circle = ge.add_circle([4782.mm,1181.mm,1160.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 (50µ)"] || model.materials.add("Filter F1 (50µ)")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # Filters → DV-01 → IBC-2 side-entry elbow
  grp = ents.add_group
  grp.name = "Filters → DV-01 → IBC-2 side-entry elbow"
  ge = grp.entities
  arc = ge.add_arc([4782.mm,1205.mm,2132.mm], [0.000000,-1.000000,0.000000], [-1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4782.mm,1181.mm,2132.mm], [0.000000,0.000000,1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Filter F1 (50µ)"] || model.materials.add("Filter F1 (50µ)")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # Filters → DV-01 → IBC-2 side-entry
  grp = ents.add_group
  grp.name = "Filters → DV-01 → IBC-2 side-entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 261.mm, 0.mm)
  circle = ge.add_circle([4782.mm,1205.mm,2156.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 (50µ)"] || model.materials.add("Filter F1 (50µ)")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-2 Recycle Flange
  grp = ents.add_group
  grp.name = "IBC-2 Recycle Flange"
  ge = grp.entities
  circle = ge.add_circle([4782.mm,1307.mm,2156.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 → IBC-4 reject
  grp = ents.add_group
  grp.name = "DV-01 → IBC-4 reject"
  ge = grp.entities
  vec = Geom::Vector3d.new(17.850000000000364.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4782.mm,1181.mm,2156.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 → IBC-4 reject elbow
  grp = ents.add_group
  grp.name = "DV-01 → IBC-4 reject elbow"
  ge = grp.entities
  arc = ge.add_arc([4799.85.mm,1181.mm,2138.85.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 17.150000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4799.85.mm,1181.mm,2156.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 → IBC-4 reject
  grp = ents.add_group
  grp.name = "DV-01 → IBC-4 reject"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1026.85.mm)
  circle = ge.add_circle([4817.mm,1181.mm,2138.85.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 → IBC-4 reject elbow
  grp = ents.add_group
  grp.name = "DV-01 → IBC-4 reject elbow"
  ge = grp.entities
  arc = ge.add_arc([4817.mm,1205.mm,1112.mm], [0.000000,-1.000000,0.000000], [1.000000,-0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4817.mm,1181.mm,1112.mm], [0.000000,0.000000,-1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 → IBC-4 reject
  grp = ents.add_group
  grp.name = "DV-01 → IBC-4 reject"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 261.mm, 0.mm)
  circle = ge.add_circle([4817.mm,1205.mm,1088.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 Reject Flange
  grp = ents.add_group
  grp.name = "IBC-4 Reject Flange"
  ge = grp.entities
  circle = ge.add_circle([4817.mm,1307.mm,1088.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Water Plumbing"
  inst.layer = model.layers["Water Plumbing"]


# rev11: the brace cage is retired (rail ends now sit on wall-seat saddles), so the old
# "FP Brace Vert L (film)" duplicate-strike for the Ø89 swing pivot post is no longer needed.

# ── Major-component callouts (Labels tag — shown only in the "Labeled" scene) ──
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Pinhole Assembly" }
if inst
  bb = inst.bounds
  cx = bb.center.x; cy = bb.center.y; mz = bb.max.z
  anc = Geom::Point3d.new(cx, cy, mz)
  # Guard the recurring "leader tip floats in empty space" bug: a thin tall
  # outrigger (push pole, hanger rod) inflates the bbox so bb.max.z hovers
  # well above the actual mass at the centre. Cast straight down from the
  # bbox top; if THIS component's own geometry there sits far (>400mm) below,
  # snap the anchor onto it. Small floats (e.g. a tray rim) stay put.
  hit = model.raytest([Geom::Point3d.new(cx, cy, mz + 1.mm), Geom::Vector3d.new(0, 0, -1)])
  if hit && hit[1] && hit[1].include?(inst) && (mz - hit[0].z) > 400.mm
    anc = hit[0]
  end
  txt = entities.add_text("PINHOLE  Ø2.17mm", anc, Geom::Vector3d.new(-140.mm, -1120.mm, 630.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Film Plane Mechanism" }
if inst
  bb = inst.bounds
  cx = bb.center.x; cy = bb.center.y; mz = bb.max.z
  anc = Geom::Point3d.new(cx, cy, mz)
  # Guard the recurring "leader tip floats in empty space" bug: a thin tall
  # outrigger (push pole, hanger rod) inflates the bbox so bb.max.z hovers
  # well above the actual mass at the centre. Cast straight down from the
  # bbox top; if THIS component's own geometry there sits far (>400mm) below,
  # snap the anchor onto it. Small floats (e.g. a tray rim) stay put.
  hit = model.raytest([Geom::Point3d.new(cx, cy, mz + 1.mm), Geom::Vector3d.new(0, 0, -1)])
  if hit && hit[1] && hit[1].include?(inst) && (mz - hit[0].z) > 400.mm
    anc = hit[0]
  end
  txt = entities.add_text("FILM PLANE
4-corner tilt/swing", anc, Geom::Vector3d.new(400.mm, 0.mm, 1250.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Processing Tray" }
if inst
  bb = inst.bounds
  cx = bb.center.x; cy = bb.center.y; mz = bb.max.z
  anc = Geom::Point3d.new(cx, cy, mz)
  # Guard the recurring "leader tip floats in empty space" bug: a thin tall
  # outrigger (push pole, hanger rod) inflates the bbox so bb.max.z hovers
  # well above the actual mass at the centre. Cast straight down from the
  # bbox top; if THIS component's own geometry there sits far (>400mm) below,
  # snap the anchor onto it. Small floats (e.g. a tray rim) stay put.
  hit = model.raytest([Geom::Point3d.new(cx, cy, mz + 1.mm), Geom::Vector3d.new(0, 0, -1)])
  if hit && hit[1] && hit[1].include?(inst) && (mz - hit[0].z) > 400.mm
    anc = hit[0]
  end
  txt = entities.add_text("PROCESSING TRAY", anc, Geom::Vector3d.new(-250.mm, 0.mm, 650.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Equipment Panel" }
if inst
  bb = inst.bounds
  cx = bb.center.x; cy = bb.center.y; mz = bb.max.z
  anc = Geom::Point3d.new(cx, cy, mz)
  # Guard the recurring "leader tip floats in empty space" bug: a thin tall
  # outrigger (push pole, hanger rod) inflates the bbox so bb.max.z hovers
  # well above the actual mass at the centre. Cast straight down from the
  # bbox top; if THIS component's own geometry there sits far (>400mm) below,
  # snap the anchor onto it. Small floats (e.g. a tray rim) stay put.
  hit = model.raytest([Geom::Point3d.new(cx, cy, mz + 1.mm), Geom::Vector3d.new(0, 0, -1)])
  if hit && hit[1] && hit[1].include?(inst) && (mz - hit[0].z) > 400.mm
    anc = hit[0]
  end
  txt = entities.add_text("EQUIPMENT PANEL
pump / filter", anc, Geom::Vector3d.new(500.mm, 0.mm, 820.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "IBC Stack" }
if inst
  bb = inst.bounds
  cx = bb.center.x; cy = bb.center.y; mz = bb.max.z
  anc = Geom::Point3d.new(cx, cy, mz)
  # Guard the recurring "leader tip floats in empty space" bug: a thin tall
  # outrigger (push pole, hanger rod) inflates the bbox so bb.max.z hovers
  # well above the actual mass at the centre. Cast straight down from the
  # bbox top; if THIS component's own geometry there sits far (>400mm) below,
  # snap the anchor onto it. Small floats (e.g. a tray rim) stay put.
  hit = model.raytest([Geom::Point3d.new(cx, cy, mz + 1.mm), Geom::Vector3d.new(0, 0, -1)])
  if hit && hit[1] && hit[1].include?(inst) && (mz - hit[0].z) > 400.mm
    anc = hit[0]
  end
  txt = entities.add_text("IBC WATER STORAGE
4x tote", anc, Geom::Vector3d.new(600.mm, 0.mm, 1300.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Light-Trap Drum" }
if inst
  bb = inst.bounds
  cx = bb.center.x; cy = bb.center.y; mz = bb.max.z
  anc = Geom::Point3d.new(cx, cy, mz)
  # Guard the recurring "leader tip floats in empty space" bug: a thin tall
  # outrigger (push pole, hanger rod) inflates the bbox so bb.max.z hovers
  # well above the actual mass at the centre. Cast straight down from the
  # bbox top; if THIS component's own geometry there sits far (>400mm) below,
  # snap the anchor onto it. Small floats (e.g. a tray rim) stay put.
  hit = model.raytest([Geom::Point3d.new(cx, cy, mz + 1.mm), Geom::Vector3d.new(0, 0, -1)])
  if hit && hit[1] && hit[1].include?(inst) && (mz - hit[0].z) > 400.mm
    anc = hit[0]
  end
  txt = entities.add_text("LIGHT-TRAP DRUM
(entry)", anc, Geom::Vector3d.new(-650.mm, 0.mm, 1050.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Electrical" }
if inst
  bb = inst.bounds
  cx = bb.center.x; cy = bb.center.y; mz = bb.max.z
  anc = Geom::Point3d.new(cx, cy, mz)
  # Guard the recurring "leader tip floats in empty space" bug: a thin tall
  # outrigger (push pole, hanger rod) inflates the bbox so bb.max.z hovers
  # well above the actual mass at the centre. Cast straight down from the
  # bbox top; if THIS component's own geometry there sits far (>400mm) below,
  # snap the anchor onto it. Small floats (e.g. a tray rim) stay put.
  hit = model.raytest([Geom::Point3d.new(cx, cy, mz + 1.mm), Geom::Vector3d.new(0, 0, -1)])
  if hit && hit[1] && hit[1].include?(inst) && (mz - hit[0].z) > 400.mm
    anc = hit[0]
  end
  txt = entities.add_text("ELECTRICAL PANEL", anc, Geom::Vector3d.new(500.mm, 0.mm, 560.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Evap Cooler & Duct" }
if inst
  bb = inst.bounds
  cx = bb.center.x; cy = bb.center.y; mz = bb.max.z
  anc = Geom::Point3d.new(cx, cy, mz)
  # Guard the recurring "leader tip floats in empty space" bug: a thin tall
  # outrigger (push pole, hanger rod) inflates the bbox so bb.max.z hovers
  # well above the actual mass at the centre. Cast straight down from the
  # bbox top; if THIS component's own geometry there sits far (>400mm) below,
  # snap the anchor onto it. Small floats (e.g. a tray rim) stay put.
  hit = model.raytest([Geom::Point3d.new(cx, cy, mz + 1.mm), Geom::Vector3d.new(0, 0, -1)])
  if hit && hit[1] && hit[1].include?(inst) && (mz - hit[0].z) > 400.mm
    anc = hit[0]
  end
  txt = entities.add_text("EVAP COOLER", anc, Geom::Vector3d.new(300.mm, 0.mm, 1700.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Chemistry Shelf" }
if inst
  bb = inst.bounds
  cx = bb.center.x; cy = bb.center.y; mz = bb.max.z
  anc = Geom::Point3d.new(cx, cy, mz)
  # Guard the recurring "leader tip floats in empty space" bug: a thin tall
  # outrigger (push pole, hanger rod) inflates the bbox so bb.max.z hovers
  # well above the actual mass at the centre. Cast straight down from the
  # bbox top; if THIS component's own geometry there sits far (>400mm) below,
  # snap the anchor onto it. Small floats (e.g. a tray rim) stay put.
  hit = model.raytest([Geom::Point3d.new(cx, cy, mz + 1.mm), Geom::Vector3d.new(0, 0, -1)])
  if hit && hit[1] && hit[1].include?(inst) && (mz - hit[0].z) > 400.mm
    anc = hit[0]
  end
  txt = entities.add_text("CHEMISTRY SHELF", anc, Geom::Vector3d.new(-200.mm, -850.mm, 700.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
anc = Geom::Point3d.new(950.mm, -1400.mm, 450.mm)
txt = entities.add_text("SOLAR ARRAY
3× 200W (30° tilt)", anc, Geom::Vector3d.new(-200.mm, -700.mm, 700.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(5618.mm, 1181.mm, 2000.mm)
txt = entities.add_text("FAN A
(exhaust, IBC end)", anc, Geom::Vector3d.new(400.mm, 0.mm, 450.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(275.mm, 365.mm, 680.mm)
txt = entities.add_text("FAN B
(intake, door end)", anc, Geom::Vector3d.new(-350.mm, 0.mm, 1250.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(2060.mm, 60.mm, 600.mm)
txt = entities.add_text("BATTERY 1× 100Ah
(2nd pack ghosted = plug-in)", anc, Geom::Vector3d.new(-300.mm, -600.mm, 900.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1970.mm, 36.mm, 1415.mm)
txt = entities.add_text("CCT-E INVERTER
12->120V AC (cooler)", anc, Geom::Vector3d.new(-430.mm, -820.mm, 480.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1420.mm, -90.mm, 1950.mm)
txt = entities.add_text("EMERGENCY E-STOP
(external panel — kills all DC)", anc, Geom::Vector3d.new(-550.mm, -450.mm, 350.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(2400.mm, 150.mm, 65.mm)
txt = entities.add_text("WALKWAYS", anc, Geom::Vector3d.new(-200.mm, -850.mm, 750.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(2400.mm, 1180.mm, 60.mm)
txt = entities.add_text("SPRAY BAR", anc, Geom::Vector3d.new(315.mm, -1890.mm, 910.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(175.mm, 2287.mm, 1700.mm)
txt = entities.add_text("PIVOT POST Ø89
(panel swing axis)", anc, Geom::Vector3d.new(500.mm, -200.mm, 600.mm))
txt.layer = model.layers["Labels"] rescue nil

# ── In-model © + license credit (default layer → shown in every scene) ──
lbb = model.bounds
lanc = Geom::Point3d.new(lbb.min.x, lbb.min.y - 400.mm, lbb.min.z)
entities.add_text("© 2026 Alvin Richards
Licensed under GNU AGPLv3
alvinr.github.io/tbs", lanc)

model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags from earlier generator versions ──
keep_tags = ["Shell", "Walkways", "Processing Tray", "Pinhole", "Optical Cone", "Film Plane", "Combined Plate", "Pivot Axle", "Spray Bar", "Equipment Panel", "IBC Stack", "IBC Rack", "Light Trap", "Electrical", "Shelf", "Light Seal", "Lighting", "Evap Cooler", "Water Hookups", "Fans", "Water Plumbing", "Solar Array", "Labels"]
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

# Overview — everything visible, Labels OFF.
model.layers["Labels"].visible = false if model.layers["Labels"]
ovp = model.pages.add("Overview"); ovp.use_camera = true

# Labeled — same view + callouts on the major system components.
model.layers["Labels"].visible = true if model.layers["Labels"]
olp = model.pages.add("Labeled"); olp.use_camera = true
model.layers["Labels"].visible = false if model.layers["Labels"]

# Grouped scenes — translucent Shell (context) + the group's subsystems.
[["Film Plane & Pinhole", ["Pinhole", "Optical Cone", "Film Plane", "Combined Plate"]], ["Water Systems", ["Processing Tray", "Spray Bar", "Equipment Panel", "IBC Stack", "IBC Rack", "Shelf", "Water Hookups", "Water Plumbing"]], ["Electrical Systems", ["Electrical", "Lighting", "Solar Array"]], ["Hinge Panel & Drum", ["Light Trap", "Light Seal", "Pivot Axle"]], ["Ventilation", ["Evap Cooler", "Fans"]], ["Walkways", ["Walkways", "Combined Plate"]]].each { |name, tags|
  model.layers.each { |l| l.visible = (l == default_layer || l.name == "Shell" || tags.include?(l.name)) }
  page = model.pages.add(name)
  page.use_camera = true
}
model.layers.each { |l| l.visible = true }

model.commit_operation
{ success: true, model: "Overview",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
