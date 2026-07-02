model = Sketchup.active_model
model.start_operation("TBS-001 Spray-Bar Gantry", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# Idempotent rebuild: erase all prior groups/instances.
to_erase = entities.to_a.select { |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text)
}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each { |p| model.pages.erase(p) }

  model.layers.add("Beam") unless model.layers["Beam"]
  model.layers.add("Carriage L") unless model.layers["Carriage L"]
  model.layers.add("Carriage R") unless model.layers["Carriage R"]
  model.layers.add("Tray Ref") unless model.layers["Tray Ref"]
  model.layers.add("Feed & Pole") unless model.layers["Feed & Pole"]
  model.layers.add("Tray") unless model.layers["Tray"]
  model.layers.add("Labels") unless model.layers["Labels"]

  # ═══ Spray Beam ═══
  defn = model.definitions.add("Spray Beam")
  ents = defn.entities
  # Spray Beam 40x25x3 304-SS RHS
  grp = ents.add_group
  grp.name = "Spray Beam 40x25x3 304-SS RHS"
  face = grp.entities.add_face([200.mm,1160.mm,29.mm], [4599.mm,1160.mm,29.mm], [4599.mm,1200.mm,29.mm], [200.mm,1200.mm,29.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Beam End Cap (feed)
  grp = ents.add_group
  grp.name = "Beam End Cap (feed)"
  face = grp.entities.add_face([196.mm,1160.mm,29.mm], [200.mm,1160.mm,29.mm], [200.mm,1200.mm,29.mm], [196.mm,1200.mm,29.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Beam End Cap
  grp = ents.add_group
  grp.name = "Beam End Cap"
  face = grp.entities.add_face([4599.mm,1160.mm,29.mm], [4603.mm,1160.mm,29.mm], [4603.mm,1200.mm,29.mm], [4599.mm,1200.mm,29.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Side Poly Manifold (3/4 LDPE)
  grp = ents.add_group
  grp.name = "Side Poly Manifold (3/4 LDPE)"
  ge = grp.entities
  circle = ge.add_circle([200.mm,1212.5.mm,41.5.mm], [1,0,0], 12.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(4399.mm)
  mat = model.materials["Side Poly Manifold (3/4 LDPE)"] || model.materials.add("Side Poly Manifold (3/4 LDPE)")
  mat.color = Sketchup::Color.new(42, 42, 42)
  mat.alpha = 1.0
  grp.material = mat

  # Water in Manifold
  grp = ents.add_group
  grp.name = "Water in Manifold"
  ge = grp.entities
  circle = ge.add_circle([200.mm,1212.5.mm,41.5.mm], [1,0,0], 9.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(4399.mm)
  mat = model.materials["Water in Manifold"] || model.materials.add("Water in Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 0.55
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([524.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([524.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([674.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([674.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([824.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([824.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([974.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([974.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([1124.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1124.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([1274.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1274.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([1424.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1424.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([1574.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1574.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([1724.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1724.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([1874.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1874.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([2024.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2024.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([2174.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2174.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([2324.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2324.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([2474.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2474.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([2624.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2624.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([2774.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2774.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([2924.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2924.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([3074.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3074.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([3224.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3224.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([3374.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3374.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([3524.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3524.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([3674.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3674.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([3824.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3824.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([3974.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3974.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([4124.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([4124.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([4274.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([4274.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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

  # ═══ Wheel Carriage L ═══
  defn = model.definitions.add("Wheel Carriage L")
  ents = defn.entities
  # Carriage Plate L L
  grp = ents.add_group
  grp.name = "Carriage Plate L L"
  face = grp.entities.add_face([200.mm,1062.mm,38.mm], [240.mm,1062.mm,38.mm], [240.mm,1160.mm,38.mm], [200.mm,1160.mm,38.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["Carriage Plate L L"] || model.materials.add("Carriage Plate L L")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage Plate R L
  grp = ents.add_group
  grp.name = "Carriage Plate R L"
  face = grp.entities.add_face([200.mm,1200.mm,38.mm], [240.mm,1200.mm,38.mm], [240.mm,1298.mm,38.mm], [200.mm,1298.mm,38.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["Carriage Plate L L"] || model.materials.add("Carriage Plate L L")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel L
  grp = ents.add_group
  grp.name = "Wheel L"
  ge = grp.entities
  circle = ge.add_circle([210.mm,1080.mm,36.mm], [1,0,0], 16.mm, 24)
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
  circle = ge.add_circle([196.mm,1080.mm,36.mm], [1,0,0], 5.mm, 24)
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
  face = ge.add_face([[201.mm,1072.mm,36.mm], [201.mm,1072.07.mm,34.96.mm], [201.mm,1072.27.mm,33.93.mm], [201.mm,1072.61.mm,32.94.mm], [201.mm,1073.07.mm,32.mm], [201.mm,1073.65.mm,31.13.mm], [201.mm,1074.34.mm,30.34.mm], [201.mm,1075.13.mm,29.65.mm], [201.mm,1076.mm,29.07.mm], [201.mm,1076.94.mm,28.61.mm], [201.mm,1077.93.mm,28.27.mm], [201.mm,1078.96.mm,28.07.mm], [201.mm,1080.mm,28.mm], [201.mm,1081.04.mm,28.07.mm], [201.mm,1082.07.mm,28.27.mm], [201.mm,1083.06.mm,28.61.mm], [201.mm,1084.mm,29.07.mm], [201.mm,1084.87.mm,29.65.mm], [201.mm,1085.66.mm,30.34.mm], [201.mm,1086.35.mm,31.13.mm], [201.mm,1086.93.mm,32.mm], [201.mm,1087.39.mm,32.94.mm], [201.mm,1087.73.mm,33.93.mm], [201.mm,1087.93.mm,34.96.mm], [201.mm,1088.mm,36.mm], [201.mm,1086.mm,36.mm], [201.mm,1085.95.mm,35.22.mm], [201.mm,1085.8.mm,34.45.mm], [201.mm,1085.54.mm,33.7.mm], [201.mm,1085.2.mm,33.mm], [201.mm,1084.76.mm,32.35.mm], [201.mm,1084.24.mm,31.76.mm], [201.mm,1083.65.mm,31.24.mm], [201.mm,1083.mm,30.8.mm], [201.mm,1082.3.mm,30.46.mm], [201.mm,1081.55.mm,30.2.mm], [201.mm,1080.78.mm,30.05.mm], [201.mm,1080.mm,30.mm], [201.mm,1079.22.mm,30.05.mm], [201.mm,1078.45.mm,30.2.mm], [201.mm,1077.7.mm,30.46.mm], [201.mm,1077.mm,30.8.mm], [201.mm,1076.35.mm,31.24.mm], [201.mm,1075.76.mm,31.76.mm], [201.mm,1075.24.mm,32.35.mm], [201.mm,1074.8.mm,33.mm], [201.mm,1074.46.mm,33.7.mm], [201.mm,1074.2.mm,34.45.mm], [201.mm,1074.05.mm,35.22.mm], [201.mm,1074.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([201.mm,1064.mm,36.mm], [207.mm,1064.mm,36.mm], [207.mm,1074.mm,36.mm], [201.mm,1074.mm,36.mm])
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
  circle = ge.add_circle([204.mm,1069.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([201.mm,1086.mm,36.mm], [207.mm,1086.mm,36.mm], [207.mm,1096.mm,36.mm], [201.mm,1096.mm,36.mm])
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
  circle = ge.add_circle([204.mm,1091.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = ge.add_face([[233.mm,1072.mm,36.mm], [233.mm,1072.07.mm,34.96.mm], [233.mm,1072.27.mm,33.93.mm], [233.mm,1072.61.mm,32.94.mm], [233.mm,1073.07.mm,32.mm], [233.mm,1073.65.mm,31.13.mm], [233.mm,1074.34.mm,30.34.mm], [233.mm,1075.13.mm,29.65.mm], [233.mm,1076.mm,29.07.mm], [233.mm,1076.94.mm,28.61.mm], [233.mm,1077.93.mm,28.27.mm], [233.mm,1078.96.mm,28.07.mm], [233.mm,1080.mm,28.mm], [233.mm,1081.04.mm,28.07.mm], [233.mm,1082.07.mm,28.27.mm], [233.mm,1083.06.mm,28.61.mm], [233.mm,1084.mm,29.07.mm], [233.mm,1084.87.mm,29.65.mm], [233.mm,1085.66.mm,30.34.mm], [233.mm,1086.35.mm,31.13.mm], [233.mm,1086.93.mm,32.mm], [233.mm,1087.39.mm,32.94.mm], [233.mm,1087.73.mm,33.93.mm], [233.mm,1087.93.mm,34.96.mm], [233.mm,1088.mm,36.mm], [233.mm,1086.mm,36.mm], [233.mm,1085.95.mm,35.22.mm], [233.mm,1085.8.mm,34.45.mm], [233.mm,1085.54.mm,33.7.mm], [233.mm,1085.2.mm,33.mm], [233.mm,1084.76.mm,32.35.mm], [233.mm,1084.24.mm,31.76.mm], [233.mm,1083.65.mm,31.24.mm], [233.mm,1083.mm,30.8.mm], [233.mm,1082.3.mm,30.46.mm], [233.mm,1081.55.mm,30.2.mm], [233.mm,1080.78.mm,30.05.mm], [233.mm,1080.mm,30.mm], [233.mm,1079.22.mm,30.05.mm], [233.mm,1078.45.mm,30.2.mm], [233.mm,1077.7.mm,30.46.mm], [233.mm,1077.mm,30.8.mm], [233.mm,1076.35.mm,31.24.mm], [233.mm,1075.76.mm,31.76.mm], [233.mm,1075.24.mm,32.35.mm], [233.mm,1074.8.mm,33.mm], [233.mm,1074.46.mm,33.7.mm], [233.mm,1074.2.mm,34.45.mm], [233.mm,1074.05.mm,35.22.mm], [233.mm,1074.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([233.mm,1064.mm,36.mm], [239.mm,1064.mm,36.mm], [239.mm,1074.mm,36.mm], [233.mm,1074.mm,36.mm])
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
  circle = ge.add_circle([236.mm,1069.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([233.mm,1086.mm,36.mm], [239.mm,1086.mm,36.mm], [239.mm,1096.mm,36.mm], [233.mm,1096.mm,36.mm])
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
  circle = ge.add_circle([236.mm,1091.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  circle = ge.add_circle([210.mm,1280.mm,36.mm], [1,0,0], 16.mm, 24)
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
  circle = ge.add_circle([196.mm,1280.mm,36.mm], [1,0,0], 5.mm, 24)
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
  face = ge.add_face([[201.mm,1272.mm,36.mm], [201.mm,1272.07.mm,34.96.mm], [201.mm,1272.27.mm,33.93.mm], [201.mm,1272.61.mm,32.94.mm], [201.mm,1273.07.mm,32.mm], [201.mm,1273.65.mm,31.13.mm], [201.mm,1274.34.mm,30.34.mm], [201.mm,1275.13.mm,29.65.mm], [201.mm,1276.mm,29.07.mm], [201.mm,1276.94.mm,28.61.mm], [201.mm,1277.93.mm,28.27.mm], [201.mm,1278.96.mm,28.07.mm], [201.mm,1280.mm,28.mm], [201.mm,1281.04.mm,28.07.mm], [201.mm,1282.07.mm,28.27.mm], [201.mm,1283.06.mm,28.61.mm], [201.mm,1284.mm,29.07.mm], [201.mm,1284.87.mm,29.65.mm], [201.mm,1285.66.mm,30.34.mm], [201.mm,1286.35.mm,31.13.mm], [201.mm,1286.93.mm,32.mm], [201.mm,1287.39.mm,32.94.mm], [201.mm,1287.73.mm,33.93.mm], [201.mm,1287.93.mm,34.96.mm], [201.mm,1288.mm,36.mm], [201.mm,1286.mm,36.mm], [201.mm,1285.95.mm,35.22.mm], [201.mm,1285.8.mm,34.45.mm], [201.mm,1285.54.mm,33.7.mm], [201.mm,1285.2.mm,33.mm], [201.mm,1284.76.mm,32.35.mm], [201.mm,1284.24.mm,31.76.mm], [201.mm,1283.65.mm,31.24.mm], [201.mm,1283.mm,30.8.mm], [201.mm,1282.3.mm,30.46.mm], [201.mm,1281.55.mm,30.2.mm], [201.mm,1280.78.mm,30.05.mm], [201.mm,1280.mm,30.mm], [201.mm,1279.22.mm,30.05.mm], [201.mm,1278.45.mm,30.2.mm], [201.mm,1277.7.mm,30.46.mm], [201.mm,1277.mm,30.8.mm], [201.mm,1276.35.mm,31.24.mm], [201.mm,1275.76.mm,31.76.mm], [201.mm,1275.24.mm,32.35.mm], [201.mm,1274.8.mm,33.mm], [201.mm,1274.46.mm,33.7.mm], [201.mm,1274.2.mm,34.45.mm], [201.mm,1274.05.mm,35.22.mm], [201.mm,1274.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([201.mm,1264.mm,36.mm], [207.mm,1264.mm,36.mm], [207.mm,1274.mm,36.mm], [201.mm,1274.mm,36.mm])
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
  circle = ge.add_circle([204.mm,1269.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([201.mm,1286.mm,36.mm], [207.mm,1286.mm,36.mm], [207.mm,1296.mm,36.mm], [201.mm,1296.mm,36.mm])
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
  circle = ge.add_circle([204.mm,1291.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = ge.add_face([[233.mm,1272.mm,36.mm], [233.mm,1272.07.mm,34.96.mm], [233.mm,1272.27.mm,33.93.mm], [233.mm,1272.61.mm,32.94.mm], [233.mm,1273.07.mm,32.mm], [233.mm,1273.65.mm,31.13.mm], [233.mm,1274.34.mm,30.34.mm], [233.mm,1275.13.mm,29.65.mm], [233.mm,1276.mm,29.07.mm], [233.mm,1276.94.mm,28.61.mm], [233.mm,1277.93.mm,28.27.mm], [233.mm,1278.96.mm,28.07.mm], [233.mm,1280.mm,28.mm], [233.mm,1281.04.mm,28.07.mm], [233.mm,1282.07.mm,28.27.mm], [233.mm,1283.06.mm,28.61.mm], [233.mm,1284.mm,29.07.mm], [233.mm,1284.87.mm,29.65.mm], [233.mm,1285.66.mm,30.34.mm], [233.mm,1286.35.mm,31.13.mm], [233.mm,1286.93.mm,32.mm], [233.mm,1287.39.mm,32.94.mm], [233.mm,1287.73.mm,33.93.mm], [233.mm,1287.93.mm,34.96.mm], [233.mm,1288.mm,36.mm], [233.mm,1286.mm,36.mm], [233.mm,1285.95.mm,35.22.mm], [233.mm,1285.8.mm,34.45.mm], [233.mm,1285.54.mm,33.7.mm], [233.mm,1285.2.mm,33.mm], [233.mm,1284.76.mm,32.35.mm], [233.mm,1284.24.mm,31.76.mm], [233.mm,1283.65.mm,31.24.mm], [233.mm,1283.mm,30.8.mm], [233.mm,1282.3.mm,30.46.mm], [233.mm,1281.55.mm,30.2.mm], [233.mm,1280.78.mm,30.05.mm], [233.mm,1280.mm,30.mm], [233.mm,1279.22.mm,30.05.mm], [233.mm,1278.45.mm,30.2.mm], [233.mm,1277.7.mm,30.46.mm], [233.mm,1277.mm,30.8.mm], [233.mm,1276.35.mm,31.24.mm], [233.mm,1275.76.mm,31.76.mm], [233.mm,1275.24.mm,32.35.mm], [233.mm,1274.8.mm,33.mm], [233.mm,1274.46.mm,33.7.mm], [233.mm,1274.2.mm,34.45.mm], [233.mm,1274.05.mm,35.22.mm], [233.mm,1274.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([233.mm,1264.mm,36.mm], [239.mm,1264.mm,36.mm], [239.mm,1274.mm,36.mm], [233.mm,1274.mm,36.mm])
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
  circle = ge.add_circle([236.mm,1269.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([233.mm,1286.mm,36.mm], [239.mm,1286.mm,36.mm], [239.mm,1296.mm,36.mm], [233.mm,1296.mm,36.mm])
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
  circle = ge.add_circle([236.mm,1291.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([200.mm,1148.mm,26.mm], [240.mm,1148.mm,26.mm], [240.mm,1212.mm,26.mm], [200.mm,1212.mm,26.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Top Clamp L
  grp = ents.add_group
  grp.name = "Top Clamp L"
  face = grp.entities.add_face([200.mm,1148.mm,54.mm], [240.mm,1148.mm,54.mm], [240.mm,1212.mm,54.mm], [200.mm,1212.mm,54.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Spacer L
  grp = ents.add_group
  grp.name = "Clamp Spacer L"
  face = grp.entities.add_face([204.mm,1152.mm,29.mm], [236.mm,1152.mm,29.mm], [236.mm,1160.mm,29.mm], [204.mm,1160.mm,29.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Carriage Plate L L"] || model.materials.add("Carriage Plate L L")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt L
  grp = ents.add_group
  grp.name = "Clamp Bolt L"
  ge = grp.entities
  circle = ge.add_circle([209.mm,1156.mm,22.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(39.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt L
  grp = ents.add_group
  grp.name = "Clamp Bolt L"
  ge = grp.entities
  circle = ge.add_circle([231.mm,1156.mm,22.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(39.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Spacer L
  grp = ents.add_group
  grp.name = "Clamp Spacer L"
  face = grp.entities.add_face([204.mm,1200.mm,29.mm], [236.mm,1200.mm,29.mm], [236.mm,1208.mm,29.mm], [204.mm,1208.mm,29.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Carriage Plate L L"] || model.materials.add("Carriage Plate L L")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt L
  grp = ents.add_group
  grp.name = "Clamp Bolt L"
  ge = grp.entities
  circle = ge.add_circle([209.mm,1204.mm,22.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(39.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt L
  grp = ents.add_group
  grp.name = "Clamp Bolt L"
  ge = grp.entities
  circle = ge.add_circle([231.mm,1204.mm,22.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(39.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Wheel Carriage L"
  inst.layer = model.layers["Carriage L"]

  # ═══ Wheel Carriage R ═══
  defn = model.definitions.add("Wheel Carriage R")
  ents = defn.entities
  # Carriage Plate L R
  grp = ents.add_group
  grp.name = "Carriage Plate L R"
  face = grp.entities.add_face([4559.mm,1062.mm,38.mm], [4599.mm,1062.mm,38.mm], [4599.mm,1160.mm,38.mm], [4559.mm,1160.mm,38.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["Carriage Plate L L"] || model.materials.add("Carriage Plate L L")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage Plate R R
  grp = ents.add_group
  grp.name = "Carriage Plate R R"
  face = grp.entities.add_face([4559.mm,1200.mm,38.mm], [4599.mm,1200.mm,38.mm], [4599.mm,1298.mm,38.mm], [4559.mm,1298.mm,38.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["Carriage Plate L L"] || model.materials.add("Carriage Plate L L")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel R
  grp = ents.add_group
  grp.name = "Wheel R"
  ge = grp.entities
  circle = ge.add_circle([4569.mm,1080.mm,36.mm], [1,0,0], 16.mm, 24)
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
  circle = ge.add_circle([4555.mm,1080.mm,36.mm], [1,0,0], 5.mm, 24)
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
  face = ge.add_face([[4560.mm,1072.mm,36.mm], [4560.mm,1072.07.mm,34.96.mm], [4560.mm,1072.27.mm,33.93.mm], [4560.mm,1072.61.mm,32.94.mm], [4560.mm,1073.07.mm,32.mm], [4560.mm,1073.65.mm,31.13.mm], [4560.mm,1074.34.mm,30.34.mm], [4560.mm,1075.13.mm,29.65.mm], [4560.mm,1076.mm,29.07.mm], [4560.mm,1076.94.mm,28.61.mm], [4560.mm,1077.93.mm,28.27.mm], [4560.mm,1078.96.mm,28.07.mm], [4560.mm,1080.mm,28.mm], [4560.mm,1081.04.mm,28.07.mm], [4560.mm,1082.07.mm,28.27.mm], [4560.mm,1083.06.mm,28.61.mm], [4560.mm,1084.mm,29.07.mm], [4560.mm,1084.87.mm,29.65.mm], [4560.mm,1085.66.mm,30.34.mm], [4560.mm,1086.35.mm,31.13.mm], [4560.mm,1086.93.mm,32.mm], [4560.mm,1087.39.mm,32.94.mm], [4560.mm,1087.73.mm,33.93.mm], [4560.mm,1087.93.mm,34.96.mm], [4560.mm,1088.mm,36.mm], [4560.mm,1086.mm,36.mm], [4560.mm,1085.95.mm,35.22.mm], [4560.mm,1085.8.mm,34.45.mm], [4560.mm,1085.54.mm,33.7.mm], [4560.mm,1085.2.mm,33.mm], [4560.mm,1084.76.mm,32.35.mm], [4560.mm,1084.24.mm,31.76.mm], [4560.mm,1083.65.mm,31.24.mm], [4560.mm,1083.mm,30.8.mm], [4560.mm,1082.3.mm,30.46.mm], [4560.mm,1081.55.mm,30.2.mm], [4560.mm,1080.78.mm,30.05.mm], [4560.mm,1080.mm,30.mm], [4560.mm,1079.22.mm,30.05.mm], [4560.mm,1078.45.mm,30.2.mm], [4560.mm,1077.7.mm,30.46.mm], [4560.mm,1077.mm,30.8.mm], [4560.mm,1076.35.mm,31.24.mm], [4560.mm,1075.76.mm,31.76.mm], [4560.mm,1075.24.mm,32.35.mm], [4560.mm,1074.8.mm,33.mm], [4560.mm,1074.46.mm,33.7.mm], [4560.mm,1074.2.mm,34.45.mm], [4560.mm,1074.05.mm,35.22.mm], [4560.mm,1074.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4560.mm,1064.mm,36.mm], [4566.mm,1064.mm,36.mm], [4566.mm,1074.mm,36.mm], [4560.mm,1074.mm,36.mm])
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
  circle = ge.add_circle([4563.mm,1069.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([4560.mm,1086.mm,36.mm], [4566.mm,1086.mm,36.mm], [4566.mm,1096.mm,36.mm], [4560.mm,1096.mm,36.mm])
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
  circle = ge.add_circle([4563.mm,1091.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = ge.add_face([[4592.mm,1072.mm,36.mm], [4592.mm,1072.07.mm,34.96.mm], [4592.mm,1072.27.mm,33.93.mm], [4592.mm,1072.61.mm,32.94.mm], [4592.mm,1073.07.mm,32.mm], [4592.mm,1073.65.mm,31.13.mm], [4592.mm,1074.34.mm,30.34.mm], [4592.mm,1075.13.mm,29.65.mm], [4592.mm,1076.mm,29.07.mm], [4592.mm,1076.94.mm,28.61.mm], [4592.mm,1077.93.mm,28.27.mm], [4592.mm,1078.96.mm,28.07.mm], [4592.mm,1080.mm,28.mm], [4592.mm,1081.04.mm,28.07.mm], [4592.mm,1082.07.mm,28.27.mm], [4592.mm,1083.06.mm,28.61.mm], [4592.mm,1084.mm,29.07.mm], [4592.mm,1084.87.mm,29.65.mm], [4592.mm,1085.66.mm,30.34.mm], [4592.mm,1086.35.mm,31.13.mm], [4592.mm,1086.93.mm,32.mm], [4592.mm,1087.39.mm,32.94.mm], [4592.mm,1087.73.mm,33.93.mm], [4592.mm,1087.93.mm,34.96.mm], [4592.mm,1088.mm,36.mm], [4592.mm,1086.mm,36.mm], [4592.mm,1085.95.mm,35.22.mm], [4592.mm,1085.8.mm,34.45.mm], [4592.mm,1085.54.mm,33.7.mm], [4592.mm,1085.2.mm,33.mm], [4592.mm,1084.76.mm,32.35.mm], [4592.mm,1084.24.mm,31.76.mm], [4592.mm,1083.65.mm,31.24.mm], [4592.mm,1083.mm,30.8.mm], [4592.mm,1082.3.mm,30.46.mm], [4592.mm,1081.55.mm,30.2.mm], [4592.mm,1080.78.mm,30.05.mm], [4592.mm,1080.mm,30.mm], [4592.mm,1079.22.mm,30.05.mm], [4592.mm,1078.45.mm,30.2.mm], [4592.mm,1077.7.mm,30.46.mm], [4592.mm,1077.mm,30.8.mm], [4592.mm,1076.35.mm,31.24.mm], [4592.mm,1075.76.mm,31.76.mm], [4592.mm,1075.24.mm,32.35.mm], [4592.mm,1074.8.mm,33.mm], [4592.mm,1074.46.mm,33.7.mm], [4592.mm,1074.2.mm,34.45.mm], [4592.mm,1074.05.mm,35.22.mm], [4592.mm,1074.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4592.mm,1064.mm,36.mm], [4598.mm,1064.mm,36.mm], [4598.mm,1074.mm,36.mm], [4592.mm,1074.mm,36.mm])
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
  circle = ge.add_circle([4595.mm,1069.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([4592.mm,1086.mm,36.mm], [4598.mm,1086.mm,36.mm], [4598.mm,1096.mm,36.mm], [4592.mm,1096.mm,36.mm])
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
  circle = ge.add_circle([4595.mm,1091.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  circle = ge.add_circle([4569.mm,1280.mm,36.mm], [1,0,0], 16.mm, 24)
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
  circle = ge.add_circle([4555.mm,1280.mm,36.mm], [1,0,0], 5.mm, 24)
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
  face = ge.add_face([[4560.mm,1272.mm,36.mm], [4560.mm,1272.07.mm,34.96.mm], [4560.mm,1272.27.mm,33.93.mm], [4560.mm,1272.61.mm,32.94.mm], [4560.mm,1273.07.mm,32.mm], [4560.mm,1273.65.mm,31.13.mm], [4560.mm,1274.34.mm,30.34.mm], [4560.mm,1275.13.mm,29.65.mm], [4560.mm,1276.mm,29.07.mm], [4560.mm,1276.94.mm,28.61.mm], [4560.mm,1277.93.mm,28.27.mm], [4560.mm,1278.96.mm,28.07.mm], [4560.mm,1280.mm,28.mm], [4560.mm,1281.04.mm,28.07.mm], [4560.mm,1282.07.mm,28.27.mm], [4560.mm,1283.06.mm,28.61.mm], [4560.mm,1284.mm,29.07.mm], [4560.mm,1284.87.mm,29.65.mm], [4560.mm,1285.66.mm,30.34.mm], [4560.mm,1286.35.mm,31.13.mm], [4560.mm,1286.93.mm,32.mm], [4560.mm,1287.39.mm,32.94.mm], [4560.mm,1287.73.mm,33.93.mm], [4560.mm,1287.93.mm,34.96.mm], [4560.mm,1288.mm,36.mm], [4560.mm,1286.mm,36.mm], [4560.mm,1285.95.mm,35.22.mm], [4560.mm,1285.8.mm,34.45.mm], [4560.mm,1285.54.mm,33.7.mm], [4560.mm,1285.2.mm,33.mm], [4560.mm,1284.76.mm,32.35.mm], [4560.mm,1284.24.mm,31.76.mm], [4560.mm,1283.65.mm,31.24.mm], [4560.mm,1283.mm,30.8.mm], [4560.mm,1282.3.mm,30.46.mm], [4560.mm,1281.55.mm,30.2.mm], [4560.mm,1280.78.mm,30.05.mm], [4560.mm,1280.mm,30.mm], [4560.mm,1279.22.mm,30.05.mm], [4560.mm,1278.45.mm,30.2.mm], [4560.mm,1277.7.mm,30.46.mm], [4560.mm,1277.mm,30.8.mm], [4560.mm,1276.35.mm,31.24.mm], [4560.mm,1275.76.mm,31.76.mm], [4560.mm,1275.24.mm,32.35.mm], [4560.mm,1274.8.mm,33.mm], [4560.mm,1274.46.mm,33.7.mm], [4560.mm,1274.2.mm,34.45.mm], [4560.mm,1274.05.mm,35.22.mm], [4560.mm,1274.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4560.mm,1264.mm,36.mm], [4566.mm,1264.mm,36.mm], [4566.mm,1274.mm,36.mm], [4560.mm,1274.mm,36.mm])
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
  circle = ge.add_circle([4563.mm,1269.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([4560.mm,1286.mm,36.mm], [4566.mm,1286.mm,36.mm], [4566.mm,1296.mm,36.mm], [4560.mm,1296.mm,36.mm])
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
  circle = ge.add_circle([4563.mm,1291.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = ge.add_face([[4592.mm,1272.mm,36.mm], [4592.mm,1272.07.mm,34.96.mm], [4592.mm,1272.27.mm,33.93.mm], [4592.mm,1272.61.mm,32.94.mm], [4592.mm,1273.07.mm,32.mm], [4592.mm,1273.65.mm,31.13.mm], [4592.mm,1274.34.mm,30.34.mm], [4592.mm,1275.13.mm,29.65.mm], [4592.mm,1276.mm,29.07.mm], [4592.mm,1276.94.mm,28.61.mm], [4592.mm,1277.93.mm,28.27.mm], [4592.mm,1278.96.mm,28.07.mm], [4592.mm,1280.mm,28.mm], [4592.mm,1281.04.mm,28.07.mm], [4592.mm,1282.07.mm,28.27.mm], [4592.mm,1283.06.mm,28.61.mm], [4592.mm,1284.mm,29.07.mm], [4592.mm,1284.87.mm,29.65.mm], [4592.mm,1285.66.mm,30.34.mm], [4592.mm,1286.35.mm,31.13.mm], [4592.mm,1286.93.mm,32.mm], [4592.mm,1287.39.mm,32.94.mm], [4592.mm,1287.73.mm,33.93.mm], [4592.mm,1287.93.mm,34.96.mm], [4592.mm,1288.mm,36.mm], [4592.mm,1286.mm,36.mm], [4592.mm,1285.95.mm,35.22.mm], [4592.mm,1285.8.mm,34.45.mm], [4592.mm,1285.54.mm,33.7.mm], [4592.mm,1285.2.mm,33.mm], [4592.mm,1284.76.mm,32.35.mm], [4592.mm,1284.24.mm,31.76.mm], [4592.mm,1283.65.mm,31.24.mm], [4592.mm,1283.mm,30.8.mm], [4592.mm,1282.3.mm,30.46.mm], [4592.mm,1281.55.mm,30.2.mm], [4592.mm,1280.78.mm,30.05.mm], [4592.mm,1280.mm,30.mm], [4592.mm,1279.22.mm,30.05.mm], [4592.mm,1278.45.mm,30.2.mm], [4592.mm,1277.7.mm,30.46.mm], [4592.mm,1277.mm,30.8.mm], [4592.mm,1276.35.mm,31.24.mm], [4592.mm,1275.76.mm,31.76.mm], [4592.mm,1275.24.mm,32.35.mm], [4592.mm,1274.8.mm,33.mm], [4592.mm,1274.46.mm,33.7.mm], [4592.mm,1274.2.mm,34.45.mm], [4592.mm,1274.05.mm,35.22.mm], [4592.mm,1274.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(6.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4592.mm,1264.mm,36.mm], [4598.mm,1264.mm,36.mm], [4598.mm,1274.mm,36.mm], [4592.mm,1274.mm,36.mm])
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
  circle = ge.add_circle([4595.mm,1269.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([4592.mm,1286.mm,36.mm], [4598.mm,1286.mm,36.mm], [4598.mm,1296.mm,36.mm], [4592.mm,1296.mm,36.mm])
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
  circle = ge.add_circle([4595.mm,1291.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([4559.mm,1148.mm,26.mm], [4599.mm,1148.mm,26.mm], [4599.mm,1212.mm,26.mm], [4559.mm,1212.mm,26.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Top Clamp R
  grp = ents.add_group
  grp.name = "Top Clamp R"
  face = grp.entities.add_face([4559.mm,1148.mm,54.mm], [4599.mm,1148.mm,54.mm], [4599.mm,1212.mm,54.mm], [4559.mm,1212.mm,54.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Axle Saddle L"] || model.materials.add("Axle Saddle L")
  mat.color = Sketchup::Color.new(192, 192, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Spacer R
  grp = ents.add_group
  grp.name = "Clamp Spacer R"
  face = grp.entities.add_face([4563.mm,1152.mm,29.mm], [4595.mm,1152.mm,29.mm], [4595.mm,1160.mm,29.mm], [4563.mm,1160.mm,29.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Carriage Plate L L"] || model.materials.add("Carriage Plate L L")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt R
  grp = ents.add_group
  grp.name = "Clamp Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4568.mm,1156.mm,22.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(39.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt R
  grp = ents.add_group
  grp.name = "Clamp Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4590.mm,1156.mm,22.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(39.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Spacer R
  grp = ents.add_group
  grp.name = "Clamp Spacer R"
  face = grp.entities.add_face([4563.mm,1200.mm,29.mm], [4595.mm,1200.mm,29.mm], [4595.mm,1208.mm,29.mm], [4563.mm,1208.mm,29.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Carriage Plate L L"] || model.materials.add("Carriage Plate L L")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt R
  grp = ents.add_group
  grp.name = "Clamp Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4568.mm,1204.mm,22.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(39.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt R
  grp = ents.add_group
  grp.name = "Clamp Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4590.mm,1204.mm,22.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(39.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Wheel Carriage R"
  inst.layer = model.layers["Carriage R"]

  # ═══ Tray Floor Ref ═══
  defn = model.definitions.add("Tray Floor Ref")
  ents = defn.entities
  # Tray Floor (ref)
  grp = ents.add_group
  grp.name = "Tray Floor (ref)"
  face = grp.entities.add_face([140.mm,1020.mm,18.mm], [4659.mm,1020.mm,18.mm], [4659.mm,1340.mm,18.mm], [140.mm,1340.mm,18.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Tray Floor (ref)"] || model.materials.add("Tray Floor (ref)")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 0.25
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Tray Floor Ref"
  inst.layer = model.layers["Tray Ref"]

  # ═══ Feed & Push Pole ═══
  defn = model.definitions.add("Feed & Push Pole")
  ents = defn.entities
  # Pole Mount Flange
  grp = ents.add_group
  grp.name = "Pole Mount Flange"
  face = grp.entities.add_face([2377.5.mm,1158.mm,54.mm], [2421.5.mm,1158.mm,54.mm], [2421.5.mm,1202.mm,54.mm], [2377.5.mm,1202.mm,54.mm])
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
  circle = ge.add_circle([2383.5.mm,1164.mm,50.mm], [0,0,1], 1.8.mm, 24)
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
  circle = ge.add_circle([2383.5.mm,1164.mm,59.mm], [0,0,1], 3.mm, 24)
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
  circle = ge.add_circle([2383.5.mm,1196.mm,50.mm], [0,0,1], 1.8.mm, 24)
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
  circle = ge.add_circle([2383.5.mm,1196.mm,59.mm], [0,0,1], 3.mm, 24)
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
  circle = ge.add_circle([2415.5.mm,1164.mm,50.mm], [0,0,1], 1.8.mm, 24)
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
  circle = ge.add_circle([2415.5.mm,1164.mm,59.mm], [0,0,1], 3.mm, 24)
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
  circle = ge.add_circle([2415.5.mm,1196.mm,50.mm], [0,0,1], 1.8.mm, 24)
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
  circle = ge.add_circle([2415.5.mm,1196.mm,59.mm], [0,0,1], 3.mm, 24)
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
  circle = ge.add_circle([2399.5.mm,1180.mm,59.mm], [0,0,1], 18.mm, 24)
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
  circle = ge.add_circle([2399.5.mm,1180.mm,75.mm], vec, 6.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, -476.mm, 427.5.mm)
  circle = ge.add_circle([2399.5.mm,1156.mm,95.mm], vec, 12.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Carriage Plate L L"] || model.materials.add("Carriage Plate L L")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Pinch Bolt
  grp = ents.add_group
  grp.name = "Pinch Bolt"
  ge = grp.entities
  circle = ge.add_circle([2381.5.mm,1154.mm,101.mm], [1,0,0], 3.mm, 24)
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
  vec = Geom::Vector3d.new(0.mm, -500.mm, 447.5.mm)
  circle = ge.add_circle([2399.5.mm,680.mm,522.5.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Carriage Plate L L"] || model.materials.add("Carriage Plate L L")
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
  face = grp.entities.add_face([2419.5.mm,1166.mm,58.mm], [2455.5.mm,1166.mm,58.mm], [2455.5.mm,1194.mm,58.mm], [2419.5.mm,1194.mm,58.mm])
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
  vec = Geom::Vector3d.new(0.mm, 500.mm, -447.5.mm)
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
  vec = Geom::Vector3d.new(0.mm, 476.mm, -427.5.mm)
  circle = ge.add_circle([2419.5.mm,680.mm,522.5.mm], vec, 8.mm, 16)
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
  circle = ge.add_circle([2419.5.mm,1156.mm,95.mm], vec, 7.mm, 14)
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
  circle = ge.add_circle([2420.6475.mm,1156.mm,95.mm], vec, 5.6000000000000005.mm, 14)
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
  circle = ge.add_circle([2421.795.mm,1156.mm,95.mm], vec, 7.mm, 14)
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
  circle = ge.add_circle([2422.9425.mm,1156.mm,95.mm], vec, 5.6000000000000005.mm, 14)
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
  circle = ge.add_circle([2424.09.mm,1156.mm,95.mm], vec, 7.mm, 14)
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
  circle = ge.add_circle([2425.2374999999997.mm,1156.mm,95.mm], vec, 5.6000000000000005.mm, 14)
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
  circle = ge.add_circle([2426.3849999999998.mm,1156.mm,95.mm], vec, 7.mm, 14)
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
  circle = ge.add_circle([2427.5325.mm,1156.mm,95.mm], vec, 5.6000000000000005.mm, 14)
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
  arc = ge.add_arc([2428.68.mm,1164.82.mm,95.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 8.820000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2428.68.mm,1156.mm,95.mm], [1.000000,0.000000,0.000000], 7.mm, 16)
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
  circle = ge.add_circle([2437.5.mm,1164.82.mm,95.mm], vec, 7.mm, 14)
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
  circle = ge.add_circle([2437.5.mm,1165.787725.mm,95.mm], vec, 5.6000000000000005.mm, 14)
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
  circle = ge.add_circle([2437.5.mm,1166.7554499999999.mm,95.mm], vec, 7.mm, 14)
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
  circle = ge.add_circle([2437.5.mm,1167.7231749999999.mm,95.mm], vec, 5.6000000000000005.mm, 14)
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
  circle = ge.add_circle([2437.5.mm,1168.6909.mm,95.mm], vec, 7.mm, 14)
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
  circle = ge.add_circle([2437.5.mm,1169.658625.mm,95.mm], vec, 5.6000000000000005.mm, 14)
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
  circle = ge.add_circle([2437.5.mm,1170.62635.mm,95.mm], vec, 7.mm, 14)
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
  circle = ge.add_circle([2437.5.mm,1171.594075.mm,95.mm], vec, 5.6000000000000005.mm, 14)
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
  arc = ge.add_arc([2437.5.mm,1172.5618.mm,87.56179999999996.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 7.438200000000032.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2437.5.mm,1172.5618.mm,95.mm], [0.000000,1.000000,0.000000], 7.mm, 16)
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
  circle = ge.add_circle([2437.5.mm,1180.mm,87.56179999999996.mm], vec, 7.mm, 14)
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
  circle = ge.add_circle([2437.5.mm,1180.mm,86.11657499999997.mm], vec, 5.6000000000000005.mm, 14)
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
  circle = ge.add_circle([2437.5.mm,1180.mm,84.67134999999998.mm], vec, 7.mm, 14)
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
  circle = ge.add_circle([2437.5.mm,1180.mm,83.22612499999998.mm], vec, 5.6000000000000005.mm, 14)
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
  circle = ge.add_circle([2437.5.mm,1180.mm,81.78089999999997.mm], vec, 7.mm, 14)
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
  circle = ge.add_circle([2437.5.mm,1180.mm,80.33567499999998.mm], vec, 5.6000000000000005.mm, 14)
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
  circle = ge.add_circle([2437.5.mm,1180.mm,78.89044999999999.mm], vec, 7.mm, 14)
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
  circle = ge.add_circle([2437.5.mm,1180.mm,77.445225.mm], vec, 5.6000000000000005.mm, 14)
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
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -6.46793719515739.mm, -7.226745469449611.mm)
  circle = ge.add_circle([2430.5.mm,263.3333333333333.mm,895.4166666666666.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-11.5.mm, -3.9974050237069036.mm, -4.466374328164079.mm)
  circle = ge.add_circle([2426.107390870624.mm,256.8653961381759.mm,888.189921197217.mm], vec, 1.2.mm, 6)
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
  circle = ge.add_circle([2414.607390870624.mm,252.86799111446902.mm,883.7235468690529.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-11.5.mm, 3.9974050237069036.mm, 4.466374328164079.mm)
  circle = ge.add_circle([2400.392609129376.mm,252.86799111446902.mm,883.7235468690529.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 6.46793719515739.mm, 7.226745469449611.mm)
  circle = ge.add_circle([2388.892609129376.mm,256.8653961381759.mm,888.189921197217.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(4.392609129376069.mm, 6.46793719515739.mm, 7.226745469449611.mm)
  circle = ge.add_circle([2384.5.mm,263.3333333333333.mm,895.4166666666666.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(11.5.mm, 3.9974050237069036.mm, 4.466374328164079.mm)
  circle = ge.add_circle([2388.892609129376.mm,269.8012705284907.mm,902.6434121361162.mm], vec, 1.2.mm, 6)
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
  circle = ge.add_circle([2400.392609129376.mm,273.7986755521976.mm,907.1097864642803.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(11.5.mm, -3.9974050237069036.mm, -4.466374328164079.mm)
  circle = ge.add_circle([2414.607390870624.mm,273.7986755521976.mm,907.1097864642803.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(4.392609129376069.mm, -6.46793719515739.mm, -7.226745469449611.mm)
  circle = ge.add_circle([2426.107390870624.mm,269.8012705284907.mm,902.6434121361162.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -6.46793719515739.mm, -7.226745469449611.mm)
  circle = ge.add_circle([2430.5.mm,430.mm,746.25.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-11.5.mm, -3.9974050237069036.mm, -4.466374328164079.mm)
  circle = ge.add_circle([2426.107390870624.mm,423.5320628048426.mm,739.0232545305504.mm], vec, 1.2.mm, 6)
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
  circle = ge.add_circle([2414.607390870624.mm,419.5346577811357.mm,734.5568802023863.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-11.5.mm, 3.9974050237069036.mm, 4.466374328164079.mm)
  circle = ge.add_circle([2400.392609129376.mm,419.5346577811357.mm,734.5568802023863.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 6.46793719515739.mm, 7.226745469449611.mm)
  circle = ge.add_circle([2388.892609129376.mm,423.5320628048426.mm,739.0232545305504.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(4.392609129376069.mm, 6.46793719515739.mm, 7.226745469449611.mm)
  circle = ge.add_circle([2384.5.mm,430.mm,746.25.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(11.5.mm, 3.9974050237069036.mm, 4.466374328164079.mm)
  circle = ge.add_circle([2388.892609129376.mm,436.4679371951574.mm,753.4767454694496.mm], vec, 1.2.mm, 6)
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
  circle = ge.add_circle([2400.392609129376.mm,440.4653422188643.mm,757.9431197976137.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(11.5.mm, -3.9974050237069036.mm, -4.466374328164079.mm)
  circle = ge.add_circle([2414.607390870624.mm,440.4653422188643.mm,757.9431197976137.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(4.392609129376069.mm, -6.46793719515739.mm, -7.226745469449611.mm)
  circle = ge.add_circle([2426.107390870624.mm,436.4679371951574.mm,753.4767454694496.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -6.467937195157333.mm, -7.226745469449611.mm)
  circle = ge.add_circle([2430.5.mm,596.6666666666667.mm,597.0833333333333.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-11.5.mm, -3.9974050237069605.mm, -4.466374328164079.mm)
  circle = ge.add_circle([2426.107390870624.mm,590.1987294715094.mm,589.8565878638836.mm], vec, 1.2.mm, 6)
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
  circle = ge.add_circle([2414.607390870624.mm,586.2013244478024.mm,585.3902135357196.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-11.5.mm, 3.9974050237069605.mm, 4.466374328164079.mm)
  circle = ge.add_circle([2400.392609129376.mm,586.2013244478024.mm,585.3902135357196.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 6.467937195157333.mm, 7.226745469449611.mm)
  circle = ge.add_circle([2388.892609129376.mm,590.1987294715094.mm,589.8565878638836.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(4.392609129376069.mm, 6.467937195157333.mm, 7.226745469449611.mm)
  circle = ge.add_circle([2384.5.mm,596.6666666666667.mm,597.0833333333333.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(11.5.mm, 3.9974050237069605.mm, 4.466374328164079.mm)
  circle = ge.add_circle([2388.892609129376.mm,603.1346038618241.mm,604.3100788027829.mm], vec, 1.2.mm, 6)
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
  circle = ge.add_circle([2400.392609129376.mm,607.132008885531.mm,608.776453130947.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(11.5.mm, -3.9974050237069605.mm, -4.466374328164079.mm)
  circle = ge.add_circle([2414.607390870624.mm,607.132008885531.mm,608.776453130947.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(4.392609129376069.mm, -6.467937195157333.mm, -7.226745469449611.mm)
  circle = ge.add_circle([2426.107390870624.mm,603.1346038618241.mm,604.3100788027829.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -6.480384390219797.mm, -7.215585894139508.mm)
  circle = ge.add_circle([2430.5.mm,759.3333333333334.mm,451.25.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-11.5.mm, -4.0050978133201625.mm, -4.459477331322546.mm)
  circle = ge.add_circle([2426.107390870624.mm,752.8529489431136.mm,444.0344141058605.mm], vec, 1.2.mm, 6)
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
  circle = ge.add_circle([2414.607390870624.mm,748.8478511297934.mm,439.57493677453795.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-11.5.mm, 4.0050978133201625.mm, 4.459477331322546.mm)
  circle = ge.add_circle([2400.392609129376.mm,748.8478511297934.mm,439.57493677453795.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 6.480384390219797.mm, 7.215585894139508.mm)
  circle = ge.add_circle([2388.892609129376.mm,752.8529489431136.mm,444.0344141058605.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(4.392609129376069.mm, 6.480384390219797.mm, 7.215585894139508.mm)
  circle = ge.add_circle([2384.5.mm,759.3333333333334.mm,451.25.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(11.5.mm, 4.0050978133201625.mm, 4.459477331322546.mm)
  circle = ge.add_circle([2388.892609129376.mm,765.8137177235532.mm,458.4655858941395.mm], vec, 1.2.mm, 6)
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
  circle = ge.add_circle([2400.392609129376.mm,769.8188155368733.mm,462.92506322546205.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(11.5.mm, -4.0050978133201625.mm, -4.459477331322546.mm)
  circle = ge.add_circle([2414.607390870624.mm,769.8188155368733.mm,462.92506322546205.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(4.392609129376069.mm, -6.480384390219797.mm, -7.215585894139508.mm)
  circle = ge.add_circle([2426.107390870624.mm,765.8137177235532.mm,458.4655858941395.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -6.480384390219797.mm, -7.215585894139508.mm)
  circle = ge.add_circle([2430.5.mm,918.mm,308.75.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-11.5.mm, -4.0050978133201625.mm, -4.459477331322546.mm)
  circle = ge.add_circle([2426.107390870624.mm,911.5196156097802.mm,301.5344141058605.mm], vec, 1.2.mm, 6)
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
  circle = ge.add_circle([2414.607390870624.mm,907.51451779646.mm,297.07493677453795.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-11.5.mm, 4.0050978133201625.mm, 4.459477331322546.mm)
  circle = ge.add_circle([2400.392609129376.mm,907.51451779646.mm,297.07493677453795.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 6.480384390219797.mm, 7.215585894139508.mm)
  circle = ge.add_circle([2388.892609129376.mm,911.5196156097802.mm,301.5344141058605.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(4.392609129376069.mm, 6.480384390219797.mm, 7.215585894139508.mm)
  circle = ge.add_circle([2384.5.mm,918.mm,308.75.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(11.5.mm, 4.0050978133201625.mm, 4.459477331322546.mm)
  circle = ge.add_circle([2388.892609129376.mm,924.4803843902198.mm,315.9655858941395.mm], vec, 1.2.mm, 6)
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
  circle = ge.add_circle([2400.392609129376.mm,928.48548220354.mm,320.42506322546205.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(11.5.mm, -4.0050978133201625.mm, -4.459477331322546.mm)
  circle = ge.add_circle([2414.607390870624.mm,928.48548220354.mm,320.42506322546205.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(4.392609129376069.mm, -6.480384390219797.mm, -7.215585894139508.mm)
  circle = ge.add_circle([2426.107390870624.mm,924.4803843902198.mm,315.9655858941395.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -6.480384390219797.mm, -7.2155858941395365.mm)
  circle = ge.add_circle([2430.5.mm,1076.6666666666667.mm,166.25.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-11.5.mm, -4.0050978133201625.mm, -4.459477331322518.mm)
  circle = ge.add_circle([2426.107390870624.mm,1070.186282276447.mm,159.03441410586046.mm], vec, 1.2.mm, 6)
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
  circle = ge.add_circle([2414.607390870624.mm,1066.1811844631268.mm,154.57493677453795.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-11.5.mm, 4.0050978133201625.mm, 4.459477331322518.mm)
  circle = ge.add_circle([2400.392609129376.mm,1066.1811844631268.mm,154.57493677453795.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 6.480384390219797.mm, 7.2155858941395365.mm)
  circle = ge.add_circle([2388.892609129376.mm,1070.186282276447.mm,159.03441410586046.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(4.392609129376069.mm, 6.480384390219797.mm, 7.215585894139508.mm)
  circle = ge.add_circle([2384.5.mm,1076.6666666666667.mm,166.25.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(11.5.mm, 4.0050978133201625.mm, 4.459477331322546.mm)
  circle = ge.add_circle([2388.892609129376.mm,1083.1470510568865.mm,173.4655858941395.mm], vec, 1.2.mm, 6)
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
  circle = ge.add_circle([2400.392609129376.mm,1087.1521488702067.mm,177.92506322546205.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(11.5.mm, -4.0050978133201625.mm, -4.459477331322518.mm)
  circle = ge.add_circle([2414.607390870624.mm,1087.1521488702067.mm,177.92506322546205.mm], vec, 1.2.mm, 6)
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
  vec = Geom::Vector3d.new(4.392609129376069.mm, -6.480384390219797.mm, -7.2155858941395365.mm)
  circle = ge.add_circle([2426.107390870624.mm,1083.1470510568865.mm,173.46558589413954.mm], vec, 1.2.mm, 6)
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
  circle = ge.add_circle([2437.5.mm,1192.mm,67.mm], vec, 3.mm, 16)
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
  arc = ge.add_arc([2432.5.mm,1205.mm,67.mm], [1.000000,0.000000,0.000000], [0.000000,-0.000000,1.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2437.5.mm,1205.mm,67.mm], [0.000000,1.000000,0.000000], 3.mm, 16)
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
  vec = Geom::Vector3d.new(-1917.0607142857143.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2432.5.mm,1210.mm,67.mm], vec, 3.mm, 16)
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
  arc = ge.add_arc([515.4392857142858.mm,1211.225.mm,67.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,-1.000000], 1.2250000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([515.4392857142858.mm,1210.mm,67.mm], [-1.000000,0.000000,0.000000], 3.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.6502500000001419.mm, 0.mm)
  circle = ge.add_circle([514.2142857142858.mm,1211.225.mm,67.mm], vec, 3.mm, 16)
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
  arc = ge.add_arc([514.2142857142858.mm,1211.87525.mm,66.37524999999995.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 0.6247500000000447.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([514.2142857142858.mm,1211.87525.mm,67.mm], [0.000000,1.000000,0.000000], 3.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -10.875249999999951.mm)
  circle = ge.add_circle([514.2142857142858.mm,1212.5.mm,66.37524999999995.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Barb Tee
  grp = ents.add_group
  grp.name = "Feed Barb Tee"
  ge = grp.entities
  circle = ge.add_circle([514.2142857142858.mm,1212.5.mm,39.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 13.mm, 0.mm)
  circle = ge.add_circle([2437.5.mm,1192.mm,67.mm], vec, 3.mm, 16)
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
  arc = ge.add_arc([2432.5.mm,1205.mm,67.mm], [1.000000,0.000000,0.000000], [0.000000,-0.000000,1.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2437.5.mm,1205.mm,67.mm], [0.000000,1.000000,0.000000], 3.mm, 16)
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
  vec = Geom::Vector3d.new(-1288.632142857143.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2432.5.mm,1210.mm,67.mm], vec, 3.mm, 16)
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
  arc = ge.add_arc([1143.867857142857.mm,1211.225.mm,67.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,-1.000000], 1.2250000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1143.867857142857.mm,1210.mm,67.mm], [-1.000000,0.000000,0.000000], 3.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.6502500000001419.mm, 0.mm)
  circle = ge.add_circle([1142.642857142857.mm,1211.225.mm,67.mm], vec, 3.mm, 16)
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
  arc = ge.add_arc([1142.642857142857.mm,1211.87525.mm,66.37524999999995.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 0.6247500000000447.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1142.642857142857.mm,1211.87525.mm,67.mm], [0.000000,1.000000,0.000000], 3.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -10.875249999999951.mm)
  circle = ge.add_circle([1142.642857142857.mm,1212.5.mm,66.37524999999995.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Barb Tee
  grp = ents.add_group
  grp.name = "Feed Barb Tee"
  ge = grp.entities
  circle = ge.add_circle([1142.642857142857.mm,1212.5.mm,39.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 13.mm, 0.mm)
  circle = ge.add_circle([2437.5.mm,1192.mm,67.mm], vec, 3.mm, 16)
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
  arc = ge.add_arc([2432.5.mm,1205.mm,67.mm], [1.000000,0.000000,0.000000], [0.000000,-0.000000,1.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2437.5.mm,1205.mm,67.mm], [0.000000,1.000000,0.000000], 3.mm, 16)
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
  vec = Geom::Vector3d.new(-660.2035714285714.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2432.5.mm,1210.mm,67.mm], vec, 3.mm, 16)
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
  arc = ge.add_arc([1772.2964285714286.mm,1211.225.mm,67.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,-1.000000], 1.2250000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1772.2964285714286.mm,1210.mm,67.mm], [-1.000000,0.000000,0.000000], 3.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.6502500000001419.mm, 0.mm)
  circle = ge.add_circle([1771.0714285714287.mm,1211.225.mm,67.mm], vec, 3.mm, 16)
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
  arc = ge.add_arc([1771.0714285714287.mm,1211.87525.mm,66.37524999999995.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 0.6247500000000447.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1771.0714285714287.mm,1211.87525.mm,67.mm], [0.000000,1.000000,0.000000], 3.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -10.875249999999951.mm)
  circle = ge.add_circle([1771.0714285714287.mm,1212.5.mm,66.37524999999995.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Barb Tee
  grp = ents.add_group
  grp.name = "Feed Barb Tee"
  ge = grp.entities
  circle = ge.add_circle([1771.0714285714287.mm,1212.5.mm,39.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(23.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2451.5.mm,1180.mm,67.mm], vec, 3.mm, 16)
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
  arc = ge.add_arc([2474.5.mm,1185.mm,67.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2474.5.mm,1180.mm,67.mm], [1.000000,0.000000,0.000000], 3.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 22.5.mm, 0.mm)
  circle = ge.add_circle([2479.5.mm,1185.mm,67.mm], vec, 3.mm, 16)
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
  arc = ge.add_arc([2479.5.mm,1207.5.mm,62.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2479.5.mm,1207.5.mm,67.mm], [0.000000,1.000000,0.000000], 3.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -6.5.mm)
  circle = ge.add_circle([2479.5.mm,1212.5.mm,62.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Barb Tee
  grp = ents.add_group
  grp.name = "Feed Barb Tee"
  ge = grp.entities
  circle = ge.add_circle([2479.5.mm,1212.5.mm,39.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(571.4285714285716.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2451.5.mm,1180.mm,67.mm], vec, 3.mm, 16)
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
  arc = ge.add_arc([3022.9285714285716.mm,1185.mm,67.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([3022.9285714285716.mm,1180.mm,67.mm], [1.000000,0.000000,0.000000], 3.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 22.5.mm, 0.mm)
  circle = ge.add_circle([3027.9285714285716.mm,1185.mm,67.mm], vec, 3.mm, 16)
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
  arc = ge.add_arc([3027.9285714285716.mm,1207.5.mm,62.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([3027.9285714285716.mm,1207.5.mm,67.mm], [0.000000,1.000000,0.000000], 3.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -6.5.mm)
  circle = ge.add_circle([3027.9285714285716.mm,1212.5.mm,62.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Barb Tee
  grp = ents.add_group
  grp.name = "Feed Barb Tee"
  ge = grp.entities
  circle = ge.add_circle([3027.9285714285716.mm,1212.5.mm,39.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(1199.8571428571427.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2451.5.mm,1180.mm,67.mm], vec, 3.mm, 16)
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
  arc = ge.add_arc([3651.3571428571427.mm,1185.mm,67.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([3651.3571428571427.mm,1180.mm,67.mm], [1.000000,0.000000,0.000000], 3.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 22.5.mm, 0.mm)
  circle = ge.add_circle([3656.3571428571427.mm,1185.mm,67.mm], vec, 3.mm, 16)
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
  arc = ge.add_arc([3656.3571428571427.mm,1207.5.mm,62.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([3656.3571428571427.mm,1207.5.mm,67.mm], [0.000000,1.000000,0.000000], 3.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -6.5.mm)
  circle = ge.add_circle([3656.3571428571427.mm,1212.5.mm,62.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Barb Tee
  grp = ents.add_group
  grp.name = "Feed Barb Tee"
  ge = grp.entities
  circle = ge.add_circle([3656.3571428571427.mm,1212.5.mm,39.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Tube
  grp = ents.add_group
  grp.name = "Feed Tube"
  ge = grp.entities
  vec = Geom::Vector3d.new(1828.2857142857138.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2451.5.mm,1180.mm,67.mm], vec, 3.mm, 16)
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
  arc = ge.add_arc([4279.785714285714.mm,1185.mm,67.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4279.785714285714.mm,1180.mm,67.mm], [1.000000,0.000000,0.000000], 3.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 22.5.mm, 0.mm)
  circle = ge.add_circle([4284.785714285714.mm,1185.mm,67.mm], vec, 3.mm, 16)
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
  arc = ge.add_arc([4284.785714285714.mm,1207.5.mm,62.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 5.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4284.785714285714.mm,1207.5.mm,67.mm], [0.000000,1.000000,0.000000], 3.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -6.5.mm)
  circle = ge.add_circle([4284.785714285714.mm,1212.5.mm,62.mm], vec, 3.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Manifold"] || model.materials.add("Feed Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Barb Tee
  grp = ents.add_group
  grp.name = "Feed Barb Tee"
  ge = grp.entities
  circle = ge.add_circle([4284.785714285714.mm,1212.5.mm,39.5.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
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
  # Tray Shim Base
  grp = ents.add_group
  grp.name = "Tray Shim Base"
  face = grp.entities.add_face([170.mm,80.mm,0.mm], [4629.mm,80.mm,0.mm], [4629.mm,2280.mm,0.mm], [170.mm,2280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Tray Shim Base"] || model.materials.add("Tray Shim Base")
  mat.color = Sketchup::Color.new(216, 207, 188)
  mat.alpha = 0.4
  grp.material = mat

  # Tray Floor
  grp = ents.add_group
  grp.name = "Tray Floor"
  face = grp.entities.add_face([170.mm,80.mm,18.mm], [4629.mm,80.mm,18.mm], [4629.mm,2280.mm,18.mm], [170.mm,2280.mm,18.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Tray Floor"] || model.materials.add("Tray Floor")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 0.55
  grp.material = mat

  # Tray Rim Near
  grp = ents.add_group
  grp.name = "Tray Rim Near"
  face = grp.entities.add_face([170.mm,80.mm,18.mm], [4629.mm,80.mm,18.mm], [4629.mm,83.mm,18.mm], [170.mm,83.mm,18.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Tray Rim Near"] || model.materials.add("Tray Rim Near")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 0.3
  grp.material = mat

  # Tray Rim Far
  grp = ents.add_group
  grp.name = "Tray Rim Far"
  face = grp.entities.add_face([170.mm,2277.mm,18.mm], [4629.mm,2277.mm,18.mm], [4629.mm,2280.mm,18.mm], [170.mm,2280.mm,18.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Tray Rim Near"] || model.materials.add("Tray Rim Near")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 0.3
  grp.material = mat

  # Tray Rim Left
  grp = ents.add_group
  grp.name = "Tray Rim Left"
  face = grp.entities.add_face([170.mm,80.mm,18.mm], [173.mm,80.mm,18.mm], [173.mm,2280.mm,18.mm], [170.mm,2280.mm,18.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Tray Rim Near"] || model.materials.add("Tray Rim Near")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 0.3
  grp.material = mat

  # Tray Rim Right
  grp = ents.add_group
  grp.name = "Tray Rim Right"
  face = grp.entities.add_face([4626.mm,80.mm,18.mm], [4629.mm,80.mm,18.mm], [4629.mm,2280.mm,18.mm], [4626.mm,2280.mm,18.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Tray Rim Near"] || model.materials.add("Tray Rim Near")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 0.3
  grp.material = mat

  # Tray Sump
  grp = ents.add_group
  grp.name = "Tray Sump"
  face = grp.entities.add_face([4475.mm,80.mm,0.mm], [4625.mm,80.mm,0.mm], [4625.mm,180.mm,0.mm], [4475.mm,180.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Tray Floor"] || model.materials.add("Tray Floor")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 0.55
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Processing Tray"
  inst.layer = model.layers["Tray"]


# ── "Labeled" scene callouts (Labels tag — shown only in the "Labeled" scene) ──
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Processing Tray" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("PROCESSING TRAY", anc, Geom::Vector3d.new(500.mm, -700.mm, 700.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
anc = Geom::Point3d.new(1400.mm, 1180.mm, 60.mm)
txt = entities.add_text("SPRAY BEAM
(40 RHS + 3/4-in LDPE bore)", anc, Geom::Vector3d.new(0.mm, -900.mm, 650.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(200.mm, 1180.mm, 60.mm)
txt = entities.add_text("WHEEL CARRIAGE
(saddle clamp + 2 wheels)", anc, Geom::Vector3d.new(-750.mm, -350.mm, 600.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4599.mm, 1180.mm, 60.mm)
txt = entities.add_text("WHEEL CARRIAGE", anc, Geom::Vector3d.new(700.mm, -350.mm, 600.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(950.mm, 1180.mm, 18.mm)
txt = entities.add_text("SPRAY NOZZLES
(26 flat-fan @ 150mm)", anc, Geom::Vector3d.new(250.mm, -950.mm, 380.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(2399.mm, 1180.mm, 90.mm)
txt = entities.add_text("FEED POLE + BALL JOINT", anc, Geom::Vector3d.new(700.mm, -250.mm, 800.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(2437.mm, 1180.mm, 75.mm)
txt = entities.add_text("DISTRIBUTION MANIFOLD
(7 feed tubes)", anc, Geom::Vector3d.new(-600.mm, -700.mm, 650.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4550.mm, 80.mm, 0.mm)
txt = entities.add_text("DRAIN SUMP", anc, Geom::Vector3d.new(200.mm, -600.mm, 450.mm))
txt.layer = model.layers["Labels"] rescue nil

# ── In-model © + license credit (default layer → shown in every scene) ──
lbb = model.bounds
lanc = Geom::Point3d.new(lbb.min.x, lbb.min.y - 400.mm, lbb.min.z)
entities.add_text("© 2026 Alvin Richards
Licensed under GNU AGPLv3
alvinr.github.io/tbs", lanc)

model.definitions.purge_unused
model.materials.purge_unused

keep_tags = ["Beam", "Carriage L", "Carriage R", "Tray Ref", "Feed & Pole", "Tray", "Labels"]
default_layer = model.layers[0]
model.layers.to_a.each { |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}

dir = Geom::Vector3d.new(0.5, -0.78, 0.38); dir.normalize!

[["Beam", ["Beam"], nil], ["Carriage Assembly", ["Beam", "Carriage L", "Carriage R", "Tray Ref"], nil], ["One Carriage", ["Carriage L"], [200.mm, 1180.mm, 55.mm, 480.mm]], ["Pole & Ball Joint", ["Beam", "Feed & Pole"], nil], ["Processing Tray", ["Tray", "Beam", "Carriage L", "Carriage R"], nil], ["Combined", ["Beam", "Carriage L", "Carriage R", "Feed & Pole", "Tray"], nil], ["Labeled", ["Beam", "Carriage L", "Carriage R", "Feed & Pole", "Tray", "Labels"], nil]].each { |name, tags, tgt|
  model.layers.each { |l| l.visible = (l == default_layer || tags.include?(l.name)) }
  if tgt
    # close-up: aim at the target with a tight standoff (no zoom_extents); use a
    # direction nearly PERPENDICULAR to the beam (mostly −Y) so the carriage reads
    # rather than the beam vanishing down the line of sight.
    t = Geom::Point3d.new(tgt[0], tgt[1], tgt[2])
    cdir = Geom::Vector3d.new(0.18, -0.88, 0.44); cdir.normalize!
    model.active_view.camera = Sketchup::Camera.new(t.offset(cdir, tgt[3]), t, Z_AXIS)
  else
    # frame just this scene's visible geometry (the tray is much larger than the bar)
    ctr = model.bounds.center
    eye = ctr.offset(dir, model.bounds.diagonal * 1.4)
    model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
    model.active_view.zoom_extents
  end
  page = model.pages.add(name)
  page.use_camera = true
}
model.layers.each { |l| l.visible = true }

model.commit_operation
{ success: true, model: "Spray-Bar Gantry",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
