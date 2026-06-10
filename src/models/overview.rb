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
  face = grp.entities.add_face([470.mm,0.mm,115.mm], [1155.mm,0.mm,115.mm], [1155.mm,300.mm,115.mm], [470.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near (widened)
  grp = ents.add_group
  grp.name = "Walkway Near (widened)"
  face = grp.entities.add_face([1155.mm,0.mm,115.mm], [2629.mm,0.mm,115.mm], [2629.mm,500.mm,115.mm], [1155.mm,500.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near (right section)
  grp = ents.add_group
  grp.name = "Walkway Near (right section)"
  face = grp.entities.add_face([2629.mm,0.mm,115.mm], [4329.mm,0.mm,115.mm], [4329.mm,300.mm,115.mm], [2629.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far
  grp = ents.add_group
  grp.name = "Walkway Far"
  face = grp.entities.add_face([470.mm,2062.mm,115.mm], [4329.mm,2062.mm,115.mm], [4329.mm,2362.mm,115.mm], [470.mm,2362.mm,115.mm])
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
  face = grp.entities.add_face([1594.17087800115.mm,0.mm,250.mm], [1794.17087800115.mm,0.mm,250.mm], [1794.17087800115.mm,12.mm,250.mm], [1594.17087800115.mm,12.mm,250.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay outside plate
  grp = ents.add_group
  grp.name = "Stay outside plate"
  face = grp.entities.add_face([1594.17087800115.mm,-52.mm,250.mm], [1794.17087800115.mm,-52.mm,250.mm], [1794.17087800115.mm,-40.mm,250.mm], [1594.17087800115.mm,-40.mm,250.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay eye
  grp = ents.add_group
  grp.name = "Stay eye"
  face = grp.entities.add_face([1679.17087800115.mm,12.mm,335.mm], [1709.17087800115.mm,12.mm,335.mm], [1709.17087800115.mm,67.mm,335.mm], [1679.17087800115.mm,67.mm,335.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1616.17087800115.mm,-58.mm,272.mm], [1632.17087800115.mm,-58.mm,272.mm], [1632.17087800115.mm,18.mm,272.mm], [1616.17087800115.mm,18.mm,272.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1616.17087800115.mm,-58.mm,412.mm], [1632.17087800115.mm,-58.mm,412.mm], [1632.17087800115.mm,18.mm,412.mm], [1616.17087800115.mm,18.mm,412.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1756.17087800115.mm,-58.mm,272.mm], [1772.17087800115.mm,-58.mm,272.mm], [1772.17087800115.mm,18.mm,272.mm], [1756.17087800115.mm,18.mm,272.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1756.17087800115.mm,-58.mm,412.mm], [1772.17087800115.mm,-58.mm,412.mm], [1772.17087800115.mm,18.mm,412.mm], [1756.17087800115.mm,18.mm,412.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay inside plate
  grp = ents.add_group
  grp.name = "Stay inside plate"
  face = grp.entities.add_face([1594.17087800115.mm,0.mm,1950.mm], [1794.17087800115.mm,0.mm,1950.mm], [1794.17087800115.mm,12.mm,1950.mm], [1594.17087800115.mm,12.mm,1950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay outside plate
  grp = ents.add_group
  grp.name = "Stay outside plate"
  face = grp.entities.add_face([1594.17087800115.mm,-52.mm,1950.mm], [1794.17087800115.mm,-52.mm,1950.mm], [1794.17087800115.mm,-40.mm,1950.mm], [1594.17087800115.mm,-40.mm,1950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay eye
  grp = ents.add_group
  grp.name = "Stay eye"
  face = grp.entities.add_face([1679.17087800115.mm,12.mm,2035.mm], [1709.17087800115.mm,12.mm,2035.mm], [1709.17087800115.mm,67.mm,2035.mm], [1679.17087800115.mm,67.mm,2035.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1616.17087800115.mm,-58.mm,1972.mm], [1632.17087800115.mm,-58.mm,1972.mm], [1632.17087800115.mm,18.mm,1972.mm], [1616.17087800115.mm,18.mm,1972.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1616.17087800115.mm,-58.mm,2112.mm], [1632.17087800115.mm,-58.mm,2112.mm], [1632.17087800115.mm,18.mm,2112.mm], [1616.17087800115.mm,18.mm,2112.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1756.17087800115.mm,-58.mm,1972.mm], [1772.17087800115.mm,-58.mm,1972.mm], [1772.17087800115.mm,18.mm,1972.mm], [1756.17087800115.mm,18.mm,1972.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1756.17087800115.mm,-58.mm,2112.mm], [1772.17087800115.mm,-58.mm,2112.mm], [1772.17087800115.mm,18.mm,2112.mm], [1756.17087800115.mm,18.mm,2112.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay hook (frame)
  grp = ents.add_group
  grp.name = "Stay hook (frame)"
  face = grp.entities.add_face([-10.mm,320.mm,315.mm], [50.mm,320.mm,315.mm], [50.mm,380.mm,315.mm], [-10.mm,380.mm,315.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Left cantilever 1 foot plate"] || model.materials.add("Left cantilever 1 foot plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay hook (frame)
  grp = ents.add_group
  grp.name = "Stay hook (frame)"
  face = grp.entities.add_face([-10.mm,320.mm,2015.mm], [50.mm,320.mm,2015.mm], [50.mm,380.mm,2015.mm], [-10.mm,380.mm,2015.mm])
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
  face = grp.entities.add_face([5240.mm,1046.mm,250.mm], [5258.mm,1046.mm,250.mm], [5258.mm,1316.mm,250.mm], [5240.mm,1316.mm,250.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2060.mm)
  mat = model.materials["Equipment Panel (ply)"] || model.materials.add("Equipment Panel (ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-01 (Blue)
  grp = ents.add_group
  grp.name = "Pump P-01 (Blue)"
  face = grp.entities.add_face([5140.mm,1045.5.mm,1370.mm], [5240.mm,1045.5.mm,1370.mm], [5240.mm,1172.5.mm,1370.mm], [5140.mm,1172.5.mm,1370.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-02 (Brown)
  grp = ents.add_group
  grp.name = "Pump P-02 (Brown)"
  face = grp.entities.add_face([5140.mm,1189.5.mm,1370.mm], [5240.mm,1189.5.mm,1370.mm], [5240.mm,1316.5.mm,1370.mm], [5140.mm,1316.5.mm,1370.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-04 (Tray drain)
  grp = ents.add_group
  grp.name = "Pump P-04 (Tray drain)"
  face = grp.entities.add_face([5140.mm,1045.5.mm,1628.mm], [5240.mm,1045.5.mm,1628.mm], [5240.mm,1172.5.mm,1628.mm], [5140.mm,1172.5.mm,1628.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-03 (Waste evac)
  grp = ents.add_group
  grp.name = "Pump P-03 (Waste evac)"
  face = grp.entities.add_face([5140.mm,1189.5.mm,1628.mm], [5240.mm,1189.5.mm,1628.mm], [5240.mm,1316.5.mm,1628.mm], [5140.mm,1316.5.mm,1628.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-05 (Brown drain)
  grp = ents.add_group
  grp.name = "Pump P-05 (Brown drain)"
  face = grp.entities.add_face([5140.mm,1189.5.mm,1996.mm], [5240.mm,1189.5.mm,1996.mm], [5240.mm,1316.5.mm,1996.mm], [5140.mm,1316.5.mm,1996.mm])
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
  circle = ge.add_circle([5177.mm,1109.mm,1996.mm], [0,0,1], 63.5.mm, 24)
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
  circle = ge.add_circle([5175.mm,1181.mm,250.mm], [0,0,1], 65.mm, 24)
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
  circle = ge.add_circle([5175.mm,1181.mm,620.mm], [0,0,1], 65.mm, 24)
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
  circle = ge.add_circle([5175.mm,1181.mm,990.mm], [0,0,1], 65.mm, 24)
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
  face = grp.entities.add_face([5240.mm,1223.mm,250.mm], [5420.mm,1223.mm,250.mm], [5420.mm,1241.mm,250.mm], [5240.mm,1241.mm,250.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1970.mm)
  mat = model.materials["Equipment Panel (ply)"] || model.materials.add("Equipment Panel (ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Drain-riser spine flange (ply)
  grp = ents.add_group
  grp.name = "Drain-riser spine flange (ply)"
  face = grp.entities.add_face([5402.mm,1226.mm,250.mm], [5420.mm,1226.mm,250.mm], [5420.mm,1280.mm,250.mm], [5402.mm,1280.mm,250.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1970.mm)
  mat = model.materials["Equipment Panel (ply)"] || model.materials.add("Equipment Panel (ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Drain-riser spine top shelf (ply)
  grp = ents.add_group
  grp.name = "Drain-riser spine top shelf (ply)"
  face = grp.entities.add_face([5240.mm,1160.mm,2220.mm], [5460.mm,1160.mm,2220.mm], [5460.mm,1241.mm,2220.mm], [5240.mm,1241.mm,2220.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Equipment Panel (ply)"] || model.materials.add("Equipment Panel (ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Blue fill pipe clamp
  grp = ents.add_group
  grp.name = "Blue fill pipe clamp"
  face = grp.entities.add_face([5420.mm,1165.mm,2238.mm], [5456.mm,1165.mm,2238.mm], [5456.mm,1197.mm,2238.mm], [5420.mm,1197.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
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
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([4734.mm,1266.mm,0.mm], [4784.mm,1266.mm,0.mm], [4784.mm,1316.mm,0.mm], [4734.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([5258.5.mm,1046.mm,0.mm], [5308.5.mm,1046.mm,0.mm], [5308.5.mm,1096.mm,0.mm], [5258.5.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([5258.5.mm,1266.mm,0.mm], [5308.5.mm,1266.mm,0.mm], [5308.5.mm,1316.mm,0.mm], [5258.5.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([5783.mm,1046.mm,0.mm], [5833.mm,1046.mm,0.mm], [5833.mm,1096.mm,0.mm], [5783.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([5783.mm,1266.mm,0.mm], [5833.mm,1266.mm,0.mm], [5833.mm,1316.mm,0.mm], [5783.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Spine
  grp = ents.add_group
  grp.name = "Rack Spine"
  face = grp.entities.add_face([4734.mm,1046.mm,960.mm], [5833.mm,1046.mm,960.mm], [5833.mm,1096.mm,960.mm], [4734.mm,1096.mm,960.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Spine
  grp = ents.add_group
  grp.name = "Rack Spine"
  face = grp.entities.add_face([4734.mm,1266.mm,960.mm], [5833.mm,1266.mm,960.mm], [5833.mm,1316.mm,960.mm], [4734.mm,1316.mm,960.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Platform Beam
  grp = ents.add_group
  grp.name = "Rack Platform Beam"
  face = grp.entities.add_face([4734.mm,30.mm,960.mm], [4784.mm,30.mm,960.mm], [4784.mm,2332.mm,960.mm], [4734.mm,2332.mm,960.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Platform Beam
  grp = ents.add_group
  grp.name = "Rack Platform Beam"
  face = grp.entities.add_face([5258.5.mm,30.mm,960.mm], [5308.5.mm,30.mm,960.mm], [5308.5.mm,2332.mm,960.mm], [5258.5.mm,2332.mm,960.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Platform Beam
  grp = ents.add_group
  grp.name = "Rack Platform Beam"
  face = grp.entities.add_face([5783.mm,30.mm,960.mm], [5833.mm,30.mm,960.mm], [5833.mm,2332.mm,960.mm], [5783.mm,2332.mm,960.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Panel Frame Upright
  grp = ents.add_group
  grp.name = "Panel Frame Upright"
  face = grp.entities.add_face([5258.5.mm,1046.mm,1010.mm], [5308.5.mm,1046.mm,1010.mm], [5308.5.mm,1096.mm,1010.mm], [5258.5.mm,1096.mm,1010.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1300.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Panel Frame Upright
  grp = ents.add_group
  grp.name = "Panel Frame Upright"
  face = grp.entities.add_face([5258.5.mm,1266.mm,1010.mm], [5308.5.mm,1266.mm,1010.mm], [5308.5.mm,1316.mm,1010.mm], [5258.5.mm,1316.mm,1010.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1300.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Panel Frame Top Rail
  grp = ents.add_group
  grp.name = "Panel Frame Top Rail"
  face = grp.entities.add_face([5258.5.mm,1046.mm,2260.mm], [5308.5.mm,1046.mm,2260.mm], [5308.5.mm,1316.mm,2260.mm], [5258.5.mm,1316.mm,2260.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Panel Frame Floor Beam
  grp = ents.add_group
  grp.name = "Panel Frame Floor Beam"
  face = grp.entities.add_face([5258.5.mm,1046.mm,0.mm], [5308.5.mm,1046.mm,0.mm], [5308.5.mm,1316.mm,0.mm], [5258.5.mm,1316.mm,0.mm])
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

  # Foot Flange Plate
  grp = ents.add_group
  grp.name = "Foot Flange Plate"
  face = grp.entities.add_face([5208.5.mm,996.mm,0.mm], [5358.5.mm,996.mm,0.mm], [5358.5.mm,1146.mm,0.mm], [5208.5.mm,1146.mm,0.mm])
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
  circle = ge.add_circle([5233.5.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5233.5.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5333.5.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5333.5.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
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
  face = grp.entities.add_face([5208.5.mm,1216.mm,0.mm], [5358.5.mm,1216.mm,0.mm], [5358.5.mm,1366.mm,0.mm], [5208.5.mm,1366.mm,0.mm])
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
  circle = ge.add_circle([5233.5.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5233.5.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5333.5.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5333.5.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
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
  face = grp.entities.add_face([5733.mm,996.mm,0.mm], [5883.mm,996.mm,0.mm], [5883.mm,1146.mm,0.mm], [5733.mm,1146.mm,0.mm])
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
  circle = ge.add_circle([5758.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5758.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5858.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5858.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
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
  face = grp.entities.add_face([5733.mm,1216.mm,0.mm], [5883.mm,1216.mm,0.mm], [5883.mm,1366.mm,0.mm], [5733.mm,1366.mm,0.mm])
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
  circle = ge.add_circle([5758.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5758.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5858.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5858.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
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
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Seat
  grp = ents.add_group
  grp.name = "Wall Bracket Seat"
  face = grp.entities.add_face([4724.mm,0.mm,950.mm], [4794.mm,0.mm,950.mm], [4794.mm,110.mm,950.mm], [4724.mm,110.mm,950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Gusset
  grp = ents.add_group
  grp.name = "Wall Bracket Gusset"
  ge = grp.entities
  f = ge.add_face([4755.mm,110.mm,950.mm], [4755.mm,0.mm,950.mm], [4755.mm,0.mm,750.mm])
  f.pushpull(8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Seat
  grp = ents.add_group
  grp.name = "Wall Bracket Seat"
  face = grp.entities.add_face([4724.mm,2252.mm,950.mm], [4794.mm,2252.mm,950.mm], [4794.mm,2362.mm,950.mm], [4724.mm,2362.mm,950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Gusset
  grp = ents.add_group
  grp.name = "Wall Bracket Gusset"
  ge = grp.entities
  f = ge.add_face([4755.mm,2252.mm,950.mm], [4755.mm,2362.mm,950.mm], [4755.mm,2362.mm,750.mm])
  f.pushpull(8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Seat
  grp = ents.add_group
  grp.name = "Wall Bracket Seat"
  face = grp.entities.add_face([5248.5.mm,0.mm,950.mm], [5318.5.mm,0.mm,950.mm], [5318.5.mm,110.mm,950.mm], [5248.5.mm,110.mm,950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Gusset
  grp = ents.add_group
  grp.name = "Wall Bracket Gusset"
  ge = grp.entities
  f = ge.add_face([5279.5.mm,110.mm,950.mm], [5279.5.mm,0.mm,950.mm], [5279.5.mm,0.mm,750.mm])
  f.pushpull(8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Seat
  grp = ents.add_group
  grp.name = "Wall Bracket Seat"
  face = grp.entities.add_face([5248.5.mm,2252.mm,950.mm], [5318.5.mm,2252.mm,950.mm], [5318.5.mm,2362.mm,950.mm], [5248.5.mm,2362.mm,950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Gusset
  grp = ents.add_group
  grp.name = "Wall Bracket Gusset"
  ge = grp.entities
  f = ge.add_face([5279.5.mm,2252.mm,950.mm], [5279.5.mm,2362.mm,950.mm], [5279.5.mm,2362.mm,750.mm])
  f.pushpull(8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Seat
  grp = ents.add_group
  grp.name = "Wall Bracket Seat"
  face = grp.entities.add_face([5773.mm,0.mm,950.mm], [5843.mm,0.mm,950.mm], [5843.mm,110.mm,950.mm], [5773.mm,110.mm,950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Gusset
  grp = ents.add_group
  grp.name = "Wall Bracket Gusset"
  ge = grp.entities
  f = ge.add_face([5804.mm,110.mm,950.mm], [5804.mm,0.mm,950.mm], [5804.mm,0.mm,750.mm])
  f.pushpull(8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Seat
  grp = ents.add_group
  grp.name = "Wall Bracket Seat"
  face = grp.entities.add_face([5773.mm,2252.mm,950.mm], [5843.mm,2252.mm,950.mm], [5843.mm,2362.mm,950.mm], [5773.mm,2362.mm,950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Gusset
  grp = ents.add_group
  grp.name = "Wall Bracket Gusset"
  ge = grp.entities
  f = ge.add_face([5804.mm,2252.mm,950.mm], [5804.mm,2362.mm,950.mm], [5804.mm,2362.mm,750.mm])
  f.pushpull(8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
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
  # Electrical Panel (EP)
  grp = ents.add_group
  grp.name = "Electrical Panel (EP)"
  face = grp.entities.add_face([1910.mm,0.mm,1500.mm], [2210.mm,0.mm,1500.mm], [2210.mm,160.mm,1500.mm], [1910.mm,160.mm,1500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(600.mm)
  mat = model.materials["Electrical Panel (EP)"] || model.materials.add("Electrical Panel (EP)")
  mat.color = Sketchup::Color.new(245, 197, 24)
  mat.alpha = 1.0
  grp.material = mat

  # Battery 1 (12V 100Ah LiFePO4)
  grp = ents.add_group
  grp.name = "Battery 1 (12V 100Ah LiFePO4)"
  face = grp.entities.add_face([1810.mm,0.mm,150.mm], [2050.mm,0.mm,150.mm], [2050.mm,120.mm,150.mm], [1810.mm,120.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(500.mm)
  mat = model.materials["Battery 1 (12V 100Ah LiFePO4)"] || model.materials.add("Battery 1 (12V 100Ah LiFePO4)")
  mat.color = Sketchup::Color.new(106, 90, 205)
  mat.alpha = 1.0
  grp.material = mat

  # Battery 2 (12V 100Ah LiFePO4)
  grp = ents.add_group
  grp.name = "Battery 2 (12V 100Ah LiFePO4)"
  face = grp.entities.add_face([2070.mm,0.mm,150.mm], [2310.mm,0.mm,150.mm], [2310.mm,120.mm,150.mm], [2070.mm,120.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(500.mm)
  mat = model.materials["Battery 1 (12V 100Ah LiFePO4)"] || model.materials.add("Battery 1 (12V 100Ah LiFePO4)")
  mat.color = Sketchup::Color.new(106, 90, 205)
  mat.alpha = 1.0
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
  face = grp.entities.add_face([3729.mm,300.mm,1053.mm], [4329.mm,300.mm,1053.mm], [4329.mm,600.mm,1053.mm], [3729.mm,600.mm,1053.mm])
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
  circle = ge.add_circle([3749.mm,320.mm,1075.mm], [0,0,1], 5.mm, 12)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(1313.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Shelf ceiling plate (to rib)
  grp = ents.add_group
  grp.name = "Shelf ceiling plate (to rib)"
  face = grp.entities.add_face([3699.mm,290.mm,2382.mm], [3799.mm,290.mm,2382.mm], [3799.mm,350.mm,2382.mm], [3699.mm,350.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Shelf ceiling bolt M10
  grp = ents.add_group
  grp.name = "Shelf ceiling bolt M10"
  ge = grp.entities
  circle = ge.add_circle([3717.mm,320.mm,2382.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Shelf ceiling bolt M10
  grp = ents.add_group
  grp.name = "Shelf ceiling bolt M10"
  ge = grp.entities
  circle = ge.add_circle([3781.mm,320.mm,2382.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Shelf Hanger Rod
  grp = ents.add_group
  grp.name = "Shelf Hanger Rod"
  ge = grp.entities
  circle = ge.add_circle([3749.mm,580.mm,1075.mm], [0,0,1], 5.mm, 12)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(1313.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Shelf ceiling plate (to rib)
  grp = ents.add_group
  grp.name = "Shelf ceiling plate (to rib)"
  face = grp.entities.add_face([3699.mm,550.mm,2382.mm], [3799.mm,550.mm,2382.mm], [3799.mm,610.mm,2382.mm], [3699.mm,610.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Shelf ceiling bolt M10
  grp = ents.add_group
  grp.name = "Shelf ceiling bolt M10"
  ge = grp.entities
  circle = ge.add_circle([3717.mm,580.mm,2382.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Shelf ceiling bolt M10
  grp = ents.add_group
  grp.name = "Shelf ceiling bolt M10"
  ge = grp.entities
  circle = ge.add_circle([3781.mm,580.mm,2382.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Shelf Hanger Rod
  grp = ents.add_group
  grp.name = "Shelf Hanger Rod"
  ge = grp.entities
  circle = ge.add_circle([4309.mm,320.mm,1075.mm], [0,0,1], 5.mm, 12)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(1313.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Shelf ceiling plate (to rib)
  grp = ents.add_group
  grp.name = "Shelf ceiling plate (to rib)"
  face = grp.entities.add_face([4259.mm,290.mm,2382.mm], [4359.mm,290.mm,2382.mm], [4359.mm,350.mm,2382.mm], [4259.mm,350.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Shelf ceiling bolt M10
  grp = ents.add_group
  grp.name = "Shelf ceiling bolt M10"
  ge = grp.entities
  circle = ge.add_circle([4277.mm,320.mm,2382.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Shelf ceiling bolt M10
  grp = ents.add_group
  grp.name = "Shelf ceiling bolt M10"
  ge = grp.entities
  circle = ge.add_circle([4341.mm,320.mm,2382.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Shelf Hanger Rod
  grp = ents.add_group
  grp.name = "Shelf Hanger Rod"
  ge = grp.entities
  circle = ge.add_circle([4309.mm,580.mm,1075.mm], [0,0,1], 5.mm, 12)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(1313.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Shelf ceiling plate (to rib)
  grp = ents.add_group
  grp.name = "Shelf ceiling plate (to rib)"
  face = grp.entities.add_face([4259.mm,550.mm,2382.mm], [4359.mm,550.mm,2382.mm], [4359.mm,610.mm,2382.mm], [4259.mm,610.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Shelf ceiling bolt M10
  grp = ents.add_group
  grp.name = "Shelf ceiling bolt M10"
  ge = grp.entities
  circle = ge.add_circle([4277.mm,580.mm,2382.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Shelf ceiling bolt M10
  grp = ents.add_group
  grp.name = "Shelf ceiling bolt M10"
  ge = grp.entities
  circle = ge.add_circle([4341.mm,580.mm,2382.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
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
  face = grp.entities.add_face([5235.mm,1176.mm,2270.mm], [5245.mm,1176.mm,2270.mm], [5245.mm,1186.mm,2270.mm], [5235.mm,1186.mm,2270.mm])
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
  vec = Geom::Vector3d.new(0.mm, 1962.mm, 0.mm)
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
  arc = ge.add_arc([5618.mm,1982.mm,2344.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 14.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5618.mm,1982.mm,2358.mm], [0.000000,1.000000,0.000000], 7.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -44.mm)
  circle = ge.add_circle([5618.mm,1996.mm,2344.mm], vec, 7.mm, 16)
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
  vec = Geom::Vector3d.new(-226.mm, 0.mm, 0.mm)
  circle = ge.add_circle([300.mm,20.mm,2358.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cable Trunking (40x25 PVC)"] || model.materials.add("Cable Trunking (40x25 PVC)")
  mat.color = Sketchup::Color.new(154, 160, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Conduit to Fan B (intake, Cct B) elbow
  grp = ents.add_group
  grp.name = "Conduit to Fan B (intake, Cct B) elbow"
  ge = grp.entities
  arc = ge.add_arc([74.mm,34.mm,2358.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,-1.000000], 14.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([74.mm,20.mm,2358.mm], [-1.000000,0.000000,0.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Cable Trunking (40x25 PVC)"] || model.materials.add("Cable Trunking (40x25 PVC)")
  mat.color = Sketchup::Color.new(154, 160, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Conduit to Fan B (intake, Cct B)
  grp = ents.add_group
  grp.name = "Conduit to Fan B (intake, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 331.mm, 0.mm)
  circle = ge.add_circle([60.mm,34.mm,2358.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cable Trunking (40x25 PVC)"] || model.materials.add("Cable Trunking (40x25 PVC)")
  mat.color = Sketchup::Color.new(154, 160, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B Flex Anchor (door-frame top rail — flex whip not shown)
  grp = ents.add_group
  grp.name = "Fan B Flex Anchor (door-frame top rail — flex whip not shown)"
  face = grp.entities.add_face([40.mm,340.mm,2333.mm], [85.mm,340.mm,2333.mm], [85.mm,390.mm,2333.mm], [40.mm,390.mm,2333.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pull Switch (ceiling)"] || model.materials.add("Pull Switch (ceiling)")
  mat.color = Sketchup::Color.new(216, 216, 240)
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
  face = grp.entities.add_face([5593.mm,1896.mm,2100.mm], [5893.mm,1896.mm,2100.mm], [5893.mm,2096.mm,2100.mm], [5593.mm,2096.mm,2100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan A (exhaust) baffle duct"] || model.materials.add("Fan A (exhaust) baffle duct")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 0.5
  grp.material = mat

  # Fan A (exhaust) baffle plate 1
  grp = ents.add_group
  grp.name = "Fan A (exhaust) baffle plate 1"
  face = grp.entities.add_face([5689.mm,1896.mm,2100.mm], [5697.mm,1896.mm,2100.mm], [5697.mm,2021.mm,2100.mm], [5689.mm,2021.mm,2100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) baffle plate 2
  grp = ents.add_group
  grp.name = "Fan A (exhaust) baffle plate 2"
  face = grp.entities.add_face([5789.mm,1971.mm,2100.mm], [5797.mm,1971.mm,2100.mm], [5797.mm,2096.mm,2100.mm], [5789.mm,2096.mm,2100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan frame top
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan frame top"
  face = grp.entities.add_face([5593.mm,1896.mm,2275.mm], [5643.mm,1896.mm,2275.mm], [5643.mm,2096.mm,2275.mm], [5593.mm,2096.mm,2275.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan frame bottom
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan frame bottom"
  face = grp.entities.add_face([5593.mm,1896.mm,2100.mm], [5643.mm,1896.mm,2100.mm], [5643.mm,2096.mm,2100.mm], [5593.mm,2096.mm,2100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan frame left
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan frame left"
  face = grp.entities.add_face([5593.mm,1896.mm,2125.mm], [5643.mm,1896.mm,2125.mm], [5643.mm,1921.mm,2125.mm], [5593.mm,1921.mm,2125.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Fan A (exhaust) baffle plate 1"] || model.materials.add("Fan A (exhaust) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan frame right
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan frame right"
  face = grp.entities.add_face([5593.mm,2071.mm,2125.mm], [5643.mm,2071.mm,2125.mm], [5643.mm,2096.mm,2125.mm], [5593.mm,2096.mm,2125.mm])
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
  circle = ge.add_circle([5593.mm,1996.mm,2200.mm], [1,0,0], 19.5.mm, 24)
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
  face = grp.entities.add_face([5615.5.mm,1981.mm,2219.5.mm], [5621.5.mm,1981.mm,2219.5.mm], [5621.5.mm,2011.mm,2219.5.mm], [5615.5.mm,2011.mm,2219.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.5.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan blade down
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan blade down"
  face = grp.entities.add_face([5615.5.mm,1981.mm,2134.mm], [5621.5.mm,1981.mm,2134.mm], [5621.5.mm,2011.mm,2134.mm], [5615.5.mm,2011.mm,2134.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.5.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan blade left
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan blade left"
  face = grp.entities.add_face([5615.5.mm,1930.mm,2185.mm], [5621.5.mm,1930.mm,2185.mm], [5621.5.mm,1976.5.mm,2185.mm], [5615.5.mm,1976.5.mm,2185.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) fan blade right
  grp = ents.add_group
  grp.name = "Fan A (exhaust) fan blade right"
  face = grp.entities.add_face([5615.5.mm,2015.5.mm,2185.mm], [5621.5.mm,2015.5.mm,2185.mm], [5621.5.mm,2062.mm,2185.mm], [5615.5.mm,2062.mm,2185.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) wall flange
  grp = ents.add_group
  grp.name = "Fan A (exhaust) wall flange"
  face = grp.entities.add_face([5888.mm,1866.mm,2070.mm], [5893.mm,1866.mm,2070.mm], [5893.mm,2126.mm,2070.mm], [5888.mm,2126.mm,2070.mm])
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
  circle = ge.add_circle([5886.5.mm,1881.mm,2085.mm], [1,0,0], 5.mm, 24)
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
  circle = ge.add_circle([5886.5.mm,1881.mm,2315.mm], [1,0,0], 5.mm, 24)
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
  circle = ge.add_circle([5886.5.mm,2111.mm,2085.mm], [1,0,0], 5.mm, 24)
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
  circle = ge.add_circle([5886.5.mm,2111.mm,2315.mm], [1,0,0], 5.mm, 24)
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
  face = grp.entities.add_face([5893.mm,1896.mm,2135.mm], [5933.mm,1896.mm,2135.mm], [5933.mm,2096.mm,2135.mm], [5893.mm,2096.mm,2135.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(130.mm)
  mat = model.materials["Fan A (exhaust) louvre grille"] || model.materials.add("Fan A (exhaust) louvre grille")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 0.55
  grp.material = mat

  # Fan A (exhaust) louvre slat
  grp = ents.add_group
  grp.name = "Fan A (exhaust) louvre slat"
  face = grp.entities.add_face([5895.mm,1900.mm,2146.5.mm], [5931.mm,1900.mm,2146.5.mm], [5931.mm,2092.mm,2146.5.mm], [5895.mm,2092.mm,2146.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) louvre slat
  grp = ents.add_group
  grp.name = "Fan A (exhaust) louvre slat"
  face = grp.entities.add_face([5895.mm,1900.mm,2172.5.mm], [5931.mm,1900.mm,2172.5.mm], [5931.mm,2092.mm,2172.5.mm], [5895.mm,2092.mm,2172.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) louvre slat
  grp = ents.add_group
  grp.name = "Fan A (exhaust) louvre slat"
  face = grp.entities.add_face([5895.mm,1900.mm,2198.5.mm], [5931.mm,1900.mm,2198.5.mm], [5931.mm,2092.mm,2198.5.mm], [5895.mm,2092.mm,2198.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) louvre slat
  grp = ents.add_group
  grp.name = "Fan A (exhaust) louvre slat"
  face = grp.entities.add_face([5895.mm,1900.mm,2224.5.mm], [5931.mm,1900.mm,2224.5.mm], [5931.mm,2092.mm,2224.5.mm], [5895.mm,2092.mm,2224.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan A (exhaust) louvre slat
  grp = ents.add_group
  grp.name = "Fan A (exhaust) louvre slat"
  face = grp.entities.add_face([5895.mm,1900.mm,2250.5.mm], [5931.mm,1900.mm,2250.5.mm], [5931.mm,2092.mm,2250.5.mm], [5895.mm,2092.mm,2250.5.mm])
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
  circle = ge.add_circle([2399.mm,12.mm,40.mm], [1,0,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(2250.mm)
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

  # TAP-01 Riser (3/4in)
  grp = ents.add_group
  grp.name = "TAP-01 Riser (3/4in)"
  ge = grp.entities
  circle = ge.add_circle([3729.mm,12.mm,40.mm], [0,0,1], 12.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(1160.mm)
  mat = model.materials["Blue Supply Trunk (1/2in HDPE)"] || model.materials.add("Blue Supply Trunk (1/2in HDPE)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # TAP-01 (chem tap)
  grp = ents.add_group
  grp.name = "TAP-01 (chem tap)"
  face = grp.entities.add_face([3714.mm,12.mm,1200.mm], [3744.mm,12.mm,1200.mm], [3744.mm,142.mm,1200.mm], [3714.mm,142.mm,1200.mm])
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -376.mm)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -376.mm)
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
  circle = ge.add_circle([5220.mm,1253.mm,1996.mm], vec, 12.mm, 16)
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
  vec = Geom::Vector3d.new(96.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5220.mm,1253.mm,1628.mm], vec, 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 151.48000000000002.mm)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1161.mm)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1423.8899999999999.mm)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 151.mm)
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
  arc = ge.add_arc([4526.mm,80.mm,171.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4550.mm,80.mm,171.mm], [0.000000,0.000000,1.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(-31.300000000000182.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4526.mm,80.mm,195.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([4494.7.mm,65.3.mm,195.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 14.700000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4494.7.mm,80.mm,195.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, -7.802999999999997.mm, 0.mm)
  circle = ge.add_circle([4480.mm,65.3.mm,195.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([4480.mm,57.497.mm,187.50300000000001.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 7.496999999999999.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4480.mm,57.497.mm,195.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -133.50300000000001.mm)
  circle = ge.add_circle([4480.mm,50.mm,187.50300000000001.mm], vec, 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 1083.mm, 0.mm)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1574.48.mm)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -670.mm)
  circle = ge.add_circle([5190.mm,1181.mm,1370.mm], vec, 12.mm, 16)
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


# rev11: the brace cage is retired (rail ends now sit on wall-seat saddles), so the old
# "FP Brace Vert L (film)" duplicate-strike for the Ø89 swing pivot post is no longer needed.

# ── Major-component callouts (Labels tag — shown only in the "Labeled" scene) ──
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Pinhole Assembly" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("PINHOLE  Ø2.17mm", anc, Geom::Vector3d.new(-200.mm, -1600.mm, 900.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Film Plane Mechanism" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("FILM PLANE
4-corner tilt/swing", anc, Geom::Vector3d.new(400.mm, 0.mm, 1250.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Processing Tray" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("PROCESSING TRAY", anc, Geom::Vector3d.new(-250.mm, 0.mm, 650.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Spray Bar" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("SPRAY BAR", anc, Geom::Vector3d.new(450.mm, -2700.mm, 1300.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Equipment Panel" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("EQUIPMENT PANEL
pump / filter", anc, Geom::Vector3d.new(500.mm, 0.mm, 820.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "IBC Stack" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("IBC WATER STORAGE
4x tote", anc, Geom::Vector3d.new(600.mm, 0.mm, 1300.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Light-Trap Drum" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("LIGHT-TRAP DRUM
(entry)", anc, Geom::Vector3d.new(-650.mm, 0.mm, 1050.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Electrical" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("ELECTRICAL PANEL", anc, Geom::Vector3d.new(500.mm, 0.mm, 560.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Evap Cooler & Duct" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("EVAP COOLER", anc, Geom::Vector3d.new(300.mm, 0.mm, 1700.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
anc = Geom::Point3d.new(5618.mm, 1996.mm, 2250.mm)
txt = entities.add_text("FAN A
(exhaust, IBC end)", anc, Geom::Vector3d.new(400.mm, 0.mm, 450.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(275.mm, 365.mm, 680.mm)
txt = entities.add_text("FAN B
(intake, door end)", anc, Geom::Vector3d.new(-350.mm, 0.mm, 1250.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(2060.mm, 60.mm, 600.mm)
txt = entities.add_text("BATTERY BANK
(LiFePO4)", anc, Geom::Vector3d.new(-300.mm, -600.mm, 900.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(2400.mm, 150.mm, 65.mm)
txt = entities.add_text("WALKWAYS", anc, Geom::Vector3d.new(-200.mm, -850.mm, 750.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(175.mm, 2287.mm, 1700.mm)
txt = entities.add_text("PIVOT POST Ø89
(panel swing axis)", anc, Geom::Vector3d.new(500.mm, -200.mm, 600.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4029.mm, 450.mm, 1075.mm)
txt = entities.add_text("CHEMISTRY SHELF", anc, Geom::Vector3d.new(-200.mm, -850.mm, 700.mm))
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
keep_tags = ["Shell", "Walkways", "Processing Tray", "Pinhole", "Optical Cone", "Film Plane", "Pivot Axle", "Spray Bar", "Equipment Panel", "IBC Stack", "IBC Rack", "Light Trap", "Electrical", "Shelf", "Light Seal", "Lighting", "Evap Cooler", "Water Hookups", "Fans", "Water Plumbing", "Labels"]
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
[["Film Plane & Pinhole", ["Pinhole", "Optical Cone", "Film Plane"]], ["Water Systems", ["Processing Tray", "Spray Bar", "Equipment Panel", "IBC Stack", "IBC Rack", "Shelf", "Water Hookups", "Water Plumbing"]], ["Electrical Systems", ["Electrical", "Lighting"]], ["Hinge Panel & Drum", ["Light Trap", "Light Seal", "Pivot Axle"]], ["Ventilation", ["Evap Cooler", "Fans"]], ["Walkways", ["Walkways"]]].each { |name, tags|
  model.layers.each { |l| l.visible = (l == default_layer || l.name == "Shell" || tags.include?(l.name)) }
  page = model.pages.add(name)
  page.use_camera = true
}
model.layers.each { |l| l.visible = true }

model.commit_operation
{ success: true, model: "Overview",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
