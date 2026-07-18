# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/ — do not edit this .rb directly.
model = Sketchup.active_model
model.start_operation("TBS-001 Light Trap (dynamic swing)", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# Idempotent rebuild: erase ALL prior instances.
to_erase = entities.to_a.select { |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text)
}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each { |p| model.pages.erase(p) }

# ── Sketchfab metadata — fill-only-if-blank; never overwrites existing values ──
model.name = "TBS-001 Lighttrap Model" if model.name.to_s.strip.empty?
model.description = "Personnel access during operation is via a revolving light trap drum built into the panel. Operators can enter or exit at any time without opening the full panel or admitting daylight \u2014 for example, between coating of the photosensitive material, or while the exposure is being made." if model.description.to_s.strip.empty?
model.set_attribute("sketchfab", "model_title", "TBS-001 Lighttrap Model") if model.get_attribute("sketchfab", "model_title").to_s.strip.empty?
model.set_attribute("sketchfab", "model_description", "Personnel access during operation is via a revolving light trap drum built into the panel. Operators can enter or exit at any time without opening the full panel or admitting daylight \u2014 for example, between coating of the photosensitive material, or while the exposure is being made.") if model.get_attribute("sketchfab", "model_description").to_s.strip.empty?
model.set_attribute("sketchfab", "model_id", "a4f73191b8bb4d17a6e764585ca695be") if model.get_attribute("sketchfab", "model_id").to_s.strip.empty?
model.set_attribute("sketchfab", "model_tags", "sketchup") if model.get_attribute("sketchfab", "model_tags").to_s.strip.empty?

# ── Tags (layers) ──
  model.layers.add("Context") unless model.layers["Context"]
  model.layers.add("Door Frame") unless model.layers["Door Frame"]
  model.layers.add("Pivot Axle") unless model.layers["Pivot Axle"]
  model.layers.add("Processing Tray") unless model.layers["Processing Tray"]
  model.layers.add("Walkways") unless model.layers["Walkways"]
  model.layers.add("Film Plane Rails") unless model.layers["Film Plane Rails"]
  model.layers.add("Near Leaf") unless model.layers["Near Leaf"]
  model.layers.add("Far Leaf") unless model.layers["Far Leaf"]
  model.layers.add("Lock anchor") unless model.layers["Lock anchor"]
  model.layers.add("Panel skin") unless model.layers["Panel skin"]
  model.layers.add("Panel Swing") unless model.layers["Panel Swing"]
  model.layers.add("Fan B") unless model.layers["Fan B"]
  model.layers.add("Drum shell") unless model.layers["Drum shell"]
  model.layers.add("Cargo Doors") unless model.layers["Cargo Doors"]
  model.layers.add("Fan B Cable") unless model.layers["Fan B Cable"]
  model.layers.add("Labels") unless model.layers["Labels"]

# ── Fixed subsystems ──
  # ═══ Context ═══
  defn = model.definitions.add("Context")
  ents = defn.entities
  # Floor (context)
  grp = ents.add_group
  grp.name = "Floor (context)"
  face = grp.entities.add_face([0.mm,0.mm,-40.mm], [2000.mm,0.mm,-40.mm], [2000.mm,2362.mm,-40.mm], [0.mm,2362.mm,-40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Floor (context)"] || model.materials.add("Floor (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.25
  grp.material = mat

  # Ceiling (context)
  grp = ents.add_group
  grp.name = "Ceiling (context)"
  face = grp.entities.add_face([0.mm,0.mm,2388.mm], [2000.mm,0.mm,2388.mm], [2000.mm,2362.mm,2388.mm], [0.mm,2362.mm,2388.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Ceiling (context)"] || model.materials.add("Ceiling (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.1
  grp.material = mat

  # Side Wall near (context)
  grp = ents.add_group
  grp.name = "Side Wall near (context)"
  face = grp.entities.add_face([0.mm,-40.mm,0.mm], [2000.mm,-40.mm,0.mm], [2000.mm,0.mm,0.mm], [0.mm,0.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Side Wall near (context)"] || model.materials.add("Side Wall near (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.16
  grp.material = mat

  # Side Wall far (context)
  grp = ents.add_group
  grp.name = "Side Wall far (context)"
  face = grp.entities.add_face([0.mm,2362.mm,0.mm], [2000.mm,2362.mm,0.mm], [2000.mm,2402.mm,0.mm], [0.mm,2402.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Side Wall near (context)"] || model.materials.add("Side Wall near (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.16
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Context"
  inst.layer = model.layers["Context"]

  # ═══ Fixed Door Frame ═══
  defn = model.definitions.add("Fixed Door Frame")
  ents = defn.entities
  # Door Frame threshold
  grp = ents.add_group
  grp.name = "Door Frame threshold"
  face = grp.entities.add_face([-50.mm,0.mm,0.mm], [0.mm,0.mm,0.mm], [0.mm,2362.mm,0.mm], [-50.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Door Frame threshold"] || model.materials.add("Door Frame threshold")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame top
  grp = ents.add_group
  grp.name = "Door Frame top"
  face = grp.entities.add_face([-50.mm,0.mm,2338.mm], [0.mm,0.mm,2338.mm], [0.mm,2362.mm,2338.mm], [-50.mm,2362.mm,2338.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Door Frame threshold"] || model.materials.add("Door Frame threshold")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame left stile
  grp = ents.add_group
  grp.name = "Door Frame left stile"
  face = grp.entities.add_face([-50.mm,0.mm,0.mm], [0.mm,0.mm,0.mm], [0.mm,50.mm,0.mm], [-50.mm,50.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Door Frame threshold"] || model.materials.add("Door Frame threshold")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame right stile
  grp = ents.add_group
  grp.name = "Door Frame right stile"
  face = grp.entities.add_face([-50.mm,2312.mm,0.mm], [0.mm,2312.mm,0.mm], [0.mm,2362.mm,0.mm], [-50.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Door Frame threshold"] || model.materials.add("Door Frame threshold")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame bottom brush seal
  grp = ents.add_group
  grp.name = "Door Frame bottom brush seal"
  face = grp.entities.add_face([-32.mm,0.mm,0.mm], [-20.mm,0.mm,0.mm], [-20.mm,2362.mm,0.mm], [-32.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(110.mm)
  mat = model.materials["Door Frame bottom brush seal"] || model.materials.add("Door Frame bottom brush seal")
  mat.color = Sketchup::Color.new(47, 168, 79)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,6.7102272727272725.mm,40.mm], [-31.mm,6.7102272727272725.mm,40.mm], [-31.mm,8.710227272727273.mm,40.mm], [-33.mm,8.710227272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,6.7102272727272725.mm,40.mm], [-19.mm,6.7102272727272725.mm,40.mm], [-19.mm,8.710227272727273.mm,40.mm], [-21.mm,8.710227272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,20.130681818181817.mm,40.mm], [-31.mm,20.130681818181817.mm,40.mm], [-31.mm,22.130681818181817.mm,40.mm], [-33.mm,22.130681818181817.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,20.130681818181817.mm,40.mm], [-19.mm,20.130681818181817.mm,40.mm], [-19.mm,22.130681818181817.mm,40.mm], [-21.mm,22.130681818181817.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,33.55113636363636.mm,40.mm], [-31.mm,33.55113636363636.mm,40.mm], [-31.mm,35.55113636363636.mm,40.mm], [-33.mm,35.55113636363636.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,33.55113636363636.mm,40.mm], [-19.mm,33.55113636363636.mm,40.mm], [-19.mm,35.55113636363636.mm,40.mm], [-21.mm,35.55113636363636.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,46.97159090909091.mm,40.mm], [-31.mm,46.97159090909091.mm,40.mm], [-31.mm,48.97159090909091.mm,40.mm], [-33.mm,48.97159090909091.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,46.97159090909091.mm,40.mm], [-19.mm,46.97159090909091.mm,40.mm], [-19.mm,48.97159090909091.mm,40.mm], [-21.mm,48.97159090909091.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,60.39204545454545.mm,40.mm], [-31.mm,60.39204545454545.mm,40.mm], [-31.mm,62.39204545454545.mm,40.mm], [-33.mm,62.39204545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,60.39204545454545.mm,40.mm], [-19.mm,60.39204545454545.mm,40.mm], [-19.mm,62.39204545454545.mm,40.mm], [-21.mm,62.39204545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,73.8125.mm,40.mm], [-31.mm,73.8125.mm,40.mm], [-31.mm,75.8125.mm,40.mm], [-33.mm,75.8125.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,73.8125.mm,40.mm], [-19.mm,73.8125.mm,40.mm], [-19.mm,75.8125.mm,40.mm], [-21.mm,75.8125.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,87.23295454545455.mm,40.mm], [-31.mm,87.23295454545455.mm,40.mm], [-31.mm,89.23295454545455.mm,40.mm], [-33.mm,89.23295454545455.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,87.23295454545455.mm,40.mm], [-19.mm,87.23295454545455.mm,40.mm], [-19.mm,89.23295454545455.mm,40.mm], [-21.mm,89.23295454545455.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,100.6534090909091.mm,40.mm], [-31.mm,100.6534090909091.mm,40.mm], [-31.mm,102.6534090909091.mm,40.mm], [-33.mm,102.6534090909091.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,100.6534090909091.mm,40.mm], [-19.mm,100.6534090909091.mm,40.mm], [-19.mm,102.6534090909091.mm,40.mm], [-21.mm,102.6534090909091.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,114.07386363636363.mm,40.mm], [-31.mm,114.07386363636363.mm,40.mm], [-31.mm,116.07386363636363.mm,40.mm], [-33.mm,116.07386363636363.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,114.07386363636363.mm,40.mm], [-19.mm,114.07386363636363.mm,40.mm], [-19.mm,116.07386363636363.mm,40.mm], [-21.mm,116.07386363636363.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,127.49431818181817.mm,40.mm], [-31.mm,127.49431818181817.mm,40.mm], [-31.mm,129.4943181818182.mm,40.mm], [-33.mm,129.4943181818182.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,127.49431818181817.mm,40.mm], [-19.mm,127.49431818181817.mm,40.mm], [-19.mm,129.4943181818182.mm,40.mm], [-21.mm,129.4943181818182.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,140.91477272727272.mm,40.mm], [-31.mm,140.91477272727272.mm,40.mm], [-31.mm,142.91477272727272.mm,40.mm], [-33.mm,142.91477272727272.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,140.91477272727272.mm,40.mm], [-19.mm,140.91477272727272.mm,40.mm], [-19.mm,142.91477272727272.mm,40.mm], [-21.mm,142.91477272727272.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,154.33522727272728.mm,40.mm], [-31.mm,154.33522727272728.mm,40.mm], [-31.mm,156.33522727272728.mm,40.mm], [-33.mm,156.33522727272728.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,154.33522727272728.mm,40.mm], [-19.mm,154.33522727272728.mm,40.mm], [-19.mm,156.33522727272728.mm,40.mm], [-21.mm,156.33522727272728.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,167.7556818181818.mm,40.mm], [-31.mm,167.7556818181818.mm,40.mm], [-31.mm,169.7556818181818.mm,40.mm], [-33.mm,169.7556818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,167.7556818181818.mm,40.mm], [-19.mm,167.7556818181818.mm,40.mm], [-19.mm,169.7556818181818.mm,40.mm], [-21.mm,169.7556818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,181.17613636363635.mm,40.mm], [-31.mm,181.17613636363635.mm,40.mm], [-31.mm,183.17613636363635.mm,40.mm], [-33.mm,183.17613636363635.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,181.17613636363635.mm,40.mm], [-19.mm,181.17613636363635.mm,40.mm], [-19.mm,183.17613636363635.mm,40.mm], [-21.mm,183.17613636363635.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,194.5965909090909.mm,40.mm], [-31.mm,194.5965909090909.mm,40.mm], [-31.mm,196.5965909090909.mm,40.mm], [-33.mm,196.5965909090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,194.5965909090909.mm,40.mm], [-19.mm,194.5965909090909.mm,40.mm], [-19.mm,196.5965909090909.mm,40.mm], [-21.mm,196.5965909090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,208.01704545454544.mm,40.mm], [-31.mm,208.01704545454544.mm,40.mm], [-31.mm,210.01704545454544.mm,40.mm], [-33.mm,210.01704545454544.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,208.01704545454544.mm,40.mm], [-19.mm,208.01704545454544.mm,40.mm], [-19.mm,210.01704545454544.mm,40.mm], [-21.mm,210.01704545454544.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,221.4375.mm,40.mm], [-31.mm,221.4375.mm,40.mm], [-31.mm,223.4375.mm,40.mm], [-33.mm,223.4375.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,221.4375.mm,40.mm], [-19.mm,221.4375.mm,40.mm], [-19.mm,223.4375.mm,40.mm], [-21.mm,223.4375.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,234.85795454545453.mm,40.mm], [-31.mm,234.85795454545453.mm,40.mm], [-31.mm,236.85795454545453.mm,40.mm], [-33.mm,236.85795454545453.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,234.85795454545453.mm,40.mm], [-19.mm,234.85795454545453.mm,40.mm], [-19.mm,236.85795454545453.mm,40.mm], [-21.mm,236.85795454545453.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,248.2784090909091.mm,40.mm], [-31.mm,248.2784090909091.mm,40.mm], [-31.mm,250.2784090909091.mm,40.mm], [-33.mm,250.2784090909091.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,248.2784090909091.mm,40.mm], [-19.mm,248.2784090909091.mm,40.mm], [-19.mm,250.2784090909091.mm,40.mm], [-21.mm,250.2784090909091.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,261.6988636363636.mm,40.mm], [-31.mm,261.6988636363636.mm,40.mm], [-31.mm,263.6988636363636.mm,40.mm], [-33.mm,263.6988636363636.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,261.6988636363636.mm,40.mm], [-19.mm,261.6988636363636.mm,40.mm], [-19.mm,263.6988636363636.mm,40.mm], [-21.mm,263.6988636363636.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,275.1193181818182.mm,40.mm], [-31.mm,275.1193181818182.mm,40.mm], [-31.mm,277.1193181818182.mm,40.mm], [-33.mm,277.1193181818182.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,275.1193181818182.mm,40.mm], [-19.mm,275.1193181818182.mm,40.mm], [-19.mm,277.1193181818182.mm,40.mm], [-21.mm,277.1193181818182.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,288.5397727272727.mm,40.mm], [-31.mm,288.5397727272727.mm,40.mm], [-31.mm,290.5397727272727.mm,40.mm], [-33.mm,290.5397727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,288.5397727272727.mm,40.mm], [-19.mm,288.5397727272727.mm,40.mm], [-19.mm,290.5397727272727.mm,40.mm], [-21.mm,290.5397727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,301.96022727272725.mm,40.mm], [-31.mm,301.96022727272725.mm,40.mm], [-31.mm,303.96022727272725.mm,40.mm], [-33.mm,303.96022727272725.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,301.96022727272725.mm,40.mm], [-19.mm,301.96022727272725.mm,40.mm], [-19.mm,303.96022727272725.mm,40.mm], [-21.mm,303.96022727272725.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,315.3806818181818.mm,40.mm], [-31.mm,315.3806818181818.mm,40.mm], [-31.mm,317.3806818181818.mm,40.mm], [-33.mm,317.3806818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,315.3806818181818.mm,40.mm], [-19.mm,315.3806818181818.mm,40.mm], [-19.mm,317.3806818181818.mm,40.mm], [-21.mm,317.3806818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,328.8011363636364.mm,40.mm], [-31.mm,328.8011363636364.mm,40.mm], [-31.mm,330.8011363636364.mm,40.mm], [-33.mm,330.8011363636364.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,328.8011363636364.mm,40.mm], [-19.mm,328.8011363636364.mm,40.mm], [-19.mm,330.8011363636364.mm,40.mm], [-21.mm,330.8011363636364.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,342.2215909090909.mm,40.mm], [-31.mm,342.2215909090909.mm,40.mm], [-31.mm,344.2215909090909.mm,40.mm], [-33.mm,344.2215909090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,342.2215909090909.mm,40.mm], [-19.mm,342.2215909090909.mm,40.mm], [-19.mm,344.2215909090909.mm,40.mm], [-21.mm,344.2215909090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,355.64204545454544.mm,40.mm], [-31.mm,355.64204545454544.mm,40.mm], [-31.mm,357.64204545454544.mm,40.mm], [-33.mm,357.64204545454544.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,355.64204545454544.mm,40.mm], [-19.mm,355.64204545454544.mm,40.mm], [-19.mm,357.64204545454544.mm,40.mm], [-21.mm,357.64204545454544.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,369.0625.mm,40.mm], [-31.mm,369.0625.mm,40.mm], [-31.mm,371.0625.mm,40.mm], [-33.mm,371.0625.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,369.0625.mm,40.mm], [-19.mm,369.0625.mm,40.mm], [-19.mm,371.0625.mm,40.mm], [-21.mm,371.0625.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,382.4829545454545.mm,40.mm], [-31.mm,382.4829545454545.mm,40.mm], [-31.mm,384.4829545454545.mm,40.mm], [-33.mm,384.4829545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,382.4829545454545.mm,40.mm], [-19.mm,382.4829545454545.mm,40.mm], [-19.mm,384.4829545454545.mm,40.mm], [-21.mm,384.4829545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,395.90340909090907.mm,40.mm], [-31.mm,395.90340909090907.mm,40.mm], [-31.mm,397.90340909090907.mm,40.mm], [-33.mm,397.90340909090907.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,395.90340909090907.mm,40.mm], [-19.mm,395.90340909090907.mm,40.mm], [-19.mm,397.90340909090907.mm,40.mm], [-21.mm,397.90340909090907.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,409.3238636363636.mm,40.mm], [-31.mm,409.3238636363636.mm,40.mm], [-31.mm,411.3238636363636.mm,40.mm], [-33.mm,411.3238636363636.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,409.3238636363636.mm,40.mm], [-19.mm,409.3238636363636.mm,40.mm], [-19.mm,411.3238636363636.mm,40.mm], [-21.mm,411.3238636363636.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,422.7443181818182.mm,40.mm], [-31.mm,422.7443181818182.mm,40.mm], [-31.mm,424.7443181818182.mm,40.mm], [-33.mm,424.7443181818182.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,422.7443181818182.mm,40.mm], [-19.mm,422.7443181818182.mm,40.mm], [-19.mm,424.7443181818182.mm,40.mm], [-21.mm,424.7443181818182.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,436.1647727272727.mm,40.mm], [-31.mm,436.1647727272727.mm,40.mm], [-31.mm,438.1647727272727.mm,40.mm], [-33.mm,438.1647727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,436.1647727272727.mm,40.mm], [-19.mm,436.1647727272727.mm,40.mm], [-19.mm,438.1647727272727.mm,40.mm], [-21.mm,438.1647727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,449.58522727272725.mm,40.mm], [-31.mm,449.58522727272725.mm,40.mm], [-31.mm,451.58522727272725.mm,40.mm], [-33.mm,451.58522727272725.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,449.58522727272725.mm,40.mm], [-19.mm,449.58522727272725.mm,40.mm], [-19.mm,451.58522727272725.mm,40.mm], [-21.mm,451.58522727272725.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,463.0056818181818.mm,40.mm], [-31.mm,463.0056818181818.mm,40.mm], [-31.mm,465.0056818181818.mm,40.mm], [-33.mm,465.0056818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,463.0056818181818.mm,40.mm], [-19.mm,463.0056818181818.mm,40.mm], [-19.mm,465.0056818181818.mm,40.mm], [-21.mm,465.0056818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,476.4261363636364.mm,40.mm], [-31.mm,476.4261363636364.mm,40.mm], [-31.mm,478.4261363636364.mm,40.mm], [-33.mm,478.4261363636364.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,476.4261363636364.mm,40.mm], [-19.mm,476.4261363636364.mm,40.mm], [-19.mm,478.4261363636364.mm,40.mm], [-21.mm,478.4261363636364.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,489.8465909090909.mm,40.mm], [-31.mm,489.8465909090909.mm,40.mm], [-31.mm,491.8465909090909.mm,40.mm], [-33.mm,491.8465909090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,489.8465909090909.mm,40.mm], [-19.mm,489.8465909090909.mm,40.mm], [-19.mm,491.8465909090909.mm,40.mm], [-21.mm,491.8465909090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,503.26704545454544.mm,40.mm], [-31.mm,503.26704545454544.mm,40.mm], [-31.mm,505.26704545454544.mm,40.mm], [-33.mm,505.26704545454544.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,503.26704545454544.mm,40.mm], [-19.mm,503.26704545454544.mm,40.mm], [-19.mm,505.26704545454544.mm,40.mm], [-21.mm,505.26704545454544.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,516.6875.mm,40.mm], [-31.mm,516.6875.mm,40.mm], [-31.mm,518.6875.mm,40.mm], [-33.mm,518.6875.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,516.6875.mm,40.mm], [-19.mm,516.6875.mm,40.mm], [-19.mm,518.6875.mm,40.mm], [-21.mm,518.6875.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,530.1079545454545.mm,40.mm], [-31.mm,530.1079545454545.mm,40.mm], [-31.mm,532.1079545454545.mm,40.mm], [-33.mm,532.1079545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,530.1079545454545.mm,40.mm], [-19.mm,530.1079545454545.mm,40.mm], [-19.mm,532.1079545454545.mm,40.mm], [-21.mm,532.1079545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,543.5284090909091.mm,40.mm], [-31.mm,543.5284090909091.mm,40.mm], [-31.mm,545.5284090909091.mm,40.mm], [-33.mm,545.5284090909091.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,543.5284090909091.mm,40.mm], [-19.mm,543.5284090909091.mm,40.mm], [-19.mm,545.5284090909091.mm,40.mm], [-21.mm,545.5284090909091.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,556.9488636363636.mm,40.mm], [-31.mm,556.9488636363636.mm,40.mm], [-31.mm,558.9488636363636.mm,40.mm], [-33.mm,558.9488636363636.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,556.9488636363636.mm,40.mm], [-19.mm,556.9488636363636.mm,40.mm], [-19.mm,558.9488636363636.mm,40.mm], [-21.mm,558.9488636363636.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,570.3693181818181.mm,40.mm], [-31.mm,570.3693181818181.mm,40.mm], [-31.mm,572.3693181818181.mm,40.mm], [-33.mm,572.3693181818181.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,570.3693181818181.mm,40.mm], [-19.mm,570.3693181818181.mm,40.mm], [-19.mm,572.3693181818181.mm,40.mm], [-21.mm,572.3693181818181.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,583.7897727272727.mm,40.mm], [-31.mm,583.7897727272727.mm,40.mm], [-31.mm,585.7897727272727.mm,40.mm], [-33.mm,585.7897727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,583.7897727272727.mm,40.mm], [-19.mm,583.7897727272727.mm,40.mm], [-19.mm,585.7897727272727.mm,40.mm], [-21.mm,585.7897727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,597.2102272727273.mm,40.mm], [-31.mm,597.2102272727273.mm,40.mm], [-31.mm,599.2102272727273.mm,40.mm], [-33.mm,599.2102272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,597.2102272727273.mm,40.mm], [-19.mm,597.2102272727273.mm,40.mm], [-19.mm,599.2102272727273.mm,40.mm], [-21.mm,599.2102272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,610.6306818181818.mm,40.mm], [-31.mm,610.6306818181818.mm,40.mm], [-31.mm,612.6306818181818.mm,40.mm], [-33.mm,612.6306818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,610.6306818181818.mm,40.mm], [-19.mm,610.6306818181818.mm,40.mm], [-19.mm,612.6306818181818.mm,40.mm], [-21.mm,612.6306818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,624.0511363636364.mm,40.mm], [-31.mm,624.0511363636364.mm,40.mm], [-31.mm,626.0511363636364.mm,40.mm], [-33.mm,626.0511363636364.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,624.0511363636364.mm,40.mm], [-19.mm,624.0511363636364.mm,40.mm], [-19.mm,626.0511363636364.mm,40.mm], [-21.mm,626.0511363636364.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,637.4715909090909.mm,40.mm], [-31.mm,637.4715909090909.mm,40.mm], [-31.mm,639.4715909090909.mm,40.mm], [-33.mm,639.4715909090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,637.4715909090909.mm,40.mm], [-19.mm,637.4715909090909.mm,40.mm], [-19.mm,639.4715909090909.mm,40.mm], [-21.mm,639.4715909090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,650.8920454545454.mm,40.mm], [-31.mm,650.8920454545454.mm,40.mm], [-31.mm,652.8920454545454.mm,40.mm], [-33.mm,652.8920454545454.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,650.8920454545454.mm,40.mm], [-19.mm,650.8920454545454.mm,40.mm], [-19.mm,652.8920454545454.mm,40.mm], [-21.mm,652.8920454545454.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,664.3125.mm,40.mm], [-31.mm,664.3125.mm,40.mm], [-31.mm,666.3125.mm,40.mm], [-33.mm,666.3125.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,664.3125.mm,40.mm], [-19.mm,664.3125.mm,40.mm], [-19.mm,666.3125.mm,40.mm], [-21.mm,666.3125.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,677.7329545454545.mm,40.mm], [-31.mm,677.7329545454545.mm,40.mm], [-31.mm,679.7329545454545.mm,40.mm], [-33.mm,679.7329545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,677.7329545454545.mm,40.mm], [-19.mm,677.7329545454545.mm,40.mm], [-19.mm,679.7329545454545.mm,40.mm], [-21.mm,679.7329545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,691.1534090909091.mm,40.mm], [-31.mm,691.1534090909091.mm,40.mm], [-31.mm,693.1534090909091.mm,40.mm], [-33.mm,693.1534090909091.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,691.1534090909091.mm,40.mm], [-19.mm,691.1534090909091.mm,40.mm], [-19.mm,693.1534090909091.mm,40.mm], [-21.mm,693.1534090909091.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,704.5738636363636.mm,40.mm], [-31.mm,704.5738636363636.mm,40.mm], [-31.mm,706.5738636363636.mm,40.mm], [-33.mm,706.5738636363636.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,704.5738636363636.mm,40.mm], [-19.mm,704.5738636363636.mm,40.mm], [-19.mm,706.5738636363636.mm,40.mm], [-21.mm,706.5738636363636.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,717.9943181818181.mm,40.mm], [-31.mm,717.9943181818181.mm,40.mm], [-31.mm,719.9943181818181.mm,40.mm], [-33.mm,719.9943181818181.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,717.9943181818181.mm,40.mm], [-19.mm,717.9943181818181.mm,40.mm], [-19.mm,719.9943181818181.mm,40.mm], [-21.mm,719.9943181818181.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,731.4147727272727.mm,40.mm], [-31.mm,731.4147727272727.mm,40.mm], [-31.mm,733.4147727272727.mm,40.mm], [-33.mm,733.4147727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,731.4147727272727.mm,40.mm], [-19.mm,731.4147727272727.mm,40.mm], [-19.mm,733.4147727272727.mm,40.mm], [-21.mm,733.4147727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,744.8352272727273.mm,40.mm], [-31.mm,744.8352272727273.mm,40.mm], [-31.mm,746.8352272727273.mm,40.mm], [-33.mm,746.8352272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,744.8352272727273.mm,40.mm], [-19.mm,744.8352272727273.mm,40.mm], [-19.mm,746.8352272727273.mm,40.mm], [-21.mm,746.8352272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,758.2556818181818.mm,40.mm], [-31.mm,758.2556818181818.mm,40.mm], [-31.mm,760.2556818181818.mm,40.mm], [-33.mm,760.2556818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,758.2556818181818.mm,40.mm], [-19.mm,758.2556818181818.mm,40.mm], [-19.mm,760.2556818181818.mm,40.mm], [-21.mm,760.2556818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,771.6761363636364.mm,40.mm], [-31.mm,771.6761363636364.mm,40.mm], [-31.mm,773.6761363636364.mm,40.mm], [-33.mm,773.6761363636364.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,771.6761363636364.mm,40.mm], [-19.mm,771.6761363636364.mm,40.mm], [-19.mm,773.6761363636364.mm,40.mm], [-21.mm,773.6761363636364.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,785.0965909090909.mm,40.mm], [-31.mm,785.0965909090909.mm,40.mm], [-31.mm,787.0965909090909.mm,40.mm], [-33.mm,787.0965909090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,785.0965909090909.mm,40.mm], [-19.mm,785.0965909090909.mm,40.mm], [-19.mm,787.0965909090909.mm,40.mm], [-21.mm,787.0965909090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,798.5170454545454.mm,40.mm], [-31.mm,798.5170454545454.mm,40.mm], [-31.mm,800.5170454545454.mm,40.mm], [-33.mm,800.5170454545454.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,798.5170454545454.mm,40.mm], [-19.mm,798.5170454545454.mm,40.mm], [-19.mm,800.5170454545454.mm,40.mm], [-21.mm,800.5170454545454.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,811.9375.mm,40.mm], [-31.mm,811.9375.mm,40.mm], [-31.mm,813.9375.mm,40.mm], [-33.mm,813.9375.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,811.9375.mm,40.mm], [-19.mm,811.9375.mm,40.mm], [-19.mm,813.9375.mm,40.mm], [-21.mm,813.9375.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,825.3579545454545.mm,40.mm], [-31.mm,825.3579545454545.mm,40.mm], [-31.mm,827.3579545454545.mm,40.mm], [-33.mm,827.3579545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,825.3579545454545.mm,40.mm], [-19.mm,825.3579545454545.mm,40.mm], [-19.mm,827.3579545454545.mm,40.mm], [-21.mm,827.3579545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,838.778409090909.mm,40.mm], [-31.mm,838.778409090909.mm,40.mm], [-31.mm,840.778409090909.mm,40.mm], [-33.mm,840.778409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,838.778409090909.mm,40.mm], [-19.mm,838.778409090909.mm,40.mm], [-19.mm,840.778409090909.mm,40.mm], [-21.mm,840.778409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,852.1988636363636.mm,40.mm], [-31.mm,852.1988636363636.mm,40.mm], [-31.mm,854.1988636363636.mm,40.mm], [-33.mm,854.1988636363636.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,852.1988636363636.mm,40.mm], [-19.mm,852.1988636363636.mm,40.mm], [-19.mm,854.1988636363636.mm,40.mm], [-21.mm,854.1988636363636.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,865.6193181818181.mm,40.mm], [-31.mm,865.6193181818181.mm,40.mm], [-31.mm,867.6193181818181.mm,40.mm], [-33.mm,867.6193181818181.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,865.6193181818181.mm,40.mm], [-19.mm,865.6193181818181.mm,40.mm], [-19.mm,867.6193181818181.mm,40.mm], [-21.mm,867.6193181818181.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,879.0397727272727.mm,40.mm], [-31.mm,879.0397727272727.mm,40.mm], [-31.mm,881.0397727272727.mm,40.mm], [-33.mm,881.0397727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,879.0397727272727.mm,40.mm], [-19.mm,879.0397727272727.mm,40.mm], [-19.mm,881.0397727272727.mm,40.mm], [-21.mm,881.0397727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,892.4602272727273.mm,40.mm], [-31.mm,892.4602272727273.mm,40.mm], [-31.mm,894.4602272727273.mm,40.mm], [-33.mm,894.4602272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,892.4602272727273.mm,40.mm], [-19.mm,892.4602272727273.mm,40.mm], [-19.mm,894.4602272727273.mm,40.mm], [-21.mm,894.4602272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,905.8806818181818.mm,40.mm], [-31.mm,905.8806818181818.mm,40.mm], [-31.mm,907.8806818181818.mm,40.mm], [-33.mm,907.8806818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,905.8806818181818.mm,40.mm], [-19.mm,905.8806818181818.mm,40.mm], [-19.mm,907.8806818181818.mm,40.mm], [-21.mm,907.8806818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,919.3011363636364.mm,40.mm], [-31.mm,919.3011363636364.mm,40.mm], [-31.mm,921.3011363636364.mm,40.mm], [-33.mm,921.3011363636364.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,919.3011363636364.mm,40.mm], [-19.mm,919.3011363636364.mm,40.mm], [-19.mm,921.3011363636364.mm,40.mm], [-21.mm,921.3011363636364.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,932.7215909090909.mm,40.mm], [-31.mm,932.7215909090909.mm,40.mm], [-31.mm,934.7215909090909.mm,40.mm], [-33.mm,934.7215909090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,932.7215909090909.mm,40.mm], [-19.mm,932.7215909090909.mm,40.mm], [-19.mm,934.7215909090909.mm,40.mm], [-21.mm,934.7215909090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,946.1420454545454.mm,40.mm], [-31.mm,946.1420454545454.mm,40.mm], [-31.mm,948.1420454545454.mm,40.mm], [-33.mm,948.1420454545454.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,946.1420454545454.mm,40.mm], [-19.mm,946.1420454545454.mm,40.mm], [-19.mm,948.1420454545454.mm,40.mm], [-21.mm,948.1420454545454.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,959.5625.mm,40.mm], [-31.mm,959.5625.mm,40.mm], [-31.mm,961.5625.mm,40.mm], [-33.mm,961.5625.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,959.5625.mm,40.mm], [-19.mm,959.5625.mm,40.mm], [-19.mm,961.5625.mm,40.mm], [-21.mm,961.5625.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,972.9829545454545.mm,40.mm], [-31.mm,972.9829545454545.mm,40.mm], [-31.mm,974.9829545454545.mm,40.mm], [-33.mm,974.9829545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,972.9829545454545.mm,40.mm], [-19.mm,972.9829545454545.mm,40.mm], [-19.mm,974.9829545454545.mm,40.mm], [-21.mm,974.9829545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,986.403409090909.mm,40.mm], [-31.mm,986.403409090909.mm,40.mm], [-31.mm,988.403409090909.mm,40.mm], [-33.mm,988.403409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,986.403409090909.mm,40.mm], [-19.mm,986.403409090909.mm,40.mm], [-19.mm,988.403409090909.mm,40.mm], [-21.mm,988.403409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,999.8238636363636.mm,40.mm], [-31.mm,999.8238636363636.mm,40.mm], [-31.mm,1001.8238636363636.mm,40.mm], [-33.mm,1001.8238636363636.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,999.8238636363636.mm,40.mm], [-19.mm,999.8238636363636.mm,40.mm], [-19.mm,1001.8238636363636.mm,40.mm], [-21.mm,1001.8238636363636.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1013.2443181818181.mm,40.mm], [-31.mm,1013.2443181818181.mm,40.mm], [-31.mm,1015.2443181818181.mm,40.mm], [-33.mm,1015.2443181818181.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1013.2443181818181.mm,40.mm], [-19.mm,1013.2443181818181.mm,40.mm], [-19.mm,1015.2443181818181.mm,40.mm], [-21.mm,1015.2443181818181.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1026.6647727272727.mm,40.mm], [-31.mm,1026.6647727272727.mm,40.mm], [-31.mm,1028.6647727272727.mm,40.mm], [-33.mm,1028.6647727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1026.6647727272727.mm,40.mm], [-19.mm,1026.6647727272727.mm,40.mm], [-19.mm,1028.6647727272727.mm,40.mm], [-21.mm,1028.6647727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1040.0852272727273.mm,40.mm], [-31.mm,1040.0852272727273.mm,40.mm], [-31.mm,1042.0852272727273.mm,40.mm], [-33.mm,1042.0852272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1040.0852272727273.mm,40.mm], [-19.mm,1040.0852272727273.mm,40.mm], [-19.mm,1042.0852272727273.mm,40.mm], [-21.mm,1042.0852272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1053.5056818181818.mm,40.mm], [-31.mm,1053.5056818181818.mm,40.mm], [-31.mm,1055.5056818181818.mm,40.mm], [-33.mm,1055.5056818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1053.5056818181818.mm,40.mm], [-19.mm,1053.5056818181818.mm,40.mm], [-19.mm,1055.5056818181818.mm,40.mm], [-21.mm,1055.5056818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1066.9261363636363.mm,40.mm], [-31.mm,1066.9261363636363.mm,40.mm], [-31.mm,1068.9261363636363.mm,40.mm], [-33.mm,1068.9261363636363.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1066.9261363636363.mm,40.mm], [-19.mm,1066.9261363636363.mm,40.mm], [-19.mm,1068.9261363636363.mm,40.mm], [-21.mm,1068.9261363636363.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1080.3465909090908.mm,40.mm], [-31.mm,1080.3465909090908.mm,40.mm], [-31.mm,1082.3465909090908.mm,40.mm], [-33.mm,1082.3465909090908.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1080.3465909090908.mm,40.mm], [-19.mm,1080.3465909090908.mm,40.mm], [-19.mm,1082.3465909090908.mm,40.mm], [-21.mm,1082.3465909090908.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1093.7670454545455.mm,40.mm], [-31.mm,1093.7670454545455.mm,40.mm], [-31.mm,1095.7670454545455.mm,40.mm], [-33.mm,1095.7670454545455.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1093.7670454545455.mm,40.mm], [-19.mm,1093.7670454545455.mm,40.mm], [-19.mm,1095.7670454545455.mm,40.mm], [-21.mm,1095.7670454545455.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1107.1875.mm,40.mm], [-31.mm,1107.1875.mm,40.mm], [-31.mm,1109.1875.mm,40.mm], [-33.mm,1109.1875.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1107.1875.mm,40.mm], [-19.mm,1107.1875.mm,40.mm], [-19.mm,1109.1875.mm,40.mm], [-21.mm,1109.1875.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1120.6079545454545.mm,40.mm], [-31.mm,1120.6079545454545.mm,40.mm], [-31.mm,1122.6079545454545.mm,40.mm], [-33.mm,1122.6079545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1120.6079545454545.mm,40.mm], [-19.mm,1120.6079545454545.mm,40.mm], [-19.mm,1122.6079545454545.mm,40.mm], [-21.mm,1122.6079545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1134.028409090909.mm,40.mm], [-31.mm,1134.028409090909.mm,40.mm], [-31.mm,1136.028409090909.mm,40.mm], [-33.mm,1136.028409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1134.028409090909.mm,40.mm], [-19.mm,1134.028409090909.mm,40.mm], [-19.mm,1136.028409090909.mm,40.mm], [-21.mm,1136.028409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1147.4488636363635.mm,40.mm], [-31.mm,1147.4488636363635.mm,40.mm], [-31.mm,1149.4488636363635.mm,40.mm], [-33.mm,1149.4488636363635.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1147.4488636363635.mm,40.mm], [-19.mm,1147.4488636363635.mm,40.mm], [-19.mm,1149.4488636363635.mm,40.mm], [-21.mm,1149.4488636363635.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1160.8693181818182.mm,40.mm], [-31.mm,1160.8693181818182.mm,40.mm], [-31.mm,1162.8693181818182.mm,40.mm], [-33.mm,1162.8693181818182.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1160.8693181818182.mm,40.mm], [-19.mm,1160.8693181818182.mm,40.mm], [-19.mm,1162.8693181818182.mm,40.mm], [-21.mm,1162.8693181818182.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1174.2897727272727.mm,40.mm], [-31.mm,1174.2897727272727.mm,40.mm], [-31.mm,1176.2897727272727.mm,40.mm], [-33.mm,1176.2897727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1174.2897727272727.mm,40.mm], [-19.mm,1174.2897727272727.mm,40.mm], [-19.mm,1176.2897727272727.mm,40.mm], [-21.mm,1176.2897727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1187.7102272727273.mm,40.mm], [-31.mm,1187.7102272727273.mm,40.mm], [-31.mm,1189.7102272727273.mm,40.mm], [-33.mm,1189.7102272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1187.7102272727273.mm,40.mm], [-19.mm,1187.7102272727273.mm,40.mm], [-19.mm,1189.7102272727273.mm,40.mm], [-21.mm,1189.7102272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1201.1306818181818.mm,40.mm], [-31.mm,1201.1306818181818.mm,40.mm], [-31.mm,1203.1306818181818.mm,40.mm], [-33.mm,1203.1306818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1201.1306818181818.mm,40.mm], [-19.mm,1201.1306818181818.mm,40.mm], [-19.mm,1203.1306818181818.mm,40.mm], [-21.mm,1203.1306818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1214.5511363636363.mm,40.mm], [-31.mm,1214.5511363636363.mm,40.mm], [-31.mm,1216.5511363636363.mm,40.mm], [-33.mm,1216.5511363636363.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1214.5511363636363.mm,40.mm], [-19.mm,1214.5511363636363.mm,40.mm], [-19.mm,1216.5511363636363.mm,40.mm], [-21.mm,1216.5511363636363.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1227.9715909090908.mm,40.mm], [-31.mm,1227.9715909090908.mm,40.mm], [-31.mm,1229.9715909090908.mm,40.mm], [-33.mm,1229.9715909090908.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1227.9715909090908.mm,40.mm], [-19.mm,1227.9715909090908.mm,40.mm], [-19.mm,1229.9715909090908.mm,40.mm], [-21.mm,1229.9715909090908.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1241.3920454545455.mm,40.mm], [-31.mm,1241.3920454545455.mm,40.mm], [-31.mm,1243.3920454545455.mm,40.mm], [-33.mm,1243.3920454545455.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1241.3920454545455.mm,40.mm], [-19.mm,1241.3920454545455.mm,40.mm], [-19.mm,1243.3920454545455.mm,40.mm], [-21.mm,1243.3920454545455.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1254.8125.mm,40.mm], [-31.mm,1254.8125.mm,40.mm], [-31.mm,1256.8125.mm,40.mm], [-33.mm,1256.8125.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1254.8125.mm,40.mm], [-19.mm,1254.8125.mm,40.mm], [-19.mm,1256.8125.mm,40.mm], [-21.mm,1256.8125.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1268.2329545454545.mm,40.mm], [-31.mm,1268.2329545454545.mm,40.mm], [-31.mm,1270.2329545454545.mm,40.mm], [-33.mm,1270.2329545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1268.2329545454545.mm,40.mm], [-19.mm,1268.2329545454545.mm,40.mm], [-19.mm,1270.2329545454545.mm,40.mm], [-21.mm,1270.2329545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1281.653409090909.mm,40.mm], [-31.mm,1281.653409090909.mm,40.mm], [-31.mm,1283.653409090909.mm,40.mm], [-33.mm,1283.653409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1281.653409090909.mm,40.mm], [-19.mm,1281.653409090909.mm,40.mm], [-19.mm,1283.653409090909.mm,40.mm], [-21.mm,1283.653409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1295.0738636363635.mm,40.mm], [-31.mm,1295.0738636363635.mm,40.mm], [-31.mm,1297.0738636363635.mm,40.mm], [-33.mm,1297.0738636363635.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1295.0738636363635.mm,40.mm], [-19.mm,1295.0738636363635.mm,40.mm], [-19.mm,1297.0738636363635.mm,40.mm], [-21.mm,1297.0738636363635.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1308.4943181818182.mm,40.mm], [-31.mm,1308.4943181818182.mm,40.mm], [-31.mm,1310.4943181818182.mm,40.mm], [-33.mm,1310.4943181818182.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1308.4943181818182.mm,40.mm], [-19.mm,1308.4943181818182.mm,40.mm], [-19.mm,1310.4943181818182.mm,40.mm], [-21.mm,1310.4943181818182.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1321.9147727272727.mm,40.mm], [-31.mm,1321.9147727272727.mm,40.mm], [-31.mm,1323.9147727272727.mm,40.mm], [-33.mm,1323.9147727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1321.9147727272727.mm,40.mm], [-19.mm,1321.9147727272727.mm,40.mm], [-19.mm,1323.9147727272727.mm,40.mm], [-21.mm,1323.9147727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1335.3352272727273.mm,40.mm], [-31.mm,1335.3352272727273.mm,40.mm], [-31.mm,1337.3352272727273.mm,40.mm], [-33.mm,1337.3352272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1335.3352272727273.mm,40.mm], [-19.mm,1335.3352272727273.mm,40.mm], [-19.mm,1337.3352272727273.mm,40.mm], [-21.mm,1337.3352272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1348.7556818181818.mm,40.mm], [-31.mm,1348.7556818181818.mm,40.mm], [-31.mm,1350.7556818181818.mm,40.mm], [-33.mm,1350.7556818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1348.7556818181818.mm,40.mm], [-19.mm,1348.7556818181818.mm,40.mm], [-19.mm,1350.7556818181818.mm,40.mm], [-21.mm,1350.7556818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1362.1761363636363.mm,40.mm], [-31.mm,1362.1761363636363.mm,40.mm], [-31.mm,1364.1761363636363.mm,40.mm], [-33.mm,1364.1761363636363.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1362.1761363636363.mm,40.mm], [-19.mm,1362.1761363636363.mm,40.mm], [-19.mm,1364.1761363636363.mm,40.mm], [-21.mm,1364.1761363636363.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1375.5965909090908.mm,40.mm], [-31.mm,1375.5965909090908.mm,40.mm], [-31.mm,1377.5965909090908.mm,40.mm], [-33.mm,1377.5965909090908.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1375.5965909090908.mm,40.mm], [-19.mm,1375.5965909090908.mm,40.mm], [-19.mm,1377.5965909090908.mm,40.mm], [-21.mm,1377.5965909090908.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1389.0170454545455.mm,40.mm], [-31.mm,1389.0170454545455.mm,40.mm], [-31.mm,1391.0170454545455.mm,40.mm], [-33.mm,1391.0170454545455.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1389.0170454545455.mm,40.mm], [-19.mm,1389.0170454545455.mm,40.mm], [-19.mm,1391.0170454545455.mm,40.mm], [-21.mm,1391.0170454545455.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1402.4375.mm,40.mm], [-31.mm,1402.4375.mm,40.mm], [-31.mm,1404.4375.mm,40.mm], [-33.mm,1404.4375.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1402.4375.mm,40.mm], [-19.mm,1402.4375.mm,40.mm], [-19.mm,1404.4375.mm,40.mm], [-21.mm,1404.4375.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1415.8579545454545.mm,40.mm], [-31.mm,1415.8579545454545.mm,40.mm], [-31.mm,1417.8579545454545.mm,40.mm], [-33.mm,1417.8579545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1415.8579545454545.mm,40.mm], [-19.mm,1415.8579545454545.mm,40.mm], [-19.mm,1417.8579545454545.mm,40.mm], [-21.mm,1417.8579545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1429.278409090909.mm,40.mm], [-31.mm,1429.278409090909.mm,40.mm], [-31.mm,1431.278409090909.mm,40.mm], [-33.mm,1431.278409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1429.278409090909.mm,40.mm], [-19.mm,1429.278409090909.mm,40.mm], [-19.mm,1431.278409090909.mm,40.mm], [-21.mm,1431.278409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1442.6988636363635.mm,40.mm], [-31.mm,1442.6988636363635.mm,40.mm], [-31.mm,1444.6988636363635.mm,40.mm], [-33.mm,1444.6988636363635.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1442.6988636363635.mm,40.mm], [-19.mm,1442.6988636363635.mm,40.mm], [-19.mm,1444.6988636363635.mm,40.mm], [-21.mm,1444.6988636363635.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1456.119318181818.mm,40.mm], [-31.mm,1456.119318181818.mm,40.mm], [-31.mm,1458.119318181818.mm,40.mm], [-33.mm,1458.119318181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1456.119318181818.mm,40.mm], [-19.mm,1456.119318181818.mm,40.mm], [-19.mm,1458.119318181818.mm,40.mm], [-21.mm,1458.119318181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1469.5397727272727.mm,40.mm], [-31.mm,1469.5397727272727.mm,40.mm], [-31.mm,1471.5397727272727.mm,40.mm], [-33.mm,1471.5397727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1469.5397727272727.mm,40.mm], [-19.mm,1469.5397727272727.mm,40.mm], [-19.mm,1471.5397727272727.mm,40.mm], [-21.mm,1471.5397727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1482.9602272727273.mm,40.mm], [-31.mm,1482.9602272727273.mm,40.mm], [-31.mm,1484.9602272727273.mm,40.mm], [-33.mm,1484.9602272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1482.9602272727273.mm,40.mm], [-19.mm,1482.9602272727273.mm,40.mm], [-19.mm,1484.9602272727273.mm,40.mm], [-21.mm,1484.9602272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1496.3806818181818.mm,40.mm], [-31.mm,1496.3806818181818.mm,40.mm], [-31.mm,1498.3806818181818.mm,40.mm], [-33.mm,1498.3806818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1496.3806818181818.mm,40.mm], [-19.mm,1496.3806818181818.mm,40.mm], [-19.mm,1498.3806818181818.mm,40.mm], [-21.mm,1498.3806818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1509.8011363636363.mm,40.mm], [-31.mm,1509.8011363636363.mm,40.mm], [-31.mm,1511.8011363636363.mm,40.mm], [-33.mm,1511.8011363636363.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1509.8011363636363.mm,40.mm], [-19.mm,1509.8011363636363.mm,40.mm], [-19.mm,1511.8011363636363.mm,40.mm], [-21.mm,1511.8011363636363.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1523.2215909090908.mm,40.mm], [-31.mm,1523.2215909090908.mm,40.mm], [-31.mm,1525.2215909090908.mm,40.mm], [-33.mm,1525.2215909090908.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1523.2215909090908.mm,40.mm], [-19.mm,1523.2215909090908.mm,40.mm], [-19.mm,1525.2215909090908.mm,40.mm], [-21.mm,1525.2215909090908.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1536.6420454545455.mm,40.mm], [-31.mm,1536.6420454545455.mm,40.mm], [-31.mm,1538.6420454545455.mm,40.mm], [-33.mm,1538.6420454545455.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1536.6420454545455.mm,40.mm], [-19.mm,1536.6420454545455.mm,40.mm], [-19.mm,1538.6420454545455.mm,40.mm], [-21.mm,1538.6420454545455.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1550.0625.mm,40.mm], [-31.mm,1550.0625.mm,40.mm], [-31.mm,1552.0625.mm,40.mm], [-33.mm,1552.0625.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1550.0625.mm,40.mm], [-19.mm,1550.0625.mm,40.mm], [-19.mm,1552.0625.mm,40.mm], [-21.mm,1552.0625.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1563.4829545454545.mm,40.mm], [-31.mm,1563.4829545454545.mm,40.mm], [-31.mm,1565.4829545454545.mm,40.mm], [-33.mm,1565.4829545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1563.4829545454545.mm,40.mm], [-19.mm,1563.4829545454545.mm,40.mm], [-19.mm,1565.4829545454545.mm,40.mm], [-21.mm,1565.4829545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1576.903409090909.mm,40.mm], [-31.mm,1576.903409090909.mm,40.mm], [-31.mm,1578.903409090909.mm,40.mm], [-33.mm,1578.903409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1576.903409090909.mm,40.mm], [-19.mm,1576.903409090909.mm,40.mm], [-19.mm,1578.903409090909.mm,40.mm], [-21.mm,1578.903409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1590.3238636363635.mm,40.mm], [-31.mm,1590.3238636363635.mm,40.mm], [-31.mm,1592.3238636363635.mm,40.mm], [-33.mm,1592.3238636363635.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1590.3238636363635.mm,40.mm], [-19.mm,1590.3238636363635.mm,40.mm], [-19.mm,1592.3238636363635.mm,40.mm], [-21.mm,1592.3238636363635.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1603.744318181818.mm,40.mm], [-31.mm,1603.744318181818.mm,40.mm], [-31.mm,1605.744318181818.mm,40.mm], [-33.mm,1605.744318181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1603.744318181818.mm,40.mm], [-19.mm,1603.744318181818.mm,40.mm], [-19.mm,1605.744318181818.mm,40.mm], [-21.mm,1605.744318181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1617.1647727272727.mm,40.mm], [-31.mm,1617.1647727272727.mm,40.mm], [-31.mm,1619.1647727272727.mm,40.mm], [-33.mm,1619.1647727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1617.1647727272727.mm,40.mm], [-19.mm,1617.1647727272727.mm,40.mm], [-19.mm,1619.1647727272727.mm,40.mm], [-21.mm,1619.1647727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1630.5852272727273.mm,40.mm], [-31.mm,1630.5852272727273.mm,40.mm], [-31.mm,1632.5852272727273.mm,40.mm], [-33.mm,1632.5852272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1630.5852272727273.mm,40.mm], [-19.mm,1630.5852272727273.mm,40.mm], [-19.mm,1632.5852272727273.mm,40.mm], [-21.mm,1632.5852272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1644.0056818181818.mm,40.mm], [-31.mm,1644.0056818181818.mm,40.mm], [-31.mm,1646.0056818181818.mm,40.mm], [-33.mm,1646.0056818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1644.0056818181818.mm,40.mm], [-19.mm,1644.0056818181818.mm,40.mm], [-19.mm,1646.0056818181818.mm,40.mm], [-21.mm,1646.0056818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1657.4261363636363.mm,40.mm], [-31.mm,1657.4261363636363.mm,40.mm], [-31.mm,1659.4261363636363.mm,40.mm], [-33.mm,1659.4261363636363.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1657.4261363636363.mm,40.mm], [-19.mm,1657.4261363636363.mm,40.mm], [-19.mm,1659.4261363636363.mm,40.mm], [-21.mm,1659.4261363636363.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1670.8465909090908.mm,40.mm], [-31.mm,1670.8465909090908.mm,40.mm], [-31.mm,1672.8465909090908.mm,40.mm], [-33.mm,1672.8465909090908.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1670.8465909090908.mm,40.mm], [-19.mm,1670.8465909090908.mm,40.mm], [-19.mm,1672.8465909090908.mm,40.mm], [-21.mm,1672.8465909090908.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1684.2670454545455.mm,40.mm], [-31.mm,1684.2670454545455.mm,40.mm], [-31.mm,1686.2670454545455.mm,40.mm], [-33.mm,1686.2670454545455.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1684.2670454545455.mm,40.mm], [-19.mm,1684.2670454545455.mm,40.mm], [-19.mm,1686.2670454545455.mm,40.mm], [-21.mm,1686.2670454545455.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1697.6875.mm,40.mm], [-31.mm,1697.6875.mm,40.mm], [-31.mm,1699.6875.mm,40.mm], [-33.mm,1699.6875.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1697.6875.mm,40.mm], [-19.mm,1697.6875.mm,40.mm], [-19.mm,1699.6875.mm,40.mm], [-21.mm,1699.6875.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1711.1079545454545.mm,40.mm], [-31.mm,1711.1079545454545.mm,40.mm], [-31.mm,1713.1079545454545.mm,40.mm], [-33.mm,1713.1079545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1711.1079545454545.mm,40.mm], [-19.mm,1711.1079545454545.mm,40.mm], [-19.mm,1713.1079545454545.mm,40.mm], [-21.mm,1713.1079545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1724.528409090909.mm,40.mm], [-31.mm,1724.528409090909.mm,40.mm], [-31.mm,1726.528409090909.mm,40.mm], [-33.mm,1726.528409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1724.528409090909.mm,40.mm], [-19.mm,1724.528409090909.mm,40.mm], [-19.mm,1726.528409090909.mm,40.mm], [-21.mm,1726.528409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1737.9488636363635.mm,40.mm], [-31.mm,1737.9488636363635.mm,40.mm], [-31.mm,1739.9488636363635.mm,40.mm], [-33.mm,1739.9488636363635.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1737.9488636363635.mm,40.mm], [-19.mm,1737.9488636363635.mm,40.mm], [-19.mm,1739.9488636363635.mm,40.mm], [-21.mm,1739.9488636363635.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1751.369318181818.mm,40.mm], [-31.mm,1751.369318181818.mm,40.mm], [-31.mm,1753.369318181818.mm,40.mm], [-33.mm,1753.369318181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1751.369318181818.mm,40.mm], [-19.mm,1751.369318181818.mm,40.mm], [-19.mm,1753.369318181818.mm,40.mm], [-21.mm,1753.369318181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1764.7897727272727.mm,40.mm], [-31.mm,1764.7897727272727.mm,40.mm], [-31.mm,1766.7897727272727.mm,40.mm], [-33.mm,1766.7897727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1764.7897727272727.mm,40.mm], [-19.mm,1764.7897727272727.mm,40.mm], [-19.mm,1766.7897727272727.mm,40.mm], [-21.mm,1766.7897727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1778.2102272727273.mm,40.mm], [-31.mm,1778.2102272727273.mm,40.mm], [-31.mm,1780.2102272727273.mm,40.mm], [-33.mm,1780.2102272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1778.2102272727273.mm,40.mm], [-19.mm,1778.2102272727273.mm,40.mm], [-19.mm,1780.2102272727273.mm,40.mm], [-21.mm,1780.2102272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1791.6306818181818.mm,40.mm], [-31.mm,1791.6306818181818.mm,40.mm], [-31.mm,1793.6306818181818.mm,40.mm], [-33.mm,1793.6306818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1791.6306818181818.mm,40.mm], [-19.mm,1791.6306818181818.mm,40.mm], [-19.mm,1793.6306818181818.mm,40.mm], [-21.mm,1793.6306818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1805.0511363636363.mm,40.mm], [-31.mm,1805.0511363636363.mm,40.mm], [-31.mm,1807.0511363636363.mm,40.mm], [-33.mm,1807.0511363636363.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1805.0511363636363.mm,40.mm], [-19.mm,1805.0511363636363.mm,40.mm], [-19.mm,1807.0511363636363.mm,40.mm], [-21.mm,1807.0511363636363.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1818.4715909090908.mm,40.mm], [-31.mm,1818.4715909090908.mm,40.mm], [-31.mm,1820.4715909090908.mm,40.mm], [-33.mm,1820.4715909090908.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1818.4715909090908.mm,40.mm], [-19.mm,1818.4715909090908.mm,40.mm], [-19.mm,1820.4715909090908.mm,40.mm], [-21.mm,1820.4715909090908.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1831.8920454545455.mm,40.mm], [-31.mm,1831.8920454545455.mm,40.mm], [-31.mm,1833.8920454545455.mm,40.mm], [-33.mm,1833.8920454545455.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1831.8920454545455.mm,40.mm], [-19.mm,1831.8920454545455.mm,40.mm], [-19.mm,1833.8920454545455.mm,40.mm], [-21.mm,1833.8920454545455.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1845.3125.mm,40.mm], [-31.mm,1845.3125.mm,40.mm], [-31.mm,1847.3125.mm,40.mm], [-33.mm,1847.3125.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1845.3125.mm,40.mm], [-19.mm,1845.3125.mm,40.mm], [-19.mm,1847.3125.mm,40.mm], [-21.mm,1847.3125.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1858.7329545454545.mm,40.mm], [-31.mm,1858.7329545454545.mm,40.mm], [-31.mm,1860.7329545454545.mm,40.mm], [-33.mm,1860.7329545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1858.7329545454545.mm,40.mm], [-19.mm,1858.7329545454545.mm,40.mm], [-19.mm,1860.7329545454545.mm,40.mm], [-21.mm,1860.7329545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1872.153409090909.mm,40.mm], [-31.mm,1872.153409090909.mm,40.mm], [-31.mm,1874.153409090909.mm,40.mm], [-33.mm,1874.153409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1872.153409090909.mm,40.mm], [-19.mm,1872.153409090909.mm,40.mm], [-19.mm,1874.153409090909.mm,40.mm], [-21.mm,1874.153409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1885.5738636363635.mm,40.mm], [-31.mm,1885.5738636363635.mm,40.mm], [-31.mm,1887.5738636363635.mm,40.mm], [-33.mm,1887.5738636363635.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1885.5738636363635.mm,40.mm], [-19.mm,1885.5738636363635.mm,40.mm], [-19.mm,1887.5738636363635.mm,40.mm], [-21.mm,1887.5738636363635.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1898.994318181818.mm,40.mm], [-31.mm,1898.994318181818.mm,40.mm], [-31.mm,1900.994318181818.mm,40.mm], [-33.mm,1900.994318181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1898.994318181818.mm,40.mm], [-19.mm,1898.994318181818.mm,40.mm], [-19.mm,1900.994318181818.mm,40.mm], [-21.mm,1900.994318181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1912.4147727272727.mm,40.mm], [-31.mm,1912.4147727272727.mm,40.mm], [-31.mm,1914.4147727272727.mm,40.mm], [-33.mm,1914.4147727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1912.4147727272727.mm,40.mm], [-19.mm,1912.4147727272727.mm,40.mm], [-19.mm,1914.4147727272727.mm,40.mm], [-21.mm,1914.4147727272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1925.8352272727273.mm,40.mm], [-31.mm,1925.8352272727273.mm,40.mm], [-31.mm,1927.8352272727273.mm,40.mm], [-33.mm,1927.8352272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1925.8352272727273.mm,40.mm], [-19.mm,1925.8352272727273.mm,40.mm], [-19.mm,1927.8352272727273.mm,40.mm], [-21.mm,1927.8352272727273.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1939.2556818181818.mm,40.mm], [-31.mm,1939.2556818181818.mm,40.mm], [-31.mm,1941.2556818181818.mm,40.mm], [-33.mm,1941.2556818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1939.2556818181818.mm,40.mm], [-19.mm,1939.2556818181818.mm,40.mm], [-19.mm,1941.2556818181818.mm,40.mm], [-21.mm,1941.2556818181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1952.6761363636363.mm,40.mm], [-31.mm,1952.6761363636363.mm,40.mm], [-31.mm,1954.6761363636363.mm,40.mm], [-33.mm,1954.6761363636363.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1952.6761363636363.mm,40.mm], [-19.mm,1952.6761363636363.mm,40.mm], [-19.mm,1954.6761363636363.mm,40.mm], [-21.mm,1954.6761363636363.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1966.0965909090908.mm,40.mm], [-31.mm,1966.0965909090908.mm,40.mm], [-31.mm,1968.0965909090908.mm,40.mm], [-33.mm,1968.0965909090908.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1966.0965909090908.mm,40.mm], [-19.mm,1966.0965909090908.mm,40.mm], [-19.mm,1968.0965909090908.mm,40.mm], [-21.mm,1968.0965909090908.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1979.5170454545455.mm,40.mm], [-31.mm,1979.5170454545455.mm,40.mm], [-31.mm,1981.5170454545455.mm,40.mm], [-33.mm,1981.5170454545455.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1979.5170454545455.mm,40.mm], [-19.mm,1979.5170454545455.mm,40.mm], [-19.mm,1981.5170454545455.mm,40.mm], [-21.mm,1981.5170454545455.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1992.9375.mm,40.mm], [-31.mm,1992.9375.mm,40.mm], [-31.mm,1994.9375.mm,40.mm], [-33.mm,1994.9375.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1992.9375.mm,40.mm], [-19.mm,1992.9375.mm,40.mm], [-19.mm,1994.9375.mm,40.mm], [-21.mm,1994.9375.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2006.3579545454545.mm,40.mm], [-31.mm,2006.3579545454545.mm,40.mm], [-31.mm,2008.3579545454545.mm,40.mm], [-33.mm,2008.3579545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2006.3579545454545.mm,40.mm], [-19.mm,2006.3579545454545.mm,40.mm], [-19.mm,2008.3579545454545.mm,40.mm], [-21.mm,2008.3579545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2019.778409090909.mm,40.mm], [-31.mm,2019.778409090909.mm,40.mm], [-31.mm,2021.778409090909.mm,40.mm], [-33.mm,2021.778409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2019.778409090909.mm,40.mm], [-19.mm,2019.778409090909.mm,40.mm], [-19.mm,2021.778409090909.mm,40.mm], [-21.mm,2021.778409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2033.1988636363635.mm,40.mm], [-31.mm,2033.1988636363635.mm,40.mm], [-31.mm,2035.1988636363635.mm,40.mm], [-33.mm,2035.1988636363635.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2033.1988636363635.mm,40.mm], [-19.mm,2033.1988636363635.mm,40.mm], [-19.mm,2035.1988636363635.mm,40.mm], [-21.mm,2035.1988636363635.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2046.619318181818.mm,40.mm], [-31.mm,2046.619318181818.mm,40.mm], [-31.mm,2048.619318181818.mm,40.mm], [-33.mm,2048.619318181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2046.619318181818.mm,40.mm], [-19.mm,2046.619318181818.mm,40.mm], [-19.mm,2048.619318181818.mm,40.mm], [-21.mm,2048.619318181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2060.0397727272725.mm,40.mm], [-31.mm,2060.0397727272725.mm,40.mm], [-31.mm,2062.0397727272725.mm,40.mm], [-33.mm,2062.0397727272725.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2060.0397727272725.mm,40.mm], [-19.mm,2060.0397727272725.mm,40.mm], [-19.mm,2062.0397727272725.mm,40.mm], [-21.mm,2062.0397727272725.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2073.460227272727.mm,40.mm], [-31.mm,2073.460227272727.mm,40.mm], [-31.mm,2075.460227272727.mm,40.mm], [-33.mm,2075.460227272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2073.460227272727.mm,40.mm], [-19.mm,2073.460227272727.mm,40.mm], [-19.mm,2075.460227272727.mm,40.mm], [-21.mm,2075.460227272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2086.8806818181815.mm,40.mm], [-31.mm,2086.8806818181815.mm,40.mm], [-31.mm,2088.8806818181815.mm,40.mm], [-33.mm,2088.8806818181815.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2086.8806818181815.mm,40.mm], [-19.mm,2086.8806818181815.mm,40.mm], [-19.mm,2088.8806818181815.mm,40.mm], [-21.mm,2088.8806818181815.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2100.3011363636365.mm,40.mm], [-31.mm,2100.3011363636365.mm,40.mm], [-31.mm,2102.3011363636365.mm,40.mm], [-33.mm,2102.3011363636365.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2100.3011363636365.mm,40.mm], [-19.mm,2100.3011363636365.mm,40.mm], [-19.mm,2102.3011363636365.mm,40.mm], [-21.mm,2102.3011363636365.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2113.721590909091.mm,40.mm], [-31.mm,2113.721590909091.mm,40.mm], [-31.mm,2115.721590909091.mm,40.mm], [-33.mm,2115.721590909091.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2113.721590909091.mm,40.mm], [-19.mm,2113.721590909091.mm,40.mm], [-19.mm,2115.721590909091.mm,40.mm], [-21.mm,2115.721590909091.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2127.1420454545455.mm,40.mm], [-31.mm,2127.1420454545455.mm,40.mm], [-31.mm,2129.1420454545455.mm,40.mm], [-33.mm,2129.1420454545455.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2127.1420454545455.mm,40.mm], [-19.mm,2127.1420454545455.mm,40.mm], [-19.mm,2129.1420454545455.mm,40.mm], [-21.mm,2129.1420454545455.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2140.5625.mm,40.mm], [-31.mm,2140.5625.mm,40.mm], [-31.mm,2142.5625.mm,40.mm], [-33.mm,2142.5625.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2140.5625.mm,40.mm], [-19.mm,2140.5625.mm,40.mm], [-19.mm,2142.5625.mm,40.mm], [-21.mm,2142.5625.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2153.9829545454545.mm,40.mm], [-31.mm,2153.9829545454545.mm,40.mm], [-31.mm,2155.9829545454545.mm,40.mm], [-33.mm,2155.9829545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2153.9829545454545.mm,40.mm], [-19.mm,2153.9829545454545.mm,40.mm], [-19.mm,2155.9829545454545.mm,40.mm], [-21.mm,2155.9829545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2167.403409090909.mm,40.mm], [-31.mm,2167.403409090909.mm,40.mm], [-31.mm,2169.403409090909.mm,40.mm], [-33.mm,2169.403409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2167.403409090909.mm,40.mm], [-19.mm,2167.403409090909.mm,40.mm], [-19.mm,2169.403409090909.mm,40.mm], [-21.mm,2169.403409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2180.8238636363635.mm,40.mm], [-31.mm,2180.8238636363635.mm,40.mm], [-31.mm,2182.8238636363635.mm,40.mm], [-33.mm,2182.8238636363635.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2180.8238636363635.mm,40.mm], [-19.mm,2180.8238636363635.mm,40.mm], [-19.mm,2182.8238636363635.mm,40.mm], [-21.mm,2182.8238636363635.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2194.244318181818.mm,40.mm], [-31.mm,2194.244318181818.mm,40.mm], [-31.mm,2196.244318181818.mm,40.mm], [-33.mm,2196.244318181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2194.244318181818.mm,40.mm], [-19.mm,2194.244318181818.mm,40.mm], [-19.mm,2196.244318181818.mm,40.mm], [-21.mm,2196.244318181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2207.6647727272725.mm,40.mm], [-31.mm,2207.6647727272725.mm,40.mm], [-31.mm,2209.6647727272725.mm,40.mm], [-33.mm,2209.6647727272725.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2207.6647727272725.mm,40.mm], [-19.mm,2207.6647727272725.mm,40.mm], [-19.mm,2209.6647727272725.mm,40.mm], [-21.mm,2209.6647727272725.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2221.085227272727.mm,40.mm], [-31.mm,2221.085227272727.mm,40.mm], [-31.mm,2223.085227272727.mm,40.mm], [-33.mm,2223.085227272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2221.085227272727.mm,40.mm], [-19.mm,2221.085227272727.mm,40.mm], [-19.mm,2223.085227272727.mm,40.mm], [-21.mm,2223.085227272727.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2234.5056818181815.mm,40.mm], [-31.mm,2234.5056818181815.mm,40.mm], [-31.mm,2236.5056818181815.mm,40.mm], [-33.mm,2236.5056818181815.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2234.5056818181815.mm,40.mm], [-19.mm,2234.5056818181815.mm,40.mm], [-19.mm,2236.5056818181815.mm,40.mm], [-21.mm,2236.5056818181815.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2247.9261363636365.mm,40.mm], [-31.mm,2247.9261363636365.mm,40.mm], [-31.mm,2249.9261363636365.mm,40.mm], [-33.mm,2249.9261363636365.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2247.9261363636365.mm,40.mm], [-19.mm,2247.9261363636365.mm,40.mm], [-19.mm,2249.9261363636365.mm,40.mm], [-21.mm,2249.9261363636365.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2261.346590909091.mm,40.mm], [-31.mm,2261.346590909091.mm,40.mm], [-31.mm,2263.346590909091.mm,40.mm], [-33.mm,2263.346590909091.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2261.346590909091.mm,40.mm], [-19.mm,2261.346590909091.mm,40.mm], [-19.mm,2263.346590909091.mm,40.mm], [-21.mm,2263.346590909091.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2274.7670454545455.mm,40.mm], [-31.mm,2274.7670454545455.mm,40.mm], [-31.mm,2276.7670454545455.mm,40.mm], [-33.mm,2276.7670454545455.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2274.7670454545455.mm,40.mm], [-19.mm,2274.7670454545455.mm,40.mm], [-19.mm,2276.7670454545455.mm,40.mm], [-21.mm,2276.7670454545455.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2288.1875.mm,40.mm], [-31.mm,2288.1875.mm,40.mm], [-31.mm,2290.1875.mm,40.mm], [-33.mm,2290.1875.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2288.1875.mm,40.mm], [-19.mm,2288.1875.mm,40.mm], [-19.mm,2290.1875.mm,40.mm], [-21.mm,2290.1875.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2301.6079545454545.mm,40.mm], [-31.mm,2301.6079545454545.mm,40.mm], [-31.mm,2303.6079545454545.mm,40.mm], [-33.mm,2303.6079545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2301.6079545454545.mm,40.mm], [-19.mm,2301.6079545454545.mm,40.mm], [-19.mm,2303.6079545454545.mm,40.mm], [-21.mm,2303.6079545454545.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2315.028409090909.mm,40.mm], [-31.mm,2315.028409090909.mm,40.mm], [-31.mm,2317.028409090909.mm,40.mm], [-33.mm,2317.028409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2315.028409090909.mm,40.mm], [-19.mm,2315.028409090909.mm,40.mm], [-19.mm,2317.028409090909.mm,40.mm], [-21.mm,2317.028409090909.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2328.4488636363635.mm,40.mm], [-31.mm,2328.4488636363635.mm,40.mm], [-31.mm,2330.4488636363635.mm,40.mm], [-33.mm,2330.4488636363635.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2328.4488636363635.mm,40.mm], [-19.mm,2328.4488636363635.mm,40.mm], [-19.mm,2330.4488636363635.mm,40.mm], [-21.mm,2330.4488636363635.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2341.869318181818.mm,40.mm], [-31.mm,2341.869318181818.mm,40.mm], [-31.mm,2343.869318181818.mm,40.mm], [-33.mm,2343.869318181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2341.869318181818.mm,40.mm], [-19.mm,2341.869318181818.mm,40.mm], [-19.mm,2343.869318181818.mm,40.mm], [-21.mm,2343.869318181818.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2355.2897727272725.mm,40.mm], [-31.mm,2355.2897727272725.mm,40.mm], [-31.mm,2357.2897727272725.mm,40.mm], [-33.mm,2357.2897727272725.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2355.2897727272725.mm,40.mm], [-19.mm,2355.2897727272725.mm,40.mm], [-19.mm,2357.2897727272725.mm,40.mm], [-21.mm,2357.2897727272725.mm,40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame top brush seal
  grp = ents.add_group
  grp.name = "Door Frame top brush seal"
  face = grp.entities.add_face([-32.mm,0.mm,2270.mm], [-20.mm,0.mm,2270.mm], [-20.mm,2362.mm,2270.mm], [-32.mm,2362.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(118.mm)
  mat = model.materials["Door Frame bottom brush seal"] || model.materials.add("Door Frame bottom brush seal")
  mat.color = Sketchup::Color.new(47, 168, 79)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,6.7102272727272725.mm,2270.mm], [-31.mm,6.7102272727272725.mm,2270.mm], [-31.mm,8.710227272727273.mm,2270.mm], [-33.mm,8.710227272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,6.7102272727272725.mm,2270.mm], [-19.mm,6.7102272727272725.mm,2270.mm], [-19.mm,8.710227272727273.mm,2270.mm], [-21.mm,8.710227272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,20.130681818181817.mm,2270.mm], [-31.mm,20.130681818181817.mm,2270.mm], [-31.mm,22.130681818181817.mm,2270.mm], [-33.mm,22.130681818181817.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,20.130681818181817.mm,2270.mm], [-19.mm,20.130681818181817.mm,2270.mm], [-19.mm,22.130681818181817.mm,2270.mm], [-21.mm,22.130681818181817.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,33.55113636363636.mm,2270.mm], [-31.mm,33.55113636363636.mm,2270.mm], [-31.mm,35.55113636363636.mm,2270.mm], [-33.mm,35.55113636363636.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,33.55113636363636.mm,2270.mm], [-19.mm,33.55113636363636.mm,2270.mm], [-19.mm,35.55113636363636.mm,2270.mm], [-21.mm,35.55113636363636.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,46.97159090909091.mm,2270.mm], [-31.mm,46.97159090909091.mm,2270.mm], [-31.mm,48.97159090909091.mm,2270.mm], [-33.mm,48.97159090909091.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,46.97159090909091.mm,2270.mm], [-19.mm,46.97159090909091.mm,2270.mm], [-19.mm,48.97159090909091.mm,2270.mm], [-21.mm,48.97159090909091.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,60.39204545454545.mm,2270.mm], [-31.mm,60.39204545454545.mm,2270.mm], [-31.mm,62.39204545454545.mm,2270.mm], [-33.mm,62.39204545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,60.39204545454545.mm,2270.mm], [-19.mm,60.39204545454545.mm,2270.mm], [-19.mm,62.39204545454545.mm,2270.mm], [-21.mm,62.39204545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,73.8125.mm,2270.mm], [-31.mm,73.8125.mm,2270.mm], [-31.mm,75.8125.mm,2270.mm], [-33.mm,75.8125.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,73.8125.mm,2270.mm], [-19.mm,73.8125.mm,2270.mm], [-19.mm,75.8125.mm,2270.mm], [-21.mm,75.8125.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,87.23295454545455.mm,2270.mm], [-31.mm,87.23295454545455.mm,2270.mm], [-31.mm,89.23295454545455.mm,2270.mm], [-33.mm,89.23295454545455.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,87.23295454545455.mm,2270.mm], [-19.mm,87.23295454545455.mm,2270.mm], [-19.mm,89.23295454545455.mm,2270.mm], [-21.mm,89.23295454545455.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,100.6534090909091.mm,2270.mm], [-31.mm,100.6534090909091.mm,2270.mm], [-31.mm,102.6534090909091.mm,2270.mm], [-33.mm,102.6534090909091.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,100.6534090909091.mm,2270.mm], [-19.mm,100.6534090909091.mm,2270.mm], [-19.mm,102.6534090909091.mm,2270.mm], [-21.mm,102.6534090909091.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,114.07386363636363.mm,2270.mm], [-31.mm,114.07386363636363.mm,2270.mm], [-31.mm,116.07386363636363.mm,2270.mm], [-33.mm,116.07386363636363.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,114.07386363636363.mm,2270.mm], [-19.mm,114.07386363636363.mm,2270.mm], [-19.mm,116.07386363636363.mm,2270.mm], [-21.mm,116.07386363636363.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,127.49431818181817.mm,2270.mm], [-31.mm,127.49431818181817.mm,2270.mm], [-31.mm,129.4943181818182.mm,2270.mm], [-33.mm,129.4943181818182.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,127.49431818181817.mm,2270.mm], [-19.mm,127.49431818181817.mm,2270.mm], [-19.mm,129.4943181818182.mm,2270.mm], [-21.mm,129.4943181818182.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,140.91477272727272.mm,2270.mm], [-31.mm,140.91477272727272.mm,2270.mm], [-31.mm,142.91477272727272.mm,2270.mm], [-33.mm,142.91477272727272.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,140.91477272727272.mm,2270.mm], [-19.mm,140.91477272727272.mm,2270.mm], [-19.mm,142.91477272727272.mm,2270.mm], [-21.mm,142.91477272727272.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,154.33522727272728.mm,2270.mm], [-31.mm,154.33522727272728.mm,2270.mm], [-31.mm,156.33522727272728.mm,2270.mm], [-33.mm,156.33522727272728.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,154.33522727272728.mm,2270.mm], [-19.mm,154.33522727272728.mm,2270.mm], [-19.mm,156.33522727272728.mm,2270.mm], [-21.mm,156.33522727272728.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,167.7556818181818.mm,2270.mm], [-31.mm,167.7556818181818.mm,2270.mm], [-31.mm,169.7556818181818.mm,2270.mm], [-33.mm,169.7556818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,167.7556818181818.mm,2270.mm], [-19.mm,167.7556818181818.mm,2270.mm], [-19.mm,169.7556818181818.mm,2270.mm], [-21.mm,169.7556818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,181.17613636363635.mm,2270.mm], [-31.mm,181.17613636363635.mm,2270.mm], [-31.mm,183.17613636363635.mm,2270.mm], [-33.mm,183.17613636363635.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,181.17613636363635.mm,2270.mm], [-19.mm,181.17613636363635.mm,2270.mm], [-19.mm,183.17613636363635.mm,2270.mm], [-21.mm,183.17613636363635.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,194.5965909090909.mm,2270.mm], [-31.mm,194.5965909090909.mm,2270.mm], [-31.mm,196.5965909090909.mm,2270.mm], [-33.mm,196.5965909090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,194.5965909090909.mm,2270.mm], [-19.mm,194.5965909090909.mm,2270.mm], [-19.mm,196.5965909090909.mm,2270.mm], [-21.mm,196.5965909090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,208.01704545454544.mm,2270.mm], [-31.mm,208.01704545454544.mm,2270.mm], [-31.mm,210.01704545454544.mm,2270.mm], [-33.mm,210.01704545454544.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,208.01704545454544.mm,2270.mm], [-19.mm,208.01704545454544.mm,2270.mm], [-19.mm,210.01704545454544.mm,2270.mm], [-21.mm,210.01704545454544.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,221.4375.mm,2270.mm], [-31.mm,221.4375.mm,2270.mm], [-31.mm,223.4375.mm,2270.mm], [-33.mm,223.4375.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,221.4375.mm,2270.mm], [-19.mm,221.4375.mm,2270.mm], [-19.mm,223.4375.mm,2270.mm], [-21.mm,223.4375.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,234.85795454545453.mm,2270.mm], [-31.mm,234.85795454545453.mm,2270.mm], [-31.mm,236.85795454545453.mm,2270.mm], [-33.mm,236.85795454545453.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,234.85795454545453.mm,2270.mm], [-19.mm,234.85795454545453.mm,2270.mm], [-19.mm,236.85795454545453.mm,2270.mm], [-21.mm,236.85795454545453.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,248.2784090909091.mm,2270.mm], [-31.mm,248.2784090909091.mm,2270.mm], [-31.mm,250.2784090909091.mm,2270.mm], [-33.mm,250.2784090909091.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,248.2784090909091.mm,2270.mm], [-19.mm,248.2784090909091.mm,2270.mm], [-19.mm,250.2784090909091.mm,2270.mm], [-21.mm,250.2784090909091.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,261.6988636363636.mm,2270.mm], [-31.mm,261.6988636363636.mm,2270.mm], [-31.mm,263.6988636363636.mm,2270.mm], [-33.mm,263.6988636363636.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,261.6988636363636.mm,2270.mm], [-19.mm,261.6988636363636.mm,2270.mm], [-19.mm,263.6988636363636.mm,2270.mm], [-21.mm,263.6988636363636.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,275.1193181818182.mm,2270.mm], [-31.mm,275.1193181818182.mm,2270.mm], [-31.mm,277.1193181818182.mm,2270.mm], [-33.mm,277.1193181818182.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,275.1193181818182.mm,2270.mm], [-19.mm,275.1193181818182.mm,2270.mm], [-19.mm,277.1193181818182.mm,2270.mm], [-21.mm,277.1193181818182.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,288.5397727272727.mm,2270.mm], [-31.mm,288.5397727272727.mm,2270.mm], [-31.mm,290.5397727272727.mm,2270.mm], [-33.mm,290.5397727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,288.5397727272727.mm,2270.mm], [-19.mm,288.5397727272727.mm,2270.mm], [-19.mm,290.5397727272727.mm,2270.mm], [-21.mm,290.5397727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,301.96022727272725.mm,2270.mm], [-31.mm,301.96022727272725.mm,2270.mm], [-31.mm,303.96022727272725.mm,2270.mm], [-33.mm,303.96022727272725.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,301.96022727272725.mm,2270.mm], [-19.mm,301.96022727272725.mm,2270.mm], [-19.mm,303.96022727272725.mm,2270.mm], [-21.mm,303.96022727272725.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,315.3806818181818.mm,2270.mm], [-31.mm,315.3806818181818.mm,2270.mm], [-31.mm,317.3806818181818.mm,2270.mm], [-33.mm,317.3806818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,315.3806818181818.mm,2270.mm], [-19.mm,315.3806818181818.mm,2270.mm], [-19.mm,317.3806818181818.mm,2270.mm], [-21.mm,317.3806818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,328.8011363636364.mm,2270.mm], [-31.mm,328.8011363636364.mm,2270.mm], [-31.mm,330.8011363636364.mm,2270.mm], [-33.mm,330.8011363636364.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,328.8011363636364.mm,2270.mm], [-19.mm,328.8011363636364.mm,2270.mm], [-19.mm,330.8011363636364.mm,2270.mm], [-21.mm,330.8011363636364.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,342.2215909090909.mm,2270.mm], [-31.mm,342.2215909090909.mm,2270.mm], [-31.mm,344.2215909090909.mm,2270.mm], [-33.mm,344.2215909090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,342.2215909090909.mm,2270.mm], [-19.mm,342.2215909090909.mm,2270.mm], [-19.mm,344.2215909090909.mm,2270.mm], [-21.mm,344.2215909090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,355.64204545454544.mm,2270.mm], [-31.mm,355.64204545454544.mm,2270.mm], [-31.mm,357.64204545454544.mm,2270.mm], [-33.mm,357.64204545454544.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,355.64204545454544.mm,2270.mm], [-19.mm,355.64204545454544.mm,2270.mm], [-19.mm,357.64204545454544.mm,2270.mm], [-21.mm,357.64204545454544.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,369.0625.mm,2270.mm], [-31.mm,369.0625.mm,2270.mm], [-31.mm,371.0625.mm,2270.mm], [-33.mm,371.0625.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,369.0625.mm,2270.mm], [-19.mm,369.0625.mm,2270.mm], [-19.mm,371.0625.mm,2270.mm], [-21.mm,371.0625.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,382.4829545454545.mm,2270.mm], [-31.mm,382.4829545454545.mm,2270.mm], [-31.mm,384.4829545454545.mm,2270.mm], [-33.mm,384.4829545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,382.4829545454545.mm,2270.mm], [-19.mm,382.4829545454545.mm,2270.mm], [-19.mm,384.4829545454545.mm,2270.mm], [-21.mm,384.4829545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,395.90340909090907.mm,2270.mm], [-31.mm,395.90340909090907.mm,2270.mm], [-31.mm,397.90340909090907.mm,2270.mm], [-33.mm,397.90340909090907.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,395.90340909090907.mm,2270.mm], [-19.mm,395.90340909090907.mm,2270.mm], [-19.mm,397.90340909090907.mm,2270.mm], [-21.mm,397.90340909090907.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,409.3238636363636.mm,2270.mm], [-31.mm,409.3238636363636.mm,2270.mm], [-31.mm,411.3238636363636.mm,2270.mm], [-33.mm,411.3238636363636.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,409.3238636363636.mm,2270.mm], [-19.mm,409.3238636363636.mm,2270.mm], [-19.mm,411.3238636363636.mm,2270.mm], [-21.mm,411.3238636363636.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,422.7443181818182.mm,2270.mm], [-31.mm,422.7443181818182.mm,2270.mm], [-31.mm,424.7443181818182.mm,2270.mm], [-33.mm,424.7443181818182.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,422.7443181818182.mm,2270.mm], [-19.mm,422.7443181818182.mm,2270.mm], [-19.mm,424.7443181818182.mm,2270.mm], [-21.mm,424.7443181818182.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,436.1647727272727.mm,2270.mm], [-31.mm,436.1647727272727.mm,2270.mm], [-31.mm,438.1647727272727.mm,2270.mm], [-33.mm,438.1647727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,436.1647727272727.mm,2270.mm], [-19.mm,436.1647727272727.mm,2270.mm], [-19.mm,438.1647727272727.mm,2270.mm], [-21.mm,438.1647727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,449.58522727272725.mm,2270.mm], [-31.mm,449.58522727272725.mm,2270.mm], [-31.mm,451.58522727272725.mm,2270.mm], [-33.mm,451.58522727272725.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,449.58522727272725.mm,2270.mm], [-19.mm,449.58522727272725.mm,2270.mm], [-19.mm,451.58522727272725.mm,2270.mm], [-21.mm,451.58522727272725.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,463.0056818181818.mm,2270.mm], [-31.mm,463.0056818181818.mm,2270.mm], [-31.mm,465.0056818181818.mm,2270.mm], [-33.mm,465.0056818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,463.0056818181818.mm,2270.mm], [-19.mm,463.0056818181818.mm,2270.mm], [-19.mm,465.0056818181818.mm,2270.mm], [-21.mm,465.0056818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,476.4261363636364.mm,2270.mm], [-31.mm,476.4261363636364.mm,2270.mm], [-31.mm,478.4261363636364.mm,2270.mm], [-33.mm,478.4261363636364.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,476.4261363636364.mm,2270.mm], [-19.mm,476.4261363636364.mm,2270.mm], [-19.mm,478.4261363636364.mm,2270.mm], [-21.mm,478.4261363636364.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,489.8465909090909.mm,2270.mm], [-31.mm,489.8465909090909.mm,2270.mm], [-31.mm,491.8465909090909.mm,2270.mm], [-33.mm,491.8465909090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,489.8465909090909.mm,2270.mm], [-19.mm,489.8465909090909.mm,2270.mm], [-19.mm,491.8465909090909.mm,2270.mm], [-21.mm,491.8465909090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,503.26704545454544.mm,2270.mm], [-31.mm,503.26704545454544.mm,2270.mm], [-31.mm,505.26704545454544.mm,2270.mm], [-33.mm,505.26704545454544.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,503.26704545454544.mm,2270.mm], [-19.mm,503.26704545454544.mm,2270.mm], [-19.mm,505.26704545454544.mm,2270.mm], [-21.mm,505.26704545454544.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,516.6875.mm,2270.mm], [-31.mm,516.6875.mm,2270.mm], [-31.mm,518.6875.mm,2270.mm], [-33.mm,518.6875.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,516.6875.mm,2270.mm], [-19.mm,516.6875.mm,2270.mm], [-19.mm,518.6875.mm,2270.mm], [-21.mm,518.6875.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,530.1079545454545.mm,2270.mm], [-31.mm,530.1079545454545.mm,2270.mm], [-31.mm,532.1079545454545.mm,2270.mm], [-33.mm,532.1079545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,530.1079545454545.mm,2270.mm], [-19.mm,530.1079545454545.mm,2270.mm], [-19.mm,532.1079545454545.mm,2270.mm], [-21.mm,532.1079545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,543.5284090909091.mm,2270.mm], [-31.mm,543.5284090909091.mm,2270.mm], [-31.mm,545.5284090909091.mm,2270.mm], [-33.mm,545.5284090909091.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,543.5284090909091.mm,2270.mm], [-19.mm,543.5284090909091.mm,2270.mm], [-19.mm,545.5284090909091.mm,2270.mm], [-21.mm,545.5284090909091.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,556.9488636363636.mm,2270.mm], [-31.mm,556.9488636363636.mm,2270.mm], [-31.mm,558.9488636363636.mm,2270.mm], [-33.mm,558.9488636363636.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,556.9488636363636.mm,2270.mm], [-19.mm,556.9488636363636.mm,2270.mm], [-19.mm,558.9488636363636.mm,2270.mm], [-21.mm,558.9488636363636.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,570.3693181818181.mm,2270.mm], [-31.mm,570.3693181818181.mm,2270.mm], [-31.mm,572.3693181818181.mm,2270.mm], [-33.mm,572.3693181818181.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,570.3693181818181.mm,2270.mm], [-19.mm,570.3693181818181.mm,2270.mm], [-19.mm,572.3693181818181.mm,2270.mm], [-21.mm,572.3693181818181.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,583.7897727272727.mm,2270.mm], [-31.mm,583.7897727272727.mm,2270.mm], [-31.mm,585.7897727272727.mm,2270.mm], [-33.mm,585.7897727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,583.7897727272727.mm,2270.mm], [-19.mm,583.7897727272727.mm,2270.mm], [-19.mm,585.7897727272727.mm,2270.mm], [-21.mm,585.7897727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,597.2102272727273.mm,2270.mm], [-31.mm,597.2102272727273.mm,2270.mm], [-31.mm,599.2102272727273.mm,2270.mm], [-33.mm,599.2102272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,597.2102272727273.mm,2270.mm], [-19.mm,597.2102272727273.mm,2270.mm], [-19.mm,599.2102272727273.mm,2270.mm], [-21.mm,599.2102272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,610.6306818181818.mm,2270.mm], [-31.mm,610.6306818181818.mm,2270.mm], [-31.mm,612.6306818181818.mm,2270.mm], [-33.mm,612.6306818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,610.6306818181818.mm,2270.mm], [-19.mm,610.6306818181818.mm,2270.mm], [-19.mm,612.6306818181818.mm,2270.mm], [-21.mm,612.6306818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,624.0511363636364.mm,2270.mm], [-31.mm,624.0511363636364.mm,2270.mm], [-31.mm,626.0511363636364.mm,2270.mm], [-33.mm,626.0511363636364.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,624.0511363636364.mm,2270.mm], [-19.mm,624.0511363636364.mm,2270.mm], [-19.mm,626.0511363636364.mm,2270.mm], [-21.mm,626.0511363636364.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,637.4715909090909.mm,2270.mm], [-31.mm,637.4715909090909.mm,2270.mm], [-31.mm,639.4715909090909.mm,2270.mm], [-33.mm,639.4715909090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,637.4715909090909.mm,2270.mm], [-19.mm,637.4715909090909.mm,2270.mm], [-19.mm,639.4715909090909.mm,2270.mm], [-21.mm,639.4715909090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,650.8920454545454.mm,2270.mm], [-31.mm,650.8920454545454.mm,2270.mm], [-31.mm,652.8920454545454.mm,2270.mm], [-33.mm,652.8920454545454.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,650.8920454545454.mm,2270.mm], [-19.mm,650.8920454545454.mm,2270.mm], [-19.mm,652.8920454545454.mm,2270.mm], [-21.mm,652.8920454545454.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,664.3125.mm,2270.mm], [-31.mm,664.3125.mm,2270.mm], [-31.mm,666.3125.mm,2270.mm], [-33.mm,666.3125.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,664.3125.mm,2270.mm], [-19.mm,664.3125.mm,2270.mm], [-19.mm,666.3125.mm,2270.mm], [-21.mm,666.3125.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,677.7329545454545.mm,2270.mm], [-31.mm,677.7329545454545.mm,2270.mm], [-31.mm,679.7329545454545.mm,2270.mm], [-33.mm,679.7329545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,677.7329545454545.mm,2270.mm], [-19.mm,677.7329545454545.mm,2270.mm], [-19.mm,679.7329545454545.mm,2270.mm], [-21.mm,679.7329545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,691.1534090909091.mm,2270.mm], [-31.mm,691.1534090909091.mm,2270.mm], [-31.mm,693.1534090909091.mm,2270.mm], [-33.mm,693.1534090909091.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,691.1534090909091.mm,2270.mm], [-19.mm,691.1534090909091.mm,2270.mm], [-19.mm,693.1534090909091.mm,2270.mm], [-21.mm,693.1534090909091.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,704.5738636363636.mm,2270.mm], [-31.mm,704.5738636363636.mm,2270.mm], [-31.mm,706.5738636363636.mm,2270.mm], [-33.mm,706.5738636363636.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,704.5738636363636.mm,2270.mm], [-19.mm,704.5738636363636.mm,2270.mm], [-19.mm,706.5738636363636.mm,2270.mm], [-21.mm,706.5738636363636.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,717.9943181818181.mm,2270.mm], [-31.mm,717.9943181818181.mm,2270.mm], [-31.mm,719.9943181818181.mm,2270.mm], [-33.mm,719.9943181818181.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,717.9943181818181.mm,2270.mm], [-19.mm,717.9943181818181.mm,2270.mm], [-19.mm,719.9943181818181.mm,2270.mm], [-21.mm,719.9943181818181.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,731.4147727272727.mm,2270.mm], [-31.mm,731.4147727272727.mm,2270.mm], [-31.mm,733.4147727272727.mm,2270.mm], [-33.mm,733.4147727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,731.4147727272727.mm,2270.mm], [-19.mm,731.4147727272727.mm,2270.mm], [-19.mm,733.4147727272727.mm,2270.mm], [-21.mm,733.4147727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,744.8352272727273.mm,2270.mm], [-31.mm,744.8352272727273.mm,2270.mm], [-31.mm,746.8352272727273.mm,2270.mm], [-33.mm,746.8352272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,744.8352272727273.mm,2270.mm], [-19.mm,744.8352272727273.mm,2270.mm], [-19.mm,746.8352272727273.mm,2270.mm], [-21.mm,746.8352272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,758.2556818181818.mm,2270.mm], [-31.mm,758.2556818181818.mm,2270.mm], [-31.mm,760.2556818181818.mm,2270.mm], [-33.mm,760.2556818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,758.2556818181818.mm,2270.mm], [-19.mm,758.2556818181818.mm,2270.mm], [-19.mm,760.2556818181818.mm,2270.mm], [-21.mm,760.2556818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,771.6761363636364.mm,2270.mm], [-31.mm,771.6761363636364.mm,2270.mm], [-31.mm,773.6761363636364.mm,2270.mm], [-33.mm,773.6761363636364.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,771.6761363636364.mm,2270.mm], [-19.mm,771.6761363636364.mm,2270.mm], [-19.mm,773.6761363636364.mm,2270.mm], [-21.mm,773.6761363636364.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,785.0965909090909.mm,2270.mm], [-31.mm,785.0965909090909.mm,2270.mm], [-31.mm,787.0965909090909.mm,2270.mm], [-33.mm,787.0965909090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,785.0965909090909.mm,2270.mm], [-19.mm,785.0965909090909.mm,2270.mm], [-19.mm,787.0965909090909.mm,2270.mm], [-21.mm,787.0965909090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,798.5170454545454.mm,2270.mm], [-31.mm,798.5170454545454.mm,2270.mm], [-31.mm,800.5170454545454.mm,2270.mm], [-33.mm,800.5170454545454.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,798.5170454545454.mm,2270.mm], [-19.mm,798.5170454545454.mm,2270.mm], [-19.mm,800.5170454545454.mm,2270.mm], [-21.mm,800.5170454545454.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,811.9375.mm,2270.mm], [-31.mm,811.9375.mm,2270.mm], [-31.mm,813.9375.mm,2270.mm], [-33.mm,813.9375.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,811.9375.mm,2270.mm], [-19.mm,811.9375.mm,2270.mm], [-19.mm,813.9375.mm,2270.mm], [-21.mm,813.9375.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,825.3579545454545.mm,2270.mm], [-31.mm,825.3579545454545.mm,2270.mm], [-31.mm,827.3579545454545.mm,2270.mm], [-33.mm,827.3579545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,825.3579545454545.mm,2270.mm], [-19.mm,825.3579545454545.mm,2270.mm], [-19.mm,827.3579545454545.mm,2270.mm], [-21.mm,827.3579545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,838.778409090909.mm,2270.mm], [-31.mm,838.778409090909.mm,2270.mm], [-31.mm,840.778409090909.mm,2270.mm], [-33.mm,840.778409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,838.778409090909.mm,2270.mm], [-19.mm,838.778409090909.mm,2270.mm], [-19.mm,840.778409090909.mm,2270.mm], [-21.mm,840.778409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,852.1988636363636.mm,2270.mm], [-31.mm,852.1988636363636.mm,2270.mm], [-31.mm,854.1988636363636.mm,2270.mm], [-33.mm,854.1988636363636.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,852.1988636363636.mm,2270.mm], [-19.mm,852.1988636363636.mm,2270.mm], [-19.mm,854.1988636363636.mm,2270.mm], [-21.mm,854.1988636363636.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,865.6193181818181.mm,2270.mm], [-31.mm,865.6193181818181.mm,2270.mm], [-31.mm,867.6193181818181.mm,2270.mm], [-33.mm,867.6193181818181.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,865.6193181818181.mm,2270.mm], [-19.mm,865.6193181818181.mm,2270.mm], [-19.mm,867.6193181818181.mm,2270.mm], [-21.mm,867.6193181818181.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,879.0397727272727.mm,2270.mm], [-31.mm,879.0397727272727.mm,2270.mm], [-31.mm,881.0397727272727.mm,2270.mm], [-33.mm,881.0397727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,879.0397727272727.mm,2270.mm], [-19.mm,879.0397727272727.mm,2270.mm], [-19.mm,881.0397727272727.mm,2270.mm], [-21.mm,881.0397727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,892.4602272727273.mm,2270.mm], [-31.mm,892.4602272727273.mm,2270.mm], [-31.mm,894.4602272727273.mm,2270.mm], [-33.mm,894.4602272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,892.4602272727273.mm,2270.mm], [-19.mm,892.4602272727273.mm,2270.mm], [-19.mm,894.4602272727273.mm,2270.mm], [-21.mm,894.4602272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,905.8806818181818.mm,2270.mm], [-31.mm,905.8806818181818.mm,2270.mm], [-31.mm,907.8806818181818.mm,2270.mm], [-33.mm,907.8806818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,905.8806818181818.mm,2270.mm], [-19.mm,905.8806818181818.mm,2270.mm], [-19.mm,907.8806818181818.mm,2270.mm], [-21.mm,907.8806818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,919.3011363636364.mm,2270.mm], [-31.mm,919.3011363636364.mm,2270.mm], [-31.mm,921.3011363636364.mm,2270.mm], [-33.mm,921.3011363636364.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,919.3011363636364.mm,2270.mm], [-19.mm,919.3011363636364.mm,2270.mm], [-19.mm,921.3011363636364.mm,2270.mm], [-21.mm,921.3011363636364.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,932.7215909090909.mm,2270.mm], [-31.mm,932.7215909090909.mm,2270.mm], [-31.mm,934.7215909090909.mm,2270.mm], [-33.mm,934.7215909090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,932.7215909090909.mm,2270.mm], [-19.mm,932.7215909090909.mm,2270.mm], [-19.mm,934.7215909090909.mm,2270.mm], [-21.mm,934.7215909090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,946.1420454545454.mm,2270.mm], [-31.mm,946.1420454545454.mm,2270.mm], [-31.mm,948.1420454545454.mm,2270.mm], [-33.mm,948.1420454545454.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,946.1420454545454.mm,2270.mm], [-19.mm,946.1420454545454.mm,2270.mm], [-19.mm,948.1420454545454.mm,2270.mm], [-21.mm,948.1420454545454.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,959.5625.mm,2270.mm], [-31.mm,959.5625.mm,2270.mm], [-31.mm,961.5625.mm,2270.mm], [-33.mm,961.5625.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,959.5625.mm,2270.mm], [-19.mm,959.5625.mm,2270.mm], [-19.mm,961.5625.mm,2270.mm], [-21.mm,961.5625.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,972.9829545454545.mm,2270.mm], [-31.mm,972.9829545454545.mm,2270.mm], [-31.mm,974.9829545454545.mm,2270.mm], [-33.mm,974.9829545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,972.9829545454545.mm,2270.mm], [-19.mm,972.9829545454545.mm,2270.mm], [-19.mm,974.9829545454545.mm,2270.mm], [-21.mm,974.9829545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,986.403409090909.mm,2270.mm], [-31.mm,986.403409090909.mm,2270.mm], [-31.mm,988.403409090909.mm,2270.mm], [-33.mm,988.403409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,986.403409090909.mm,2270.mm], [-19.mm,986.403409090909.mm,2270.mm], [-19.mm,988.403409090909.mm,2270.mm], [-21.mm,988.403409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,999.8238636363636.mm,2270.mm], [-31.mm,999.8238636363636.mm,2270.mm], [-31.mm,1001.8238636363636.mm,2270.mm], [-33.mm,1001.8238636363636.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,999.8238636363636.mm,2270.mm], [-19.mm,999.8238636363636.mm,2270.mm], [-19.mm,1001.8238636363636.mm,2270.mm], [-21.mm,1001.8238636363636.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1013.2443181818181.mm,2270.mm], [-31.mm,1013.2443181818181.mm,2270.mm], [-31.mm,1015.2443181818181.mm,2270.mm], [-33.mm,1015.2443181818181.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1013.2443181818181.mm,2270.mm], [-19.mm,1013.2443181818181.mm,2270.mm], [-19.mm,1015.2443181818181.mm,2270.mm], [-21.mm,1015.2443181818181.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1026.6647727272727.mm,2270.mm], [-31.mm,1026.6647727272727.mm,2270.mm], [-31.mm,1028.6647727272727.mm,2270.mm], [-33.mm,1028.6647727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1026.6647727272727.mm,2270.mm], [-19.mm,1026.6647727272727.mm,2270.mm], [-19.mm,1028.6647727272727.mm,2270.mm], [-21.mm,1028.6647727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1040.0852272727273.mm,2270.mm], [-31.mm,1040.0852272727273.mm,2270.mm], [-31.mm,1042.0852272727273.mm,2270.mm], [-33.mm,1042.0852272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1040.0852272727273.mm,2270.mm], [-19.mm,1040.0852272727273.mm,2270.mm], [-19.mm,1042.0852272727273.mm,2270.mm], [-21.mm,1042.0852272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1053.5056818181818.mm,2270.mm], [-31.mm,1053.5056818181818.mm,2270.mm], [-31.mm,1055.5056818181818.mm,2270.mm], [-33.mm,1055.5056818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1053.5056818181818.mm,2270.mm], [-19.mm,1053.5056818181818.mm,2270.mm], [-19.mm,1055.5056818181818.mm,2270.mm], [-21.mm,1055.5056818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1066.9261363636363.mm,2270.mm], [-31.mm,1066.9261363636363.mm,2270.mm], [-31.mm,1068.9261363636363.mm,2270.mm], [-33.mm,1068.9261363636363.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1066.9261363636363.mm,2270.mm], [-19.mm,1066.9261363636363.mm,2270.mm], [-19.mm,1068.9261363636363.mm,2270.mm], [-21.mm,1068.9261363636363.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1080.3465909090908.mm,2270.mm], [-31.mm,1080.3465909090908.mm,2270.mm], [-31.mm,1082.3465909090908.mm,2270.mm], [-33.mm,1082.3465909090908.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1080.3465909090908.mm,2270.mm], [-19.mm,1080.3465909090908.mm,2270.mm], [-19.mm,1082.3465909090908.mm,2270.mm], [-21.mm,1082.3465909090908.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1093.7670454545455.mm,2270.mm], [-31.mm,1093.7670454545455.mm,2270.mm], [-31.mm,1095.7670454545455.mm,2270.mm], [-33.mm,1095.7670454545455.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1093.7670454545455.mm,2270.mm], [-19.mm,1093.7670454545455.mm,2270.mm], [-19.mm,1095.7670454545455.mm,2270.mm], [-21.mm,1095.7670454545455.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1107.1875.mm,2270.mm], [-31.mm,1107.1875.mm,2270.mm], [-31.mm,1109.1875.mm,2270.mm], [-33.mm,1109.1875.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1107.1875.mm,2270.mm], [-19.mm,1107.1875.mm,2270.mm], [-19.mm,1109.1875.mm,2270.mm], [-21.mm,1109.1875.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1120.6079545454545.mm,2270.mm], [-31.mm,1120.6079545454545.mm,2270.mm], [-31.mm,1122.6079545454545.mm,2270.mm], [-33.mm,1122.6079545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1120.6079545454545.mm,2270.mm], [-19.mm,1120.6079545454545.mm,2270.mm], [-19.mm,1122.6079545454545.mm,2270.mm], [-21.mm,1122.6079545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1134.028409090909.mm,2270.mm], [-31.mm,1134.028409090909.mm,2270.mm], [-31.mm,1136.028409090909.mm,2270.mm], [-33.mm,1136.028409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1134.028409090909.mm,2270.mm], [-19.mm,1134.028409090909.mm,2270.mm], [-19.mm,1136.028409090909.mm,2270.mm], [-21.mm,1136.028409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1147.4488636363635.mm,2270.mm], [-31.mm,1147.4488636363635.mm,2270.mm], [-31.mm,1149.4488636363635.mm,2270.mm], [-33.mm,1149.4488636363635.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1147.4488636363635.mm,2270.mm], [-19.mm,1147.4488636363635.mm,2270.mm], [-19.mm,1149.4488636363635.mm,2270.mm], [-21.mm,1149.4488636363635.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1160.8693181818182.mm,2270.mm], [-31.mm,1160.8693181818182.mm,2270.mm], [-31.mm,1162.8693181818182.mm,2270.mm], [-33.mm,1162.8693181818182.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1160.8693181818182.mm,2270.mm], [-19.mm,1160.8693181818182.mm,2270.mm], [-19.mm,1162.8693181818182.mm,2270.mm], [-21.mm,1162.8693181818182.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1174.2897727272727.mm,2270.mm], [-31.mm,1174.2897727272727.mm,2270.mm], [-31.mm,1176.2897727272727.mm,2270.mm], [-33.mm,1176.2897727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1174.2897727272727.mm,2270.mm], [-19.mm,1174.2897727272727.mm,2270.mm], [-19.mm,1176.2897727272727.mm,2270.mm], [-21.mm,1176.2897727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1187.7102272727273.mm,2270.mm], [-31.mm,1187.7102272727273.mm,2270.mm], [-31.mm,1189.7102272727273.mm,2270.mm], [-33.mm,1189.7102272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1187.7102272727273.mm,2270.mm], [-19.mm,1187.7102272727273.mm,2270.mm], [-19.mm,1189.7102272727273.mm,2270.mm], [-21.mm,1189.7102272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1201.1306818181818.mm,2270.mm], [-31.mm,1201.1306818181818.mm,2270.mm], [-31.mm,1203.1306818181818.mm,2270.mm], [-33.mm,1203.1306818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1201.1306818181818.mm,2270.mm], [-19.mm,1201.1306818181818.mm,2270.mm], [-19.mm,1203.1306818181818.mm,2270.mm], [-21.mm,1203.1306818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1214.5511363636363.mm,2270.mm], [-31.mm,1214.5511363636363.mm,2270.mm], [-31.mm,1216.5511363636363.mm,2270.mm], [-33.mm,1216.5511363636363.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1214.5511363636363.mm,2270.mm], [-19.mm,1214.5511363636363.mm,2270.mm], [-19.mm,1216.5511363636363.mm,2270.mm], [-21.mm,1216.5511363636363.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1227.9715909090908.mm,2270.mm], [-31.mm,1227.9715909090908.mm,2270.mm], [-31.mm,1229.9715909090908.mm,2270.mm], [-33.mm,1229.9715909090908.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1227.9715909090908.mm,2270.mm], [-19.mm,1227.9715909090908.mm,2270.mm], [-19.mm,1229.9715909090908.mm,2270.mm], [-21.mm,1229.9715909090908.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1241.3920454545455.mm,2270.mm], [-31.mm,1241.3920454545455.mm,2270.mm], [-31.mm,1243.3920454545455.mm,2270.mm], [-33.mm,1243.3920454545455.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1241.3920454545455.mm,2270.mm], [-19.mm,1241.3920454545455.mm,2270.mm], [-19.mm,1243.3920454545455.mm,2270.mm], [-21.mm,1243.3920454545455.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1254.8125.mm,2270.mm], [-31.mm,1254.8125.mm,2270.mm], [-31.mm,1256.8125.mm,2270.mm], [-33.mm,1256.8125.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1254.8125.mm,2270.mm], [-19.mm,1254.8125.mm,2270.mm], [-19.mm,1256.8125.mm,2270.mm], [-21.mm,1256.8125.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1268.2329545454545.mm,2270.mm], [-31.mm,1268.2329545454545.mm,2270.mm], [-31.mm,1270.2329545454545.mm,2270.mm], [-33.mm,1270.2329545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1268.2329545454545.mm,2270.mm], [-19.mm,1268.2329545454545.mm,2270.mm], [-19.mm,1270.2329545454545.mm,2270.mm], [-21.mm,1270.2329545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1281.653409090909.mm,2270.mm], [-31.mm,1281.653409090909.mm,2270.mm], [-31.mm,1283.653409090909.mm,2270.mm], [-33.mm,1283.653409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1281.653409090909.mm,2270.mm], [-19.mm,1281.653409090909.mm,2270.mm], [-19.mm,1283.653409090909.mm,2270.mm], [-21.mm,1283.653409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1295.0738636363635.mm,2270.mm], [-31.mm,1295.0738636363635.mm,2270.mm], [-31.mm,1297.0738636363635.mm,2270.mm], [-33.mm,1297.0738636363635.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1295.0738636363635.mm,2270.mm], [-19.mm,1295.0738636363635.mm,2270.mm], [-19.mm,1297.0738636363635.mm,2270.mm], [-21.mm,1297.0738636363635.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1308.4943181818182.mm,2270.mm], [-31.mm,1308.4943181818182.mm,2270.mm], [-31.mm,1310.4943181818182.mm,2270.mm], [-33.mm,1310.4943181818182.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1308.4943181818182.mm,2270.mm], [-19.mm,1308.4943181818182.mm,2270.mm], [-19.mm,1310.4943181818182.mm,2270.mm], [-21.mm,1310.4943181818182.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1321.9147727272727.mm,2270.mm], [-31.mm,1321.9147727272727.mm,2270.mm], [-31.mm,1323.9147727272727.mm,2270.mm], [-33.mm,1323.9147727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1321.9147727272727.mm,2270.mm], [-19.mm,1321.9147727272727.mm,2270.mm], [-19.mm,1323.9147727272727.mm,2270.mm], [-21.mm,1323.9147727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1335.3352272727273.mm,2270.mm], [-31.mm,1335.3352272727273.mm,2270.mm], [-31.mm,1337.3352272727273.mm,2270.mm], [-33.mm,1337.3352272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1335.3352272727273.mm,2270.mm], [-19.mm,1335.3352272727273.mm,2270.mm], [-19.mm,1337.3352272727273.mm,2270.mm], [-21.mm,1337.3352272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1348.7556818181818.mm,2270.mm], [-31.mm,1348.7556818181818.mm,2270.mm], [-31.mm,1350.7556818181818.mm,2270.mm], [-33.mm,1350.7556818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1348.7556818181818.mm,2270.mm], [-19.mm,1348.7556818181818.mm,2270.mm], [-19.mm,1350.7556818181818.mm,2270.mm], [-21.mm,1350.7556818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1362.1761363636363.mm,2270.mm], [-31.mm,1362.1761363636363.mm,2270.mm], [-31.mm,1364.1761363636363.mm,2270.mm], [-33.mm,1364.1761363636363.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1362.1761363636363.mm,2270.mm], [-19.mm,1362.1761363636363.mm,2270.mm], [-19.mm,1364.1761363636363.mm,2270.mm], [-21.mm,1364.1761363636363.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1375.5965909090908.mm,2270.mm], [-31.mm,1375.5965909090908.mm,2270.mm], [-31.mm,1377.5965909090908.mm,2270.mm], [-33.mm,1377.5965909090908.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1375.5965909090908.mm,2270.mm], [-19.mm,1375.5965909090908.mm,2270.mm], [-19.mm,1377.5965909090908.mm,2270.mm], [-21.mm,1377.5965909090908.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1389.0170454545455.mm,2270.mm], [-31.mm,1389.0170454545455.mm,2270.mm], [-31.mm,1391.0170454545455.mm,2270.mm], [-33.mm,1391.0170454545455.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1389.0170454545455.mm,2270.mm], [-19.mm,1389.0170454545455.mm,2270.mm], [-19.mm,1391.0170454545455.mm,2270.mm], [-21.mm,1391.0170454545455.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1402.4375.mm,2270.mm], [-31.mm,1402.4375.mm,2270.mm], [-31.mm,1404.4375.mm,2270.mm], [-33.mm,1404.4375.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1402.4375.mm,2270.mm], [-19.mm,1402.4375.mm,2270.mm], [-19.mm,1404.4375.mm,2270.mm], [-21.mm,1404.4375.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1415.8579545454545.mm,2270.mm], [-31.mm,1415.8579545454545.mm,2270.mm], [-31.mm,1417.8579545454545.mm,2270.mm], [-33.mm,1417.8579545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1415.8579545454545.mm,2270.mm], [-19.mm,1415.8579545454545.mm,2270.mm], [-19.mm,1417.8579545454545.mm,2270.mm], [-21.mm,1417.8579545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1429.278409090909.mm,2270.mm], [-31.mm,1429.278409090909.mm,2270.mm], [-31.mm,1431.278409090909.mm,2270.mm], [-33.mm,1431.278409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1429.278409090909.mm,2270.mm], [-19.mm,1429.278409090909.mm,2270.mm], [-19.mm,1431.278409090909.mm,2270.mm], [-21.mm,1431.278409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1442.6988636363635.mm,2270.mm], [-31.mm,1442.6988636363635.mm,2270.mm], [-31.mm,1444.6988636363635.mm,2270.mm], [-33.mm,1444.6988636363635.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1442.6988636363635.mm,2270.mm], [-19.mm,1442.6988636363635.mm,2270.mm], [-19.mm,1444.6988636363635.mm,2270.mm], [-21.mm,1444.6988636363635.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1456.119318181818.mm,2270.mm], [-31.mm,1456.119318181818.mm,2270.mm], [-31.mm,1458.119318181818.mm,2270.mm], [-33.mm,1458.119318181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1456.119318181818.mm,2270.mm], [-19.mm,1456.119318181818.mm,2270.mm], [-19.mm,1458.119318181818.mm,2270.mm], [-21.mm,1458.119318181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1469.5397727272727.mm,2270.mm], [-31.mm,1469.5397727272727.mm,2270.mm], [-31.mm,1471.5397727272727.mm,2270.mm], [-33.mm,1471.5397727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1469.5397727272727.mm,2270.mm], [-19.mm,1469.5397727272727.mm,2270.mm], [-19.mm,1471.5397727272727.mm,2270.mm], [-21.mm,1471.5397727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1482.9602272727273.mm,2270.mm], [-31.mm,1482.9602272727273.mm,2270.mm], [-31.mm,1484.9602272727273.mm,2270.mm], [-33.mm,1484.9602272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1482.9602272727273.mm,2270.mm], [-19.mm,1482.9602272727273.mm,2270.mm], [-19.mm,1484.9602272727273.mm,2270.mm], [-21.mm,1484.9602272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1496.3806818181818.mm,2270.mm], [-31.mm,1496.3806818181818.mm,2270.mm], [-31.mm,1498.3806818181818.mm,2270.mm], [-33.mm,1498.3806818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1496.3806818181818.mm,2270.mm], [-19.mm,1496.3806818181818.mm,2270.mm], [-19.mm,1498.3806818181818.mm,2270.mm], [-21.mm,1498.3806818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1509.8011363636363.mm,2270.mm], [-31.mm,1509.8011363636363.mm,2270.mm], [-31.mm,1511.8011363636363.mm,2270.mm], [-33.mm,1511.8011363636363.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1509.8011363636363.mm,2270.mm], [-19.mm,1509.8011363636363.mm,2270.mm], [-19.mm,1511.8011363636363.mm,2270.mm], [-21.mm,1511.8011363636363.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1523.2215909090908.mm,2270.mm], [-31.mm,1523.2215909090908.mm,2270.mm], [-31.mm,1525.2215909090908.mm,2270.mm], [-33.mm,1525.2215909090908.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1523.2215909090908.mm,2270.mm], [-19.mm,1523.2215909090908.mm,2270.mm], [-19.mm,1525.2215909090908.mm,2270.mm], [-21.mm,1525.2215909090908.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1536.6420454545455.mm,2270.mm], [-31.mm,1536.6420454545455.mm,2270.mm], [-31.mm,1538.6420454545455.mm,2270.mm], [-33.mm,1538.6420454545455.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1536.6420454545455.mm,2270.mm], [-19.mm,1536.6420454545455.mm,2270.mm], [-19.mm,1538.6420454545455.mm,2270.mm], [-21.mm,1538.6420454545455.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1550.0625.mm,2270.mm], [-31.mm,1550.0625.mm,2270.mm], [-31.mm,1552.0625.mm,2270.mm], [-33.mm,1552.0625.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1550.0625.mm,2270.mm], [-19.mm,1550.0625.mm,2270.mm], [-19.mm,1552.0625.mm,2270.mm], [-21.mm,1552.0625.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1563.4829545454545.mm,2270.mm], [-31.mm,1563.4829545454545.mm,2270.mm], [-31.mm,1565.4829545454545.mm,2270.mm], [-33.mm,1565.4829545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1563.4829545454545.mm,2270.mm], [-19.mm,1563.4829545454545.mm,2270.mm], [-19.mm,1565.4829545454545.mm,2270.mm], [-21.mm,1565.4829545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1576.903409090909.mm,2270.mm], [-31.mm,1576.903409090909.mm,2270.mm], [-31.mm,1578.903409090909.mm,2270.mm], [-33.mm,1578.903409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1576.903409090909.mm,2270.mm], [-19.mm,1576.903409090909.mm,2270.mm], [-19.mm,1578.903409090909.mm,2270.mm], [-21.mm,1578.903409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1590.3238636363635.mm,2270.mm], [-31.mm,1590.3238636363635.mm,2270.mm], [-31.mm,1592.3238636363635.mm,2270.mm], [-33.mm,1592.3238636363635.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1590.3238636363635.mm,2270.mm], [-19.mm,1590.3238636363635.mm,2270.mm], [-19.mm,1592.3238636363635.mm,2270.mm], [-21.mm,1592.3238636363635.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1603.744318181818.mm,2270.mm], [-31.mm,1603.744318181818.mm,2270.mm], [-31.mm,1605.744318181818.mm,2270.mm], [-33.mm,1605.744318181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1603.744318181818.mm,2270.mm], [-19.mm,1603.744318181818.mm,2270.mm], [-19.mm,1605.744318181818.mm,2270.mm], [-21.mm,1605.744318181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1617.1647727272727.mm,2270.mm], [-31.mm,1617.1647727272727.mm,2270.mm], [-31.mm,1619.1647727272727.mm,2270.mm], [-33.mm,1619.1647727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1617.1647727272727.mm,2270.mm], [-19.mm,1617.1647727272727.mm,2270.mm], [-19.mm,1619.1647727272727.mm,2270.mm], [-21.mm,1619.1647727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1630.5852272727273.mm,2270.mm], [-31.mm,1630.5852272727273.mm,2270.mm], [-31.mm,1632.5852272727273.mm,2270.mm], [-33.mm,1632.5852272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1630.5852272727273.mm,2270.mm], [-19.mm,1630.5852272727273.mm,2270.mm], [-19.mm,1632.5852272727273.mm,2270.mm], [-21.mm,1632.5852272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1644.0056818181818.mm,2270.mm], [-31.mm,1644.0056818181818.mm,2270.mm], [-31.mm,1646.0056818181818.mm,2270.mm], [-33.mm,1646.0056818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1644.0056818181818.mm,2270.mm], [-19.mm,1644.0056818181818.mm,2270.mm], [-19.mm,1646.0056818181818.mm,2270.mm], [-21.mm,1646.0056818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1657.4261363636363.mm,2270.mm], [-31.mm,1657.4261363636363.mm,2270.mm], [-31.mm,1659.4261363636363.mm,2270.mm], [-33.mm,1659.4261363636363.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1657.4261363636363.mm,2270.mm], [-19.mm,1657.4261363636363.mm,2270.mm], [-19.mm,1659.4261363636363.mm,2270.mm], [-21.mm,1659.4261363636363.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1670.8465909090908.mm,2270.mm], [-31.mm,1670.8465909090908.mm,2270.mm], [-31.mm,1672.8465909090908.mm,2270.mm], [-33.mm,1672.8465909090908.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1670.8465909090908.mm,2270.mm], [-19.mm,1670.8465909090908.mm,2270.mm], [-19.mm,1672.8465909090908.mm,2270.mm], [-21.mm,1672.8465909090908.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1684.2670454545455.mm,2270.mm], [-31.mm,1684.2670454545455.mm,2270.mm], [-31.mm,1686.2670454545455.mm,2270.mm], [-33.mm,1686.2670454545455.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1684.2670454545455.mm,2270.mm], [-19.mm,1684.2670454545455.mm,2270.mm], [-19.mm,1686.2670454545455.mm,2270.mm], [-21.mm,1686.2670454545455.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1697.6875.mm,2270.mm], [-31.mm,1697.6875.mm,2270.mm], [-31.mm,1699.6875.mm,2270.mm], [-33.mm,1699.6875.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1697.6875.mm,2270.mm], [-19.mm,1697.6875.mm,2270.mm], [-19.mm,1699.6875.mm,2270.mm], [-21.mm,1699.6875.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1711.1079545454545.mm,2270.mm], [-31.mm,1711.1079545454545.mm,2270.mm], [-31.mm,1713.1079545454545.mm,2270.mm], [-33.mm,1713.1079545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1711.1079545454545.mm,2270.mm], [-19.mm,1711.1079545454545.mm,2270.mm], [-19.mm,1713.1079545454545.mm,2270.mm], [-21.mm,1713.1079545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1724.528409090909.mm,2270.mm], [-31.mm,1724.528409090909.mm,2270.mm], [-31.mm,1726.528409090909.mm,2270.mm], [-33.mm,1726.528409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1724.528409090909.mm,2270.mm], [-19.mm,1724.528409090909.mm,2270.mm], [-19.mm,1726.528409090909.mm,2270.mm], [-21.mm,1726.528409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1737.9488636363635.mm,2270.mm], [-31.mm,1737.9488636363635.mm,2270.mm], [-31.mm,1739.9488636363635.mm,2270.mm], [-33.mm,1739.9488636363635.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1737.9488636363635.mm,2270.mm], [-19.mm,1737.9488636363635.mm,2270.mm], [-19.mm,1739.9488636363635.mm,2270.mm], [-21.mm,1739.9488636363635.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1751.369318181818.mm,2270.mm], [-31.mm,1751.369318181818.mm,2270.mm], [-31.mm,1753.369318181818.mm,2270.mm], [-33.mm,1753.369318181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1751.369318181818.mm,2270.mm], [-19.mm,1751.369318181818.mm,2270.mm], [-19.mm,1753.369318181818.mm,2270.mm], [-21.mm,1753.369318181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1764.7897727272727.mm,2270.mm], [-31.mm,1764.7897727272727.mm,2270.mm], [-31.mm,1766.7897727272727.mm,2270.mm], [-33.mm,1766.7897727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1764.7897727272727.mm,2270.mm], [-19.mm,1764.7897727272727.mm,2270.mm], [-19.mm,1766.7897727272727.mm,2270.mm], [-21.mm,1766.7897727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1778.2102272727273.mm,2270.mm], [-31.mm,1778.2102272727273.mm,2270.mm], [-31.mm,1780.2102272727273.mm,2270.mm], [-33.mm,1780.2102272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1778.2102272727273.mm,2270.mm], [-19.mm,1778.2102272727273.mm,2270.mm], [-19.mm,1780.2102272727273.mm,2270.mm], [-21.mm,1780.2102272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1791.6306818181818.mm,2270.mm], [-31.mm,1791.6306818181818.mm,2270.mm], [-31.mm,1793.6306818181818.mm,2270.mm], [-33.mm,1793.6306818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1791.6306818181818.mm,2270.mm], [-19.mm,1791.6306818181818.mm,2270.mm], [-19.mm,1793.6306818181818.mm,2270.mm], [-21.mm,1793.6306818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1805.0511363636363.mm,2270.mm], [-31.mm,1805.0511363636363.mm,2270.mm], [-31.mm,1807.0511363636363.mm,2270.mm], [-33.mm,1807.0511363636363.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1805.0511363636363.mm,2270.mm], [-19.mm,1805.0511363636363.mm,2270.mm], [-19.mm,1807.0511363636363.mm,2270.mm], [-21.mm,1807.0511363636363.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1818.4715909090908.mm,2270.mm], [-31.mm,1818.4715909090908.mm,2270.mm], [-31.mm,1820.4715909090908.mm,2270.mm], [-33.mm,1820.4715909090908.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1818.4715909090908.mm,2270.mm], [-19.mm,1818.4715909090908.mm,2270.mm], [-19.mm,1820.4715909090908.mm,2270.mm], [-21.mm,1820.4715909090908.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1831.8920454545455.mm,2270.mm], [-31.mm,1831.8920454545455.mm,2270.mm], [-31.mm,1833.8920454545455.mm,2270.mm], [-33.mm,1833.8920454545455.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1831.8920454545455.mm,2270.mm], [-19.mm,1831.8920454545455.mm,2270.mm], [-19.mm,1833.8920454545455.mm,2270.mm], [-21.mm,1833.8920454545455.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1845.3125.mm,2270.mm], [-31.mm,1845.3125.mm,2270.mm], [-31.mm,1847.3125.mm,2270.mm], [-33.mm,1847.3125.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1845.3125.mm,2270.mm], [-19.mm,1845.3125.mm,2270.mm], [-19.mm,1847.3125.mm,2270.mm], [-21.mm,1847.3125.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1858.7329545454545.mm,2270.mm], [-31.mm,1858.7329545454545.mm,2270.mm], [-31.mm,1860.7329545454545.mm,2270.mm], [-33.mm,1860.7329545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1858.7329545454545.mm,2270.mm], [-19.mm,1858.7329545454545.mm,2270.mm], [-19.mm,1860.7329545454545.mm,2270.mm], [-21.mm,1860.7329545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1872.153409090909.mm,2270.mm], [-31.mm,1872.153409090909.mm,2270.mm], [-31.mm,1874.153409090909.mm,2270.mm], [-33.mm,1874.153409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1872.153409090909.mm,2270.mm], [-19.mm,1872.153409090909.mm,2270.mm], [-19.mm,1874.153409090909.mm,2270.mm], [-21.mm,1874.153409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1885.5738636363635.mm,2270.mm], [-31.mm,1885.5738636363635.mm,2270.mm], [-31.mm,1887.5738636363635.mm,2270.mm], [-33.mm,1887.5738636363635.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1885.5738636363635.mm,2270.mm], [-19.mm,1885.5738636363635.mm,2270.mm], [-19.mm,1887.5738636363635.mm,2270.mm], [-21.mm,1887.5738636363635.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1898.994318181818.mm,2270.mm], [-31.mm,1898.994318181818.mm,2270.mm], [-31.mm,1900.994318181818.mm,2270.mm], [-33.mm,1900.994318181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1898.994318181818.mm,2270.mm], [-19.mm,1898.994318181818.mm,2270.mm], [-19.mm,1900.994318181818.mm,2270.mm], [-21.mm,1900.994318181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1912.4147727272727.mm,2270.mm], [-31.mm,1912.4147727272727.mm,2270.mm], [-31.mm,1914.4147727272727.mm,2270.mm], [-33.mm,1914.4147727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1912.4147727272727.mm,2270.mm], [-19.mm,1912.4147727272727.mm,2270.mm], [-19.mm,1914.4147727272727.mm,2270.mm], [-21.mm,1914.4147727272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1925.8352272727273.mm,2270.mm], [-31.mm,1925.8352272727273.mm,2270.mm], [-31.mm,1927.8352272727273.mm,2270.mm], [-33.mm,1927.8352272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1925.8352272727273.mm,2270.mm], [-19.mm,1925.8352272727273.mm,2270.mm], [-19.mm,1927.8352272727273.mm,2270.mm], [-21.mm,1927.8352272727273.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1939.2556818181818.mm,2270.mm], [-31.mm,1939.2556818181818.mm,2270.mm], [-31.mm,1941.2556818181818.mm,2270.mm], [-33.mm,1941.2556818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1939.2556818181818.mm,2270.mm], [-19.mm,1939.2556818181818.mm,2270.mm], [-19.mm,1941.2556818181818.mm,2270.mm], [-21.mm,1941.2556818181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1952.6761363636363.mm,2270.mm], [-31.mm,1952.6761363636363.mm,2270.mm], [-31.mm,1954.6761363636363.mm,2270.mm], [-33.mm,1954.6761363636363.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1952.6761363636363.mm,2270.mm], [-19.mm,1952.6761363636363.mm,2270.mm], [-19.mm,1954.6761363636363.mm,2270.mm], [-21.mm,1954.6761363636363.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1966.0965909090908.mm,2270.mm], [-31.mm,1966.0965909090908.mm,2270.mm], [-31.mm,1968.0965909090908.mm,2270.mm], [-33.mm,1968.0965909090908.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1966.0965909090908.mm,2270.mm], [-19.mm,1966.0965909090908.mm,2270.mm], [-19.mm,1968.0965909090908.mm,2270.mm], [-21.mm,1968.0965909090908.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1979.5170454545455.mm,2270.mm], [-31.mm,1979.5170454545455.mm,2270.mm], [-31.mm,1981.5170454545455.mm,2270.mm], [-33.mm,1981.5170454545455.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1979.5170454545455.mm,2270.mm], [-19.mm,1979.5170454545455.mm,2270.mm], [-19.mm,1981.5170454545455.mm,2270.mm], [-21.mm,1981.5170454545455.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,1992.9375.mm,2270.mm], [-31.mm,1992.9375.mm,2270.mm], [-31.mm,1994.9375.mm,2270.mm], [-33.mm,1994.9375.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,1992.9375.mm,2270.mm], [-19.mm,1992.9375.mm,2270.mm], [-19.mm,1994.9375.mm,2270.mm], [-21.mm,1994.9375.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2006.3579545454545.mm,2270.mm], [-31.mm,2006.3579545454545.mm,2270.mm], [-31.mm,2008.3579545454545.mm,2270.mm], [-33.mm,2008.3579545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2006.3579545454545.mm,2270.mm], [-19.mm,2006.3579545454545.mm,2270.mm], [-19.mm,2008.3579545454545.mm,2270.mm], [-21.mm,2008.3579545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2019.778409090909.mm,2270.mm], [-31.mm,2019.778409090909.mm,2270.mm], [-31.mm,2021.778409090909.mm,2270.mm], [-33.mm,2021.778409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2019.778409090909.mm,2270.mm], [-19.mm,2019.778409090909.mm,2270.mm], [-19.mm,2021.778409090909.mm,2270.mm], [-21.mm,2021.778409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2033.1988636363635.mm,2270.mm], [-31.mm,2033.1988636363635.mm,2270.mm], [-31.mm,2035.1988636363635.mm,2270.mm], [-33.mm,2035.1988636363635.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2033.1988636363635.mm,2270.mm], [-19.mm,2033.1988636363635.mm,2270.mm], [-19.mm,2035.1988636363635.mm,2270.mm], [-21.mm,2035.1988636363635.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2046.619318181818.mm,2270.mm], [-31.mm,2046.619318181818.mm,2270.mm], [-31.mm,2048.619318181818.mm,2270.mm], [-33.mm,2048.619318181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2046.619318181818.mm,2270.mm], [-19.mm,2046.619318181818.mm,2270.mm], [-19.mm,2048.619318181818.mm,2270.mm], [-21.mm,2048.619318181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2060.0397727272725.mm,2270.mm], [-31.mm,2060.0397727272725.mm,2270.mm], [-31.mm,2062.0397727272725.mm,2270.mm], [-33.mm,2062.0397727272725.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2060.0397727272725.mm,2270.mm], [-19.mm,2060.0397727272725.mm,2270.mm], [-19.mm,2062.0397727272725.mm,2270.mm], [-21.mm,2062.0397727272725.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2073.460227272727.mm,2270.mm], [-31.mm,2073.460227272727.mm,2270.mm], [-31.mm,2075.460227272727.mm,2270.mm], [-33.mm,2075.460227272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2073.460227272727.mm,2270.mm], [-19.mm,2073.460227272727.mm,2270.mm], [-19.mm,2075.460227272727.mm,2270.mm], [-21.mm,2075.460227272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2086.8806818181815.mm,2270.mm], [-31.mm,2086.8806818181815.mm,2270.mm], [-31.mm,2088.8806818181815.mm,2270.mm], [-33.mm,2088.8806818181815.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2086.8806818181815.mm,2270.mm], [-19.mm,2086.8806818181815.mm,2270.mm], [-19.mm,2088.8806818181815.mm,2270.mm], [-21.mm,2088.8806818181815.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2100.3011363636365.mm,2270.mm], [-31.mm,2100.3011363636365.mm,2270.mm], [-31.mm,2102.3011363636365.mm,2270.mm], [-33.mm,2102.3011363636365.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2100.3011363636365.mm,2270.mm], [-19.mm,2100.3011363636365.mm,2270.mm], [-19.mm,2102.3011363636365.mm,2270.mm], [-21.mm,2102.3011363636365.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2113.721590909091.mm,2270.mm], [-31.mm,2113.721590909091.mm,2270.mm], [-31.mm,2115.721590909091.mm,2270.mm], [-33.mm,2115.721590909091.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2113.721590909091.mm,2270.mm], [-19.mm,2113.721590909091.mm,2270.mm], [-19.mm,2115.721590909091.mm,2270.mm], [-21.mm,2115.721590909091.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2127.1420454545455.mm,2270.mm], [-31.mm,2127.1420454545455.mm,2270.mm], [-31.mm,2129.1420454545455.mm,2270.mm], [-33.mm,2129.1420454545455.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2127.1420454545455.mm,2270.mm], [-19.mm,2127.1420454545455.mm,2270.mm], [-19.mm,2129.1420454545455.mm,2270.mm], [-21.mm,2129.1420454545455.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2140.5625.mm,2270.mm], [-31.mm,2140.5625.mm,2270.mm], [-31.mm,2142.5625.mm,2270.mm], [-33.mm,2142.5625.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2140.5625.mm,2270.mm], [-19.mm,2140.5625.mm,2270.mm], [-19.mm,2142.5625.mm,2270.mm], [-21.mm,2142.5625.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2153.9829545454545.mm,2270.mm], [-31.mm,2153.9829545454545.mm,2270.mm], [-31.mm,2155.9829545454545.mm,2270.mm], [-33.mm,2155.9829545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2153.9829545454545.mm,2270.mm], [-19.mm,2153.9829545454545.mm,2270.mm], [-19.mm,2155.9829545454545.mm,2270.mm], [-21.mm,2155.9829545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2167.403409090909.mm,2270.mm], [-31.mm,2167.403409090909.mm,2270.mm], [-31.mm,2169.403409090909.mm,2270.mm], [-33.mm,2169.403409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2167.403409090909.mm,2270.mm], [-19.mm,2167.403409090909.mm,2270.mm], [-19.mm,2169.403409090909.mm,2270.mm], [-21.mm,2169.403409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2180.8238636363635.mm,2270.mm], [-31.mm,2180.8238636363635.mm,2270.mm], [-31.mm,2182.8238636363635.mm,2270.mm], [-33.mm,2182.8238636363635.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2180.8238636363635.mm,2270.mm], [-19.mm,2180.8238636363635.mm,2270.mm], [-19.mm,2182.8238636363635.mm,2270.mm], [-21.mm,2182.8238636363635.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2194.244318181818.mm,2270.mm], [-31.mm,2194.244318181818.mm,2270.mm], [-31.mm,2196.244318181818.mm,2270.mm], [-33.mm,2196.244318181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2194.244318181818.mm,2270.mm], [-19.mm,2194.244318181818.mm,2270.mm], [-19.mm,2196.244318181818.mm,2270.mm], [-21.mm,2196.244318181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2207.6647727272725.mm,2270.mm], [-31.mm,2207.6647727272725.mm,2270.mm], [-31.mm,2209.6647727272725.mm,2270.mm], [-33.mm,2209.6647727272725.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2207.6647727272725.mm,2270.mm], [-19.mm,2207.6647727272725.mm,2270.mm], [-19.mm,2209.6647727272725.mm,2270.mm], [-21.mm,2209.6647727272725.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2221.085227272727.mm,2270.mm], [-31.mm,2221.085227272727.mm,2270.mm], [-31.mm,2223.085227272727.mm,2270.mm], [-33.mm,2223.085227272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2221.085227272727.mm,2270.mm], [-19.mm,2221.085227272727.mm,2270.mm], [-19.mm,2223.085227272727.mm,2270.mm], [-21.mm,2223.085227272727.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2234.5056818181815.mm,2270.mm], [-31.mm,2234.5056818181815.mm,2270.mm], [-31.mm,2236.5056818181815.mm,2270.mm], [-33.mm,2236.5056818181815.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2234.5056818181815.mm,2270.mm], [-19.mm,2234.5056818181815.mm,2270.mm], [-19.mm,2236.5056818181815.mm,2270.mm], [-21.mm,2236.5056818181815.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2247.9261363636365.mm,2270.mm], [-31.mm,2247.9261363636365.mm,2270.mm], [-31.mm,2249.9261363636365.mm,2270.mm], [-33.mm,2249.9261363636365.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2247.9261363636365.mm,2270.mm], [-19.mm,2247.9261363636365.mm,2270.mm], [-19.mm,2249.9261363636365.mm,2270.mm], [-21.mm,2249.9261363636365.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2261.346590909091.mm,2270.mm], [-31.mm,2261.346590909091.mm,2270.mm], [-31.mm,2263.346590909091.mm,2270.mm], [-33.mm,2263.346590909091.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2261.346590909091.mm,2270.mm], [-19.mm,2261.346590909091.mm,2270.mm], [-19.mm,2263.346590909091.mm,2270.mm], [-21.mm,2263.346590909091.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2274.7670454545455.mm,2270.mm], [-31.mm,2274.7670454545455.mm,2270.mm], [-31.mm,2276.7670454545455.mm,2270.mm], [-33.mm,2276.7670454545455.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2274.7670454545455.mm,2270.mm], [-19.mm,2274.7670454545455.mm,2270.mm], [-19.mm,2276.7670454545455.mm,2270.mm], [-21.mm,2276.7670454545455.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2288.1875.mm,2270.mm], [-31.mm,2288.1875.mm,2270.mm], [-31.mm,2290.1875.mm,2270.mm], [-33.mm,2290.1875.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2288.1875.mm,2270.mm], [-19.mm,2288.1875.mm,2270.mm], [-19.mm,2290.1875.mm,2270.mm], [-21.mm,2290.1875.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2301.6079545454545.mm,2270.mm], [-31.mm,2301.6079545454545.mm,2270.mm], [-31.mm,2303.6079545454545.mm,2270.mm], [-33.mm,2303.6079545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2301.6079545454545.mm,2270.mm], [-19.mm,2301.6079545454545.mm,2270.mm], [-19.mm,2303.6079545454545.mm,2270.mm], [-21.mm,2303.6079545454545.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2315.028409090909.mm,2270.mm], [-31.mm,2315.028409090909.mm,2270.mm], [-31.mm,2317.028409090909.mm,2270.mm], [-33.mm,2317.028409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2315.028409090909.mm,2270.mm], [-19.mm,2315.028409090909.mm,2270.mm], [-19.mm,2317.028409090909.mm,2270.mm], [-21.mm,2317.028409090909.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2328.4488636363635.mm,2270.mm], [-31.mm,2328.4488636363635.mm,2270.mm], [-31.mm,2330.4488636363635.mm,2270.mm], [-33.mm,2330.4488636363635.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2328.4488636363635.mm,2270.mm], [-19.mm,2328.4488636363635.mm,2270.mm], [-19.mm,2330.4488636363635.mm,2270.mm], [-21.mm,2330.4488636363635.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2341.869318181818.mm,2270.mm], [-31.mm,2341.869318181818.mm,2270.mm], [-31.mm,2343.869318181818.mm,2270.mm], [-33.mm,2343.869318181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2341.869318181818.mm,2270.mm], [-19.mm,2341.869318181818.mm,2270.mm], [-19.mm,2343.869318181818.mm,2270.mm], [-21.mm,2343.869318181818.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-33.mm,2355.2897727272725.mm,2270.mm], [-31.mm,2355.2897727272725.mm,2270.mm], [-31.mm,2357.2897727272725.mm,2270.mm], [-33.mm,2357.2897727272725.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  # Brush bristle
  grp = ents.add_group
  grp.name = "Brush bristle"
  face = grp.entities.add_face([-21.mm,2355.2897727272725.mm,2270.mm], [-19.mm,2355.2897727272725.mm,2270.mm], [-19.mm,2357.2897727272725.mm,2270.mm], [-21.mm,2357.2897727272725.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Brush bristle"] || model.materials.add("Brush bristle")
  mat.color = Sketchup::Color.new(20, 20, 20)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Fixed Door Frame"
  inst.layer = model.layers["Door Frame"]

  # ═══ Pivot Axle (Ø89 post + bearings) ═══
  defn = model.definitions.add("Pivot Axle (Ø89 post + bearings)")
  ents = defn.entities
  # Pivot post (Ø89 CHS)
  grp = ents.add_group
  grp.name = "Pivot post (Ø89 CHS)"
  ge = grp.entities
  circle = ge.add_circle([175.mm,2287.mm,0.mm], [0,0,1], 44.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2388.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
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
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
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
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
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
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Pivot Axle (Ø89 post + bearings)"
  inst.layer = model.layers["Pivot Axle"]

  # ═══ Fixed left panel ═══
  defn = model.definitions.add("Fixed left panel")
  ents = defn.entities
  # Fixed left panel (Yd0-180)
  grp = ents.add_group
  grp.name = "Fixed left panel (Yd0-180)"
  face = grp.entities.add_face([0.mm,0.mm,130.mm], [40.mm,0.mm,130.mm], [40.mm,180.mm,130.mm], [0.mm,180.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2170.mm)
  mat = model.materials["Fixed left panel (Yd0-180)"] || model.materials.add("Fixed left panel (Yd0-180)")
  mat.color = Sketchup::Color.new(200, 160, 96)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM fixed-panel top
  grp = ents.add_group
  grp.name = "EPDM fixed-panel top"
  face = grp.entities.add_face([-20.mm,0.mm,2260.mm], [0.mm,0.mm,2260.mm], [0.mm,180.mm,2260.mm], [-20.mm,180.mm,2260.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["EPDM fixed-panel top"] || model.materials.add("EPDM fixed-panel top")
  mat.color = Sketchup::Color.new(20, 83, 45)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM fixed-panel bottom
  grp = ents.add_group
  grp.name = "EPDM fixed-panel bottom"
  face = grp.entities.add_face([-20.mm,0.mm,130.mm], [0.mm,0.mm,130.mm], [0.mm,180.mm,130.mm], [-20.mm,180.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["EPDM fixed-panel top"] || model.materials.add("EPDM fixed-panel top")
  mat.color = Sketchup::Color.new(20, 83, 45)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM fixed-panel left
  grp = ents.add_group
  grp.name = "EPDM fixed-panel left"
  face = grp.entities.add_face([-20.mm,0.mm,130.mm], [0.mm,0.mm,130.mm], [0.mm,40.mm,130.mm], [-20.mm,40.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2170.mm)
  mat = model.materials["EPDM fixed-panel top"] || model.materials.add("EPDM fixed-panel top")
  mat.color = Sketchup::Color.new(20, 83, 45)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM cut seal (fixed-swing joint)
  grp = ents.add_group
  grp.name = "EPDM cut seal (fixed-swing joint)"
  face = grp.entities.add_face([0.mm,174.mm,130.mm], [40.mm,174.mm,130.mm], [40.mm,186.mm,130.mm], [0.mm,186.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2170.mm)
  mat = model.materials["EPDM fixed-panel top"] || model.materials.add("EPDM fixed-panel top")
  mat.color = Sketchup::Color.new(20, 83, 45)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Fixed left panel"
  inst.layer = model.layers["Near Leaf"]

  # ═══ Fixed far strip ═══
  defn = model.definitions.add("Fixed far strip")
  ents = defn.entities
  # Fixed far panel strip (Yd2287-2362)
  grp = ents.add_group
  grp.name = "Fixed far panel strip (Yd2287-2362)"
  face = grp.entities.add_face([0.mm,2287.mm,130.mm], [40.mm,2287.mm,130.mm], [40.mm,2362.mm,130.mm], [0.mm,2362.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2170.mm)
  mat = model.materials["Fixed left panel (Yd0-180)"] || model.materials.add("Fixed left panel (Yd0-180)")
  mat.color = Sketchup::Color.new(200, 160, 96)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM fixed-far top
  grp = ents.add_group
  grp.name = "EPDM fixed-far top"
  face = grp.entities.add_face([-20.mm,2287.mm,2260.mm], [0.mm,2287.mm,2260.mm], [0.mm,2362.mm,2260.mm], [-20.mm,2362.mm,2260.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["EPDM fixed-panel top"] || model.materials.add("EPDM fixed-panel top")
  mat.color = Sketchup::Color.new(20, 83, 45)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM fixed-far bottom
  grp = ents.add_group
  grp.name = "EPDM fixed-far bottom"
  face = grp.entities.add_face([-20.mm,2287.mm,130.mm], [0.mm,2287.mm,130.mm], [0.mm,2362.mm,130.mm], [-20.mm,2362.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["EPDM fixed-panel top"] || model.materials.add("EPDM fixed-panel top")
  mat.color = Sketchup::Color.new(20, 83, 45)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM fixed-far right (far wall)
  grp = ents.add_group
  grp.name = "EPDM fixed-far right (far wall)"
  face = grp.entities.add_face([-20.mm,2322.mm,130.mm], [0.mm,2322.mm,130.mm], [0.mm,2362.mm,130.mm], [-20.mm,2362.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2170.mm)
  mat = model.materials["EPDM fixed-panel top"] || model.materials.add("EPDM fixed-panel top")
  mat.color = Sketchup::Color.new(20, 83, 45)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM far cut seal (swing-fixed joint)
  grp = ents.add_group
  grp.name = "EPDM far cut seal (swing-fixed joint)"
  face = grp.entities.add_face([0.mm,2281.mm,130.mm], [40.mm,2281.mm,130.mm], [40.mm,2293.mm,130.mm], [0.mm,2293.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2170.mm)
  mat = model.materials["EPDM fixed-panel top"] || model.materials.add("EPDM fixed-panel top")
  mat.color = Sketchup::Color.new(20, 83, 45)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Fixed far strip"
  inst.layer = model.layers["Far Leaf"]

  # ═══ Processing Tray (partial) ═══
  defn = model.definitions.add("Processing Tray (partial)")
  ents = defn.entities
  # Tray Shim Base (partial)
  grp = ents.add_group
  grp.name = "Tray Shim Base (partial)"
  face = grp.entities.add_face([170.mm,80.mm,0.mm], [1600.mm,80.mm,0.mm], [1600.mm,2280.mm,0.mm], [170.mm,2280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.22.mm)
  mat = model.materials["Tray Shim Base (partial)"] || model.materials.add("Tray Shim Base (partial)")
  mat.color = Sketchup::Color.new(216, 208, 188)
  mat.alpha = 0.6
  grp.material = mat

  # Processing Tray Floor (partial)
  grp = ents.add_group
  grp.name = "Processing Tray Floor (partial)"
  face = grp.entities.add_face([170.mm,80.mm,42.22.mm], [1600.mm,80.mm,42.22.mm], [1600.mm,2280.mm,42.22.mm], [170.mm,2280.mm,42.22.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Processing Tray Floor (partial)"] || model.materials.add("Processing Tray Floor (partial)")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Near (partial)
  grp = ents.add_group
  grp.name = "Tray Rim Near (partial)"
  face = grp.entities.add_face([170.mm,80.mm,44.22.mm], [1600.mm,80.mm,44.22.mm], [1600.mm,82.mm,44.22.mm], [170.mm,82.mm,44.22.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Processing Tray Floor (partial)"] || model.materials.add("Processing Tray Floor (partial)")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Far (partial)
  grp = ents.add_group
  grp.name = "Tray Rim Far (partial)"
  face = grp.entities.add_face([170.mm,2278.mm,44.22.mm], [1600.mm,2278.mm,44.22.mm], [1600.mm,2280.mm,44.22.mm], [170.mm,2280.mm,44.22.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Processing Tray Floor (partial)"] || model.materials.add("Processing Tray Floor (partial)")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Left (cargo end)
  grp = ents.add_group
  grp.name = "Tray Rim Left (cargo end)"
  face = grp.entities.add_face([170.mm,80.mm,44.22.mm], [172.mm,80.mm,44.22.mm], [172.mm,2280.mm,44.22.mm], [170.mm,2280.mm,44.22.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Processing Tray Floor (partial)"] || model.materials.add("Processing Tray Floor (partial)")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Chemistry Bath (partial)
  grp = ents.add_group
  grp.name = "Chemistry Bath (partial)"
  face = grp.entities.add_face([172.mm,82.mm,44.22.mm], [1598.mm,82.mm,44.22.mm], [1598.mm,2278.mm,44.22.mm], [172.mm,2278.mm,44.22.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Chemistry Bath (partial)"] || model.materials.add("Chemistry Bath (partial)")
  mat.color = Sketchup::Color.new(46, 111, 160)
  mat.alpha = 0.45
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Processing Tray (partial)"
  inst.layer = model.layers["Processing Tray"]

  # ═══ Walkways (near + far, partial) ═══
  defn = model.definitions.add("Walkways (near + far, partial)")
  ents = defn.entities
  # Walkway Near (partial)
  grp = ents.add_group
  grp.name = "Walkway Near (partial)"
  face = grp.entities.add_face([950.mm,0.mm,115.mm], [1600.mm,0.mm,115.mm], [1600.mm,300.mm,115.mm], [950.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (partial)"] || model.materials.add("Walkway Near (partial)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far (partial)
  grp = ents.add_group
  grp.name = "Walkway Far (partial)"
  face = grp.entities.add_face([470.mm,2062.mm,115.mm], [1600.mm,2062.mm,115.mm], [1600.mm,2362.mm,115.mm], [470.mm,2362.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (partial)"] || model.materials.add("Walkway Near (partial)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Walkways (near + far, partial)"
  inst.layer = model.layers["Walkways"]

  # ═══ Film-Plane Rails (left, removable) ═══
  defn = model.definitions.add("Film-Plane Rails (left, removable)")
  ents = defn.entities
  # FP Brace Beam Lower (near wall)
  grp = ents.add_group
  grp.name = "FP Brace Beam Lower (near wall)"
  face = grp.entities.add_face([150.mm,100.mm,100.mm], [2000.mm,100.mm,100.mm], [2000.mm,150.mm,100.mm], [150.mm,150.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Brace Beam Upper (near wall)
  grp = ents.add_group
  grp.name = "FP Brace Beam Upper (near wall)"
  face = grp.entities.add_face([150.mm,100.mm,2204.mm], [2000.mm,100.mm,2204.mm], [2000.mm,150.mm,2204.mm], [150.mm,150.mm,2204.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Brace Post L (near wall)
  grp = ents.add_group
  grp.name = "FP Brace Post L (near wall)"
  face = grp.entities.add_face([150.mm,100.mm,100.mm], [200.mm,100.mm,100.mm], [200.mm,150.mm,100.mm], [150.mm,150.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2104.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Brace Beam Lower (far wall)
  grp = ents.add_group
  grp.name = "FP Brace Beam Lower (far wall)"
  face = grp.entities.add_face([150.mm,2262.mm,100.mm], [2000.mm,2262.mm,100.mm], [2000.mm,2312.mm,100.mm], [150.mm,2312.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Brace Beam Upper (far wall)
  grp = ents.add_group
  grp.name = "FP Brace Beam Upper (far wall)"
  face = grp.entities.add_face([150.mm,2262.mm,2204.mm], [2000.mm,2262.mm,2204.mm], [2000.mm,2312.mm,2204.mm], [150.mm,2312.mm,2204.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Brace Post L (far wall)
  grp = ents.add_group
  grp.name = "FP Brace Post L (far wall)"
  face = grp.entities.add_face([150.mm,2262.mm,100.mm], [200.mm,2262.mm,100.mm], [200.mm,2312.mm,100.mm], [150.mm,2312.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2104.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail saddle shelf
  grp = ents.add_group
  grp.name = "Rail saddle shelf"
  face = grp.entities.add_face([133.mm,100.mm,86.mm], [207.mm,100.mm,86.mm], [207.mm,180.mm,86.mm], [133.mm,180.mm,86.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail saddle cheek -X
  grp = ents.add_group
  grp.name = "Rail saddle cheek -X"
  face = grp.entities.add_face([133.mm,100.mm,100.mm], [145.mm,100.mm,100.mm], [145.mm,180.mm,100.mm], [133.mm,180.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(44.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail saddle cheek +X
  grp = ents.add_group
  grp.name = "Rail saddle cheek +X"
  face = grp.entities.add_face([195.mm,100.mm,100.mm], [207.mm,100.mm,100.mm], [207.mm,180.mm,100.mm], [195.mm,180.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(44.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail locating dowel (taper)
  grp = ents.add_group
  grp.name = "Rail locating dowel (taper)"
  ge = grp.entities
  circle = ge.add_circle([170.mm,140.mm,86.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(22.mm)
  mat = model.materials["Rail locating dowel (taper)"] || model.materials.add("Rail locating dowel (taper)")
  mat.color = Sketchup::Color.new(154, 154, 162)
  mat.alpha = 1.0
  grp.material = mat

  # Rail saddle shelf
  grp = ents.add_group
  grp.name = "Rail saddle shelf"
  face = grp.entities.add_face([133.mm,100.mm,2190.mm], [207.mm,100.mm,2190.mm], [207.mm,180.mm,2190.mm], [133.mm,180.mm,2190.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail saddle cheek -X
  grp = ents.add_group
  grp.name = "Rail saddle cheek -X"
  face = grp.entities.add_face([133.mm,100.mm,2204.mm], [145.mm,100.mm,2204.mm], [145.mm,180.mm,2204.mm], [133.mm,180.mm,2204.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(44.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail saddle cheek +X
  grp = ents.add_group
  grp.name = "Rail saddle cheek +X"
  face = grp.entities.add_face([195.mm,100.mm,2204.mm], [207.mm,100.mm,2204.mm], [207.mm,180.mm,2204.mm], [195.mm,180.mm,2204.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(44.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail locating dowel (taper)
  grp = ents.add_group
  grp.name = "Rail locating dowel (taper)"
  ge = grp.entities
  circle = ge.add_circle([170.mm,140.mm,2190.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(22.mm)
  mat = model.materials["Rail locating dowel (taper)"] || model.materials.add("Rail locating dowel (taper)")
  mat.color = Sketchup::Color.new(154, 154, 162)
  mat.alpha = 1.0
  grp.material = mat

  # Rail saddle shelf
  grp = ents.add_group
  grp.name = "Rail saddle shelf"
  face = grp.entities.add_face([133.mm,2182.mm,86.mm], [207.mm,2182.mm,86.mm], [207.mm,2262.mm,86.mm], [133.mm,2262.mm,86.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail saddle cheek -X
  grp = ents.add_group
  grp.name = "Rail saddle cheek -X"
  face = grp.entities.add_face([133.mm,2182.mm,100.mm], [145.mm,2182.mm,100.mm], [145.mm,2262.mm,100.mm], [133.mm,2262.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(44.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail saddle cheek +X
  grp = ents.add_group
  grp.name = "Rail saddle cheek +X"
  face = grp.entities.add_face([195.mm,2182.mm,100.mm], [207.mm,2182.mm,100.mm], [207.mm,2262.mm,100.mm], [195.mm,2262.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(44.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail locating dowel (taper)
  grp = ents.add_group
  grp.name = "Rail locating dowel (taper)"
  ge = grp.entities
  circle = ge.add_circle([170.mm,2222.mm,86.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(22.mm)
  mat = model.materials["Rail locating dowel (taper)"] || model.materials.add("Rail locating dowel (taper)")
  mat.color = Sketchup::Color.new(154, 154, 162)
  mat.alpha = 1.0
  grp.material = mat

  # Rail saddle shelf
  grp = ents.add_group
  grp.name = "Rail saddle shelf"
  face = grp.entities.add_face([133.mm,2182.mm,2190.mm], [207.mm,2182.mm,2190.mm], [207.mm,2262.mm,2190.mm], [133.mm,2262.mm,2190.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail saddle cheek -X
  grp = ents.add_group
  grp.name = "Rail saddle cheek -X"
  face = grp.entities.add_face([133.mm,2182.mm,2204.mm], [145.mm,2182.mm,2204.mm], [145.mm,2262.mm,2204.mm], [133.mm,2262.mm,2204.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(44.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail saddle cheek +X
  grp = ents.add_group
  grp.name = "Rail saddle cheek +X"
  face = grp.entities.add_face([195.mm,2182.mm,2204.mm], [207.mm,2182.mm,2204.mm], [207.mm,2262.mm,2204.mm], [195.mm,2262.mm,2204.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(44.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail locating dowel (taper)
  grp = ents.add_group
  grp.name = "Rail locating dowel (taper)"
  ge = grp.entities
  circle = ge.add_circle([170.mm,2222.mm,2190.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(22.mm)
  mat = model.materials["Rail locating dowel (taper)"] || model.materials.add("Rail locating dowel (taper)")
  mat.color = Sketchup::Color.new(154, 154, 162)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Film-Plane Rails (left, removable)"
  inst.layer = model.layers["Film Plane Rails"]

  # ═══ Transport stay wall anchors ═══
  defn = model.definitions.add("Transport stay wall anchors")
  ents = defn.entities
  # Stay inside plate
  grp = ents.add_group
  grp.name = "Stay inside plate"
  face = grp.entities.add_face([1614.mm,0.mm,400.mm], [1814.mm,0.mm,400.mm], [1814.mm,12.mm,400.mm], [1614.mm,12.mm,400.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay outside plate
  grp = ents.add_group
  grp.name = "Stay outside plate"
  face = grp.entities.add_face([1614.mm,-52.mm,400.mm], [1814.mm,-52.mm,400.mm], [1814.mm,-40.mm,400.mm], [1614.mm,-40.mm,400.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay eye
  grp = ents.add_group
  grp.name = "Stay eye"
  face = grp.entities.add_face([1699.mm,12.mm,485.mm], [1729.mm,12.mm,485.mm], [1729.mm,67.mm,485.mm], [1699.mm,67.mm,485.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1636.mm,-58.mm,422.mm], [1652.mm,-58.mm,422.mm], [1652.mm,18.mm,422.mm], [1636.mm,18.mm,422.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1636.mm,-58.mm,562.mm], [1652.mm,-58.mm,562.mm], [1652.mm,18.mm,562.mm], [1636.mm,18.mm,562.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1776.mm,-58.mm,422.mm], [1792.mm,-58.mm,422.mm], [1792.mm,18.mm,422.mm], [1776.mm,18.mm,422.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1776.mm,-58.mm,562.mm], [1792.mm,-58.mm,562.mm], [1792.mm,18.mm,562.mm], [1776.mm,18.mm,562.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay inside plate
  grp = ents.add_group
  grp.name = "Stay inside plate"
  face = grp.entities.add_face([1614.mm,0.mm,1950.mm], [1814.mm,0.mm,1950.mm], [1814.mm,12.mm,1950.mm], [1614.mm,12.mm,1950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay outside plate
  grp = ents.add_group
  grp.name = "Stay outside plate"
  face = grp.entities.add_face([1614.mm,-52.mm,1950.mm], [1814.mm,-52.mm,1950.mm], [1814.mm,-40.mm,1950.mm], [1614.mm,-40.mm,1950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay eye
  grp = ents.add_group
  grp.name = "Stay eye"
  face = grp.entities.add_face([1699.mm,12.mm,2035.mm], [1729.mm,12.mm,2035.mm], [1729.mm,67.mm,2035.mm], [1699.mm,67.mm,2035.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1636.mm,-58.mm,1972.mm], [1652.mm,-58.mm,1972.mm], [1652.mm,18.mm,1972.mm], [1636.mm,18.mm,1972.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1636.mm,-58.mm,2112.mm], [1652.mm,-58.mm,2112.mm], [1652.mm,18.mm,2112.mm], [1636.mm,18.mm,2112.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1776.mm,-58.mm,1972.mm], [1792.mm,-58.mm,1972.mm], [1792.mm,18.mm,1972.mm], [1776.mm,18.mm,1972.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1776.mm,-58.mm,2112.mm], [1792.mm,-58.mm,2112.mm], [1792.mm,18.mm,2112.mm], [1776.mm,18.mm,2112.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Transport stay wall anchors"
  inst.layer = model.layers["Lock anchor"]

  # ═══ Fan B electrical box ═══
  defn = model.definitions.add("Fan B electrical box")
  ents = defn.entities
  # Fan B electrical box (Cct B — flex connector to fan, unplugged for swing)
  grp = ents.add_group
  grp.name = "Fan B electrical box (Cct B — flex connector to fan, unplugged for swing)"
  face = grp.entities.add_face([260.mm,0.mm,555.mm], [340.mm,0.mm,555.mm], [340.mm,60.mm,555.mm], [260.mm,60.mm,555.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Fan B electrical box (Cct B — flex connector to fan, unplugged for swing)"] || model.materials.add("Fan B electrical box (Cct B — flex connector to fan, unplugged for swing)")
  mat.color = Sketchup::Color.new(216, 216, 240)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Fan B electrical box"
  inst.layer = model.layers["Fan B Cable"]


# Strike the original 50×50 far brace post — the Ø89 pivot post replaces it.
fpdef = model.definitions.to_a.find { |d| d.name =~ /Film-Plane Rails/ }
fpdef.entities.grep(Sketchup::Group).each { |g| g.erase! if g.name =~ /FP Brace Post L .far wall./ } if fpdef

# ═══ Panel Swing — DYNAMIC COMPONENT (the swinging assembly) ═══
# Interact tool → click to ANIMATE the panel 0→56° about the vertical pivot. The whole
# assembly (panel + bay + housing + drum rotor + cage + Fan B + hub) is STATIC geometry in
# this def — it all swings rigidly as one. (The old nested drum-revolve DC reset its own
# position on redraw, so the rotor is now baked into the swing assembly at the correct place.)
defn = model.definitions.add("Panel Swing")
ents = defn.entities
  # Panel near corner (40mm)
  grp = ents.add_group
  grp.name = "Panel near corner (40mm)"
  face = grp.entities.add_face([0.mm,0.mm,130.mm], [40.mm,0.mm,130.mm], [40.mm,653.mm,130.mm], [0.mm,653.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2170.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(110, 140, 160)
  mat.alpha = 0.5
  grp.material = mat

  # Panel far corner (40mm)
  grp = ents.add_group
  grp.name = "Panel far corner (40mm)"
  face = grp.entities.add_face([0.mm,1709.mm,130.mm], [40.mm,1709.mm,130.mm], [40.mm,2362.mm,130.mm], [0.mm,2362.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2170.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(110, 140, 160)
  mat.alpha = 0.5
  grp.material = mat

  # Panel center jamb L (120mm frame)
  grp = ents.add_group
  grp.name = "Panel center jamb L (120mm frame)"
  face = grp.entities.add_face([0.mm,653.mm,130.mm], [120.mm,653.mm,130.mm], [120.mm,713.mm,130.mm], [0.mm,713.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2170.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Panel center jamb R (120mm frame)
  grp = ents.add_group
  grp.name = "Panel center jamb R (120mm frame)"
  face = grp.entities.add_face([0.mm,1649.mm,130.mm], [120.mm,1649.mm,130.mm], [120.mm,1709.mm,130.mm], [0.mm,1709.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2170.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Panel header over housing (120mm frame)
  grp = ents.add_group
  grp.name = "Panel header over housing (120mm frame)"
  face = grp.entities.add_face([0.mm,653.mm,2250.mm], [120.mm,653.mm,2250.mm], [120.mm,1709.mm,2250.mm], [0.mm,1709.mm,2250.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM seal bottom L
  grp = ents.add_group
  grp.name = "EPDM seal bottom L"
  face = grp.entities.add_face([-20.mm,0.mm,130.mm], [0.mm,0.mm,130.mm], [0.mm,716.mm,130.mm], [-20.mm,716.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["EPDM seal bottom L"] || model.materials.add("EPDM seal bottom L")
  mat.color = Sketchup::Color.new(20, 83, 45)
  mat.alpha = 0.5
  grp.material = mat

  # EPDM seal bottom R
  grp = ents.add_group
  grp.name = "EPDM seal bottom R"
  face = grp.entities.add_face([-20.mm,1646.mm,130.mm], [0.mm,1646.mm,130.mm], [0.mm,2362.mm,130.mm], [-20.mm,2362.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["EPDM seal bottom L"] || model.materials.add("EPDM seal bottom L")
  mat.color = Sketchup::Color.new(20, 83, 45)
  mat.alpha = 0.5
  grp.material = mat

  # EPDM seal top
  grp = ents.add_group
  grp.name = "EPDM seal top"
  face = grp.entities.add_face([-20.mm,0.mm,2260.mm], [0.mm,0.mm,2260.mm], [0.mm,2362.mm,2260.mm], [-20.mm,2362.mm,2260.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["EPDM seal bottom L"] || model.materials.add("EPDM seal bottom L")
  mat.color = Sketchup::Color.new(20, 83, 45)
  mat.alpha = 0.5
  grp.material = mat

  # EPDM seal left
  grp = ents.add_group
  grp.name = "EPDM seal left"
  face = grp.entities.add_face([-20.mm,0.mm,130.mm], [0.mm,0.mm,130.mm], [0.mm,40.mm,130.mm], [-20.mm,40.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2170.mm)
  mat = model.materials["EPDM seal bottom L"] || model.materials.add("EPDM seal bottom L")
  mat.color = Sketchup::Color.new(20, 83, 45)
  mat.alpha = 0.5
  grp.material = mat

  # EPDM seal right
  grp = ents.add_group
  grp.name = "EPDM seal right"
  face = grp.entities.add_face([-20.mm,2322.mm,130.mm], [0.mm,2322.mm,130.mm], [0.mm,2362.mm,130.mm], [-20.mm,2362.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2170.mm)
  mat = model.materials["EPDM seal bottom L"] || model.materials.add("EPDM seal bottom L")
  mat.color = Sketchup::Color.new(20, 83, 45)
  mat.alpha = 0.5
  grp.material = mat

  # Piano hinge
  grp = ents.add_group
  grp.name = "Piano hinge"
  face = grp.entities.add_face([-30.mm,0.mm,220.mm], [30.mm,0.mm,220.mm], [30.mm,30.mm,220.mm], [-30.mm,30.mm,220.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Piano hinge
  grp = ents.add_group
  grp.name = "Piano hinge"
  face = grp.entities.add_face([-30.mm,0.mm,1190.mm], [30.mm,0.mm,1190.mm], [30.mm,30.mm,1190.mm], [-30.mm,30.mm,1190.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Piano hinge
  grp = ents.add_group
  grp.name = "Piano hinge"
  face = grp.entities.add_face([-30.mm,0.mm,2158.mm], [30.mm,0.mm,2158.mm], [30.mm,30.mm,2158.mm], [-30.mm,30.mm,2158.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Southco cam latch
  grp = ents.add_group
  grp.name = "Southco cam latch"
  face = grp.entities.add_face([40.mm,175.mm,195.mm], [95.mm,175.mm,195.mm], [95.mm,245.mm,195.mm], [40.mm,245.mm,195.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Southco cam latch"] || model.materials.add("Southco cam latch")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Southco cam latch
  grp = ents.add_group
  grp.name = "Southco cam latch"
  face = grp.entities.add_face([40.mm,175.mm,2143.mm], [95.mm,175.mm,2143.mm], [95.mm,245.mm,2143.mm], [40.mm,245.mm,2143.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Southco cam latch"] || model.materials.add("Southco cam latch")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Southco cam latch
  grp = ents.add_group
  grp.name = "Southco cam latch"
  face = grp.entities.add_face([40.mm,2117.mm,195.mm], [95.mm,2117.mm,195.mm], [95.mm,2187.mm,195.mm], [40.mm,2187.mm,195.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Southco cam latch"] || model.materials.add("Southco cam latch")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Southco cam latch
  grp = ents.add_group
  grp.name = "Southco cam latch"
  face = grp.entities.add_face([40.mm,2117.mm,2143.mm], [95.mm,2117.mm,2143.mm], [95.mm,2187.mm,2143.mm], [40.mm,2187.mm,2143.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Southco cam latch"] || model.materials.add("Southco cam latch")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Pull-handle standoff
  grp = ents.add_group
  grp.name = "Pull-handle standoff"
  face = grp.entities.add_face([120.mm,673.mm,1160.mm], [148.mm,673.mm,1160.mm], [148.mm,693.mm,1160.mm], [120.mm,693.mm,1160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Pull-handle standoff"] || model.materials.add("Pull-handle standoff")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Pull-handle standoff
  grp = ents.add_group
  grp.name = "Pull-handle standoff"
  face = grp.entities.add_face([120.mm,673.mm,1424.mm], [148.mm,673.mm,1424.mm], [148.mm,693.mm,1424.mm], [120.mm,693.mm,1424.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Pull-handle standoff"] || model.materials.add("Pull-handle standoff")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Pull-handle grip (matte black)
  grp = ents.add_group
  grp.name = "Pull-handle grip (matte black)"
  face = grp.entities.add_face([148.mm,671.mm,1150.mm], [172.mm,671.mm,1150.mm], [172.mm,695.mm,1150.mm], [148.mm,695.mm,1150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(300.mm)
  mat = model.materials["Pull-handle standoff"] || model.materials.add("Pull-handle standoff")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B mount band (18mm ply)
  grp = ents.add_group
  grp.name = "Fan B mount band (18mm ply)"
  face = grp.entities.add_face([0.mm,180.mm,130.mm], [40.mm,180.mm,130.mm], [40.mm,653.mm,130.mm], [0.mm,653.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(995.mm)
  mat = model.materials["Fan B mount band (18mm ply)"] || model.materials.add("Fan B mount band (18mm ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 0.5
  grp.material = mat

  # Panel near (swing, Yd180-653)
  grp = ents.add_group
  grp.name = "Panel near (swing, Yd180-653)"
  face = grp.entities.add_face([0.mm,180.mm,1125.mm], [40.mm,180.mm,1125.mm], [40.mm,653.mm,1125.mm], [0.mm,653.mm,1125.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1175.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(110, 140, 160)
  mat.alpha = 0.5
  grp.material = mat

  # EPDM seal top (trimmed)
  grp = ents.add_group
  grp.name = "EPDM seal top (trimmed)"
  face = grp.entities.add_face([-20.mm,180.mm,2260.mm], [0.mm,180.mm,2260.mm], [0.mm,2287.mm,2260.mm], [-20.mm,2287.mm,2260.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["EPDM seal bottom L"] || model.materials.add("EPDM seal bottom L")
  mat.color = Sketchup::Color.new(20, 83, 45)
  mat.alpha = 0.5
  grp.material = mat

  # EPDM seal bottom L (trimmed)
  grp = ents.add_group
  grp.name = "EPDM seal bottom L (trimmed)"
  face = grp.entities.add_face([-20.mm,180.mm,130.mm], [0.mm,180.mm,130.mm], [0.mm,716.mm,130.mm], [-20.mm,716.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["EPDM seal bottom L"] || model.materials.add("EPDM seal bottom L")
  mat.color = Sketchup::Color.new(20, 83, 45)
  mat.alpha = 0.5
  grp.material = mat

  # Panel far corner (trimmed)
  grp = ents.add_group
  grp.name = "Panel far corner (trimmed)"
  face = grp.entities.add_face([0.mm,1709.mm,130.mm], [40.mm,1709.mm,130.mm], [40.mm,2287.mm,130.mm], [0.mm,2287.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2170.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(110, 140, 160)
  mat.alpha = 0.5
  grp.material = mat

  # EPDM seal bottom R (trimmed)
  grp = ents.add_group
  grp.name = "EPDM seal bottom R (trimmed)"
  face = grp.entities.add_face([-20.mm,1646.mm,130.mm], [0.mm,1646.mm,130.mm], [0.mm,2287.mm,130.mm], [-20.mm,2287.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["EPDM seal bottom L"] || model.materials.add("EPDM seal bottom L")
  mat.color = Sketchup::Color.new(20, 83, 45)
  mat.alpha = 0.5
  grp.material = mat

  # Bay wall near (Yd)
  grp = ents.add_group
  grp.name = "Bay wall near (Yd)"
  face = grp.entities.add_face([-890.mm,653.mm,130.mm], [0.mm,653.mm,130.mm], [0.mm,659.mm,130.mm], [-890.mm,659.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2170.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(110, 140, 160)
  mat.alpha = 0.5
  grp.material = mat

  # Bay wall far (Yd)
  grp = ents.add_group
  grp.name = "Bay wall far (Yd)"
  face = grp.entities.add_face([-890.mm,1703.mm,130.mm], [0.mm,1703.mm,130.mm], [0.mm,1709.mm,130.mm], [-890.mm,1709.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2170.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(110, 140, 160)
  mat.alpha = 0.5
  grp.material = mat

  # Bay wall top
  grp = ents.add_group
  grp.name = "Bay wall top"
  face = grp.entities.add_face([-890.mm,653.mm,2294.mm], [0.mm,653.mm,2294.mm], [0.mm,1709.mm,2294.mm], [-890.mm,1709.mm,2294.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(110, 140, 160)
  mat.alpha = 0.5
  grp.material = mat

  # Bay wall bottom
  grp = ents.add_group
  grp.name = "Bay wall bottom"
  face = grp.entities.add_face([-890.mm,653.mm,130.mm], [0.mm,653.mm,130.mm], [0.mm,1709.mm,130.mm], [-890.mm,1709.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(110, 140, 160)
  mat.alpha = 0.5
  grp.material = mat

  # LT Housing arc (near Yd)
  grp = ents.add_group
  grp.name = "LT Housing arc (near Yd)"
  ge = grp.entities
  face = ge.add_face([[-55.28.mm,1470.25.mm,130.mm], [-66.02.mm,1482.59.mm,130.mm], [-77.21.mm,1494.54.mm,130.mm], [-88.82.mm,1506.06.mm,130.mm], [-100.84.mm,1517.16.mm,130.mm], [-113.26.mm,1527.81.mm,130.mm], [-126.06.mm,1538.01.mm,130.mm], [-139.22.mm,1547.73.mm,130.mm], [-152.72.mm,1556.97.mm,130.mm], [-166.55.mm,1565.71.mm,130.mm], [-180.69.mm,1573.94.mm,130.mm], [-195.12.mm,1581.66.mm,130.mm], [-209.82.mm,1588.84.mm,130.mm], [-224.77.mm,1595.48.mm,130.mm], [-239.96.mm,1601.58.mm,130.mm], [-255.35.mm,1607.12.mm,130.mm], [-270.94.mm,1612.1.mm,130.mm], [-286.7.mm,1616.5.mm,130.mm], [-302.6.mm,1620.33.mm,130.mm], [-318.64.mm,1623.58.mm,130.mm], [-334.78.mm,1626.25.mm,130.mm], [-351.01.mm,1628.33.mm,130.mm], [-367.3.mm,1629.81.mm,130.mm], [-383.64.mm,1630.7.mm,130.mm], [-400.mm,1631.mm,130.mm], [-416.36.mm,1630.7.mm,130.mm], [-432.7.mm,1629.81.mm,130.mm], [-448.99.mm,1628.33.mm,130.mm], [-465.22.mm,1626.25.mm,130.mm], [-481.36.mm,1623.58.mm,130.mm], [-497.4.mm,1620.33.mm,130.mm], [-513.3.mm,1616.5.mm,130.mm], [-529.06.mm,1612.1.mm,130.mm], [-544.65.mm,1607.12.mm,130.mm], [-560.04.mm,1601.58.mm,130.mm], [-575.23.mm,1595.48.mm,130.mm], [-590.18.mm,1588.84.mm,130.mm], [-604.88.mm,1581.66.mm,130.mm], [-619.31.mm,1573.94.mm,130.mm], [-633.45.mm,1565.71.mm,130.mm], [-647.28.mm,1556.97.mm,130.mm], [-660.78.mm,1547.73.mm,130.mm], [-673.94.mm,1538.01.mm,130.mm], [-686.74.mm,1527.81.mm,130.mm], [-699.16.mm,1517.16.mm,130.mm], [-711.18.mm,1506.06.mm,130.mm], [-722.79.mm,1494.54.mm,130.mm], [-733.98.mm,1482.59.mm,130.mm], [-744.72.mm,1470.25.mm,130.mm], [-740.89.mm,1467.04.mm,130.mm], [-730.27.mm,1479.24.mm,130.mm], [-719.21.mm,1491.05.mm,130.mm], [-707.72.mm,1502.45.mm,130.mm], [-695.83.mm,1513.43.mm,130.mm], [-683.55.mm,1523.96.mm,130.mm], [-670.9.mm,1534.04.mm,130.mm], [-657.89.mm,1543.66.mm,130.mm], [-644.53.mm,1552.79.mm,130.mm], [-630.85.mm,1561.44.mm,130.mm], [-616.87.mm,1569.58.mm,130.mm], [-602.6.mm,1577.2.mm,130.mm], [-588.07.mm,1584.31.mm,130.mm], [-573.28.mm,1590.88.mm,130.mm], [-558.26.mm,1596.91.mm,130.mm], [-543.04.mm,1602.38.mm,130.mm], [-527.63.mm,1607.31.mm,130.mm], [-512.05.mm,1611.66.mm,130.mm], [-496.32.mm,1615.45.mm,130.mm], [-480.46.mm,1618.67.mm,130.mm], [-464.49.mm,1621.3.mm,130.mm], [-448.45.mm,1623.36.mm,130.mm], [-432.33.mm,1624.82.mm,130.mm], [-416.18.mm,1625.71.mm,130.mm], [-400.mm,1626.mm,130.mm], [-383.82.mm,1625.71.mm,130.mm], [-367.67.mm,1624.82.mm,130.mm], [-351.55.mm,1623.36.mm,130.mm], [-335.51.mm,1621.3.mm,130.mm], [-319.54.mm,1618.67.mm,130.mm], [-303.68.mm,1615.45.mm,130.mm], [-287.95.mm,1611.66.mm,130.mm], [-272.37.mm,1607.31.mm,130.mm], [-256.96.mm,1602.38.mm,130.mm], [-241.74.mm,1596.91.mm,130.mm], [-226.72.mm,1590.88.mm,130.mm], [-211.93.mm,1584.31.mm,130.mm], [-197.4.mm,1577.2.mm,130.mm], [-183.13.mm,1569.58.mm,130.mm], [-169.15.mm,1561.44.mm,130.mm], [-155.47.mm,1552.79.mm,130.mm], [-142.11.mm,1543.66.mm,130.mm], [-129.1.mm,1534.04.mm,130.mm], [-116.45.mm,1523.96.mm,130.mm], [-104.17.mm,1513.43.mm,130.mm], [-92.28.mm,1502.45.mm,130.mm], [-80.79.mm,1491.05.mm,130.mm], [-69.73.mm,1479.24.mm,130.mm], [-59.11.mm,1467.04.mm,130.mm]])
  face.reverse! if face.normal.z < 0
  face.pushpull(2120.mm)
  mat = model.materials["LT Housing arc (near Yd)"] || model.materials.add("LT Housing arc (near Yd)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.5
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
  mat.alpha = 0.5
  grp.material = mat

  # LT Upper bearing (SKF 6215)
  grp = ents.add_group
  grp.name = "LT Upper bearing (SKF 6215)"
  ge = grp.entities
  circle = ge.add_circle([-400.mm,1181.mm,2250.mm], [0,0,1], 65.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(25.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
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
  mat = model.materials["LT Housing arc (near Yd)"] || model.materials.add("LT Housing arc (near Yd)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.5
  grp.material = mat

  # LT Drum top cap
  grp = ents.add_group
  grp.name = "LT Drum top cap"
  ge = grp.entities
  circle = ge.add_circle([-400.mm,1181.mm,2245.mm], [0,0,1], 432.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["LT Drum top cap"] || model.materials.add("LT Drum top cap")
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
  mat = model.materials["LT Drum top cap"] || model.materials.add("LT Drum top cap")
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
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
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
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Grab rail standoff
  grp = ents.add_group
  grp.name = "LT Grab rail standoff"
  face = grp.entities.add_face([-43.mm,1175.mm,720.mm], [28.mm,1175.mm,720.mm], [28.mm,1187.mm,720.mm], [-43.mm,1187.mm,720.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Grab rail standoff
  grp = ents.add_group
  grp.name = "LT Grab rail standoff"
  face = grp.entities.add_face([-43.mm,1175.mm,1080.mm], [28.mm,1175.mm,1080.mm], [28.mm,1187.mm,1080.mm], [-43.mm,1187.mm,1080.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
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
  mat = model.materials["Walkway Near (partial)"] || model.materials.add("Walkway Near (partial)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum opening brush seal
  grp = ents.add_group
  grp.name = "LT Drum opening brush seal"
  ge = grp.entities
  circle = ge.add_circle([-735.9104883076718.mm,899.1376331524525.mm,130.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2120.mm)
  mat = model.materials["Walkway Near (partial)"] || model.materials.add("Walkway Near (partial)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Drum frame rail (X near)
  grp = ents.add_group
  grp.name = "Drum frame rail (X near)"
  face = grp.entities.add_face([-890.mm,700.mm,130.mm], [50.mm,700.mm,130.mm], [50.mm,750.mm,130.mm], [-890.mm,750.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Drum frame rail (X far)
  grp = ents.add_group
  grp.name = "Drum frame rail (X far)"
  face = grp.entities.add_face([-890.mm,1612.mm,130.mm], [50.mm,1612.mm,130.mm], [50.mm,1662.mm,130.mm], [-890.mm,1662.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Drum frame rail (Yd front)
  grp = ents.add_group
  grp.name = "Drum frame rail (Yd front)"
  face = grp.entities.add_face([-890.mm,700.mm,130.mm], [-840.mm,700.mm,130.mm], [-840.mm,1662.mm,130.mm], [-890.mm,1662.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Drum frame rail (Yd back)
  grp = ents.add_group
  grp.name = "Drum frame rail (Yd back)"
  face = grp.entities.add_face([0.mm,700.mm,130.mm], [50.mm,700.mm,130.mm], [50.mm,1662.mm,130.mm], [0.mm,1662.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Drum frame rail (X near)
  grp = ents.add_group
  grp.name = "Drum frame rail (X near)"
  face = grp.entities.add_face([-890.mm,700.mm,2200.mm], [50.mm,700.mm,2200.mm], [50.mm,750.mm,2200.mm], [-890.mm,750.mm,2200.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Drum frame rail (X far)
  grp = ents.add_group
  grp.name = "Drum frame rail (X far)"
  face = grp.entities.add_face([-890.mm,1612.mm,2200.mm], [50.mm,1612.mm,2200.mm], [50.mm,1662.mm,2200.mm], [-890.mm,1662.mm,2200.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Drum frame rail (Yd front)
  grp = ents.add_group
  grp.name = "Drum frame rail (Yd front)"
  face = grp.entities.add_face([-890.mm,700.mm,2200.mm], [-840.mm,700.mm,2200.mm], [-840.mm,1662.mm,2200.mm], [-890.mm,1662.mm,2200.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Drum frame rail (Yd back)
  grp = ents.add_group
  grp.name = "Drum frame rail (Yd back)"
  face = grp.entities.add_face([0.mm,700.mm,2200.mm], [50.mm,700.mm,2200.mm], [50.mm,1662.mm,2200.mm], [0.mm,1662.mm,2200.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Drum frame post
  grp = ents.add_group
  grp.name = "Drum frame post"
  face = grp.entities.add_face([-890.mm,700.mm,130.mm], [-840.mm,700.mm,130.mm], [-840.mm,750.mm,130.mm], [-890.mm,750.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2120.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Drum frame post
  grp = ents.add_group
  grp.name = "Drum frame post"
  face = grp.entities.add_face([-890.mm,1612.mm,130.mm], [-840.mm,1612.mm,130.mm], [-840.mm,1662.mm,130.mm], [-890.mm,1662.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2120.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Drum frame post
  grp = ents.add_group
  grp.name = "Drum frame post"
  face = grp.entities.add_face([0.mm,700.mm,130.mm], [50.mm,700.mm,130.mm], [50.mm,750.mm,130.mm], [0.mm,750.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2120.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Drum frame post
  grp = ents.add_group
  grp.name = "Drum frame post"
  face = grp.entities.add_face([0.mm,1612.mm,130.mm], [50.mm,1612.mm,130.mm], [50.mm,1662.mm,130.mm], [0.mm,1662.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2120.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Drum bearing cross-beam (top)
  grp = ents.add_group
  grp.name = "Drum bearing cross-beam (top)"
  face = grp.entities.add_face([-425.mm,700.mm,2200.mm], [-375.mm,700.mm,2200.mm], [-375.mm,1662.mm,2200.mm], [-425.mm,1662.mm,2200.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Drum top radial journal (Ø120 guide)
  grp = ents.add_group
  grp.name = "Drum top radial journal (Ø120 guide)"
  ge = grp.entities
  circle = ge.add_circle([-400.mm,1181.mm,2200.mm], [0,0,1], 60.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(50.mm)
  mat = model.materials["Drum top radial journal (Ø120 guide)"] || model.materials.add("Drum top radial journal (Ø120 guide)")
  mat.color = Sketchup::Color.new(90, 90, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Drum top pivot pin
  grp = ents.add_group
  grp.name = "Drum top pivot pin"
  ge = grp.entities
  circle = ge.add_circle([-400.mm,1181.mm,2130.mm], [0,0,1], 22.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(80.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Drum bearing cross-beam (bottom, recessed)
  grp = ents.add_group
  grp.name = "Drum bearing cross-beam (bottom, recessed)"
  face = grp.entities.add_face([-425.mm,700.mm,80.mm], [-375.mm,700.mm,80.mm], [-375.mm,1662.mm,80.mm], [-425.mm,1662.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Drum bottom thrust bearing (Ø220 flush slew pad)
  grp = ents.add_group
  grp.name = "Drum bottom thrust bearing (Ø220 flush slew pad)"
  ge = grp.entities
  circle = ge.add_circle([-400.mm,1181.mm,108.mm], [0,0,1], 110.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(22.mm)
  mat = model.materials["Drum top radial journal (Ø120 guide)"] || model.materials.add("Drum top radial journal (Ø120 guide)")
  mat.color = Sketchup::Color.new(90, 90, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Drum threshold sill (flush, chamfered step-over)
  grp = ents.add_group
  grp.name = "Drum threshold sill (flush, chamfered step-over)"
  face = grp.entities.add_face([-640.mm,861.mm,122.mm], [-390.mm,861.mm,122.mm], [-390.mm,1501.mm,122.mm], [-640.mm,1501.mm,122.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Drum threshold sill (flush, chamfered step-over)"] || model.materials.add("Drum threshold sill (flush, chamfered step-over)")
  mat.color = Sketchup::Color.new(122, 122, 130)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) baffle duct
  grp = ents.add_group
  grp.name = "Fan B (intake) baffle duct"
  face = grp.entities.add_face([0.mm,265.mm,500.mm], [300.mm,265.mm,500.mm], [300.mm,465.mm,500.mm], [0.mm,465.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan B (intake) baffle duct"] || model.materials.add("Fan B (intake) baffle duct")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 0.5
  grp.material = mat

  # Fan B (intake) baffle plate 1
  grp = ents.add_group
  grp.name = "Fan B (intake) baffle plate 1"
  face = grp.entities.add_face([96.mm,265.mm,500.mm], [104.mm,265.mm,500.mm], [104.mm,390.mm,500.mm], [96.mm,390.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan B (intake) baffle plate 1"] || model.materials.add("Fan B (intake) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) baffle plate 2
  grp = ents.add_group
  grp.name = "Fan B (intake) baffle plate 2"
  face = grp.entities.add_face([196.mm,340.mm,500.mm], [204.mm,340.mm,500.mm], [204.mm,465.mm,500.mm], [196.mm,465.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan B (intake) baffle plate 1"] || model.materials.add("Fan B (intake) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan frame top
  grp = ents.add_group
  grp.name = "Fan B (intake) fan frame top"
  face = grp.entities.add_face([250.mm,265.mm,675.mm], [300.mm,265.mm,675.mm], [300.mm,465.mm,675.mm], [250.mm,465.mm,675.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Fan B (intake) baffle plate 1"] || model.materials.add("Fan B (intake) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan frame bottom
  grp = ents.add_group
  grp.name = "Fan B (intake) fan frame bottom"
  face = grp.entities.add_face([250.mm,265.mm,500.mm], [300.mm,265.mm,500.mm], [300.mm,465.mm,500.mm], [250.mm,465.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Fan B (intake) baffle plate 1"] || model.materials.add("Fan B (intake) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan frame left
  grp = ents.add_group
  grp.name = "Fan B (intake) fan frame left"
  face = grp.entities.add_face([250.mm,265.mm,525.mm], [300.mm,265.mm,525.mm], [300.mm,290.mm,525.mm], [250.mm,290.mm,525.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Fan B (intake) baffle plate 1"] || model.materials.add("Fan B (intake) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan frame right
  grp = ents.add_group
  grp.name = "Fan B (intake) fan frame right"
  face = grp.entities.add_face([250.mm,440.mm,525.mm], [300.mm,440.mm,525.mm], [300.mm,465.mm,525.mm], [250.mm,465.mm,525.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Fan B (intake) baffle plate 1"] || model.materials.add("Fan B (intake) baffle plate 1")
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
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade up
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade up"
  face = grp.entities.add_face([272.5.mm,350.mm,619.5.mm], [278.5.mm,350.mm,619.5.mm], [278.5.mm,380.mm,619.5.mm], [272.5.mm,380.mm,619.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.5.mm)
  mat = model.materials["LT Drum top cap"] || model.materials.add("LT Drum top cap")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade down
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade down"
  face = grp.entities.add_face([272.5.mm,350.mm,534.mm], [278.5.mm,350.mm,534.mm], [278.5.mm,380.mm,534.mm], [272.5.mm,380.mm,534.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.5.mm)
  mat = model.materials["LT Drum top cap"] || model.materials.add("LT Drum top cap")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade left
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade left"
  face = grp.entities.add_face([272.5.mm,299.mm,585.mm], [278.5.mm,299.mm,585.mm], [278.5.mm,345.5.mm,585.mm], [272.5.mm,345.5.mm,585.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["LT Drum top cap"] || model.materials.add("LT Drum top cap")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade right
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade right"
  face = grp.entities.add_face([272.5.mm,384.5.mm,585.mm], [278.5.mm,384.5.mm,585.mm], [278.5.mm,431.mm,585.mm], [272.5.mm,431.mm,585.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["LT Drum top cap"] || model.materials.add("LT Drum top cap")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) wall flange
  grp = ents.add_group
  grp.name = "Fan B (intake) wall flange"
  face = grp.entities.add_face([0.mm,235.mm,470.mm], [5.mm,235.mm,470.mm], [5.mm,495.mm,470.mm], [0.mm,495.mm,470.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(260.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
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
  mat = model.materials["Fan B (intake) flange bolt M10"] || model.materials.add("Fan B (intake) flange bolt M10")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["Fan B (intake) flange bolt M10"] || model.materials.add("Fan B (intake) flange bolt M10")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["Fan B (intake) flange bolt M10"] || model.materials.add("Fan B (intake) flange bolt M10")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["Fan B (intake) flange bolt M10"] || model.materials.add("Fan B (intake) flange bolt M10")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre grille
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre grille"
  face = grp.entities.add_face([-40.mm,265.mm,535.mm], [0.mm,265.mm,535.mm], [0.mm,465.mm,535.mm], [-40.mm,465.mm,535.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(130.mm)
  mat = model.materials["Fan B (intake) louvre grille"] || model.materials.add("Fan B (intake) louvre grille")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 0.55
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,269.mm,546.5.mm], [-2.mm,269.mm,546.5.mm], [-2.mm,461.mm,546.5.mm], [-38.mm,461.mm,546.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,269.mm,572.5.mm], [-2.mm,269.mm,572.5.mm], [-2.mm,461.mm,572.5.mm], [-38.mm,461.mm,572.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,269.mm,598.5.mm], [-2.mm,269.mm,598.5.mm], [-2.mm,461.mm,598.5.mm], [-38.mm,461.mm,598.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,269.mm,624.5.mm], [-2.mm,269.mm,624.5.mm], [-2.mm,461.mm,624.5.mm], [-38.mm,461.mm,624.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,269.mm,650.5.mm], [-2.mm,269.mm,650.5.mm], [-2.mm,461.mm,650.5.mm], [-38.mm,461.mm,650.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Hub tube
  grp = ents.add_group
  grp.name = "Hub tube"
  ge = grp.entities
  circle = ge.add_circle([175.mm,2287.mm,180.mm], [0,0,1], 58.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(1870.mm)
  mat = model.materials["Hub tube"] || model.materials.add("Hub tube")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.4
  grp.material = mat

  # Hub thrust bearing
  grp = ents.add_group
  grp.name = "Hub thrust bearing"
  ge = grp.entities
  circle = ge.add_circle([175.mm,2287.mm,155.mm], [0,0,1], 70.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(25.mm)
  mat = model.materials["Drum top radial journal (Ø120 guide)"] || model.materials.add("Drum top radial journal (Ø120 guide)")
  mat.color = Sketchup::Color.new(90, 90, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Hub radial bearing (bottom)
  grp = ents.add_group
  grp.name = "Hub radial bearing (bottom)"
  ge = grp.entities
  circle = ge.add_circle([175.mm,2287.mm,220.mm], [0,0,1], 60.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(55.mm)
  mat = model.materials["Drum top radial journal (Ø120 guide)"] || model.materials.add("Drum top radial journal (Ø120 guide)")
  mat.color = Sketchup::Color.new(90, 90, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Hub radial bearing (top)
  grp = ents.add_group
  grp.name = "Hub radial bearing (top)"
  ge = grp.entities
  circle = ge.add_circle([175.mm,2287.mm,2050.mm], [0,0,1], 60.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(55.mm)
  mat = model.materials["Drum top radial journal (Ø120 guide)"] || model.materials.add("Drum top radial journal (Ø120 guide)")
  mat.color = Sketchup::Color.new(90, 90, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Hinge bracket (panel→hub)
  grp = ents.add_group
  grp.name = "Hinge bracket (panel→hub)"
  face = grp.entities.add_face([55.mm,2252.mm,300.mm], [195.mm,2252.mm,300.mm], [195.mm,2322.mm,300.mm], [55.mm,2322.mm,300.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(110.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Hinge bracket (panel→hub)
  grp = ents.add_group
  grp.name = "Hinge bracket (panel→hub)"
  face = grp.entities.add_face([55.mm,2252.mm,1180.mm], [195.mm,2252.mm,1180.mm], [195.mm,2322.mm,1180.mm], [55.mm,2322.mm,1180.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(110.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Hinge bracket (panel→hub)
  grp = ents.add_group
  grp.name = "Hinge bracket (panel→hub)"
  face = grp.entities.add_face([55.mm,2252.mm,2000.mm], [195.mm,2252.mm,2000.mm], [195.mm,2322.mm,2000.mm], [55.mm,2322.mm,2000.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(110.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay hook (frame)
  grp = ents.add_group
  grp.name = "Stay hook (frame)"
  face = grp.entities.add_face([-10.mm,175.mm,465.mm], [50.mm,175.mm,465.mm], [50.mm,235.mm,465.mm], [-10.mm,235.mm,465.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay hook (frame)
  grp = ents.add_group
  grp.name = "Stay hook (frame)"
  face = grp.entities.add_face([-10.mm,175.mm,2015.mm], [50.mm,175.mm,2015.mm], [50.mm,235.mm,2015.mm], [-10.mm,235.mm,2015.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

# Trim to the 3-zone split: erase the un-split corners + full-width seals + piano hinges
# (the fixed left/far leaves + the trimmed swing seals provide the rest).
defn.entities.grep(Sketchup::Group).select { |g| g.name =~ /Panel near corner|Panel far corner .40mm.|EPDM seal left|EPDM seal right|EPDM seal bottom L$|EPDM seal bottom R$|EPDM seal top$|Piano hinge/ }.each { |g| g.erase! }

# ── Lift-out walkways — a CHILD DC component inside the swing def: HIDDEN when the panel
#    swings (lifted out for transport). Built at world coords, then shifted with the rest
#    of the def below so the instance's +pivot translate restores the world position. The
#    child's `_hidden_formula` reads the parent Panel Swing's `swing` attribute. ──
lw_defn = model.definitions.add("Lift-out Walkways")
ents = lw_defn.entities
  # Left walkway (removable)
  grp = ents.add_group
  grp.name = "Left walkway (removable)"
  face = grp.entities.add_face([170.mm,0.mm,115.mm], [470.mm,0.mm,115.mm], [470.mm,2362.mm,115.mm], [170.mm,2362.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Left walkway (removable)"] || model.materials.add("Left walkway (removable)")
  mat.color = Sketchup::Color.new(192, 96, 0)
  mat.alpha = 0.6
  grp.material = mat

  # Left walkway punch-out (removable)
  grp = ents.add_group
  grp.name = "Left walkway punch-out (removable)"
  face = grp.entities.add_face([470.mm,800.mm,115.mm], [770.mm,800.mm,115.mm], [770.mm,1560.mm,115.mm], [470.mm,1560.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Left walkway (removable)"] || model.materials.add("Left walkway (removable)")
  mat.color = Sketchup::Color.new(192, 96, 0)
  mat.alpha = 0.6
  grp.material = mat

  # Walkway Near (door-end, removable)
  grp = ents.add_group
  grp.name = "Walkway Near (door-end, removable)"
  face = grp.entities.add_face([470.mm,0.mm,115.mm], [950.mm,0.mm,115.mm], [950.mm,300.mm,115.mm], [470.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Left walkway (removable)"] || model.materials.add("Left walkway (removable)")
  mat.color = Sketchup::Color.new(192, 96, 0)
  mat.alpha = 0.6
  grp.material = mat

ents = defn.entities
lw_inst = ents.add_instance(lw_defn, Geom::Transformation.new)
lw_inst.name = "Lift-out Walkways"
lw_inst.layer = model.layers["Walkways"]
lw_inst.set_attribute("dynamic_attributes", "_name", "LiftoutWalkways")
lw_inst.set_attribute("dynamic_attributes", "hidden", 0.0)
lw_inst.set_attribute("dynamic_attributes", "_hidden_formula", "PanelSwing!swing>0.5")

# ── Transport stay rods — a CHILD DC component inside the swing def: SHOWN only when the
#    panel is swung open (the M16 turnbuckle stays are engaged AFTER the swing). Built in
#    TRANSPORT (swung) coords, then added with a -LOCK° pre-rotation about the pivot so the
#    parent's +LOCK°·swing cancels it at swing=1 → the rod lands exactly on the frame hook
#    (which also swings to SOCKET) and the static wall-anchor eye. A child, so its
#    `_hidden_formula` (ancestor ref PanelSwing!swing) re-evaluates as the panel animates. ──
sr_defn = model.definitions.add("Transport Stay Rods")
ents = sr_defn.entities
  # Stay clevis (eye end)
  grp = ents.add_group
  grp.name = "Stay clevis (eye end)"
  face = grp.entities.add_face([1702.mm,42.mm,488.mm], [1726.mm,42.mm,488.mm], [1726.mm,66.mm,488.mm], [1702.mm,66.mm,488.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay rod (eye side)
  grp = ents.add_group
  grp.name = "Stay rod (eye side)"
  ge = grp.entities
  circle = ge.add_circle([1714.mm,60.mm,500.mm], [0,1,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(406.91679805254313.mm)
  mat = model.materials["Stay rod (eye side)"] || model.materials.add("Stay rod (eye side)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Turnbuckle barrel
  grp = ents.add_group
  grp.name = "Turnbuckle barrel"
  ge = grp.entities
  circle = ge.add_circle([1714.mm,466.91679805254313.mm,500.mm], [0,1,0], 14.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(120.mm)
  mat = model.materials["Turnbuckle barrel"] || model.materials.add("Turnbuckle barrel")
  mat.color = Sketchup::Color.new(106, 106, 114)
  mat.alpha = 1.0
  grp.material = mat

  # Stay rod (hook side)
  grp = ents.add_group
  grp.name = "Stay rod (hook side)"
  ge = grp.entities
  circle = ge.add_circle([1714.mm,586.9167980525431.mm,500.mm], [0,1,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(377.3427531753305.mm)
  mat = model.materials["Stay rod (eye side)"] || model.materials.add("Stay rod (eye side)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Stay clevis (hook end)
  grp = ents.add_group
  grp.name = "Stay clevis (hook end)"
  face = grp.entities.add_face([1702.mm,964.2595512278735.mm,488.mm], [1726.mm,964.2595512278735.mm,488.mm], [1726.mm,988.2595512278735.mm,488.mm], [1702.mm,988.2595512278735.mm,488.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay clevis (eye end)
  grp = ents.add_group
  grp.name = "Stay clevis (eye end)"
  face = grp.entities.add_face([1702.mm,42.mm,2038.mm], [1726.mm,42.mm,2038.mm], [1726.mm,66.mm,2038.mm], [1702.mm,66.mm,2038.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay rod (eye side)
  grp = ents.add_group
  grp.name = "Stay rod (eye side)"
  ge = grp.entities
  circle = ge.add_circle([1714.mm,60.mm,2050.mm], [0,1,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(406.91679805254313.mm)
  mat = model.materials["Stay rod (eye side)"] || model.materials.add("Stay rod (eye side)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Turnbuckle barrel
  grp = ents.add_group
  grp.name = "Turnbuckle barrel"
  ge = grp.entities
  circle = ge.add_circle([1714.mm,466.91679805254313.mm,2050.mm], [0,1,0], 14.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(120.mm)
  mat = model.materials["Turnbuckle barrel"] || model.materials.add("Turnbuckle barrel")
  mat.color = Sketchup::Color.new(106, 106, 114)
  mat.alpha = 1.0
  grp.material = mat

  # Stay rod (hook side)
  grp = ents.add_group
  grp.name = "Stay rod (hook side)"
  ge = grp.entities
  circle = ge.add_circle([1714.mm,586.9167980525431.mm,2050.mm], [0,1,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(377.3427531753305.mm)
  mat = model.materials["Stay rod (eye side)"] || model.materials.add("Stay rod (eye side)")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Stay clevis (hook end)
  grp = ents.add_group
  grp.name = "Stay clevis (hook end)"
  face = grp.entities.add_face([1702.mm,964.2595512278735.mm,2038.mm], [1726.mm,964.2595512278735.mm,2038.mm], [1726.mm,988.2595512278735.mm,2038.mm], [1702.mm,988.2595512278735.mm,2038.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

ents = defn.entities
sr_tr = Geom::Transformation.rotation([175.mm, 2287.mm, 0], Z_AXIS, (-56).degrees)
sr_inst = ents.add_instance(sr_defn, sr_tr)
sr_inst.name = "Transport Stay Rods"
sr_inst.layer = model.layers["Lock anchor"]
sr_inst.set_attribute("dynamic_attributes", "_name", "TransportStayRods")
sr_inst.set_attribute("dynamic_attributes", "hidden", 1.0)
sr_inst.set_attribute("dynamic_attributes", "_hidden_formula", "PanelSwing!swing<0.5")

# ── Fan B flexible connector — a CHILD DC component inside the swing def: SHOWN when the
#    door is CLOSED (plugged in), HIDDEN when the panel swings open (the jumper is unplugged
#    before transport). Built at world (closed) coords; the orange coil follows Fan B and
#    hides past swing 0.5. Same child-DC + hidden-formula pattern as the lift-out walkways. ──
fbc_defn = model.definitions.add("Fan B Cable")
ents = fbc_defn.entities
  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-24.mm, 34.7.mm, 0.mm)
  circle = ge.add_circle([300.mm,18.mm,600.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.88254607774877.mm, 20.51503667241026.mm, -19.800321490536817.mm)
  circle = ge.add_circle([276.mm,52.7.mm,600.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.68564383602245.mm, -2.0105125474890855.mm, -8.199678256131165.mm)
  circle = ge.add_circle([285.88254607774877.mm,73.21503667241026.mm,580.1996785094632.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.6838289165739.mm, -2.0092572717898207.mm, 8.2050052627593.mm)
  circle = ge.add_circle([263.1969022417263.mm,71.20452412492118.mm,572.000000253332.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-13.141618916088305.mm, 4.590542152177164.mm, 19.80252750221382.mm)
  circle = ge.add_circle([240.51307332515242.mm,69.19526685313136.mm,580.2050055160913.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.35038128882598585.mm, 13.922184945201437.mm, 19.798114045701254.mm)
  circle = ge.add_circle([227.3714544090641.mm,73.78580900530852.mm,600.0075330183051.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.887457576706709.mm, 20.518433674571412.mm, 8.194350656005668.mm)
  circle = ge.add_circle([227.7218356978901.mm,87.70799395050996.mm,619.8056470640064.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.882012818492626.mm, 20.514667847564553.mm, -8.210331675504335.mm)
  circle = ge.add_circle([237.6092932745968.mm,108.22642762508137.mm,627.9999977200121.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.3372369976175946.mm, 13.913093792780643.mm, -19.804732080572876.mm)
  circle = ge.add_circle([247.49130609308943.mm,128.74109547264592.mm,619.7896660445077.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-13.154761742458732.mm, 4.581452012900797.mm, -19.79590516786675.mm)
  circle = ge.add_circle([247.82854309070703.mm,142.65418926542657.mm,599.9849339639348.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.6892701384956.mm, -2.013020652946068.mm, -8.189022462768548.mm)
  circle = ge.add_circle([234.6737813482483.mm,147.23564127832736.mm,580.1890287960681.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.680195541909967.mm, -2.006744274904122.mm, 8.215657493981098.mm)
  circle = ge.add_circle([211.9845112097527.mm,145.2226206253813.mm,572.0000063332996.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-13.132854591501854.mm, 4.596603932871005.mm, 19.806935225453913.mm)
  circle = ge.add_circle([189.30431566784273.mm,143.21587635047717.mm,580.2156638272807.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.3591417071779972.mm, 13.928244024176877.mm, 19.7936948571936.mm)
  circle = ge.add_circle([176.17146107634088.mm,147.81248028334818.mm,600.0225990527346.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.891081521257831.mm, 20.520940149188903.mm, 8.183693676805206.mm)
  circle = ge.add_circle([176.53060278351887.mm,161.74072430752506.mm,619.8162939099282.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.878377086957585.mm, 20.512153220566233.mm, -8.22098271780385.mm)
  circle = ge.add_circle([186.4216843047767.mm,182.26166445671396.mm,627.9999875867334.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.32847169805819476.mm, 13.907031337753978.mm, -19.809136936697882.mm)
  circle = ge.add_circle([196.3000613917343.mm,202.7738176772802.mm,619.7790048689295.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-13.16352118266667.mm, 4.575393610451471.mm, -19.79148311384131.mm)
  circle = ge.add_circle([196.62853308979248.mm,216.68084901503417.mm,599.9698679322316.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.692891724862363.mm, -2.0155254965426366.mm, -8.178364298501492.mm)
  circle = ge.add_circle([183.4650119071258.mm,221.25624262548564.mm,580.1783848183903.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.676557453766975.mm, -2.0042280179752368.mm, 8.226307346587078.mm)
  circle = ge.add_circle([160.77212018226345.mm,219.240717128943.mm,572.0000205198888.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-13.124088317603963.mm, 4.602667061791692.mm, 19.81133721414517.mm)
  circle = ge.add_circle([138.09556272849647.mm,217.23648911096777.mm,580.2263278664759.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.3679001686079175.mm, 13.934301749661557.mm, 19.789269937970403.mm)
  circle = ge.add_circle([124.97147441089251.mm,221.83915617275946.mm,600.0376650806211.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.894700749178014.mm, 20.523443361583247.mm, 8.173034328243148.mm)
  circle = ge.add_circle([125.33937457950043.mm,235.77345792242102.mm,619.8269350185915.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.87473664246994.mm, 20.509635333888923.mm, -8.231631379945611.mm)
  circle = ge.add_circle([135.23407532867844.mm,256.29690128400426.mm,627.9999693468346.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.3197044504563564.mm, 13.900967535378072.mm, -19.81353605763661.mm)
  circle = ge.add_circle([145.10881197114838.mm,276.8065366178932.mm,619.768337966889.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-13.172278664684654.mm, 4.5693365623699265.mm, -19.787055329740838.mm)
  circle = ge.add_circle([145.42851642160474.mm,290.70750415327126.mm,599.9548019092524.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.69650859407416.mm, -2.018027077553654.mm, -8.167703766415912.mm)
  circle = ge.add_circle([132.2562377569201.mm,295.2768407156412.mm,580.1677465795116.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.672914653198006.mm, -2.0017085017315708.mm, 8.236954817493938.mm)
  circle = ge.add_circle([109.55972916284593.mm,293.25881363808753.mm,572.0000428130957.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-13.115320096932777.mm, 4.608731537183758.mm, 19.815733467013047.mm)
  circle = ge.add_circle([86.88681450964792.mm,291.25710513635596.mm,580.2369976305896.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.37665667058003294.mm, 13.940358119901646.mm, 19.784839289313027.mm)
  circle = ge.add_circle([73.77149441271514.mm,295.8658366735397.mm,600.0527310976026.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.898315259419547.mm, 20.52594331102989.mm, 8.162372613405523.mm)
  circle = ge.add_circle([74.14815108329518.mm,309.80619479344136.mm,619.8375703869157.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-0.04646634271472294.mm, -0.03213810447130072.mm, -27.999943000321196.mm)
  circle = ge.add_circle([84.04646634271472.mm,330.33213810447126.mm,627.9999430003212.mm], vec, 5.mm, 8)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B flex connector (box -> fan, Cct B)
  grp = ents.add_group
  grp.name = "Fan B flex connector (box -> fan, Cct B)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-24.mm, 34.700000000000045.mm, 0.mm)
  circle = ge.add_circle([84.mm,330.29999999999995.mm,600.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fan B flex connector (box -> fan, Cct B)"] || model.materials.add("Fan B flex connector (box -> fan, Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

ents = defn.entities
fbc_inst = ents.add_instance(fbc_defn, Geom::Transformation.new)
fbc_inst.name = "Fan B Cable"
fbc_inst.layer = model.layers["Fan B Cable"]
fbc_inst.set_attribute("dynamic_attributes", "_name", "FanBCable")
fbc_inst.set_attribute("dynamic_attributes", "hidden", 0.0)
fbc_inst.set_attribute("dynamic_attributes", "_hidden_formula", "PanelSwing!swing>0.5")

# ── Lift-out film rail — a CHILD DC component inside the swing def: HIDDEN when the panel
#    swings (the removable left rail pair + clamp bars are lifted out for transport, clearing
#    the X=150 rail plane for the swinging drum surround). Built at world coords; same child-DC
#    + hidden-formula pattern as the lift-out walkways. As a swing child it also rides rigidly
#    with the surround through the animation, so it never sweeps into it. ──
lfr_defn = model.definitions.add("Lift-out Film Rail")
ents = lfr_defn.entities
  # FP Rail BL (lower left)
  grp = ents.add_group
  grp.name = "FP Rail BL (lower left)"
  face = grp.entities.add_face([150.mm,100.mm,100.mm], [190.mm,100.mm,100.mm], [190.mm,2262.mm,100.mm], [150.mm,2262.mm,100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Rail TL (upper left)
  grp = ents.add_group
  grp.name = "FP Rail TL (upper left)"
  face = grp.entities.add_face([150.mm,100.mm,2204.mm], [190.mm,100.mm,2204.mm], [190.mm,2262.mm,2204.mm], [150.mm,2262.mm,2204.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Pivot post (Ø89 CHS)"] || model.materials.add("Pivot post (Ø89 CHS)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail clamp bar (removable)
  grp = ents.add_group
  grp.name = "Rail clamp bar (removable)"
  face = grp.entities.add_face([133.mm,122.mm,140.mm], [207.mm,122.mm,140.mm], [207.mm,158.mm,140.mm], [133.mm,158.mm,140.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Drum threshold sill (flush, chamfered step-over)"] || model.materials.add("Drum threshold sill (flush, chamfered step-over)")
  mat.color = Sketchup::Color.new(122, 122, 130)
  mat.alpha = 1.0
  grp.material = mat

  # Rail clamp bar (removable)
  grp = ents.add_group
  grp.name = "Rail clamp bar (removable)"
  face = grp.entities.add_face([133.mm,122.mm,2244.mm], [207.mm,122.mm,2244.mm], [207.mm,158.mm,2244.mm], [133.mm,158.mm,2244.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Drum threshold sill (flush, chamfered step-over)"] || model.materials.add("Drum threshold sill (flush, chamfered step-over)")
  mat.color = Sketchup::Color.new(122, 122, 130)
  mat.alpha = 1.0
  grp.material = mat

  # Rail clamp bar (removable)
  grp = ents.add_group
  grp.name = "Rail clamp bar (removable)"
  face = grp.entities.add_face([133.mm,2204.mm,140.mm], [207.mm,2204.mm,140.mm], [207.mm,2240.mm,140.mm], [133.mm,2240.mm,140.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Drum threshold sill (flush, chamfered step-over)"] || model.materials.add("Drum threshold sill (flush, chamfered step-over)")
  mat.color = Sketchup::Color.new(122, 122, 130)
  mat.alpha = 1.0
  grp.material = mat

  # Rail clamp bar (removable)
  grp = ents.add_group
  grp.name = "Rail clamp bar (removable)"
  face = grp.entities.add_face([133.mm,2204.mm,2244.mm], [207.mm,2204.mm,2244.mm], [207.mm,2240.mm,2244.mm], [133.mm,2240.mm,2244.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Drum threshold sill (flush, chamfered step-over)"] || model.materials.add("Drum threshold sill (flush, chamfered step-over)")
  mat.color = Sketchup::Color.new(122, 122, 130)
  mat.alpha = 1.0
  grp.material = mat

ents = defn.entities
lfr_inst = ents.add_instance(lfr_defn, Geom::Transformation.new)
lfr_inst.name = "Lift-out Film Rail"
lfr_inst.layer = model.layers["Film Plane Rails"]
lfr_inst.set_attribute("dynamic_attributes", "_name", "LiftoutFilmRail")
lfr_inst.set_attribute("dynamic_attributes", "hidden", 0.0)
lfr_inst.set_attribute("dynamic_attributes", "_hidden_formula", "PanelSwing!swing>0.5")

# Shift the moving def by -pivot so the def origin sits at the pivot — then the instance's
# RotZ swings the assembly about the pivot (same origin-at-rotation-point pattern the
# cargo-door leaves use).
shift = Geom::Transformation.translation([(-175).mm, (-2287).mm, 0])
defn.entities.transform_entities(shift, defn.entities.to_a)

inst = entities.add_instance(defn, Geom::Transformation.translation([175.mm, 2287.mm, 0]))
inst.name = "Panel Swing"
inst.layer = model.layers["Panel Swing"]
da = "dynamic_attributes"
[defn, inst].each do |e|
  e.set_attribute(da, "_name", "PanelSwing")
  e.set_attribute(da, "_lengthunits", "MILLIMETERS")
  e.set_attribute(da, "swing", 0.0)
end
inst.set_attribute(da, "_swing_access", "VIEW")
inst.set_attribute(da, "_swing_label", "Swing")
inst.set_attribute(da, "rotz", 0.0)
inst.set_attribute(da, "_rotz_formula", "56*swing")
inst.set_attribute(da, "onclick", 'ANIMATE("swing", 0, 1)')
inst.set_attribute(da, "_onclick_access", "NONE")
dc_inst = inst

# ═══ Cargo Doors — DYNAMIC COMPONENT (click to close) ═══
# Parent "Cargo Doors" holds two leaf children whose RotZ is driven by the
# parent's "shut" attribute (0 = open / ±180°, 1 = closed / 0°). Click the parent
# with the Interact tool → ANIMATE shut 0↔1 swings both leaves together.
doors_defn = model.definitions.add("Cargo Doors")
doors_ents = doors_defn.entities

near_defn = model.definitions.add("Cargo Door Leaf Near")
ents = near_defn.entities
  # Cargo door leaf near
  grp = ents.add_group
  grp.name = "Cargo door leaf near"
  face = grp.entities.add_face([-30.mm,0.mm,0.mm], [30.mm,0.mm,0.mm], [30.mm,1178.mm,0.mm], [-30.mm,1178.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Cargo door leaf near"] || model.materials.add("Cargo door leaf near")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.25
  grp.material = mat

near_inst = doors_ents.add_instance(near_defn, Geom::Transformation.translation([-85.mm, 0, 0]))
near_inst.name = "Leaf Near"

far_defn = model.definitions.add("Cargo Door Leaf Far")
ents = far_defn.entities
  # Cargo door leaf far
  grp = ents.add_group
  grp.name = "Cargo door leaf far"
  face = grp.entities.add_face([-30.mm,-1178.mm,0.mm], [30.mm,-1178.mm,0.mm], [30.mm,0.mm,0.mm], [-30.mm,0.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Cargo door leaf near"] || model.materials.add("Cargo door leaf near")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.25
  grp.material = mat

far_inst = doors_ents.add_instance(far_defn, Geom::Transformation.translation([-85.mm, 2362.mm, 0]))
far_inst.name = "Leaf Far"

doors_inst = entities.add_instance(doors_defn, Geom::Transformation.new)
doors_inst.name = "Cargo Doors"
doors_inst.layer = model.layers["Cargo Doors"]

dda = "dynamic_attributes"
doors_inst.set_attribute(dda, "_name", "CargoDoors")
doors_inst.set_attribute(dda, "shut", 0.0)
doors_inst.set_attribute(dda, "_shut_access", "VIEW")
doors_inst.set_attribute(dda, "_shut_label", "Shut")
doors_inst.set_attribute(dda, "onclick", 'ANIMATE("shut", 0, 1)')
doors_inst.set_attribute(dda, "_onclick_access", "NONE")
near_inst.set_attribute(dda, "_name", "LeafNear")
near_inst.set_attribute(dda, "rotz", 180.0)
near_inst.set_attribute(dda, "_rotz_formula", "180*(1-CargoDoors!shut)")
far_inst.set_attribute(dda, "_name", "LeafFar")
far_inst.set_attribute(dda, "rotz", -180.0)
far_inst.set_attribute(dda, "_rotz_formula", "-180*(1-CargoDoors!shut)")

# ── "Labeled" scene callouts (Labels tag — shown only in the "Labeled" scene) ──
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Fixed Door Frame" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("DOOR FRAME", anc, Geom::Vector3d.new(-500.mm, -200.mm, 800.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Panel Swing" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("HINGE PANEL
(swings 56° for transport)", anc, Geom::Vector3d.new(550.mm, -100.mm, 1250.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Cargo Doors" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("CARGO DOORS", anc, Geom::Vector3d.new(-100.mm, -1600.mm, 150.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Processing Tray (partial)" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("PROCESSING TRAY", anc, Geom::Vector3d.new(950.mm, 500.mm, 300.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
anc = Geom::Point3d.new(-400.mm, 1181.mm, 1700.mm)
txt = entities.add_text("LIGHT-TRAP DRUM
(revolving door)", anc, Geom::Vector3d.new(-750.mm, 0.mm, 650.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(150.mm, 365.mm, 700.mm)
txt = entities.add_text("FAN B (intake)", anc, Geom::Vector3d.new(-200.mm, -650.mm, 1000.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(175.mm, 2287.mm, 1600.mm)
txt = entities.add_text("PIVOT POST Ø89 CHS
(= film far-left post)", anc, Geom::Vector3d.new(550.mm, -200.mm, 700.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1035.mm, 150.mm, 73.mm)
txt = entities.add_text("WALKWAYS", anc, Geom::Vector3d.new(250.mm, -750.mm, 900.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(170.mm, 1181.mm, 2268.mm)
txt = entities.add_text("FILM-PLANE RAILS
(left pair removable)", anc, Geom::Vector3d.new(1400.mm, 0.mm, 300.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1814.3813260216311.mm, 0.mm, 1075.mm)
txt = entities.add_text("TRANSPORT STAY anchor
(bolted plates; rod→wall when swung)", anc, Geom::Vector3d.new(300.mm, -300.mm, 700.mm))
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
keep_tags = ["Context", "Door Frame", "Pivot Axle", "Processing Tray", "Walkways", "Film Plane Rails", "Near Leaf", "Far Leaf", "Lock anchor", "Panel skin", "Panel Swing", "Fan B", "Drum shell", "Cargo Doors", "Fan B Cable", "Labels"]
default_layer = model.layers[0]
model.layers.to_a.each { |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}

# ── Tag the Panel Swing's skin / EPDM-seal / Fan-B sub-parts onto hideable tags (they
#    default to the always-on untagged layer, so the "Handle · Frame · Pivot" scene can't
#    drop them otherwise). The frame jambs/header, handle, hinges, latches, drum stay. ──
ps_defn = model.definitions["Panel Swing"]
if ps_defn
  skin_l = model.layers["Panel skin"]
  fan_l  = model.layers["Fan B"]
  drum_l = model.layers["Drum shell"]
  ps_defn.entities.grep(Sketchup::Group).each do |g|
    nm = g.name.to_s
    if nm.include?("corner") || nm.include?("near (swing") || nm.include?("EPDM") || nm.include?("Bay wall") || nm.include?("mount band")
      g.layer = skin_l if skin_l
    elsif nm.include?("Fan B")
      g.layer = fan_l if fan_l
    elsif nm.include?("C-shell") || nm.include?("Housing arc")
      g.layer = drum_l if drum_l
    end
  end
end

# ── Camera + scenes (the swing is interactive; plus a "Labeled" callout scene) ──
model.layers.each { |l| l.visible = true }
model.layers["Labels"].visible = false if model.layers["Labels"]  # frame geometry, not labels
bb = model.bounds
ctr = bb.center
dir = Geom::Vector3d.new(-0.6, -0.72, 0.45); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.5)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents
model.active_view.zoom(0.62)   # pull back so callouts have margin (and read larger)
# Overview — main interactive scene (Labels OFF), listed first.
page = model.pages.add("Overview")
page.use_camera = true

# ── "Handle · Frame · Pivot" scene — isolate the swinging panel (frame + interior pull
#    handle) and the Ø89 pivot post, hiding the container/tray/walkway clutter so the
#    handle-to-frame mounting reads clearly. Per-page tag visibility is captured on add. ──
hf_keep = ["Door Frame", "Pivot Axle", "Panel Swing"]
model.layers.each { |l| l.visible = false }
hf_keep.each { |n| model.layers[n].visible = true if model.layers[n] }
# drum panels + the blue/brown panel skins stay visible here at 50% opacity for context
# (Fan B stays hidden); the steel frame + handle read solid on top.
model.layers["Drum shell"].visible = true if model.layers["Drum shell"]
model.layers["Panel skin"].visible = true if model.layers["Panel skin"]
# 3/4 view from the interior side (high X), near-Yd corner, slightly above — sets the
# viewing DIRECTION; the zoom-to-fit below then frames it (the old fixed eye read zoomed-out).
hf_eye = Geom::Point3d.new(3200, 250, 1950)
hf_tgt = Geom::Point3d.new(120, 1150, 1080)
model.active_view.camera = Sketchup::Camera.new(hf_eye, hf_tgt, Z_AXIS)
hf_focus = model.entities.grep(Sketchup::ComponentInstance).select { |i|
  hf_keep.include?(i.layer.name) }
model.active_view.zoom(hf_focus) unless hf_focus.empty?   # fit the isolated panel + pivot
model.active_view.zoom(0.9)                               # small margin around the assembly
hfpage = model.pages.add("Handle · Frame · Pivot"); hfpage.use_camera = true
model.layers.each { |l| l.visible = true }      # restore for the default state
model.layers["Labels"].visible = false if model.layers["Labels"]

# Labeled — Overview view + component callouts, listed LAST (project rule: every .skp gets a Labeled scene).
model.active_view.zoom_extents
model.active_view.zoom(0.62)
model.layers["Labels"].visible = true if model.layers["Labels"]
lpage = model.pages.add("Labeled"); lpage.use_camera = true
model.layers["Labels"].visible = false if model.layers["Labels"]

model.commit_operation

# Register the DC attributes with the Dynamic Components engine so the Interact tool
# drives the swing (skipped if the extension isn't loaded).
dc_ready = false
if defined?($dc_observers) && $dc_observers.respond_to?(:get_latest_class)
  cls = $dc_observers.get_latest_class
  if cls
    [dc_inst, doors_inst].each { |di| cls.redraw_with_undo(di) rescue nil }
    dc_ready = true
  end
end

{ success: true, model: "Light Trap (dynamic swing)",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   dynamic_engine: dc_ready, swing_deg: 56,
   tags: model.layers.count, scenes: model.pages.count }.to_json
