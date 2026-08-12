# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/ — do not edit this .rb directly.
model = Sketchup.active_model
model.start_operation("TBS-001 Walkway + Cantilevers", true)
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

# ── Sketchfab metadata — sketchfab dict fill-only-if-blank; name/desc forced when requested ──
model.name = "TBS-001 Walkway Model" if model.name.to_s.strip.empty?
model.description = "The perimeter walkway provides dry-foot operator access around all four sides of the processing tray without wading through chemical solution." if model.description.to_s.strip.empty?
model.set_attribute("sketchfab", "model_title", "TBS-001 Walkway Model") if model.get_attribute("sketchfab", "model_title").to_s.strip.empty?
model.set_attribute("sketchfab", "model_description", "The perimeter walkway provides dry-foot operator access around all four sides of the processing tray without wading through chemical solution.") if model.get_attribute("sketchfab", "model_description").to_s.strip.empty?
model.set_attribute("sketchfab", "model_id", "96b3d0e5fc8b4fc18c528f64bda028bc") if model.get_attribute("sketchfab", "model_id").to_s.strip.empty?
model.set_attribute("sketchfab", "model_tags", "sketchup") if model.get_attribute("sketchfab", "model_tags").to_s.strip.empty?

# ── Tags (layers) ──
  model.layers.add("Container") unless model.layers["Container"]
  model.layers.add("Processing Tray") unless model.layers["Processing Tray"]
  model.layers.add("Walkways") unless model.layers["Walkways"]
  model.layers.add("Cantilevers") unless model.layers["Cantilevers"]
  model.layers.add("Cantilever Types") unless model.layers["Cantilever Types"]
  model.layers.add("Right Cantilever") unless model.layers["Right Cantilever"]
  model.layers.add("Film Plane") unless model.layers["Film Plane"]
  model.layers.add("Film Plane Left") unless model.layers["Film Plane Left"]
  model.layers.add("IBC Frame") unless model.layers["IBC Frame"]
  model.layers.add("Left Support") unless model.layers["Left Support"]
  model.layers.add("Labels") unless model.layers["Labels"]

# ── Subsystems (each a component on its tag) ──
  # ═══ Container (ghost) ═══
  defn = model.definitions.add("Container (ghost)")
  ents = defn.entities
  # Floor (ghost)
  grp = ents.add_group
  grp.name = "Floor (ghost)"
  face = grp.entities.add_face([0.mm,0.mm,-40.mm], [5893.mm,0.mm,-40.mm], [5893.mm,2362.mm,-40.mm], [0.mm,2362.mm,-40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Floor (ghost)"] || model.materials.add("Floor (ghost)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.22
  grp.material = mat

  # Ceiling (ghost)
  grp = ents.add_group
  grp.name = "Ceiling (ghost)"
  face = grp.entities.add_face([0.mm,0.mm,2388.mm], [5893.mm,0.mm,2388.mm], [5893.mm,2362.mm,2388.mm], [0.mm,2362.mm,2388.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Ceiling (ghost)"] || model.materials.add("Ceiling (ghost)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.1
  grp.material = mat

  # Side wall near (ghost)
  grp = ents.add_group
  grp.name = "Side wall near (ghost)"
  face = grp.entities.add_face([0.mm,-40.mm,0.mm], [5893.mm,-40.mm,0.mm], [5893.mm,0.mm,0.mm], [0.mm,0.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Side wall near (ghost)"] || model.materials.add("Side wall near (ghost)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.14
  grp.material = mat

  # Side wall far (ghost)
  grp = ents.add_group
  grp.name = "Side wall far (ghost)"
  face = grp.entities.add_face([0.mm,2362.mm,0.mm], [5893.mm,2362.mm,0.mm], [5893.mm,2402.mm,0.mm], [0.mm,2402.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Side wall near (ghost)"] || model.materials.add("Side wall near (ghost)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.14
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Container (ghost)"
  inst.layer = model.layers["Container"]

  # ═══ Processing Tray ═══
  defn = model.definitions.add("Processing Tray")
  ents = defn.entities
  # Tray Shim Base
  grp = ents.add_group
  grp.name = "Tray Shim Base"
  face = grp.entities.add_face([280.mm,80.mm,0.mm], [4629.mm,80.mm,0.mm], [4629.mm,2280.mm,0.mm], [280.mm,2280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Tray Shim Base"] || model.materials.add("Tray Shim Base")
  mat.color = Sketchup::Color.new(216, 208, 188)
  mat.alpha = 0.9
  grp.material = mat

  # Processing Tray Floor A
  grp = ents.add_group
  grp.name = "Processing Tray Floor A"
  ge = grp.entities
  f = ge.add_face([280.mm,80.mm,20.mm], [4629.mm,80.mm,20.mm], [4629.mm,2280.mm,31.mm])
  f.pushpull(-2.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Processing Tray Floor B
  grp = ents.add_group
  grp.name = "Processing Tray Floor B"
  ge = grp.entities
  f = ge.add_face([280.mm,80.mm,20.mm], [4629.mm,2280.mm,31.mm], [280.mm,2280.mm,31.mm])
  f.pushpull(-2.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Near
  grp = ents.add_group
  grp.name = "Tray Rim Near"
  face = grp.entities.add_face([280.mm,80.mm,20.mm], [4629.mm,80.mm,20.mm], [4629.mm,82.mm,20.mm], [280.mm,82.mm,20.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Far
  grp = ents.add_group
  grp.name = "Tray Rim Far"
  face = grp.entities.add_face([280.mm,2278.mm,31.mm], [4629.mm,2278.mm,31.mm], [4629.mm,2280.mm,31.mm], [280.mm,2280.mm,31.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Left
  grp = ents.add_group
  grp.name = "Tray Rim Left"
  face = grp.entities.add_face([280.mm,80.mm,25.5.mm], [282.mm,80.mm,25.5.mm], [282.mm,2280.mm,25.5.mm], [280.mm,2280.mm,25.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Right
  grp = ents.add_group
  grp.name = "Tray Rim Right"
  face = grp.entities.add_face([4627.mm,80.mm,25.5.mm], [4629.mm,80.mm,25.5.mm], [4629.mm,2280.mm,25.5.mm], [4627.mm,2280.mm,25.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Chemistry Bath
  grp = ents.add_group
  grp.name = "Chemistry Bath"
  face = grp.entities.add_face([282.mm,82.mm,25.5.mm], [4627.mm,82.mm,25.5.mm], [4627.mm,2278.mm,25.5.mm], [282.mm,2278.mm,25.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Chemistry Bath"] || model.materials.add("Chemistry Bath")
  mat.color = Sketchup::Color.new(46, 111, 160)
  mat.alpha = 0.45
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Processing Tray"
  inst.layer = model.layers["Processing Tray"]

  # ═══ Walkway Decks (near/far/left + right grate) ═══
  defn = model.definitions.add("Walkway Decks (near/far/left + right grate)")
  ents = defn.entities
  # Walkway Near (door-end, removable)
  grp = ents.add_group
  grp.name = "Walkway Near (door-end, removable)"
  face = grp.entities.add_face([580.mm,8.mm,115.mm], [950.mm,8.mm,115.mm], [950.mm,300.mm,115.mm], [580.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (door-end, removable)"] || model.materials.add("Walkway Near (door-end, removable)")
  mat.color = Sketchup::Color.new(192, 96, 0)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near (fixed, bump integral)
  grp = ents.add_group
  grp.name = "Walkway Near (fixed, bump integral)"
  face = grp.entities.add_face([950.mm,8.mm,115.mm], [4329.mm,8.mm,115.mm], [4329.mm,300.mm,115.mm], [3193.mm,300.mm,115.mm], [3193.mm,500.mm,115.mm], [1165.mm,500.mm,115.mm], [1165.mm,300.mm,115.mm], [950.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (fixed, bump integral)"] || model.materials.add("Walkway Near (fixed, bump integral)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far
  grp = ents.add_group
  grp.name = "Walkway Far"
  face = grp.entities.add_face([580.mm,2062.mm,115.mm], [4329.mm,2062.mm,115.mm], [4329.mm,2354.mm,115.mm], [580.mm,2354.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (fixed, bump integral)"] || model.materials.add("Walkway Near (fixed, bump integral)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Left (removable)
  grp = ents.add_group
  grp.name = "Walkway Left (removable)"
  face = grp.entities.add_face([280.mm,0.mm,115.mm], [280.mm,2362.mm,115.mm], [580.mm,2362.mm,115.mm], [580.mm,2062.mm,115.mm], [480.mm,2062.mm,115.mm], [480.mm,1912.mm,115.mm], [580.mm,1912.mm,115.mm], [580.mm,1560.mm,115.mm], [880.mm,1560.mm,115.mm], [880.mm,800.mm,115.mm], [580.mm,800.mm,115.mm], [580.mm,0.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (door-end, removable)"] || model.materials.add("Walkway Near (door-end, removable)")
  mat.color = Sketchup::Color.new(192, 96, 0)
  mat.alpha = 1.0
  grp.material = mat

  # Right walkway grate (cantilevered)
  grp = ents.add_group
  grp.name = "Right walkway grate (cantilevered)"
  face = grp.entities.add_face([4329.mm,0.mm,115.mm], [4629.mm,0.mm,115.mm], [4629.mm,2362.mm,115.mm], [4329.mm,2362.mm,115.mm], [4329.mm,2062.mm,115.mm], [4429.mm,2062.mm,115.mm], [4429.mm,1912.mm,115.mm], [4329.mm,1912.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (fixed, bump integral)"] || model.materials.add("Walkway Near (fixed, bump integral)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Walkway Decks (near/far/left + right grate)"
  inst.layer = model.layers["Walkways"]

  # ═══ Wall Cantilevers ═══
  defn = model.definitions.add("Wall Cantilevers")
  ents = defn.entities
  # Cantilever Near 1 plate
  grp = ents.add_group
  grp.name = "Cantilever Near 1 plate"
  face = grp.entities.add_face([748.mm,0.mm,0.mm], [868.mm,0.mm,0.mm], [868.mm,8.mm,0.mm], [748.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 1 arm
  grp = ents.add_group
  grp.name = "Cantilever Near 1 arm"
  face = grp.entities.add_face([804.mm,8.mm,105.mm], [812.mm,8.mm,105.mm], [812.mm,300.mm,105.mm], [804.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 1 gusset
  grp = ents.add_group
  grp.name = "Cantilever Near 1 gusset"
  ge = grp.entities
  f = ge.add_face([804.mm,8.mm,0.mm], [804.mm,8.mm,105.mm], [804.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 1 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Near 1 ext reinf plate"
  face = grp.entities.add_face([758.mm,-46.mm,0.mm], [858.mm,-46.mm,0.mm], [858.mm,-40.mm,0.mm], [758.mm,-40.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(180.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 1 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([808.mm,-46.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 1 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 1 bolt head"
  face = grp.entities.add_face([799.mm,-52.mm,111.mm], [817.mm,-52.mm,111.mm], [817.mm,-46.mm,111.mm], [799.mm,-46.mm,111.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 1 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([776.mm,-46.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 1 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 1 bolt head"
  face = grp.entities.add_face([767.mm,-52.mm,33.mm], [785.mm,-52.mm,33.mm], [785.mm,-46.mm,33.mm], [767.mm,-46.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 1 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([840.mm,-46.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 1 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 1 bolt head"
  face = grp.entities.add_face([831.mm,-52.mm,33.mm], [849.mm,-52.mm,33.mm], [849.mm,-46.mm,33.mm], [831.mm,-46.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 (widened) plate
  grp = ents.add_group
  grp.name = "Cantilever Near 2 (widened) plate"
  face = grp.entities.add_face([1205.mm,0.mm,0.mm], [1325.mm,0.mm,0.mm], [1325.mm,10.mm,0.mm], [1205.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 (widened) arm
  grp = ents.add_group
  grp.name = "Cantilever Near 2 (widened) arm"
  face = grp.entities.add_face([1260.mm,10.mm,103.mm], [1270.mm,10.mm,103.mm], [1270.mm,500.mm,103.mm], [1260.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 (widened) gusset
  grp = ents.add_group
  grp.name = "Cantilever Near 2 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([1260.mm,10.mm,0.mm], [1260.mm,10.mm,103.mm], [1260.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 (widened) ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Near 2 (widened) ext reinf plate"
  face = grp.entities.add_face([1205.mm,-46.mm,0.mm], [1325.mm,-46.mm,0.mm], [1325.mm,-40.mm,0.mm], [1205.mm,-40.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(220.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 2 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1233.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 2 (widened) bolt head"
  face = grp.entities.add_face([1224.mm,-52.mm,26.mm], [1242.mm,-52.mm,26.mm], [1242.mm,-46.mm,26.mm], [1224.mm,-46.mm,26.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 2 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1297.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 2 (widened) bolt head"
  face = grp.entities.add_face([1288.mm,-52.mm,26.mm], [1306.mm,-52.mm,26.mm], [1306.mm,-46.mm,26.mm], [1288.mm,-46.mm,26.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 2 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1233.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 2 (widened) bolt head"
  face = grp.entities.add_face([1224.mm,-52.mm,151.mm], [1242.mm,-52.mm,151.mm], [1242.mm,-46.mm,151.mm], [1224.mm,-46.mm,151.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 2 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1297.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 2 (widened) bolt head"
  face = grp.entities.add_face([1288.mm,-52.mm,151.mm], [1306.mm,-52.mm,151.mm], [1306.mm,-46.mm,151.mm], [1288.mm,-46.mm,151.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 3 (widened) plate
  grp = ents.add_group
  grp.name = "Cantilever Near 3 (widened) plate"
  face = grp.entities.add_face([1662.mm,0.mm,0.mm], [1782.mm,0.mm,0.mm], [1782.mm,10.mm,0.mm], [1662.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 3 (widened) arm
  grp = ents.add_group
  grp.name = "Cantilever Near 3 (widened) arm"
  face = grp.entities.add_face([1717.mm,10.mm,103.mm], [1727.mm,10.mm,103.mm], [1727.mm,500.mm,103.mm], [1717.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 3 (widened) gusset
  grp = ents.add_group
  grp.name = "Cantilever Near 3 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([1717.mm,10.mm,0.mm], [1717.mm,10.mm,103.mm], [1717.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 3 (widened) ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Near 3 (widened) ext reinf plate"
  face = grp.entities.add_face([1662.mm,-46.mm,0.mm], [1782.mm,-46.mm,0.mm], [1782.mm,-40.mm,0.mm], [1662.mm,-40.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(220.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 3 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 3 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1690.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 3 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 3 (widened) bolt head"
  face = grp.entities.add_face([1681.mm,-52.mm,26.mm], [1699.mm,-52.mm,26.mm], [1699.mm,-46.mm,26.mm], [1681.mm,-46.mm,26.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 3 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 3 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1754.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 3 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 3 (widened) bolt head"
  face = grp.entities.add_face([1745.mm,-52.mm,26.mm], [1763.mm,-52.mm,26.mm], [1763.mm,-46.mm,26.mm], [1745.mm,-46.mm,26.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 3 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 3 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1690.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 3 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 3 (widened) bolt head"
  face = grp.entities.add_face([1681.mm,-52.mm,151.mm], [1699.mm,-52.mm,151.mm], [1699.mm,-46.mm,151.mm], [1681.mm,-46.mm,151.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 3 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 3 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1754.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 3 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 3 (widened) bolt head"
  face = grp.entities.add_face([1745.mm,-52.mm,151.mm], [1763.mm,-52.mm,151.mm], [1763.mm,-46.mm,151.mm], [1745.mm,-46.mm,151.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 4 (widened) plate
  grp = ents.add_group
  grp.name = "Cantilever Near 4 (widened) plate"
  face = grp.entities.add_face([2119.mm,0.mm,0.mm], [2239.mm,0.mm,0.mm], [2239.mm,10.mm,0.mm], [2119.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 4 (widened) arm
  grp = ents.add_group
  grp.name = "Cantilever Near 4 (widened) arm"
  face = grp.entities.add_face([2174.mm,10.mm,103.mm], [2184.mm,10.mm,103.mm], [2184.mm,500.mm,103.mm], [2174.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 4 (widened) gusset
  grp = ents.add_group
  grp.name = "Cantilever Near 4 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([2174.mm,10.mm,0.mm], [2174.mm,10.mm,103.mm], [2174.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 4 (widened) ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Near 4 (widened) ext reinf plate"
  face = grp.entities.add_face([2119.mm,-46.mm,0.mm], [2239.mm,-46.mm,0.mm], [2239.mm,-40.mm,0.mm], [2119.mm,-40.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(220.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 4 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 4 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2147.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 4 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 4 (widened) bolt head"
  face = grp.entities.add_face([2138.mm,-52.mm,26.mm], [2156.mm,-52.mm,26.mm], [2156.mm,-46.mm,26.mm], [2138.mm,-46.mm,26.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 4 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 4 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2211.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 4 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 4 (widened) bolt head"
  face = grp.entities.add_face([2202.mm,-52.mm,26.mm], [2220.mm,-52.mm,26.mm], [2220.mm,-46.mm,26.mm], [2202.mm,-46.mm,26.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 4 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 4 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2147.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 4 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 4 (widened) bolt head"
  face = grp.entities.add_face([2138.mm,-52.mm,151.mm], [2156.mm,-52.mm,151.mm], [2156.mm,-46.mm,151.mm], [2138.mm,-46.mm,151.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 4 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 4 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2211.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 4 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 4 (widened) bolt head"
  face = grp.entities.add_face([2202.mm,-52.mm,151.mm], [2220.mm,-52.mm,151.mm], [2220.mm,-46.mm,151.mm], [2202.mm,-46.mm,151.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 5 (widened) plate
  grp = ents.add_group
  grp.name = "Cantilever Near 5 (widened) plate"
  face = grp.entities.add_face([2576.mm,0.mm,0.mm], [2696.mm,0.mm,0.mm], [2696.mm,10.mm,0.mm], [2576.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 5 (widened) arm
  grp = ents.add_group
  grp.name = "Cantilever Near 5 (widened) arm"
  face = grp.entities.add_face([2631.mm,10.mm,103.mm], [2641.mm,10.mm,103.mm], [2641.mm,500.mm,103.mm], [2631.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 5 (widened) gusset
  grp = ents.add_group
  grp.name = "Cantilever Near 5 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([2631.mm,10.mm,0.mm], [2631.mm,10.mm,103.mm], [2631.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 5 (widened) ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Near 5 (widened) ext reinf plate"
  face = grp.entities.add_face([2576.mm,-46.mm,0.mm], [2696.mm,-46.mm,0.mm], [2696.mm,-40.mm,0.mm], [2576.mm,-40.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(220.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 5 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 5 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2604.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 5 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 5 (widened) bolt head"
  face = grp.entities.add_face([2595.mm,-52.mm,26.mm], [2613.mm,-52.mm,26.mm], [2613.mm,-46.mm,26.mm], [2595.mm,-46.mm,26.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 5 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 5 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2668.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 5 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 5 (widened) bolt head"
  face = grp.entities.add_face([2659.mm,-52.mm,26.mm], [2677.mm,-52.mm,26.mm], [2677.mm,-46.mm,26.mm], [2659.mm,-46.mm,26.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 5 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 5 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2604.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 5 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 5 (widened) bolt head"
  face = grp.entities.add_face([2595.mm,-52.mm,151.mm], [2613.mm,-52.mm,151.mm], [2613.mm,-46.mm,151.mm], [2595.mm,-46.mm,151.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 5 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 5 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2668.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 5 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 5 (widened) bolt head"
  face = grp.entities.add_face([2659.mm,-52.mm,151.mm], [2677.mm,-52.mm,151.mm], [2677.mm,-46.mm,151.mm], [2659.mm,-46.mm,151.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 (widened) plate
  grp = ents.add_group
  grp.name = "Cantilever Near 6 (widened) plate"
  face = grp.entities.add_face([3033.mm,0.mm,0.mm], [3153.mm,0.mm,0.mm], [3153.mm,10.mm,0.mm], [3033.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 (widened) arm
  grp = ents.add_group
  grp.name = "Cantilever Near 6 (widened) arm"
  face = grp.entities.add_face([3088.mm,10.mm,103.mm], [3098.mm,10.mm,103.mm], [3098.mm,500.mm,103.mm], [3088.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 (widened) gusset
  grp = ents.add_group
  grp.name = "Cantilever Near 6 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([3088.mm,10.mm,0.mm], [3088.mm,10.mm,103.mm], [3088.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 (widened) ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Near 6 (widened) ext reinf plate"
  face = grp.entities.add_face([3033.mm,-46.mm,0.mm], [3153.mm,-46.mm,0.mm], [3153.mm,-40.mm,0.mm], [3033.mm,-40.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(220.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 6 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3061.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 6 (widened) bolt head"
  face = grp.entities.add_face([3052.mm,-52.mm,26.mm], [3070.mm,-52.mm,26.mm], [3070.mm,-46.mm,26.mm], [3052.mm,-46.mm,26.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 6 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3125.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 6 (widened) bolt head"
  face = grp.entities.add_face([3116.mm,-52.mm,26.mm], [3134.mm,-52.mm,26.mm], [3134.mm,-46.mm,26.mm], [3116.mm,-46.mm,26.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 6 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3061.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 6 (widened) bolt head"
  face = grp.entities.add_face([3052.mm,-52.mm,151.mm], [3070.mm,-52.mm,151.mm], [3070.mm,-46.mm,151.mm], [3052.mm,-46.mm,151.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 6 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3125.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 6 (widened) bolt head"
  face = grp.entities.add_face([3116.mm,-52.mm,151.mm], [3134.mm,-52.mm,151.mm], [3134.mm,-46.mm,151.mm], [3116.mm,-46.mm,151.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 7 plate
  grp = ents.add_group
  grp.name = "Cantilever Near 7 plate"
  face = grp.entities.add_face([3490.mm,0.mm,0.mm], [3610.mm,0.mm,0.mm], [3610.mm,8.mm,0.mm], [3490.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 7 arm
  grp = ents.add_group
  grp.name = "Cantilever Near 7 arm"
  face = grp.entities.add_face([3546.mm,8.mm,105.mm], [3554.mm,8.mm,105.mm], [3554.mm,300.mm,105.mm], [3546.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 7 gusset
  grp = ents.add_group
  grp.name = "Cantilever Near 7 gusset"
  ge = grp.entities
  f = ge.add_face([3546.mm,8.mm,0.mm], [3546.mm,8.mm,105.mm], [3546.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 7 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Near 7 ext reinf plate"
  face = grp.entities.add_face([3500.mm,-46.mm,0.mm], [3600.mm,-46.mm,0.mm], [3600.mm,-40.mm,0.mm], [3500.mm,-40.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(180.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 7 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3550.mm,-46.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 7 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 7 bolt head"
  face = grp.entities.add_face([3541.mm,-52.mm,111.mm], [3559.mm,-52.mm,111.mm], [3559.mm,-46.mm,111.mm], [3541.mm,-46.mm,111.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 7 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3518.mm,-46.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 7 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 7 bolt head"
  face = grp.entities.add_face([3509.mm,-52.mm,33.mm], [3527.mm,-52.mm,33.mm], [3527.mm,-46.mm,33.mm], [3509.mm,-46.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 7 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3582.mm,-46.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 7 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 7 bolt head"
  face = grp.entities.add_face([3573.mm,-52.mm,33.mm], [3591.mm,-52.mm,33.mm], [3591.mm,-46.mm,33.mm], [3573.mm,-46.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 8 plate
  grp = ents.add_group
  grp.name = "Cantilever Near 8 plate"
  face = grp.entities.add_face([3947.mm,0.mm,0.mm], [4067.mm,0.mm,0.mm], [4067.mm,8.mm,0.mm], [3947.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 8 arm
  grp = ents.add_group
  grp.name = "Cantilever Near 8 arm"
  face = grp.entities.add_face([4003.mm,8.mm,105.mm], [4011.mm,8.mm,105.mm], [4011.mm,300.mm,105.mm], [4003.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 8 gusset
  grp = ents.add_group
  grp.name = "Cantilever Near 8 gusset"
  ge = grp.entities
  f = ge.add_face([4003.mm,8.mm,0.mm], [4003.mm,8.mm,105.mm], [4003.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 8 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Near 8 ext reinf plate"
  face = grp.entities.add_face([3957.mm,-46.mm,0.mm], [4057.mm,-46.mm,0.mm], [4057.mm,-40.mm,0.mm], [3957.mm,-40.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(180.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 8 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4007.mm,-46.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 8 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 8 bolt head"
  face = grp.entities.add_face([3998.mm,-52.mm,111.mm], [4016.mm,-52.mm,111.mm], [4016.mm,-46.mm,111.mm], [3998.mm,-46.mm,111.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 8 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3975.mm,-46.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 8 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 8 bolt head"
  face = grp.entities.add_face([3966.mm,-52.mm,33.mm], [3984.mm,-52.mm,33.mm], [3984.mm,-46.mm,33.mm], [3966.mm,-46.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 8 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4039.mm,-46.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 8 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 8 bolt head"
  face = grp.entities.add_face([4030.mm,-52.mm,33.mm], [4048.mm,-52.mm,33.mm], [4048.mm,-46.mm,33.mm], [4030.mm,-46.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 1 plate
  grp = ents.add_group
  grp.name = "Cantilever Far 1 plate"
  face = grp.entities.add_face([748.mm,2354.mm,0.mm], [868.mm,2354.mm,0.mm], [868.mm,2362.mm,0.mm], [748.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 1 arm
  grp = ents.add_group
  grp.name = "Cantilever Far 1 arm"
  face = grp.entities.add_face([804.mm,2062.mm,105.mm], [812.mm,2062.mm,105.mm], [812.mm,2354.mm,105.mm], [804.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 1 gusset
  grp = ents.add_group
  grp.name = "Cantilever Far 1 gusset"
  ge = grp.entities
  f = ge.add_face([804.mm,2354.mm,0.mm], [804.mm,2354.mm,105.mm], [804.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 1 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Far 1 ext reinf plate"
  face = grp.entities.add_face([758.mm,2402.mm,0.mm], [858.mm,2402.mm,0.mm], [858.mm,2408.mm,0.mm], [758.mm,2408.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(180.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 1 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([808.mm,2354.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 1 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 1 bolt head"
  face = grp.entities.add_face([799.mm,2408.mm,111.mm], [817.mm,2408.mm,111.mm], [817.mm,2414.mm,111.mm], [799.mm,2414.mm,111.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 1 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([776.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 1 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 1 bolt head"
  face = grp.entities.add_face([767.mm,2408.mm,33.mm], [785.mm,2408.mm,33.mm], [785.mm,2414.mm,33.mm], [767.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 1 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([840.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 1 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 1 bolt head"
  face = grp.entities.add_face([831.mm,2408.mm,33.mm], [849.mm,2408.mm,33.mm], [849.mm,2414.mm,33.mm], [831.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 2 plate
  grp = ents.add_group
  grp.name = "Cantilever Far 2 plate"
  face = grp.entities.add_face([1205.mm,2354.mm,0.mm], [1325.mm,2354.mm,0.mm], [1325.mm,2362.mm,0.mm], [1205.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 2 arm
  grp = ents.add_group
  grp.name = "Cantilever Far 2 arm"
  face = grp.entities.add_face([1261.mm,2062.mm,105.mm], [1269.mm,2062.mm,105.mm], [1269.mm,2354.mm,105.mm], [1261.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 2 gusset
  grp = ents.add_group
  grp.name = "Cantilever Far 2 gusset"
  ge = grp.entities
  f = ge.add_face([1261.mm,2354.mm,0.mm], [1261.mm,2354.mm,105.mm], [1261.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 2 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Far 2 ext reinf plate"
  face = grp.entities.add_face([1215.mm,2402.mm,0.mm], [1315.mm,2402.mm,0.mm], [1315.mm,2408.mm,0.mm], [1215.mm,2408.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(180.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 2 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 2 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1265.mm,2354.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 2 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 2 bolt head"
  face = grp.entities.add_face([1256.mm,2408.mm,111.mm], [1274.mm,2408.mm,111.mm], [1274.mm,2414.mm,111.mm], [1256.mm,2414.mm,111.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 2 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 2 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1233.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 2 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 2 bolt head"
  face = grp.entities.add_face([1224.mm,2408.mm,33.mm], [1242.mm,2408.mm,33.mm], [1242.mm,2414.mm,33.mm], [1224.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 2 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 2 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1297.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 2 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 2 bolt head"
  face = grp.entities.add_face([1288.mm,2408.mm,33.mm], [1306.mm,2408.mm,33.mm], [1306.mm,2414.mm,33.mm], [1288.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 3 plate
  grp = ents.add_group
  grp.name = "Cantilever Far 3 plate"
  face = grp.entities.add_face([1662.mm,2354.mm,0.mm], [1782.mm,2354.mm,0.mm], [1782.mm,2362.mm,0.mm], [1662.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 3 arm
  grp = ents.add_group
  grp.name = "Cantilever Far 3 arm"
  face = grp.entities.add_face([1718.mm,2062.mm,105.mm], [1726.mm,2062.mm,105.mm], [1726.mm,2354.mm,105.mm], [1718.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 3 gusset
  grp = ents.add_group
  grp.name = "Cantilever Far 3 gusset"
  ge = grp.entities
  f = ge.add_face([1718.mm,2354.mm,0.mm], [1718.mm,2354.mm,105.mm], [1718.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 3 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Far 3 ext reinf plate"
  face = grp.entities.add_face([1672.mm,2402.mm,0.mm], [1772.mm,2402.mm,0.mm], [1772.mm,2408.mm,0.mm], [1672.mm,2408.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(180.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 3 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 3 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1722.mm,2354.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 3 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 3 bolt head"
  face = grp.entities.add_face([1713.mm,2408.mm,111.mm], [1731.mm,2408.mm,111.mm], [1731.mm,2414.mm,111.mm], [1713.mm,2414.mm,111.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 3 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 3 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1690.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 3 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 3 bolt head"
  face = grp.entities.add_face([1681.mm,2408.mm,33.mm], [1699.mm,2408.mm,33.mm], [1699.mm,2414.mm,33.mm], [1681.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 3 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 3 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1754.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 3 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 3 bolt head"
  face = grp.entities.add_face([1745.mm,2408.mm,33.mm], [1763.mm,2408.mm,33.mm], [1763.mm,2414.mm,33.mm], [1745.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 4 plate
  grp = ents.add_group
  grp.name = "Cantilever Far 4 plate"
  face = grp.entities.add_face([2119.mm,2354.mm,0.mm], [2239.mm,2354.mm,0.mm], [2239.mm,2362.mm,0.mm], [2119.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 4 arm
  grp = ents.add_group
  grp.name = "Cantilever Far 4 arm"
  face = grp.entities.add_face([2175.mm,2062.mm,105.mm], [2183.mm,2062.mm,105.mm], [2183.mm,2354.mm,105.mm], [2175.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 4 gusset
  grp = ents.add_group
  grp.name = "Cantilever Far 4 gusset"
  ge = grp.entities
  f = ge.add_face([2175.mm,2354.mm,0.mm], [2175.mm,2354.mm,105.mm], [2175.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 4 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Far 4 ext reinf plate"
  face = grp.entities.add_face([2129.mm,2402.mm,0.mm], [2229.mm,2402.mm,0.mm], [2229.mm,2408.mm,0.mm], [2129.mm,2408.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(180.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 4 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 4 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2179.mm,2354.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 4 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 4 bolt head"
  face = grp.entities.add_face([2170.mm,2408.mm,111.mm], [2188.mm,2408.mm,111.mm], [2188.mm,2414.mm,111.mm], [2170.mm,2414.mm,111.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 4 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 4 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2147.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 4 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 4 bolt head"
  face = grp.entities.add_face([2138.mm,2408.mm,33.mm], [2156.mm,2408.mm,33.mm], [2156.mm,2414.mm,33.mm], [2138.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 4 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 4 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2211.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 4 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 4 bolt head"
  face = grp.entities.add_face([2202.mm,2408.mm,33.mm], [2220.mm,2408.mm,33.mm], [2220.mm,2414.mm,33.mm], [2202.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 5 plate
  grp = ents.add_group
  grp.name = "Cantilever Far 5 plate"
  face = grp.entities.add_face([2576.mm,2354.mm,0.mm], [2696.mm,2354.mm,0.mm], [2696.mm,2362.mm,0.mm], [2576.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 5 arm
  grp = ents.add_group
  grp.name = "Cantilever Far 5 arm"
  face = grp.entities.add_face([2632.mm,2062.mm,105.mm], [2640.mm,2062.mm,105.mm], [2640.mm,2354.mm,105.mm], [2632.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 5 gusset
  grp = ents.add_group
  grp.name = "Cantilever Far 5 gusset"
  ge = grp.entities
  f = ge.add_face([2632.mm,2354.mm,0.mm], [2632.mm,2354.mm,105.mm], [2632.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 5 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Far 5 ext reinf plate"
  face = grp.entities.add_face([2586.mm,2402.mm,0.mm], [2686.mm,2402.mm,0.mm], [2686.mm,2408.mm,0.mm], [2586.mm,2408.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(180.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 5 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 5 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2636.mm,2354.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 5 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 5 bolt head"
  face = grp.entities.add_face([2627.mm,2408.mm,111.mm], [2645.mm,2408.mm,111.mm], [2645.mm,2414.mm,111.mm], [2627.mm,2414.mm,111.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 5 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 5 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2604.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 5 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 5 bolt head"
  face = grp.entities.add_face([2595.mm,2408.mm,33.mm], [2613.mm,2408.mm,33.mm], [2613.mm,2414.mm,33.mm], [2595.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 5 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 5 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2668.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 5 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 5 bolt head"
  face = grp.entities.add_face([2659.mm,2408.mm,33.mm], [2677.mm,2408.mm,33.mm], [2677.mm,2414.mm,33.mm], [2659.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 6 plate
  grp = ents.add_group
  grp.name = "Cantilever Far 6 plate"
  face = grp.entities.add_face([3033.mm,2354.mm,0.mm], [3153.mm,2354.mm,0.mm], [3153.mm,2362.mm,0.mm], [3033.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 6 arm
  grp = ents.add_group
  grp.name = "Cantilever Far 6 arm"
  face = grp.entities.add_face([3089.mm,2062.mm,105.mm], [3097.mm,2062.mm,105.mm], [3097.mm,2354.mm,105.mm], [3089.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 6 gusset
  grp = ents.add_group
  grp.name = "Cantilever Far 6 gusset"
  ge = grp.entities
  f = ge.add_face([3089.mm,2354.mm,0.mm], [3089.mm,2354.mm,105.mm], [3089.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 6 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Far 6 ext reinf plate"
  face = grp.entities.add_face([3043.mm,2402.mm,0.mm], [3143.mm,2402.mm,0.mm], [3143.mm,2408.mm,0.mm], [3043.mm,2408.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(180.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 6 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3093.mm,2354.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 6 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 6 bolt head"
  face = grp.entities.add_face([3084.mm,2408.mm,111.mm], [3102.mm,2408.mm,111.mm], [3102.mm,2414.mm,111.mm], [3084.mm,2414.mm,111.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 6 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3061.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 6 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 6 bolt head"
  face = grp.entities.add_face([3052.mm,2408.mm,33.mm], [3070.mm,2408.mm,33.mm], [3070.mm,2414.mm,33.mm], [3052.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 6 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3125.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 6 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 6 bolt head"
  face = grp.entities.add_face([3116.mm,2408.mm,33.mm], [3134.mm,2408.mm,33.mm], [3134.mm,2414.mm,33.mm], [3116.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 7 plate
  grp = ents.add_group
  grp.name = "Cantilever Far 7 plate"
  face = grp.entities.add_face([3490.mm,2354.mm,0.mm], [3610.mm,2354.mm,0.mm], [3610.mm,2362.mm,0.mm], [3490.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 7 arm
  grp = ents.add_group
  grp.name = "Cantilever Far 7 arm"
  face = grp.entities.add_face([3546.mm,2062.mm,105.mm], [3554.mm,2062.mm,105.mm], [3554.mm,2354.mm,105.mm], [3546.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 7 gusset
  grp = ents.add_group
  grp.name = "Cantilever Far 7 gusset"
  ge = grp.entities
  f = ge.add_face([3546.mm,2354.mm,0.mm], [3546.mm,2354.mm,105.mm], [3546.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 7 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Far 7 ext reinf plate"
  face = grp.entities.add_face([3500.mm,2402.mm,0.mm], [3600.mm,2402.mm,0.mm], [3600.mm,2408.mm,0.mm], [3500.mm,2408.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(180.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 7 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3550.mm,2354.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 7 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 7 bolt head"
  face = grp.entities.add_face([3541.mm,2408.mm,111.mm], [3559.mm,2408.mm,111.mm], [3559.mm,2414.mm,111.mm], [3541.mm,2414.mm,111.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 7 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3518.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 7 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 7 bolt head"
  face = grp.entities.add_face([3509.mm,2408.mm,33.mm], [3527.mm,2408.mm,33.mm], [3527.mm,2414.mm,33.mm], [3509.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 7 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3582.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 7 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 7 bolt head"
  face = grp.entities.add_face([3573.mm,2408.mm,33.mm], [3591.mm,2408.mm,33.mm], [3591.mm,2414.mm,33.mm], [3573.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 8 plate
  grp = ents.add_group
  grp.name = "Cantilever Far 8 plate"
  face = grp.entities.add_face([3947.mm,2354.mm,0.mm], [4067.mm,2354.mm,0.mm], [4067.mm,2362.mm,0.mm], [3947.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 8 arm
  grp = ents.add_group
  grp.name = "Cantilever Far 8 arm"
  face = grp.entities.add_face([4003.mm,2062.mm,105.mm], [4011.mm,2062.mm,105.mm], [4011.mm,2354.mm,105.mm], [4003.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 8 gusset
  grp = ents.add_group
  grp.name = "Cantilever Far 8 gusset"
  ge = grp.entities
  f = ge.add_face([4003.mm,2354.mm,0.mm], [4003.mm,2354.mm,105.mm], [4003.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 8 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Far 8 ext reinf plate"
  face = grp.entities.add_face([3957.mm,2402.mm,0.mm], [4057.mm,2402.mm,0.mm], [4057.mm,2408.mm,0.mm], [3957.mm,2408.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(180.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 8 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4007.mm,2354.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 8 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 8 bolt head"
  face = grp.entities.add_face([3998.mm,2408.mm,111.mm], [4016.mm,2408.mm,111.mm], [4016.mm,2414.mm,111.mm], [3998.mm,2414.mm,111.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 8 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3975.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 8 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 8 bolt head"
  face = grp.entities.add_face([3966.mm,2408.mm,33.mm], [3984.mm,2408.mm,33.mm], [3984.mm,2414.mm,33.mm], [3966.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 8 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Far 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4039.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 8 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 8 bolt head"
  face = grp.entities.add_face([4030.mm,2408.mm,33.mm], [4048.mm,2408.mm,33.mm], [4048.mm,2414.mm,33.mm], [4030.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Wall Cantilevers"
  inst.layer = model.layers["Cantilevers"]

  # ═══ Cantilever Types ═══
  defn = model.definitions.add("Cantilever Types")
  ents = defn.entities
  # Type FloorCant short foot plate
  grp = ents.add_group
  grp.name = "Type FloorCant short foot plate"
  face = grp.entities.add_face([1936.mm,0.mm,0.mm], [2064.mm,0.mm,0.mm], [2064.mm,60.mm,0.mm], [1936.mm,60.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type FloorCant short post (2x2x0.120 SHS)
  grp = ents.add_group
  grp.name = "Type FloorCant short post (2x2x0.120 SHS)"
  face = grp.entities.add_face([1974.6.mm,0.mm,0.mm], [2025.3999999999999.mm,0.mm,0.mm], [2025.3999999999999.mm,60.mm,0.mm], [1974.6.mm,60.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type FloorCant short arm (to X580)
  grp = ents.add_group
  grp.name = "Type FloorCant short arm (to X580)"
  face = grp.entities.add_face([2025.4.mm,0.mm,89.6.mm], [2330.mm,0.mm,89.6.mm], [2330.mm,50.8.mm,89.6.mm], [2025.4.mm,50.8.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type FloorCant long foot plate
  grp = ents.add_group
  grp.name = "Type FloorCant long foot plate"
  face = grp.entities.add_face([2936.mm,0.mm,0.mm], [3064.mm,0.mm,0.mm], [3064.mm,60.mm,0.mm], [2936.mm,60.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type FloorCant long post (2x2x0.120 SHS)
  grp = ents.add_group
  grp.name = "Type FloorCant long post (2x2x0.120 SHS)"
  face = grp.entities.add_face([2974.6.mm,0.mm,0.mm], [3025.4.mm,0.mm,0.mm], [3025.4.mm,60.mm,0.mm], [2974.6.mm,60.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type FloorCant long arm (to X880)
  grp = ents.add_group
  grp.name = "Type FloorCant long arm (to X880)"
  face = grp.entities.add_face([3025.4.mm,0.mm,89.6.mm], [3630.mm,0.mm,89.6.mm], [3630.mm,50.8.mm,89.6.mm], [3025.4.mm,50.8.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type Standard plate
  grp = ents.add_group
  grp.name = "Type Standard plate"
  face = grp.entities.add_face([3940.mm,0.mm,0.mm], [4060.mm,0.mm,0.mm], [4060.mm,8.mm,0.mm], [3940.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type Standard arm
  grp = ents.add_group
  grp.name = "Type Standard arm"
  face = grp.entities.add_face([3996.mm,8.mm,105.mm], [4004.mm,8.mm,105.mm], [4004.mm,300.mm,105.mm], [3996.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type Standard gusset
  grp = ents.add_group
  grp.name = "Type Standard gusset"
  ge = grp.entities
  f = ge.add_face([3996.mm,8.mm,0.mm], [3996.mm,8.mm,105.mm], [3996.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type Standard ext reinf plate
  grp = ents.add_group
  grp.name = "Type Standard ext reinf plate"
  face = grp.entities.add_face([3950.mm,-46.mm,0.mm], [4050.mm,-46.mm,0.mm], [4050.mm,-40.mm,0.mm], [3950.mm,-40.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(180.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type Standard bolt M12
  grp = ents.add_group
  grp.name = "Type Standard bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4000.mm,-46.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Type Standard bolt head
  grp = ents.add_group
  grp.name = "Type Standard bolt head"
  face = grp.entities.add_face([3991.mm,-52.mm,111.mm], [4009.mm,-52.mm,111.mm], [4009.mm,-46.mm,111.mm], [3991.mm,-46.mm,111.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Type Standard bolt M12
  grp = ents.add_group
  grp.name = "Type Standard bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3968.mm,-46.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Type Standard bolt head
  grp = ents.add_group
  grp.name = "Type Standard bolt head"
  face = grp.entities.add_face([3959.mm,-52.mm,33.mm], [3977.mm,-52.mm,33.mm], [3977.mm,-46.mm,33.mm], [3959.mm,-46.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Type Standard bolt M12
  grp = ents.add_group
  grp.name = "Type Standard bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4032.mm,-46.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Type Standard bolt head
  grp = ents.add_group
  grp.name = "Type Standard bolt head"
  face = grp.entities.add_face([4023.mm,-52.mm,33.mm], [4041.mm,-52.mm,33.mm], [4041.mm,-46.mm,33.mm], [4023.mm,-46.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Type Widened plate
  grp = ents.add_group
  grp.name = "Type Widened plate"
  face = grp.entities.add_face([4940.mm,0.mm,0.mm], [5060.mm,0.mm,0.mm], [5060.mm,10.mm,0.mm], [4940.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type Widened arm
  grp = ents.add_group
  grp.name = "Type Widened arm"
  face = grp.entities.add_face([4995.mm,10.mm,103.mm], [5005.mm,10.mm,103.mm], [5005.mm,500.mm,103.mm], [4995.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type Widened gusset
  grp = ents.add_group
  grp.name = "Type Widened gusset"
  ge = grp.entities
  f = ge.add_face([4995.mm,10.mm,0.mm], [4995.mm,10.mm,103.mm], [4995.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type Widened ext reinf plate
  grp = ents.add_group
  grp.name = "Type Widened ext reinf plate"
  face = grp.entities.add_face([4940.mm,-46.mm,0.mm], [5060.mm,-46.mm,0.mm], [5060.mm,-40.mm,0.mm], [4940.mm,-40.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(220.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type Widened bolt M12
  grp = ents.add_group
  grp.name = "Type Widened bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4968.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Type Widened bolt head
  grp = ents.add_group
  grp.name = "Type Widened bolt head"
  face = grp.entities.add_face([4959.mm,-52.mm,26.mm], [4977.mm,-52.mm,26.mm], [4977.mm,-46.mm,26.mm], [4959.mm,-46.mm,26.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Type Widened bolt M12
  grp = ents.add_group
  grp.name = "Type Widened bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5032.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Type Widened bolt head
  grp = ents.add_group
  grp.name = "Type Widened bolt head"
  face = grp.entities.add_face([5023.mm,-52.mm,26.mm], [5041.mm,-52.mm,26.mm], [5041.mm,-46.mm,26.mm], [5023.mm,-46.mm,26.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Type Widened bolt M12
  grp = ents.add_group
  grp.name = "Type Widened bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4968.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Type Widened bolt head
  grp = ents.add_group
  grp.name = "Type Widened bolt head"
  face = grp.entities.add_face([4959.mm,-52.mm,151.mm], [4977.mm,-52.mm,151.mm], [4977.mm,-46.mm,151.mm], [4959.mm,-46.mm,151.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Type Widened bolt M12
  grp = ents.add_group
  grp.name = "Type Widened bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5032.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Type Widened bolt head
  grp = ents.add_group
  grp.name = "Type Widened bolt head"
  face = grp.entities.add_face([5023.mm,-52.mm,151.mm], [5041.mm,-52.mm,151.mm], [5041.mm,-46.mm,151.mm], [5023.mm,-46.mm,151.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat plate (Type RWk Cleat)
  grp = ents.add_group
  grp.name = "RWk wall cleat plate (Type RWk Cleat)"
  face = grp.entities.add_face([5955.mm,0.mm,79.6.mm], [6045.mm,0.mm,79.6.mm], [6045.mm,8.mm,79.6.mm], [5955.mm,8.mm,79.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(45.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat ext plate (Type RWk Cleat)
  grp = ents.add_group
  grp.name = "RWk wall cleat ext plate (Type RWk Cleat)"
  face = grp.entities.add_face([5955.mm,-48.mm,79.6.mm], [6045.mm,-48.mm,79.6.mm], [6045.mm,-40.mm,79.6.mm], [5955.mm,-40.mm,79.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(45.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat shelf (Type RWk Cleat)
  grp = ents.add_group
  grp.name = "RWk wall cleat shelf (Type RWk Cleat)"
  face = grp.entities.add_face([5955.mm,0.mm,79.6.mm], [6045.mm,0.mm,79.6.mm], [6045.mm,55.mm,79.6.mm], [5955.mm,55.mm,79.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall bolt (Type RWk Cleat) Z95
  grp = ents.add_group
  grp.name = "RWk wall bolt (Type RWk Cleat) Z95"
  ge = grp.entities
  circle = ge.add_circle([6000.mm,-48.mm,95.6.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall bolt (Type RWk Cleat) Z109
  grp = ents.add_group
  grp.name = "RWk wall bolt (Type RWk Cleat) Z109"
  ge = grp.entities
  circle = ge.add_circle([6000.mm,-48.mm,109.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner plate (near)
  grp = ents.add_group
  grp.name = "FP combined corner plate (near)"
  face = grp.entities.add_face([6925.mm,0.mm,77.6.mm], [7075.mm,0.mm,77.6.mm], [7075.mm,10.mm,77.6.mm], [6925.mm,10.mm,77.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(235.4.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner ext plate (near)
  grp = ents.add_group
  grp.name = "FP combined corner ext plate (near)"
  face = grp.entities.add_face([6925.mm,-50.mm,77.6.mm], [7075.mm,-50.mm,77.6.mm], [7075.mm,-40.mm,77.6.mm], [6925.mm,-40.mm,77.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(235.4.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined right-beam seat (near)
  grp = ents.add_group
  grp.name = "FP combined right-beam seat (near)"
  face = grp.entities.add_face([6925.mm,0.mm,77.6.mm], [7075.mm,0.mm,77.6.mm], [7075.mm,55.mm,77.6.mm], [6925.mm,55.mm,77.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined BR rail seat (near)
  grp = ents.add_group
  grp.name = "FP combined BR rail seat (near)"
  face = grp.entities.add_face([6970.mm,0.mm,220.mm], [7030.mm,0.mm,220.mm], [7030.mm,55.mm,220.mm], [6970.mm,55.mm,220.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X6950 Z103
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X6950 Z103"
  ge = grp.entities
  circle = ge.add_circle([6950.mm,-50.mm,103.6.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X6950 Z270
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X6950 Z270"
  ge = grp.entities
  circle = ge.add_circle([6950.mm,-50.mm,270.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X7050 Z103
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X7050 Z103"
  ge = grp.entities
  circle = ge.add_circle([7050.mm,-50.mm,103.6.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X7050 Z270
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X7050 Z270"
  ge = grp.entities
  circle = ge.add_circle([7050.mm,-50.mm,270.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type RWk IBC upright (50x50 RHS)
  grp = ents.add_group
  grp.name = "Type RWk IBC upright (50x50 RHS)"
  face = grp.entities.add_face([8000.mm,0.mm,0.mm], [8050.8.mm,0.mm,0.mm], [8050.8.mm,50.8.mm,0.mm], [8000.mm,50.8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(335.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type RWk cantilever arm (40x40 SHS)
  grp = ents.add_group
  grp.name = "Type RWk cantilever arm (40x40 SHS)"
  face = grp.entities.add_face([7675.mm,0.mm,89.6.mm], [8000.mm,0.mm,89.6.mm], [8000.mm,50.8.mm,89.6.mm], [7675.mm,50.8.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type RWk upright clamp
  grp = ents.add_group
  grp.name = "Type RWk upright clamp"
  face = grp.entities.add_face([7996.mm,54.8.mm,64.6.mm], [8054.8.mm,54.8.mm,64.6.mm], [8054.8.mm,62.8.mm,64.6.mm], [7996.mm,62.8.mm,64.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(80.4.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type RWk upright bolt M12
  grp = ents.add_group
  grp.name = "Type RWk upright bolt M12"
  ge = grp.entities
  circle = ge.add_circle([8025.4.mm,-12.mm,95.6.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(74.8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Cantilever Types"
  inst.layer = model.layers["Cantilever Types"]

  # ═══ Right Walkway (cantilever rectangle) ═══
  defn = model.definitions.add("Right Walkway (cantilever rectangle)")
  ents = defn.entities
  # RWk Long beam X4329 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 upper"
  face = grp.entities.add_face([4329.mm,0.mm,95.mm], [4379.8.mm,0.mm,95.mm], [4379.8.mm,1812.mm,95.mm], [4329.mm,1812.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4329 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 lower"
  face = grp.entities.add_face([4329.mm,0.mm,89.6.mm], [4379.8.mm,0.mm,89.6.mm], [4379.8.mm,1046.mm,89.6.mm], [4329.mm,1046.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4329 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 lower"
  face = grp.entities.add_face([4329.mm,1096.8.mm,89.6.mm], [4379.8.mm,1096.8.mm,89.6.mm], [4379.8.mm,1265.2.mm,89.6.mm], [4329.mm,1265.2.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4329 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 lower"
  face = grp.entities.add_face([4329.mm,1316.mm,89.6.mm], [4379.8.mm,1316.mm,89.6.mm], [4379.8.mm,1812.mm,89.6.mm], [4329.mm,1812.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam inner ramp-out
  grp = ents.add_group
  grp.name = "RWk Long beam inner ramp-out"
  face = grp.entities.add_face([4329.mm,1812.mm,89.6.mm], [4379.8.mm,1812.mm,89.6.mm], [4479.8.mm,1912.mm,89.6.mm], [4429.mm,1912.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4429 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4429 upper"
  face = grp.entities.add_face([4429.mm,1912.mm,95.mm], [4479.8.mm,1912.mm,95.mm], [4479.8.mm,2062.mm,95.mm], [4429.mm,2062.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4429 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4429 lower"
  face = grp.entities.add_face([4429.mm,1912.mm,89.6.mm], [4479.8.mm,1912.mm,89.6.mm], [4479.8.mm,2062.mm,89.6.mm], [4429.mm,2062.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam inner ramp-in
  grp = ents.add_group
  grp.name = "RWk Long beam inner ramp-in"
  face = grp.entities.add_face([4429.mm,2062.mm,89.6.mm], [4479.8.mm,2062.mm,89.6.mm], [4379.8.mm,2162.mm,89.6.mm], [4329.mm,2162.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4329 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 upper"
  face = grp.entities.add_face([4329.mm,2162.mm,95.mm], [4379.8.mm,2162.mm,95.mm], [4379.8.mm,2362.mm,95.mm], [4329.mm,2362.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4329 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 lower"
  face = grp.entities.add_face([4329.mm,2162.mm,89.6.mm], [4379.8.mm,2162.mm,89.6.mm], [4379.8.mm,2362.mm,89.6.mm], [4329.mm,2362.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4578 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 upper"
  face = grp.entities.add_face([4578.2.mm,0.mm,95.mm], [4629.mm,0.mm,95.mm], [4629.mm,1093.mm,95.mm], [4578.2.mm,1093.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4578 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 upper"
  face = grp.entities.add_face([4578.2.mm,1149.mm,95.mm], [4629.mm,1149.mm,95.mm], [4629.mm,1177.mm,95.mm], [4578.2.mm,1177.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4578 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 upper"
  face = grp.entities.add_face([4578.2.mm,1211.mm,95.mm], [4629.mm,1211.mm,95.mm], [4629.mm,1224.mm,95.mm], [4578.2.mm,1224.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4578 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 upper"
  face = grp.entities.add_face([4578.2.mm,1258.mm,95.mm], [4629.mm,1258.mm,95.mm], [4629.mm,2362.mm,95.mm], [4578.2.mm,2362.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4578 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 lower"
  face = grp.entities.add_face([4578.2.mm,0.mm,89.6.mm], [4629.mm,0.mm,89.6.mm], [4629.mm,1046.mm,89.6.mm], [4578.2.mm,1046.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4578 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 lower"
  face = grp.entities.add_face([4578.2.mm,1149.mm,89.6.mm], [4629.mm,1149.mm,89.6.mm], [4629.mm,1177.mm,89.6.mm], [4578.2.mm,1177.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4578 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 lower"
  face = grp.entities.add_face([4578.2.mm,1211.mm,89.6.mm], [4629.mm,1211.mm,89.6.mm], [4629.mm,1224.mm,89.6.mm], [4578.2.mm,1224.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4578 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 lower"
  face = grp.entities.add_face([4578.2.mm,1258.mm,89.6.mm], [4629.mm,1258.mm,89.6.mm], [4629.mm,1265.2.mm,89.6.mm], [4578.2.mm,1265.2.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4578 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 lower"
  face = grp.entities.add_face([4578.2.mm,1316.mm,89.6.mm], [4629.mm,1316.mm,89.6.mm], [4629.mm,2362.mm,89.6.mm], [4578.2.mm,2362.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4578 notch web
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 notch web"
  face = grp.entities.add_face([4578.2.mm,1096.8.mm,89.6.mm], [4629.mm,1096.8.mm,89.6.mm], [4629.mm,1265.2.mm,89.6.mm], [4578.2.mm,1265.2.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.4000000000000057.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4578 notch web
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 notch web"
  face = grp.entities.add_face([4578.2.mm,1115.mm,89.6.mm], [4629.mm,1115.mm,89.6.mm], [4629.mm,1265.2.mm,89.6.mm], [4578.2.mm,1265.2.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.4000000000000057.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4578 notch web
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 notch web"
  face = grp.entities.add_face([4578.2.mm,1177.mm,89.6.mm], [4629.mm,1177.mm,89.6.mm], [4629.mm,1265.2.mm,89.6.mm], [4578.2.mm,1265.2.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.4000000000000057.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4578 notch web
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 notch web"
  face = grp.entities.add_face([4578.2.mm,1224.mm,89.6.mm], [4629.mm,1224.mm,89.6.mm], [4629.mm,1265.2.mm,89.6.mm], [4578.2.mm,1265.2.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.4000000000000057.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk end beam Yd0
  grp = ents.add_group
  grp.name = "RWk end beam Yd0"
  face = grp.entities.add_face([4329.mm,0.mm,89.6.mm], [4629.mm,0.mm,89.6.mm], [4629.mm,50.8.mm,89.6.mm], [4329.mm,50.8.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk end beam Yd2311
  grp = ents.add_group
  grp.name = "RWk end beam Yd2311"
  face = grp.entities.add_face([4329.mm,2311.2.mm,89.6.mm], [4629.mm,2311.2.mm,89.6.mm], [4629.mm,2362.mm,89.6.mm], [4329.mm,2362.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1046 lower
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 lower"
  face = grp.entities.add_face([4329.mm,1046.mm,89.6.mm], [4654.mm,1046.mm,89.6.mm], [4654.mm,1096.8.mm,89.6.mm], [4329.mm,1096.8.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1046 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 upper"
  face = grp.entities.add_face([4379.8.mm,1046.mm,95.mm], [4578.2.mm,1046.mm,95.mm], [4578.2.mm,1096.8.mm,95.mm], [4379.8.mm,1096.8.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1046 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 upper"
  face = grp.entities.add_face([4629.mm,1046.mm,95.mm], [4654.mm,1046.mm,95.mm], [4654.mm,1096.8.mm,95.mm], [4629.mm,1096.8.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1046 Y1038
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1046 Y1038"
  face = grp.entities.add_face([4650.mm,1038.mm,64.6.mm], [4708.8.mm,1038.mm,64.6.mm], [4708.8.mm,1046.mm,64.6.mm], [4650.mm,1046.mm,64.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(80.4.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1046 Y1096
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1046 Y1096"
  face = grp.entities.add_face([4650.mm,1096.8.mm,64.6.mm], [4708.8.mm,1096.8.mm,64.6.mm], [4708.8.mm,1104.8.mm,64.6.mm], [4650.mm,1104.8.mm,64.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(80.4.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1046 Z95
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1046 Z95"
  ge = grp.entities
  circle = ge.add_circle([4679.4.mm,1034.mm,95.6.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(74.8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1046 Z133
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1046 Z133"
  ge = grp.entities
  circle = ge.add_circle([4679.4.mm,1034.mm,133.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(74.8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1265.2 lower
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1265.2 lower"
  face = grp.entities.add_face([4329.mm,1265.2.mm,89.6.mm], [4654.mm,1265.2.mm,89.6.mm], [4654.mm,1316.mm,89.6.mm], [4329.mm,1316.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1265.2 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1265.2 upper"
  face = grp.entities.add_face([4379.8.mm,1265.2.mm,95.mm], [4578.2.mm,1265.2.mm,95.mm], [4578.2.mm,1316.mm,95.mm], [4379.8.mm,1316.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1265.2 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1265.2 upper"
  face = grp.entities.add_face([4629.mm,1265.2.mm,95.mm], [4654.mm,1265.2.mm,95.mm], [4654.mm,1316.mm,95.mm], [4629.mm,1316.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1265.2 Y1257
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1265.2 Y1257"
  face = grp.entities.add_face([4650.mm,1257.2.mm,64.6.mm], [4708.8.mm,1257.2.mm,64.6.mm], [4708.8.mm,1265.2.mm,64.6.mm], [4650.mm,1265.2.mm,64.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(80.4.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1265.2 Y1316
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1265.2 Y1316"
  face = grp.entities.add_face([4650.mm,1316.mm,64.6.mm], [4708.8.mm,1316.mm,64.6.mm], [4708.8.mm,1324.mm,64.6.mm], [4650.mm,1324.mm,64.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(80.4.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1265.2 Z95
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1265.2 Z95"
  ge = grp.entities
  circle = ge.add_circle([4679.4.mm,1253.2.mm,95.6.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(74.8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1265.2 Z133
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1265.2 Z133"
  ge = grp.entities
  circle = ge.add_circle([4679.4.mm,1253.2.mm,133.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(74.8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat plate (near)
  grp = ents.add_group
  grp.name = "RWk wall cleat plate (near)"
  face = grp.entities.add_face([4309.mm,0.mm,79.6.mm], [4399.mm,0.mm,79.6.mm], [4399.mm,8.mm,79.6.mm], [4309.mm,8.mm,79.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(45.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat ext plate (near)
  grp = ents.add_group
  grp.name = "RWk wall cleat ext plate (near)"
  face = grp.entities.add_face([4309.mm,-48.mm,79.6.mm], [4399.mm,-48.mm,79.6.mm], [4399.mm,-40.mm,79.6.mm], [4309.mm,-40.mm,79.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(45.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat shelf (near)
  grp = ents.add_group
  grp.name = "RWk wall cleat shelf (near)"
  face = grp.entities.add_face([4309.mm,0.mm,79.6.mm], [4399.mm,0.mm,79.6.mm], [4399.mm,55.mm,79.6.mm], [4309.mm,55.mm,79.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall bolt (near) Z95
  grp = ents.add_group
  grp.name = "RWk wall bolt (near) Z95"
  ge = grp.entities
  circle = ge.add_circle([4354.mm,-48.mm,95.6.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall bolt (near) Z109
  grp = ents.add_group
  grp.name = "RWk wall bolt (near) Z109"
  ge = grp.entities
  circle = ge.add_circle([4354.mm,-48.mm,109.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner plate (near)
  grp = ents.add_group
  grp.name = "FP combined corner plate (near)"
  face = grp.entities.add_face([4574.mm,0.mm,77.6.mm], [4724.mm,0.mm,77.6.mm], [4724.mm,10.mm,77.6.mm], [4574.mm,10.mm,77.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(235.4.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner ext plate (near)
  grp = ents.add_group
  grp.name = "FP combined corner ext plate (near)"
  face = grp.entities.add_face([4574.mm,-50.mm,77.6.mm], [4724.mm,-50.mm,77.6.mm], [4724.mm,-40.mm,77.6.mm], [4574.mm,-40.mm,77.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(235.4.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined right-beam seat (near)
  grp = ents.add_group
  grp.name = "FP combined right-beam seat (near)"
  face = grp.entities.add_face([4574.mm,0.mm,77.6.mm], [4724.mm,0.mm,77.6.mm], [4724.mm,55.mm,77.6.mm], [4574.mm,55.mm,77.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined BR rail seat (near)
  grp = ents.add_group
  grp.name = "FP combined BR rail seat (near)"
  face = grp.entities.add_face([4619.mm,0.mm,220.mm], [4679.mm,0.mm,220.mm], [4679.mm,55.mm,220.mm], [4619.mm,55.mm,220.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X4599 Z103
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X4599 Z103"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,-50.mm,103.6.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X4599 Z270
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X4599 Z270"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,-50.mm,270.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X4699 Z103
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X4699 Z103"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,-50.mm,103.6.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X4699 Z270
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X4699 Z270"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,-50.mm,270.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat plate (far)
  grp = ents.add_group
  grp.name = "RWk wall cleat plate (far)"
  face = grp.entities.add_face([4309.mm,2354.mm,79.6.mm], [4399.mm,2354.mm,79.6.mm], [4399.mm,2362.mm,79.6.mm], [4309.mm,2362.mm,79.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(45.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat ext plate (far)
  grp = ents.add_group
  grp.name = "RWk wall cleat ext plate (far)"
  face = grp.entities.add_face([4309.mm,2402.mm,79.6.mm], [4399.mm,2402.mm,79.6.mm], [4399.mm,2410.mm,79.6.mm], [4309.mm,2410.mm,79.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(45.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat shelf (far)
  grp = ents.add_group
  grp.name = "RWk wall cleat shelf (far)"
  face = grp.entities.add_face([4309.mm,2307.mm,79.6.mm], [4399.mm,2307.mm,79.6.mm], [4399.mm,2362.mm,79.6.mm], [4309.mm,2362.mm,79.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall bolt (far) Z95
  grp = ents.add_group
  grp.name = "RWk wall bolt (far) Z95"
  ge = grp.entities
  circle = ge.add_circle([4354.mm,2354.mm,95.6.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall bolt (far) Z109
  grp = ents.add_group
  grp.name = "RWk wall bolt (far) Z109"
  ge = grp.entities
  circle = ge.add_circle([4354.mm,2354.mm,109.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner plate (far)
  grp = ents.add_group
  grp.name = "FP combined corner plate (far)"
  face = grp.entities.add_face([4574.mm,2352.mm,77.6.mm], [4724.mm,2352.mm,77.6.mm], [4724.mm,2362.mm,77.6.mm], [4574.mm,2362.mm,77.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(235.4.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner ext plate (far)
  grp = ents.add_group
  grp.name = "FP combined corner ext plate (far)"
  face = grp.entities.add_face([4574.mm,2402.mm,77.6.mm], [4724.mm,2402.mm,77.6.mm], [4724.mm,2412.mm,77.6.mm], [4574.mm,2412.mm,77.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(235.4.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined right-beam seat (far)
  grp = ents.add_group
  grp.name = "FP combined right-beam seat (far)"
  face = grp.entities.add_face([4574.mm,2307.mm,77.6.mm], [4724.mm,2307.mm,77.6.mm], [4724.mm,2362.mm,77.6.mm], [4574.mm,2362.mm,77.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined BR rail seat (far)
  grp = ents.add_group
  grp.name = "FP combined BR rail seat (far)"
  face = grp.entities.add_face([4619.mm,2307.mm,220.mm], [4679.mm,2307.mm,220.mm], [4679.mm,2362.mm,220.mm], [4619.mm,2362.mm,220.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (far) X4599 Z103
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (far) X4599 Z103"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,2352.mm,103.6.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (far) X4599 Z270
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (far) X4599 Z270"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,2352.mm,270.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (far) X4699 Z103
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (far) X4699 Z103"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,2352.mm,103.6.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (far) X4699 Z270
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (far) X4699 Z270"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,2352.mm,270.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Right Walkway (cantilever rectangle)"
  inst.layer = model.layers["Right Cantilever"]

  # ═══ Film-Plane Support Beams (right) ═══
  defn = model.definitions.add("Film-Plane Support Beams (right)")
  ents = defn.entities
  # U-rail (FLANGED) web BR
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) web BR"
  face = grp.entities.add_face([4638.mm,0.mm,232.mm], [4643.mm,0.mm,232.mm], [4643.mm,2362.mm,232.mm], [4638.mm,2362.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-rail (FLANGED) web BR"] || model.materials.add("U-rail (FLANGED) web BR")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) flange BR 303
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) flange BR 303"
  face = grp.entities.add_face([4605.mm,0.mm,303.mm], [4643.mm,0.mm,303.mm], [4643.mm,2362.mm,303.mm], [4605.mm,2362.mm,303.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail (FLANGED) web BR"] || model.materials.add("U-rail (FLANGED) web BR")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) flange BR 232
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) flange BR 232"
  face = grp.entities.add_face([4605.mm,0.mm,232.mm], [4643.mm,0.mm,232.mm], [4643.mm,2362.mm,232.mm], [4605.mm,2362.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail (FLANGED) web BR"] || model.materials.add("U-rail (FLANGED) web BR")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) bottom-flange lip BR
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) bottom-flange lip BR"
  face = grp.entities.add_face([4605.mm,0.mm,237.mm], [4610.mm,0.mm,237.mm], [4610.mm,2362.mm,237.mm], [4605.mm,2362.mm,237.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-rail (FLANGED) web BR"] || model.materials.add("U-rail (FLANGED) web BR")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Rail end flange (outboard-trimmed) BR 0
  grp = ents.add_group
  grp.name = "Rail end flange (outboard-trimmed) BR 0"
  face = grp.entities.add_face([4569.mm,0.mm,227.mm], [4644.mm,0.mm,227.mm], [4644.mm,12.mm,227.mm], [4569.mm,12.mm,227.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(86.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Rail end flange (outboard-trimmed) BR 2350
  grp = ents.add_group
  grp.name = "Rail end flange (outboard-trimmed) BR 2350"
  face = grp.entities.add_face([4569.mm,2350.mm,227.mm], [4644.mm,2350.mm,227.mm], [4644.mm,2362.mm,227.mm], [4569.mm,2362.mm,227.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(86.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal roller Ø32 (wide face) BR 2245
  grp = ents.add_group
  grp.name = "Acetal roller Ø32 (wide face) BR 2245"
  ge = grp.entities
  circle = ge.add_circle([4614.mm,2245.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal roller Ø32 (wide face) BR 2245"] || model.materials.add("Acetal roller Ø32 (wide face) BR 2245")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel axle Ø10 BR 2245
  grp = ents.add_group
  grp.name = "Wheel axle Ø10 BR 2245"
  ge = grp.entities
  circle = ge.add_circle([4585.mm,2245.mm,253.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper roller Ø20 (anti-lift / anti-tip) BR 2245
  grp = ents.add_group
  grp.name = "Keeper roller Ø20 (anti-lift / anti-tip) BR 2245"
  ge = grp.entities
  circle = ge.add_circle([4618.mm,2245.mm,293.mm], [1,0,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["Acetal roller Ø32 (wide face) BR 2245"] || model.materials.add("Acetal roller Ø32 (wide face) BR 2245")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper axle Ø8 BR 2245
  grp = ents.add_group
  grp.name = "Keeper axle Ø8 BR 2245"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2245.mm,293.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(37.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal roller Ø32 (wide face) BR 2285
  grp = ents.add_group
  grp.name = "Acetal roller Ø32 (wide face) BR 2285"
  ge = grp.entities
  circle = ge.add_circle([4614.mm,2285.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal roller Ø32 (wide face) BR 2245"] || model.materials.add("Acetal roller Ø32 (wide face) BR 2245")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel axle Ø10 BR 2285
  grp = ents.add_group
  grp.name = "Wheel axle Ø10 BR 2285"
  ge = grp.entities
  circle = ge.add_circle([4585.mm,2285.mm,253.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper roller Ø20 (anti-lift / anti-tip) BR 2285
  grp = ents.add_group
  grp.name = "Keeper roller Ø20 (anti-lift / anti-tip) BR 2285"
  ge = grp.entities
  circle = ge.add_circle([4618.mm,2285.mm,293.mm], [1,0,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["Acetal roller Ø32 (wide face) BR 2245"] || model.materials.add("Acetal roller Ø32 (wide face) BR 2245")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper axle Ø8 BR 2285
  grp = ents.add_group
  grp.name = "Keeper axle Ø8 BR 2285"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2285.mm,293.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(37.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (bolted to skate axles) BR
  grp = ents.add_group
  grp.name = "Carriage plate (bolted to skate axles) BR"
  face = grp.entities.add_face([4585.mm,2238.mm,154.mm], [4599.mm,2238.mm,154.mm], [4599.mm,2324.mm,154.mm], [4585.mm,2324.mm,154.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(157.mm)
  mat = model.materials["Acetal roller Ø32 (wide face) BR 2245"] || model.materials.add("Acetal roller Ø32 (wide face) BR 2245")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) BR 2245
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) BR 2245"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2245.mm,231.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) BR 2285
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) BR 2285"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2285.mm,231.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake base (5128A63) BR
  grp = ents.add_group
  grp.name = "Cam-brake base (5128A63) BR"
  face = grp.entities.add_face([4589.mm,2270.mm,311.mm], [4599.mm,2270.mm,311.mm], [4599.mm,2292.mm,311.mm], [4589.mm,2292.mm,311.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Cam-brake base (5128A63) BR"] || model.materials.add("Cam-brake base (5128A63) BR")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake hold-down arm BR
  grp = ents.add_group
  grp.name = "Cam-brake hold-down arm BR"
  face = grp.entities.add_face([4594.mm,2277.mm,312.mm], [4616.mm,2277.mm,312.mm], [4616.mm,2285.mm,312.mm], [4594.mm,2285.mm,312.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Cam-brake base (5128A63) BR"] || model.materials.add("Cam-brake base (5128A63) BR")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake UHMW pad BR
  grp = ents.add_group
  grp.name = "Cam-brake UHMW pad BR"
  face = grp.entities.add_face([4610.mm,2276.mm,308.mm], [4622.mm,2276.mm,308.mm], [4622.mm,2286.mm,308.mm], [4610.mm,2286.mm,308.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Cam-brake UHMW pad BR"] || model.materials.add("Cam-brake UHMW pad BR")
  mat.color = Sketchup::Color.new(216, 212, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake lever BR
  grp = ents.add_group
  grp.name = "Cam-brake lever BR"
  ge = grp.entities
  circle = ge.add_circle([4616.mm,2281.mm,312.mm], [0,0,1], 2.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Cam-brake base (5128A63) BR"] || model.materials.add("Cam-brake base (5128A63) BR")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z slide rail (TILT, green) BR
  grp = ents.add_group
  grp.name = "Vertical Z slide rail (TILT, green) BR"
  face = grp.entities.add_face([4593.mm,2238.mm,140.mm], [4603.mm,2238.mm,140.mm], [4603.mm,2256.mm,140.mm], [4593.mm,2256.mm,140.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(250.mm)
  mat = model.materials["Vertical Z slide rail (TILT, green) BR"] || model.materials.add("Vertical Z slide rail (TILT, green) BR")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X slide rail (SWING, purple) BR
  grp = ents.add_group
  grp.name = "Horizontal X slide rail (SWING, purple) BR"
  face = grp.entities.add_face([4384.mm,2238.mm,142.mm], [4644.mm,2238.mm,142.mm], [4644.mm,2252.mm,142.mm], [4384.mm,2252.mm,142.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X slide rail (SWING, purple) BR"] || model.materials.add("Horizontal X slide rail (SWING, purple) BR")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint (Belden UJ-SS750x375, setscrew) BR
  grp = ents.add_group
  grp.name = "U-joint (Belden UJ-SS750x375, setscrew) BR"
  face = grp.entities.add_face([4612.mm,2233.mm,146.mm], [4636.mm,2233.mm,146.mm], [4636.mm,2257.mm,146.mm], [4612.mm,2257.mm,146.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Input stub 3/8 (X slide → U-joint) BR
  grp = ents.add_group
  grp.name = "Input stub 3/8 (X slide → U-joint) BR"
  ge = grp.entities
  circle = ge.add_circle([4573.mm,2245.mm,160.mm], [1,0,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(46.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 4040N12 304 shaft support (clamps input stub → X slide) BR
  grp = ents.add_group
  grp.name = "4040N12 304 shaft support (clamps input stub → X slide) BR"
  face = grp.entities.add_face([4575.mm,2236.mm,149.mm], [4598.mm,2236.mm,149.mm], [4598.mm,2254.mm,149.mm], [4575.mm,2254.mm,149.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Output stub 3/8 (U-joint → corner plate) BR
  grp = ents.add_group
  grp.name = "Output stub 3/8 (U-joint → corner plate) BR"
  ge = grp.entities
  circle = ge.add_circle([4624.mm,2223.mm,160.mm], [0,1,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Corner plate 304 SS (U-joint mount — angle frame → U-joint) BR
  grp = ents.add_group
  grp.name = "Corner plate 304 SS (U-joint mount — angle frame → U-joint) BR"
  face = grp.entities.add_face([4604.mm,2229.mm,165.mm], [4638.mm,2229.mm,165.mm], [4638.mm,2245.mm,165.mm], [4604.mm,2245.mm,165.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (angle frame → bracket) BR
  grp = ents.add_group
  grp.name = "Frame-corner bolt (angle frame → bracket) BR"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2231.mm,160.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) web TR
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) web TR"
  face = grp.entities.add_face([4638.mm,0.mm,2262.mm], [4643.mm,0.mm,2262.mm], [4643.mm,2362.mm,2262.mm], [4638.mm,2362.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-rail (FLANGED) web BR"] || model.materials.add("U-rail (FLANGED) web BR")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) flange TR 2333
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) flange TR 2333"
  face = grp.entities.add_face([4605.mm,0.mm,2333.mm], [4643.mm,0.mm,2333.mm], [4643.mm,2362.mm,2333.mm], [4605.mm,2362.mm,2333.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail (FLANGED) web BR"] || model.materials.add("U-rail (FLANGED) web BR")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) flange TR 2262
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) flange TR 2262"
  face = grp.entities.add_face([4605.mm,0.mm,2262.mm], [4643.mm,0.mm,2262.mm], [4643.mm,2362.mm,2262.mm], [4605.mm,2362.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail (FLANGED) web BR"] || model.materials.add("U-rail (FLANGED) web BR")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail (FLANGED) bottom-flange lip TR
  grp = ents.add_group
  grp.name = "U-rail (FLANGED) bottom-flange lip TR"
  face = grp.entities.add_face([4605.mm,0.mm,2267.mm], [4610.mm,0.mm,2267.mm], [4610.mm,2362.mm,2267.mm], [4605.mm,2362.mm,2267.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-rail (FLANGED) web BR"] || model.materials.add("U-rail (FLANGED) web BR")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Rail end flange (outboard-trimmed) TR 0
  grp = ents.add_group
  grp.name = "Rail end flange (outboard-trimmed) TR 0"
  face = grp.entities.add_face([4569.mm,0.mm,2257.mm], [4644.mm,0.mm,2257.mm], [4644.mm,12.mm,2257.mm], [4569.mm,12.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(86.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Rail end flange (outboard-trimmed) TR 2350
  grp = ents.add_group
  grp.name = "Rail end flange (outboard-trimmed) TR 2350"
  face = grp.entities.add_face([4569.mm,2350.mm,2257.mm], [4644.mm,2350.mm,2257.mm], [4644.mm,2362.mm,2257.mm], [4569.mm,2362.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(86.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal roller Ø32 (wide face) TR 2245
  grp = ents.add_group
  grp.name = "Acetal roller Ø32 (wide face) TR 2245"
  ge = grp.entities
  circle = ge.add_circle([4614.mm,2245.mm,2283.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal roller Ø32 (wide face) BR 2245"] || model.materials.add("Acetal roller Ø32 (wide face) BR 2245")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel axle Ø10 TR 2245
  grp = ents.add_group
  grp.name = "Wheel axle Ø10 TR 2245"
  ge = grp.entities
  circle = ge.add_circle([4585.mm,2245.mm,2283.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper roller Ø20 (anti-lift / anti-tip) TR 2245
  grp = ents.add_group
  grp.name = "Keeper roller Ø20 (anti-lift / anti-tip) TR 2245"
  ge = grp.entities
  circle = ge.add_circle([4618.mm,2245.mm,2323.mm], [1,0,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["Acetal roller Ø32 (wide face) BR 2245"] || model.materials.add("Acetal roller Ø32 (wide face) BR 2245")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper axle Ø8 TR 2245
  grp = ents.add_group
  grp.name = "Keeper axle Ø8 TR 2245"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2245.mm,2323.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(37.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal roller Ø32 (wide face) TR 2285
  grp = ents.add_group
  grp.name = "Acetal roller Ø32 (wide face) TR 2285"
  ge = grp.entities
  circle = ge.add_circle([4614.mm,2285.mm,2283.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal roller Ø32 (wide face) BR 2245"] || model.materials.add("Acetal roller Ø32 (wide face) BR 2245")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel axle Ø10 TR 2285
  grp = ents.add_group
  grp.name = "Wheel axle Ø10 TR 2285"
  ge = grp.entities
  circle = ge.add_circle([4585.mm,2285.mm,2283.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper roller Ø20 (anti-lift / anti-tip) TR 2285
  grp = ents.add_group
  grp.name = "Keeper roller Ø20 (anti-lift / anti-tip) TR 2285"
  ge = grp.entities
  circle = ge.add_circle([4618.mm,2285.mm,2323.mm], [1,0,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["Acetal roller Ø32 (wide face) BR 2245"] || model.materials.add("Acetal roller Ø32 (wide face) BR 2245")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper axle Ø8 TR 2285
  grp = ents.add_group
  grp.name = "Keeper axle Ø8 TR 2285"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2285.mm,2323.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(37.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (bolted to skate axles) TR
  grp = ents.add_group
  grp.name = "Carriage plate (bolted to skate axles) TR"
  face = grp.entities.add_face([4585.mm,2238.mm,2246.mm], [4599.mm,2238.mm,2246.mm], [4599.mm,2324.mm,2246.mm], [4585.mm,2324.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(95.mm)
  mat = model.materials["Acetal roller Ø32 (wide face) BR 2245"] || model.materials.add("Acetal roller Ø32 (wide face) BR 2245")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) TR 2245
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) TR 2245"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2245.mm,2261.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) TR 2285
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) TR 2285"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2285.mm,2261.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake base (5128A63) TR
  grp = ents.add_group
  grp.name = "Cam-brake base (5128A63) TR"
  face = grp.entities.add_face([4589.mm,2270.mm,2341.mm], [4599.mm,2270.mm,2341.mm], [4599.mm,2292.mm,2341.mm], [4589.mm,2292.mm,2341.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Cam-brake base (5128A63) BR"] || model.materials.add("Cam-brake base (5128A63) BR")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake hold-down arm TR
  grp = ents.add_group
  grp.name = "Cam-brake hold-down arm TR"
  face = grp.entities.add_face([4594.mm,2277.mm,2342.mm], [4616.mm,2277.mm,2342.mm], [4616.mm,2285.mm,2342.mm], [4594.mm,2285.mm,2342.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Cam-brake base (5128A63) BR"] || model.materials.add("Cam-brake base (5128A63) BR")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake UHMW pad TR
  grp = ents.add_group
  grp.name = "Cam-brake UHMW pad TR"
  face = grp.entities.add_face([4610.mm,2276.mm,2338.mm], [4622.mm,2276.mm,2338.mm], [4622.mm,2286.mm,2338.mm], [4610.mm,2286.mm,2338.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Cam-brake UHMW pad BR"] || model.materials.add("Cam-brake UHMW pad BR")
  mat.color = Sketchup::Color.new(216, 212, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake lever TR
  grp = ents.add_group
  grp.name = "Cam-brake lever TR"
  ge = grp.entities
  circle = ge.add_circle([4616.mm,2281.mm,2342.mm], [0,0,1], 2.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Cam-brake base (5128A63) BR"] || model.materials.add("Cam-brake base (5128A63) BR")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z slide rail (TILT, green) TR
  grp = ents.add_group
  grp.name = "Vertical Z slide rail (TILT, green) TR"
  face = grp.entities.add_face([4595.mm,2238.mm,1998.mm], [4605.mm,2238.mm,1998.mm], [4605.mm,2256.mm,1998.mm], [4595.mm,2256.mm,1998.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(250.mm)
  mat = model.materials["Vertical Z slide rail (TILT, green) BR"] || model.materials.add("Vertical Z slide rail (TILT, green) BR")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X slide rail (SWING, purple) TR
  grp = ents.add_group
  grp.name = "Horizontal X slide rail (SWING, purple) TR"
  face = grp.entities.add_face([4384.mm,2238.mm,2256.mm], [4644.mm,2238.mm,2256.mm], [4644.mm,2252.mm,2256.mm], [4384.mm,2252.mm,2256.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X slide rail (SWING, purple) BR"] || model.materials.add("Horizontal X slide rail (SWING, purple) BR")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint (Belden UJ-SS750x375, setscrew) TR
  grp = ents.add_group
  grp.name = "U-joint (Belden UJ-SS750x375, setscrew) TR"
  face = grp.entities.add_face([4612.mm,2233.mm,2238.mm], [4636.mm,2233.mm,2238.mm], [4636.mm,2257.mm,2238.mm], [4612.mm,2257.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Input stub 3/8 (X slide → U-joint) TR
  grp = ents.add_group
  grp.name = "Input stub 3/8 (X slide → U-joint) TR"
  ge = grp.entities
  circle = ge.add_circle([4573.mm,2245.mm,2252.mm], [1,0,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(46.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 4040N12 304 shaft support (clamps input stub → X slide) TR
  grp = ents.add_group
  grp.name = "4040N12 304 shaft support (clamps input stub → X slide) TR"
  face = grp.entities.add_face([4575.mm,2236.mm,2241.mm], [4598.mm,2236.mm,2241.mm], [4598.mm,2254.mm,2241.mm], [4575.mm,2254.mm,2241.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Output stub 3/8 (U-joint → corner plate) TR
  grp = ents.add_group
  grp.name = "Output stub 3/8 (U-joint → corner plate) TR"
  ge = grp.entities
  circle = ge.add_circle([4624.mm,2223.mm,2252.mm], [0,1,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Corner plate 304 SS (U-joint mount — angle frame → U-joint) TR
  grp = ents.add_group
  grp.name = "Corner plate 304 SS (U-joint mount — angle frame → U-joint) TR"
  face = grp.entities.add_face([4604.mm,2229.mm,2207.mm], [4638.mm,2229.mm,2207.mm], [4638.mm,2245.mm,2207.mm], [4604.mm,2245.mm,2207.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (angle frame → bracket) TR
  grp = ents.add_group
  grp.name = "Frame-corner bolt (angle frame → bracket) TR"
  ge = grp.entities
  circle = ge.add_circle([4591.mm,2231.mm,2252.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Film-Plane Support Beams (right)"
  inst.layer = model.layers["Film Plane"]

  # ═══ Film-Plane Support Beams (left) ═══
  defn = model.definitions.add("Film-Plane Support Beams (left)")
  ents = defn.entities
  # U-rail STUB (fixed, parks corner) web BL
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) web BL"
  face = grp.entities.add_face([241.mm,2090.mm,232.mm], [246.mm,2090.mm,232.mm], [246.mm,2362.mm,232.mm], [241.mm,2362.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-rail (FLANGED) web BR"] || model.materials.add("U-rail (FLANGED) web BR")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail STUB (fixed, parks corner) flange BL 303
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) flange BL 303"
  face = grp.entities.add_face([241.mm,2090.mm,303.mm], [279.mm,2090.mm,303.mm], [279.mm,2362.mm,303.mm], [241.mm,2362.mm,303.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail (FLANGED) web BR"] || model.materials.add("U-rail (FLANGED) web BR")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail STUB (fixed, parks corner) flange BL 232
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) flange BL 232"
  face = grp.entities.add_face([241.mm,2090.mm,232.mm], [279.mm,2090.mm,232.mm], [279.mm,2362.mm,232.mm], [241.mm,2362.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail (FLANGED) web BR"] || model.materials.add("U-rail (FLANGED) web BR")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail STUB (fixed, parks corner) bottom-flange lip BL
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) bottom-flange lip BL"
  face = grp.entities.add_face([274.mm,2090.mm,237.mm], [279.mm,2090.mm,237.mm], [279.mm,2362.mm,237.mm], [274.mm,2362.mm,237.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-rail (FLANGED) web BR"] || model.materials.add("U-rail (FLANGED) web BR")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail REMOVABLE (out for transport) web BL
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) web BL"
  face = grp.entities.add_face([241.mm,0.mm,232.mm], [246.mm,0.mm,232.mm], [246.mm,2090.mm,232.mm], [241.mm,2090.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.3
  grp.material = mat

  # U-rail REMOVABLE (out for transport) flange BL 303
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) flange BL 303"
  face = grp.entities.add_face([241.mm,0.mm,303.mm], [279.mm,0.mm,303.mm], [279.mm,2090.mm,303.mm], [241.mm,2090.mm,303.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.3
  grp.material = mat

  # U-rail REMOVABLE (out for transport) flange BL 232
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) flange BL 232"
  face = grp.entities.add_face([241.mm,0.mm,232.mm], [279.mm,0.mm,232.mm], [279.mm,2090.mm,232.mm], [241.mm,2090.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.3
  grp.material = mat

  # U-rail REMOVABLE (out for transport) bottom-flange lip BL
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) bottom-flange lip BL"
  face = grp.entities.add_face([274.mm,0.mm,237.mm], [279.mm,0.mm,237.mm], [279.mm,2090.mm,237.mm], [274.mm,2090.mm,237.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.3
  grp.material = mat

  # Welded bridge (welded to REMOVABLE, bears on stub, ON TOP) BL
  grp = ents.add_group
  grp.name = "Welded bridge (welded to REMOVABLE, bears on stub, ON TOP) BL"
  face = grp.entities.add_face([241.mm,2030.mm,308.mm], [279.mm,2030.mm,308.mm], [279.mm,2180.mm,308.mm], [241.mm,2180.mm,308.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Locating pin (bridge↔STUB, flush to inner-rail top) BL
  grp = ents.add_group
  grp.name = "Locating pin (bridge↔STUB, flush to inner-rail top) BL"
  ge = grp.entities
  circle = ge.add_circle([260.mm,2135.mm,303.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(17.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Bottom support bridge (STUB → beam underside) BL
  grp = ents.add_group
  grp.name = "Bottom support bridge (STUB → beam underside) BL"
  face = grp.entities.add_face([241.mm,2058.mm,220.mm], [279.mm,2058.mm,220.mm], [279.mm,2122.mm,220.mm], [241.mm,2122.mm,220.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Rail far flange (pivot post) BL
  grp = ents.add_group
  grp.name = "Rail far flange (pivot post) BL"
  face = grp.entities.add_face([205.mm,2350.mm,227.mm], [315.mm,2350.mm,227.mm], [315.mm,2362.mm,227.mm], [205.mm,2362.mm,227.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(86.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Pinhole-wall gusset/seat BL
  grp = ents.add_group
  grp.name = "Pinhole-wall gusset/seat BL"
  face = grp.entities.add_face([204.mm,0.mm,202.mm], [316.mm,0.mm,202.mm], [316.mm,45.mm,202.mm], [204.mm,45.mm,202.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(131.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Length splice (pinhole end, outboard web) BL
  grp = ents.add_group
  grp.name = "Length splice (pinhole end, outboard web) BL"
  face = grp.entities.add_face([229.mm,205.mm,232.mm], [241.mm,205.mm,232.mm], [241.mm,315.mm,232.mm], [229.mm,315.mm,232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal roller Ø32 (wide face) BL 2245
  grp = ents.add_group
  grp.name = "Acetal roller Ø32 (wide face) BL 2245"
  ge = grp.entities
  circle = ge.add_circle([250.mm,2245.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal roller Ø32 (wide face) BR 2245"] || model.materials.add("Acetal roller Ø32 (wide face) BR 2245")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel axle Ø10 BL 2245
  grp = ents.add_group
  grp.name = "Wheel axle Ø10 BL 2245"
  ge = grp.entities
  circle = ge.add_circle([250.mm,2245.mm,253.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper roller Ø20 (anti-lift / anti-tip) BL 2245
  grp = ents.add_group
  grp.name = "Keeper roller Ø20 (anti-lift / anti-tip) BL 2245"
  ge = grp.entities
  circle = ge.add_circle([254.mm,2245.mm,293.mm], [1,0,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["Acetal roller Ø32 (wide face) BR 2245"] || model.materials.add("Acetal roller Ø32 (wide face) BR 2245")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper axle Ø8 BL 2245
  grp = ents.add_group
  grp.name = "Keeper axle Ø8 BL 2245"
  ge = grp.entities
  circle = ge.add_circle([254.mm,2245.mm,293.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal roller Ø32 (wide face) BL 2285
  grp = ents.add_group
  grp.name = "Acetal roller Ø32 (wide face) BL 2285"
  ge = grp.entities
  circle = ge.add_circle([250.mm,2285.mm,253.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal roller Ø32 (wide face) BR 2245"] || model.materials.add("Acetal roller Ø32 (wide face) BR 2245")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel axle Ø10 BL 2285
  grp = ents.add_group
  grp.name = "Wheel axle Ø10 BL 2285"
  ge = grp.entities
  circle = ge.add_circle([250.mm,2285.mm,253.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper roller Ø20 (anti-lift / anti-tip) BL 2285
  grp = ents.add_group
  grp.name = "Keeper roller Ø20 (anti-lift / anti-tip) BL 2285"
  ge = grp.entities
  circle = ge.add_circle([254.mm,2285.mm,293.mm], [1,0,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["Acetal roller Ø32 (wide face) BR 2245"] || model.materials.add("Acetal roller Ø32 (wide face) BR 2245")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper axle Ø8 BL 2285
  grp = ents.add_group
  grp.name = "Keeper axle Ø8 BL 2285"
  ge = grp.entities
  circle = ge.add_circle([254.mm,2285.mm,293.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (bolted to skate axles) BL
  grp = ents.add_group
  grp.name = "Carriage plate (bolted to skate axles) BL"
  face = grp.entities.add_face([287.mm,2238.mm,154.mm], [301.mm,2238.mm,154.mm], [301.mm,2324.mm,154.mm], [287.mm,2324.mm,154.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(157.mm)
  mat = model.materials["Acetal roller Ø32 (wide face) BR 2245"] || model.materials.add("Acetal roller Ø32 (wide face) BR 2245")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) BL 2245
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) BL 2245"
  ge = grp.entities
  circle = ge.add_circle([293.mm,2245.mm,231.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) BL 2285
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) BL 2285"
  ge = grp.entities
  circle = ge.add_circle([293.mm,2285.mm,231.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake base (5128A63) BL
  grp = ents.add_group
  grp.name = "Cam-brake base (5128A63) BL"
  face = grp.entities.add_face([285.mm,2270.mm,311.mm], [295.mm,2270.mm,311.mm], [295.mm,2292.mm,311.mm], [285.mm,2292.mm,311.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Cam-brake base (5128A63) BR"] || model.materials.add("Cam-brake base (5128A63) BR")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake hold-down arm BL
  grp = ents.add_group
  grp.name = "Cam-brake hold-down arm BL"
  face = grp.entities.add_face([268.mm,2277.mm,312.mm], [290.mm,2277.mm,312.mm], [290.mm,2285.mm,312.mm], [268.mm,2285.mm,312.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Cam-brake base (5128A63) BR"] || model.materials.add("Cam-brake base (5128A63) BR")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake UHMW pad BL
  grp = ents.add_group
  grp.name = "Cam-brake UHMW pad BL"
  face = grp.entities.add_face([262.mm,2276.mm,308.mm], [274.mm,2276.mm,308.mm], [274.mm,2286.mm,308.mm], [262.mm,2286.mm,308.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Cam-brake UHMW pad BR"] || model.materials.add("Cam-brake UHMW pad BR")
  mat.color = Sketchup::Color.new(216, 212, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake lever BL
  grp = ents.add_group
  grp.name = "Cam-brake lever BL"
  ge = grp.entities
  circle = ge.add_circle([268.mm,2281.mm,312.mm], [0,0,1], 2.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Cam-brake base (5128A63) BR"] || model.materials.add("Cam-brake base (5128A63) BR")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z slide rail (TILT, green) BL
  grp = ents.add_group
  grp.name = "Vertical Z slide rail (TILT, green) BL"
  face = grp.entities.add_face([281.mm,2238.mm,140.mm], [291.mm,2238.mm,140.mm], [291.mm,2256.mm,140.mm], [281.mm,2256.mm,140.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(250.mm)
  mat = model.materials["Vertical Z slide rail (TILT, green) BR"] || model.materials.add("Vertical Z slide rail (TILT, green) BR")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X slide rail (SWING, purple) BL
  grp = ents.add_group
  grp.name = "Horizontal X slide rail (SWING, purple) BL"
  face = grp.entities.add_face([240.mm,2238.mm,142.mm], [500.mm,2238.mm,142.mm], [500.mm,2252.mm,142.mm], [240.mm,2252.mm,142.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X slide rail (SWING, purple) BR"] || model.materials.add("Horizontal X slide rail (SWING, purple) BR")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint (Belden UJ-SS750x375, setscrew) BL
  grp = ents.add_group
  grp.name = "U-joint (Belden UJ-SS750x375, setscrew) BL"
  face = grp.entities.add_face([248.mm,2233.mm,146.mm], [272.mm,2233.mm,146.mm], [272.mm,2257.mm,146.mm], [248.mm,2257.mm,146.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Input stub 3/8 (X slide → U-joint) BL
  grp = ents.add_group
  grp.name = "Input stub 3/8 (X slide → U-joint) BL"
  ge = grp.entities
  circle = ge.add_circle([265.mm,2245.mm,160.mm], [1,0,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(46.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 4040N12 304 shaft support (clamps input stub → X slide) BL
  grp = ents.add_group
  grp.name = "4040N12 304 shaft support (clamps input stub → X slide) BL"
  face = grp.entities.add_face([286.mm,2236.mm,149.mm], [309.mm,2236.mm,149.mm], [309.mm,2254.mm,149.mm], [286.mm,2254.mm,149.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Output stub 3/8 (U-joint → corner plate) BL
  grp = ents.add_group
  grp.name = "Output stub 3/8 (U-joint → corner plate) BL"
  ge = grp.entities
  circle = ge.add_circle([260.mm,2223.mm,160.mm], [0,1,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Corner plate 304 SS (U-joint mount — angle frame → U-joint) BL
  grp = ents.add_group
  grp.name = "Corner plate 304 SS (U-joint mount — angle frame → U-joint) BL"
  face = grp.entities.add_face([246.mm,2229.mm,165.mm], [280.mm,2229.mm,165.mm], [280.mm,2245.mm,165.mm], [246.mm,2245.mm,165.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (angle frame → bracket) BL
  grp = ents.add_group
  grp.name = "Frame-corner bolt (angle frame → bracket) BL"
  ge = grp.entities
  circle = ge.add_circle([293.mm,2231.mm,160.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail STUB (fixed, parks corner) web TL
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) web TL"
  face = grp.entities.add_face([241.mm,2090.mm,2262.mm], [246.mm,2090.mm,2262.mm], [246.mm,2362.mm,2262.mm], [241.mm,2362.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-rail (FLANGED) web BR"] || model.materials.add("U-rail (FLANGED) web BR")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail STUB (fixed, parks corner) flange TL 2333
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) flange TL 2333"
  face = grp.entities.add_face([241.mm,2090.mm,2333.mm], [279.mm,2090.mm,2333.mm], [279.mm,2362.mm,2333.mm], [241.mm,2362.mm,2333.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail (FLANGED) web BR"] || model.materials.add("U-rail (FLANGED) web BR")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail STUB (fixed, parks corner) flange TL 2262
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) flange TL 2262"
  face = grp.entities.add_face([241.mm,2090.mm,2262.mm], [279.mm,2090.mm,2262.mm], [279.mm,2362.mm,2262.mm], [241.mm,2362.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail (FLANGED) web BR"] || model.materials.add("U-rail (FLANGED) web BR")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail STUB (fixed, parks corner) bottom-flange lip TL
  grp = ents.add_group
  grp.name = "U-rail STUB (fixed, parks corner) bottom-flange lip TL"
  face = grp.entities.add_face([274.mm,2090.mm,2267.mm], [279.mm,2090.mm,2267.mm], [279.mm,2362.mm,2267.mm], [274.mm,2362.mm,2267.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-rail (FLANGED) web BR"] || model.materials.add("U-rail (FLANGED) web BR")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # U-rail REMOVABLE (out for transport) web TL
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) web TL"
  face = grp.entities.add_face([241.mm,0.mm,2262.mm], [246.mm,0.mm,2262.mm], [246.mm,2090.mm,2262.mm], [241.mm,2090.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.3
  grp.material = mat

  # U-rail REMOVABLE (out for transport) flange TL 2333
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) flange TL 2333"
  face = grp.entities.add_face([241.mm,0.mm,2333.mm], [279.mm,0.mm,2333.mm], [279.mm,2090.mm,2333.mm], [241.mm,2090.mm,2333.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.3
  grp.material = mat

  # U-rail REMOVABLE (out for transport) flange TL 2262
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) flange TL 2262"
  face = grp.entities.add_face([241.mm,0.mm,2262.mm], [279.mm,0.mm,2262.mm], [279.mm,2090.mm,2262.mm], [241.mm,2090.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.3
  grp.material = mat

  # U-rail REMOVABLE (out for transport) bottom-flange lip TL
  grp = ents.add_group
  grp.name = "U-rail REMOVABLE (out for transport) bottom-flange lip TL"
  face = grp.entities.add_face([274.mm,0.mm,2267.mm], [279.mm,0.mm,2267.mm], [279.mm,2090.mm,2267.mm], [274.mm,2090.mm,2267.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(9.mm)
  mat = model.materials["U-rail REMOVABLE (out for transport) web BL"] || model.materials.add("U-rail REMOVABLE (out for transport) web BL")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.3
  grp.material = mat

  # Welded bridge (welded to REMOVABLE, bears on stub, ON TOP) TL
  grp = ents.add_group
  grp.name = "Welded bridge (welded to REMOVABLE, bears on stub, ON TOP) TL"
  face = grp.entities.add_face([241.mm,2030.mm,2338.mm], [279.mm,2030.mm,2338.mm], [279.mm,2180.mm,2338.mm], [241.mm,2180.mm,2338.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Locating pin (bridge↔STUB, flush to inner-rail top) TL
  grp = ents.add_group
  grp.name = "Locating pin (bridge↔STUB, flush to inner-rail top) TL"
  ge = grp.entities
  circle = ge.add_circle([260.mm,2135.mm,2333.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(17.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Bottom support bridge (STUB → beam underside) TL
  grp = ents.add_group
  grp.name = "Bottom support bridge (STUB → beam underside) TL"
  face = grp.entities.add_face([241.mm,2058.mm,2250.mm], [279.mm,2058.mm,2250.mm], [279.mm,2122.mm,2250.mm], [241.mm,2122.mm,2250.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Rail far flange (pivot post) TL
  grp = ents.add_group
  grp.name = "Rail far flange (pivot post) TL"
  face = grp.entities.add_face([205.mm,2350.mm,2257.mm], [315.mm,2350.mm,2257.mm], [315.mm,2362.mm,2257.mm], [205.mm,2362.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(86.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Pinhole-wall gusset/seat TL
  grp = ents.add_group
  grp.name = "Pinhole-wall gusset/seat TL"
  face = grp.entities.add_face([204.mm,0.mm,2232.mm], [316.mm,0.mm,2232.mm], [316.mm,45.mm,2232.mm], [204.mm,45.mm,2232.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(131.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Length splice (pinhole end, outboard web) TL
  grp = ents.add_group
  grp.name = "Length splice (pinhole end, outboard web) TL"
  face = grp.entities.add_face([229.mm,205.mm,2262.mm], [241.mm,205.mm,2262.mm], [241.mm,315.mm,2262.mm], [229.mm,315.mm,2262.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(76.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal roller Ø32 (wide face) TL 2245
  grp = ents.add_group
  grp.name = "Acetal roller Ø32 (wide face) TL 2245"
  ge = grp.entities
  circle = ge.add_circle([250.mm,2245.mm,2283.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal roller Ø32 (wide face) BR 2245"] || model.materials.add("Acetal roller Ø32 (wide face) BR 2245")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel axle Ø10 TL 2245
  grp = ents.add_group
  grp.name = "Wheel axle Ø10 TL 2245"
  ge = grp.entities
  circle = ge.add_circle([250.mm,2245.mm,2283.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper roller Ø20 (anti-lift / anti-tip) TL 2245
  grp = ents.add_group
  grp.name = "Keeper roller Ø20 (anti-lift / anti-tip) TL 2245"
  ge = grp.entities
  circle = ge.add_circle([254.mm,2245.mm,2323.mm], [1,0,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["Acetal roller Ø32 (wide face) BR 2245"] || model.materials.add("Acetal roller Ø32 (wide face) BR 2245")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper axle Ø8 TL 2245
  grp = ents.add_group
  grp.name = "Keeper axle Ø8 TL 2245"
  ge = grp.entities
  circle = ge.add_circle([254.mm,2245.mm,2323.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Acetal roller Ø32 (wide face) TL 2285
  grp = ents.add_group
  grp.name = "Acetal roller Ø32 (wide face) TL 2285"
  ge = grp.entities
  circle = ge.add_circle([250.mm,2285.mm,2283.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Acetal roller Ø32 (wide face) BR 2245"] || model.materials.add("Acetal roller Ø32 (wide face) BR 2245")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel axle Ø10 TL 2285
  grp = ents.add_group
  grp.name = "Wheel axle Ø10 TL 2285"
  ge = grp.entities
  circle = ge.add_circle([250.mm,2285.mm,2283.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper roller Ø20 (anti-lift / anti-tip) TL 2285
  grp = ents.add_group
  grp.name = "Keeper roller Ø20 (anti-lift / anti-tip) TL 2285"
  ge = grp.entities
  circle = ge.add_circle([254.mm,2285.mm,2323.mm], [1,0,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["Acetal roller Ø32 (wide face) BR 2245"] || model.materials.add("Acetal roller Ø32 (wide face) BR 2245")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Keeper axle Ø8 TL 2285
  grp = ents.add_group
  grp.name = "Keeper axle Ø8 TL 2285"
  ge = grp.entities
  circle = ge.add_circle([254.mm,2285.mm,2323.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(49.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage plate (bolted to skate axles) TL
  grp = ents.add_group
  grp.name = "Carriage plate (bolted to skate axles) TL"
  face = grp.entities.add_face([287.mm,2238.mm,2246.mm], [301.mm,2238.mm,2246.mm], [301.mm,2324.mm,2246.mm], [287.mm,2324.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(95.mm)
  mat = model.materials["Acetal roller Ø32 (wide face) BR 2245"] || model.materials.add("Acetal roller Ø32 (wide face) BR 2245")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) TL 2245
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) TL 2245"
  ge = grp.entities
  circle = ge.add_circle([293.mm,2245.mm,2261.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Axle retainer bolt (thru plate) TL 2285
  grp = ents.add_group
  grp.name = "Axle retainer bolt (thru plate) TL 2285"
  ge = grp.entities
  circle = ge.add_circle([293.mm,2285.mm,2261.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake base (5128A63) TL
  grp = ents.add_group
  grp.name = "Cam-brake base (5128A63) TL"
  face = grp.entities.add_face([285.mm,2270.mm,2341.mm], [295.mm,2270.mm,2341.mm], [295.mm,2292.mm,2341.mm], [285.mm,2292.mm,2341.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Cam-brake base (5128A63) BR"] || model.materials.add("Cam-brake base (5128A63) BR")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake hold-down arm TL
  grp = ents.add_group
  grp.name = "Cam-brake hold-down arm TL"
  face = grp.entities.add_face([268.mm,2277.mm,2342.mm], [290.mm,2277.mm,2342.mm], [290.mm,2285.mm,2342.mm], [268.mm,2285.mm,2342.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Cam-brake base (5128A63) BR"] || model.materials.add("Cam-brake base (5128A63) BR")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake UHMW pad TL
  grp = ents.add_group
  grp.name = "Cam-brake UHMW pad TL"
  face = grp.entities.add_face([262.mm,2276.mm,2338.mm], [274.mm,2276.mm,2338.mm], [274.mm,2286.mm,2338.mm], [262.mm,2286.mm,2338.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Cam-brake UHMW pad BR"] || model.materials.add("Cam-brake UHMW pad BR")
  mat.color = Sketchup::Color.new(216, 212, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Cam-brake lever TL
  grp = ents.add_group
  grp.name = "Cam-brake lever TL"
  ge = grp.entities
  circle = ge.add_circle([268.mm,2281.mm,2342.mm], [0,0,1], 2.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Cam-brake base (5128A63) BR"] || model.materials.add("Cam-brake base (5128A63) BR")
  mat.color = Sketchup::Color.new(58, 58, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Vertical Z slide rail (TILT, green) TL
  grp = ents.add_group
  grp.name = "Vertical Z slide rail (TILT, green) TL"
  face = grp.entities.add_face([273.mm,2238.mm,1998.mm], [283.mm,2238.mm,1998.mm], [283.mm,2256.mm,1998.mm], [273.mm,2256.mm,1998.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(250.mm)
  mat = model.materials["Vertical Z slide rail (TILT, green) BR"] || model.materials.add("Vertical Z slide rail (TILT, green) BR")
  mat.color = Sketchup::Color.new(46, 139, 87)
  mat.alpha = 1.0
  grp.material = mat

  # Horizontal X slide rail (SWING, purple) TL
  grp = ents.add_group
  grp.name = "Horizontal X slide rail (SWING, purple) TL"
  face = grp.entities.add_face([240.mm,2238.mm,2256.mm], [500.mm,2238.mm,2256.mm], [500.mm,2252.mm,2256.mm], [240.mm,2252.mm,2256.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Horizontal X slide rail (SWING, purple) BR"] || model.materials.add("Horizontal X slide rail (SWING, purple) BR")
  mat.color = Sketchup::Color.new(123, 94, 167)
  mat.alpha = 1.0
  grp.material = mat

  # U-joint (Belden UJ-SS750x375, setscrew) TL
  grp = ents.add_group
  grp.name = "U-joint (Belden UJ-SS750x375, setscrew) TL"
  face = grp.entities.add_face([248.mm,2233.mm,2238.mm], [272.mm,2233.mm,2238.mm], [272.mm,2257.mm,2238.mm], [248.mm,2257.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Rail end flange (outboard-trimmed) BR 0"] || model.materials.add("Rail end flange (outboard-trimmed) BR 0")
  mat.color = Sketchup::Color.new(138, 138, 146)
  mat.alpha = 1.0
  grp.material = mat

  # Input stub 3/8 (X slide → U-joint) TL
  grp = ents.add_group
  grp.name = "Input stub 3/8 (X slide → U-joint) TL"
  ge = grp.entities
  circle = ge.add_circle([265.mm,2245.mm,2252.mm], [1,0,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(46.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 4040N12 304 shaft support (clamps input stub → X slide) TL
  grp = ents.add_group
  grp.name = "4040N12 304 shaft support (clamps input stub → X slide) TL"
  face = grp.entities.add_face([286.mm,2236.mm,2241.mm], [309.mm,2236.mm,2241.mm], [309.mm,2254.mm,2241.mm], [286.mm,2254.mm,2241.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Output stub 3/8 (U-joint → corner plate) TL
  grp = ents.add_group
  grp.name = "Output stub 3/8 (U-joint → corner plate) TL"
  ge = grp.entities
  circle = ge.add_circle([260.mm,2223.mm,2252.mm], [0,1,0], 4.75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Corner plate 304 SS (U-joint mount — angle frame → U-joint) TL
  grp = ents.add_group
  grp.name = "Corner plate 304 SS (U-joint mount — angle frame → U-joint) TL"
  face = grp.entities.add_face([246.mm,2229.mm,2207.mm], [280.mm,2229.mm,2207.mm], [280.mm,2245.mm,2207.mm], [246.mm,2245.mm,2207.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame-corner bolt (angle frame → bracket) TL
  grp = ents.add_group
  grp.name = "Frame-corner bolt (angle frame → bracket) TL"
  ge = grp.entities
  circle = ge.add_circle([293.mm,2231.mm,2252.mm], [0,1,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Film-Plane Support Beams (left)"
  inst.layer = model.layers["Film Plane Left"]

  # ═══ IBC Corridor Frame (deep box) ═══
  defn = model.definitions.add("IBC Corridor Frame (deep box)")
  ents = defn.entities
  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([4654.mm,1046.mm,0.mm], [4704.8.mm,1046.mm,0.mm], [4704.8.mm,1096.8.mm,0.mm], [4654.mm,1096.8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([4654.mm,1265.2.mm,0.mm], [4704.8.mm,1265.2.mm,0.mm], [4704.8.mm,1316.mm,0.mm], [4654.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([5104.mm,1046.mm,0.mm], [5154.8.mm,1046.mm,0.mm], [5154.8.mm,1096.8.mm,0.mm], [5104.mm,1096.8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([5104.mm,1265.2.mm,0.mm], [5154.8.mm,1265.2.mm,0.mm], [5154.8.mm,1316.mm,0.mm], [5104.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([4654.mm,1096.8.mm,0.mm], [4704.8.mm,1096.8.mm,0.mm], [4704.8.mm,1265.2.mm,0.mm], [4654.mm,1265.2.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([5104.mm,1096.8.mm,0.mm], [5154.8.mm,1096.8.mm,0.mm], [5154.8.mm,1265.2.mm,0.mm], [5104.mm,1265.2.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.8.mm,1046.mm,0.mm], [5104.mm,1046.mm,0.mm], [5104.mm,1096.8.mm,0.mm], [4704.8.mm,1096.8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.8.mm,1265.2.mm,0.mm], [5104.mm,1265.2.mm,0.mm], [5104.mm,1316.mm,0.mm], [4704.8.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([4654.mm,1096.8.mm,2245.2.mm], [4704.8.mm,1096.8.mm,2245.2.mm], [4704.8.mm,1265.2.mm,2245.2.mm], [4654.mm,1265.2.mm,2245.2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([5104.mm,1096.8.mm,2245.2.mm], [5154.8.mm,1096.8.mm,2245.2.mm], [5154.8.mm,1265.2.mm,2245.2.mm], [5104.mm,1265.2.mm,2245.2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.8.mm,1046.mm,2245.2.mm], [5104.mm,1046.mm,2245.2.mm], [5104.mm,1096.8.mm,2245.2.mm], [4704.8.mm,1096.8.mm,2245.2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.8.mm,1265.2.mm,2245.2.mm], [5104.mm,1265.2.mm,2245.2.mm], [5104.mm,1316.mm,2245.2.mm], [4704.8.mm,1316.mm,2245.2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot plate
  grp = ents.add_group
  grp.name = "Foot plate"
  face = grp.entities.add_face([4604.4.mm,996.4000000000001.mm,0.mm], [4754.4.mm,996.4000000000001.mm,0.mm], [4754.4.mm,1146.4.mm,0.mm], [4604.4.mm,1146.4.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4629.4.mm,1021.4000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4629.4.mm,1121.4.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4729.4.mm,1021.4000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4729.4.mm,1121.4.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot plate
  grp = ents.add_group
  grp.name = "Foot plate"
  face = grp.entities.add_face([4604.4.mm,1215.6000000000001.mm,0.mm], [4754.4.mm,1215.6000000000001.mm,0.mm], [4754.4.mm,1365.6000000000001.mm,0.mm], [4604.4.mm,1365.6000000000001.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4629.4.mm,1240.6000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4629.4.mm,1340.6000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4729.4.mm,1240.6000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4729.4.mm,1340.6000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot plate
  grp = ents.add_group
  grp.name = "Foot plate"
  face = grp.entities.add_face([5054.4.mm,996.4000000000001.mm,0.mm], [5204.4.mm,996.4000000000001.mm,0.mm], [5204.4.mm,1146.4.mm,0.mm], [5054.4.mm,1146.4.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5079.4.mm,1021.4000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5079.4.mm,1121.4.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5179.4.mm,1021.4000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5179.4.mm,1121.4.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot plate
  grp = ents.add_group
  grp.name = "Foot plate"
  face = grp.entities.add_face([5054.4.mm,1215.6000000000001.mm,0.mm], [5204.4.mm,1215.6000000000001.mm,0.mm], [5204.4.mm,1365.6000000000001.mm,0.mm], [5054.4.mm,1365.6000000000001.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5079.4.mm,1240.6000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5079.4.mm,1340.6000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5179.4.mm,1240.6000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5179.4.mm,1340.6000000000001.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1096.8.mm,90.mm], [5152.mm,1096.8.mm,90.mm], [5152.mm,1136.8.mm,90.mm], [5122.mm,1136.8.mm,90.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1096.8.mm,1118.mm], [5152.mm,1096.8.mm,1118.mm], [5152.mm,1136.8.mm,1118.mm], [5122.mm,1136.8.mm,1118.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1096.8.mm,2146.mm], [5152.mm,1096.8.mm,2146.mm], [5152.mm,1136.8.mm,2146.mm], [5122.mm,1136.8.mm,2146.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1225.2.mm,90.mm], [5152.mm,1225.2.mm,90.mm], [5152.mm,1265.2.mm,90.mm], [5122.mm,1265.2.mm,90.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1225.2.mm,1118.mm], [5152.mm,1225.2.mm,1118.mm], [5152.mm,1265.2.mm,1118.mm], [5122.mm,1265.2.mm,1118.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1225.2.mm,2146.mm], [5152.mm,1225.2.mm,2146.mm], [5152.mm,1265.2.mm,2146.mm], [5122.mm,1265.2.mm,2146.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "IBC Corridor Frame (deep box)"
  inst.layer = model.layers["IBC Frame"]

  # ═══ Left Walkway Support ═══
  defn = model.definitions.add("Left Walkway Support")
  ents = defn.entities
  # Left cantilever 1 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 1 foot plate"
  face = grp.entities.add_face([38.mm,220.mm,0.mm], [166.mm,220.mm,0.mm], [166.mm,280.mm,0.mm], [38.mm,280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 1 post (2x2x0.120 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 1 post (2x2x0.120 SHS)"
  face = grp.entities.add_face([224.6.mm,220.mm,0.mm], [275.4.mm,220.mm,0.mm], [275.4.mm,280.mm,0.mm], [224.6.mm,280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 1 arm (to X580)
  grp = ents.add_group
  grp.name = "Left cantilever 1 arm (to X580)"
  face = grp.entities.add_face([275.4.mm,224.6.mm,89.6.mm], [580.mm,224.6.mm,89.6.mm], [580.mm,275.4.mm,89.6.mm], [275.4.mm,275.4.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 2 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 2 foot plate"
  face = grp.entities.add_face([38.mm,770.mm,0.mm], [166.mm,770.mm,0.mm], [166.mm,830.mm,0.mm], [38.mm,830.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 2 post (2x2x0.120 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 2 post (2x2x0.120 SHS)"
  face = grp.entities.add_face([224.6.mm,770.mm,0.mm], [275.4.mm,770.mm,0.mm], [275.4.mm,830.mm,0.mm], [224.6.mm,830.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 2 arm (to X880)
  grp = ents.add_group
  grp.name = "Left cantilever 2 arm (to X880)"
  face = grp.entities.add_face([275.4.mm,774.6.mm,89.6.mm], [880.mm,774.6.mm,89.6.mm], [880.mm,825.4.mm,89.6.mm], [275.4.mm,825.4.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 3 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 3 foot plate"
  face = grp.entities.add_face([38.mm,1150.mm,0.mm], [166.mm,1150.mm,0.mm], [166.mm,1210.mm,0.mm], [38.mm,1210.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 3 post (2x2x0.120 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 3 post (2x2x0.120 SHS)"
  face = grp.entities.add_face([224.6.mm,1150.mm,0.mm], [275.4.mm,1150.mm,0.mm], [275.4.mm,1210.mm,0.mm], [224.6.mm,1210.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 3 arm (to X880)
  grp = ents.add_group
  grp.name = "Left cantilever 3 arm (to X880)"
  face = grp.entities.add_face([275.4.mm,1154.6.mm,89.6.mm], [880.mm,1154.6.mm,89.6.mm], [880.mm,1205.3999999999999.mm,89.6.mm], [275.4.mm,1205.3999999999999.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 4 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 4 foot plate"
  face = grp.entities.add_face([38.mm,1530.mm,0.mm], [166.mm,1530.mm,0.mm], [166.mm,1590.mm,0.mm], [38.mm,1590.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 4 post (2x2x0.120 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 4 post (2x2x0.120 SHS)"
  face = grp.entities.add_face([224.6.mm,1530.mm,0.mm], [275.4.mm,1530.mm,0.mm], [275.4.mm,1590.mm,0.mm], [224.6.mm,1590.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 4 arm (to X880)
  grp = ents.add_group
  grp.name = "Left cantilever 4 arm (to X880)"
  face = grp.entities.add_face([275.4.mm,1534.6.mm,89.6.mm], [880.mm,1534.6.mm,89.6.mm], [880.mm,1585.3999999999999.mm,89.6.mm], [275.4.mm,1585.3999999999999.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 5 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 5 foot plate"
  face = grp.entities.add_face([38.mm,2080.mm,0.mm], [166.mm,2080.mm,0.mm], [166.mm,2140.mm,0.mm], [38.mm,2140.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 5 post (2x2x0.120 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 5 post (2x2x0.120 SHS)"
  face = grp.entities.add_face([224.6.mm,2080.mm,0.mm], [275.4.mm,2080.mm,0.mm], [275.4.mm,2140.mm,0.mm], [224.6.mm,2140.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 5 arm (to X580)
  grp = ents.add_group
  grp.name = "Left cantilever 5 arm (to X580)"
  face = grp.entities.add_face([275.4.mm,2084.6.mm,89.6.mm], [580.mm,2084.6.mm,89.6.mm], [580.mm,2135.4.mm,89.6.mm], [275.4.mm,2135.4.mm,89.6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.400000000000006.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Left Walkway Support"
  inst.layer = model.layers["Left Support"]


# ── "Labeled" scene callouts (Labels tag — shown only in the "Labeled" scene) ──
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Processing Tray" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("PROCESSING TRAY", anc, Geom::Vector3d.new(400.mm, -700.mm, 700.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
anc = Geom::Point3d.new(2400.mm, 150.mm, 73.mm)
txt = entities.add_text("NEAR WALKWAY", anc, Geom::Vector3d.new(0.mm, -900.mm, 550.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(710.mm, 150.mm, 140.mm)
txt = entities.add_text("NEAR LIFT-OUT
(removable for transport)", anc, Geom::Vector3d.new(-350.mm, -800.mm, 700.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(2400.mm, 2212.mm, 73.mm)
txt = entities.add_text("FAR WALKWAY", anc, Geom::Vector3d.new(300.mm, 500.mm, 900.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4479.mm, 1181.mm, 73.mm)
txt = entities.add_text("RIGHT WALKWAY", anc, Geom::Vector3d.new(750.mm, -200.mm, 650.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(320.mm, 1181.mm, 73.mm)
txt = entities.add_text("LEFT WALKWAY
(removable)", anc, Geom::Vector3d.new(-800.mm, -300.mm, 800.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(2298.mm, 30.mm, 150.mm)
txt = entities.add_text("NEAR/FAR CANTILEVERS", anc, Geom::Vector3d.new(-300.mm, -1000.mm, 450.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4629.mm, 400.mm, 90.mm)
txt = entities.add_text("RIGHT CANTILEVER
(IBC-end support)", anc, Geom::Vector3d.new(700.mm, -300.mm, 700.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(140.mm, 1181.mm, 100.mm)
txt = entities.add_text("LEFT SUPPORT
(floor-leg cantilevers)", anc, Geom::Vector3d.new(-850.mm, -200.mm, 600.mm))
txt.layer = model.layers["Labels"] rescue nil

# ── In-model © + license credit (default layer → shown in every scene) ──
lbb = model.bounds
lanc = Geom::Point3d.new(lbb.min.x, lbb.min.y - 400.mm, lbb.min.z)
entities.add_text("© 2026 Alvin Richards
Licensed under GNU AGPLv3
alvinr.github.io/tbs", lanc)

# ── Type callouts for the "Cantilevers" scene (on the Cantilever Types tag) ──
anc = Geom::Point3d.new(2000.mm, 0.mm, 115.mm)
txt = entities.add_text("FLOOR-LEG CANTILEVER — standard reach
50x50 post on bare floor + arm to the
grate inner edge (X=470)", anc, Geom::Vector3d.new(-200.mm, -300.mm, 800.mm))
txt.layer = model.layers["Cantilever Types"] rescue nil
anc = Geom::Point3d.new(3000.mm, 0.mm, 115.mm)
txt = entities.add_text("FLOOR-LEG CANTILEVER — extended reach
3 of the 5 brackets reach to X=770 on
the drum-exit punch-out (deeper landing)", anc, Geom::Vector3d.new(-200.mm, -300.mm, 800.mm))
txt.layer = model.layers["Cantilever Types"] rescue nil
anc = Geom::Point3d.new(4000.mm, 0.mm, 150.mm)
txt = entities.add_text("STANDARD CANTILEVER
8mm plate / 150 leg / 300 arm
3x M12 (triangular)", anc, Geom::Vector3d.new(0.mm, -300.mm, 720.mm))
txt.layer = model.layers["Cantilever Types"] rescue nil
anc = Geom::Point3d.new(5000.mm, 0.mm, 200.mm)
txt = entities.add_text("WIDENED CANTILEVER (EP / battery zone)
10mm plate / 200 leg / 500 arm
4x M12 (rectangular)", anc, Geom::Vector3d.new(200.mm, -300.mm, 850.mm))
txt.layer = model.layers["Cantilever Types"] rescue nil
anc = Geom::Point3d.new(6000.mm, 0.mm, 115.mm)
txt = entities.add_text("RIGHT WALKWAY — WALL CLEAT (left corners)
8mm back-plate + ext plate + shelf,
the long beam lands on it; M12 through-bolts", anc, Geom::Vector3d.new(-150.mm, -300.mm, 800.mm))
txt.layer = model.layers["Cantilever Types"] rescue nil
anc = Geom::Point3d.new(7000.mm, 0.mm, 270.mm)
txt = entities.add_text("RIGHT WALKWAY — COMBINED CORNER PLATE (right corners)
10mm, carries the walkway right beam (Z70 seat)
+ the BR film rail (web-vertical: Z232 seat / Z270 bolt); 4x M12", anc, Geom::Vector3d.new(0.mm, -300.mm, 850.mm))
txt.layer = model.layers["Cantilever Types"] rescue nil
anc = Geom::Point3d.new(8000.mm, 0.mm, 115.mm)
txt = entities.add_text("RIGHT WALKWAY — CENTER CANTILEVER ARM
40x40 SHS off an IBC corridor upright
(half-lapped at the long beams); M12 clamp", anc, Geom::Vector3d.new(150.mm, -300.mm, 820.mm))
txt.layer = model.layers["Cantilever Types"] rescue nil

model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags from earlier generator versions ──
keep_tags = ["Container", "Processing Tray", "Walkways", "Cantilevers", "Cantilever Types", "Right Cantilever", "Film Plane", "Film Plane Left", "IBC Frame", "Left Support", "Labels"]
default_layer = model.layers[0]
model.layers.to_a.each { |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}

# ── Scenes — one shared iso camera; scenes only toggle visibility ──
model.layers.each { |l| l.visible = true }
model.layers["Labels"].visible = false if model.layers["Labels"]  # frame geometry, not labels
model.layers["Cantilever Types"].visible = false if model.layers["Cantilever Types"]  # catalog shows only in its own scene
bb = model.bounds
ctr = bb.center
dir = Geom::Vector3d.new(-0.55, -0.7, 0.45); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.4)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents
model.active_view.zoom(0.72)   # pull back so callouts have margin (and read larger)

# Overview — all subsystems, Labels + type-catalog OFF; listed first.
model.pages.add("Overview")
[["Walkway", ["Walkways", "Right Cantilever", "Film Plane", "Film Plane Left", "IBC Frame", "Processing Tray"]], ["Near/Far Cantilevers", ["Cantilevers", "Processing Tray"]], ["Left Support", ["Left Support", "Processing Tray"]], ["Right Cantilever", ["Right Cantilever", "IBC Frame", "Processing Tray"]]].each { |name, tags|
  model.layers.each { |l| l.visible = (l == default_layer || l.name == "Container" || tags.include?(l.name)) }
  page = model.pages.add(name)
  page.use_camera = true
}

# ── "Cantilevers" — one of each UNIQUE bracket type, isolated side-by-side with a
#    close-up camera (the only scene showing the Cantilever Types catalog tag; the
#    wall is hidden so the full bracket — plate, arm, gusset, bolts — reads) ──
model.layers.each { |l| l.visible = (l.name == "Cantilever Types") }
ct_tgt = Geom::Point3d.new(5000.mm, -100.mm, 450.mm)
ct_dir = Geom::Vector3d.new(-0.18, -0.84, 0.38); ct_dir.normalize!
ct_eye = ct_tgt.offset(ct_dir, 8800.mm)
ct_cam = Sketchup::Camera.new(ct_eye, ct_tgt, Z_AXIS)
ct_cam.perspective = true
ct_cam.fov = 46
model.active_view.camera = ct_cam
ctp = model.pages.add("Cantilevers")
ctp.use_camera = true

model.layers.each { |l| l.visible = true }
model.layers["Cantilever Types"].visible = false if model.layers["Cantilever Types"]

# Labeled — Overview view + callouts on the major parts, listed LAST (project rule).
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents
model.active_view.zoom(0.72)
model.layers["Labels"].visible = true if model.layers["Labels"]
lpage = model.pages.add("Labeled"); lpage.use_camera = true
model.layers["Labels"].visible = false if model.layers["Labels"]

model.commit_operation
{ success: true, model: "Walkway + Cantilevers",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
