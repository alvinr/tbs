model = Sketchup.active_model
model.start_operation("TBS-001 Walkway + Cantilevers", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# Idempotent rebuild: erase ALL prior instances.
to_erase = entities.to_a.select { |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance)
}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each { |p| model.pages.erase(p) }

# ── Tags (layers) ──
  model.layers.add("Container") unless model.layers["Container"]
  model.layers.add("Processing Tray") unless model.layers["Processing Tray"]
  model.layers.add("Walkways") unless model.layers["Walkways"]
  model.layers.add("Cantilevers") unless model.layers["Cantilevers"]
  model.layers.add("Right Hangers") unless model.layers["Right Hangers"]
  model.layers.add("Left Support") unless model.layers["Left Support"]

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

  # ═══ Walkway Decks (gates) ═══
  defn = model.definitions.add("Walkway Decks (gates)")
  ents = defn.entities
  # Walkway Near (left)
  grp = ents.add_group
  grp.name = "Walkway Near (left)"
  face = grp.entities.add_face([470.mm,0.mm,65.mm], [1155.mm,0.mm,65.mm], [1155.mm,300.mm,65.mm], [470.mm,300.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left)"] || model.materials.add("Walkway Near (left)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near (widened)
  grp = ents.add_group
  grp.name = "Walkway Near (widened)"
  face = grp.entities.add_face([1155.mm,0.mm,65.mm], [2629.mm,0.mm,65.mm], [2629.mm,500.mm,65.mm], [1155.mm,500.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left)"] || model.materials.add("Walkway Near (left)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near (right)
  grp = ents.add_group
  grp.name = "Walkway Near (right)"
  face = grp.entities.add_face([2629.mm,0.mm,65.mm], [4329.mm,0.mm,65.mm], [4329.mm,300.mm,65.mm], [2629.mm,300.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left)"] || model.materials.add("Walkway Near (left)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far
  grp = ents.add_group
  grp.name = "Walkway Far"
  face = grp.entities.add_face([470.mm,2062.mm,65.mm], [4329.mm,2062.mm,65.mm], [4329.mm,2362.mm,65.mm], [470.mm,2362.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left)"] || model.materials.add("Walkway Near (left)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Right (IBC end)
  grp = ents.add_group
  grp.name = "Walkway Right (IBC end)"
  face = grp.entities.add_face([4329.mm,0.mm,65.mm], [4629.mm,0.mm,65.mm], [4629.mm,2362.mm,65.mm], [4329.mm,2362.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left)"] || model.materials.add("Walkway Near (left)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Left (removable)
  grp = ents.add_group
  grp.name = "Walkway Left (removable)"
  face = grp.entities.add_face([170.mm,0.mm,65.mm], [470.mm,0.mm,65.mm], [470.mm,2362.mm,65.mm], [170.mm,2362.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Left (removable)"] || model.materials.add("Walkway Left (removable)")
  mat.color = Sketchup::Color.new(192, 96, 0)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Left punch-out
  grp = ents.add_group
  grp.name = "Walkway Left punch-out"
  face = grp.entities.add_face([470.mm,800.mm,65.mm], [770.mm,800.mm,65.mm], [770.mm,1560.mm,65.mm], [470.mm,1560.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Left (removable)"] || model.materials.add("Walkway Left (removable)")
  mat.color = Sketchup::Color.new(192, 96, 0)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Walkway Decks (gates)"
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
  face = grp.entities.add_face([694.mm,0.mm,55.mm], [702.mm,0.mm,55.mm], [702.mm,300.mm,55.mm], [694.mm,300.mm,55.mm])
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
  f = ge.add_face([694.mm,0.mm,0.mm], [694.mm,0.mm,55.mm], [694.mm,70.mm,55.mm])
  f.pushpull(8.mm)
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
  face = grp.entities.add_face([1150.mm,0.mm,53.mm], [1160.mm,0.mm,53.mm], [1160.mm,500.mm,53.mm], [1150.mm,500.mm,53.mm])
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
  f = ge.add_face([1150.mm,0.mm,0.mm], [1150.mm,0.mm,53.mm], [1150.mm,70.mm,53.mm])
  f.pushpull(10.mm)
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
  face = grp.entities.add_face([1607.mm,0.mm,53.mm], [1617.mm,0.mm,53.mm], [1617.mm,500.mm,53.mm], [1607.mm,500.mm,53.mm])
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
  f = ge.add_face([1607.mm,0.mm,0.mm], [1607.mm,0.mm,53.mm], [1607.mm,70.mm,53.mm])
  f.pushpull(10.mm)
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
  face = grp.entities.add_face([2064.mm,0.mm,53.mm], [2074.mm,0.mm,53.mm], [2074.mm,500.mm,53.mm], [2064.mm,500.mm,53.mm])
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
  f = ge.add_face([2064.mm,0.mm,0.mm], [2064.mm,0.mm,53.mm], [2064.mm,70.mm,53.mm])
  f.pushpull(10.mm)
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
  face = grp.entities.add_face([2521.mm,0.mm,53.mm], [2531.mm,0.mm,53.mm], [2531.mm,500.mm,53.mm], [2521.mm,500.mm,53.mm])
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
  f = ge.add_face([2521.mm,0.mm,0.mm], [2521.mm,0.mm,53.mm], [2521.mm,70.mm,53.mm])
  f.pushpull(10.mm)
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
  face = grp.entities.add_face([2979.mm,0.mm,55.mm], [2987.mm,0.mm,55.mm], [2987.mm,300.mm,55.mm], [2979.mm,300.mm,55.mm])
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
  f = ge.add_face([2979.mm,0.mm,0.mm], [2979.mm,0.mm,55.mm], [2979.mm,70.mm,55.mm])
  f.pushpull(8.mm)
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
  face = grp.entities.add_face([3436.mm,0.mm,55.mm], [3444.mm,0.mm,55.mm], [3444.mm,300.mm,55.mm], [3436.mm,300.mm,55.mm])
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
  f = ge.add_face([3436.mm,0.mm,0.mm], [3436.mm,0.mm,55.mm], [3436.mm,70.mm,55.mm])
  f.pushpull(8.mm)
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
  face = grp.entities.add_face([3893.mm,0.mm,55.mm], [3901.mm,0.mm,55.mm], [3901.mm,300.mm,55.mm], [3893.mm,300.mm,55.mm])
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
  f = ge.add_face([3893.mm,0.mm,0.mm], [3893.mm,0.mm,55.mm], [3893.mm,70.mm,55.mm])
  f.pushpull(8.mm)
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
  face = grp.entities.add_face([694.mm,2062.mm,55.mm], [702.mm,2062.mm,55.mm], [702.mm,2362.mm,55.mm], [694.mm,2362.mm,55.mm])
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
  f = ge.add_face([694.mm,2362.mm,0.mm], [694.mm,2362.mm,55.mm], [694.mm,2292.mm,55.mm])
  f.pushpull(8.mm)
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
  face = grp.entities.add_face([1151.mm,2062.mm,55.mm], [1159.mm,2062.mm,55.mm], [1159.mm,2362.mm,55.mm], [1151.mm,2362.mm,55.mm])
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
  f = ge.add_face([1151.mm,2362.mm,0.mm], [1151.mm,2362.mm,55.mm], [1151.mm,2292.mm,55.mm])
  f.pushpull(8.mm)
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
  face = grp.entities.add_face([1608.mm,2062.mm,55.mm], [1616.mm,2062.mm,55.mm], [1616.mm,2362.mm,55.mm], [1608.mm,2362.mm,55.mm])
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
  f = ge.add_face([1608.mm,2362.mm,0.mm], [1608.mm,2362.mm,55.mm], [1608.mm,2292.mm,55.mm])
  f.pushpull(8.mm)
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
  face = grp.entities.add_face([2065.mm,2062.mm,55.mm], [2073.mm,2062.mm,55.mm], [2073.mm,2362.mm,55.mm], [2065.mm,2362.mm,55.mm])
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
  f = ge.add_face([2065.mm,2362.mm,0.mm], [2065.mm,2362.mm,55.mm], [2065.mm,2292.mm,55.mm])
  f.pushpull(8.mm)
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
  face = grp.entities.add_face([2522.mm,2062.mm,55.mm], [2530.mm,2062.mm,55.mm], [2530.mm,2362.mm,55.mm], [2522.mm,2362.mm,55.mm])
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
  f = ge.add_face([2522.mm,2362.mm,0.mm], [2522.mm,2362.mm,55.mm], [2522.mm,2292.mm,55.mm])
  f.pushpull(8.mm)
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
  face = grp.entities.add_face([2979.mm,2062.mm,55.mm], [2987.mm,2062.mm,55.mm], [2987.mm,2362.mm,55.mm], [2979.mm,2362.mm,55.mm])
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
  f = ge.add_face([2979.mm,2362.mm,0.mm], [2979.mm,2362.mm,55.mm], [2979.mm,2292.mm,55.mm])
  f.pushpull(8.mm)
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
  face = grp.entities.add_face([3436.mm,2062.mm,55.mm], [3444.mm,2062.mm,55.mm], [3444.mm,2362.mm,55.mm], [3436.mm,2362.mm,55.mm])
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
  f = ge.add_face([3436.mm,2362.mm,0.mm], [3436.mm,2362.mm,55.mm], [3436.mm,2292.mm,55.mm])
  f.pushpull(8.mm)
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
  face = grp.entities.add_face([3893.mm,2062.mm,55.mm], [3901.mm,2062.mm,55.mm], [3901.mm,2362.mm,55.mm], [3893.mm,2362.mm,55.mm])
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
  f = ge.add_face([3893.mm,2362.mm,0.mm], [3893.mm,2362.mm,55.mm], [3893.mm,2292.mm,55.mm])
  f.pushpull(8.mm)
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

  # ═══ Right Walkway Hangers ═══
  defn = model.definitions.add("Right Walkway Hangers")
  ents = defn.entities
  # Right bearer (25x25x5 L) X4329
  grp = ents.add_group
  grp.name = "Right bearer (25x25x5 L) X4329"
  face = grp.entities.add_face([4316.5.mm,0.mm,40.mm], [4341.5.mm,0.mm,40.mm], [4341.5.mm,2362.mm,40.mm], [4316.5.mm,2362.mm,40.mm])
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
  circle = ge.add_circle([4329.mm,320.mm,65.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2323.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate X4329 Y320
  grp = ents.add_group
  grp.name = "Right ceiling plate X4329 Y320"
  face = grp.entities.add_face([4279.mm,290.mm,2382.mm], [4379.mm,290.mm,2382.mm], [4379.mm,350.mm,2382.mm], [4279.mm,350.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right hanger rod M10 X4329 Y457
  grp = ents.add_group
  grp.name = "Right hanger rod M10 X4329 Y457"
  ge = grp.entities
  circle = ge.add_circle([4329.mm,457.mm,65.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2323.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate X4329 Y457
  grp = ents.add_group
  grp.name = "Right ceiling plate X4329 Y457"
  face = grp.entities.add_face([4279.mm,427.mm,2382.mm], [4379.mm,427.mm,2382.mm], [4379.mm,487.mm,2382.mm], [4279.mm,487.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right hanger rod M10 X4329 Y914
  grp = ents.add_group
  grp.name = "Right hanger rod M10 X4329 Y914"
  ge = grp.entities
  circle = ge.add_circle([4329.mm,914.mm,65.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2323.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate X4329 Y914
  grp = ents.add_group
  grp.name = "Right ceiling plate X4329 Y914"
  face = grp.entities.add_face([4279.mm,884.mm,2382.mm], [4379.mm,884.mm,2382.mm], [4379.mm,944.mm,2382.mm], [4279.mm,944.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right hanger rod M10 X4329 Y1371
  grp = ents.add_group
  grp.name = "Right hanger rod M10 X4329 Y1371"
  ge = grp.entities
  circle = ge.add_circle([4329.mm,1371.mm,65.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2323.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate X4329 Y1371
  grp = ents.add_group
  grp.name = "Right ceiling plate X4329 Y1371"
  face = grp.entities.add_face([4279.mm,1341.mm,2382.mm], [4379.mm,1341.mm,2382.mm], [4379.mm,1401.mm,2382.mm], [4279.mm,1401.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right hanger rod M10 X4329 Y1828
  grp = ents.add_group
  grp.name = "Right hanger rod M10 X4329 Y1828"
  ge = grp.entities
  circle = ge.add_circle([4329.mm,1828.mm,65.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2323.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate X4329 Y1828
  grp = ents.add_group
  grp.name = "Right ceiling plate X4329 Y1828"
  face = grp.entities.add_face([4279.mm,1798.mm,2382.mm], [4379.mm,1798.mm,2382.mm], [4379.mm,1858.mm,2382.mm], [4279.mm,1858.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right bearer (25x25x5 L) X4629
  grp = ents.add_group
  grp.name = "Right bearer (25x25x5 L) X4629"
  face = grp.entities.add_face([4616.5.mm,0.mm,40.mm], [4641.5.mm,0.mm,40.mm], [4641.5.mm,2362.mm,40.mm], [4616.5.mm,2362.mm,40.mm])
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
  circle = ge.add_circle([4629.mm,320.mm,65.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2323.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate X4629 Y320
  grp = ents.add_group
  grp.name = "Right ceiling plate X4629 Y320"
  face = grp.entities.add_face([4579.mm,290.mm,2382.mm], [4679.mm,290.mm,2382.mm], [4679.mm,350.mm,2382.mm], [4579.mm,350.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right hanger rod M10 X4629 Y457
  grp = ents.add_group
  grp.name = "Right hanger rod M10 X4629 Y457"
  ge = grp.entities
  circle = ge.add_circle([4629.mm,457.mm,65.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2323.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate X4629 Y457
  grp = ents.add_group
  grp.name = "Right ceiling plate X4629 Y457"
  face = grp.entities.add_face([4579.mm,427.mm,2382.mm], [4679.mm,427.mm,2382.mm], [4679.mm,487.mm,2382.mm], [4579.mm,487.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right hanger rod M10 X4629 Y914
  grp = ents.add_group
  grp.name = "Right hanger rod M10 X4629 Y914"
  ge = grp.entities
  circle = ge.add_circle([4629.mm,914.mm,65.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2323.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate X4629 Y914
  grp = ents.add_group
  grp.name = "Right ceiling plate X4629 Y914"
  face = grp.entities.add_face([4579.mm,884.mm,2382.mm], [4679.mm,884.mm,2382.mm], [4679.mm,944.mm,2382.mm], [4579.mm,944.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right hanger rod M10 X4629 Y1371
  grp = ents.add_group
  grp.name = "Right hanger rod M10 X4629 Y1371"
  ge = grp.entities
  circle = ge.add_circle([4629.mm,1371.mm,65.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2323.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate X4629 Y1371
  grp = ents.add_group
  grp.name = "Right ceiling plate X4629 Y1371"
  face = grp.entities.add_face([4579.mm,1341.mm,2382.mm], [4679.mm,1341.mm,2382.mm], [4679.mm,1401.mm,2382.mm], [4579.mm,1401.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right hanger rod M10 X4629 Y1828
  grp = ents.add_group
  grp.name = "Right hanger rod M10 X4629 Y1828"
  ge = grp.entities
  circle = ge.add_circle([4629.mm,1828.mm,65.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2323.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right ceiling plate X4629 Y1828
  grp = ents.add_group
  grp.name = "Right ceiling plate X4629 Y1828"
  face = grp.entities.add_face([4579.mm,1798.mm,2382.mm], [4679.mm,1798.mm,2382.mm], [4679.mm,1858.mm,2382.mm], [4579.mm,1858.mm,2382.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
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
  # Left edge beam (40x40x3 steel SHS, full width)
  grp = ents.add_group
  grp.name = "Left edge beam (40x40x3 steel SHS, full width)"
  face = grp.entities.add_face([470.mm,0.mm,52.mm], [510.mm,0.mm,52.mm], [510.mm,2362.mm,52.mm], [470.mm,2362.mm,52.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left wall-seat plate near
  grp = ents.add_group
  grp.name = "Left wall-seat plate near"
  face = grp.entities.add_face([460.mm,0.mm,30.mm], [520.mm,0.mm,30.mm], [520.mm,8.mm,30.mm], [460.mm,8.mm,30.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(62.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left wall-seat ext plate near
  grp = ents.add_group
  grp.name = "Left wall-seat ext plate near"
  face = grp.entities.add_face([440.mm,-46.mm,-18.mm], [540.mm,-46.mm,-18.mm], [540.mm,-40.mm,-18.mm], [440.mm,-40.mm,-18.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(180.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left wall-seat bolt near
  grp = ents.add_group
  grp.name = "Left wall-seat bolt near"
  ge = grp.entities
  circle = ge.add_circle([490.mm,-46.mm,94.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Left wall-seat head near
  grp = ents.add_group
  grp.name = "Left wall-seat head near"
  face = grp.entities.add_face([481.mm,-52.mm,85.mm], [499.mm,-52.mm,85.mm], [499.mm,-46.mm,85.mm], [481.mm,-46.mm,85.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Left wall-seat bolt near
  grp = ents.add_group
  grp.name = "Left wall-seat bolt near"
  ge = grp.entities
  circle = ge.add_circle([462.mm,-46.mm,56.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Left wall-seat head near
  grp = ents.add_group
  grp.name = "Left wall-seat head near"
  face = grp.entities.add_face([453.mm,-52.mm,47.mm], [471.mm,-52.mm,47.mm], [471.mm,-46.mm,47.mm], [453.mm,-46.mm,47.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Left wall-seat bolt near
  grp = ents.add_group
  grp.name = "Left wall-seat bolt near"
  ge = grp.entities
  circle = ge.add_circle([518.mm,-46.mm,56.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Left wall-seat head near
  grp = ents.add_group
  grp.name = "Left wall-seat head near"
  face = grp.entities.add_face([509.mm,-52.mm,47.mm], [527.mm,-52.mm,47.mm], [527.mm,-46.mm,47.mm], [509.mm,-46.mm,47.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Left wall-seat plate far
  grp = ents.add_group
  grp.name = "Left wall-seat plate far"
  face = grp.entities.add_face([460.mm,2354.mm,30.mm], [520.mm,2354.mm,30.mm], [520.mm,2362.mm,30.mm], [460.mm,2362.mm,30.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(62.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left wall-seat ext plate far
  grp = ents.add_group
  grp.name = "Left wall-seat ext plate far"
  face = grp.entities.add_face([440.mm,2402.mm,-18.mm], [540.mm,2402.mm,-18.mm], [540.mm,2408.mm,-18.mm], [440.mm,2408.mm,-18.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(180.mm)
  mat = model.materials["Cantilever Near 1 plate"] || model.materials.add("Cantilever Near 1 plate")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left wall-seat bolt far
  grp = ents.add_group
  grp.name = "Left wall-seat bolt far"
  ge = grp.entities
  circle = ge.add_circle([490.mm,2354.mm,94.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Left wall-seat head far
  grp = ents.add_group
  grp.name = "Left wall-seat head far"
  face = grp.entities.add_face([481.mm,2408.mm,85.mm], [499.mm,2408.mm,85.mm], [499.mm,2414.mm,85.mm], [481.mm,2414.mm,85.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Left wall-seat bolt far
  grp = ents.add_group
  grp.name = "Left wall-seat bolt far"
  ge = grp.entities
  circle = ge.add_circle([462.mm,2354.mm,56.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Left wall-seat head far
  grp = ents.add_group
  grp.name = "Left wall-seat head far"
  face = grp.entities.add_face([453.mm,2408.mm,47.mm], [471.mm,2408.mm,47.mm], [471.mm,2414.mm,47.mm], [453.mm,2414.mm,47.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Left wall-seat bolt far
  grp = ents.add_group
  grp.name = "Left wall-seat bolt far"
  ge = grp.entities
  circle = ge.add_circle([518.mm,2354.mm,56.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(54.mm)
  mat = model.materials["Cantilever Near 1 bolt M12"] || model.materials.add("Cantilever Near 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Left wall-seat head far
  grp = ents.add_group
  grp.name = "Left wall-seat head far"
  face = grp.entities.add_face([509.mm,2408.mm,47.mm], [527.mm,2408.mm,47.mm], [527.mm,2414.mm,47.mm], [509.mm,2414.mm,47.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Cantilever Near 1 bolt head"] || model.materials.add("Cantilever Near 1 bolt head")
  mat.color = Sketchup::Color.new(60, 60, 68)
  mat.alpha = 1.0
  grp.material = mat

  # Left bearing strip (Al)
  grp = ents.add_group
  grp.name = "Left bearing strip (Al)"
  face = grp.entities.add_face([170.mm,300.mm,50.mm], [195.mm,300.mm,50.mm], [195.mm,2062.mm,50.mm], [170.mm,2062.mm,50.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Left bearing strip (Al)"] || model.materials.add("Left bearing strip (Al)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Left leg 1 (25x25x3 SHS)
  grp = ents.add_group
  grp.name = "Left leg 1 (25x25x3 SHS)"
  face = grp.entities.add_face([127.5.mm,727.5.mm,0.mm], [152.5.mm,727.5.mm,0.mm], [152.5.mm,752.5.mm,0.mm], [127.5.mm,752.5.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(65.mm)
  mat = model.materials["Left bearing strip (Al)"] || model.materials.add("Left bearing strip (Al)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Left leg 1 foot plate
  grp = ents.add_group
  grp.name = "Left leg 1 foot plate"
  face = grp.entities.add_face([110.mm,710.mm,0.mm], [170.mm,710.mm,0.mm], [170.mm,770.mm,0.mm], [110.mm,770.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Left bearing strip (Al)"] || model.materials.add("Left bearing strip (Al)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Left leg 1 arm
  grp = ents.add_group
  grp.name = "Left leg 1 arm"
  face = grp.entities.add_face([140.mm,727.5.mm,55.mm], [190.mm,727.5.mm,55.mm], [190.mm,752.5.mm,55.mm], [140.mm,752.5.mm,55.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Left bearing strip (Al)"] || model.materials.add("Left bearing strip (Al)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Left leg 2 (25x25x3 SHS)
  grp = ents.add_group
  grp.name = "Left leg 2 (25x25x3 SHS)"
  face = grp.entities.add_face([127.5.mm,1168.5.mm,0.mm], [152.5.mm,1168.5.mm,0.mm], [152.5.mm,1193.5.mm,0.mm], [127.5.mm,1193.5.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(65.mm)
  mat = model.materials["Left bearing strip (Al)"] || model.materials.add("Left bearing strip (Al)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Left leg 2 foot plate
  grp = ents.add_group
  grp.name = "Left leg 2 foot plate"
  face = grp.entities.add_face([110.mm,1151.mm,0.mm], [170.mm,1151.mm,0.mm], [170.mm,1211.mm,0.mm], [110.mm,1211.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Left bearing strip (Al)"] || model.materials.add("Left bearing strip (Al)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Left leg 2 arm
  grp = ents.add_group
  grp.name = "Left leg 2 arm"
  face = grp.entities.add_face([140.mm,1168.5.mm,55.mm], [190.mm,1168.5.mm,55.mm], [190.mm,1193.5.mm,55.mm], [140.mm,1193.5.mm,55.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Left bearing strip (Al)"] || model.materials.add("Left bearing strip (Al)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Left leg 3 (25x25x3 SHS)
  grp = ents.add_group
  grp.name = "Left leg 3 (25x25x3 SHS)"
  face = grp.entities.add_face([127.5.mm,1609.5.mm,0.mm], [152.5.mm,1609.5.mm,0.mm], [152.5.mm,1634.5.mm,0.mm], [127.5.mm,1634.5.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(65.mm)
  mat = model.materials["Left bearing strip (Al)"] || model.materials.add("Left bearing strip (Al)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Left leg 3 foot plate
  grp = ents.add_group
  grp.name = "Left leg 3 foot plate"
  face = grp.entities.add_face([110.mm,1592.mm,0.mm], [170.mm,1592.mm,0.mm], [170.mm,1652.mm,0.mm], [110.mm,1652.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Left bearing strip (Al)"] || model.materials.add("Left bearing strip (Al)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Left leg 3 arm
  grp = ents.add_group
  grp.name = "Left leg 3 arm"
  face = grp.entities.add_face([140.mm,1609.5.mm,55.mm], [190.mm,1609.5.mm,55.mm], [190.mm,1634.5.mm,55.mm], [140.mm,1634.5.mm,55.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Left bearing strip (Al)"] || model.materials.add("Left bearing strip (Al)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Left Walkway Support"
  inst.layer = model.layers["Left Support"]


model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags from earlier generator versions ──
keep_tags = ["Container", "Processing Tray", "Walkways", "Cantilevers", "Right Hangers", "Left Support"]
default_layer = model.layers[0]
model.layers.to_a.each { |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}

# ── Scenes — one shared iso camera; scenes only toggle visibility ──
model.layers.each { |l| l.visible = true }
bb = model.bounds
ctr = bb.center
dir = Geom::Vector3d.new(-0.55, -0.7, 0.45); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.4)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

model.pages.add("Combined")
[["Gates (walkway decks)", ["Walkways", "Processing Tray"]], ["Cantilevers (+ exterior braces/bolts)", ["Cantilevers", "Processing Tray"]], ["Right Hangers", ["Right Hangers", "Walkways", "Processing Tray"]], ["Left Support (bearer + legs)", ["Left Support", "Cantilevers", "Processing Tray"]], ["Processing Tray", ["Processing Tray"]]].each { |name, tags|
  model.layers.each { |l| l.visible = (l == default_layer || l.name == "Container" || tags.include?(l.name)) }
  page = model.pages.add(name)
  page.use_camera = true
}
model.layers.each { |l| l.visible = true }

model.commit_operation
{ success: true, model: "Walkway + Cantilevers",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
