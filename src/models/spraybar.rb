model = Sketchup.active_model
model.start_operation("TBS-001 Spray-Bar Gantry", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# Idempotent rebuild: erase all prior groups/instances.
to_erase = entities.to_a.select { |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance)
}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each { |p| model.pages.erase(p) }

  model.layers.add("Beam") unless model.layers["Beam"]
  model.layers.add("Carriages") unless model.layers["Carriages"]
  model.layers.add("Feed & Pole") unless model.layers["Feed & Pole"]
  model.layers.add("Tray") unless model.layers["Tray"]

  # ═══ Spray Beam ═══
  defn = model.definitions.add("Spray Beam")
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

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Spray Beam"
  inst.layer = model.layers["Beam"]

  # ═══ Wheel Carriages ═══
  defn = model.definitions.add("Wheel Carriages")
  ents = defn.entities
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

  # Tray Floor (ref)
  grp = ents.add_group
  grp.name = "Tray Floor (ref)"
  face = grp.entities.add_face([410.mm,1020.mm,0.mm], [4389.mm,1020.mm,0.mm], [4389.mm,1340.mm,0.mm], [410.mm,1340.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Tray Floor (ref)"] || model.materials.add("Tray Floor (ref)")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 0.25
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Wheel Carriages"
  inst.layer = model.layers["Carriages"]

  # ═══ Feed & Push Pole ═══
  defn = model.definitions.add("Feed & Push Pole")
  ents = defn.entities
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
  inst.name = "Feed & Push Pole"
  inst.layer = model.layers["Feed & Pole"]

  # ═══ Processing Tray ═══
  defn = model.definitions.add("Processing Tray")
  ents = defn.entities
  # Tray Floor
  grp = ents.add_group
  grp.name = "Tray Floor"
  face = grp.entities.add_face([170.mm,80.mm,0.mm], [4629.mm,80.mm,0.mm], [4629.mm,2280.mm,0.mm], [170.mm,2280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Tray Floor"] || model.materials.add("Tray Floor")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 0.55
  grp.material = mat

  # Tray Rim Near
  grp = ents.add_group
  grp.name = "Tray Rim Near"
  face = grp.entities.add_face([170.mm,80.mm,0.mm], [4629.mm,80.mm,0.mm], [4629.mm,83.mm,0.mm], [170.mm,83.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Tray Rim Near"] || model.materials.add("Tray Rim Near")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 0.3
  grp.material = mat

  # Tray Rim Far
  grp = ents.add_group
  grp.name = "Tray Rim Far"
  face = grp.entities.add_face([170.mm,2277.mm,0.mm], [4629.mm,2277.mm,0.mm], [4629.mm,2280.mm,0.mm], [170.mm,2280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Tray Rim Near"] || model.materials.add("Tray Rim Near")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 0.3
  grp.material = mat

  # Tray Rim Left
  grp = ents.add_group
  grp.name = "Tray Rim Left"
  face = grp.entities.add_face([170.mm,80.mm,0.mm], [173.mm,80.mm,0.mm], [173.mm,2280.mm,0.mm], [170.mm,2280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Tray Rim Near"] || model.materials.add("Tray Rim Near")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 0.3
  grp.material = mat

  # Tray Rim Right
  grp = ents.add_group
  grp.name = "Tray Rim Right"
  face = grp.entities.add_face([4626.mm,80.mm,0.mm], [4629.mm,80.mm,0.mm], [4629.mm,2280.mm,0.mm], [4626.mm,2280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Tray Rim Near"] || model.materials.add("Tray Rim Near")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 0.3
  grp.material = mat

  # Tray Sump
  grp = ents.add_group
  grp.name = "Tray Sump"
  face = grp.entities.add_face([4475.mm,80.mm,-20.mm], [4625.mm,80.mm,-20.mm], [4625.mm,180.mm,-20.mm], [4475.mm,180.mm,-20.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Tray Floor"] || model.materials.add("Tray Floor")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 0.55
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Processing Tray"
  inst.layer = model.layers["Tray"]


model.definitions.purge_unused
model.materials.purge_unused

keep_tags = ["Beam", "Carriages", "Feed & Pole", "Tray"]
default_layer = model.layers[0]
model.layers.to_a.each { |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}

dir = Geom::Vector3d.new(0.5, -0.78, 0.38); dir.normalize!

[["Beam", ["Beam"]], ["Carriage Assembly", ["Beam", "Carriages"]], ["Pole & Ball Joint", ["Beam", "Feed & Pole"]], ["Processing Tray", ["Tray", "Beam", "Carriages"]], ["Combined", ["Beam", "Carriages", "Feed & Pole", "Tray"]]].each { |name, tags|
  model.layers.each { |l| l.visible = (l == default_layer || tags.include?(l.name)) }
  # frame just this scene's visible geometry (the tray is much larger than the bar)
  ctr = model.bounds.center
  eye = ctr.offset(dir, model.bounds.diagonal * 1.4)
  model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
  model.active_view.zoom_extents
  page = model.pages.add(name)
  page.use_camera = true
}
model.layers.each { |l| l.visible = true }

model.commit_operation
{ success: true, model: "Spray-Bar Gantry",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
