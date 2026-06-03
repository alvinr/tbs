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
  circle = ge.add_circle([524.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([524.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([674.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([674.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([824.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([824.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([974.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([974.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1124.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1124.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1274.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1274.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1424.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1424.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1574.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1574.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1724.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1724.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1874.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1874.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2024.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2024.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2174.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2174.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2324.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2324.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2474.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2474.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2624.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2624.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2774.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2774.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2924.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2924.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3074.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3074.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3224.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3224.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3374.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3374.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3524.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3524.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3674.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3674.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3824.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3824.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3974.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3974.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([4124.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([4124.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([4274.5.mm,1180.mm,14.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(46.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([4274.5.mm,1180.mm,10.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
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

  # Pole U-bolt
  grp = ents.add_group
  grp.name = "Pole U-bolt"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 37.mm)
  circle = ge.add_circle([2399.5.mm,1158.mm,54.mm], vec, 2.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Pole U-bolt"] || model.materials.add("Pole U-bolt")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Pole U-bolt elbow
  grp = ents.add_group
  grp.name = "Pole U-bolt elbow"
  ge = grp.entities
  arc = ge.add_arc([2399.5.mm,1163.mm,91.mm], [0.000000,-1.000000,0.000000], [-1.000000,0.000000,0.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2399.5.mm,1158.mm,91.mm], [0.000000,0.000000,1.000000], 2.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Pole U-bolt"] || model.materials.add("Pole U-bolt")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Pole U-bolt
  grp = ents.add_group
  grp.name = "Pole U-bolt"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 34.mm, 0.mm)
  circle = ge.add_circle([2399.5.mm,1163.mm,96.mm], vec, 2.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Pole U-bolt"] || model.materials.add("Pole U-bolt")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Pole U-bolt elbow
  grp = ents.add_group
  grp.name = "Pole U-bolt elbow"
  ge = grp.entities
  arc = ge.add_arc([2399.5.mm,1197.mm,91.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2399.5.mm,1197.mm,96.mm], [0.000000,1.000000,0.000000], 2.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Pole U-bolt"] || model.materials.add("Pole U-bolt")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Pole U-bolt
  grp = ents.add_group
  grp.name = "Pole U-bolt"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -37.mm)
  circle = ge.add_circle([2399.5.mm,1202.mm,91.mm], vec, 2.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Pole U-bolt"] || model.materials.add("Pole U-bolt")
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
  mat = model.materials["Pole U-bolt"] || model.materials.add("Pole U-bolt")
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

  # Feed Hose (upper)
  grp = ents.add_group
  grp.name = "Feed Hose (upper)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 500.mm, -444.5.mm)
  circle = ge.add_circle([2421.5.mm,180.mm,970.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Hose (lower)
  grp = ents.add_group
  grp.name = "Feed Hose (lower)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 490.mm, -432.5.mm)
  circle = ge.add_circle([2421.5.mm,680.mm,525.5.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Hose into Pipe
  grp = ents.add_group
  grp.name = "Feed Hose into Pipe"
  ge = grp.entities
  vec = Geom::Vector3d.new(-92.mm, 10.mm, -53.mm)
  circle = ge.add_circle([2421.5.mm,1170.mm,93.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
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
