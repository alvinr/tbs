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

# ── Tags (layers) ──
  model.layers.add("Container") unless model.layers["Container"]
  model.layers.add("Processing Tray") unless model.layers["Processing Tray"]
  model.layers.add("Walkways") unless model.layers["Walkways"]
  model.layers.add("Walkway Right") unless model.layers["Walkway Right"]
  model.layers.add("Cantilevers") unless model.layers["Cantilevers"]
  model.layers.add("Cantilever Types") unless model.layers["Cantilever Types"]
  model.layers.add("Right Hangers") unless model.layers["Right Hangers"]
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

  # ═══ Walkway Decks (near/far/left) ═══
  defn = model.definitions.add("Walkway Decks (near/far/left)")
  ents = defn.entities
  # Walkway Near (door-end, removable)
  grp = ents.add_group
  grp.name = "Walkway Near (door-end, removable)"
  face = grp.entities.add_face([470.mm,0.mm,115.mm], [900.mm,0.mm,115.mm], [900.mm,300.mm,115.mm], [470.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (door-end, removable)"] || model.materials.add("Walkway Near (door-end, removable)")
  mat.color = Sketchup::Color.new(192, 96, 0)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near (left)
  grp = ents.add_group
  grp.name = "Walkway Near (left)"
  face = grp.entities.add_face([900.mm,0.mm,115.mm], [1155.mm,0.mm,115.mm], [1155.mm,300.mm,115.mm], [900.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left)"] || model.materials.add("Walkway Near (left)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near (widened)
  grp = ents.add_group
  grp.name = "Walkway Near (widened)"
  face = grp.entities.add_face([1155.mm,0.mm,115.mm], [2629.mm,0.mm,115.mm], [2629.mm,500.mm,115.mm], [1155.mm,500.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left)"] || model.materials.add("Walkway Near (left)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near (right)
  grp = ents.add_group
  grp.name = "Walkway Near (right)"
  face = grp.entities.add_face([2629.mm,0.mm,115.mm], [4329.mm,0.mm,115.mm], [4329.mm,300.mm,115.mm], [2629.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left)"] || model.materials.add("Walkway Near (left)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far
  grp = ents.add_group
  grp.name = "Walkway Far"
  face = grp.entities.add_face([470.mm,2062.mm,115.mm], [4329.mm,2062.mm,115.mm], [4329.mm,2362.mm,115.mm], [470.mm,2362.mm,115.mm])
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

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Walkway Decks (near/far/left)"
  inst.layer = model.layers["Walkways"]

  # ═══ Walkway Right (IBC end) ═══
  defn = model.definitions.add("Walkway Right (IBC end)")
  ents = defn.entities
  # Walkway Right (IBC end)
  grp = ents.add_group
  grp.name = "Walkway Right (IBC end)"
  face = grp.entities.add_face([4329.mm,0.mm,115.mm], [4629.mm,0.mm,115.mm], [4629.mm,2362.mm,115.mm], [4329.mm,2362.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left)"] || model.materials.add("Walkway Near (left)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Walkway Right (IBC end)"
  inst.layer = model.layers["Walkway Right"]

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

  # Cantilever Near 2 (widened) plate
  grp = ents.add_group
  grp.name = "Cantilever Near 2 (widened) plate"
  face = grp.entities.add_face([1095.mm,0.mm,0.mm], [1215.mm,0.mm,0.mm], [1215.mm,10.mm,0.mm], [1095.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 (widened) arm
  grp = ents.add_group
  grp.name = "Cantilever Near 2 (widened) arm"
  face = grp.entities.add_face([1150.mm,10.mm,103.mm], [1160.mm,10.mm,103.mm], [1160.mm,500.mm,103.mm], [1150.mm,500.mm,103.mm])
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
  f = ge.add_face([1150.mm,10.mm,0.mm], [1150.mm,10.mm,103.mm], [1150.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 (widened) ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Near 2 (widened) ext reinf plate"
  face = grp.entities.add_face([1095.mm,-46.mm,0.mm], [1215.mm,-46.mm,0.mm], [1215.mm,-40.mm,0.mm], [1095.mm,-40.mm,0.mm])
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
  circle = ge.add_circle([1123.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 2 (widened) bolt head"
  face = grp.entities.add_face([1114.mm,-52.mm,26.mm], [1132.mm,-52.mm,26.mm], [1132.mm,-46.mm,26.mm], [1114.mm,-46.mm,26.mm])
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
  circle = ge.add_circle([1187.mm,-46.mm,35.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 2 (widened) bolt head"
  face = grp.entities.add_face([1178.mm,-52.mm,26.mm], [1196.mm,-52.mm,26.mm], [1196.mm,-46.mm,26.mm], [1178.mm,-46.mm,26.mm])
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
  circle = ge.add_circle([1123.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 2 (widened) bolt head"
  face = grp.entities.add_face([1114.mm,-52.mm,151.mm], [1132.mm,-52.mm,151.mm], [1132.mm,-46.mm,151.mm], [1114.mm,-46.mm,151.mm])
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
  circle = ge.add_circle([1187.mm,-46.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 2 (widened) bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 2 (widened) bolt head"
  face = grp.entities.add_face([1178.mm,-52.mm,151.mm], [1196.mm,-52.mm,151.mm], [1196.mm,-46.mm,151.mm], [1178.mm,-46.mm,151.mm])
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

  # Cantilever Near 6 plate
  grp = ents.add_group
  grp.name = "Cantilever Near 6 plate"
  face = grp.entities.add_face([2923.mm,0.mm,0.mm], [3043.mm,0.mm,0.mm], [3043.mm,8.mm,0.mm], [2923.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 arm
  grp = ents.add_group
  grp.name = "Cantilever Near 6 arm"
  face = grp.entities.add_face([2979.mm,8.mm,105.mm], [2987.mm,8.mm,105.mm], [2987.mm,300.mm,105.mm], [2979.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 gusset
  grp = ents.add_group
  grp.name = "Cantilever Near 6 gusset"
  ge = grp.entities
  f = ge.add_face([2979.mm,8.mm,0.mm], [2979.mm,8.mm,105.mm], [2979.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 ext reinf plate
  grp = ents.add_group
  grp.name = "Cantilever Near 6 ext reinf plate"
  face = grp.entities.add_face([2933.mm,-46.mm,0.mm], [3033.mm,-46.mm,0.mm], [3033.mm,-40.mm,0.mm], [2933.mm,-40.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(180.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2983.mm,-46.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 6 bolt head"
  face = grp.entities.add_face([2974.mm,-52.mm,111.mm], [2992.mm,-52.mm,111.mm], [2992.mm,-46.mm,111.mm], [2974.mm,-46.mm,111.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2951.mm,-46.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 6 bolt head"
  face = grp.entities.add_face([2942.mm,-52.mm,33.mm], [2960.mm,-52.mm,33.mm], [2960.mm,-46.mm,33.mm], [2942.mm,-46.mm,33.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 bolt M12
  grp = ents.add_group
  grp.name = "Cantilever Near 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3015.mm,-46.mm,42.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever Near 6 bolt head
  grp = ents.add_group
  grp.name = "Cantilever Near 6 bolt head"
  face = grp.entities.add_face([3006.mm,-52.mm,33.mm], [3024.mm,-52.mm,33.mm], [3024.mm,-46.mm,33.mm], [3006.mm,-46.mm,33.mm])
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

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Cantilever Types"
  inst.layer = model.layers["Cantilever Types"]

  # ═══ Right Walkway Hangers ═══
  defn = model.definitions.add("Right Walkway Hangers")
  ents = defn.entities
  # Right bearer (25x25x5 L) X4329
  grp = ents.add_group
  grp.name = "Right bearer (25x25x5 L) X4329"
  face = grp.entities.add_face([4316.5.mm,0.mm,90.mm], [4341.5.mm,0.mm,90.mm], [4341.5.mm,2362.mm,90.mm], [4316.5.mm,2362.mm,90.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right hanger rod M10 X4329 Y320
  grp = ents.add_group
  grp.name = "Right hanger rod M10 X4329 Y320"
  ge = grp.entities
  circle = ge.add_circle([4329.mm,320.mm,115.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2273.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate (inside) X4329 Y320
  grp = ents.add_group
  grp.name = "Right ceiling plate (inside) X4329 Y320"
  face = grp.entities.add_face([4269.mm,275.mm,2382.mm], [4389.mm,275.mm,2382.mm], [4389.mm,365.mm,2382.mm], [4269.mm,365.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate (outside) X4329 Y320
  grp = ents.add_group
  grp.name = "Right ceiling plate (outside) X4329 Y320"
  face = grp.entities.add_face([4269.mm,275.mm,2428.mm], [4389.mm,275.mm,2428.mm], [4389.mm,365.mm,2428.mm], [4269.mm,365.mm,2428.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4329 Y320
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4329 Y320"
  ge = grp.entities
  circle = ge.add_circle([4287.mm,292.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4329 Y320
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4329 Y320"
  ge = grp.entities
  circle = ge.add_circle([4287.mm,348.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4329 Y320
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4329 Y320"
  ge = grp.entities
  circle = ge.add_circle([4371.mm,292.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4329 Y320
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4329 Y320"
  ge = grp.entities
  circle = ge.add_circle([4371.mm,348.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right hanger rod M10 X4329 Y457
  grp = ents.add_group
  grp.name = "Right hanger rod M10 X4329 Y457"
  ge = grp.entities
  circle = ge.add_circle([4329.mm,457.mm,115.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2273.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate (inside) X4329 Y457
  grp = ents.add_group
  grp.name = "Right ceiling plate (inside) X4329 Y457"
  face = grp.entities.add_face([4269.mm,412.mm,2382.mm], [4389.mm,412.mm,2382.mm], [4389.mm,502.mm,2382.mm], [4269.mm,502.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate (outside) X4329 Y457
  grp = ents.add_group
  grp.name = "Right ceiling plate (outside) X4329 Y457"
  face = grp.entities.add_face([4269.mm,412.mm,2428.mm], [4389.mm,412.mm,2428.mm], [4389.mm,502.mm,2428.mm], [4269.mm,502.mm,2428.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4329 Y457
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4329 Y457"
  ge = grp.entities
  circle = ge.add_circle([4287.mm,429.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4329 Y457
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4329 Y457"
  ge = grp.entities
  circle = ge.add_circle([4287.mm,485.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4329 Y457
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4329 Y457"
  ge = grp.entities
  circle = ge.add_circle([4371.mm,429.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4329 Y457
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4329 Y457"
  ge = grp.entities
  circle = ge.add_circle([4371.mm,485.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right hanger rod M10 X4329 Y914
  grp = ents.add_group
  grp.name = "Right hanger rod M10 X4329 Y914"
  ge = grp.entities
  circle = ge.add_circle([4329.mm,914.mm,115.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2273.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate (inside) X4329 Y914
  grp = ents.add_group
  grp.name = "Right ceiling plate (inside) X4329 Y914"
  face = grp.entities.add_face([4269.mm,869.mm,2382.mm], [4389.mm,869.mm,2382.mm], [4389.mm,959.mm,2382.mm], [4269.mm,959.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate (outside) X4329 Y914
  grp = ents.add_group
  grp.name = "Right ceiling plate (outside) X4329 Y914"
  face = grp.entities.add_face([4269.mm,869.mm,2428.mm], [4389.mm,869.mm,2428.mm], [4389.mm,959.mm,2428.mm], [4269.mm,959.mm,2428.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4329 Y914
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4329 Y914"
  ge = grp.entities
  circle = ge.add_circle([4287.mm,886.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4329 Y914
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4329 Y914"
  ge = grp.entities
  circle = ge.add_circle([4287.mm,942.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4329 Y914
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4329 Y914"
  ge = grp.entities
  circle = ge.add_circle([4371.mm,886.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4329 Y914
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4329 Y914"
  ge = grp.entities
  circle = ge.add_circle([4371.mm,942.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right hanger rod M10 X4329 Y1371
  grp = ents.add_group
  grp.name = "Right hanger rod M10 X4329 Y1371"
  ge = grp.entities
  circle = ge.add_circle([4329.mm,1371.mm,115.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2273.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate (inside) X4329 Y1371
  grp = ents.add_group
  grp.name = "Right ceiling plate (inside) X4329 Y1371"
  face = grp.entities.add_face([4269.mm,1326.mm,2382.mm], [4389.mm,1326.mm,2382.mm], [4389.mm,1416.mm,2382.mm], [4269.mm,1416.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate (outside) X4329 Y1371
  grp = ents.add_group
  grp.name = "Right ceiling plate (outside) X4329 Y1371"
  face = grp.entities.add_face([4269.mm,1326.mm,2428.mm], [4389.mm,1326.mm,2428.mm], [4389.mm,1416.mm,2428.mm], [4269.mm,1416.mm,2428.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4329 Y1371
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4329 Y1371"
  ge = grp.entities
  circle = ge.add_circle([4287.mm,1343.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4329 Y1371
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4329 Y1371"
  ge = grp.entities
  circle = ge.add_circle([4287.mm,1399.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4329 Y1371
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4329 Y1371"
  ge = grp.entities
  circle = ge.add_circle([4371.mm,1343.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4329 Y1371
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4329 Y1371"
  ge = grp.entities
  circle = ge.add_circle([4371.mm,1399.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right hanger rod M10 X4329 Y1828
  grp = ents.add_group
  grp.name = "Right hanger rod M10 X4329 Y1828"
  ge = grp.entities
  circle = ge.add_circle([4329.mm,1828.mm,115.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2273.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate (inside) X4329 Y1828
  grp = ents.add_group
  grp.name = "Right ceiling plate (inside) X4329 Y1828"
  face = grp.entities.add_face([4269.mm,1783.mm,2382.mm], [4389.mm,1783.mm,2382.mm], [4389.mm,1873.mm,2382.mm], [4269.mm,1873.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate (outside) X4329 Y1828
  grp = ents.add_group
  grp.name = "Right ceiling plate (outside) X4329 Y1828"
  face = grp.entities.add_face([4269.mm,1783.mm,2428.mm], [4389.mm,1783.mm,2428.mm], [4389.mm,1873.mm,2428.mm], [4269.mm,1873.mm,2428.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4329 Y1828
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4329 Y1828"
  ge = grp.entities
  circle = ge.add_circle([4287.mm,1800.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4329 Y1828
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4329 Y1828"
  ge = grp.entities
  circle = ge.add_circle([4287.mm,1856.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4329 Y1828
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4329 Y1828"
  ge = grp.entities
  circle = ge.add_circle([4371.mm,1800.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4329 Y1828
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4329 Y1828"
  ge = grp.entities
  circle = ge.add_circle([4371.mm,1856.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right bearer (25x25x5 L) X4629
  grp = ents.add_group
  grp.name = "Right bearer (25x25x5 L) X4629"
  face = grp.entities.add_face([4616.5.mm,0.mm,90.mm], [4641.5.mm,0.mm,90.mm], [4641.5.mm,2362.mm,90.mm], [4616.5.mm,2362.mm,90.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right hanger rod M10 X4629 Y320
  grp = ents.add_group
  grp.name = "Right hanger rod M10 X4629 Y320"
  ge = grp.entities
  circle = ge.add_circle([4629.mm,320.mm,115.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2273.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate (inside) X4629 Y320
  grp = ents.add_group
  grp.name = "Right ceiling plate (inside) X4629 Y320"
  face = grp.entities.add_face([4569.mm,275.mm,2382.mm], [4689.mm,275.mm,2382.mm], [4689.mm,365.mm,2382.mm], [4569.mm,365.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate (outside) X4629 Y320
  grp = ents.add_group
  grp.name = "Right ceiling plate (outside) X4629 Y320"
  face = grp.entities.add_face([4569.mm,275.mm,2428.mm], [4689.mm,275.mm,2428.mm], [4689.mm,365.mm,2428.mm], [4569.mm,365.mm,2428.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4629 Y320
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4629 Y320"
  ge = grp.entities
  circle = ge.add_circle([4587.mm,292.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4629 Y320
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4629 Y320"
  ge = grp.entities
  circle = ge.add_circle([4587.mm,348.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4629 Y320
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4629 Y320"
  ge = grp.entities
  circle = ge.add_circle([4671.mm,292.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4629 Y320
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4629 Y320"
  ge = grp.entities
  circle = ge.add_circle([4671.mm,348.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right hanger rod M10 X4629 Y457
  grp = ents.add_group
  grp.name = "Right hanger rod M10 X4629 Y457"
  ge = grp.entities
  circle = ge.add_circle([4629.mm,457.mm,115.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2273.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate (inside) X4629 Y457
  grp = ents.add_group
  grp.name = "Right ceiling plate (inside) X4629 Y457"
  face = grp.entities.add_face([4569.mm,412.mm,2382.mm], [4689.mm,412.mm,2382.mm], [4689.mm,502.mm,2382.mm], [4569.mm,502.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate (outside) X4629 Y457
  grp = ents.add_group
  grp.name = "Right ceiling plate (outside) X4629 Y457"
  face = grp.entities.add_face([4569.mm,412.mm,2428.mm], [4689.mm,412.mm,2428.mm], [4689.mm,502.mm,2428.mm], [4569.mm,502.mm,2428.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4629 Y457
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4629 Y457"
  ge = grp.entities
  circle = ge.add_circle([4587.mm,429.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4629 Y457
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4629 Y457"
  ge = grp.entities
  circle = ge.add_circle([4587.mm,485.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4629 Y457
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4629 Y457"
  ge = grp.entities
  circle = ge.add_circle([4671.mm,429.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4629 Y457
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4629 Y457"
  ge = grp.entities
  circle = ge.add_circle([4671.mm,485.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right hanger rod M10 X4629 Y914
  grp = ents.add_group
  grp.name = "Right hanger rod M10 X4629 Y914"
  ge = grp.entities
  circle = ge.add_circle([4629.mm,914.mm,115.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2273.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate (inside) X4629 Y914
  grp = ents.add_group
  grp.name = "Right ceiling plate (inside) X4629 Y914"
  face = grp.entities.add_face([4569.mm,869.mm,2382.mm], [4689.mm,869.mm,2382.mm], [4689.mm,959.mm,2382.mm], [4569.mm,959.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate (outside) X4629 Y914
  grp = ents.add_group
  grp.name = "Right ceiling plate (outside) X4629 Y914"
  face = grp.entities.add_face([4569.mm,869.mm,2428.mm], [4689.mm,869.mm,2428.mm], [4689.mm,959.mm,2428.mm], [4569.mm,959.mm,2428.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4629 Y914
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4629 Y914"
  ge = grp.entities
  circle = ge.add_circle([4587.mm,886.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4629 Y914
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4629 Y914"
  ge = grp.entities
  circle = ge.add_circle([4587.mm,942.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4629 Y914
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4629 Y914"
  ge = grp.entities
  circle = ge.add_circle([4671.mm,886.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4629 Y914
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4629 Y914"
  ge = grp.entities
  circle = ge.add_circle([4671.mm,942.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right hanger rod M10 X4629 Y1371
  grp = ents.add_group
  grp.name = "Right hanger rod M10 X4629 Y1371"
  ge = grp.entities
  circle = ge.add_circle([4629.mm,1371.mm,115.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2273.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate (inside) X4629 Y1371
  grp = ents.add_group
  grp.name = "Right ceiling plate (inside) X4629 Y1371"
  face = grp.entities.add_face([4569.mm,1326.mm,2382.mm], [4689.mm,1326.mm,2382.mm], [4689.mm,1416.mm,2382.mm], [4569.mm,1416.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate (outside) X4629 Y1371
  grp = ents.add_group
  grp.name = "Right ceiling plate (outside) X4629 Y1371"
  face = grp.entities.add_face([4569.mm,1326.mm,2428.mm], [4689.mm,1326.mm,2428.mm], [4689.mm,1416.mm,2428.mm], [4569.mm,1416.mm,2428.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4629 Y1371
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4629 Y1371"
  ge = grp.entities
  circle = ge.add_circle([4587.mm,1343.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4629 Y1371
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4629 Y1371"
  ge = grp.entities
  circle = ge.add_circle([4587.mm,1399.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4629 Y1371
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4629 Y1371"
  ge = grp.entities
  circle = ge.add_circle([4671.mm,1343.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4629 Y1371
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4629 Y1371"
  ge = grp.entities
  circle = ge.add_circle([4671.mm,1399.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right hanger rod M10 X4629 Y1828
  grp = ents.add_group
  grp.name = "Right hanger rod M10 X4629 Y1828"
  ge = grp.entities
  circle = ge.add_circle([4629.mm,1828.mm,115.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2273.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate (inside) X4629 Y1828
  grp = ents.add_group
  grp.name = "Right ceiling plate (inside) X4629 Y1828"
  face = grp.entities.add_face([4569.mm,1783.mm,2382.mm], [4689.mm,1783.mm,2382.mm], [4689.mm,1873.mm,2382.mm], [4569.mm,1873.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate (outside) X4629 Y1828
  grp = ents.add_group
  grp.name = "Right ceiling plate (outside) X4629 Y1828"
  face = grp.entities.add_face([4569.mm,1783.mm,2428.mm], [4689.mm,1783.mm,2428.mm], [4689.mm,1873.mm,2428.mm], [4569.mm,1873.mm,2428.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4629 Y1828
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4629 Y1828"
  ge = grp.entities
  circle = ge.add_circle([4587.mm,1800.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4629 Y1828
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4629 Y1828"
  ge = grp.entities
  circle = ge.add_circle([4587.mm,1856.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4629 Y1828
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4629 Y1828"
  ge = grp.entities
  circle = ge.add_circle([4671.mm,1800.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling bolt M12 X4629 Y1828
  grp = ents.add_group
  grp.name = "Right ceiling bolt M12 X4629 Y1828"
  ge = grp.entities
  circle = ge.add_circle([4671.mm,1856.mm,2378.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Right Walkway Hangers"
  inst.layer = model.layers["Right Hangers"]

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
anc = Geom::Point3d.new(4479.mm, 400.mm, 2100.mm)
txt = entities.add_text("RIGHT HANGERS
(ceiling-hung)", anc, Geom::Vector3d.new(800.mm, -200.mm, 350.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(140.mm, 1181.mm, 100.mm)
txt = entities.add_text("LEFT SUPPORT
(floor-leg cantilevers)", anc, Geom::Vector3d.new(-850.mm, -200.mm, 600.mm))
txt.layer = model.layers["Labels"] rescue nil

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

model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags from earlier generator versions ──
keep_tags = ["Container", "Processing Tray", "Walkways", "Walkway Right", "Cantilevers", "Cantilever Types", "Right Hangers", "Left Support", "Labels"]
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

# Combined — all subsystems, Labels + type-catalog OFF.
model.pages.add("Combined")
# Labeled — same view + callouts on the major parts.
model.layers.each { |l| l.visible = true }
model.layers["Cantilever Types"].visible = false if model.layers["Cantilever Types"]
model.pages.add("Labeled")
model.layers["Labels"].visible = false if model.layers["Labels"]
[["Walkway", ["Walkways", "Walkway Right", "Processing Tray"]], ["Near/Far Cantilevers", ["Cantilevers", "Processing Tray"]], ["Right Hangers", ["Right Hangers", "Walkway Right", "Processing Tray"]], ["Left Support", ["Left Support", "Processing Tray"]]].each { |name, tags|
  model.layers.each { |l| l.visible = (l == default_layer || l.name == "Container" || tags.include?(l.name)) }
  page = model.pages.add(name)
  page.use_camera = true
}

# ── "Cantilevers" — one of each UNIQUE bracket type, isolated side-by-side with a
#    close-up camera (the only scene showing the Cantilever Types catalog tag; the
#    wall is hidden so the full bracket — plate, arm, gusset, bolts — reads) ──
model.layers.each { |l| l.visible = (l.name == "Cantilever Types") }
ct_tgt = Geom::Point3d.new(3500.mm, -100.mm, 450.mm)
ct_dir = Geom::Vector3d.new(-0.22, -0.82, 0.40); ct_dir.normalize!
ct_eye = ct_tgt.offset(ct_dir, 5000.mm)
ct_cam = Sketchup::Camera.new(ct_eye, ct_tgt, Z_AXIS)
ct_cam.perspective = true
ct_cam.fov = 40
model.active_view.camera = ct_cam
ctp = model.pages.add("Cantilevers")
ctp.use_camera = true

model.layers.each { |l| l.visible = true }
model.layers["Cantilever Types"].visible = false if model.layers["Cantilever Types"]

model.commit_operation
{ success: true, model: "Walkway + Cantilevers",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
