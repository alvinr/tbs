# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/ — do not edit this .rb directly.
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

# ── Sketchfab metadata — sketchfab dict fill-only-if-blank; name/desc forced when requested ──
model.name = "TBS-001 Spraybar Model" if model.name.to_s.strip.empty?
model.description = "The processing tray provides the containment surface and the spray bar delivers even water distribution across the full print width." if model.description.to_s.strip.empty?
model.set_attribute("sketchfab", "model_title", "TBS-001 Spraybar Model") if model.get_attribute("sketchfab", "model_title").to_s.strip.empty?
model.set_attribute("sketchfab", "model_description", "The processing tray provides the containment surface and the spray bar delivers even water distribution across the full print width.") if model.get_attribute("sketchfab", "model_description").to_s.strip.empty?
model.set_attribute("sketchfab", "model_id", "18fb381fbf48459cac25dcaa23958387") if model.get_attribute("sketchfab", "model_id").to_s.strip.empty?
model.set_attribute("sketchfab", "model_tags", "sketchup") if model.get_attribute("sketchfab", "model_tags").to_s.strip.empty?

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
  circle = ge.add_circle([-450.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([-450.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([-300.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([-300.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([-150.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([-150.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([-0.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([-0.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([149.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([149.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([299.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([299.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([449.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([449.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([599.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([599.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([749.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([749.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([899.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([899.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([1049.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([1049.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([1199.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([1199.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([1349.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([1349.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([1499.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([1499.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([1649.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([1649.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([1799.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([1799.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([1949.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([1949.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([2099.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([2099.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([2249.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([2249.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([2399.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([2399.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([2549.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([2549.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([2699.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([2699.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([2849.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([2849.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([2999.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([2999.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([3149.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([3149.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([3299.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([3299.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([3449.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([3449.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([3599.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([3599.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([3749.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([3749.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([3899.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([3899.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([4049.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([4049.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([4199.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([4199.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([4349.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([4349.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([4499.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([4499.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([4649.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([4649.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([4799.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([4799.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([4949.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([4949.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([5099.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([5099.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([5249.5.mm,1212.5.mm,29.5.mm], [0,0,1], 4.mm, 24)
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
  circle = ge.add_circle([5249.5.mm,1212.5.mm,23.5.mm], [0,0,1], 6.5.mm, 24)
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
  circle = ge.add_circle([187.mm,1080.mm,36.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(66.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle L
  grp = ents.add_group
  grp.name = "Axle Saddle L"
  ge = grp.entities
  face = ge.add_face([[189.mm,1070.82.mm,36.mm], [189.mm,1070.9.mm,34.8.mm], [189.mm,1071.13.mm,33.62.mm], [189.mm,1071.52.mm,32.49.mm], [189.mm,1072.05.mm,31.41.mm], [189.mm,1072.72.mm,30.41.mm], [189.mm,1073.51.mm,29.51.mm], [189.mm,1074.41.mm,28.72.mm], [189.mm,1075.41.mm,28.05.mm], [189.mm,1076.49.mm,27.52.mm], [189.mm,1077.62.mm,27.13.mm], [189.mm,1078.8.mm,26.9.mm], [189.mm,1080.mm,26.82.mm], [189.mm,1081.2.mm,26.9.mm], [189.mm,1082.38.mm,27.13.mm], [189.mm,1083.51.mm,27.52.mm], [189.mm,1084.59.mm,28.05.mm], [189.mm,1085.59.mm,28.72.mm], [189.mm,1086.49.mm,29.51.mm], [189.mm,1087.28.mm,30.41.mm], [189.mm,1087.95.mm,31.41.mm], [189.mm,1088.48.mm,32.49.mm], [189.mm,1088.87.mm,33.62.mm], [189.mm,1089.1.mm,34.8.mm], [189.mm,1089.18.mm,36.mm], [189.mm,1086.mm,36.mm], [189.mm,1085.95.mm,35.22.mm], [189.mm,1085.8.mm,34.45.mm], [189.mm,1085.54.mm,33.7.mm], [189.mm,1085.2.mm,33.mm], [189.mm,1084.76.mm,32.35.mm], [189.mm,1084.24.mm,31.76.mm], [189.mm,1083.65.mm,31.24.mm], [189.mm,1083.mm,30.8.mm], [189.mm,1082.3.mm,30.46.mm], [189.mm,1081.55.mm,30.2.mm], [189.mm,1080.78.mm,30.05.mm], [189.mm,1080.mm,30.mm], [189.mm,1079.22.mm,30.05.mm], [189.mm,1078.45.mm,30.2.mm], [189.mm,1077.7.mm,30.46.mm], [189.mm,1077.mm,30.8.mm], [189.mm,1076.35.mm,31.24.mm], [189.mm,1075.76.mm,31.76.mm], [189.mm,1075.24.mm,32.35.mm], [189.mm,1074.8.mm,33.mm], [189.mm,1074.46.mm,33.7.mm], [189.mm,1074.2.mm,34.45.mm], [189.mm,1074.05.mm,35.22.mm], [189.mm,1074.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(19.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([189.mm,1062.mm,34.82.mm], [208.mm,1062.mm,34.82.mm], [208.mm,1074.mm,34.82.mm], [189.mm,1074.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([198.5.mm,1068.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([189.mm,1086.mm,34.82.mm], [208.mm,1086.mm,34.82.mm], [208.mm,1098.mm,34.82.mm], [189.mm,1098.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([198.5.mm,1092.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = ge.add_face([[232.mm,1070.82.mm,36.mm], [232.mm,1070.9.mm,34.8.mm], [232.mm,1071.13.mm,33.62.mm], [232.mm,1071.52.mm,32.49.mm], [232.mm,1072.05.mm,31.41.mm], [232.mm,1072.72.mm,30.41.mm], [232.mm,1073.51.mm,29.51.mm], [232.mm,1074.41.mm,28.72.mm], [232.mm,1075.41.mm,28.05.mm], [232.mm,1076.49.mm,27.52.mm], [232.mm,1077.62.mm,27.13.mm], [232.mm,1078.8.mm,26.9.mm], [232.mm,1080.mm,26.82.mm], [232.mm,1081.2.mm,26.9.mm], [232.mm,1082.38.mm,27.13.mm], [232.mm,1083.51.mm,27.52.mm], [232.mm,1084.59.mm,28.05.mm], [232.mm,1085.59.mm,28.72.mm], [232.mm,1086.49.mm,29.51.mm], [232.mm,1087.28.mm,30.41.mm], [232.mm,1087.95.mm,31.41.mm], [232.mm,1088.48.mm,32.49.mm], [232.mm,1088.87.mm,33.62.mm], [232.mm,1089.1.mm,34.8.mm], [232.mm,1089.18.mm,36.mm], [232.mm,1086.mm,36.mm], [232.mm,1085.95.mm,35.22.mm], [232.mm,1085.8.mm,34.45.mm], [232.mm,1085.54.mm,33.7.mm], [232.mm,1085.2.mm,33.mm], [232.mm,1084.76.mm,32.35.mm], [232.mm,1084.24.mm,31.76.mm], [232.mm,1083.65.mm,31.24.mm], [232.mm,1083.mm,30.8.mm], [232.mm,1082.3.mm,30.46.mm], [232.mm,1081.55.mm,30.2.mm], [232.mm,1080.78.mm,30.05.mm], [232.mm,1080.mm,30.mm], [232.mm,1079.22.mm,30.05.mm], [232.mm,1078.45.mm,30.2.mm], [232.mm,1077.7.mm,30.46.mm], [232.mm,1077.mm,30.8.mm], [232.mm,1076.35.mm,31.24.mm], [232.mm,1075.76.mm,31.76.mm], [232.mm,1075.24.mm,32.35.mm], [232.mm,1074.8.mm,33.mm], [232.mm,1074.46.mm,33.7.mm], [232.mm,1074.2.mm,34.45.mm], [232.mm,1074.05.mm,35.22.mm], [232.mm,1074.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(19.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([232.mm,1062.mm,34.82.mm], [251.mm,1062.mm,34.82.mm], [251.mm,1074.mm,34.82.mm], [232.mm,1074.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([241.5.mm,1068.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([232.mm,1086.mm,34.82.mm], [251.mm,1086.mm,34.82.mm], [251.mm,1098.mm,34.82.mm], [232.mm,1098.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([241.5.mm,1092.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  circle = ge.add_circle([187.mm,1280.mm,36.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(66.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle L
  grp = ents.add_group
  grp.name = "Axle Saddle L"
  ge = grp.entities
  face = ge.add_face([[189.mm,1270.82.mm,36.mm], [189.mm,1270.9.mm,34.8.mm], [189.mm,1271.13.mm,33.62.mm], [189.mm,1271.52.mm,32.49.mm], [189.mm,1272.05.mm,31.41.mm], [189.mm,1272.72.mm,30.41.mm], [189.mm,1273.51.mm,29.51.mm], [189.mm,1274.41.mm,28.72.mm], [189.mm,1275.41.mm,28.05.mm], [189.mm,1276.49.mm,27.52.mm], [189.mm,1277.62.mm,27.13.mm], [189.mm,1278.8.mm,26.9.mm], [189.mm,1280.mm,26.82.mm], [189.mm,1281.2.mm,26.9.mm], [189.mm,1282.38.mm,27.13.mm], [189.mm,1283.51.mm,27.52.mm], [189.mm,1284.59.mm,28.05.mm], [189.mm,1285.59.mm,28.72.mm], [189.mm,1286.49.mm,29.51.mm], [189.mm,1287.28.mm,30.41.mm], [189.mm,1287.95.mm,31.41.mm], [189.mm,1288.48.mm,32.49.mm], [189.mm,1288.87.mm,33.62.mm], [189.mm,1289.1.mm,34.8.mm], [189.mm,1289.18.mm,36.mm], [189.mm,1286.mm,36.mm], [189.mm,1285.95.mm,35.22.mm], [189.mm,1285.8.mm,34.45.mm], [189.mm,1285.54.mm,33.7.mm], [189.mm,1285.2.mm,33.mm], [189.mm,1284.76.mm,32.35.mm], [189.mm,1284.24.mm,31.76.mm], [189.mm,1283.65.mm,31.24.mm], [189.mm,1283.mm,30.8.mm], [189.mm,1282.3.mm,30.46.mm], [189.mm,1281.55.mm,30.2.mm], [189.mm,1280.78.mm,30.05.mm], [189.mm,1280.mm,30.mm], [189.mm,1279.22.mm,30.05.mm], [189.mm,1278.45.mm,30.2.mm], [189.mm,1277.7.mm,30.46.mm], [189.mm,1277.mm,30.8.mm], [189.mm,1276.35.mm,31.24.mm], [189.mm,1275.76.mm,31.76.mm], [189.mm,1275.24.mm,32.35.mm], [189.mm,1274.8.mm,33.mm], [189.mm,1274.46.mm,33.7.mm], [189.mm,1274.2.mm,34.45.mm], [189.mm,1274.05.mm,35.22.mm], [189.mm,1274.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(19.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([189.mm,1262.mm,34.82.mm], [208.mm,1262.mm,34.82.mm], [208.mm,1274.mm,34.82.mm], [189.mm,1274.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([198.5.mm,1268.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([189.mm,1286.mm,34.82.mm], [208.mm,1286.mm,34.82.mm], [208.mm,1298.mm,34.82.mm], [189.mm,1298.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([198.5.mm,1292.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = ge.add_face([[232.mm,1270.82.mm,36.mm], [232.mm,1270.9.mm,34.8.mm], [232.mm,1271.13.mm,33.62.mm], [232.mm,1271.52.mm,32.49.mm], [232.mm,1272.05.mm,31.41.mm], [232.mm,1272.72.mm,30.41.mm], [232.mm,1273.51.mm,29.51.mm], [232.mm,1274.41.mm,28.72.mm], [232.mm,1275.41.mm,28.05.mm], [232.mm,1276.49.mm,27.52.mm], [232.mm,1277.62.mm,27.13.mm], [232.mm,1278.8.mm,26.9.mm], [232.mm,1280.mm,26.82.mm], [232.mm,1281.2.mm,26.9.mm], [232.mm,1282.38.mm,27.13.mm], [232.mm,1283.51.mm,27.52.mm], [232.mm,1284.59.mm,28.05.mm], [232.mm,1285.59.mm,28.72.mm], [232.mm,1286.49.mm,29.51.mm], [232.mm,1287.28.mm,30.41.mm], [232.mm,1287.95.mm,31.41.mm], [232.mm,1288.48.mm,32.49.mm], [232.mm,1288.87.mm,33.62.mm], [232.mm,1289.1.mm,34.8.mm], [232.mm,1289.18.mm,36.mm], [232.mm,1286.mm,36.mm], [232.mm,1285.95.mm,35.22.mm], [232.mm,1285.8.mm,34.45.mm], [232.mm,1285.54.mm,33.7.mm], [232.mm,1285.2.mm,33.mm], [232.mm,1284.76.mm,32.35.mm], [232.mm,1284.24.mm,31.76.mm], [232.mm,1283.65.mm,31.24.mm], [232.mm,1283.mm,30.8.mm], [232.mm,1282.3.mm,30.46.mm], [232.mm,1281.55.mm,30.2.mm], [232.mm,1280.78.mm,30.05.mm], [232.mm,1280.mm,30.mm], [232.mm,1279.22.mm,30.05.mm], [232.mm,1278.45.mm,30.2.mm], [232.mm,1277.7.mm,30.46.mm], [232.mm,1277.mm,30.8.mm], [232.mm,1276.35.mm,31.24.mm], [232.mm,1275.76.mm,31.76.mm], [232.mm,1275.24.mm,32.35.mm], [232.mm,1274.8.mm,33.mm], [232.mm,1274.46.mm,33.7.mm], [232.mm,1274.2.mm,34.45.mm], [232.mm,1274.05.mm,35.22.mm], [232.mm,1274.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(19.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([232.mm,1262.mm,34.82.mm], [251.mm,1262.mm,34.82.mm], [251.mm,1274.mm,34.82.mm], [232.mm,1274.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([241.5.mm,1268.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([232.mm,1286.mm,34.82.mm], [251.mm,1286.mm,34.82.mm], [251.mm,1298.mm,34.82.mm], [232.mm,1298.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([241.5.mm,1292.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Top Clamp L
  grp = ents.add_group
  grp.name = "Top Clamp L"
  face = grp.entities.add_face([200.mm,1148.mm,54.mm], [240.mm,1148.mm,54.mm], [240.mm,1212.mm,54.mm], [200.mm,1212.mm,54.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
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
  circle = ge.add_circle([209.mm,1156.mm,26.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(35.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt CSK Head L
  grp = ents.add_group
  grp.name = "Clamp Bolt CSK Head L"
  ge = grp.entities
  ge.add_face([213.5.mm,1156.mm,26.mm], [212.89711431702997.mm,1158.25.mm,26.mm], [211.1650635094611.mm,1157.25.mm,29.mm], [211.5.mm,1156.mm,29.mm])
  ge.add_face([212.89711431702997.mm,1158.25.mm,26.mm], [211.25.mm,1159.89711431703.mm,26.mm], [210.25.mm,1158.165063509461.mm,29.mm], [211.1650635094611.mm,1157.25.mm,29.mm])
  ge.add_face([211.25.mm,1159.89711431703.mm,26.mm], [209.mm,1160.5.mm,26.mm], [209.mm,1158.5.mm,29.mm], [210.25.mm,1158.165063509461.mm,29.mm])
  ge.add_face([209.mm,1160.5.mm,26.mm], [206.75.mm,1159.89711431703.mm,26.mm], [207.75.mm,1158.165063509461.mm,29.mm], [209.mm,1158.5.mm,29.mm])
  ge.add_face([206.75.mm,1159.89711431703.mm,26.mm], [205.10288568297003.mm,1158.25.mm,26.mm], [206.8349364905389.mm,1157.25.mm,29.mm], [207.75.mm,1158.165063509461.mm,29.mm])
  ge.add_face([205.10288568297003.mm,1158.25.mm,26.mm], [204.5.mm,1156.mm,26.mm], [206.5.mm,1156.mm,29.mm], [206.8349364905389.mm,1157.25.mm,29.mm])
  ge.add_face([204.5.mm,1156.mm,26.mm], [205.10288568297003.mm,1153.75.mm,26.mm], [206.8349364905389.mm,1154.75.mm,29.mm], [206.5.mm,1156.mm,29.mm])
  ge.add_face([205.10288568297003.mm,1153.75.mm,26.mm], [206.75.mm,1152.10288568297.mm,26.mm], [207.75.mm,1153.834936490539.mm,29.mm], [206.8349364905389.mm,1154.75.mm,29.mm])
  ge.add_face([206.75.mm,1152.10288568297.mm,26.mm], [209.mm,1151.5.mm,26.mm], [209.mm,1153.5.mm,29.mm], [207.75.mm,1153.834936490539.mm,29.mm])
  ge.add_face([209.mm,1151.5.mm,26.mm], [211.25.mm,1152.10288568297.mm,26.mm], [210.25.mm,1153.834936490539.mm,29.mm], [209.mm,1153.5.mm,29.mm])
  ge.add_face([211.25.mm,1152.10288568297.mm,26.mm], [212.89711431702997.mm,1153.75.mm,26.mm], [211.1650635094611.mm,1154.75.mm,29.mm], [210.25.mm,1153.834936490539.mm,29.mm])
  ge.add_face([212.89711431702997.mm,1153.75.mm,26.mm], [213.5.mm,1156.mm,26.mm], [211.5.mm,1156.mm,29.mm], [211.1650635094611.mm,1154.75.mm,29.mm])
  ge.add_face([213.5.mm,1156.mm,26.mm], [212.89711431702997.mm,1158.25.mm,26.mm], [211.25.mm,1159.89711431703.mm,26.mm], [209.mm,1160.5.mm,26.mm], [206.75.mm,1159.89711431703.mm,26.mm], [205.10288568297003.mm,1158.25.mm,26.mm], [204.5.mm,1156.mm,26.mm], [205.10288568297003.mm,1153.75.mm,26.mm], [206.75.mm,1152.10288568297.mm,26.mm], [209.mm,1151.5.mm,26.mm], [211.25.mm,1152.10288568297.mm,26.mm], [212.89711431702997.mm,1153.75.mm,26.mm])
  mat = model.materials["Clamp Bolt CSK Head L"] || model.materials.add("Clamp Bolt CSK Head L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  grp.material = mat

  # Clamp Bolt L
  grp = ents.add_group
  grp.name = "Clamp Bolt L"
  ge = grp.entities
  circle = ge.add_circle([231.mm,1156.mm,26.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(35.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt CSK Head L
  grp = ents.add_group
  grp.name = "Clamp Bolt CSK Head L"
  ge = grp.entities
  ge.add_face([235.5.mm,1156.mm,26.mm], [234.89711431702997.mm,1158.25.mm,26.mm], [233.1650635094611.mm,1157.25.mm,29.mm], [233.5.mm,1156.mm,29.mm])
  ge.add_face([234.89711431702997.mm,1158.25.mm,26.mm], [233.25.mm,1159.89711431703.mm,26.mm], [232.25.mm,1158.165063509461.mm,29.mm], [233.1650635094611.mm,1157.25.mm,29.mm])
  ge.add_face([233.25.mm,1159.89711431703.mm,26.mm], [231.mm,1160.5.mm,26.mm], [231.mm,1158.5.mm,29.mm], [232.25.mm,1158.165063509461.mm,29.mm])
  ge.add_face([231.mm,1160.5.mm,26.mm], [228.75.mm,1159.89711431703.mm,26.mm], [229.75.mm,1158.165063509461.mm,29.mm], [231.mm,1158.5.mm,29.mm])
  ge.add_face([228.75.mm,1159.89711431703.mm,26.mm], [227.10288568297003.mm,1158.25.mm,26.mm], [228.8349364905389.mm,1157.25.mm,29.mm], [229.75.mm,1158.165063509461.mm,29.mm])
  ge.add_face([227.10288568297003.mm,1158.25.mm,26.mm], [226.5.mm,1156.mm,26.mm], [228.5.mm,1156.mm,29.mm], [228.8349364905389.mm,1157.25.mm,29.mm])
  ge.add_face([226.5.mm,1156.mm,26.mm], [227.10288568297003.mm,1153.75.mm,26.mm], [228.8349364905389.mm,1154.75.mm,29.mm], [228.5.mm,1156.mm,29.mm])
  ge.add_face([227.10288568297003.mm,1153.75.mm,26.mm], [228.75.mm,1152.10288568297.mm,26.mm], [229.75.mm,1153.834936490539.mm,29.mm], [228.8349364905389.mm,1154.75.mm,29.mm])
  ge.add_face([228.75.mm,1152.10288568297.mm,26.mm], [231.mm,1151.5.mm,26.mm], [231.mm,1153.5.mm,29.mm], [229.75.mm,1153.834936490539.mm,29.mm])
  ge.add_face([231.mm,1151.5.mm,26.mm], [233.25.mm,1152.10288568297.mm,26.mm], [232.25.mm,1153.834936490539.mm,29.mm], [231.mm,1153.5.mm,29.mm])
  ge.add_face([233.25.mm,1152.10288568297.mm,26.mm], [234.89711431702997.mm,1153.75.mm,26.mm], [233.1650635094611.mm,1154.75.mm,29.mm], [232.25.mm,1153.834936490539.mm,29.mm])
  ge.add_face([234.89711431702997.mm,1153.75.mm,26.mm], [235.5.mm,1156.mm,26.mm], [233.5.mm,1156.mm,29.mm], [233.1650635094611.mm,1154.75.mm,29.mm])
  ge.add_face([235.5.mm,1156.mm,26.mm], [234.89711431702997.mm,1158.25.mm,26.mm], [233.25.mm,1159.89711431703.mm,26.mm], [231.mm,1160.5.mm,26.mm], [228.75.mm,1159.89711431703.mm,26.mm], [227.10288568297003.mm,1158.25.mm,26.mm], [226.5.mm,1156.mm,26.mm], [227.10288568297003.mm,1153.75.mm,26.mm], [228.75.mm,1152.10288568297.mm,26.mm], [231.mm,1151.5.mm,26.mm], [233.25.mm,1152.10288568297.mm,26.mm], [234.89711431702997.mm,1153.75.mm,26.mm])
  mat = model.materials["Clamp Bolt CSK Head L"] || model.materials.add("Clamp Bolt CSK Head L")
  mat.color = Sketchup::Color.new(128, 128, 138)
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
  circle = ge.add_circle([209.mm,1204.mm,26.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(35.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt CSK Head L
  grp = ents.add_group
  grp.name = "Clamp Bolt CSK Head L"
  ge = grp.entities
  ge.add_face([213.5.mm,1204.mm,26.mm], [212.89711431702997.mm,1206.25.mm,26.mm], [211.1650635094611.mm,1205.25.mm,29.mm], [211.5.mm,1204.mm,29.mm])
  ge.add_face([212.89711431702997.mm,1206.25.mm,26.mm], [211.25.mm,1207.89711431703.mm,26.mm], [210.25.mm,1206.165063509461.mm,29.mm], [211.1650635094611.mm,1205.25.mm,29.mm])
  ge.add_face([211.25.mm,1207.89711431703.mm,26.mm], [209.mm,1208.5.mm,26.mm], [209.mm,1206.5.mm,29.mm], [210.25.mm,1206.165063509461.mm,29.mm])
  ge.add_face([209.mm,1208.5.mm,26.mm], [206.75.mm,1207.89711431703.mm,26.mm], [207.75.mm,1206.165063509461.mm,29.mm], [209.mm,1206.5.mm,29.mm])
  ge.add_face([206.75.mm,1207.89711431703.mm,26.mm], [205.10288568297003.mm,1206.25.mm,26.mm], [206.8349364905389.mm,1205.25.mm,29.mm], [207.75.mm,1206.165063509461.mm,29.mm])
  ge.add_face([205.10288568297003.mm,1206.25.mm,26.mm], [204.5.mm,1204.mm,26.mm], [206.5.mm,1204.mm,29.mm], [206.8349364905389.mm,1205.25.mm,29.mm])
  ge.add_face([204.5.mm,1204.mm,26.mm], [205.10288568297003.mm,1201.75.mm,26.mm], [206.8349364905389.mm,1202.75.mm,29.mm], [206.5.mm,1204.mm,29.mm])
  ge.add_face([205.10288568297003.mm,1201.75.mm,26.mm], [206.75.mm,1200.10288568297.mm,26.mm], [207.75.mm,1201.834936490539.mm,29.mm], [206.8349364905389.mm,1202.75.mm,29.mm])
  ge.add_face([206.75.mm,1200.10288568297.mm,26.mm], [209.mm,1199.5.mm,26.mm], [209.mm,1201.5.mm,29.mm], [207.75.mm,1201.834936490539.mm,29.mm])
  ge.add_face([209.mm,1199.5.mm,26.mm], [211.25.mm,1200.10288568297.mm,26.mm], [210.25.mm,1201.834936490539.mm,29.mm], [209.mm,1201.5.mm,29.mm])
  ge.add_face([211.25.mm,1200.10288568297.mm,26.mm], [212.89711431702997.mm,1201.75.mm,26.mm], [211.1650635094611.mm,1202.75.mm,29.mm], [210.25.mm,1201.834936490539.mm,29.mm])
  ge.add_face([212.89711431702997.mm,1201.75.mm,26.mm], [213.5.mm,1204.mm,26.mm], [211.5.mm,1204.mm,29.mm], [211.1650635094611.mm,1202.75.mm,29.mm])
  ge.add_face([213.5.mm,1204.mm,26.mm], [212.89711431702997.mm,1206.25.mm,26.mm], [211.25.mm,1207.89711431703.mm,26.mm], [209.mm,1208.5.mm,26.mm], [206.75.mm,1207.89711431703.mm,26.mm], [205.10288568297003.mm,1206.25.mm,26.mm], [204.5.mm,1204.mm,26.mm], [205.10288568297003.mm,1201.75.mm,26.mm], [206.75.mm,1200.10288568297.mm,26.mm], [209.mm,1199.5.mm,26.mm], [211.25.mm,1200.10288568297.mm,26.mm], [212.89711431702997.mm,1201.75.mm,26.mm])
  mat = model.materials["Clamp Bolt CSK Head L"] || model.materials.add("Clamp Bolt CSK Head L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  grp.material = mat

  # Clamp Bolt L
  grp = ents.add_group
  grp.name = "Clamp Bolt L"
  ge = grp.entities
  circle = ge.add_circle([231.mm,1204.mm,26.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(35.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt CSK Head L
  grp = ents.add_group
  grp.name = "Clamp Bolt CSK Head L"
  ge = grp.entities
  ge.add_face([235.5.mm,1204.mm,26.mm], [234.89711431702997.mm,1206.25.mm,26.mm], [233.1650635094611.mm,1205.25.mm,29.mm], [233.5.mm,1204.mm,29.mm])
  ge.add_face([234.89711431702997.mm,1206.25.mm,26.mm], [233.25.mm,1207.89711431703.mm,26.mm], [232.25.mm,1206.165063509461.mm,29.mm], [233.1650635094611.mm,1205.25.mm,29.mm])
  ge.add_face([233.25.mm,1207.89711431703.mm,26.mm], [231.mm,1208.5.mm,26.mm], [231.mm,1206.5.mm,29.mm], [232.25.mm,1206.165063509461.mm,29.mm])
  ge.add_face([231.mm,1208.5.mm,26.mm], [228.75.mm,1207.89711431703.mm,26.mm], [229.75.mm,1206.165063509461.mm,29.mm], [231.mm,1206.5.mm,29.mm])
  ge.add_face([228.75.mm,1207.89711431703.mm,26.mm], [227.10288568297003.mm,1206.25.mm,26.mm], [228.8349364905389.mm,1205.25.mm,29.mm], [229.75.mm,1206.165063509461.mm,29.mm])
  ge.add_face([227.10288568297003.mm,1206.25.mm,26.mm], [226.5.mm,1204.mm,26.mm], [228.5.mm,1204.mm,29.mm], [228.8349364905389.mm,1205.25.mm,29.mm])
  ge.add_face([226.5.mm,1204.mm,26.mm], [227.10288568297003.mm,1201.75.mm,26.mm], [228.8349364905389.mm,1202.75.mm,29.mm], [228.5.mm,1204.mm,29.mm])
  ge.add_face([227.10288568297003.mm,1201.75.mm,26.mm], [228.75.mm,1200.10288568297.mm,26.mm], [229.75.mm,1201.834936490539.mm,29.mm], [228.8349364905389.mm,1202.75.mm,29.mm])
  ge.add_face([228.75.mm,1200.10288568297.mm,26.mm], [231.mm,1199.5.mm,26.mm], [231.mm,1201.5.mm,29.mm], [229.75.mm,1201.834936490539.mm,29.mm])
  ge.add_face([231.mm,1199.5.mm,26.mm], [233.25.mm,1200.10288568297.mm,26.mm], [232.25.mm,1201.834936490539.mm,29.mm], [231.mm,1201.5.mm,29.mm])
  ge.add_face([233.25.mm,1200.10288568297.mm,26.mm], [234.89711431702997.mm,1201.75.mm,26.mm], [233.1650635094611.mm,1202.75.mm,29.mm], [232.25.mm,1201.834936490539.mm,29.mm])
  ge.add_face([234.89711431702997.mm,1201.75.mm,26.mm], [235.5.mm,1204.mm,26.mm], [233.5.mm,1204.mm,29.mm], [233.1650635094611.mm,1202.75.mm,29.mm])
  ge.add_face([235.5.mm,1204.mm,26.mm], [234.89711431702997.mm,1206.25.mm,26.mm], [233.25.mm,1207.89711431703.mm,26.mm], [231.mm,1208.5.mm,26.mm], [228.75.mm,1207.89711431703.mm,26.mm], [227.10288568297003.mm,1206.25.mm,26.mm], [226.5.mm,1204.mm,26.mm], [227.10288568297003.mm,1201.75.mm,26.mm], [228.75.mm,1200.10288568297.mm,26.mm], [231.mm,1199.5.mm,26.mm], [233.25.mm,1200.10288568297.mm,26.mm], [234.89711431702997.mm,1201.75.mm,26.mm])
  mat = model.materials["Clamp Bolt CSK Head L"] || model.materials.add("Clamp Bolt CSK Head L")
  mat.color = Sketchup::Color.new(128, 128, 138)
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
  circle = ge.add_circle([4546.mm,1080.mm,36.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(66.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle R
  grp = ents.add_group
  grp.name = "Axle Saddle R"
  ge = grp.entities
  face = ge.add_face([[4548.mm,1070.82.mm,36.mm], [4548.mm,1070.9.mm,34.8.mm], [4548.mm,1071.13.mm,33.62.mm], [4548.mm,1071.52.mm,32.49.mm], [4548.mm,1072.05.mm,31.41.mm], [4548.mm,1072.72.mm,30.41.mm], [4548.mm,1073.51.mm,29.51.mm], [4548.mm,1074.41.mm,28.72.mm], [4548.mm,1075.41.mm,28.05.mm], [4548.mm,1076.49.mm,27.52.mm], [4548.mm,1077.62.mm,27.13.mm], [4548.mm,1078.8.mm,26.9.mm], [4548.mm,1080.mm,26.82.mm], [4548.mm,1081.2.mm,26.9.mm], [4548.mm,1082.38.mm,27.13.mm], [4548.mm,1083.51.mm,27.52.mm], [4548.mm,1084.59.mm,28.05.mm], [4548.mm,1085.59.mm,28.72.mm], [4548.mm,1086.49.mm,29.51.mm], [4548.mm,1087.28.mm,30.41.mm], [4548.mm,1087.95.mm,31.41.mm], [4548.mm,1088.48.mm,32.49.mm], [4548.mm,1088.87.mm,33.62.mm], [4548.mm,1089.1.mm,34.8.mm], [4548.mm,1089.18.mm,36.mm], [4548.mm,1086.mm,36.mm], [4548.mm,1085.95.mm,35.22.mm], [4548.mm,1085.8.mm,34.45.mm], [4548.mm,1085.54.mm,33.7.mm], [4548.mm,1085.2.mm,33.mm], [4548.mm,1084.76.mm,32.35.mm], [4548.mm,1084.24.mm,31.76.mm], [4548.mm,1083.65.mm,31.24.mm], [4548.mm,1083.mm,30.8.mm], [4548.mm,1082.3.mm,30.46.mm], [4548.mm,1081.55.mm,30.2.mm], [4548.mm,1080.78.mm,30.05.mm], [4548.mm,1080.mm,30.mm], [4548.mm,1079.22.mm,30.05.mm], [4548.mm,1078.45.mm,30.2.mm], [4548.mm,1077.7.mm,30.46.mm], [4548.mm,1077.mm,30.8.mm], [4548.mm,1076.35.mm,31.24.mm], [4548.mm,1075.76.mm,31.76.mm], [4548.mm,1075.24.mm,32.35.mm], [4548.mm,1074.8.mm,33.mm], [4548.mm,1074.46.mm,33.7.mm], [4548.mm,1074.2.mm,34.45.mm], [4548.mm,1074.05.mm,35.22.mm], [4548.mm,1074.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(19.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4548.mm,1062.mm,34.82.mm], [4567.mm,1062.mm,34.82.mm], [4567.mm,1074.mm,34.82.mm], [4548.mm,1074.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4557.5.mm,1068.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([4548.mm,1086.mm,34.82.mm], [4567.mm,1086.mm,34.82.mm], [4567.mm,1098.mm,34.82.mm], [4548.mm,1098.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4557.5.mm,1092.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = ge.add_face([[4591.mm,1070.82.mm,36.mm], [4591.mm,1070.9.mm,34.8.mm], [4591.mm,1071.13.mm,33.62.mm], [4591.mm,1071.52.mm,32.49.mm], [4591.mm,1072.05.mm,31.41.mm], [4591.mm,1072.72.mm,30.41.mm], [4591.mm,1073.51.mm,29.51.mm], [4591.mm,1074.41.mm,28.72.mm], [4591.mm,1075.41.mm,28.05.mm], [4591.mm,1076.49.mm,27.52.mm], [4591.mm,1077.62.mm,27.13.mm], [4591.mm,1078.8.mm,26.9.mm], [4591.mm,1080.mm,26.82.mm], [4591.mm,1081.2.mm,26.9.mm], [4591.mm,1082.38.mm,27.13.mm], [4591.mm,1083.51.mm,27.52.mm], [4591.mm,1084.59.mm,28.05.mm], [4591.mm,1085.59.mm,28.72.mm], [4591.mm,1086.49.mm,29.51.mm], [4591.mm,1087.28.mm,30.41.mm], [4591.mm,1087.95.mm,31.41.mm], [4591.mm,1088.48.mm,32.49.mm], [4591.mm,1088.87.mm,33.62.mm], [4591.mm,1089.1.mm,34.8.mm], [4591.mm,1089.18.mm,36.mm], [4591.mm,1086.mm,36.mm], [4591.mm,1085.95.mm,35.22.mm], [4591.mm,1085.8.mm,34.45.mm], [4591.mm,1085.54.mm,33.7.mm], [4591.mm,1085.2.mm,33.mm], [4591.mm,1084.76.mm,32.35.mm], [4591.mm,1084.24.mm,31.76.mm], [4591.mm,1083.65.mm,31.24.mm], [4591.mm,1083.mm,30.8.mm], [4591.mm,1082.3.mm,30.46.mm], [4591.mm,1081.55.mm,30.2.mm], [4591.mm,1080.78.mm,30.05.mm], [4591.mm,1080.mm,30.mm], [4591.mm,1079.22.mm,30.05.mm], [4591.mm,1078.45.mm,30.2.mm], [4591.mm,1077.7.mm,30.46.mm], [4591.mm,1077.mm,30.8.mm], [4591.mm,1076.35.mm,31.24.mm], [4591.mm,1075.76.mm,31.76.mm], [4591.mm,1075.24.mm,32.35.mm], [4591.mm,1074.8.mm,33.mm], [4591.mm,1074.46.mm,33.7.mm], [4591.mm,1074.2.mm,34.45.mm], [4591.mm,1074.05.mm,35.22.mm], [4591.mm,1074.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(19.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4591.mm,1062.mm,34.82.mm], [4610.mm,1062.mm,34.82.mm], [4610.mm,1074.mm,34.82.mm], [4591.mm,1074.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4600.5.mm,1068.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([4591.mm,1086.mm,34.82.mm], [4610.mm,1086.mm,34.82.mm], [4610.mm,1098.mm,34.82.mm], [4591.mm,1098.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4600.5.mm,1092.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  circle = ge.add_circle([4546.mm,1280.mm,36.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(66.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle R
  grp = ents.add_group
  grp.name = "Axle Saddle R"
  ge = grp.entities
  face = ge.add_face([[4548.mm,1270.82.mm,36.mm], [4548.mm,1270.9.mm,34.8.mm], [4548.mm,1271.13.mm,33.62.mm], [4548.mm,1271.52.mm,32.49.mm], [4548.mm,1272.05.mm,31.41.mm], [4548.mm,1272.72.mm,30.41.mm], [4548.mm,1273.51.mm,29.51.mm], [4548.mm,1274.41.mm,28.72.mm], [4548.mm,1275.41.mm,28.05.mm], [4548.mm,1276.49.mm,27.52.mm], [4548.mm,1277.62.mm,27.13.mm], [4548.mm,1278.8.mm,26.9.mm], [4548.mm,1280.mm,26.82.mm], [4548.mm,1281.2.mm,26.9.mm], [4548.mm,1282.38.mm,27.13.mm], [4548.mm,1283.51.mm,27.52.mm], [4548.mm,1284.59.mm,28.05.mm], [4548.mm,1285.59.mm,28.72.mm], [4548.mm,1286.49.mm,29.51.mm], [4548.mm,1287.28.mm,30.41.mm], [4548.mm,1287.95.mm,31.41.mm], [4548.mm,1288.48.mm,32.49.mm], [4548.mm,1288.87.mm,33.62.mm], [4548.mm,1289.1.mm,34.8.mm], [4548.mm,1289.18.mm,36.mm], [4548.mm,1286.mm,36.mm], [4548.mm,1285.95.mm,35.22.mm], [4548.mm,1285.8.mm,34.45.mm], [4548.mm,1285.54.mm,33.7.mm], [4548.mm,1285.2.mm,33.mm], [4548.mm,1284.76.mm,32.35.mm], [4548.mm,1284.24.mm,31.76.mm], [4548.mm,1283.65.mm,31.24.mm], [4548.mm,1283.mm,30.8.mm], [4548.mm,1282.3.mm,30.46.mm], [4548.mm,1281.55.mm,30.2.mm], [4548.mm,1280.78.mm,30.05.mm], [4548.mm,1280.mm,30.mm], [4548.mm,1279.22.mm,30.05.mm], [4548.mm,1278.45.mm,30.2.mm], [4548.mm,1277.7.mm,30.46.mm], [4548.mm,1277.mm,30.8.mm], [4548.mm,1276.35.mm,31.24.mm], [4548.mm,1275.76.mm,31.76.mm], [4548.mm,1275.24.mm,32.35.mm], [4548.mm,1274.8.mm,33.mm], [4548.mm,1274.46.mm,33.7.mm], [4548.mm,1274.2.mm,34.45.mm], [4548.mm,1274.05.mm,35.22.mm], [4548.mm,1274.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(19.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4548.mm,1262.mm,34.82.mm], [4567.mm,1262.mm,34.82.mm], [4567.mm,1274.mm,34.82.mm], [4548.mm,1274.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4557.5.mm,1268.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([4548.mm,1286.mm,34.82.mm], [4567.mm,1286.mm,34.82.mm], [4567.mm,1298.mm,34.82.mm], [4548.mm,1298.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4557.5.mm,1292.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = ge.add_face([[4591.mm,1270.82.mm,36.mm], [4591.mm,1270.9.mm,34.8.mm], [4591.mm,1271.13.mm,33.62.mm], [4591.mm,1271.52.mm,32.49.mm], [4591.mm,1272.05.mm,31.41.mm], [4591.mm,1272.72.mm,30.41.mm], [4591.mm,1273.51.mm,29.51.mm], [4591.mm,1274.41.mm,28.72.mm], [4591.mm,1275.41.mm,28.05.mm], [4591.mm,1276.49.mm,27.52.mm], [4591.mm,1277.62.mm,27.13.mm], [4591.mm,1278.8.mm,26.9.mm], [4591.mm,1280.mm,26.82.mm], [4591.mm,1281.2.mm,26.9.mm], [4591.mm,1282.38.mm,27.13.mm], [4591.mm,1283.51.mm,27.52.mm], [4591.mm,1284.59.mm,28.05.mm], [4591.mm,1285.59.mm,28.72.mm], [4591.mm,1286.49.mm,29.51.mm], [4591.mm,1287.28.mm,30.41.mm], [4591.mm,1287.95.mm,31.41.mm], [4591.mm,1288.48.mm,32.49.mm], [4591.mm,1288.87.mm,33.62.mm], [4591.mm,1289.1.mm,34.8.mm], [4591.mm,1289.18.mm,36.mm], [4591.mm,1286.mm,36.mm], [4591.mm,1285.95.mm,35.22.mm], [4591.mm,1285.8.mm,34.45.mm], [4591.mm,1285.54.mm,33.7.mm], [4591.mm,1285.2.mm,33.mm], [4591.mm,1284.76.mm,32.35.mm], [4591.mm,1284.24.mm,31.76.mm], [4591.mm,1283.65.mm,31.24.mm], [4591.mm,1283.mm,30.8.mm], [4591.mm,1282.3.mm,30.46.mm], [4591.mm,1281.55.mm,30.2.mm], [4591.mm,1280.78.mm,30.05.mm], [4591.mm,1280.mm,30.mm], [4591.mm,1279.22.mm,30.05.mm], [4591.mm,1278.45.mm,30.2.mm], [4591.mm,1277.7.mm,30.46.mm], [4591.mm,1277.mm,30.8.mm], [4591.mm,1276.35.mm,31.24.mm], [4591.mm,1275.76.mm,31.76.mm], [4591.mm,1275.24.mm,32.35.mm], [4591.mm,1274.8.mm,33.mm], [4591.mm,1274.46.mm,33.7.mm], [4591.mm,1274.2.mm,34.45.mm], [4591.mm,1274.05.mm,35.22.mm], [4591.mm,1274.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(19.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4591.mm,1262.mm,34.82.mm], [4610.mm,1262.mm,34.82.mm], [4610.mm,1274.mm,34.82.mm], [4591.mm,1274.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4600.5.mm,1268.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  face = grp.entities.add_face([4591.mm,1286.mm,34.82.mm], [4610.mm,1286.mm,34.82.mm], [4610.mm,1298.mm,34.82.mm], [4591.mm,1298.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4600.5.mm,1292.mm,34.mm], [0,0,1], 2.5.mm, 24)
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
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Top Clamp R
  grp = ents.add_group
  grp.name = "Top Clamp R"
  face = grp.entities.add_face([4559.mm,1148.mm,54.mm], [4599.mm,1148.mm,54.mm], [4599.mm,1212.mm,54.mm], [4559.mm,1212.mm,54.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
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
  circle = ge.add_circle([4568.mm,1156.mm,26.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(35.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt CSK Head R
  grp = ents.add_group
  grp.name = "Clamp Bolt CSK Head R"
  ge = grp.entities
  ge.add_face([4572.5.mm,1156.mm,26.mm], [4571.89711431703.mm,1158.25.mm,26.mm], [4570.165063509461.mm,1157.25.mm,29.mm], [4570.5.mm,1156.mm,29.mm])
  ge.add_face([4571.89711431703.mm,1158.25.mm,26.mm], [4570.25.mm,1159.89711431703.mm,26.mm], [4569.25.mm,1158.165063509461.mm,29.mm], [4570.165063509461.mm,1157.25.mm,29.mm])
  ge.add_face([4570.25.mm,1159.89711431703.mm,26.mm], [4568.mm,1160.5.mm,26.mm], [4568.mm,1158.5.mm,29.mm], [4569.25.mm,1158.165063509461.mm,29.mm])
  ge.add_face([4568.mm,1160.5.mm,26.mm], [4565.75.mm,1159.89711431703.mm,26.mm], [4566.75.mm,1158.165063509461.mm,29.mm], [4568.mm,1158.5.mm,29.mm])
  ge.add_face([4565.75.mm,1159.89711431703.mm,26.mm], [4564.10288568297.mm,1158.25.mm,26.mm], [4565.834936490539.mm,1157.25.mm,29.mm], [4566.75.mm,1158.165063509461.mm,29.mm])
  ge.add_face([4564.10288568297.mm,1158.25.mm,26.mm], [4563.5.mm,1156.mm,26.mm], [4565.5.mm,1156.mm,29.mm], [4565.834936490539.mm,1157.25.mm,29.mm])
  ge.add_face([4563.5.mm,1156.mm,26.mm], [4564.10288568297.mm,1153.75.mm,26.mm], [4565.834936490539.mm,1154.75.mm,29.mm], [4565.5.mm,1156.mm,29.mm])
  ge.add_face([4564.10288568297.mm,1153.75.mm,26.mm], [4565.75.mm,1152.10288568297.mm,26.mm], [4566.75.mm,1153.834936490539.mm,29.mm], [4565.834936490539.mm,1154.75.mm,29.mm])
  ge.add_face([4565.75.mm,1152.10288568297.mm,26.mm], [4568.mm,1151.5.mm,26.mm], [4568.mm,1153.5.mm,29.mm], [4566.75.mm,1153.834936490539.mm,29.mm])
  ge.add_face([4568.mm,1151.5.mm,26.mm], [4570.25.mm,1152.10288568297.mm,26.mm], [4569.25.mm,1153.834936490539.mm,29.mm], [4568.mm,1153.5.mm,29.mm])
  ge.add_face([4570.25.mm,1152.10288568297.mm,26.mm], [4571.89711431703.mm,1153.75.mm,26.mm], [4570.165063509461.mm,1154.75.mm,29.mm], [4569.25.mm,1153.834936490539.mm,29.mm])
  ge.add_face([4571.89711431703.mm,1153.75.mm,26.mm], [4572.5.mm,1156.mm,26.mm], [4570.5.mm,1156.mm,29.mm], [4570.165063509461.mm,1154.75.mm,29.mm])
  ge.add_face([4572.5.mm,1156.mm,26.mm], [4571.89711431703.mm,1158.25.mm,26.mm], [4570.25.mm,1159.89711431703.mm,26.mm], [4568.mm,1160.5.mm,26.mm], [4565.75.mm,1159.89711431703.mm,26.mm], [4564.10288568297.mm,1158.25.mm,26.mm], [4563.5.mm,1156.mm,26.mm], [4564.10288568297.mm,1153.75.mm,26.mm], [4565.75.mm,1152.10288568297.mm,26.mm], [4568.mm,1151.5.mm,26.mm], [4570.25.mm,1152.10288568297.mm,26.mm], [4571.89711431703.mm,1153.75.mm,26.mm])
  mat = model.materials["Clamp Bolt CSK Head R"] || model.materials.add("Clamp Bolt CSK Head R")
  mat.color = Sketchup::Color.new(128, 128, 138)
  grp.material = mat

  # Clamp Bolt R
  grp = ents.add_group
  grp.name = "Clamp Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4590.mm,1156.mm,26.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(35.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt CSK Head R
  grp = ents.add_group
  grp.name = "Clamp Bolt CSK Head R"
  ge = grp.entities
  ge.add_face([4594.5.mm,1156.mm,26.mm], [4593.89711431703.mm,1158.25.mm,26.mm], [4592.165063509461.mm,1157.25.mm,29.mm], [4592.5.mm,1156.mm,29.mm])
  ge.add_face([4593.89711431703.mm,1158.25.mm,26.mm], [4592.25.mm,1159.89711431703.mm,26.mm], [4591.25.mm,1158.165063509461.mm,29.mm], [4592.165063509461.mm,1157.25.mm,29.mm])
  ge.add_face([4592.25.mm,1159.89711431703.mm,26.mm], [4590.mm,1160.5.mm,26.mm], [4590.mm,1158.5.mm,29.mm], [4591.25.mm,1158.165063509461.mm,29.mm])
  ge.add_face([4590.mm,1160.5.mm,26.mm], [4587.75.mm,1159.89711431703.mm,26.mm], [4588.75.mm,1158.165063509461.mm,29.mm], [4590.mm,1158.5.mm,29.mm])
  ge.add_face([4587.75.mm,1159.89711431703.mm,26.mm], [4586.10288568297.mm,1158.25.mm,26.mm], [4587.834936490539.mm,1157.25.mm,29.mm], [4588.75.mm,1158.165063509461.mm,29.mm])
  ge.add_face([4586.10288568297.mm,1158.25.mm,26.mm], [4585.5.mm,1156.mm,26.mm], [4587.5.mm,1156.mm,29.mm], [4587.834936490539.mm,1157.25.mm,29.mm])
  ge.add_face([4585.5.mm,1156.mm,26.mm], [4586.10288568297.mm,1153.75.mm,26.mm], [4587.834936490539.mm,1154.75.mm,29.mm], [4587.5.mm,1156.mm,29.mm])
  ge.add_face([4586.10288568297.mm,1153.75.mm,26.mm], [4587.75.mm,1152.10288568297.mm,26.mm], [4588.75.mm,1153.834936490539.mm,29.mm], [4587.834936490539.mm,1154.75.mm,29.mm])
  ge.add_face([4587.75.mm,1152.10288568297.mm,26.mm], [4590.mm,1151.5.mm,26.mm], [4590.mm,1153.5.mm,29.mm], [4588.75.mm,1153.834936490539.mm,29.mm])
  ge.add_face([4590.mm,1151.5.mm,26.mm], [4592.25.mm,1152.10288568297.mm,26.mm], [4591.25.mm,1153.834936490539.mm,29.mm], [4590.mm,1153.5.mm,29.mm])
  ge.add_face([4592.25.mm,1152.10288568297.mm,26.mm], [4593.89711431703.mm,1153.75.mm,26.mm], [4592.165063509461.mm,1154.75.mm,29.mm], [4591.25.mm,1153.834936490539.mm,29.mm])
  ge.add_face([4593.89711431703.mm,1153.75.mm,26.mm], [4594.5.mm,1156.mm,26.mm], [4592.5.mm,1156.mm,29.mm], [4592.165063509461.mm,1154.75.mm,29.mm])
  ge.add_face([4594.5.mm,1156.mm,26.mm], [4593.89711431703.mm,1158.25.mm,26.mm], [4592.25.mm,1159.89711431703.mm,26.mm], [4590.mm,1160.5.mm,26.mm], [4587.75.mm,1159.89711431703.mm,26.mm], [4586.10288568297.mm,1158.25.mm,26.mm], [4585.5.mm,1156.mm,26.mm], [4586.10288568297.mm,1153.75.mm,26.mm], [4587.75.mm,1152.10288568297.mm,26.mm], [4590.mm,1151.5.mm,26.mm], [4592.25.mm,1152.10288568297.mm,26.mm], [4593.89711431703.mm,1153.75.mm,26.mm])
  mat = model.materials["Clamp Bolt CSK Head R"] || model.materials.add("Clamp Bolt CSK Head R")
  mat.color = Sketchup::Color.new(128, 128, 138)
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
  circle = ge.add_circle([4568.mm,1204.mm,26.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(35.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt CSK Head R
  grp = ents.add_group
  grp.name = "Clamp Bolt CSK Head R"
  ge = grp.entities
  ge.add_face([4572.5.mm,1204.mm,26.mm], [4571.89711431703.mm,1206.25.mm,26.mm], [4570.165063509461.mm,1205.25.mm,29.mm], [4570.5.mm,1204.mm,29.mm])
  ge.add_face([4571.89711431703.mm,1206.25.mm,26.mm], [4570.25.mm,1207.89711431703.mm,26.mm], [4569.25.mm,1206.165063509461.mm,29.mm], [4570.165063509461.mm,1205.25.mm,29.mm])
  ge.add_face([4570.25.mm,1207.89711431703.mm,26.mm], [4568.mm,1208.5.mm,26.mm], [4568.mm,1206.5.mm,29.mm], [4569.25.mm,1206.165063509461.mm,29.mm])
  ge.add_face([4568.mm,1208.5.mm,26.mm], [4565.75.mm,1207.89711431703.mm,26.mm], [4566.75.mm,1206.165063509461.mm,29.mm], [4568.mm,1206.5.mm,29.mm])
  ge.add_face([4565.75.mm,1207.89711431703.mm,26.mm], [4564.10288568297.mm,1206.25.mm,26.mm], [4565.834936490539.mm,1205.25.mm,29.mm], [4566.75.mm,1206.165063509461.mm,29.mm])
  ge.add_face([4564.10288568297.mm,1206.25.mm,26.mm], [4563.5.mm,1204.mm,26.mm], [4565.5.mm,1204.mm,29.mm], [4565.834936490539.mm,1205.25.mm,29.mm])
  ge.add_face([4563.5.mm,1204.mm,26.mm], [4564.10288568297.mm,1201.75.mm,26.mm], [4565.834936490539.mm,1202.75.mm,29.mm], [4565.5.mm,1204.mm,29.mm])
  ge.add_face([4564.10288568297.mm,1201.75.mm,26.mm], [4565.75.mm,1200.10288568297.mm,26.mm], [4566.75.mm,1201.834936490539.mm,29.mm], [4565.834936490539.mm,1202.75.mm,29.mm])
  ge.add_face([4565.75.mm,1200.10288568297.mm,26.mm], [4568.mm,1199.5.mm,26.mm], [4568.mm,1201.5.mm,29.mm], [4566.75.mm,1201.834936490539.mm,29.mm])
  ge.add_face([4568.mm,1199.5.mm,26.mm], [4570.25.mm,1200.10288568297.mm,26.mm], [4569.25.mm,1201.834936490539.mm,29.mm], [4568.mm,1201.5.mm,29.mm])
  ge.add_face([4570.25.mm,1200.10288568297.mm,26.mm], [4571.89711431703.mm,1201.75.mm,26.mm], [4570.165063509461.mm,1202.75.mm,29.mm], [4569.25.mm,1201.834936490539.mm,29.mm])
  ge.add_face([4571.89711431703.mm,1201.75.mm,26.mm], [4572.5.mm,1204.mm,26.mm], [4570.5.mm,1204.mm,29.mm], [4570.165063509461.mm,1202.75.mm,29.mm])
  ge.add_face([4572.5.mm,1204.mm,26.mm], [4571.89711431703.mm,1206.25.mm,26.mm], [4570.25.mm,1207.89711431703.mm,26.mm], [4568.mm,1208.5.mm,26.mm], [4565.75.mm,1207.89711431703.mm,26.mm], [4564.10288568297.mm,1206.25.mm,26.mm], [4563.5.mm,1204.mm,26.mm], [4564.10288568297.mm,1201.75.mm,26.mm], [4565.75.mm,1200.10288568297.mm,26.mm], [4568.mm,1199.5.mm,26.mm], [4570.25.mm,1200.10288568297.mm,26.mm], [4571.89711431703.mm,1201.75.mm,26.mm])
  mat = model.materials["Clamp Bolt CSK Head R"] || model.materials.add("Clamp Bolt CSK Head R")
  mat.color = Sketchup::Color.new(128, 128, 138)
  grp.material = mat

  # Clamp Bolt R
  grp = ents.add_group
  grp.name = "Clamp Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4590.mm,1204.mm,26.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(35.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt CSK Head R
  grp = ents.add_group
  grp.name = "Clamp Bolt CSK Head R"
  ge = grp.entities
  ge.add_face([4594.5.mm,1204.mm,26.mm], [4593.89711431703.mm,1206.25.mm,26.mm], [4592.165063509461.mm,1205.25.mm,29.mm], [4592.5.mm,1204.mm,29.mm])
  ge.add_face([4593.89711431703.mm,1206.25.mm,26.mm], [4592.25.mm,1207.89711431703.mm,26.mm], [4591.25.mm,1206.165063509461.mm,29.mm], [4592.165063509461.mm,1205.25.mm,29.mm])
  ge.add_face([4592.25.mm,1207.89711431703.mm,26.mm], [4590.mm,1208.5.mm,26.mm], [4590.mm,1206.5.mm,29.mm], [4591.25.mm,1206.165063509461.mm,29.mm])
  ge.add_face([4590.mm,1208.5.mm,26.mm], [4587.75.mm,1207.89711431703.mm,26.mm], [4588.75.mm,1206.165063509461.mm,29.mm], [4590.mm,1206.5.mm,29.mm])
  ge.add_face([4587.75.mm,1207.89711431703.mm,26.mm], [4586.10288568297.mm,1206.25.mm,26.mm], [4587.834936490539.mm,1205.25.mm,29.mm], [4588.75.mm,1206.165063509461.mm,29.mm])
  ge.add_face([4586.10288568297.mm,1206.25.mm,26.mm], [4585.5.mm,1204.mm,26.mm], [4587.5.mm,1204.mm,29.mm], [4587.834936490539.mm,1205.25.mm,29.mm])
  ge.add_face([4585.5.mm,1204.mm,26.mm], [4586.10288568297.mm,1201.75.mm,26.mm], [4587.834936490539.mm,1202.75.mm,29.mm], [4587.5.mm,1204.mm,29.mm])
  ge.add_face([4586.10288568297.mm,1201.75.mm,26.mm], [4587.75.mm,1200.10288568297.mm,26.mm], [4588.75.mm,1201.834936490539.mm,29.mm], [4587.834936490539.mm,1202.75.mm,29.mm])
  ge.add_face([4587.75.mm,1200.10288568297.mm,26.mm], [4590.mm,1199.5.mm,26.mm], [4590.mm,1201.5.mm,29.mm], [4588.75.mm,1201.834936490539.mm,29.mm])
  ge.add_face([4590.mm,1199.5.mm,26.mm], [4592.25.mm,1200.10288568297.mm,26.mm], [4591.25.mm,1201.834936490539.mm,29.mm], [4590.mm,1201.5.mm,29.mm])
  ge.add_face([4592.25.mm,1200.10288568297.mm,26.mm], [4593.89711431703.mm,1201.75.mm,26.mm], [4592.165063509461.mm,1202.75.mm,29.mm], [4591.25.mm,1201.834936490539.mm,29.mm])
  ge.add_face([4593.89711431703.mm,1201.75.mm,26.mm], [4594.5.mm,1204.mm,26.mm], [4592.5.mm,1204.mm,29.mm], [4592.165063509461.mm,1202.75.mm,29.mm])
  ge.add_face([4594.5.mm,1204.mm,26.mm], [4593.89711431703.mm,1206.25.mm,26.mm], [4592.25.mm,1207.89711431703.mm,26.mm], [4590.mm,1208.5.mm,26.mm], [4587.75.mm,1207.89711431703.mm,26.mm], [4586.10288568297.mm,1206.25.mm,26.mm], [4585.5.mm,1204.mm,26.mm], [4586.10288568297.mm,1201.75.mm,26.mm], [4587.75.mm,1200.10288568297.mm,26.mm], [4590.mm,1199.5.mm,26.mm], [4592.25.mm,1200.10288568297.mm,26.mm], [4593.89711431703.mm,1201.75.mm,26.mm])
  mat = model.materials["Clamp Bolt CSK Head R"] || model.materials.add("Clamp Bolt CSK Head R")
  mat.color = Sketchup::Color.new(128, 128, 138)
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
  vec = Geom::Vector3d.new(0.mm, -246.mm, 592.5.mm)
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
  vec = Geom::Vector3d.new(0.mm, -270.mm, 612.5.mm)
  circle = ge.add_circle([2399.5.mm,910.mm,687.5.mm], vec, 11.mm, 16)
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
  circle = ge.add_circle([2309.5.mm,640.mm,1300.mm], [1,0,0], 9.mm, 24)
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
  vec = Geom::Vector3d.new(0.mm, 270.mm, -612.5.mm)
  circle = ge.add_circle([2419.5.mm,640.mm,1300.mm], vec, 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 246.mm, -592.5.mm)
  circle = ge.add_circle([2419.5.mm,910.mm,687.5.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.1666666666667425.mm, 0.mm)
  circle = ge.add_circle([2419.5.mm,1156.mm,95.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.166666666666515.mm, 0.mm)
  circle = ge.add_circle([2419.5.mm,1161.1666666666667.mm,95.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.1666666666667425.mm, 0.mm)
  circle = ge.add_circle([2419.5.mm,1166.3333333333333.mm,95.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.1666666666667425.mm, 0.mm)
  circle = ge.add_circle([2419.5.mm,1171.5.mm,95.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.166666666666515.mm, 0.mm)
  circle = ge.add_circle([2419.5.mm,1176.6666666666667.mm,95.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.1666666666667425.mm, 0.mm)
  circle = ge.add_circle([2419.5.mm,1181.8333333333333.mm,95.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.1666666666667425.mm, 0.mm)
  circle = ge.add_circle([2419.5.mm,1187.mm,95.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.166666666666515.mm, 0.mm)
  circle = ge.add_circle([2419.5.mm,1192.1666666666667.mm,95.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.1666666666667425.mm, 0.mm)
  circle = ge.add_circle([2419.5.mm,1197.3333333333333.mm,95.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector elbow
  grp = ents.add_group
  grp.name = "Feed Flex Connector elbow"
  ge = grp.entities
  arc = ge.add_arc([2419.5.mm,1202.5.mm,85.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 10.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2419.5.mm,1202.5.mm,95.mm], [0.000000,1.000000,0.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1.9625000000000057.mm)
  circle = ge.add_circle([2419.5.mm,1212.5.mm,85.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1.9624999999999915.mm)
  circle = ge.add_circle([2419.5.mm,1212.5.mm,83.0375.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1.9625000000000057.mm)
  circle = ge.add_circle([2419.5.mm,1212.5.mm,81.075.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1.9624999999999915.mm)
  circle = ge.add_circle([2419.5.mm,1212.5.mm,79.1125.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1.9625000000000057.mm)
  circle = ge.add_circle([2419.5.mm,1212.5.mm,77.15.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1.9625000000000057.mm)
  circle = ge.add_circle([2419.5.mm,1212.5.mm,75.1875.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1.9624999999999915.mm)
  circle = ge.add_circle([2419.5.mm,1212.5.mm,73.225.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1.9625000000000057.mm)
  circle = ge.add_circle([2419.5.mm,1212.5.mm,71.2625.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector elbow
  grp = ents.add_group
  grp.name = "Feed Flex Connector elbow"
  ge = grp.entities
  arc = ge.add_arc([2409.7.mm,1212.5.mm,69.3.mm], [1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 9.800000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2419.5.mm,1212.5.mm,69.3.mm], [0.000000,0.000000,-1.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.275000000000091.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2409.7.mm,1212.5.mm,59.5.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.275000000000091.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2408.4249999999997.mm,1212.5.mm,59.5.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.2749999999996362.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2407.1499999999996.mm,1212.5.mm,59.5.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.275000000000091.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2405.875.mm,1212.5.mm,59.5.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.275000000000091.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2404.6.mm,1212.5.mm,59.5.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.2749999999996362.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2403.325.mm,1212.5.mm,59.5.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.275000000000091.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2402.05.mm,1212.5.mm,59.5.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.275000000000091.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2400.775.mm,1212.5.mm,59.5.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -8.87447055288169.mm, -3.912011509025433.mm)
  circle = ge.add_circle([2430.5.mm,685.mm,1197.9166666666667.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, -5.4847244338408245.mm, -2.4177560769583124.mm)
  circle = ge.add_circle([2426.107390870624.mm,676.1255294471183.mm,1194.0046551576413.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
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
  circle = ge.add_circle([2414.607390870624.mm,670.6408050132775.mm,1191.586899080683.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, 5.4847244338408245.mm, 2.4177560769583124.mm)
  circle = ge.add_circle([2400.392609129376.mm,670.6408050132775.mm,1191.586899080683.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 8.87447055288169.mm, 3.912011509025433.mm)
  circle = ge.add_circle([2388.892609129376.mm,676.1255294471183.mm,1194.0046551576413.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, 8.87447055288169.mm, 3.912011509025433.mm)
  circle = ge.add_circle([2384.5.mm,685.mm,1197.9166666666667.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, 5.4847244338408245.mm, 2.4177560769583124.mm)
  circle = ge.add_circle([2388.892609129376.mm,693.8744705528817.mm,1201.8286781756922.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
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
  circle = ge.add_circle([2400.392609129376.mm,699.3591949867225.mm,1204.2464342526505.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, -5.4847244338408245.mm, -2.4177560769583124.mm)
  circle = ge.add_circle([2414.607390870624.mm,699.3591949867225.mm,1204.2464342526505.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, -8.87447055288169.mm, -3.912011509025433.mm)
  circle = ge.add_circle([2426.107390870624.mm,693.8744705528817.mm,1201.8286781756922.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -8.87447055288169.mm, -3.9120115090253194.mm)
  circle = ge.add_circle([2430.5.mm,775.mm,993.75.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, -5.4847244338408245.mm, -2.41775607695854.mm)
  circle = ge.add_circle([2426.107390870624.mm,766.1255294471183.mm,989.8379884909747.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
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
  circle = ge.add_circle([2414.607390870624.mm,760.6408050132775.mm,987.4202324140161.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, 5.4847244338408245.mm, 2.41775607695854.mm)
  circle = ge.add_circle([2400.392609129376.mm,760.6408050132775.mm,987.4202324140161.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 8.87447055288169.mm, 3.9120115090253194.mm)
  circle = ge.add_circle([2388.892609129376.mm,766.1255294471183.mm,989.8379884909747.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, 8.87447055288169.mm, 3.9120115090253194.mm)
  circle = ge.add_circle([2384.5.mm,775.mm,993.75.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, 5.4847244338408245.mm, 2.41775607695854.mm)
  circle = ge.add_circle([2388.892609129376.mm,783.8744705528817.mm,997.6620115090253.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
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
  circle = ge.add_circle([2400.392609129376.mm,789.3591949867225.mm,1000.0797675859839.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, -5.4847244338408245.mm, -2.41775607695854.mm)
  circle = ge.add_circle([2414.607390870624.mm,789.3591949867225.mm,1000.0797675859839.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, -8.87447055288169.mm, -3.9120115090253194.mm)
  circle = ge.add_circle([2426.107390870624.mm,783.8744705528817.mm,997.6620115090253.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -8.87447055288169.mm, -3.9120115090253194.mm)
  circle = ge.add_circle([2430.5.mm,865.mm,789.5833333333333.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, -5.4847244338408245.mm, -2.41775607695854.mm)
  circle = ge.add_circle([2426.107390870624.mm,856.1255294471183.mm,785.6713218243079.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
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
  circle = ge.add_circle([2414.607390870624.mm,850.6408050132775.mm,783.2535657473494.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, 5.4847244338408245.mm, 2.41775607695854.mm)
  circle = ge.add_circle([2400.392609129376.mm,850.6408050132775.mm,783.2535657473494.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 8.87447055288169.mm, 3.9120115090253194.mm)
  circle = ge.add_circle([2388.892609129376.mm,856.1255294471183.mm,785.6713218243079.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, 8.87447055288169.mm, 3.9120115090253194.mm)
  circle = ge.add_circle([2384.5.mm,865.mm,789.5833333333333.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, 5.4847244338408245.mm, 2.41775607695854.mm)
  circle = ge.add_circle([2388.892609129376.mm,873.8744705528817.mm,793.4953448423586.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
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
  circle = ge.add_circle([2400.392609129376.mm,879.3591949867225.mm,795.9131009193171.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, -5.4847244338408245.mm, -2.41775607695854.mm)
  circle = ge.add_circle([2414.607390870624.mm,879.3591949867225.mm,795.9131009193171.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, -8.87447055288169.mm, -3.9120115090253194.mm)
  circle = ge.add_circle([2426.107390870624.mm,873.8744705528817.mm,793.4953448423586.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -8.957110700421481.mm, -3.718901657896481.mm)
  circle = ge.add_circle([2430.5.mm,951.mm,588.75.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, -5.535798853855795.mm, -2.298407625398454.mm)
  circle = ge.add_circle([2426.107390870624.mm,942.0428892995785.mm,585.0310983421035.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
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
  circle = ge.add_circle([2414.607390870624.mm,936.5070904457227.mm,582.7326907167051.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, 5.535798853855795.mm, 2.298407625398454.mm)
  circle = ge.add_circle([2400.392609129376.mm,936.5070904457227.mm,582.7326907167051.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 8.957110700421481.mm, 3.718901657896481.mm)
  circle = ge.add_circle([2388.892609129376.mm,942.0428892995785.mm,585.0310983421035.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, 8.957110700421481.mm, 3.718901657896481.mm)
  circle = ge.add_circle([2384.5.mm,951.mm,588.75.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, 5.535798853855795.mm, 2.298407625398454.mm)
  circle = ge.add_circle([2388.892609129376.mm,959.9571107004215.mm,592.4689016578965.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
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
  circle = ge.add_circle([2400.392609129376.mm,965.4929095542773.mm,594.7673092832949.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, -5.535798853855795.mm, -2.298407625398454.mm)
  circle = ge.add_circle([2414.607390870624.mm,965.4929095542773.mm,594.7673092832949.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, -8.957110700421481.mm, -3.718901657896481.mm)
  circle = ge.add_circle([2426.107390870624.mm,959.9571107004215.mm,592.4689016578965.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -8.957110700421481.mm, -3.718901657896538.mm)
  circle = ge.add_circle([2430.5.mm,1033.mm,391.25.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, -5.535798853855795.mm, -2.2984076253983403.mm)
  circle = ge.add_circle([2426.107390870624.mm,1024.0428892995785.mm,387.53109834210346.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
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
  circle = ge.add_circle([2414.607390870624.mm,1018.5070904457227.mm,385.2326907167051.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, 5.535798853855795.mm, 2.2984076253983403.mm)
  circle = ge.add_circle([2400.392609129376.mm,1018.5070904457227.mm,385.2326907167051.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 8.957110700421481.mm, 3.718901657896538.mm)
  circle = ge.add_circle([2388.892609129376.mm,1024.0428892995785.mm,387.53109834210346.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, 8.957110700421481.mm, 3.718901657896538.mm)
  circle = ge.add_circle([2384.5.mm,1033.mm,391.25.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, 5.535798853855795.mm, 2.2984076253983403.mm)
  circle = ge.add_circle([2388.892609129376.mm,1041.9571107004215.mm,394.96890165789654.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
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
  circle = ge.add_circle([2400.392609129376.mm,1047.4929095542773.mm,397.2673092832949.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, -5.535798853855795.mm, -2.2984076253983403.mm)
  circle = ge.add_circle([2414.607390870624.mm,1047.4929095542773.mm,397.2673092832949.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, -8.957110700421481.mm, -3.718901657896538.mm)
  circle = ge.add_circle([2426.107390870624.mm,1041.9571107004215.mm,394.96890165789654.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -8.957110700421481.mm, -3.7189016578965095.mm)
  circle = ge.add_circle([2430.5.mm,1115.mm,193.75.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, -5.535798853855795.mm, -2.2984076253983687.mm)
  circle = ge.add_circle([2426.107390870624.mm,1106.0428892995785.mm,190.0310983421035.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
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
  circle = ge.add_circle([2414.607390870624.mm,1100.5070904457227.mm,187.73269071670512.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, 5.535798853855795.mm, 2.2984076253983687.mm)
  circle = ge.add_circle([2400.392609129376.mm,1100.5070904457227.mm,187.73269071670512.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 8.957110700421481.mm, 3.7189016578965095.mm)
  circle = ge.add_circle([2388.892609129376.mm,1106.0428892995785.mm,190.0310983421035.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, 8.957110700421481.mm, 3.7189016578965095.mm)
  circle = ge.add_circle([2384.5.mm,1115.mm,193.75.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, 5.535798853855795.mm, 2.2984076253983687.mm)
  circle = ge.add_circle([2388.892609129376.mm,1123.9571107004215.mm,197.4689016578965.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
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
  circle = ge.add_circle([2400.392609129376.mm,1129.4929095542773.mm,199.76730928329488.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, -5.535798853855795.mm, -2.2984076253983687.mm)
  circle = ge.add_circle([2414.607390870624.mm,1129.4929095542773.mm,199.76730928329488.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, -8.957110700421481.mm, -3.7189016578965095.mm)
  circle = ge.add_circle([2426.107390870624.mm,1123.9571107004215.mm,197.4689016578965.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Center Feed Barb Tee
  grp = ents.add_group
  grp.name = "Center Feed Barb Tee"
  ge = grp.entities
  circle = ge.add_circle([2399.5.mm,1212.5.mm,39.5.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(18.mm)
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
  mat.color = Sketchup::Color.new(216, 208, 188)
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
  face = grp.entities.add_face([4471.mm,80.mm,0.mm], [4629.mm,80.mm,0.mm], [4629.mm,180.mm,0.mm], [4471.mm,180.mm,0.mm])
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
(39 90-deg down-jets @ 100mm)", anc, Geom::Vector3d.new(250.mm, -950.mm, 380.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(2399.mm, 1180.mm, 90.mm)
txt = entities.add_text("FEED POLE + BALL JOINT", anc, Geom::Vector3d.new(700.mm, -250.mm, 800.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(2399.mm, 1200.mm, 70.mm)
txt = entities.add_text("CENTER FEED
(single inlet tee)", anc, Geom::Vector3d.new(-600.mm, -700.mm, 650.mm))
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

[["Overview", ["Beam", "Carriage L", "Carriage R", "Feed & Pole", "Tray"], nil], ["Beam", ["Beam"], nil], ["Carriage Assembly", ["Beam", "Carriage L", "Carriage R", "Tray Ref"], nil], ["One Carriage", ["Carriage L"], [200.mm, 1180.mm, 55.mm, 480.mm]], ["Pole & Ball Joint", ["Beam", "Feed & Pole"], nil], ["Processing Tray", ["Tray", "Beam", "Carriage L", "Carriage R"], nil], ["Labeled", ["Beam", "Carriage L", "Carriage R", "Feed & Pole", "Tray", "Labels"], nil]].each { |name, tags, tgt|
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
