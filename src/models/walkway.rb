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

# ── Sketchfab upload metadata (stamped every regen; keeps the stable model UID) ──
model.name = "TBS-001 Walkway Model"
model.description = "The perimeter walkway provides dry-foot operator access around all four sides of the processing tray without wading through chemical solution."
model.set_attribute("sketchfab", "model_title", "TBS-001 Walkway Model")
model.set_attribute("sketchfab", "model_description", "The perimeter walkway provides dry-foot operator access around all four sides of the processing tray without wading through chemical solution.")
model.set_attribute("sketchfab", "model_id", "96b3d0e5fc8b4fc18c528f64bda028bc")
model.set_attribute("sketchfab", "model_tags", "sketchup")

# ── Tags (layers) ──
  model.layers.add("Container") unless model.layers["Container"]
  model.layers.add("Processing Tray") unless model.layers["Processing Tray"]
  model.layers.add("Walkways") unless model.layers["Walkways"]
  model.layers.add("Cantilevers") unless model.layers["Cantilevers"]
  model.layers.add("Cantilever Types") unless model.layers["Cantilever Types"]
  model.layers.add("Right Cantilever") unless model.layers["Right Cantilever"]
  model.layers.add("Film Plane") unless model.layers["Film Plane"]
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
  face = grp.entities.add_face([170.mm,80.mm,0.mm], [4629.mm,80.mm,0.mm], [4629.mm,2280.mm,0.mm], [170.mm,2280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Tray Shim Base"] || model.materials.add("Tray Shim Base")
  mat.color = Sketchup::Color.new(216, 207, 188)
  mat.alpha = 0.9
  grp.material = mat

  # Processing Tray Floor A
  grp = ents.add_group
  grp.name = "Processing Tray Floor A"
  ge = grp.entities
  f = ge.add_face([170.mm,80.mm,42.295.mm], [4629.mm,80.mm,20.mm], [4629.mm,2280.mm,31.mm])
  f.pushpull(-2.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Processing Tray Floor B
  grp = ents.add_group
  grp.name = "Processing Tray Floor B"
  ge = grp.entities
  f = ge.add_face([170.mm,80.mm,42.295.mm], [4629.mm,2280.mm,31.mm], [170.mm,2280.mm,53.295.mm])
  f.pushpull(-2.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Near
  grp = ents.add_group
  grp.name = "Tray Rim Near"
  face = grp.entities.add_face([170.mm,80.mm,31.1475.mm], [4629.mm,80.mm,31.1475.mm], [4629.mm,82.mm,31.1475.mm], [170.mm,82.mm,31.1475.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Far
  grp = ents.add_group
  grp.name = "Tray Rim Far"
  face = grp.entities.add_face([170.mm,2278.mm,42.1475.mm], [4629.mm,2278.mm,42.1475.mm], [4629.mm,2280.mm,42.1475.mm], [170.mm,2280.mm,42.1475.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Left
  grp = ents.add_group
  grp.name = "Tray Rim Left"
  face = grp.entities.add_face([170.mm,80.mm,47.795.mm], [172.mm,80.mm,47.795.mm], [172.mm,2280.mm,47.795.mm], [170.mm,2280.mm,47.795.mm])
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
  face = grp.entities.add_face([172.mm,82.mm,36.6475.mm], [4627.mm,82.mm,36.6475.mm], [4627.mm,2278.mm,36.6475.mm], [172.mm,2278.mm,36.6475.mm])
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
  face = grp.entities.add_face([470.mm,8.mm,115.mm], [950.mm,8.mm,115.mm], [950.mm,300.mm,115.mm], [470.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (door-end, removable)"] || model.materials.add("Walkway Near (door-end, removable)")
  mat.color = Sketchup::Color.new(192, 96, 0)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near (left)
  grp = ents.add_group
  grp.name = "Walkway Near (left)"
  face = grp.entities.add_face([950.mm,8.mm,115.mm], [1525.mm,8.mm,115.mm], [1525.mm,300.mm,115.mm], [950.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left)"] || model.materials.add("Walkway Near (left)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near (widened)
  grp = ents.add_group
  grp.name = "Walkway Near (widened)"
  face = grp.entities.add_face([1525.mm,10.mm,115.mm], [2999.mm,10.mm,115.mm], [2999.mm,500.mm,115.mm], [1525.mm,500.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left)"] || model.materials.add("Walkway Near (left)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near (right)
  grp = ents.add_group
  grp.name = "Walkway Near (right)"
  face = grp.entities.add_face([2999.mm,8.mm,115.mm], [4329.mm,8.mm,115.mm], [4329.mm,300.mm,115.mm], [2999.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left)"] || model.materials.add("Walkway Near (left)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far
  grp = ents.add_group
  grp.name = "Walkway Far"
  face = grp.entities.add_face([470.mm,2062.mm,115.mm], [4329.mm,2062.mm,115.mm], [4329.mm,2354.mm,115.mm], [470.mm,2354.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left)"] || model.materials.add("Walkway Near (left)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Left (removable)
  grp = ents.add_group
  grp.name = "Walkway Left (removable)"
  face = grp.entities.add_face([170.mm,0.mm,115.mm], [470.mm,0.mm,115.mm], [470.mm,2362.mm,115.mm], [170.mm,2362.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (door-end, removable)"] || model.materials.add("Walkway Near (door-end, removable)")
  mat.color = Sketchup::Color.new(192, 96, 0)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Left punch-out
  grp = ents.add_group
  grp.name = "Walkway Left punch-out"
  face = grp.entities.add_face([470.mm,800.mm,115.mm], [770.mm,800.mm,115.mm], [770.mm,1560.mm,115.mm], [470.mm,1560.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (door-end, removable)"] || model.materials.add("Walkway Near (door-end, removable)")
  mat.color = Sketchup::Color.new(192, 96, 0)
  mat.alpha = 1.0
  grp.material = mat

  # Right walkway grate (cantilevered)
  grp = ents.add_group
  grp.name = "Right walkway grate (cantilevered)"
  face = grp.entities.add_face([4329.mm,0.mm,115.mm], [4629.mm,0.mm,115.mm], [4629.mm,2362.mm,115.mm], [4329.mm,2362.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left)"] || model.materials.add("Walkway Near (left)")
  mat.color = Sketchup::Color.new(128, 128, 128)
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
  face = grp.entities.add_face([638.mm,0.mm,0.mm], [758.mm,0.mm,0.mm], [758.mm,8.mm,0.mm], [638.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 1 arm
  grp = ents.add_group
  grp.name = "Cantilever Near 1 arm"
  face = grp.entities.add_face([694.mm,8.mm,105.mm], [702.mm,8.mm,105.mm], [702.mm,300.mm,105.mm], [694.mm,300.mm,105.mm])
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
  f = ge.add_face([694.mm,8.mm,0.mm], [694.mm,8.mm,105.mm], [694.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 1 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Near 1 ext reinf plate"
  face = grp.entities.add_face([648.mm,-46.mm,0.mm], [748.mm,-46.mm,0.mm], [748.mm,-40.mm,0.mm], [648.mm,-40.mm,0.mm])
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
  circle = ge.add_circle([698.mm,-46.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 1 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 1 bolt head"
  face = grp.entities.add_face([689.mm,-52.mm,111.mm], [707.mm,-52.mm,111.mm], [707.mm,-46.mm,111.mm], [689.mm,-46.mm,111.mm])
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
  circle = ge.add_circle([666.mm,-46.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 1 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 1 bolt head"
  face = grp.entities.add_face([657.mm,-52.mm,33.mm], [675.mm,-52.mm,33.mm], [675.mm,-46.mm,33.mm], [657.mm,-46.mm,33.mm])
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
  circle = ge.add_circle([730.mm,-46.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 1 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 1 bolt head"
  face = grp.entities.add_face([721.mm,-52.mm,33.mm], [739.mm,-52.mm,33.mm], [739.mm,-46.mm,33.mm], [721.mm,-46.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 plate
  grp = ents.add_group
  grp.name = "Cantilever Near 2 plate"
  face = grp.entities.add_face([1095.mm,0.mm,0.mm], [1215.mm,0.mm,0.mm], [1215.mm,8.mm,0.mm], [1095.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 arm
  grp = ents.add_group
  grp.name = "Cantilever Near 2 arm"
  face = grp.entities.add_face([1151.mm,8.mm,105.mm], [1159.mm,8.mm,105.mm], [1159.mm,300.mm,105.mm], [1151.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 gusset
  grp = ents.add_group
  grp.name = "Cantilever Near 2 gusset"
  ge = grp.entities
  f = ge.add_face([1151.mm,8.mm,0.mm], [1151.mm,8.mm,105.mm], [1151.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Near 2 ext reinf plate"
  face = grp.entities.add_face([1105.mm,-46.mm,0.mm], [1205.mm,-46.mm,0.mm], [1205.mm,-40.mm,0.mm], [1105.mm,-40.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(180.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 2 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1155.mm,-46.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 2 bolt head"
  face = grp.entities.add_face([1146.mm,-52.mm,111.mm], [1164.mm,-52.mm,111.mm], [1164.mm,-46.mm,111.mm], [1146.mm,-46.mm,111.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 2 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1123.mm,-46.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 2 bolt head"
  face = grp.entities.add_face([1114.mm,-52.mm,33.mm], [1132.mm,-52.mm,33.mm], [1132.mm,-46.mm,33.mm], [1114.mm,-46.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 2 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1187.mm,-46.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 2 bolt head"
  face = grp.entities.add_face([1178.mm,-52.mm,33.mm], [1196.mm,-52.mm,33.mm], [1196.mm,-46.mm,33.mm], [1178.mm,-46.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 3 (widened) plate
  grp = ents.add_group
  grp.name = "Cantilever Near 3 (widened) plate"
  face = grp.entities.add_face([1552.mm,0.mm,0.mm], [1672.mm,0.mm,0.mm], [1672.mm,10.mm,0.mm], [1552.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 3 (widened) arm
  grp = ents.add_group
  grp.name = "Cantilever Near 3 (widened) arm"
  face = grp.entities.add_face([1607.mm,10.mm,103.mm], [1617.mm,10.mm,103.mm], [1617.mm,500.mm,103.mm], [1607.mm,500.mm,103.mm])
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
  f = ge.add_face([1607.mm,10.mm,0.mm], [1607.mm,10.mm,103.mm], [1607.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 3 (widened) ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Near 3 (widened) ext reinf plate"
  face = grp.entities.add_face([1552.mm,-46.mm,0.mm], [1672.mm,-46.mm,0.mm], [1672.mm,-40.mm,0.mm], [1552.mm,-40.mm,0.mm])
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
  circle = ge.add_circle([1580.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 3 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 3 (widened) bolt head"
  face = grp.entities.add_face([1571.mm,-52.mm,26.mm], [1589.mm,-52.mm,26.mm], [1589.mm,-46.mm,26.mm], [1571.mm,-46.mm,26.mm])
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
  circle = ge.add_circle([1644.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 3 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 3 (widened) bolt head"
  face = grp.entities.add_face([1635.mm,-52.mm,26.mm], [1653.mm,-52.mm,26.mm], [1653.mm,-46.mm,26.mm], [1635.mm,-46.mm,26.mm])
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
  circle = ge.add_circle([1580.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 3 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 3 (widened) bolt head"
  face = grp.entities.add_face([1571.mm,-52.mm,151.mm], [1589.mm,-52.mm,151.mm], [1589.mm,-46.mm,151.mm], [1571.mm,-46.mm,151.mm])
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
  circle = ge.add_circle([1644.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 3 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 3 (widened) bolt head"
  face = grp.entities.add_face([1635.mm,-52.mm,151.mm], [1653.mm,-52.mm,151.mm], [1653.mm,-46.mm,151.mm], [1635.mm,-46.mm,151.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 4 (widened) plate
  grp = ents.add_group
  grp.name = "Cantilever Near 4 (widened) plate"
  face = grp.entities.add_face([2009.mm,0.mm,0.mm], [2129.mm,0.mm,0.mm], [2129.mm,10.mm,0.mm], [2009.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 4 (widened) arm
  grp = ents.add_group
  grp.name = "Cantilever Near 4 (widened) arm"
  face = grp.entities.add_face([2064.mm,10.mm,103.mm], [2074.mm,10.mm,103.mm], [2074.mm,500.mm,103.mm], [2064.mm,500.mm,103.mm])
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
  f = ge.add_face([2064.mm,10.mm,0.mm], [2064.mm,10.mm,103.mm], [2064.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 4 (widened) ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Near 4 (widened) ext reinf plate"
  face = grp.entities.add_face([2009.mm,-46.mm,0.mm], [2129.mm,-46.mm,0.mm], [2129.mm,-40.mm,0.mm], [2009.mm,-40.mm,0.mm])
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
  circle = ge.add_circle([2037.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 4 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 4 (widened) bolt head"
  face = grp.entities.add_face([2028.mm,-52.mm,26.mm], [2046.mm,-52.mm,26.mm], [2046.mm,-46.mm,26.mm], [2028.mm,-46.mm,26.mm])
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
  circle = ge.add_circle([2101.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 4 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 4 (widened) bolt head"
  face = grp.entities.add_face([2092.mm,-52.mm,26.mm], [2110.mm,-52.mm,26.mm], [2110.mm,-46.mm,26.mm], [2092.mm,-46.mm,26.mm])
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
  circle = ge.add_circle([2037.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 4 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 4 (widened) bolt head"
  face = grp.entities.add_face([2028.mm,-52.mm,151.mm], [2046.mm,-52.mm,151.mm], [2046.mm,-46.mm,151.mm], [2028.mm,-46.mm,151.mm])
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
  circle = ge.add_circle([2101.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 4 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 4 (widened) bolt head"
  face = grp.entities.add_face([2092.mm,-52.mm,151.mm], [2110.mm,-52.mm,151.mm], [2110.mm,-46.mm,151.mm], [2092.mm,-46.mm,151.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 5 (widened) plate
  grp = ents.add_group
  grp.name = "Cantilever Near 5 (widened) plate"
  face = grp.entities.add_face([2466.mm,0.mm,0.mm], [2586.mm,0.mm,0.mm], [2586.mm,10.mm,0.mm], [2466.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 5 (widened) arm
  grp = ents.add_group
  grp.name = "Cantilever Near 5 (widened) arm"
  face = grp.entities.add_face([2521.mm,10.mm,103.mm], [2531.mm,10.mm,103.mm], [2531.mm,500.mm,103.mm], [2521.mm,500.mm,103.mm])
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
  f = ge.add_face([2521.mm,10.mm,0.mm], [2521.mm,10.mm,103.mm], [2521.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 5 (widened) ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Near 5 (widened) ext reinf plate"
  face = grp.entities.add_face([2466.mm,-46.mm,0.mm], [2586.mm,-46.mm,0.mm], [2586.mm,-40.mm,0.mm], [2466.mm,-40.mm,0.mm])
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
  circle = ge.add_circle([2494.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 5 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 5 (widened) bolt head"
  face = grp.entities.add_face([2485.mm,-52.mm,26.mm], [2503.mm,-52.mm,26.mm], [2503.mm,-46.mm,26.mm], [2485.mm,-46.mm,26.mm])
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
  circle = ge.add_circle([2558.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 5 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 5 (widened) bolt head"
  face = grp.entities.add_face([2549.mm,-52.mm,26.mm], [2567.mm,-52.mm,26.mm], [2567.mm,-46.mm,26.mm], [2549.mm,-46.mm,26.mm])
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
  circle = ge.add_circle([2494.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 5 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 5 (widened) bolt head"
  face = grp.entities.add_face([2485.mm,-52.mm,151.mm], [2503.mm,-52.mm,151.mm], [2503.mm,-46.mm,151.mm], [2485.mm,-46.mm,151.mm])
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
  circle = ge.add_circle([2558.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 5 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 5 (widened) bolt head"
  face = grp.entities.add_face([2549.mm,-52.mm,151.mm], [2567.mm,-52.mm,151.mm], [2567.mm,-46.mm,151.mm], [2549.mm,-46.mm,151.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 (widened) plate
  grp = ents.add_group
  grp.name = "Cantilever Near 6 (widened) plate"
  face = grp.entities.add_face([2923.mm,0.mm,0.mm], [3043.mm,0.mm,0.mm], [3043.mm,10.mm,0.mm], [2923.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 (widened) arm
  grp = ents.add_group
  grp.name = "Cantilever Near 6 (widened) arm"
  face = grp.entities.add_face([2978.mm,10.mm,103.mm], [2988.mm,10.mm,103.mm], [2988.mm,500.mm,103.mm], [2978.mm,500.mm,103.mm])
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
  f = ge.add_face([2978.mm,10.mm,0.mm], [2978.mm,10.mm,103.mm], [2978.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 (widened) ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Near 6 (widened) ext reinf plate"
  face = grp.entities.add_face([2923.mm,-46.mm,0.mm], [3043.mm,-46.mm,0.mm], [3043.mm,-40.mm,0.mm], [2923.mm,-40.mm,0.mm])
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
  circle = ge.add_circle([2951.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 6 (widened) bolt head"
  face = grp.entities.add_face([2942.mm,-52.mm,26.mm], [2960.mm,-52.mm,26.mm], [2960.mm,-46.mm,26.mm], [2942.mm,-46.mm,26.mm])
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
  circle = ge.add_circle([3015.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 6 (widened) bolt head"
  face = grp.entities.add_face([3006.mm,-52.mm,26.mm], [3024.mm,-52.mm,26.mm], [3024.mm,-46.mm,26.mm], [3006.mm,-46.mm,26.mm])
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
  circle = ge.add_circle([2951.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 6 (widened) bolt head"
  face = grp.entities.add_face([2942.mm,-52.mm,151.mm], [2960.mm,-52.mm,151.mm], [2960.mm,-46.mm,151.mm], [2942.mm,-46.mm,151.mm])
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
  circle = ge.add_circle([3015.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 6 (widened) bolt head"
  face = grp.entities.add_face([3006.mm,-52.mm,151.mm], [3024.mm,-52.mm,151.mm], [3024.mm,-46.mm,151.mm], [3006.mm,-46.mm,151.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 7 plate
  grp = ents.add_group
  grp.name = "Cantilever Near 7 plate"
  face = grp.entities.add_face([3380.mm,0.mm,0.mm], [3500.mm,0.mm,0.mm], [3500.mm,8.mm,0.mm], [3380.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 7 arm
  grp = ents.add_group
  grp.name = "Cantilever Near 7 arm"
  face = grp.entities.add_face([3436.mm,8.mm,105.mm], [3444.mm,8.mm,105.mm], [3444.mm,300.mm,105.mm], [3436.mm,300.mm,105.mm])
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
  f = ge.add_face([3436.mm,8.mm,0.mm], [3436.mm,8.mm,105.mm], [3436.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 7 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Near 7 ext reinf plate"
  face = grp.entities.add_face([3390.mm,-46.mm,0.mm], [3490.mm,-46.mm,0.mm], [3490.mm,-40.mm,0.mm], [3390.mm,-40.mm,0.mm])
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
  circle = ge.add_circle([3440.mm,-46.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 7 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 7 bolt head"
  face = grp.entities.add_face([3431.mm,-52.mm,111.mm], [3449.mm,-52.mm,111.mm], [3449.mm,-46.mm,111.mm], [3431.mm,-46.mm,111.mm])
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
  circle = ge.add_circle([3408.mm,-46.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 7 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 7 bolt head"
  face = grp.entities.add_face([3399.mm,-52.mm,33.mm], [3417.mm,-52.mm,33.mm], [3417.mm,-46.mm,33.mm], [3399.mm,-46.mm,33.mm])
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
  circle = ge.add_circle([3472.mm,-46.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 7 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 7 bolt head"
  face = grp.entities.add_face([3463.mm,-52.mm,33.mm], [3481.mm,-52.mm,33.mm], [3481.mm,-46.mm,33.mm], [3463.mm,-46.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 8 plate
  grp = ents.add_group
  grp.name = "Cantilever Near 8 plate"
  face = grp.entities.add_face([3837.mm,0.mm,0.mm], [3957.mm,0.mm,0.mm], [3957.mm,8.mm,0.mm], [3837.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 8 arm
  grp = ents.add_group
  grp.name = "Cantilever Near 8 arm"
  face = grp.entities.add_face([3893.mm,8.mm,105.mm], [3901.mm,8.mm,105.mm], [3901.mm,300.mm,105.mm], [3893.mm,300.mm,105.mm])
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
  f = ge.add_face([3893.mm,8.mm,0.mm], [3893.mm,8.mm,105.mm], [3893.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 8 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Near 8 ext reinf plate"
  face = grp.entities.add_face([3847.mm,-46.mm,0.mm], [3947.mm,-46.mm,0.mm], [3947.mm,-40.mm,0.mm], [3847.mm,-40.mm,0.mm])
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
  circle = ge.add_circle([3897.mm,-46.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 8 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 8 bolt head"
  face = grp.entities.add_face([3888.mm,-52.mm,111.mm], [3906.mm,-52.mm,111.mm], [3906.mm,-46.mm,111.mm], [3888.mm,-46.mm,111.mm])
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
  circle = ge.add_circle([3865.mm,-46.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 8 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 8 bolt head"
  face = grp.entities.add_face([3856.mm,-52.mm,33.mm], [3874.mm,-52.mm,33.mm], [3874.mm,-46.mm,33.mm], [3856.mm,-46.mm,33.mm])
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
  circle = ge.add_circle([3929.mm,-46.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 8 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 8 bolt head"
  face = grp.entities.add_face([3920.mm,-52.mm,33.mm], [3938.mm,-52.mm,33.mm], [3938.mm,-46.mm,33.mm], [3920.mm,-46.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 1 plate
  grp = ents.add_group
  grp.name = "Cantilever Far 1 plate"
  face = grp.entities.add_face([638.mm,2354.mm,0.mm], [758.mm,2354.mm,0.mm], [758.mm,2362.mm,0.mm], [638.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 1 arm
  grp = ents.add_group
  grp.name = "Cantilever Far 1 arm"
  face = grp.entities.add_face([694.mm,2062.mm,105.mm], [702.mm,2062.mm,105.mm], [702.mm,2354.mm,105.mm], [694.mm,2354.mm,105.mm])
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
  f = ge.add_face([694.mm,2354.mm,0.mm], [694.mm,2354.mm,105.mm], [694.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 1 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Far 1 ext reinf plate"
  face = grp.entities.add_face([648.mm,2402.mm,0.mm], [748.mm,2402.mm,0.mm], [748.mm,2408.mm,0.mm], [648.mm,2408.mm,0.mm])
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
  circle = ge.add_circle([698.mm,2354.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 1 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 1 bolt head"
  face = grp.entities.add_face([689.mm,2408.mm,111.mm], [707.mm,2408.mm,111.mm], [707.mm,2414.mm,111.mm], [689.mm,2414.mm,111.mm])
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
  circle = ge.add_circle([666.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 1 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 1 bolt head"
  face = grp.entities.add_face([657.mm,2408.mm,33.mm], [675.mm,2408.mm,33.mm], [675.mm,2414.mm,33.mm], [657.mm,2414.mm,33.mm])
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
  circle = ge.add_circle([730.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 1 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 1 bolt head"
  face = grp.entities.add_face([721.mm,2408.mm,33.mm], [739.mm,2408.mm,33.mm], [739.mm,2414.mm,33.mm], [721.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 2 plate
  grp = ents.add_group
  grp.name = "Cantilever Far 2 plate"
  face = grp.entities.add_face([1095.mm,2354.mm,0.mm], [1215.mm,2354.mm,0.mm], [1215.mm,2362.mm,0.mm], [1095.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 2 arm
  grp = ents.add_group
  grp.name = "Cantilever Far 2 arm"
  face = grp.entities.add_face([1151.mm,2062.mm,105.mm], [1159.mm,2062.mm,105.mm], [1159.mm,2354.mm,105.mm], [1151.mm,2354.mm,105.mm])
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
  f = ge.add_face([1151.mm,2354.mm,0.mm], [1151.mm,2354.mm,105.mm], [1151.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 2 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Far 2 ext reinf plate"
  face = grp.entities.add_face([1105.mm,2402.mm,0.mm], [1205.mm,2402.mm,0.mm], [1205.mm,2408.mm,0.mm], [1105.mm,2408.mm,0.mm])
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
  circle = ge.add_circle([1155.mm,2354.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 2 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 2 bolt head"
  face = grp.entities.add_face([1146.mm,2408.mm,111.mm], [1164.mm,2408.mm,111.mm], [1164.mm,2414.mm,111.mm], [1146.mm,2414.mm,111.mm])
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
  circle = ge.add_circle([1123.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 2 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 2 bolt head"
  face = grp.entities.add_face([1114.mm,2408.mm,33.mm], [1132.mm,2408.mm,33.mm], [1132.mm,2414.mm,33.mm], [1114.mm,2414.mm,33.mm])
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
  circle = ge.add_circle([1187.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 2 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 2 bolt head"
  face = grp.entities.add_face([1178.mm,2408.mm,33.mm], [1196.mm,2408.mm,33.mm], [1196.mm,2414.mm,33.mm], [1178.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 3 plate
  grp = ents.add_group
  grp.name = "Cantilever Far 3 plate"
  face = grp.entities.add_face([1552.mm,2354.mm,0.mm], [1672.mm,2354.mm,0.mm], [1672.mm,2362.mm,0.mm], [1552.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 3 arm
  grp = ents.add_group
  grp.name = "Cantilever Far 3 arm"
  face = grp.entities.add_face([1608.mm,2062.mm,105.mm], [1616.mm,2062.mm,105.mm], [1616.mm,2354.mm,105.mm], [1608.mm,2354.mm,105.mm])
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
  f = ge.add_face([1608.mm,2354.mm,0.mm], [1608.mm,2354.mm,105.mm], [1608.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 3 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Far 3 ext reinf plate"
  face = grp.entities.add_face([1562.mm,2402.mm,0.mm], [1662.mm,2402.mm,0.mm], [1662.mm,2408.mm,0.mm], [1562.mm,2408.mm,0.mm])
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
  circle = ge.add_circle([1612.mm,2354.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 3 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 3 bolt head"
  face = grp.entities.add_face([1603.mm,2408.mm,111.mm], [1621.mm,2408.mm,111.mm], [1621.mm,2414.mm,111.mm], [1603.mm,2414.mm,111.mm])
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
  circle = ge.add_circle([1580.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 3 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 3 bolt head"
  face = grp.entities.add_face([1571.mm,2408.mm,33.mm], [1589.mm,2408.mm,33.mm], [1589.mm,2414.mm,33.mm], [1571.mm,2414.mm,33.mm])
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
  circle = ge.add_circle([1644.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 3 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 3 bolt head"
  face = grp.entities.add_face([1635.mm,2408.mm,33.mm], [1653.mm,2408.mm,33.mm], [1653.mm,2414.mm,33.mm], [1635.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 4 plate
  grp = ents.add_group
  grp.name = "Cantilever Far 4 plate"
  face = grp.entities.add_face([2009.mm,2354.mm,0.mm], [2129.mm,2354.mm,0.mm], [2129.mm,2362.mm,0.mm], [2009.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 4 arm
  grp = ents.add_group
  grp.name = "Cantilever Far 4 arm"
  face = grp.entities.add_face([2065.mm,2062.mm,105.mm], [2073.mm,2062.mm,105.mm], [2073.mm,2354.mm,105.mm], [2065.mm,2354.mm,105.mm])
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
  f = ge.add_face([2065.mm,2354.mm,0.mm], [2065.mm,2354.mm,105.mm], [2065.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 4 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Far 4 ext reinf plate"
  face = grp.entities.add_face([2019.mm,2402.mm,0.mm], [2119.mm,2402.mm,0.mm], [2119.mm,2408.mm,0.mm], [2019.mm,2408.mm,0.mm])
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
  circle = ge.add_circle([2069.mm,2354.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 4 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 4 bolt head"
  face = grp.entities.add_face([2060.mm,2408.mm,111.mm], [2078.mm,2408.mm,111.mm], [2078.mm,2414.mm,111.mm], [2060.mm,2414.mm,111.mm])
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
  circle = ge.add_circle([2037.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 4 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 4 bolt head"
  face = grp.entities.add_face([2028.mm,2408.mm,33.mm], [2046.mm,2408.mm,33.mm], [2046.mm,2414.mm,33.mm], [2028.mm,2414.mm,33.mm])
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
  circle = ge.add_circle([2101.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 4 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 4 bolt head"
  face = grp.entities.add_face([2092.mm,2408.mm,33.mm], [2110.mm,2408.mm,33.mm], [2110.mm,2414.mm,33.mm], [2092.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 5 plate
  grp = ents.add_group
  grp.name = "Cantilever Far 5 plate"
  face = grp.entities.add_face([2466.mm,2354.mm,0.mm], [2586.mm,2354.mm,0.mm], [2586.mm,2362.mm,0.mm], [2466.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 5 arm
  grp = ents.add_group
  grp.name = "Cantilever Far 5 arm"
  face = grp.entities.add_face([2522.mm,2062.mm,105.mm], [2530.mm,2062.mm,105.mm], [2530.mm,2354.mm,105.mm], [2522.mm,2354.mm,105.mm])
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
  f = ge.add_face([2522.mm,2354.mm,0.mm], [2522.mm,2354.mm,105.mm], [2522.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 5 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Far 5 ext reinf plate"
  face = grp.entities.add_face([2476.mm,2402.mm,0.mm], [2576.mm,2402.mm,0.mm], [2576.mm,2408.mm,0.mm], [2476.mm,2408.mm,0.mm])
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
  circle = ge.add_circle([2526.mm,2354.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 5 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 5 bolt head"
  face = grp.entities.add_face([2517.mm,2408.mm,111.mm], [2535.mm,2408.mm,111.mm], [2535.mm,2414.mm,111.mm], [2517.mm,2414.mm,111.mm])
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
  circle = ge.add_circle([2494.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 5 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 5 bolt head"
  face = grp.entities.add_face([2485.mm,2408.mm,33.mm], [2503.mm,2408.mm,33.mm], [2503.mm,2414.mm,33.mm], [2485.mm,2414.mm,33.mm])
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
  circle = ge.add_circle([2558.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 5 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 5 bolt head"
  face = grp.entities.add_face([2549.mm,2408.mm,33.mm], [2567.mm,2408.mm,33.mm], [2567.mm,2414.mm,33.mm], [2549.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 6 plate
  grp = ents.add_group
  grp.name = "Cantilever Far 6 plate"
  face = grp.entities.add_face([2923.mm,2354.mm,0.mm], [3043.mm,2354.mm,0.mm], [3043.mm,2362.mm,0.mm], [2923.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 6 arm
  grp = ents.add_group
  grp.name = "Cantilever Far 6 arm"
  face = grp.entities.add_face([2979.mm,2062.mm,105.mm], [2987.mm,2062.mm,105.mm], [2987.mm,2354.mm,105.mm], [2979.mm,2354.mm,105.mm])
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
  f = ge.add_face([2979.mm,2354.mm,0.mm], [2979.mm,2354.mm,105.mm], [2979.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 6 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Far 6 ext reinf plate"
  face = grp.entities.add_face([2933.mm,2402.mm,0.mm], [3033.mm,2402.mm,0.mm], [3033.mm,2408.mm,0.mm], [2933.mm,2408.mm,0.mm])
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
  circle = ge.add_circle([2983.mm,2354.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 6 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 6 bolt head"
  face = grp.entities.add_face([2974.mm,2408.mm,111.mm], [2992.mm,2408.mm,111.mm], [2992.mm,2414.mm,111.mm], [2974.mm,2414.mm,111.mm])
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
  circle = ge.add_circle([2951.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 6 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 6 bolt head"
  face = grp.entities.add_face([2942.mm,2408.mm,33.mm], [2960.mm,2408.mm,33.mm], [2960.mm,2414.mm,33.mm], [2942.mm,2414.mm,33.mm])
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
  circle = ge.add_circle([3015.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 6 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 6 bolt head"
  face = grp.entities.add_face([3006.mm,2408.mm,33.mm], [3024.mm,2408.mm,33.mm], [3024.mm,2414.mm,33.mm], [3006.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 7 plate
  grp = ents.add_group
  grp.name = "Cantilever Far 7 plate"
  face = grp.entities.add_face([3380.mm,2354.mm,0.mm], [3500.mm,2354.mm,0.mm], [3500.mm,2362.mm,0.mm], [3380.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 7 arm
  grp = ents.add_group
  grp.name = "Cantilever Far 7 arm"
  face = grp.entities.add_face([3436.mm,2062.mm,105.mm], [3444.mm,2062.mm,105.mm], [3444.mm,2354.mm,105.mm], [3436.mm,2354.mm,105.mm])
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
  f = ge.add_face([3436.mm,2354.mm,0.mm], [3436.mm,2354.mm,105.mm], [3436.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 7 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Far 7 ext reinf plate"
  face = grp.entities.add_face([3390.mm,2402.mm,0.mm], [3490.mm,2402.mm,0.mm], [3490.mm,2408.mm,0.mm], [3390.mm,2408.mm,0.mm])
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
  circle = ge.add_circle([3440.mm,2354.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 7 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 7 bolt head"
  face = grp.entities.add_face([3431.mm,2408.mm,111.mm], [3449.mm,2408.mm,111.mm], [3449.mm,2414.mm,111.mm], [3431.mm,2414.mm,111.mm])
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
  circle = ge.add_circle([3408.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 7 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 7 bolt head"
  face = grp.entities.add_face([3399.mm,2408.mm,33.mm], [3417.mm,2408.mm,33.mm], [3417.mm,2414.mm,33.mm], [3399.mm,2414.mm,33.mm])
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
  circle = ge.add_circle([3472.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 7 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 7 bolt head"
  face = grp.entities.add_face([3463.mm,2408.mm,33.mm], [3481.mm,2408.mm,33.mm], [3481.mm,2414.mm,33.mm], [3463.mm,2414.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 8 plate
  grp = ents.add_group
  grp.name = "Cantilever Far 8 plate"
  face = grp.entities.add_face([3837.mm,2354.mm,0.mm], [3957.mm,2354.mm,0.mm], [3957.mm,2362.mm,0.mm], [3837.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 8 arm
  grp = ents.add_group
  grp.name = "Cantilever Far 8 arm"
  face = grp.entities.add_face([3893.mm,2062.mm,105.mm], [3901.mm,2062.mm,105.mm], [3901.mm,2354.mm,105.mm], [3893.mm,2354.mm,105.mm])
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
  f = ge.add_face([3893.mm,2354.mm,0.mm], [3893.mm,2354.mm,105.mm], [3893.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 8 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Far 8 ext reinf plate"
  face = grp.entities.add_face([3847.mm,2402.mm,0.mm], [3947.mm,2402.mm,0.mm], [3947.mm,2408.mm,0.mm], [3847.mm,2408.mm,0.mm])
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
  circle = ge.add_circle([3897.mm,2354.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 8 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 8 bolt head"
  face = grp.entities.add_face([3888.mm,2408.mm,111.mm], [3906.mm,2408.mm,111.mm], [3906.mm,2414.mm,111.mm], [3888.mm,2414.mm,111.mm])
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
  circle = ge.add_circle([3865.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 8 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 8 bolt head"
  face = grp.entities.add_face([3856.mm,2408.mm,33.mm], [3874.mm,2408.mm,33.mm], [3874.mm,2414.mm,33.mm], [3856.mm,2414.mm,33.mm])
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
  circle = ge.add_circle([3929.mm,2354.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Far 8 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Far 8 bolt head"
  face = grp.entities.add_face([3920.mm,2408.mm,33.mm], [3938.mm,2408.mm,33.mm], [3938.mm,2414.mm,33.mm], [3920.mm,2414.mm,33.mm])
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

  # Type FloorCant short post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Type FloorCant short post (50x50x3 SHS)"
  face = grp.entities.add_face([1975.mm,0.mm,0.mm], [2025.mm,0.mm,0.mm], [2025.mm,60.mm,0.mm], [1975.mm,60.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type FloorCant short arm (to X470)
  grp = ents.add_group
  grp.name = "Type FloorCant short arm (to X470)"
  face = grp.entities.add_face([2025.mm,0.mm,75.mm], [2330.mm,0.mm,75.mm], [2330.mm,40.mm,75.mm], [2025.mm,40.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
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

  # Type FloorCant long post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Type FloorCant long post (50x50x3 SHS)"
  face = grp.entities.add_face([2975.mm,0.mm,0.mm], [3025.mm,0.mm,0.mm], [3025.mm,60.mm,0.mm], [2975.mm,60.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type FloorCant long arm (to X770)
  grp = ents.add_group
  grp.name = "Type FloorCant long arm (to X770)"
  face = grp.entities.add_face([3025.mm,0.mm,75.mm], [3630.mm,0.mm,75.mm], [3630.mm,40.mm,75.mm], [3025.mm,40.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  mat.color = Sketchup::Color.new(80, 80, 88)
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
  face = grp.entities.add_face([5955.mm,0.mm,60.mm], [6045.mm,0.mm,60.mm], [6045.mm,8.mm,60.mm], [5955.mm,8.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(65.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat ext plate (Type RWk Cleat)
  grp = ents.add_group
  grp.name = "RWk wall cleat ext plate (Type RWk Cleat)"
  face = grp.entities.add_face([5955.mm,-48.mm,60.mm], [6045.mm,-48.mm,60.mm], [6045.mm,-40.mm,60.mm], [5955.mm,-40.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(65.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat shelf (Type RWk Cleat)
  grp = ents.add_group
  grp.name = "RWk wall cleat shelf (Type RWk Cleat)"
  face = grp.entities.add_face([5955.mm,0.mm,60.mm], [6045.mm,0.mm,60.mm], [6045.mm,55.mm,60.mm], [5955.mm,55.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall bolt (Type RWk Cleat) Z76
  grp = ents.add_group
  grp.name = "RWk wall bolt (Type RWk Cleat) Z76"
  ge = grp.entities
  circle = ge.add_circle([6000.mm,-48.mm,76.mm], [0,1,0], 5.mm, 24)
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
  face = grp.entities.add_face([6925.mm,0.mm,58.mm], [7075.mm,0.mm,58.mm], [7075.mm,10.mm,58.mm], [6925.mm,10.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(167.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner ext plate (near)
  grp = ents.add_group
  grp.name = "FP combined corner ext plate (near)"
  face = grp.entities.add_face([6925.mm,-50.mm,58.mm], [7075.mm,-50.mm,58.mm], [7075.mm,-40.mm,58.mm], [6925.mm,-40.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(167.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined right-beam seat (near)
  grp = ents.add_group
  grp.name = "FP combined right-beam seat (near)"
  face = grp.entities.add_face([6925.mm,0.mm,58.mm], [7075.mm,0.mm,58.mm], [7075.mm,55.mm,58.mm], [6925.mm,55.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined BR rail seat (near)
  grp = ents.add_group
  grp.name = "FP combined BR rail seat (near)"
  face = grp.entities.add_face([6970.mm,0.mm,138.mm], [7030.mm,0.mm,138.mm], [7030.mm,55.mm,138.mm], [6970.mm,55.mm,138.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X6950 Z84
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X6950 Z84"
  ge = grp.entities
  circle = ge.add_circle([6950.mm,-50.mm,84.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X6950 Z178
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X6950 Z178"
  ge = grp.entities
  circle = ge.add_circle([6950.mm,-50.mm,178.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X7050 Z84
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X7050 Z84"
  ge = grp.entities
  circle = ge.add_circle([7050.mm,-50.mm,84.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X7050 Z178
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X7050 Z178"
  ge = grp.entities
  circle = ge.add_circle([7050.mm,-50.mm,178.mm], [0,1,0], 6.mm, 24)
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
  face = grp.entities.add_face([8000.mm,0.mm,0.mm], [8050.mm,0.mm,0.mm], [8050.mm,50.mm,0.mm], [8000.mm,50.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(335.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type RWk cantilever arm (40x40 SHS)
  grp = ents.add_group
  grp.name = "Type RWk cantilever arm (40x40 SHS)"
  face = grp.entities.add_face([7675.mm,0.mm,70.mm], [8000.mm,0.mm,70.mm], [8000.mm,40.mm,70.mm], [7675.mm,40.mm,70.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(45.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type RWk upright clamp
  grp = ents.add_group
  grp.name = "Type RWk upright clamp"
  face = grp.entities.add_face([7996.mm,44.mm,45.mm], [8054.mm,44.mm,45.mm], [8054.mm,52.mm,45.mm], [7996.mm,52.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Type RWk upright bolt M12
  grp = ents.add_group
  grp.name = "Type RWk upright bolt M12"
  ge = grp.entities
  circle = ge.add_circle([8025.mm,-12.mm,76.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(64.mm)
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
  face = grp.entities.add_face([4329.mm,0.mm,95.mm], [4369.mm,0.mm,95.mm], [4369.mm,2362.mm,95.mm], [4329.mm,2362.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4329 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 lower"
  face = grp.entities.add_face([4329.mm,0.mm,80.mm], [4369.mm,0.mm,80.mm], [4369.mm,1046.mm,80.mm], [4329.mm,1046.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4329 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 lower"
  face = grp.entities.add_face([4329.mm,1086.mm,80.mm], [4369.mm,1086.mm,80.mm], [4369.mm,1266.mm,80.mm], [4329.mm,1266.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4329 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 lower"
  face = grp.entities.add_face([4329.mm,1306.mm,80.mm], [4369.mm,1306.mm,80.mm], [4369.mm,2362.mm,80.mm], [4329.mm,2362.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 upper"
  face = grp.entities.add_face([4589.mm,0.mm,95.mm], [4629.mm,0.mm,95.mm], [4629.mm,1093.mm,95.mm], [4589.mm,1093.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 upper"
  face = grp.entities.add_face([4589.mm,1149.mm,95.mm], [4629.mm,1149.mm,95.mm], [4629.mm,1177.mm,95.mm], [4589.mm,1177.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 upper"
  face = grp.entities.add_face([4589.mm,1211.mm,95.mm], [4629.mm,1211.mm,95.mm], [4629.mm,1224.mm,95.mm], [4589.mm,1224.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 upper"
  face = grp.entities.add_face([4589.mm,1258.mm,95.mm], [4629.mm,1258.mm,95.mm], [4629.mm,2362.mm,95.mm], [4589.mm,2362.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 lower"
  face = grp.entities.add_face([4589.mm,0.mm,80.mm], [4629.mm,0.mm,80.mm], [4629.mm,1046.mm,80.mm], [4589.mm,1046.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 lower"
  face = grp.entities.add_face([4589.mm,1086.mm,80.mm], [4629.mm,1086.mm,80.mm], [4629.mm,1093.mm,80.mm], [4589.mm,1093.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 lower"
  face = grp.entities.add_face([4589.mm,1149.mm,80.mm], [4629.mm,1149.mm,80.mm], [4629.mm,1177.mm,80.mm], [4589.mm,1177.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 lower"
  face = grp.entities.add_face([4589.mm,1211.mm,80.mm], [4629.mm,1211.mm,80.mm], [4629.mm,1224.mm,80.mm], [4589.mm,1224.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 lower"
  face = grp.entities.add_face([4589.mm,1258.mm,80.mm], [4629.mm,1258.mm,80.mm], [4629.mm,1266.mm,80.mm], [4589.mm,1266.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 lower"
  face = grp.entities.add_face([4589.mm,1306.mm,80.mm], [4629.mm,1306.mm,80.mm], [4629.mm,2362.mm,80.mm], [4589.mm,2362.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 notch web
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 notch web"
  face = grp.entities.add_face([4589.mm,1093.mm,80.mm], [4629.mm,1093.mm,80.mm], [4629.mm,1266.mm,80.mm], [4589.mm,1266.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 notch web
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 notch web"
  face = grp.entities.add_face([4589.mm,1115.mm,80.mm], [4629.mm,1115.mm,80.mm], [4629.mm,1266.mm,80.mm], [4589.mm,1266.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 notch web
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 notch web"
  face = grp.entities.add_face([4589.mm,1177.mm,80.mm], [4629.mm,1177.mm,80.mm], [4629.mm,1266.mm,80.mm], [4589.mm,1266.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 notch web
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 notch web"
  face = grp.entities.add_face([4589.mm,1224.mm,80.mm], [4629.mm,1224.mm,80.mm], [4629.mm,1266.mm,80.mm], [4589.mm,1266.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk end beam Yd0
  grp = ents.add_group
  grp.name = "RWk end beam Yd0"
  face = grp.entities.add_face([4329.mm,0.mm,80.mm], [4629.mm,0.mm,80.mm], [4629.mm,40.mm,80.mm], [4329.mm,40.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(35.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk end beam Yd2322
  grp = ents.add_group
  grp.name = "RWk end beam Yd2322"
  face = grp.entities.add_face([4329.mm,2322.mm,80.mm], [4629.mm,2322.mm,80.mm], [4629.mm,2362.mm,80.mm], [4329.mm,2362.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(35.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1046 lower
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 lower"
  face = grp.entities.add_face([4329.mm,1046.mm,70.mm], [4654.mm,1046.mm,70.mm], [4654.mm,1086.mm,70.mm], [4329.mm,1086.mm,70.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1046 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 upper"
  face = grp.entities.add_face([4369.mm,1046.mm,95.mm], [4589.mm,1046.mm,95.mm], [4589.mm,1086.mm,95.mm], [4369.mm,1086.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1046 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 upper"
  face = grp.entities.add_face([4629.mm,1046.mm,95.mm], [4654.mm,1046.mm,95.mm], [4654.mm,1086.mm,95.mm], [4629.mm,1086.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1046 Y1038
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1046 Y1038"
  face = grp.entities.add_face([4650.mm,1038.mm,45.mm], [4708.mm,1038.mm,45.mm], [4708.mm,1046.mm,45.mm], [4650.mm,1046.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1046 Y1086
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1046 Y1086"
  face = grp.entities.add_face([4650.mm,1086.mm,45.mm], [4708.mm,1086.mm,45.mm], [4708.mm,1094.mm,45.mm], [4650.mm,1094.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1046 Z76
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1046 Z76"
  ge = grp.entities
  circle = ge.add_circle([4679.mm,1034.mm,76.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(64.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1046 Z133
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1046 Z133"
  ge = grp.entities
  circle = ge.add_circle([4679.mm,1034.mm,133.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(64.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1266 lower
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 lower"
  face = grp.entities.add_face([4329.mm,1266.mm,70.mm], [4654.mm,1266.mm,70.mm], [4654.mm,1306.mm,70.mm], [4329.mm,1306.mm,70.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1266 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 upper"
  face = grp.entities.add_face([4369.mm,1266.mm,95.mm], [4589.mm,1266.mm,95.mm], [4589.mm,1306.mm,95.mm], [4369.mm,1306.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1266 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 upper"
  face = grp.entities.add_face([4629.mm,1266.mm,95.mm], [4654.mm,1266.mm,95.mm], [4654.mm,1306.mm,95.mm], [4629.mm,1306.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1266 Y1258
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1266 Y1258"
  face = grp.entities.add_face([4650.mm,1258.mm,45.mm], [4708.mm,1258.mm,45.mm], [4708.mm,1266.mm,45.mm], [4650.mm,1266.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1266 Y1306
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1266 Y1306"
  face = grp.entities.add_face([4650.mm,1306.mm,45.mm], [4708.mm,1306.mm,45.mm], [4708.mm,1314.mm,45.mm], [4650.mm,1314.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1266 Z76
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1266 Z76"
  ge = grp.entities
  circle = ge.add_circle([4679.mm,1254.mm,76.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(64.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1266 Z133
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1266 Z133"
  ge = grp.entities
  circle = ge.add_circle([4679.mm,1254.mm,133.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(64.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat plate (near)
  grp = ents.add_group
  grp.name = "RWk wall cleat plate (near)"
  face = grp.entities.add_face([4304.mm,0.mm,60.mm], [4394.mm,0.mm,60.mm], [4394.mm,8.mm,60.mm], [4304.mm,8.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(65.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat ext plate (near)
  grp = ents.add_group
  grp.name = "RWk wall cleat ext plate (near)"
  face = grp.entities.add_face([4304.mm,-48.mm,60.mm], [4394.mm,-48.mm,60.mm], [4394.mm,-40.mm,60.mm], [4304.mm,-40.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(65.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat shelf (near)
  grp = ents.add_group
  grp.name = "RWk wall cleat shelf (near)"
  face = grp.entities.add_face([4304.mm,0.mm,60.mm], [4394.mm,0.mm,60.mm], [4394.mm,55.mm,60.mm], [4304.mm,55.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
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
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
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
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner plate (near)
  grp = ents.add_group
  grp.name = "FP combined corner plate (near)"
  face = grp.entities.add_face([4574.mm,0.mm,58.mm], [4724.mm,0.mm,58.mm], [4724.mm,10.mm,58.mm], [4574.mm,10.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(167.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner ext plate (near)
  grp = ents.add_group
  grp.name = "FP combined corner ext plate (near)"
  face = grp.entities.add_face([4574.mm,-50.mm,58.mm], [4724.mm,-50.mm,58.mm], [4724.mm,-40.mm,58.mm], [4574.mm,-40.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(167.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined right-beam seat (near)
  grp = ents.add_group
  grp.name = "FP combined right-beam seat (near)"
  face = grp.entities.add_face([4574.mm,0.mm,58.mm], [4724.mm,0.mm,58.mm], [4724.mm,55.mm,58.mm], [4574.mm,55.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined BR rail seat (near)
  grp = ents.add_group
  grp.name = "FP combined BR rail seat (near)"
  face = grp.entities.add_face([4619.mm,0.mm,138.mm], [4679.mm,0.mm,138.mm], [4679.mm,55.mm,138.mm], [4619.mm,55.mm,138.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
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
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
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
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
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
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
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
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat plate (far)
  grp = ents.add_group
  grp.name = "RWk wall cleat plate (far)"
  face = grp.entities.add_face([4304.mm,2354.mm,60.mm], [4394.mm,2354.mm,60.mm], [4394.mm,2362.mm,60.mm], [4304.mm,2362.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(65.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat ext plate (far)
  grp = ents.add_group
  grp.name = "RWk wall cleat ext plate (far)"
  face = grp.entities.add_face([4304.mm,2402.mm,60.mm], [4394.mm,2402.mm,60.mm], [4394.mm,2410.mm,60.mm], [4304.mm,2410.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(65.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat shelf (far)
  grp = ents.add_group
  grp.name = "RWk wall cleat shelf (far)"
  face = grp.entities.add_face([4304.mm,2307.mm,60.mm], [4394.mm,2307.mm,60.mm], [4394.mm,2362.mm,60.mm], [4304.mm,2362.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
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
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
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
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner plate (far)
  grp = ents.add_group
  grp.name = "FP combined corner plate (far)"
  face = grp.entities.add_face([4574.mm,2352.mm,58.mm], [4724.mm,2352.mm,58.mm], [4724.mm,2362.mm,58.mm], [4574.mm,2362.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(167.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner ext plate (far)
  grp = ents.add_group
  grp.name = "FP combined corner ext plate (far)"
  face = grp.entities.add_face([4574.mm,2402.mm,58.mm], [4724.mm,2402.mm,58.mm], [4724.mm,2412.mm,58.mm], [4574.mm,2412.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(167.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined right-beam seat (far)
  grp = ents.add_group
  grp.name = "FP combined right-beam seat (far)"
  face = grp.entities.add_face([4574.mm,2307.mm,58.mm], [4724.mm,2307.mm,58.mm], [4724.mm,2362.mm,58.mm], [4574.mm,2362.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined BR rail seat (far)
  grp = ents.add_group
  grp.name = "FP combined BR rail seat (far)"
  face = grp.entities.add_face([4619.mm,2307.mm,138.mm], [4679.mm,2307.mm,138.mm], [4679.mm,2362.mm,138.mm], [4619.mm,2362.mm,138.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
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
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
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
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
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
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
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
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Right Walkway (cantilever rectangle)"
  inst.layer = model.layers["Right Cantilever"]

  # ═══ Film-Plane Right Support Beams ═══
  defn = model.definitions.add("Film-Plane Right Support Beams")
  ents = defn.entities
  # FP support beam R-bot
  grp = ents.add_group
  grp.name = "FP support beam R-bot"
  face = grp.entities.add_face([4609.mm,0.mm,150.mm], [4649.mm,0.mm,150.mm], [4649.mm,2362.mm,150.mm], [4609.mm,2362.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP support beam R-top
  grp = ents.add_group
  grp.name = "FP support beam R-top"
  face = grp.entities.add_face([4609.mm,0.mm,2248.mm], [4649.mm,0.mm,2248.mm], [4649.mm,2362.mm,2248.mm], [4609.mm,2362.mm,2248.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Film-Plane Right Support Beams"
  inst.layer = model.layers["Film Plane"]

  # ═══ IBC Corridor Frame (deep box) ═══
  defn = model.definitions.add("IBC Corridor Frame (deep box)")
  ents = defn.entities
  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([4654.mm,1046.mm,0.mm], [4704.mm,1046.mm,0.mm], [4704.mm,1096.mm,0.mm], [4654.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([4654.mm,1266.mm,0.mm], [4704.mm,1266.mm,0.mm], [4704.mm,1316.mm,0.mm], [4654.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([5104.mm,1046.mm,0.mm], [5154.mm,1046.mm,0.mm], [5154.mm,1096.mm,0.mm], [5104.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([5104.mm,1266.mm,0.mm], [5154.mm,1266.mm,0.mm], [5154.mm,1316.mm,0.mm], [5104.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([4654.mm,1096.mm,0.mm], [4704.mm,1096.mm,0.mm], [4704.mm,1266.mm,0.mm], [4654.mm,1266.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([5104.mm,1096.mm,0.mm], [5154.mm,1096.mm,0.mm], [5154.mm,1266.mm,0.mm], [5104.mm,1266.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.mm,1046.mm,0.mm], [5104.mm,1046.mm,0.mm], [5104.mm,1096.mm,0.mm], [4704.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.mm,1266.mm,0.mm], [5104.mm,1266.mm,0.mm], [5104.mm,1316.mm,0.mm], [4704.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([4654.mm,1096.mm,2246.mm], [4704.mm,1096.mm,2246.mm], [4704.mm,1266.mm,2246.mm], [4654.mm,1266.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([5104.mm,1096.mm,2246.mm], [5154.mm,1096.mm,2246.mm], [5154.mm,1266.mm,2246.mm], [5104.mm,1266.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.mm,1046.mm,2246.mm], [5104.mm,1046.mm,2246.mm], [5104.mm,1096.mm,2246.mm], [4704.mm,1096.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.mm,1266.mm,2246.mm], [5104.mm,1266.mm,2246.mm], [5104.mm,1316.mm,2246.mm], [4704.mm,1316.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot plate
  grp = ents.add_group
  grp.name = "Foot plate"
  face = grp.entities.add_face([4604.mm,996.mm,0.mm], [4754.mm,996.mm,0.mm], [4754.mm,1146.mm,0.mm], [4604.mm,1146.mm,0.mm])
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
  circle = ge.add_circle([4629.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4629.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4729.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4729.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot plate
  grp = ents.add_group
  grp.name = "Foot plate"
  face = grp.entities.add_face([4604.mm,1216.mm,0.mm], [4754.mm,1216.mm,0.mm], [4754.mm,1366.mm,0.mm], [4604.mm,1366.mm,0.mm])
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
  circle = ge.add_circle([4629.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4629.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4729.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4729.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot plate
  grp = ents.add_group
  grp.name = "Foot plate"
  face = grp.entities.add_face([5054.mm,996.mm,0.mm], [5204.mm,996.mm,0.mm], [5204.mm,1146.mm,0.mm], [5054.mm,1146.mm,0.mm])
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
  circle = ge.add_circle([5079.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5079.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5179.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5179.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot plate
  grp = ents.add_group
  grp.name = "Foot plate"
  face = grp.entities.add_face([5054.mm,1216.mm,0.mm], [5204.mm,1216.mm,0.mm], [5204.mm,1366.mm,0.mm], [5054.mm,1366.mm,0.mm])
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
  circle = ge.add_circle([5079.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5079.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5179.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5179.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1096.mm,90.mm], [5152.mm,1096.mm,90.mm], [5152.mm,1136.mm,90.mm], [5122.mm,1136.mm,90.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1096.mm,1118.mm], [5152.mm,1096.mm,1118.mm], [5152.mm,1136.mm,1118.mm], [5122.mm,1136.mm,1118.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1096.mm,2146.mm], [5152.mm,1096.mm,2146.mm], [5152.mm,1136.mm,2146.mm], [5122.mm,1136.mm,2146.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1226.mm,90.mm], [5152.mm,1226.mm,90.mm], [5152.mm,1266.mm,90.mm], [5122.mm,1266.mm,90.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1226.mm,1118.mm], [5152.mm,1226.mm,1118.mm], [5152.mm,1266.mm,1118.mm], [5122.mm,1266.mm,1118.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1226.mm,2146.mm], [5152.mm,1226.mm,2146.mm], [5152.mm,1266.mm,2146.mm], [5122.mm,1266.mm,2146.mm])
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

  # Left cantilever 1 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 1 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,220.mm,0.mm], [165.mm,220.mm,0.mm], [165.mm,280.mm,0.mm], [115.mm,280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 1 arm (to X470)
  grp = ents.add_group
  grp.name = "Left cantilever 1 arm (to X470)"
  face = grp.entities.add_face([165.mm,230.mm,75.mm], [470.mm,230.mm,75.mm], [470.mm,270.mm,75.mm], [165.mm,270.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
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

  # Left cantilever 2 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 2 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,770.mm,0.mm], [165.mm,770.mm,0.mm], [165.mm,830.mm,0.mm], [115.mm,830.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 2 arm (to X770)
  grp = ents.add_group
  grp.name = "Left cantilever 2 arm (to X770)"
  face = grp.entities.add_face([165.mm,770.mm,75.mm], [770.mm,770.mm,75.mm], [770.mm,830.mm,75.mm], [165.mm,830.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
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

  # Left cantilever 3 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 3 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,1150.mm,0.mm], [165.mm,1150.mm,0.mm], [165.mm,1210.mm,0.mm], [115.mm,1210.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 3 arm (to X770)
  grp = ents.add_group
  grp.name = "Left cantilever 3 arm (to X770)"
  face = grp.entities.add_face([165.mm,1150.mm,75.mm], [770.mm,1150.mm,75.mm], [770.mm,1210.mm,75.mm], [165.mm,1210.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
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

  # Left cantilever 4 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 4 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,1530.mm,0.mm], [165.mm,1530.mm,0.mm], [165.mm,1590.mm,0.mm], [115.mm,1590.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 4 arm (to X770)
  grp = ents.add_group
  grp.name = "Left cantilever 4 arm (to X770)"
  face = grp.entities.add_face([165.mm,1530.mm,75.mm], [770.mm,1530.mm,75.mm], [770.mm,1590.mm,75.mm], [165.mm,1590.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
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

  # Left cantilever 5 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 5 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,2080.mm,0.mm], [165.mm,2080.mm,0.mm], [165.mm,2140.mm,0.mm], [115.mm,2140.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 5 arm (to X470)
  grp = ents.add_group
  grp.name = "Left cantilever 5 arm (to X470)"
  face = grp.entities.add_face([165.mm,2090.mm,75.mm], [470.mm,2090.mm,75.mm], [470.mm,2130.mm,75.mm], [165.mm,2130.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
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
anc = Geom::Point3d.new(7000.mm, 0.mm, 150.mm)
txt = entities.add_text("RIGHT WALKWAY — COMBINED CORNER PLATE (right corners)
10mm, carries the walkway right beam (Z70 seat)
+ the BR film rail (Z150 seat); 4x M12", anc, Geom::Vector3d.new(0.mm, -300.mm, 850.mm))
txt.layer = model.layers["Cantilever Types"] rescue nil
anc = Geom::Point3d.new(8000.mm, 0.mm, 115.mm)
txt = entities.add_text("RIGHT WALKWAY — CENTER CANTILEVER ARM
40x40 SHS off an IBC corridor upright
(half-lapped at the long beams); M12 clamp", anc, Geom::Vector3d.new(150.mm, -300.mm, 820.mm))
txt.layer = model.layers["Cantilever Types"] rescue nil

model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags from earlier generator versions ──
keep_tags = ["Container", "Processing Tray", "Walkways", "Cantilevers", "Cantilever Types", "Right Cantilever", "Film Plane", "IBC Frame", "Left Support", "Labels"]
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
[["Walkway", ["Walkways", "Right Cantilever", "Film Plane", "IBC Frame", "Processing Tray"]], ["Near/Far Cantilevers", ["Cantilevers", "Processing Tray"]], ["Right Cantilever", ["Right Cantilever", "Film Plane", "IBC Frame", "Processing Tray"]], ["Left Support", ["Left Support", "Processing Tray"]]].each { |name, tags|
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
