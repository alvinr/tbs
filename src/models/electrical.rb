# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/ — do not edit this .rb directly.
model = Sketchup.active_model
model.start_operation("TBS-001 Electrical", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# ── Idempotent rebuild: clear prior groups/instances/text ──
to_erase = entities.to_a.select { |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text)
}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each { |p| model.pages.erase(p) }

# ── Sketchfab metadata — sketchfab dict fill-only-if-blank; name/desc forced when requested ──
model.name = "TBS-001 Electrical Model" if model.name.to_s.strip.empty?
model.description = "There are a number of discrete systems, color-coded in the diagram below. This view is shown from the optical axis, looking through the container wall. Each of these sub-systems, has a detailed breakdown of construction, schematic and other diagrams to show how each system it built, installed, used and maintained. The 3d model below provides a simply way to view the whole system." if model.description.to_s.strip.empty?
model.set_attribute("sketchfab", "model_title", "TBS-001 Electrical Model") if model.get_attribute("sketchfab", "model_title").to_s.strip.empty?
model.set_attribute("sketchfab", "model_description", "There are a number of discrete systems, color-coded in the diagram below. This view is shown from the optical axis, looking through the container wall. Each of these sub-systems, has a detailed breakdown of construction, schematic and other diagrams to show how each system it built, installed, used and maintained. The 3d model below provides a simply way to view the whole system.") if model.get_attribute("sketchfab", "model_description").to_s.strip.empty?
model.set_attribute("sketchfab", "model_id", "6930c96be025469fb8ef702393d7c35f") if model.get_attribute("sketchfab", "model_id").to_s.strip.empty?
model.set_attribute("sketchfab", "model_tags", "sketchup") if model.get_attribute("sketchfab", "model_tags").to_s.strip.empty?

# ── Tags ──
  model.layers.add("Context") unless model.layers["Context"]
  model.layers.add("Solar Array") unless model.layers["Solar Array"]
  model.layers.add("Power Core") unless model.layers["Power Core"]
  model.layers.add("Battery") unless model.layers["Battery"]
  model.layers.add("External Panel") unless model.layers["External Panel"]
  model.layers.add("Inverter") unless model.layers["Inverter"]
  model.layers.add("Circuit Runs") unless model.layers["Circuit Runs"]
  model.layers.add("Labels") unless model.layers["Labels"]

# ── Subsystems ──
  # ═══ Container (ghost) ═══
  defn = model.definitions.add("Container (ghost)")
  ents = defn.entities
  # Floor (context)
  grp = ents.add_group
  grp.name = "Floor (context)"
  face = grp.entities.add_face([0.mm,0.mm,-40.mm], [5893.mm,0.mm,-40.mm], [5893.mm,2362.mm,-40.mm], [0.mm,2362.mm,-40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Floor (context)"] || model.materials.add("Floor (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.22
  grp.material = mat

  # Pinhole Wall (context)
  grp = ents.add_group
  grp.name = "Pinhole Wall (context)"
  face = grp.entities.add_face([0.mm,-40.mm,0.mm], [5893.mm,-40.mm,0.mm], [5893.mm,0.mm,0.mm], [0.mm,0.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Pinhole Wall (context)"] || model.materials.add("Pinhole Wall (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.1
  grp.material = mat

  # Fan A ghost (exhaust)
  grp = ents.add_group
  grp.name = "Fan A ghost (exhaust)"
  face = grp.entities.add_face([5558.mm,1106.mm,1925.mm], [5678.mm,1106.mm,1925.mm], [5678.mm,1256.mm,1925.mm], [5558.mm,1256.mm,1925.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Fan A ghost (exhaust)"] || model.materials.add("Fan A ghost (exhaust)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 0.18
  grp.material = mat

  # Fan B wall box ghost (Cct B)
  grp = ents.add_group
  grp.name = "Fan B wall box ghost (Cct B)"
  face = grp.entities.add_face([260.mm,0.mm,555.mm], [340.mm,0.mm,555.mm], [340.mm,60.mm,555.mm], [260.mm,60.mm,555.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Fan B wall box ghost (Cct B)"] || model.materials.add("Fan B wall box ghost (Cct B)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 0.2
  grp.material = mat

  # Pump zone ghost (Cct C)
  grp = ents.add_group
  grp.name = "Pump zone ghost (Cct C)"
  face = grp.entities.add_face([4734.mm,1046.mm,1100.mm], [4884.mm,1046.mm,1100.mm], [4884.mm,1316.mm,1100.mm], [4734.mm,1316.mm,1100.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1170.mm)
  mat = model.materials["Pump zone ghost (Cct C)"] || model.materials.add("Pump zone ghost (Cct C)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 0.14
  grp.material = mat

  # White LED ghost (Cct G)
  grp = ents.add_group
  grp.name = "White LED ghost (Cct G)"
  face = grp.entities.add_face([1000.mm,1031.mm,2348.mm], [1600.mm,1031.mm,2348.mm], [1600.mm,1331.mm,2348.mm], [1000.mm,1331.mm,2348.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["White LED ghost (Cct G)"] || model.materials.add("White LED ghost (Cct G)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 0.16
  grp.material = mat

  # White LED ghost (Cct G)
  grp = ents.add_group
  grp.name = "White LED ghost (Cct G)"
  face = grp.entities.add_face([2900.mm,1031.mm,2348.mm], [3500.mm,1031.mm,2348.mm], [3500.mm,1331.mm,2348.mm], [2900.mm,1331.mm,2348.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["White LED ghost (Cct G)"] || model.materials.add("White LED ghost (Cct G)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 0.16
  grp.material = mat

  # White LED ghost (Cct G)
  grp = ents.add_group
  grp.name = "White LED ghost (Cct G)"
  face = grp.entities.add_face([4424.mm,881.mm,2348.mm], [4724.mm,881.mm,2348.mm], [4724.mm,1481.mm,2348.mm], [4424.mm,1481.mm,2348.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["White LED ghost (Cct G)"] || model.materials.add("White LED ghost (Cct G)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 0.16
  grp.material = mat

  # Safelight ghost (Cct D)
  grp = ents.add_group
  grp.name = "Safelight ghost (Cct D)"
  face = grp.entities.add_face([500.mm,100.mm,2363.mm], [540.mm,100.mm,2363.mm], [540.mm,2262.mm,2363.mm], [500.mm,2262.mm,2363.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Safelight ghost (Cct D)"] || model.materials.add("Safelight ghost (Cct D)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 0.16
  grp.material = mat

  # Safelight ghost (Cct D)
  grp = ents.add_group
  grp.name = "Safelight ghost (Cct D)"
  face = grp.entities.add_face([2250.mm,100.mm,2363.mm], [2290.mm,100.mm,2363.mm], [2290.mm,2262.mm,2363.mm], [2250.mm,2262.mm,2363.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Safelight ghost (Cct D)"] || model.materials.add("Safelight ghost (Cct D)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 0.16
  grp.material = mat

  # Safelight ghost (Cct D)
  grp = ents.add_group
  grp.name = "Safelight ghost (Cct D)"
  face = grp.entities.add_face([4150.mm,100.mm,2363.mm], [4190.mm,100.mm,2363.mm], [4190.mm,2262.mm,2363.mm], [4150.mm,2262.mm,2363.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Safelight ghost (Cct D)"] || model.materials.add("Safelight ghost (Cct D)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 0.16
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Container (ghost)"
  inst.layer = model.layers["Context"]

  # ═══ Transport Locks (context) ═══
  defn = model.definitions.add("Transport Locks (context)")
  ents = defn.entities
  # Stay inside plate
  grp = ents.add_group
  grp.name = "Stay inside plate"
  face = grp.entities.add_face([1614.mm,0.mm,400.mm], [1814.mm,0.mm,400.mm], [1814.mm,12.mm,400.mm], [1614.mm,12.mm,400.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay outside plate
  grp = ents.add_group
  grp.name = "Stay outside plate"
  face = grp.entities.add_face([1614.mm,-52.mm,400.mm], [1814.mm,-52.mm,400.mm], [1814.mm,-40.mm,400.mm], [1614.mm,-40.mm,400.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay eye
  grp = ents.add_group
  grp.name = "Stay eye"
  face = grp.entities.add_face([1699.mm,12.mm,485.mm], [1729.mm,12.mm,485.mm], [1729.mm,67.mm,485.mm], [1699.mm,67.mm,485.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1636.mm,-58.mm,422.mm], [1652.mm,-58.mm,422.mm], [1652.mm,18.mm,422.mm], [1636.mm,18.mm,422.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1636.mm,-58.mm,562.mm], [1652.mm,-58.mm,562.mm], [1652.mm,18.mm,562.mm], [1636.mm,18.mm,562.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1776.mm,-58.mm,422.mm], [1792.mm,-58.mm,422.mm], [1792.mm,18.mm,422.mm], [1776.mm,18.mm,422.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1776.mm,-58.mm,562.mm], [1792.mm,-58.mm,562.mm], [1792.mm,18.mm,562.mm], [1776.mm,18.mm,562.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay inside plate
  grp = ents.add_group
  grp.name = "Stay inside plate"
  face = grp.entities.add_face([1614.mm,0.mm,1950.mm], [1814.mm,0.mm,1950.mm], [1814.mm,12.mm,1950.mm], [1614.mm,12.mm,1950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay outside plate
  grp = ents.add_group
  grp.name = "Stay outside plate"
  face = grp.entities.add_face([1614.mm,-52.mm,1950.mm], [1814.mm,-52.mm,1950.mm], [1814.mm,-40.mm,1950.mm], [1614.mm,-40.mm,1950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay eye
  grp = ents.add_group
  grp.name = "Stay eye"
  face = grp.entities.add_face([1699.mm,12.mm,2035.mm], [1729.mm,12.mm,2035.mm], [1729.mm,67.mm,2035.mm], [1699.mm,67.mm,2035.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1636.mm,-58.mm,1972.mm], [1652.mm,-58.mm,1972.mm], [1652.mm,18.mm,1972.mm], [1636.mm,18.mm,1972.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1636.mm,-58.mm,2112.mm], [1652.mm,-58.mm,2112.mm], [1652.mm,18.mm,2112.mm], [1636.mm,18.mm,2112.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1776.mm,-58.mm,1972.mm], [1792.mm,-58.mm,1972.mm], [1792.mm,18.mm,1972.mm], [1776.mm,18.mm,1972.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Stay bolt M16
  grp = ents.add_group
  grp.name = "Stay bolt M16"
  face = grp.entities.add_face([1776.mm,-58.mm,2112.mm], [1792.mm,-58.mm,2112.mm], [1792.mm,18.mm,2112.mm], [1776.mm,18.mm,2112.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Transport Locks (context)"
  inst.layer = model.layers["Context"]

  # ═══ Chem Prep Shelf (context) ═══
  defn = model.definitions.add("Chem Prep Shelf (context)")
  ents = defn.entities
  # Chem Shelf (board, deployed)
  grp = ents.add_group
  grp.name = "Chem Shelf (board, deployed)"
  face = grp.entities.add_face([1180.mm,0.mm,1053.mm], [1780.mm,0.mm,1053.mm], [1780.mm,225.mm,1053.mm], [1180.mm,225.mm,1053.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Chem Shelf (board, deployed)"] || model.materials.add("Chem Shelf (board, deployed)")
  mat.color = Sketchup::Color.new(200, 176, 112)
  mat.alpha = 1.0
  grp.material = mat

  # Chem Shelf lip (front)
  grp = ents.add_group
  grp.name = "Chem Shelf lip (front)"
  face = grp.entities.add_face([1180.mm,219.mm,1075.mm], [1780.mm,219.mm,1075.mm], [1780.mm,225.mm,1075.mm], [1180.mm,225.mm,1075.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Chem Shelf (board, deployed)"] || model.materials.add("Chem Shelf (board, deployed)")
  mat.color = Sketchup::Color.new(200, 176, 112)
  mat.alpha = 1.0
  grp.material = mat

  # Chem Shelf lip (end)
  grp = ents.add_group
  grp.name = "Chem Shelf lip (end)"
  face = grp.entities.add_face([1180.mm,0.mm,1075.mm], [1186.mm,0.mm,1075.mm], [1186.mm,225.mm,1075.mm], [1180.mm,225.mm,1075.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Chem Shelf (board, deployed)"] || model.materials.add("Chem Shelf (board, deployed)")
  mat.color = Sketchup::Color.new(200, 176, 112)
  mat.alpha = 1.0
  grp.material = mat

  # Chem Shelf lip (end)
  grp = ents.add_group
  grp.name = "Chem Shelf lip (end)"
  face = grp.entities.add_face([1774.mm,0.mm,1075.mm], [1780.mm,0.mm,1075.mm], [1780.mm,225.mm,1075.mm], [1774.mm,225.mm,1075.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Chem Shelf (board, deployed)"] || model.materials.add("Chem Shelf (board, deployed)")
  mat.color = Sketchup::Color.new(200, 176, 112)
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
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Chem Shelf stay
  grp = ents.add_group
  grp.name = "Chem Shelf stay"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 215.mm, -230.mm)
  circle = ge.add_circle([1205.mm,0.mm,1305.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Chem Shelf stay anchor
  grp = ents.add_group
  grp.name = "Chem Shelf stay anchor"
  face = grp.entities.add_face([1193.mm,0.mm,1293.mm], [1217.mm,0.mm,1293.mm], [1217.mm,8.mm,1293.mm], [1193.mm,8.mm,1293.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Chem Shelf stay
  grp = ents.add_group
  grp.name = "Chem Shelf stay"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 215.mm, -230.mm)
  circle = ge.add_circle([1755.mm,0.mm,1305.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Chem Shelf stay anchor
  grp = ents.add_group
  grp.name = "Chem Shelf stay anchor"
  face = grp.entities.add_face([1743.mm,0.mm,1293.mm], [1767.mm,0.mm,1293.mm], [1767.mm,8.mm,1293.mm], [1743.mm,8.mm,1293.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Chem Prep Shelf (context)"
  inst.layer = model.layers["Context"]

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
  mat.alpha = 0.3
  grp.material = mat

  # Solar Panel 2 (200W)
  grp = ents.add_group
  grp.name = "Solar Panel 2 (200W)"
  face = grp.entities.add_face([960.mm,-900.mm,120.mm], [1640.mm,-900.mm,120.mm], [1640.mm,-2181.7175976009694.mm,859.9999999999999.mm], [960.mm,-2181.7175976009694.mm,859.9999999999999.mm])
  face.pushpull(35.mm)
  mat = model.materials["Solar Panel 1 (200W)"] || model.materials.add("Solar Panel 1 (200W)")
  mat.color = Sketchup::Color.new(27, 58, 107)
  mat.alpha = 0.3
  grp.material = mat

  # Solar Panel 3 (200W)
  grp = ents.add_group
  grp.name = "Solar Panel 3 (200W)"
  face = grp.entities.add_face([1670.mm,-900.mm,120.mm], [2350.mm,-900.mm,120.mm], [2350.mm,-2181.7175976009694.mm,859.9999999999999.mm], [1670.mm,-2181.7175976009694.mm,859.9999999999999.mm])
  face.pushpull(35.mm)
  mat = model.materials["Solar Panel 1 (200W)"] || model.materials.add("Solar Panel 1 (200W)")
  mat.color = Sketchup::Color.new(27, 58, 107)
  mat.alpha = 0.3
  grp.material = mat

  # Tilt Frame front rail
  grp = ents.add_group
  grp.name = "Tilt Frame front rail"
  face = grp.entities.add_face([250.mm,-920.mm,0.mm], [2350.mm,-920.mm,0.mm], [2350.mm,-880.mm,0.mm], [250.mm,-880.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Tilt Frame back rail
  grp = ents.add_group
  grp.name = "Tilt Frame back rail"
  face = grp.entities.add_face([250.mm,-2201.7175976009694.mm,0.mm], [2350.mm,-2201.7175976009694.mm,0.mm], [2350.mm,-2161.7175976009694.mm,0.mm], [250.mm,-2161.7175976009694.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Tilt Frame back leg
  grp = ents.add_group
  grp.name = "Tilt Frame back leg"
  face = grp.entities.add_face([250.mm,-2201.7175976009694.mm,0.mm], [290.mm,-2201.7175976009694.mm,0.mm], [290.mm,-2161.7175976009694.mm,0.mm], [250.mm,-2161.7175976009694.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(859.9999999999999.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Tilt Frame back leg
  grp = ents.add_group
  grp.name = "Tilt Frame back leg"
  face = grp.entities.add_face([2310.mm,-2201.7175976009694.mm,0.mm], [2350.mm,-2201.7175976009694.mm,0.mm], [2350.mm,-2161.7175976009694.mm,0.mm], [2310.mm,-2161.7175976009694.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(859.9999999999999.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.3710904324400417.mm, 11.174603174603135.mm, -9.294027154632516.mm)
  circle = ge.add_circle([1304.9884758210587.mm,-772.6031746031746.mm,60.54726213625084.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.933421446249213.mm, 11.174603174603249.mm, -4.235229948707875.mm)
  circle = ge.add_circle([1301.6173853886187.mm,-761.4285714285714.mm,51.25323498161833.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.7777073955937794.mm, 11.174603174603135.mm, 9.488283990227053.mm)
  circle = ge.add_circle([1279.0719702576096.mm,-638.5079365079365.mm,58.633966698844425.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.648268936837894.mm, 11.174603174603249.mm, 4.790682190550854.mm)
  circle = ge.add_circle([1281.8496776532033.mm,-627.3333333333334.mm,68.12225068907148.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-6.091062472885142.mm, 11.174603174603135.mm, 7.78730694182191.mm)
  circle = ge.add_circle([1285.5749983342314.mm,-292.0952380952381.mm,48.69870124300441.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.1477544109268365.mm, 11.174603174603249.mm, 9.819666555791699.mm)
  circle = ge.add_circle([1279.4839358613463.mm,-280.92063492063494.mm,56.48600818482632.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.418368879275704.mm, -2.5357148359493706.mm, 11.37928719490992.mm)
  circle = ge.add_circle([1311.1398123176873.mm,-57.11590977512742.mm,1140.3413249442387.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.828357313004972.mm, -8.573226322840902.mm, 11.305328620385353.mm)
  circle = ge.add_circle([1301.7214434384116.mm,-59.65162461107679.mm,1151.7206121391487.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.482696639387086.mm, -2.278244054865958.mm, 11.3803237041584.mm)
  circle = ge.add_circle([1314.3772508079644.mm,-57.166800775558926.mm,1319.9296338243005.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.05565119709172.mm, -8.436279561400461.mm, 11.308990992783038.mm)
  circle = ge.add_circle([1304.8945541685773.mm,-59.445044830424884.mm,1331.3099575284589.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.512274654742669.mm, -2.1488868572789173.mm, 11.380800292904041.mm)
  circle = ge.add_circle([1315.9954293873695.mm,-57.195686389145656.mm,1409.7237969760447.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (+) (array -> panel MC4, bonded pair)
  grp = ents.add_group
  grp.name = "PV cord (+) (array -> panel MC4, bonded pair)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.167905496732828.mm, -8.365540100386568.mm, 11.310799739420418.mm)
  circle = ge.add_circle([1306.4831547326269.mm,-59.344573246424574.mm,1421.1045972689487.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  vec = Geom::Vector3d.new(-3.3710904324400417.mm, 11.174603174603135.mm, -9.294027154632516.mm)
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
  vec = Geom::Vector3d.new(-8.933421446249213.mm, 11.174603174603249.mm, -4.235229948707875.mm)
  circle = ge.add_circle([1317.6173853886187.mm,-761.4285714285714.mm,51.25323498161833.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(2.7777073955937794.mm, 11.174603174603135.mm, 9.488283990227053.mm)
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
  vec = Geom::Vector3d.new(8.648268936837894.mm, 11.174603174603249.mm, 4.790682190550854.mm)
  circle = ge.add_circle([1297.8496776532033.mm,-627.3333333333334.mm,68.12225068907148.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-6.091062472885142.mm, 11.174603174603135.mm, 7.78730694182191.mm)
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
  vec = Geom::Vector3d.new(1.1477544109268365.mm, 11.174603174603249.mm, 9.819666555791699.mm)
  circle = ge.add_circle([1295.4839358613463.mm,-280.92063492063494.mm,56.48600818482632.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-9.418368879275704.mm, -2.5357148359493706.mm, 11.37928719490992.mm)
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
  vec = Geom::Vector3d.new(-4.828357313004972.mm, -8.573226322840902.mm, 11.305328620385353.mm)
  circle = ge.add_circle([1317.7214434384116.mm,-59.65162461107679.mm,1151.7206121391487.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-9.482696639387086.mm, -2.278244054865958.mm, 11.3803237041584.mm)
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
  vec = Geom::Vector3d.new(-5.05565119709172.mm, -8.436279561400461.mm, 11.308990992783038.mm)
  circle = ge.add_circle([1320.8945541685773.mm,-59.445044830424884.mm,1331.3099575284589.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-9.512274654742669.mm, -2.1488868572789173.mm, 11.380800292904041.mm)
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
  vec = Geom::Vector3d.new(-5.167905496732828.mm, -8.365540100386568.mm, 11.310799739420418.mm)
  circle = ge.add_circle([1322.4831547326269.mm,-59.344573246424574.mm,1421.1045972689487.mm], vec, 5.mm, 6)
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

  # ═══ Power Core ═══
  defn = model.definitions.add("Power Core")
  ents = defn.entities
  # EP plywood backing panel (18mm)
  grp = ents.add_group
  grp.name = "EP plywood backing panel (18mm)"
  face = grp.entities.add_face([1817.mm,-18.mm,148.mm], [2181.mm,-18.mm,148.mm], [2181.mm,0.mm,148.mm], [1817.mm,0.mm,148.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1424.mm)
  mat = model.materials["EP plywood backing panel (18mm)"] || model.materials.add("EP plywood backing panel (18mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Plywood side lip (left, 18mm)
  grp = ents.add_group
  grp.name = "Plywood side lip (left, 18mm)"
  face = grp.entities.add_face([1817.mm,0.mm,148.mm], [1835.mm,0.mm,148.mm], [1835.mm,100.mm,148.mm], [1817.mm,100.mm,148.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1424.mm)
  mat = model.materials["EP plywood backing panel (18mm)"] || model.materials.add("EP plywood backing panel (18mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Plywood side lip (right, 18mm)
  grp = ents.add_group
  grp.name = "Plywood side lip (right, 18mm)"
  face = grp.entities.add_face([2163.mm,0.mm,148.mm], [2181.mm,0.mm,148.mm], [2181.mm,100.mm,148.mm], [2163.mm,100.mm,148.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1424.mm)
  mat = model.materials["EP plywood backing panel (18mm)"] || model.materials.add("EP plywood backing panel (18mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # IP65 enclosure (ghosted, fuse block + busbars)
  grp = ents.add_group
  grp.name = "IP65 enclosure (ghosted, fuse block + busbars)"
  face = grp.entities.add_face([1834.mm,12.mm,1150.mm], [2034.mm,12.mm,1150.mm], [2034.mm,152.mm,1150.mm], [1834.mm,152.mm,1150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(220.mm)
  mat = model.materials["IP65 enclosure (ghosted, fuse block + busbars)"] || model.materials.add("IP65 enclosure (ghosted, fuse block + busbars)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.12
  grp.material = mat

  # MPPT Controller (100/50)
  grp = ents.add_group
  grp.name = "MPPT Controller (100/50)"
  face = grp.entities.add_face([1844.mm,120.mm,1460.mm], [2029.mm,120.mm,1460.mm], [2029.mm,190.mm,1460.mm], [1844.mm,190.mm,1460.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["MPPT Controller (100/50)"] || model.materials.add("MPPT Controller (100/50)")
  mat.color = Sketchup::Color.new(58, 91, 160)
  mat.alpha = 1.0
  grp.material = mat

  # MPPT backing panel (18mm ply)
  grp = ents.add_group
  grp.name = "MPPT backing panel (18mm ply)"
  face = grp.entities.add_face([1837.mm,102.mm,1430.mm], [2042.mm,102.mm,1430.mm], [2042.mm,120.mm,1430.mm], [1837.mm,120.mm,1430.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(130.mm)
  mat = model.materials["EP plywood backing panel (18mm)"] || model.materials.add("EP plywood backing panel (18mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # MPPT sub-panel gusset (ply)
  grp = ents.add_group
  grp.name = "MPPT sub-panel gusset (ply)"
  face = grp.entities.add_face([1837.mm,0.mm,1430.mm], [1855.mm,0.mm,1430.mm], [1855.mm,120.mm,1430.mm], [1837.mm,120.mm,1430.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(130.mm)
  mat = model.materials["EP plywood backing panel (18mm)"] || model.materials.add("EP plywood backing panel (18mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # MPPT sub-panel gusset (ply)
  grp = ents.add_group
  grp.name = "MPPT sub-panel gusset (ply)"
  face = grp.entities.add_face([2024.mm,0.mm,1430.mm], [2042.mm,0.mm,1430.mm], [2042.mm,120.mm,1430.mm], [2024.mm,120.mm,1430.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(130.mm)
  mat = model.materials["EP plywood backing panel (18mm)"] || model.materials.add("EP plywood backing panel (18mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse Block base (Blue Sea 5026)
  grp = ents.add_group
  grp.name = "Fuse Block base (Blue Sea 5026)"
  face = grp.entities.add_face([1844.mm,25.mm,1190.mm], [2008.mm,25.mm,1190.mm], [2008.mm,64.mm,1190.mm], [1844.mm,64.mm,1190.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Fuse Block base (Blue Sea 5026)"] || model.materials.add("Fuse Block base (Blue Sea 5026)")
  mat.color = Sketchup::Color.new(42, 42, 42)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse A (5A — exhaust fan)
  grp = ents.add_group
  grp.name = "Fuse A (5A — exhaust fan)"
  face = grp.entities.add_face([1849.2142857142858.mm,40.mm,1218.mm], [1862.2142857142858.mm,40.mm,1218.mm], [1862.2142857142858.mm,49.mm,1218.mm], [1849.2142857142858.mm,49.mm,1218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse B (5A — intake fan)
  grp = ents.add_group
  grp.name = "Fuse B (5A — intake fan)"
  face = grp.entities.add_face([1872.642857142857.mm,40.mm,1218.mm], [1885.642857142857.mm,40.mm,1218.mm], [1885.642857142857.mm,49.mm,1218.mm], [1872.642857142857.mm,49.mm,1218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse C (15A — water pumps)
  grp = ents.add_group
  grp.name = "Fuse C (15A — water pumps)"
  face = grp.entities.add_face([1896.0714285714287.mm,40.mm,1218.mm], [1909.0714285714287.mm,40.mm,1218.mm], [1909.0714285714287.mm,49.mm,1218.mm], [1896.0714285714287.mm,49.mm,1218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse D (5A — safelight)
  grp = ents.add_group
  grp.name = "Fuse D (5A — safelight)"
  face = grp.entities.add_face([1919.5.mm,40.mm,1218.mm], [1932.5.mm,40.mm,1218.mm], [1932.5.mm,49.mm,1218.mm], [1919.5.mm,49.mm,1218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse D (5A — safelight)"] || model.materials.add("Fuse D (5A — safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse E (40A — cooler / inverter)
  grp = ents.add_group
  grp.name = "Fuse E (40A — cooler / inverter)"
  face = grp.entities.add_face([1942.9285714285713.mm,40.mm,1218.mm], [1955.9285714285713.mm,40.mm,1218.mm], [1955.9285714285713.mm,49.mm,1218.mm], [1942.9285714285713.mm,49.mm,1218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse E (40A — cooler / inverter)"] || model.materials.add("Fuse E (40A — cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse F (20A — actuators (spare))
  grp = ents.add_group
  grp.name = "Fuse F (20A — actuators (spare))"
  face = grp.entities.add_face([1966.357142857143.mm,40.mm,1218.mm], [1979.357142857143.mm,40.mm,1218.mm], [1979.357142857143.mm,49.mm,1218.mm], [1966.357142857143.mm,49.mm,1218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse F (20A — actuators (spare))"] || model.materials.add("Fuse F (20A — actuators (spare))")
  mat.color = Sketchup::Color.new(127, 140, 141)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse G (10A — white LED)
  grp = ents.add_group
  grp.name = "Fuse G (10A — white LED)"
  face = grp.entities.add_face([1989.7857142857142.mm,40.mm,1218.mm], [2002.7857142857142.mm,40.mm,1218.mm], [2002.7857142857142.mm,49.mm,1218.mm], [1989.7857142857142.mm,49.mm,1218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse G (10A — white LED)"] || model.materials.add("Fuse G (10A — white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Master pump switch (Cct C, on EP)
  grp = ents.add_group
  grp.name = "Master pump switch (Cct C, on EP)"
  face = grp.entities.add_face([1934.mm,0.mm,1045.mm], [1984.mm,0.mm,1045.mm], [1984.mm,46.mm,1045.mm], [1934.mm,46.mm,1045.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(84.mm)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Master switch lever (OFF cutoff)
  grp = ents.add_group
  grp.name = "Master switch lever (OFF cutoff)"
  face = grp.entities.add_face([1951.mm,46.mm,1085.mm], [1967.mm,46.mm,1085.mm], [1967.mm,80.mm,1085.mm], [1951.mm,80.mm,1085.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Master switch lever (OFF cutoff)"] || model.materials.add("Master switch lever (OFF cutoff)")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # Busbar (+)
  grp = ents.add_group
  grp.name = "Busbar (+)"
  face = grp.entities.add_face([1844.mm,30.mm,1320.mm], [1964.mm,30.mm,1320.mm], [1964.mm,50.mm,1320.mm], [1844.mm,50.mm,1320.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Busbar (-)
  grp = ents.add_group
  grp.name = "Busbar (-)"
  face = grp.entities.add_face([1844.mm,30.mm,1290.mm], [1964.mm,30.mm,1290.mm], [1964.mm,50.mm,1290.mm], [1844.mm,50.mm,1290.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Fuse Block base (Blue Sea 5026)"] || model.materials.add("Fuse Block base (Blue Sea 5026)")
  mat.color = Sketchup::Color.new(42, 42, 42)
  mat.alpha = 1.0
  grp.material = mat

  # Main Disconnect (m-Series)
  grp = ents.add_group
  grp.name = "Main Disconnect (m-Series)"
  ge = grp.entities
  circle = ge.add_circle([1884.mm,0.mm,1045.mm], [0,1,0], 35.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Main Disconnect (m-Series)"] || model.materials.add("Main Disconnect (m-Series)")
  mat.color = Sketchup::Color.new(212, 58, 47)
  mat.alpha = 1.0
  grp.material = mat

  # Main feed (disconnect → busbar +)
  grp = ents.add_group
  grp.name = "Main feed (disconnect → busbar +)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.649999999999999.mm, 0.mm)
  circle = ge.add_circle([1884.mm,30.mm,1135.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Main feed (disconnect → busbar +) elbow
  grp = ents.add_group
  grp.name = "Main feed (disconnect → busbar +) elbow"
  ge = grp.entities
  arc = ge.add_arc([1884.mm,37.65.mm,1142.35.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 7.3500000000000005.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1884.mm,37.65.mm,1135.mm], [0.000000,1.000000,0.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Main feed (disconnect → busbar +)
  grp = ents.add_group
  grp.name = "Main feed (disconnect → busbar +)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 158.05000000000018.mm)
  circle = ge.add_circle([1884.mm,45.mm,1142.35.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Main feed (disconnect → busbar +) elbow
  grp = ents.add_group
  grp.name = "Main feed (disconnect → busbar +) elbow"
  ge = grp.entities
  arc = ge.add_arc([1864.4.mm,45.mm,1300.4.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 19.600000000000005.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1884.mm,45.mm,1300.4.mm], [0.000000,0.000000,1.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Main feed (disconnect → busbar +)
  grp = ents.add_group
  grp.name = "Main feed (disconnect → busbar +)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-20.40000000000009.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1864.4.mm,45.mm,1320.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Charge-line Fuse (60A, MPPT -> battery)
  grp = ents.add_group
  grp.name = "Charge-line Fuse (60A, MPPT -> battery)"
  face = grp.entities.add_face([1844.mm,95.mm,1305.mm], [1889.mm,95.mm,1305.mm], [1889.mm,125.mm,1305.mm], [1844.mm,125.mm,1305.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(45.mm)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Interior E-stop collar (safety yellow)
  grp = ents.add_group
  grp.name = "Interior E-stop collar (safety yellow)"
  ge = grp.entities
  circle = ge.add_circle([2099.mm,0.mm,1065.mm], [0,1,0], 30.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(12.mm)
  mat = model.materials["Interior E-stop collar (safety yellow)"] || model.materials.add("Interior E-stop collar (safety yellow)")
  mat.color = Sketchup::Color.new(242, 194, 0)
  mat.alpha = 1.0
  grp.material = mat

  # Interior E-stop button (red mushroom)
  grp = ents.add_group
  grp.name = "Interior E-stop button (red mushroom)"
  ge = grp.entities
  circle = ge.add_circle([2099.mm,12.mm,1065.mm], [0,1,0], 24.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(26.mm)
  mat = model.materials["Interior E-stop button (red mushroom)"] || model.materials.add("Interior E-stop button (red mushroom)")
  mat.color = Sketchup::Color.new(196, 43, 28)
  mat.alpha = 1.0
  grp.material = mat

  # PV feed (MC4 -> array disconnect, top)
  grp = ents.add_group
  grp.name = "PV feed (MC4 -> array disconnect, top)"
  ge = grp.entities
  vec = Geom::Vector3d.new(702.8.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1328.2.mm,22.mm,1884.mm], vec, 9.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV feed (MC4 -> array disconnect, top) elbow
  grp = ents.add_group
  grp.name = "PV feed (MC4 -> array disconnect, top) elbow"
  ge = grp.entities
  arc = ge.add_arc([2031.mm,22.mm,1866.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 18.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2031.mm,22.mm,1884.mm], [1.000000,0.000000,0.000000], 9.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV feed (MC4 -> array disconnect, top)
  grp = ents.add_group
  grp.name = "PV feed (MC4 -> array disconnect, top)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -751.mm)
  circle = ge.add_circle([2049.mm,22.mm,1866.mm], vec, 9.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV feed (array disconnect -> MPPT, top)
  grp = ents.add_group
  grp.name = "PV feed (array disconnect -> MPPT, top)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 357.mm)
  circle = ge.add_circle([2009.mm,22.mm,1115.mm], vec, 9.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV feed (array disconnect -> MPPT, top) elbow
  grp = ents.add_group
  grp.name = "PV feed (array disconnect -> MPPT, top) elbow"
  ge = grp.entities
  arc = ge.add_arc([2009.mm,40.mm,1472.mm], [0.000000,-1.000000,0.000000], [-1.000000,0.000000,0.000000], 18.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2009.mm,22.mm,1472.mm], [0.000000,0.000000,1.000000], 9.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV feed (array disconnect -> MPPT, top)
  grp = ents.add_group
  grp.name = "PV feed (array disconnect -> MPPT, top)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 77.47901099647534.mm, 0.mm)
  circle = ge.add_circle([2009.mm,40.mm,1490.mm], vec, 9.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV feed (array disconnect -> MPPT, top) elbow
  grp = ents.add_group
  grp.name = "PV feed (array disconnect -> MPPT, top) elbow"
  ge = grp.entities
  arc = ge.add_arc([2009.mm,117.47901099647534.mm,1508.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 18.mm, 0.0, 0.278300, 8)
  circle = ge.add_circle([2009.mm,117.47901099647534.mm,1490.mm], [0.000000,1.000000,0.000000], 9.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV feed (array disconnect -> MPPT, top)
  grp = ents.add_group
  grp.name = "PV feed (array disconnect -> MPPT, top)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 32.57600870137186.mm, 9.307431057534814.mm)
  circle = ge.add_circle([2009.mm,122.42399129862814.mm,1490.6925689424652.mm], vec, 9.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop trip line (contactor coil -> interior E-stop)
  grp = ents.add_group
  grp.name = "E-stop trip line (contactor coil -> interior E-stop)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -28.054054863004325.mm, 16.030888493145312.mm)
  circle = ge.add_circle([1899.mm,45.mm,718.mm], vec, 4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["E-stop trip line (contactor coil -> interior E-stop)"] || model.materials.add("E-stop trip line (contactor coil -> interior E-stop)")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop trip line (contactor coil -> interior E-stop) elbow
  grp = ents.add_group
  grp.name = "E-stop trip line (contactor coil -> interior E-stop) elbow"
  ge = grp.entities
  arc = ge.add_arc([1907.mm,16.945945136995675.mm,734.0308884931453.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.496139,0.868243], 8.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1899.mm,16.945945136995675.mm,734.0308884931453.mm], [0.000000,-0.868243,0.496139], 4.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["E-stop trip line (contactor coil -> interior E-stop)"] || model.materials.add("E-stop trip line (contactor coil -> interior E-stop)")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop trip line (contactor coil -> interior E-stop)
  grp = ents.add_group
  grp.name = "E-stop trip line (contactor coil -> interior E-stop)"
  ge = grp.entities
  vec = Geom::Vector3d.new(184.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1907.mm,10.mm,738.mm], vec, 4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["E-stop trip line (contactor coil -> interior E-stop)"] || model.materials.add("E-stop trip line (contactor coil -> interior E-stop)")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop trip line (contactor coil -> interior E-stop) elbow
  grp = ents.add_group
  grp.name = "E-stop trip line (contactor coil -> interior E-stop) elbow"
  ge = grp.entities
  arc = ge.add_arc([2091.mm,10.mm,746.mm], [0.000000,0.000000,-1.000000], [0.000000,-1.000000,0.000000], 8.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2091.mm,10.mm,738.mm], [1.000000,0.000000,0.000000], 4.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["E-stop trip line (contactor coil -> interior E-stop)"] || model.materials.add("E-stop trip line (contactor coil -> interior E-stop)")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop trip line (contactor coil -> interior E-stop)
  grp = ents.add_group
  grp.name = "E-stop trip line (contactor coil -> interior E-stop)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 314.0999999999999.mm)
  circle = ge.add_circle([2099.mm,10.mm,746.mm], vec, 4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["E-stop trip line (contactor coil -> interior E-stop)"] || model.materials.add("E-stop trip line (contactor coil -> interior E-stop)")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop trip line (contactor coil -> interior E-stop) elbow
  grp = ents.add_group
  grp.name = "E-stop trip line (contactor coil -> interior E-stop) elbow"
  ge = grp.entities
  arc = ge.add_arc([2099.mm,5.099999999999999.mm,1060.1.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 4.900000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2099.mm,10.mm,1060.1.mm], [0.000000,0.000000,1.000000], 4.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["E-stop trip line (contactor coil -> interior E-stop)"] || model.materials.add("E-stop trip line (contactor coil -> interior E-stop)")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop trip line (contactor coil -> interior E-stop)
  grp = ents.add_group
  grp.name = "E-stop trip line (contactor coil -> interior E-stop)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -5.1.mm, 0.mm)
  circle = ge.add_circle([2099.mm,5.1.mm,1065.mm], vec, 4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["E-stop trip line (contactor coil -> interior E-stop)"] || model.materials.add("E-stop trip line (contactor coil -> interior E-stop)")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop parallel link (interior -> exterior E-stop)
  grp = ents.add_group
  grp.name = "E-stop parallel link (interior -> exterior E-stop)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.1.mm, 0.mm)
  circle = ge.add_circle([2099.mm,0.mm,1065.mm], vec, 4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["E-stop trip line (contactor coil -> interior E-stop)"] || model.materials.add("E-stop trip line (contactor coil -> interior E-stop)")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop parallel link (interior -> exterior E-stop) elbow
  grp = ents.add_group
  grp.name = "E-stop parallel link (interior -> exterior E-stop) elbow"
  ge = grp.entities
  arc = ge.add_arc([2099.mm,5.1.mm,1069.9.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 4.900000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2099.mm,5.1.mm,1065.mm], [0.000000,1.000000,0.000000], 4.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["E-stop trip line (contactor coil -> interior E-stop)"] || model.materials.add("E-stop trip line (contactor coil -> interior E-stop)")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop parallel link (interior -> exterior E-stop)
  grp = ents.add_group
  grp.name = "E-stop parallel link (interior -> exterior E-stop)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 822.0999999999999.mm)
  circle = ge.add_circle([2099.mm,10.mm,1069.9.mm], vec, 4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["E-stop trip line (contactor coil -> interior E-stop)"] || model.materials.add("E-stop trip line (contactor coil -> interior E-stop)")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop parallel link (interior -> exterior E-stop) elbow
  grp = ents.add_group
  grp.name = "E-stop parallel link (interior -> exterior E-stop) elbow"
  ge = grp.entities
  arc = ge.add_arc([2091.mm,10.mm,1892.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 8.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2099.mm,10.mm,1892.mm], [0.000000,0.000000,1.000000], 4.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["E-stop trip line (contactor coil -> interior E-stop)"] || model.materials.add("E-stop trip line (contactor coil -> interior E-stop)")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop parallel link (interior -> exterior E-stop)
  grp = ents.add_group
  grp.name = "E-stop parallel link (interior -> exterior E-stop)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-663.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2091.mm,10.mm,1900.mm], vec, 4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["E-stop trip line (contactor coil -> interior E-stop)"] || model.materials.add("E-stop trip line (contactor coil -> interior E-stop)")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop parallel link (interior -> exterior E-stop) elbow
  grp = ents.add_group
  grp.name = "E-stop parallel link (interior -> exterior E-stop) elbow"
  ge = grp.entities
  arc = ge.add_arc([1428.mm,10.mm,1908.mm], [0.000000,0.000000,-1.000000], [0.000000,1.000000,-0.000000], 8.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1428.mm,10.mm,1900.mm], [-1.000000,0.000000,0.000000], 4.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["E-stop trip line (contactor coil -> interior E-stop)"] || model.materials.add("E-stop trip line (contactor coil -> interior E-stop)")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop parallel link (interior -> exterior E-stop)
  grp = ents.add_group
  grp.name = "E-stop parallel link (interior -> exterior E-stop)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 34.mm)
  circle = ge.add_circle([1420.mm,10.mm,1908.mm], vec, 4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["E-stop trip line (contactor coil -> interior E-stop)"] || model.materials.add("E-stop trip line (contactor coil -> interior E-stop)")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop parallel link (interior -> exterior E-stop) elbow
  grp = ents.add_group
  grp.name = "E-stop parallel link (interior -> exterior E-stop) elbow"
  ge = grp.entities
  arc = ge.add_arc([1420.mm,2.mm,1942.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 8.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1420.mm,10.mm,1942.mm], [0.000000,0.000000,1.000000], 4.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["E-stop trip line (contactor coil -> interior E-stop)"] || model.materials.add("E-stop trip line (contactor coil -> interior E-stop)")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop parallel link (interior -> exterior E-stop)
  grp = ents.add_group
  grp.name = "E-stop parallel link (interior -> exterior E-stop)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -42.mm, 0.mm)
  circle = ge.add_circle([1420.mm,2.000000000000001.mm,1950.mm], vec, 4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["E-stop trip line (contactor coil -> interior E-stop)"] || model.materials.add("E-stop trip line (contactor coil -> interior E-stop)")
  mat.color = Sketchup::Color.new(88, 96, 112)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Power Core"
  inst.layer = model.layers["Power Core"]

  # ═══ Battery Bank ═══
  defn = model.definitions.add("Battery Bank")
  ents = defn.entities
  # Battery 1 (12V 100Ah LiFePO4)
  grp = ents.add_group
  grp.name = "Battery 1 (12V 100Ah LiFePO4)"
  face = grp.entities.add_face([1829.mm,0.mm,160.mm], [2089.mm,0.mm,160.mm], [2089.mm,169.mm,160.mm], [1829.mm,169.mm,160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(211.mm)
  mat = model.materials["Battery 1 (12V 100Ah LiFePO4)"] || model.materials.add("Battery 1 (12V 100Ah LiFePO4)")
  mat.color = Sketchup::Color.new(106, 90, 205)
  mat.alpha = 1.0
  grp.material = mat

  # Battery 2 (optional 2nd pack, ghosted)
  grp = ents.add_group
  grp.name = "Battery 2 (optional 2nd pack, ghosted)"
  face = grp.entities.add_face([1829.mm,0.mm,387.mm], [2089.mm,0.mm,387.mm], [2089.mm,169.mm,387.mm], [1829.mm,169.mm,387.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(211.mm)
  mat = model.materials["Battery 2 (optional 2nd pack, ghosted)"] || model.materials.add("Battery 2 (optional 2nd pack, ghosted)")
  mat.color = Sketchup::Color.new(106, 90, 205)
  mat.alpha = 0.28
  grp.material = mat

  # Battery Contactor (ML-RBS)
  grp = ents.add_group
  grp.name = "Battery Contactor (ML-RBS)"
  face = grp.entities.add_face([1839.mm,15.mm,618.mm], [1959.mm,15.mm,618.mm], [1959.mm,105.mm,618.mm], [1839.mm,105.mm,618.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Interior E-stop button (red mushroom)"] || model.materials.add("Interior E-stop button (red mushroom)")
  mat.color = Sketchup::Color.new(196, 43, 28)
  mat.alpha = 1.0
  grp.material = mat

  # MRBF Main Fuse (on + post)
  grp = ents.add_group
  grp.name = "MRBF Main Fuse (on + post)"
  face = grp.entities.add_face([1979.mm,20.mm,618.mm], [2019.mm,20.mm,618.mm], [2019.mm,60.mm,618.mm], [1979.mm,60.mm,618.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(38.mm)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF → main disconnect)
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF → main disconnect)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 332.mm)
  circle = ge.add_circle([1999.mm,45.mm,656.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF → main disconnect) elbow
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF → main disconnect) elbow"
  ge = grp.entities
  arc = ge.add_arc([1977.mm,45.mm,988.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 22.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1999.mm,45.mm,988.mm], [0.000000,0.000000,1.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF → main disconnect)
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF → main disconnect)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-85.65000000000009.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1977.mm,45.mm,1010.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF → main disconnect) elbow
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF → main disconnect) elbow"
  ge = grp.entities
  arc = ge.add_arc([1891.35.mm,37.65.mm,1010.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 7.3500000000000005.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1891.35.mm,45.mm,1010.mm], [-1.000000,0.000000,0.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF → main disconnect)
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF → main disconnect)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.649999999999999.mm, 0.mm)
  circle = ge.add_circle([1884.mm,37.65.mm,1010.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery − cable (2/0 AWG)
  grp = ents.add_group
  grp.name = "Battery − cable (2/0 AWG)"
  ge = grp.entities
  vec = Geom::Vector3d.new(78.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1869.mm,60.mm,598.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery − cable (2/0 AWG) elbow
  grp = ents.add_group
  grp.name = "Battery − cable (2/0 AWG) elbow"
  ge = grp.entities
  arc = ge.add_arc([1947.mm,60.mm,620.mm], [0.000000,0.000000,-1.000000], [0.000000,-1.000000,0.000000], 22.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1947.mm,60.mm,598.mm], [1.000000,0.000000,0.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery − cable (2/0 AWG)
  grp = ents.add_group
  grp.name = "Battery − cable (2/0 AWG)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 658.mm)
  circle = ge.add_circle([1969.mm,60.mm,620.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery − cable (2/0 AWG) elbow
  grp = ents.add_group
  grp.name = "Battery − cable (2/0 AWG) elbow"
  ge = grp.entities
  arc = ge.add_arc([1947.mm,60.mm,1278.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 22.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1969.mm,60.mm,1278.mm], [0.000000,0.000000,1.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery − cable (2/0 AWG)
  grp = ents.add_group
  grp.name = "Battery − cable (2/0 AWG)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-78.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1947.mm,60.mm,1300.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (-) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (-) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Battery Bank"
  inst.layer = model.layers["Battery"]

  # ═══ External Power Panel ═══
  defn = model.definitions.add("External Power Panel")
  ents = defn.entities
  # EP box front face (flange)
  grp = ents.add_group
  grp.name = "EP box front face (flange)"
  face = grp.entities.add_face([1250.mm,-65.mm,1830.mm], [1590.mm,-65.mm,1830.mm], [1590.mm,-62.mm,1830.mm], [1250.mm,-62.mm,1830.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(240.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # EP box shroud (left)
  grp = ents.add_group
  grp.name = "EP box shroud (left)"
  face = grp.entities.add_face([1272.mm,-62.mm,1852.mm], [1280.mm,-62.mm,1852.mm], [1280.mm,28.mm,1852.mm], [1272.mm,28.mm,1852.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(196.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # EP box shroud (right)
  grp = ents.add_group
  grp.name = "EP box shroud (right)"
  face = grp.entities.add_face([1560.mm,-62.mm,1852.mm], [1568.mm,-62.mm,1852.mm], [1568.mm,28.mm,1852.mm], [1560.mm,28.mm,1852.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(196.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # EP box shroud (bottom)
  grp = ents.add_group
  grp.name = "EP box shroud (bottom)"
  face = grp.entities.add_face([1272.mm,-62.mm,1852.mm], [1568.mm,-62.mm,1852.mm], [1568.mm,28.mm,1852.mm], [1272.mm,28.mm,1852.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # EP box shroud (top)
  grp = ents.add_group
  grp.name = "EP box shroud (top)"
  face = grp.entities.add_face([1272.mm,-62.mm,2040.mm], [1568.mm,-62.mm,2040.mm], [1568.mm,28.mm,2040.mm], [1272.mm,28.mm,2040.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Stay inside plate"] || model.materials.add("Stay inside plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
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

  # NEMA 5-15 shore inlet
  grp = ents.add_group
  grp.name = "NEMA 5-15 shore inlet"
  face = grp.entities.add_face([1472.28.mm,-95.mm,2018.72.mm], [1532.28.mm,-95.mm,2018.72.mm], [1532.28.mm,-65.mm,2018.72.mm], [1472.28.mm,-65.mm,2018.72.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(45.mm)
  mat = model.materials["NEMA 5-15 shore inlet"] || model.materials.add("NEMA 5-15 shore inlet")
  mat.color = Sketchup::Color.new(255, 240, 204)
  mat.alpha = 1.0
  grp.material = mat

  # NEMA inlet weatherproof cover
  grp = ents.add_group
  grp.name = "NEMA inlet weatherproof cover"
  face = grp.entities.add_face([1466.28.mm,-107.mm,2012.72.mm], [1538.28.mm,-107.mm,2012.72.mm], [1538.28.mm,-95.mm,2012.72.mm], [1466.28.mm,-95.mm,2012.72.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(57.mm)
  mat = model.materials["NEMA inlet weatherproof cover"] || model.materials.add("NEMA inlet weatherproof cover")
  mat.color = Sketchup::Color.new(214, 230, 245)
  mat.alpha = 0.5
  grp.material = mat

  # WR duplex outlet (Cct E cooler)
  grp = ents.add_group
  grp.name = "WR duplex outlet (Cct E cooler)"
  face = grp.entities.add_face([1487.78.mm,-87.mm,1903.008.mm], [1533.78.mm,-87.mm,1903.008.mm], [1533.78.mm,-65.mm,1903.008.mm], [1487.78.mm,-65.mm,1903.008.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["NEMA 5-15 shore inlet"] || model.materials.add("NEMA 5-15 shore inlet")
  mat.color = Sketchup::Color.new(255, 240, 204)
  mat.alpha = 1.0
  grp.material = mat

  # WR duplex in-use cover
  grp = ents.add_group
  grp.name = "WR duplex in-use cover"
  face = grp.entities.add_face([1481.78.mm,-101.mm,1897.008.mm], [1539.78.mm,-101.mm,1897.008.mm], [1539.78.mm,-87.mm,1897.008.mm], [1481.78.mm,-87.mm,1897.008.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(72.mm)
  mat = model.materials["NEMA inlet weatherproof cover"] || model.materials.add("NEMA inlet weatherproof cover")
  mat.color = Sketchup::Color.new(214, 230, 245)
  mat.alpha = 0.5
  grp.material = mat

  # E-stop collar (safety yellow)
  grp = ents.add_group
  grp.name = "E-stop collar (safety yellow)"
  ge = grp.entities
  circle = ge.add_circle([1420.mm,-77.mm,1950.mm], [0,1,0], 35.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(12.mm)
  mat = model.materials["Interior E-stop collar (safety yellow)"] || model.materials.add("Interior E-stop collar (safety yellow)")
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
  mat = model.materials["Interior E-stop button (red mushroom)"] || model.materials.add("Interior E-stop button (red mushroom)")
  mat.color = Sketchup::Color.new(196, 43, 28)
  mat.alpha = 1.0
  grp.material = mat

  # PV Array Disconnect (load-break isolator)
  grp = ents.add_group
  grp.name = "PV Array Disconnect (load-break isolator)"
  face = grp.entities.add_face([1994.mm,0.mm,1045.mm], [2064.mm,0.mm,1045.mm], [2064.mm,45.mm,1045.mm], [1994.mm,45.mm,1045.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Main Disconnect (m-Series)"] || model.materials.add("Main Disconnect (m-Series)")
  mat.color = Sketchup::Color.new(212, 58, 47)
  mat.alpha = 1.0
  grp.material = mat

  # PV disconnect lever (red switch)
  grp = ents.add_group
  grp.name = "PV disconnect lever (red switch)"
  face = grp.entities.add_face([2022.mm,45.mm,1065.mm], [2036.mm,45.mm,1065.mm], [2036.mm,85.mm,1065.mm], [2022.mm,85.mm,1065.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Master switch lever (OFF cutoff)"] || model.materials.add("Master switch lever (OFF cutoff)")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # Evap Cooler (Hessaire MC18M, external)
  grp = ents.add_group
  grp.name = "Evap Cooler (Hessaire MC18M, external)"
  face = grp.entities.add_face([746.mm,-394.mm,0.mm], [1254.mm,-394.mm,0.mm], [1254.mm,-140.mm,0.mm], [746.mm,-140.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(711.mm)
  mat = model.materials["Evap Cooler (Hessaire MC18M, external)"] || model.materials.add("Evap Cooler (Hessaire MC18M, external)")
  mat.color = Sketchup::Color.new(61, 170, 150)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-33.67800000000011.mm, -19.200000000000003.mm, -129.20080000000007.mm)
  circle = ge.add_circle([1510.78.mm,-75.mm,1933.008.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.966373224972585.mm, -20.470150400952107.mm, -2.9682282298904283.mm)
  circle = ge.add_circle([1477.1019999999999.mm,-94.2.mm,1803.8072.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.759890839617356.mm, 18.262731376249448.mm, -11.645289392795576.mm)
  circle = ge.add_circle([1455.1356267750273.mm,-114.67015040095211.mm,1800.8389717701095.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.098476936704174.mm, 17.68217736709191.mm, -15.692721552620242.mm)
  circle = ge.add_circle([1444.37573593541.mm,-96.40741902470266.mm,1789.193682377314.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.333276291792345.mm, 5.823606093500217.mm, -16.858975973860424.mm)
  circle = ge.add_circle([1449.474212872114.mm,-78.72524165761075.mm,1773.5009608246937.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.373347824044913.mm, -10.376982997526383.mm, -14.461918204214044.mm)
  circle = ge.add_circle([1465.8074891639064.mm,-72.90163556411053.mm,1756.6419848508333.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.19525396082895.mm, -21.44397312349608.mm, -9.903571386361364.mm)
  circle = ge.add_circle([1482.1808369879514.mm,-83.27861856163692.mm,1742.1800666466193.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.663012561207779.mm, -20.904355384541404.mm, -5.850082248978424.mm)
  circle = ge.add_circle([1487.3760909487803.mm,-104.722591685133.mm,1732.276495260258.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.926057152821613.mm, -9.073748606288973.mm, -4.672309622075545.mm)
  circle = ge.add_circle([1476.7130783875725.mm,-125.6269470696744.mm,1726.4264130112795.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.006199961473385.mm, 7.128204011547922.mm, -7.05912487981891.mm)
  circle = ge.add_circle([1454.787021234751.mm,-134.70069567596337.mm,1721.754103389204.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.856565991543903.mm, 18.225088168717193.mm, -11.614495656602003.mm)
  circle = ge.add_circle([1432.7808212732775.mm,-127.57249166441545.mm,1714.694978509385.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.001498022568057.mm, 17.72641014537723.mm, -15.67401589037081.mm)
  circle = ge.add_circle([1421.9242552817336.mm,-109.34740349569826.mm,1703.080482852783.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.29271593715839.mm, 5.923843399849332.mm, -16.863299202962253.mm)
  circle = ge.add_circle([1426.9257533043017.mm,-91.62099335032103.mm,1687.4064669624122.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.412929510503773.mm, -10.279369296753416.mm, -14.48674169672654.mm)
  circle = ge.add_circle([1443.21846924146.mm,-85.6971499504717.mm,1670.54316775945.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.2918266232945825.mm, -21.40607663249162.mm, -9.93437604665587.mm)
  circle = ge.add_circle([1459.6313987519638.mm,-95.97651924722511.mm,1656.0564260627234.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.565933630547306.mm, -20.948341508781724.mm, -5.868850636181378.mm)
  circle = ge.add_circle([1464.9232253752584.mm,-117.38259587971673.mm,1646.1220500160675.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.885252774678065.mm, -9.173890154330365.mm, -4.668064231371545.mm)
  circle = ge.add_circle([1454.3572917447111.mm,-138.33093738849846.mm,1640.2531993798862.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.045536345165146.mm, 7.030479164948332.mm, -7.034348811987911.mm)
  circle = ge.add_circle([1432.472038970033.mm,-147.50482754282882.mm,1635.5851351485146.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.953035547940999.mm, 18.18693863620618.mm, -11.583680268891158.mm)
  circle = ge.add_circle([1410.426502624868.mm,-140.4743483778805.mm,1628.5507863365267.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.904319695224103.mm, 17.77014933472509.mm, -15.655184898048674.mm)
  circle = ge.add_circle([1399.473467076927.mm,-122.28740974167431.mm,1616.9671060676355.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.251667796037054.mm, 6.023888550187962.mm, -16.867466728161617.mm)
  circle = ge.add_circle([1404.377786772151.mm,-104.51726040694922.mm,1601.3119211695869.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.4520203402692.mm, -10.181533928291742.mm, -14.51147018168399.mm)
  circle = ge.add_circle([1420.629454568188.mm,-98.49337185676126.mm,1584.4444544414253.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.38819245767354.mm, -21.367674302055462.mm, -9.965201965029564.mm)
  circle = ge.add_circle([1437.0814749084573.mm,-108.674905785053.mm,1569.9329842597413.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.468656526994437.mm, -20.991833483966246.mm, -5.887744113388408.mm)
  circle = ge.add_circle([1442.4696673661308.mm,-130.04258008710846.mm,1559.9677822947117.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.84396113266871.mm, -9.273838268186807.mm, -4.6639745982849945.mm)
  circle = ge.add_circle([1432.0010108391364.mm,-151.0344135710747.mm,1554.0800381813233.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.084381371412064.mm, 6.932533899294725.mm, -7.009668067793655.mm)
  circle = ge.add_circle([1410.1570497064677.mm,-160.30825183926152.mm,1549.4160635830383.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.049297045014555.mm, 18.148283753040573.mm, -11.552844016675635.mm)
  circle = ge.add_circle([1388.0726683350556.mm,-153.3757179399668.mm,1542.4063955152446.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.806944436568074.mm, 17.813393818053754.mm, -15.63622905659031.mm)
  circle = ge.add_circle([1377.023371290041.mm,-135.22743418692622.mm,1530.853551498569.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.210132916783323.mm, 6.123738989402284.mm, -16.871478443022852.mm)
  circle = ge.add_circle([1381.8303157266091.mm,-117.41404036887246.mm,1515.2173224419787.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.490619314975447.mm, -10.083479390818155.mm, -14.536103027530544.mm)
  circle = ge.add_circle([1398.0404486433924.mm,-111.29030137947018.mm,1498.3458439989558.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.484349002820409.mm, -21.328767112968478.mm, -9.99604835419973.mm)
  circle = ge.add_circle([1414.5310679583679.mm,-121.37378077028833.mm,1483.8097409714253.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.371183734968099.mm, -21.034830199326763.mm, -5.906762198067327.mm)
  circle = ge.add_circle([1420.0154169611883.mm,-142.7025478832568.mm,1473.8136926172256.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.802183281366524.mm, -9.373590395222635.mm, -4.660040827264083.mm)
  circle = ge.add_circle([1409.6442332262202.mm,-163.73737808258358.mm,1467.9069304191582.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.122734048127086.mm, 6.834370716070822.mm, -6.98508327757304.mm)
  circle = ge.add_circle([1387.8420499448537.mm,-173.1109684778062.mm,1463.2468895918942.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.145348024283294.mm, 18.10912450645108.mm, -11.521987687501905.mm)
  circle = ge.add_circle([1365.7193158967266.mm,-166.2765977617354.mm,1456.2618063143211.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.709374733526374.mm, 17.856142490915857.mm, -15.617148850119975.mm)
  circle = ge.add_circle([1354.5739678724433.mm,-148.1674732552843.mm,1444.7398186268192.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.168112360180658.mm, 6.223392167351136.mm, -16.87533424508706.mm)
  circle = ge.add_circle([1359.2833426059697.mm,-130.31133076436845.mm,1429.1226697766992.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.52872544882098.mm, -9.985208188607203.mm, -14.560639605153256.mm)
  circle = ge.add_circle([1375.4514549661503.mm,-124.08793859701731.mm,1412.2473355316122.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.580293802934193.mm, -21.289356058904616.mm, -10.02691442636251.mm)
  circle = ge.add_circle([1391.9801804149713.mm,-134.07314678562452.mm,1397.686695926459.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.273517743884895.mm, -21.077330556744215.mm, -5.925904404502944.mm)
  circle = ge.add_circle([1397.5604742179055.mm,-155.36250284452913.mm,1387.6597815000964.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.759920287761588.mm, -9.473143987807731.mm, -4.656263018775462.mm)
  circle = ge.add_circle([1387.2869564740206.mm,-176.43983340127335.mm,1381.7338770955935.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.160593395798287.mm, 6.735992122325769.mm, -6.960595069212104.mm)
  circle = ge.add_circle([1365.527036186259.mm,-185.91297738908108.mm,1377.077614076818.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.2411860326431.mm, 18.069461896549342.mm, -11.491112069428027.mm)
  circle = ge.add_circle([1343.3664427904607.mm,-179.1769852667553.mm,1370.117019007606.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.611613077991024.mm, 17.898394261527358.mm, -15.597944765939701.mm)
  circle = ge.add_circle([1332.1252567578176.mm,-161.10752337020597.mm,1358.6259069381779.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.125607199418027.mm, 6.322845538931432.mm, -16.879034035879158.mm)
  circle = ge.add_circle([1336.7368698358086.mm,-143.2091291086786.mm,1343.0279621722382.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.56633776858962.mm, -9.88672283146687.mm, -14.585079287897088.mm)
  circle = ge.add_circle([1352.8624770352267.mm,-136.88628356974718.mm,1326.148928136359.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.676024407622435.mm, -21.249442146407034.mm, -10.057799393209734.mm)
  circle = ge.add_circle([1369.4288148038163.mm,-146.77300640121405.mm,1311.563848848462.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.175661048096345.mm, -21.119333470775842.mm, -5.945170243811617.mm)
  circle = ge.add_circle([1375.1048392114387.mm,-168.02244854762108.mm,1301.5060494552522.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.717173231233346.mm, -9.572496503382382.mm, -4.652641269302649.mm)
  circle = ge.add_circle([1364.9291781633424.mm,-189.14178201839692.mm,1295.5608792114406.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.197958447512747.mm, 6.63740063061033.mm, -6.936204068130564.mm)
  circle = ge.add_circle([1343.212004932109.mm,-198.7142785217793.mm,1290.908237942138.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.33680862242909.mm, 18.029296936302813.mm, -11.460217951004779.mm)
  circle = ge.add_circle([1321.0140464845963.mm,-192.07687789116898.mm,1283.9720338740074.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.513661966756217.mm, 17.94014805079445.mm, -15.578617294513606.mm)
  circle = ge.add_circle([1309.6772378621672.mm,-174.04758095486616.mm,1272.5118159230026.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.082618520060578.mm, 6.4220965641432315.mm, -16.882577720908102.mm)
  circle = ge.add_circle([1314.1908998289234.mm,-156.10743290407171.mm,1256.933198628489.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.60345531367716.mm, -9.788025834674443.mm, -14.60942145158242.mm)
  circle = ge.add_circle([1330.273518348984.mm,-149.68533633992848.mm,1240.0506209075809.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.771538371963743.mm, -21.209026394861326.mm, -10.088702465951883.mm)
  circle = ge.add_circle([1346.8769736626612.mm,-159.47336217460293.mm,1225.4411994559985.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.077616146824312.mm, -21.160837868684098.mm, -5.964559223951028.mm)
  circle = ge.add_circle([1352.648512034625.mm,-180.68238856946425.mm,1215.3524969900466.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.673943203525596.mm, -9.671645404522138.mm, -4.64917567134421.mm)
  circle = ge.add_circle([1342.5708958878006.mm,-201.84322643814835.mm,1209.3879377660955.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.23482824898133.mm, 6.538598758912713.mm, -6.911910897264079.mm)
  circle = ge.add_circle([1320.896952684275.mm,-211.5148718426705.mm,1204.7387620947513.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.432213351477003.mm, 17.98863065150877.mm, -11.429306121256559.mm)
  circle = ge.add_circle([1298.6621244352937.mm,-204.97627308375777.mm,1197.8268511974873.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.415523901454662.mm, 17.981402792341868.mm, -15.559166929457888.mm)
  circle = ge.add_circle([1287.2299110838167.mm,-186.987642432249.mm,1186.3975450762307.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.039147420022573.mm, 6.521142708154002.mm, -16.885965209669166.mm)
  circle = ge.add_circle([1291.6454349852713.mm,-169.00623963990714.mm,1170.8383781467728.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.64007713611636.mm, -9.689119718912622.mm, -14.63366547451983.mm)
  circle = ge.add_circle([1307.684582405294.mm,-162.48509693175313.mm,1153.9524129371036.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.866833256568043.mm, -21.16810983647008.mm, -10.119622855336956.mm)
  circle = ge.add_circle([1324.3246595414103.mm,-172.17421665066576.mm,1139.3187474625838.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.979385544096658.mm, -21.201842690462456.mm, -5.984070849734508.mm)
  circle = ge.add_circle([1330.1914927979783.mm,-193.34232648713584.mm,1129.1991246072469.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.630231308715793.mm, -9.770588159003125.mm, -4.6458663134089875.mm)
  circle = ge.add_circle([1320.2121072538816.mm,-214.5441691775983.mm,1123.2150537575124.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.27120185856461.mm, 6.439589030593709.mm, -6.887716177051743.mm)
  circle = ge.add_circle([1298.5818759451658.mm,-224.31475733660142.mm,1118.5691874441034.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.527397783188007.mm, 17.94746408076861.mm, -11.398377369659329.mm)
  circle = ge.add_circle([1276.3106740866012.mm,-217.8751683060077.mm,1111.6814712670516.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.317201388494368.mm, 18.022157432539245.mm, -15.539594167526502.mm)
  circle = ge.add_circle([1264.7832763034132.mm,-199.9277042252391.mm,1100.2830938973923.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(15.995195009538293.mm, 6.6199814413643026.mm, -16.889196415647348.mm)
  circle = ge.add_circle([1269.1004776919076.mm,-181.90554679269985.mm,1084.7434997298658.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.676202300600607.mm, -9.590007010204943.mm, -14.657810737526688.mm)
  circle = ge.add_circle([1285.095672701446.mm,-175.28556535133555.mm,1067.8543033142184.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.961906627641611.mm, -21.12669351622563.mm, -10.150559771669577.mm)
  circle = ge.add_circle([1301.7718750020465.mm,-184.8755723615405.mm,1053.1964925766918.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.880971748684487.mm, -21.242346888864432.mm, -6.003704622842406.mm)
  circle = ge.add_circle([1307.733781629688.mm,-206.00226587776612.mm,1043.0459328050222.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.586038663189356.mm, -9.869322239865994.mm, -4.642713280018597.mm)
  circle = ge.add_circle([1297.8528098810036.mm,-227.24461276663055.mm,1037.0422281821798.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.307078347293555.mm, 6.340373974323086.mm, -6.863620525416081.mm)
  circle = ge.add_circle([1276.2667712178143.mm,-237.11393500649655.mm,1032.3995149021612.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.622359486589176.mm, 17.905798275459915.mm, -11.367432486120947.mm)
  circle = ge.add_circle([1253.9596928705207.mm,-230.77356103217346.mm,1025.535894376745.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.218696938993844.mm, 18.06241093052958.mm, -15.519899508601611.mm)
  circle = ge.add_circle([1242.3373333839315.mm,-212.86776275671355.mm,1014.1684618906241.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(15.950762411135429.mm, 6.718610239471559.mm, -16.89227125631885.mm)
  circle = ge.add_circle([1246.5560303229254.mm,-194.80535182618397.mm,998.6485623820225.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.711829884506642.mm, -9.490690239850892.mm, -14.681856623942167.mm)
  circle = ge.add_circle([1262.5067927340608.mm,-188.0867415867124.mm,981.7562911257037.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(6.0567560570480055.mm, -21.084778491885032.mm, -10.181512424833159.mm)
  circle = ge.add_circle([1279.2186226185675.mm,-197.5774318265633.mm,967.0744345017615.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.782377274037572.mm, -21.28234942942828.mm, -6.023460041836188.mm)
  circle = ge.add_circle([1285.2753786756155.mm,-218.66221031844833.mm,956.8929220769284.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.54136639560852.mm, -9.967845125481233.mm, -4.639716651698791.mm)
  circle = ge.add_circle([1275.4930014015779.mm,-239.9445597478766.mm,950.8694620350922.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.342456798897956.mm, 6.240956124014588.mm, -6.8396245577513355.mm)
  circle = ge.add_circle([1253.9516350059694.mm,-249.91240487335784.mm,946.2297453833934.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.717096036395105.mm, 17.863634299711066.mm, -11.336472260961727.mm)
  circle = ge.add_circle([1231.6091782070714.mm,-243.67144874934326.mm,939.390120825642.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.120013068717753.mm, 18.10216225825431.mm, -15.500083455675963.mm)
  circle = ge.add_circle([1219.8920821706763.mm,-225.8078144496322.mm,928.0536485646803.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(15.905850759605073.mm, 6.81702658353467.mm, -16.89518965315392.mm)
  circle = ge.add_circle([1224.012095239394.mm,-207.70565219137788.mm,912.5535651090044.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.746958977920485.mm, -9.3911719443619.mm, -14.705802519643612.mm)
  circle = ge.add_circle([1239.9179459989991.mm,-200.8886256078432.mm,895.6583754558504.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(6.15137912236969.mm, -21.042365833941716.mm, -10.212480024309684.mm)
  circle = ge.add_circle([1256.6649049769196.mm,-210.2797975522051.mm,880.9525729362068.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.683604638220459.mm, -21.32184929050473.mm, -6.043336602169916.mm)
  circle = ge.add_circle([1262.8162840992893.mm,-231.32216338614683.mm,870.7400929118971.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.496215646885275.mm, -10.066154299612691.mm, -4.636876504982638.mm)
  circle = ge.add_circle([1253.1326794610688.mm,-252.64401267665156.mm,864.6967563097272.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.37733630982507.mm, 6.141338018760791.mm, -6.815728886905276.mm)
  circle = ge.add_circle([1231.6364638141836.mm,-262.71016697626425.mm,860.0598798047446.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.811605013072722.mm, 17.820973230373966.mm, -11.305497484893635.mm)
  circle = ge.add_circle([1209.2591275043585.mm,-256.56882895750346.mm,853.2441509178393.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.021152298013703.mm, 18.141410400479373.mm, -15.480146514843796.mm)
  circle = ge.add_circle([1197.4475224912858.mm,-238.7478557271295.mm,841.9386534329457.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(15.860461201973294.mm, 6.915227960039402.mm, -16.897951531617082.mm)
  circle = ge.add_circle([1201.4686747892995.mm,-220.60644532665012.mm,826.4585069181019.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.781588683658583.mm, -9.291454665396373.mm, -14.729647813062797.mm)
  circle = ge.add_circle([1217.3291359912728.mm,-213.69121736661072.mm,809.5605553864848.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(6.245773406971011.mm, -20.99945662559759.mm, -10.243461779198242.mm)
  circle = ge.add_circle([1234.1107246749314.mm,-222.9826720320071.mm,794.830907573422.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.584656363846989.mm, -21.360845463283113.mm, -6.063333796204688.mm)
  circle = ge.add_circle([1240.3564980819024.mm,-243.98212865760468.mm,784.5874457942238.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.450587570153175.mm, -10.164247251483118.mm, -4.634192912406206.mm)
  circle = ge.add_circle([1230.7718417180554.mm,-265.3429741208878.mm,778.5241119980191.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.6432541479023257.mm, 27.707221372370896.mm, -3.689119085613015.mm)
  circle = ge.add_circle([1209.3212541479022.mm,-275.5072213723709.mm,773.8899190856129.mm], vec, 5.mm, 8)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-33.677999999999884.mm, -19.19999999999999.mm, -129.20079999999984.mm)
  circle = ge.add_circle([1207.6779999999999.mm,-247.8.mm,770.2007999999998.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "External Power Panel"
  inst.layer = model.layers["External Panel"]

  # ═══ Circuit-E Inverter ═══
  defn = model.definitions.add("Circuit-E Inverter")
  ents = defn.entities
  # Cct E Inverter (12->120V AC)
  grp = ents.add_group
  grp.name = "Cct E Inverter (12->120V AC)"
  face = grp.entities.add_face([1829.mm,0.mm,760.mm], [1949.mm,0.mm,760.mm], [1949.mm,72.mm,760.mm], [1829.mm,72.mm,760.mm])
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 924.008.mm)
  circle = ge.add_circle([1889.mm,30.mm,995.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E AC line (inverter -> panel GFCI) elbow
  grp = ents.add_group
  grp.name = "Cct E AC line (inverter -> panel GFCI) elbow"
  ge = grp.entities
  arc = ge.add_arc([1875.mm,30.mm,1919.008.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 14.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1889.mm,30.mm,1919.008.mm], [0.000000,0.000000,1.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E AC line (inverter -> panel GFCI)
  grp = ents.add_group
  grp.name = "Cct E AC line (inverter -> panel GFCI)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-358.3399999999999.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1875.mm,30.mm,1933.008.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E AC line (inverter -> panel GFCI) elbow
  grp = ents.add_group
  grp.name = "Cct E AC line (inverter -> panel GFCI) elbow"
  ge = grp.entities
  arc = ge.add_arc([1516.66.mm,24.119999999999997.mm,1933.008.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 5.880000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1516.66.mm,30.mm,1933.008.mm], [-1.000000,0.000000,0.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E AC line (inverter -> panel GFCI)
  grp = ents.add_group
  grp.name = "Cct E AC line (inverter -> panel GFCI)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -6.120000000000001.mm, 0.mm)
  circle = ge.add_circle([1510.78.mm,24.12.mm,1933.008.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct E cooler cord (panel GFCI -> cooler, flexible)"] || model.materials.add("Cct E cooler cord (panel GFCI -> cooler, flexible)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Circuit-E Inverter"
  inst.layer = model.layers["Inverter"]

  # ═══ Circuit Runs ═══
  defn = model.definitions.add("Circuit Runs")
  ents = defn.entities
  # Cable Trunking (40x25 PVC)
  grp = ents.add_group
  grp.name = "Cable Trunking (40x25 PVC)"
  face = grp.entities.add_face([260.mm,0.mm,2363.mm], [5658.mm,0.mm,2363.mm], [5658.mm,40.mm,2363.mm], [260.mm,40.mm,2363.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["MC4 PV1 (-)"] || model.materials.add("MC4 PV1 (-)")
  mat.color = Sketchup::Color.new(154, 160, 166)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit A (exhaust fan)
  grp = ents.add_group
  grp.name = "Circuit A (exhaust fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 118.5.mm, 0.mm)
  circle = ge.add_circle([1855.7142857142858.mm,44.5.mm,1260.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit A (exhaust fan) elbow
  grp = ents.add_group
  grp.name = "Circuit A (exhaust fan) elbow"
  ge = grp.entities
  arc = ge.add_arc([1855.7142857142858.mm,163.mm,1272.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1855.7142857142858.mm,163.mm,1260.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit A (exhaust fan)
  grp = ents.add_group
  grp.name = "Circuit A (exhaust fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1091.mm)
  circle = ge.add_circle([1855.7142857142858.mm,175.mm,1272.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit A (exhaust fan) elbow
  grp = ents.add_group
  grp.name = "Circuit A (exhaust fan) elbow"
  ge = grp.entities
  arc = ge.add_arc([1855.7142857142858.mm,163.mm,2363.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1855.7142857142858.mm,175.mm,2363.mm], [0.000000,0.000000,1.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit A (exhaust fan)
  grp = ents.add_group
  grp.name = "Circuit A (exhaust fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -131.mm, 0.mm)
  circle = ge.add_circle([1855.7142857142858.mm,163.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit A (exhaust fan) elbow
  grp = ents.add_group
  grp.name = "Circuit A (exhaust fan) elbow"
  ge = grp.entities
  arc = ge.add_arc([1867.7142857142858.mm,32.mm,2375.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.000000,1.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1855.7142857142858.mm,32.mm,2375.mm], [0.000000,-1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit A (exhaust fan)
  grp = ents.add_group
  grp.name = "Circuit A (exhaust fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3738.285714285714.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1867.7142857142858.mm,20.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit A (exhaust fan) elbow
  grp = ents.add_group
  grp.name = "Circuit A (exhaust fan) elbow"
  ge = grp.entities
  arc = ge.add_arc([5606.mm,32.mm,2375.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5606.mm,20.mm,2375.mm], [1.000000,0.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit A (exhaust fan)
  grp = ents.add_group
  grp.name = "Circuit A (exhaust fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 1137.mm, 0.mm)
  circle = ge.add_circle([5618.mm,32.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit A (exhaust fan) elbow
  grp = ents.add_group
  grp.name = "Circuit A (exhaust fan) elbow"
  ge = grp.entities
  arc = ge.add_arc([5618.mm,1169.mm,2363.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5618.mm,1169.mm,2375.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit A (exhaust fan)
  grp = ents.add_group
  grp.name = "Circuit A (exhaust fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -263.mm)
  circle = ge.add_circle([5618.mm,1181.mm,2363.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit B (intake fan)
  grp = ents.add_group
  grp.name = "Circuit B (intake fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 118.5.mm, 0.mm)
  circle = ge.add_circle([1879.142857142857.mm,44.5.mm,1260.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit B (intake fan) elbow
  grp = ents.add_group
  grp.name = "Circuit B (intake fan) elbow"
  ge = grp.entities
  arc = ge.add_arc([1879.142857142857.mm,163.mm,1272.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1879.142857142857.mm,163.mm,1260.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit B (intake fan)
  grp = ents.add_group
  grp.name = "Circuit B (intake fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1091.mm)
  circle = ge.add_circle([1879.142857142857.mm,175.mm,1272.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit B (intake fan) elbow
  grp = ents.add_group
  grp.name = "Circuit B (intake fan) elbow"
  ge = grp.entities
  arc = ge.add_arc([1879.142857142857.mm,163.mm,2363.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1879.142857142857.mm,175.mm,2363.mm], [0.000000,0.000000,1.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit B (intake fan)
  grp = ents.add_group
  grp.name = "Circuit B (intake fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -131.mm, 0.mm)
  circle = ge.add_circle([1879.142857142857.mm,163.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit B (intake fan) elbow
  grp = ents.add_group
  grp.name = "Circuit B (intake fan) elbow"
  ge = grp.entities
  arc = ge.add_arc([1867.142857142857.mm,32.mm,2375.mm], [1.000000,0.000000,0.000000], [-0.000000,-0.000000,-1.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1879.142857142857.mm,32.mm,2375.mm], [0.000000,-1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit B (intake fan)
  grp = ents.add_group
  grp.name = "Circuit B (intake fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1566.162857142857.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1867.142857142857.mm,20.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit B (intake fan) elbow
  grp = ents.add_group
  grp.name = "Circuit B (intake fan) elbow"
  ge = grp.entities
  arc = ge.add_arc([300.98.mm,19.02.mm,2375.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 0.9800000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([300.98.mm,20.mm,2375.mm], [-1.000000,0.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit B (intake fan)
  grp = ents.add_group
  grp.name = "Circuit B (intake fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -0.5201999999999991.mm, 0.mm)
  circle = ge.add_circle([300.mm,19.02.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit B (intake fan) elbow
  grp = ents.add_group
  grp.name = "Circuit B (intake fan) elbow"
  ge = grp.entities
  arc = ge.add_arc([300.mm,18.4998.mm,2374.5002.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 0.49979999999999986.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([300.mm,18.4998.mm,2375.mm], [0.000000,-1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit B (intake fan)
  grp = ents.add_group
  grp.name = "Circuit B (intake fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1729.5002.mm)
  circle = ge.add_circle([300.mm,18.mm,2374.5002.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit E (cooler / inverter)
  grp = ents.add_group
  grp.name = "Circuit E (cooler / inverter)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 118.5.mm, 0.mm)
  circle = ge.add_circle([1949.4285714285713.mm,44.5.mm,1260.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse E (40A — cooler / inverter)"] || model.materials.add("Fuse E (40A — cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit E (cooler / inverter) elbow
  grp = ents.add_group
  grp.name = "Circuit E (cooler / inverter) elbow"
  ge = grp.entities
  arc = ge.add_arc([1949.4285714285713.mm,163.mm,1272.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1949.4285714285713.mm,163.mm,1260.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse E (40A — cooler / inverter)"] || model.materials.add("Fuse E (40A — cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit E (cooler / inverter)
  grp = ents.add_group
  grp.name = "Circuit E (cooler / inverter)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1091.mm)
  circle = ge.add_circle([1949.4285714285713.mm,175.mm,1272.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse E (40A — cooler / inverter)"] || model.materials.add("Fuse E (40A — cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit E (cooler / inverter) elbow
  grp = ents.add_group
  grp.name = "Circuit E (cooler / inverter) elbow"
  ge = grp.entities
  arc = ge.add_arc([1949.4285714285713.mm,163.mm,2363.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1949.4285714285713.mm,175.mm,2363.mm], [0.000000,0.000000,1.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse E (40A — cooler / inverter)"] || model.materials.add("Fuse E (40A — cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit E (cooler / inverter)
  grp = ents.add_group
  grp.name = "Circuit E (cooler / inverter)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -131.mm, 0.mm)
  circle = ge.add_circle([1949.4285714285713.mm,163.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse E (40A — cooler / inverter)"] || model.materials.add("Fuse E (40A — cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit E (cooler / inverter) elbow
  grp = ents.add_group
  grp.name = "Circuit E (cooler / inverter) elbow"
  ge = grp.entities
  arc = ge.add_arc([1937.4285714285713.mm,32.mm,2375.mm], [1.000000,0.000000,0.000000], [-0.000000,-0.000000,-1.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1949.4285714285713.mm,32.mm,2375.mm], [0.000000,-1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse E (40A — cooler / inverter)"] || model.materials.add("Fuse E (40A — cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit E (cooler / inverter)
  grp = ents.add_group
  grp.name = "Circuit E (cooler / inverter)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-40.58857142857141.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1937.4285714285713.mm,20.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse E (40A — cooler / inverter)"] || model.materials.add("Fuse E (40A — cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit E (cooler / inverter) elbow
  grp = ents.add_group
  grp.name = "Circuit E (cooler / inverter) elbow"
  ge = grp.entities
  arc = ge.add_arc([1896.84.mm,27.84.mm,2375.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,-1.000000], 7.840000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1896.84.mm,20.mm,2375.mm], [-1.000000,0.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse E (40A — cooler / inverter)"] || model.materials.add("Fuse E (40A — cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit E (cooler / inverter)
  grp = ents.add_group
  grp.name = "Circuit E (cooler / inverter)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 4.161599999999996.mm, 0.mm)
  circle = ge.add_circle([1889.mm,27.84.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse E (40A — cooler / inverter)"] || model.materials.add("Fuse E (40A — cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit E (cooler / inverter) elbow
  grp = ents.add_group
  grp.name = "Circuit E (cooler / inverter) elbow"
  ge = grp.entities
  arc = ge.add_arc([1889.mm,32.001599999999996.mm,2371.0016.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 3.9984000000000006.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1889.mm,32.001599999999996.mm,2375.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse E (40A — cooler / inverter)"] || model.materials.add("Fuse E (40A — cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit E (cooler / inverter)
  grp = ents.add_group
  grp.name = "Circuit E (cooler / inverter)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1493.5016.mm)
  circle = ge.add_circle([1889.mm,36.mm,2371.0016.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse E (40A — cooler / inverter)"] || model.materials.add("Fuse E (40A — cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C distribution wireway
  grp = ents.add_group
  grp.name = "Cct C distribution wireway"
  face = grp.entities.add_face([4849.mm,1146.mm,595.mm], [4899.mm,1146.mm,595.mm], [4899.mm,1216.mm,595.mm], [4849.mm,1216.mm,595.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1675.mm)
  mat = model.materials["Fuse Block base (Blue Sea 5026)"] || model.materials.add("Fuse Block base (Blue Sea 5026)")
  mat.color = Sketchup::Color.new(42, 42, 42)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C feed (fuse C -> master switch)
  grp = ents.add_group
  grp.name = "Cct C feed (fuse C -> master switch)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -119.mm)
  circle = ge.add_circle([1902.5714285714287.mm,44.5.mm,1260.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C feed (fuse C -> master switch) elbow
  grp = ents.add_group
  grp.name = "Cct C feed (fuse C -> master switch) elbow"
  ge = grp.entities
  arc = ge.add_arc([1914.5714285714287.mm,44.5.mm,1141.mm], [-1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1902.5714285714287.mm,44.5.mm,1141.mm], [0.000000,0.000000,-1.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C feed (fuse C -> master switch)
  grp = ents.add_group
  grp.name = "Cct C feed (fuse C -> master switch)"
  ge = grp.entities
  vec = Geom::Vector3d.new(43.69357142857143.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1914.5714285714287.mm,44.5.mm,1129.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C feed (fuse C -> master switch) elbow
  grp = ents.add_group
  grp.name = "Cct C feed (fuse C -> master switch) elbow"
  ge = grp.entities
  arc = ge.add_arc([1958.265.mm,45.235.mm,1129.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 0.7350000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1958.265.mm,44.5.mm,1129.mm], [1.000000,0.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C feed (fuse C -> master switch)
  grp = ents.add_group
  grp.name = "Cct C feed (fuse C -> master switch)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.7650000000000006.mm, 0.mm)
  circle = ge.add_circle([1959.mm,45.235.mm,1129.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C switched feed (master switch -> pump wireway)
  grp = ents.add_group
  grp.name = "Cct C switched feed (master switch -> pump wireway)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1234.mm)
  circle = ge.add_circle([1959.mm,46.mm,1129.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C switched feed (master switch -> pump wireway) elbow
  grp = ents.add_group
  grp.name = "Cct C switched feed (master switch -> pump wireway) elbow"
  ge = grp.entities
  arc = ge.add_arc([1959.mm,34.mm,2363.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1959.mm,46.mm,2363.mm], [0.000000,0.000000,1.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C switched feed (master switch -> pump wireway)
  grp = ents.add_group
  grp.name = "Cct C switched feed (master switch -> pump wireway)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.140000000000001.mm, 0.mm)
  circle = ge.add_circle([1959.mm,34.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C switched feed (master switch -> pump wireway) elbow
  grp = ents.add_group
  grp.name = "Cct C switched feed (master switch -> pump wireway) elbow"
  ge = grp.entities
  arc = ge.add_arc([1965.86.mm,26.86.mm,2375.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.000000,1.000000], 6.86.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1959.mm,26.86.mm,2375.mm], [0.000000,-1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C switched feed (master switch -> pump wireway)
  grp = ents.add_group
  grp.name = "Cct C switched feed (master switch -> pump wireway)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2896.1400000000003.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1965.86.mm,20.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C switched feed (master switch -> pump wireway) elbow
  grp = ents.add_group
  grp.name = "Cct C switched feed (master switch -> pump wireway) elbow"
  ge = grp.entities
  arc = ge.add_arc([4862.mm,32.mm,2375.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4862.mm,20.mm,2375.mm], [1.000000,0.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C switched feed (master switch -> pump wireway)
  grp = ents.add_group
  grp.name = "Cct C switched feed (master switch -> pump wireway)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 1137.mm, 0.mm)
  circle = ge.add_circle([4874.mm,32.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C switched feed (master switch -> pump wireway) elbow
  grp = ents.add_group
  grp.name = "Cct C switched feed (master switch -> pump wireway) elbow"
  ge = grp.entities
  arc = ge.add_arc([4874.mm,1169.mm,2363.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4874.mm,1169.mm,2375.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C switched feed (master switch -> pump wireway)
  grp = ents.add_group
  grp.name = "Cct C switched feed (master switch -> pump wireway)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -118.mm)
  circle = ge.add_circle([4874.mm,1181.mm,2363.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-01
  grp = ents.add_group
  grp.name = "Cct C branch P-01"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -72.mm, 0.mm)
  circle = ge.add_circle([4874.mm,1181.mm,675.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-04
  grp = ents.add_group
  grp.name = "Cct C branch P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -72.mm, 0.mm)
  circle = ge.add_circle([4874.mm,1181.mm,1000.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-05
  grp = ents.add_group
  grp.name = "Cct C branch P-05"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -72.mm, 0.mm)
  circle = ge.add_circle([4874.mm,1181.mm,1400.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-03
  grp = ents.add_group
  grp.name = "Cct C branch P-03"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -72.mm, 0.mm)
  circle = ge.add_circle([4874.mm,1181.mm,1800.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 (Brown recycle - Pinhole-Wall filter pump)
  grp = ents.add_group
  grp.name = "P-02 (Brown recycle - Pinhole-Wall filter pump)"
  face = grp.entities.add_face([3033.mm,70.mm,2139.mm], [3083.mm,70.mm,2139.mm], [3083.mm,130.mm,2139.mm], [3033.mm,130.mm,2139.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(180.mm)
  mat = model.materials["P-02 (Brown recycle - Pinhole-Wall filter pump)"] || model.materials.add("P-02 (Brown recycle - Pinhole-Wall filter pump)")
  mat.color = Sketchup::Color.new(107, 68, 35)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-02 (taps ceiling feed - Pinhole-Wall panel)
  grp = ents.add_group
  grp.name = "Cct C branch P-02 (taps ceiling feed - Pinhole-Wall panel)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 68.mm, 0.mm)
  circle = ge.add_circle([3058.mm,20.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-02 (taps ceiling feed - Pinhole-Wall panel) elbow
  grp = ents.add_group
  grp.name = "Cct C branch P-02 (taps ceiling feed - Pinhole-Wall panel) elbow"
  ge = grp.entities
  arc = ge.add_arc([3058.mm,88.mm,2363.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([3058.mm,88.mm,2375.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-02 (taps ceiling feed - Pinhole-Wall panel)
  grp = ents.add_group
  grp.name = "Cct C branch P-02 (taps ceiling feed - Pinhole-Wall panel)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -44.mm)
  circle = ge.add_circle([3058.mm,100.mm,2363.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G feed (white LED)
  grp = ents.add_group
  grp.name = "Circuit G feed (white LED)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 118.5.mm, 0.mm)
  circle = ge.add_circle([1996.2857142857142.mm,44.5.mm,1260.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse G (10A — white LED)"] || model.materials.add("Fuse G (10A — white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G feed (white LED) elbow
  grp = ents.add_group
  grp.name = "Circuit G feed (white LED) elbow"
  ge = grp.entities
  arc = ge.add_arc([1996.2857142857142.mm,163.mm,1272.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1996.2857142857142.mm,163.mm,1260.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse G (10A — white LED)"] || model.materials.add("Fuse G (10A — white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G feed (white LED)
  grp = ents.add_group
  grp.name = "Circuit G feed (white LED)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1091.mm)
  circle = ge.add_circle([1996.2857142857142.mm,175.mm,1272.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse G (10A — white LED)"] || model.materials.add("Fuse G (10A — white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G feed (white LED) elbow
  grp = ents.add_group
  grp.name = "Circuit G feed (white LED) elbow"
  ge = grp.entities
  arc = ge.add_arc([1996.2857142857142.mm,163.mm,2363.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1996.2857142857142.mm,175.mm,2363.mm], [0.000000,0.000000,1.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse G (10A — white LED)"] || model.materials.add("Fuse G (10A — white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G feed (white LED)
  grp = ents.add_group
  grp.name = "Circuit G feed (white LED)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -143.mm, 0.mm)
  circle = ge.add_circle([1996.2857142857142.mm,163.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse G (10A — white LED)"] || model.materials.add("Fuse G (10A — white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G ceiling spine (white LED)
  grp = ents.add_group
  grp.name = "Circuit G ceiling spine (white LED)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3274.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1300.mm,20.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse G (10A — white LED)"] || model.materials.add("Fuse G (10A — white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G drop X1300 (white LED)
  grp = ents.add_group
  grp.name = "Circuit G drop X1300 (white LED)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 999.mm, 0.mm)
  circle = ge.add_circle([1300.mm,20.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse G (10A — white LED)"] || model.materials.add("Fuse G (10A — white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G drop X1300 (white LED) elbow
  grp = ents.add_group
  grp.name = "Circuit G drop X1300 (white LED) elbow"
  ge = grp.entities
  arc = ge.add_arc([1300.mm,1019.mm,2363.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1300.mm,1019.mm,2375.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse G (10A — white LED)"] || model.materials.add("Fuse G (10A — white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G drop X1300 (white LED)
  grp = ents.add_group
  grp.name = "Circuit G drop X1300 (white LED)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -15.mm)
  circle = ge.add_circle([1300.mm,1031.mm,2363.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse G (10A — white LED)"] || model.materials.add("Fuse G (10A — white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G drop X3200 (white LED)
  grp = ents.add_group
  grp.name = "Circuit G drop X3200 (white LED)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 999.mm, 0.mm)
  circle = ge.add_circle([3200.mm,20.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse G (10A — white LED)"] || model.materials.add("Fuse G (10A — white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G drop X3200 (white LED) elbow
  grp = ents.add_group
  grp.name = "Circuit G drop X3200 (white LED) elbow"
  ge = grp.entities
  arc = ge.add_arc([3200.mm,1019.mm,2363.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([3200.mm,1019.mm,2375.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse G (10A — white LED)"] || model.materials.add("Fuse G (10A — white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G drop X3200 (white LED)
  grp = ents.add_group
  grp.name = "Circuit G drop X3200 (white LED)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -15.mm)
  circle = ge.add_circle([3200.mm,1031.mm,2363.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse G (10A — white LED)"] || model.materials.add("Fuse G (10A — white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G drop X4574 (white LED)
  grp = ents.add_group
  grp.name = "Circuit G drop X4574 (white LED)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 849.mm, 0.mm)
  circle = ge.add_circle([4574.mm,20.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse G (10A — white LED)"] || model.materials.add("Fuse G (10A — white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G drop X4574 (white LED) elbow
  grp = ents.add_group
  grp.name = "Circuit G drop X4574 (white LED) elbow"
  ge = grp.entities
  arc = ge.add_arc([4574.mm,869.mm,2363.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4574.mm,869.mm,2375.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse G (10A — white LED)"] || model.materials.add("Fuse G (10A — white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G drop X4574 (white LED)
  grp = ents.add_group
  grp.name = "Circuit G drop X4574 (white LED)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -15.mm)
  circle = ge.add_circle([4574.mm,881.mm,2363.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse G (10A — white LED)"] || model.materials.add("Fuse G (10A — white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D feed (safelight)
  grp = ents.add_group
  grp.name = "Circuit D feed (safelight)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 118.5.mm, 0.mm)
  circle = ge.add_circle([1926.mm,44.5.mm,1260.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse D (5A — safelight)"] || model.materials.add("Fuse D (5A — safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D feed (safelight) elbow
  grp = ents.add_group
  grp.name = "Circuit D feed (safelight) elbow"
  ge = grp.entities
  arc = ge.add_arc([1926.mm,163.mm,1272.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1926.mm,163.mm,1260.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse D (5A — safelight)"] || model.materials.add("Fuse D (5A — safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D feed (safelight)
  grp = ents.add_group
  grp.name = "Circuit D feed (safelight)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1091.mm)
  circle = ge.add_circle([1926.mm,175.mm,1272.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse D (5A — safelight)"] || model.materials.add("Fuse D (5A — safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D feed (safelight) elbow
  grp = ents.add_group
  grp.name = "Circuit D feed (safelight) elbow"
  ge = grp.entities
  arc = ge.add_arc([1926.mm,163.mm,2363.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1926.mm,175.mm,2363.mm], [0.000000,0.000000,1.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse D (5A — safelight)"] || model.materials.add("Fuse D (5A — safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D feed (safelight)
  grp = ents.add_group
  grp.name = "Circuit D feed (safelight)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -143.mm, 0.mm)
  circle = ge.add_circle([1926.mm,163.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse D (5A — safelight)"] || model.materials.add("Fuse D (5A — safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D ceiling spine (safelight)
  grp = ents.add_group
  grp.name = "Circuit D ceiling spine (safelight)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3650.mm, 0.mm, 0.mm)
  circle = ge.add_circle([520.mm,20.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse D (5A — safelight)"] || model.materials.add("Fuse D (5A — safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D drop X520 (safelight)
  grp = ents.add_group
  grp.name = "Circuit D drop X520 (safelight)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 74.12.mm, 0.mm)
  circle = ge.add_circle([520.mm,20.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse D (5A — safelight)"] || model.materials.add("Fuse D (5A — safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D drop X520 (safelight) elbow
  grp = ents.add_group
  grp.name = "Circuit D drop X520 (safelight) elbow"
  ge = grp.entities
  arc = ge.add_arc([520.mm,94.12.mm,2369.12.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 5.880000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([520.mm,94.12.mm,2375.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse D (5A — safelight)"] || model.materials.add("Fuse D (5A — safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D drop X520 (safelight)
  grp = ents.add_group
  grp.name = "Circuit D drop X520 (safelight)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -6.119999999999891.mm)
  circle = ge.add_circle([520.mm,100.mm,2369.12.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse D (5A — safelight)"] || model.materials.add("Fuse D (5A — safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D drop X2270 (safelight)
  grp = ents.add_group
  grp.name = "Circuit D drop X2270 (safelight)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 74.12.mm, 0.mm)
  circle = ge.add_circle([2270.mm,20.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse D (5A — safelight)"] || model.materials.add("Fuse D (5A — safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D drop X2270 (safelight) elbow
  grp = ents.add_group
  grp.name = "Circuit D drop X2270 (safelight) elbow"
  ge = grp.entities
  arc = ge.add_arc([2270.mm,94.12.mm,2369.12.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 5.880000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2270.mm,94.12.mm,2375.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse D (5A — safelight)"] || model.materials.add("Fuse D (5A — safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D drop X2270 (safelight)
  grp = ents.add_group
  grp.name = "Circuit D drop X2270 (safelight)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -6.119999999999891.mm)
  circle = ge.add_circle([2270.mm,100.mm,2369.12.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse D (5A — safelight)"] || model.materials.add("Fuse D (5A — safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D drop X4170 (safelight)
  grp = ents.add_group
  grp.name = "Circuit D drop X4170 (safelight)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 74.12.mm, 0.mm)
  circle = ge.add_circle([4170.mm,20.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse D (5A — safelight)"] || model.materials.add("Fuse D (5A — safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D drop X4170 (safelight) elbow
  grp = ents.add_group
  grp.name = "Circuit D drop X4170 (safelight) elbow"
  ge = grp.entities
  arc = ge.add_arc([4170.mm,94.12.mm,2369.12.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 5.880000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4170.mm,94.12.mm,2375.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Fuse D (5A — safelight)"] || model.materials.add("Fuse D (5A — safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D drop X4170 (safelight)
  grp = ents.add_group
  grp.name = "Circuit D drop X4170 (safelight)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -6.119999999999891.mm)
  circle = ge.add_circle([4170.mm,100.mm,2369.12.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse D (5A — safelight)"] || model.materials.add("Fuse D (5A — safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
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
  vec = Geom::Vector3d.new(-1.5002345951338185.mm, 13.004426672891782.mm, 20.238523937893206.mm)
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
  vec = Geom::Vector3d.new(8.220974819980384.mm, 20.530524284593128.mm, 9.585239367105373.mm)
  circle = ge.add_circle([115.26778510716863.mm,259.0460271797435.mm,618.3365092902702.mm], vec, 5.mm, 6)
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
  inst.name = "Circuit Runs"
  inst.layer = model.layers["Circuit Runs"]


# ── In-model labels (Labels tag; visible only in the "Labeled" scene) ──
anc = Geom::Point3d.new(950.mm, -1500.mm, 700.mm)
txt = entities.add_text("SOLAR ARRAY
3x 200W (30deg tilt)", anc, Geom::Vector3d.new(-200.mm, -700.mm, 700.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1919.mm, 40.mm, 1500.mm)
txt = entities.add_text("MPPT 100/50", anc, Geom::Vector3d.new(-380.mm, 700.mm, 280.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1919.mm, 40.mm, 1260.mm)
txt = entities.add_text("FUSE STACK A-G
5/5/15/5/40/20/10 A", anc, Geom::Vector3d.new(420.mm, 700.mm, 240.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1919.mm, 40.mm, 1310.mm)
txt = entities.add_text("+/- BUSBARS", anc, Geom::Vector3d.new(420.mm, 640.mm, -120.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1884.mm, 0.mm, 1045.mm)
txt = entities.add_text("MAIN DISCONNECT", anc, Geom::Vector3d.new(360.mm, 760.mm, -260.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1889.mm, 40.mm, 678.mm)
txt = entities.add_text("BATTERY CONTACTOR
+ MRBF main fuse", anc, Geom::Vector3d.new(-300.mm, 760.mm, 900.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1979.mm, 60.mm, 260.mm)
txt = entities.add_text("BATTERY 1x 100Ah
(2nd pack ghosted)", anc, Geom::Vector3d.new(-320.mm, 640.mm, 760.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1889.mm, 36.mm, 995.mm)
txt = entities.add_text("CCT-E INVERTER
12->120V AC (cooler)", anc, Geom::Vector3d.new(-430.mm, 820.mm, 480.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1420.mm, -80.mm, 2090.mm)
txt = entities.add_text("EXTERNAL PANEL
MC4 PV / shore / WR cooler / E-STOP", anc, Geom::Vector3d.new(220.mm, -520.mm, 380.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1000.mm, -287.mm, 711.mm)
txt = entities.add_text("EVAP COOLER
(Hessaire MC18M, Cct E)", anc, Geom::Vector3d.new(-260.mm, -520.mm, 520.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4874.mm, 1181.mm, 2230.mm)
txt = entities.add_text("CCT-C PUMP DISTRIBUTION
dist block → pumps (master sw on EP)", anc, Geom::Vector3d.new(-350.mm, -700.mm, 250.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(2029.mm, 22.mm, 1080.mm)
txt = entities.add_text("PV DISCONNECT
(load-break, array->MPPT)", anc, Geom::Vector3d.new(300.mm, 560.mm, 320.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1869.mm, 95.mm, 1305.mm)
txt = entities.add_text("60A CHARGE FUSE
(MPPT -> battery)", anc, Geom::Vector3d.new(440.mm, 680.mm, 160.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(2099.mm, 20.mm, 1065.mm)
txt = entities.add_text("INTERIOR E-STOP
(parallel)", anc, Geom::Vector3d.new(-340.mm, 560.mm, -160.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(300.mm, 30.mm, 600.mm)
txt = entities.add_text("FAN B FEED (Cct B)
wall box -> flex jumper", anc, Geom::Vector3d.new(320.mm, 650.mm, 760.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(5618.mm, 1181.mm, 2000.mm)
txt = entities.add_text("FAN A FEED (Cct A)
exhaust, sealed end", anc, Geom::Vector3d.new(400.mm, -550.mm, -400.mm))
txt.layer = model.layers["Labels"] rescue nil

# ── In-model © + license credit (default layer → shown in every scene) ──
lbb = model.bounds
lanc = Geom::Point3d.new(lbb.min.x, lbb.min.y - 400.mm, lbb.min.z)
entities.add_text("© 2026 Alvin Richards
Licensed under GNU AGPLv3
alvinr.github.io/tbs", lanc)

model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags from earlier versions ──
keep_tags = ["Context", "Solar Array", "Power Core", "Battery", "External Panel", "Inverter", "Circuit Runs", "Labels"]
default_layer = model.layers[0]
model.layers.to_a.each { |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}

# ── Scenes ── shared iso camera, with a tighter eye for the zoom scenes. ──
model.layers.each { |l| l.visible = (l.name != "Labels") }
bb = model.bounds
ctr = bb.center
dir = Geom::Vector3d.new(0.72, -0.7, 0.5); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.5)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

zoom = {"Power Core" => [1979.mm, 90.mm, 1355.mm, 1400.mm], "External Panel" => [1420.mm, -65.mm, 1950.mm, 1600.mm]}
[["Overview", ["Context", "Solar Array", "Power Core", "Battery", "External Panel", "Inverter", "Circuit Runs"]], ["Power Core", ["Power Core", "Battery", "Inverter"]], ["Distribution", ["Circuit Runs", "Power Core", "Battery"]], ["External Panel", ["External Panel", "Solar Array"]], ["Labeled", ["Context", "Solar Array", "Power Core", "Battery", "External Panel", "Inverter", "Circuit Runs", "Labels"]]].each { |name, tags|
  model.layers.each { |l| l.visible = (l == default_layer || l.name == "Context" || tags.include?(l.name)) }
  # A Page captures the active_view camera at add-time (Page has no camera= setter),
  # so set the camera FIRST — zoomed for the detail scenes, shared otherwise.
  if zoom[name]
    zx, zy, zz, zd = zoom[name]
    tgt = Geom::Point3d.new(zx, zy, zz)
    zeye = tgt.offset(dir, zd)
    model.active_view.camera = Sketchup::Camera.new(zeye, tgt, Z_AXIS)
  else
    model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
  end
  page = model.pages.add(name)
  page.use_camera = true
}
model.layers.each { |l| l.visible = true }

model.commit_operation
{ success: true, model: "Electrical",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
