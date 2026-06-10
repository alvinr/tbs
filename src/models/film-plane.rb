model = Sketchup.active_model
model.start_operation("TBS-001 Film Plane (Option A)", true)
entities = model.active_entities
opts = model.options["UnitsOptions"]; opts["LengthUnit"]=2; opts["LengthFormat"]=0; opts["LengthPrecision"]=1

to_erase = entities.to_a.select { |e| e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text) }
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each { |p| model.pages.erase(p) }

  model.layers.add("Context") unless model.layers["Context"]
  model.layers.add("Film Plane") unless model.layers["Film Plane"]
  model.layers.add("Corner Mechanism") unless model.layers["Corner Mechanism"]
  model.layers.add("Processing Tray") unless model.layers["Processing Tray"]
  model.layers.add("Walkways") unless model.layers["Walkways"]
  model.layers.add("Corner Detail") unless model.layers["Corner Detail"]
  model.layers.add("Labels") unless model.layers["Labels"]

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

  # Ceiling (context)
  grp = ents.add_group
  grp.name = "Ceiling (context)"
  face = grp.entities.add_face([0.mm,0.mm,2388.mm], [5893.mm,0.mm,2388.mm], [5893.mm,2362.mm,2388.mm], [0.mm,2362.mm,2388.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Ceiling (context)"] || model.materials.add("Ceiling (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.08
  grp.material = mat

  # Side Wall near (context)
  grp = ents.add_group
  grp.name = "Side Wall near (context)"
  face = grp.entities.add_face([0.mm,-40.mm,0.mm], [5893.mm,-40.mm,0.mm], [5893.mm,0.mm,0.mm], [0.mm,0.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Side Wall near (context)"] || model.materials.add("Side Wall near (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.14
  grp.material = mat

  # Side Wall far (context)
  grp = ents.add_group
  grp.name = "Side Wall far (context)"
  face = grp.entities.add_face([0.mm,2362.mm,0.mm], [5893.mm,2362.mm,0.mm], [5893.mm,2402.mm,0.mm], [0.mm,2402.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Side Wall near (context)"] || model.materials.add("Side Wall near (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.14
  grp.material = mat

  # Pinhole Wall (context)
  grp = ents.add_group
  grp.name = "Pinhole Wall (context)"
  face = grp.entities.add_face([-40.mm,0.mm,0.mm], [0.mm,0.mm,0.mm], [0.mm,2362.mm,0.mm], [-40.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Pinhole Wall (context)"] || model.materials.add("Pinhole Wall (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.16
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Container (ghost)"
  inst.layer = model.layers["Context"]

  # ═══ Near-wall equipment (ghost) ═══
  defn = model.definitions.add("Near-wall equipment (ghost)")
  ents = defn.entities
  # Electrical Panel (EP) [ghost]
  grp = ents.add_group
  grp.name = "Electrical Panel (EP) [ghost]"
  face = grp.entities.add_face([1910.mm,0.mm,1650.mm], [2210.mm,0.mm,1650.mm], [2210.mm,160.mm,1650.mm], [1910.mm,160.mm,1650.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(600.mm)
  mat = model.materials["Electrical Panel (EP) [ghost]"] || model.materials.add("Electrical Panel (EP) [ghost]")
  mat.color = Sketchup::Color.new(245, 197, 24)
  mat.alpha = 0.28
  grp.material = mat

  # Battery 1 [ghost]
  grp = ents.add_group
  grp.name = "Battery 1 [ghost]"
  face = grp.entities.add_face([1810.mm,0.mm,150.mm], [2050.mm,0.mm,150.mm], [2050.mm,120.mm,150.mm], [1810.mm,120.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(500.mm)
  mat = model.materials["Battery 1 [ghost]"] || model.materials.add("Battery 1 [ghost]")
  mat.color = Sketchup::Color.new(106, 90, 205)
  mat.alpha = 0.28
  grp.material = mat

  # Battery 2 [ghost]
  grp = ents.add_group
  grp.name = "Battery 2 [ghost]"
  face = grp.entities.add_face([2070.mm,0.mm,150.mm], [2310.mm,0.mm,150.mm], [2310.mm,120.mm,150.mm], [2070.mm,120.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(500.mm)
  mat = model.materials["Battery 1 [ghost]"] || model.materials.add("Battery 1 [ghost]")
  mat.color = Sketchup::Color.new(106, 90, 205)
  mat.alpha = 0.28
  grp.material = mat

  # Power panel (interior face) [ghost]
  grp = ents.add_group
  grp.name = "Power panel (interior face) [ghost]"
  face = grp.entities.add_face([1250.mm,0.mm,1830.mm], [1590.mm,0.mm,1830.mm], [1590.mm,20.mm,1830.mm], [1250.mm,20.mm,1830.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(240.mm)
  mat = model.materials["Electrical Panel (EP) [ghost]"] || model.materials.add("Electrical Panel (EP) [ghost]")
  mat.color = Sketchup::Color.new(245, 197, 24)
  mat.alpha = 0.28
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Near-wall equipment (ghost)"
  inst.layer = model.layers["Context"]

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

  # ═══ Corner Mechanism ═══
  defn = model.definitions.add("Corner Mechanism")
  ents = defn.entities
  # HGR20 Rail TL
  grp = ents.add_group
  grp.name = "HGR20 Rail TL"
  face = grp.entities.add_face([138.mm,100.mm,2280.mm], [162.mm,100.mm,2280.mm], [162.mm,2300.mm,2280.mm], [138.mm,2300.mm,2280.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Detail Rail TR"] || model.materials.add("Detail Rail TR")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Leadscrew TL
  grp = ents.add_group
  grp.name = "Leadscrew TL"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 2200.mm, 0.mm)
  circle = ge.add_circle([184.mm,100.mm,2288.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # HGR20 Rail TR
  grp = ents.add_group
  grp.name = "HGR20 Rail TR"
  face = grp.entities.add_face([4637.mm,100.mm,2280.mm], [4661.mm,100.mm,2280.mm], [4661.mm,2300.mm,2280.mm], [4637.mm,2300.mm,2280.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Detail Rail TR"] || model.materials.add("Detail Rail TR")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Leadscrew TR
  grp = ents.add_group
  grp.name = "Leadscrew TR"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 2200.mm, 0.mm)
  circle = ge.add_circle([4683.mm,100.mm,2288.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # HGR20 Rail BL
  grp = ents.add_group
  grp.name = "HGR20 Rail BL"
  face = grp.entities.add_face([138.mm,100.mm,142.mm], [162.mm,100.mm,142.mm], [162.mm,2300.mm,142.mm], [138.mm,2300.mm,142.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Detail Rail TR"] || model.materials.add("Detail Rail TR")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Leadscrew BL
  grp = ents.add_group
  grp.name = "Leadscrew BL"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 2200.mm, 0.mm)
  circle = ge.add_circle([184.mm,100.mm,150.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # HGR20 Rail BR
  grp = ents.add_group
  grp.name = "HGR20 Rail BR"
  face = grp.entities.add_face([4637.mm,100.mm,142.mm], [4661.mm,100.mm,142.mm], [4661.mm,2300.mm,142.mm], [4637.mm,2300.mm,142.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Detail Rail TR"] || model.materials.add("Detail Rail TR")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Leadscrew BR
  grp = ents.add_group
  grp.name = "Leadscrew BR"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 2200.mm, 0.mm)
  circle = ge.add_circle([4683.mm,100.mm,150.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Brace Vert L (near/pinhole)
  grp = ents.add_group
  grp.name = "FP Brace Vert L (near/pinhole)"
  face = grp.entities.add_face([150.mm,100.mm,150.mm], [200.mm,100.mm,150.mm], [200.mm,150.mm,150.mm], [150.mm,150.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2138.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Brace Vert R (near/pinhole)
  grp = ents.add_group
  grp.name = "FP Brace Vert R (near/pinhole)"
  face = grp.entities.add_face([4599.mm,100.mm,150.mm], [4649.mm,100.mm,150.mm], [4649.mm,150.mm,150.mm], [4599.mm,150.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2138.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Brace Beam Bottom (near/pinhole)
  grp = ents.add_group
  grp.name = "FP Brace Beam Bottom (near/pinhole)"
  face = grp.entities.add_face([150.mm,100.mm,150.mm], [4649.mm,100.mm,150.mm], [4649.mm,150.mm,150.mm], [150.mm,150.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Brace Beam Top (near/pinhole)
  grp = ents.add_group
  grp.name = "FP Brace Beam Top (near/pinhole)"
  face = grp.entities.add_face([150.mm,100.mm,2238.mm], [4649.mm,100.mm,2238.mm], [4649.mm,150.mm,2238.mm], [150.mm,150.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Brace Vert L (far/film)
  grp = ents.add_group
  grp.name = "FP Brace Vert L (far/film)"
  face = grp.entities.add_face([150.mm,2262.mm,150.mm], [200.mm,2262.mm,150.mm], [200.mm,2312.mm,150.mm], [150.mm,2312.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2138.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Brace Vert R (far/film)
  grp = ents.add_group
  grp.name = "FP Brace Vert R (far/film)"
  face = grp.entities.add_face([4599.mm,2262.mm,150.mm], [4649.mm,2262.mm,150.mm], [4649.mm,2312.mm,150.mm], [4599.mm,2312.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2138.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Brace Beam Bottom (far/film)
  grp = ents.add_group
  grp.name = "FP Brace Beam Bottom (far/film)"
  face = grp.entities.add_face([150.mm,2262.mm,150.mm], [4649.mm,2262.mm,150.mm], [4649.mm,2312.mm,150.mm], [150.mm,2312.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Brace Beam Top (far/film)
  grp = ents.add_group
  grp.name = "FP Brace Beam Top (far/film)"
  face = grp.entities.add_face([150.mm,2262.mm,2238.mm], [4649.mm,2262.mm,2238.mm], [4649.mm,2312.mm,2238.mm], [150.mm,2312.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall-tie strut X600 Z150 near
  grp = ents.add_group
  grp.name = "FP wall-tie strut X600 Z150 near"
  face = grp.entities.add_face([578.mm,0.mm,150.mm], [622.mm,0.mm,150.mm], [622.mm,100.mm,150.mm], [578.mm,100.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP inside plate X600 Z150 near
  grp = ents.add_group
  grp.name = "FP inside plate X600 Z150 near"
  face = grp.entities.add_face([550.mm,0.mm,130.mm], [650.mm,0.mm,130.mm], [650.mm,8.mm,130.mm], [550.mm,8.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP OUTSIDE plate X600 Z150 near
  grp = ents.add_group
  grp.name = "FP OUTSIDE plate X600 Z150 near"
  face = grp.entities.add_face([550.mm,-48.mm,130.mm], [650.mm,-48.mm,130.mm], [650.mm,-40.mm,130.mm], [550.mm,-40.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X570 Z150 near
  grp = ents.add_group
  grp.name = "FP wall bolt X570 Z150 near"
  face = grp.entities.add_face([564.mm,-48.mm,169.mm], [576.mm,-48.mm,169.mm], [576.mm,8.mm,169.mm], [564.mm,8.mm,169.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X630 Z150 near
  grp = ents.add_group
  grp.name = "FP wall bolt X630 Z150 near"
  face = grp.entities.add_face([624.mm,-48.mm,169.mm], [636.mm,-48.mm,169.mm], [636.mm,8.mm,169.mm], [624.mm,8.mm,169.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall-tie strut X600 Z2238 near
  grp = ents.add_group
  grp.name = "FP wall-tie strut X600 Z2238 near"
  face = grp.entities.add_face([578.mm,0.mm,2238.mm], [622.mm,0.mm,2238.mm], [622.mm,100.mm,2238.mm], [578.mm,100.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP inside plate X600 Z2238 near
  grp = ents.add_group
  grp.name = "FP inside plate X600 Z2238 near"
  face = grp.entities.add_face([550.mm,0.mm,2218.mm], [650.mm,0.mm,2218.mm], [650.mm,8.mm,2218.mm], [550.mm,8.mm,2218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP OUTSIDE plate X600 Z2238 near
  grp = ents.add_group
  grp.name = "FP OUTSIDE plate X600 Z2238 near"
  face = grp.entities.add_face([550.mm,-48.mm,2218.mm], [650.mm,-48.mm,2218.mm], [650.mm,-40.mm,2218.mm], [550.mm,-40.mm,2218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X570 Z2238 near
  grp = ents.add_group
  grp.name = "FP wall bolt X570 Z2238 near"
  face = grp.entities.add_face([564.mm,-48.mm,2257.mm], [576.mm,-48.mm,2257.mm], [576.mm,8.mm,2257.mm], [564.mm,8.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X630 Z2238 near
  grp = ents.add_group
  grp.name = "FP wall bolt X630 Z2238 near"
  face = grp.entities.add_face([624.mm,-48.mm,2257.mm], [636.mm,-48.mm,2257.mm], [636.mm,8.mm,2257.mm], [624.mm,8.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall-tie strut X1300 Z150 near
  grp = ents.add_group
  grp.name = "FP wall-tie strut X1300 Z150 near"
  face = grp.entities.add_face([1278.mm,0.mm,150.mm], [1322.mm,0.mm,150.mm], [1322.mm,100.mm,150.mm], [1278.mm,100.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP inside plate X1300 Z150 near
  grp = ents.add_group
  grp.name = "FP inside plate X1300 Z150 near"
  face = grp.entities.add_face([1250.mm,0.mm,130.mm], [1350.mm,0.mm,130.mm], [1350.mm,8.mm,130.mm], [1250.mm,8.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP OUTSIDE plate X1300 Z150 near
  grp = ents.add_group
  grp.name = "FP OUTSIDE plate X1300 Z150 near"
  face = grp.entities.add_face([1250.mm,-48.mm,130.mm], [1350.mm,-48.mm,130.mm], [1350.mm,-40.mm,130.mm], [1250.mm,-40.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X1270 Z150 near
  grp = ents.add_group
  grp.name = "FP wall bolt X1270 Z150 near"
  face = grp.entities.add_face([1264.mm,-48.mm,169.mm], [1276.mm,-48.mm,169.mm], [1276.mm,8.mm,169.mm], [1264.mm,8.mm,169.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X1330 Z150 near
  grp = ents.add_group
  grp.name = "FP wall bolt X1330 Z150 near"
  face = grp.entities.add_face([1324.mm,-48.mm,169.mm], [1336.mm,-48.mm,169.mm], [1336.mm,8.mm,169.mm], [1324.mm,8.mm,169.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall-tie strut X1300 Z2238 near
  grp = ents.add_group
  grp.name = "FP wall-tie strut X1300 Z2238 near"
  face = grp.entities.add_face([1278.mm,0.mm,2238.mm], [1322.mm,0.mm,2238.mm], [1322.mm,100.mm,2238.mm], [1278.mm,100.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP inside plate X1300 Z2238 near
  grp = ents.add_group
  grp.name = "FP inside plate X1300 Z2238 near"
  face = grp.entities.add_face([1250.mm,0.mm,2218.mm], [1350.mm,0.mm,2218.mm], [1350.mm,8.mm,2218.mm], [1250.mm,8.mm,2218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP OUTSIDE plate X1300 Z2238 near
  grp = ents.add_group
  grp.name = "FP OUTSIDE plate X1300 Z2238 near"
  face = grp.entities.add_face([1250.mm,-48.mm,2218.mm], [1350.mm,-48.mm,2218.mm], [1350.mm,-40.mm,2218.mm], [1250.mm,-40.mm,2218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X1270 Z2238 near
  grp = ents.add_group
  grp.name = "FP wall bolt X1270 Z2238 near"
  face = grp.entities.add_face([1264.mm,-48.mm,2257.mm], [1276.mm,-48.mm,2257.mm], [1276.mm,8.mm,2257.mm], [1264.mm,8.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X1330 Z2238 near
  grp = ents.add_group
  grp.name = "FP wall bolt X1330 Z2238 near"
  face = grp.entities.add_face([1324.mm,-48.mm,2257.mm], [1336.mm,-48.mm,2257.mm], [1336.mm,8.mm,2257.mm], [1324.mm,8.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall-tie strut X3100 Z150 near
  grp = ents.add_group
  grp.name = "FP wall-tie strut X3100 Z150 near"
  face = grp.entities.add_face([3078.mm,0.mm,150.mm], [3122.mm,0.mm,150.mm], [3122.mm,100.mm,150.mm], [3078.mm,100.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP inside plate X3100 Z150 near
  grp = ents.add_group
  grp.name = "FP inside plate X3100 Z150 near"
  face = grp.entities.add_face([3050.mm,0.mm,130.mm], [3150.mm,0.mm,130.mm], [3150.mm,8.mm,130.mm], [3050.mm,8.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP OUTSIDE plate X3100 Z150 near
  grp = ents.add_group
  grp.name = "FP OUTSIDE plate X3100 Z150 near"
  face = grp.entities.add_face([3050.mm,-48.mm,130.mm], [3150.mm,-48.mm,130.mm], [3150.mm,-40.mm,130.mm], [3050.mm,-40.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X3070 Z150 near
  grp = ents.add_group
  grp.name = "FP wall bolt X3070 Z150 near"
  face = grp.entities.add_face([3064.mm,-48.mm,169.mm], [3076.mm,-48.mm,169.mm], [3076.mm,8.mm,169.mm], [3064.mm,8.mm,169.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X3130 Z150 near
  grp = ents.add_group
  grp.name = "FP wall bolt X3130 Z150 near"
  face = grp.entities.add_face([3124.mm,-48.mm,169.mm], [3136.mm,-48.mm,169.mm], [3136.mm,8.mm,169.mm], [3124.mm,8.mm,169.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall-tie strut X3100 Z2238 near
  grp = ents.add_group
  grp.name = "FP wall-tie strut X3100 Z2238 near"
  face = grp.entities.add_face([3078.mm,0.mm,2238.mm], [3122.mm,0.mm,2238.mm], [3122.mm,100.mm,2238.mm], [3078.mm,100.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP inside plate X3100 Z2238 near
  grp = ents.add_group
  grp.name = "FP inside plate X3100 Z2238 near"
  face = grp.entities.add_face([3050.mm,0.mm,2218.mm], [3150.mm,0.mm,2218.mm], [3150.mm,8.mm,2218.mm], [3050.mm,8.mm,2218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP OUTSIDE plate X3100 Z2238 near
  grp = ents.add_group
  grp.name = "FP OUTSIDE plate X3100 Z2238 near"
  face = grp.entities.add_face([3050.mm,-48.mm,2218.mm], [3150.mm,-48.mm,2218.mm], [3150.mm,-40.mm,2218.mm], [3050.mm,-40.mm,2218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X3070 Z2238 near
  grp = ents.add_group
  grp.name = "FP wall bolt X3070 Z2238 near"
  face = grp.entities.add_face([3064.mm,-48.mm,2257.mm], [3076.mm,-48.mm,2257.mm], [3076.mm,8.mm,2257.mm], [3064.mm,8.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X3130 Z2238 near
  grp = ents.add_group
  grp.name = "FP wall bolt X3130 Z2238 near"
  face = grp.entities.add_face([3124.mm,-48.mm,2257.mm], [3136.mm,-48.mm,2257.mm], [3136.mm,8.mm,2257.mm], [3124.mm,8.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall-tie strut X4200 Z150 near
  grp = ents.add_group
  grp.name = "FP wall-tie strut X4200 Z150 near"
  face = grp.entities.add_face([4178.mm,0.mm,150.mm], [4222.mm,0.mm,150.mm], [4222.mm,100.mm,150.mm], [4178.mm,100.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP inside plate X4200 Z150 near
  grp = ents.add_group
  grp.name = "FP inside plate X4200 Z150 near"
  face = grp.entities.add_face([4150.mm,0.mm,130.mm], [4250.mm,0.mm,130.mm], [4250.mm,8.mm,130.mm], [4150.mm,8.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP OUTSIDE plate X4200 Z150 near
  grp = ents.add_group
  grp.name = "FP OUTSIDE plate X4200 Z150 near"
  face = grp.entities.add_face([4150.mm,-48.mm,130.mm], [4250.mm,-48.mm,130.mm], [4250.mm,-40.mm,130.mm], [4150.mm,-40.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X4170 Z150 near
  grp = ents.add_group
  grp.name = "FP wall bolt X4170 Z150 near"
  face = grp.entities.add_face([4164.mm,-48.mm,169.mm], [4176.mm,-48.mm,169.mm], [4176.mm,8.mm,169.mm], [4164.mm,8.mm,169.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X4230 Z150 near
  grp = ents.add_group
  grp.name = "FP wall bolt X4230 Z150 near"
  face = grp.entities.add_face([4224.mm,-48.mm,169.mm], [4236.mm,-48.mm,169.mm], [4236.mm,8.mm,169.mm], [4224.mm,8.mm,169.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall-tie strut X4200 Z2238 near
  grp = ents.add_group
  grp.name = "FP wall-tie strut X4200 Z2238 near"
  face = grp.entities.add_face([4178.mm,0.mm,2238.mm], [4222.mm,0.mm,2238.mm], [4222.mm,100.mm,2238.mm], [4178.mm,100.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP inside plate X4200 Z2238 near
  grp = ents.add_group
  grp.name = "FP inside plate X4200 Z2238 near"
  face = grp.entities.add_face([4150.mm,0.mm,2218.mm], [4250.mm,0.mm,2218.mm], [4250.mm,8.mm,2218.mm], [4150.mm,8.mm,2218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP OUTSIDE plate X4200 Z2238 near
  grp = ents.add_group
  grp.name = "FP OUTSIDE plate X4200 Z2238 near"
  face = grp.entities.add_face([4150.mm,-48.mm,2218.mm], [4250.mm,-48.mm,2218.mm], [4250.mm,-40.mm,2218.mm], [4150.mm,-40.mm,2218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X4170 Z2238 near
  grp = ents.add_group
  grp.name = "FP wall bolt X4170 Z2238 near"
  face = grp.entities.add_face([4164.mm,-48.mm,2257.mm], [4176.mm,-48.mm,2257.mm], [4176.mm,8.mm,2257.mm], [4164.mm,8.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X4230 Z2238 near
  grp = ents.add_group
  grp.name = "FP wall bolt X4230 Z2238 near"
  face = grp.entities.add_face([4224.mm,-48.mm,2257.mm], [4236.mm,-48.mm,2257.mm], [4236.mm,8.mm,2257.mm], [4224.mm,8.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall-tie strut X600 Z150 far
  grp = ents.add_group
  grp.name = "FP wall-tie strut X600 Z150 far"
  face = grp.entities.add_face([578.mm,2262.mm,150.mm], [622.mm,2262.mm,150.mm], [622.mm,2362.mm,150.mm], [578.mm,2362.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP inside plate X600 Z150 far
  grp = ents.add_group
  grp.name = "FP inside plate X600 Z150 far"
  face = grp.entities.add_face([550.mm,2354.mm,130.mm], [650.mm,2354.mm,130.mm], [650.mm,2362.mm,130.mm], [550.mm,2362.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP OUTSIDE plate X600 Z150 far
  grp = ents.add_group
  grp.name = "FP OUTSIDE plate X600 Z150 far"
  face = grp.entities.add_face([550.mm,2402.mm,130.mm], [650.mm,2402.mm,130.mm], [650.mm,2410.mm,130.mm], [550.mm,2410.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X570 Z150 far
  grp = ents.add_group
  grp.name = "FP wall bolt X570 Z150 far"
  face = grp.entities.add_face([564.mm,2354.mm,169.mm], [576.mm,2354.mm,169.mm], [576.mm,2410.mm,169.mm], [564.mm,2410.mm,169.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X630 Z150 far
  grp = ents.add_group
  grp.name = "FP wall bolt X630 Z150 far"
  face = grp.entities.add_face([624.mm,2354.mm,169.mm], [636.mm,2354.mm,169.mm], [636.mm,2410.mm,169.mm], [624.mm,2410.mm,169.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall-tie strut X600 Z2238 far
  grp = ents.add_group
  grp.name = "FP wall-tie strut X600 Z2238 far"
  face = grp.entities.add_face([578.mm,2262.mm,2238.mm], [622.mm,2262.mm,2238.mm], [622.mm,2362.mm,2238.mm], [578.mm,2362.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP inside plate X600 Z2238 far
  grp = ents.add_group
  grp.name = "FP inside plate X600 Z2238 far"
  face = grp.entities.add_face([550.mm,2354.mm,2218.mm], [650.mm,2354.mm,2218.mm], [650.mm,2362.mm,2218.mm], [550.mm,2362.mm,2218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP OUTSIDE plate X600 Z2238 far
  grp = ents.add_group
  grp.name = "FP OUTSIDE plate X600 Z2238 far"
  face = grp.entities.add_face([550.mm,2402.mm,2218.mm], [650.mm,2402.mm,2218.mm], [650.mm,2410.mm,2218.mm], [550.mm,2410.mm,2218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X570 Z2238 far
  grp = ents.add_group
  grp.name = "FP wall bolt X570 Z2238 far"
  face = grp.entities.add_face([564.mm,2354.mm,2257.mm], [576.mm,2354.mm,2257.mm], [576.mm,2410.mm,2257.mm], [564.mm,2410.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X630 Z2238 far
  grp = ents.add_group
  grp.name = "FP wall bolt X630 Z2238 far"
  face = grp.entities.add_face([624.mm,2354.mm,2257.mm], [636.mm,2354.mm,2257.mm], [636.mm,2410.mm,2257.mm], [624.mm,2410.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall-tie strut X1700 Z150 far
  grp = ents.add_group
  grp.name = "FP wall-tie strut X1700 Z150 far"
  face = grp.entities.add_face([1678.mm,2262.mm,150.mm], [1722.mm,2262.mm,150.mm], [1722.mm,2362.mm,150.mm], [1678.mm,2362.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP inside plate X1700 Z150 far
  grp = ents.add_group
  grp.name = "FP inside plate X1700 Z150 far"
  face = grp.entities.add_face([1650.mm,2354.mm,130.mm], [1750.mm,2354.mm,130.mm], [1750.mm,2362.mm,130.mm], [1650.mm,2362.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP OUTSIDE plate X1700 Z150 far
  grp = ents.add_group
  grp.name = "FP OUTSIDE plate X1700 Z150 far"
  face = grp.entities.add_face([1650.mm,2402.mm,130.mm], [1750.mm,2402.mm,130.mm], [1750.mm,2410.mm,130.mm], [1650.mm,2410.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X1670 Z150 far
  grp = ents.add_group
  grp.name = "FP wall bolt X1670 Z150 far"
  face = grp.entities.add_face([1664.mm,2354.mm,169.mm], [1676.mm,2354.mm,169.mm], [1676.mm,2410.mm,169.mm], [1664.mm,2410.mm,169.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X1730 Z150 far
  grp = ents.add_group
  grp.name = "FP wall bolt X1730 Z150 far"
  face = grp.entities.add_face([1724.mm,2354.mm,169.mm], [1736.mm,2354.mm,169.mm], [1736.mm,2410.mm,169.mm], [1724.mm,2410.mm,169.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall-tie strut X1700 Z2238 far
  grp = ents.add_group
  grp.name = "FP wall-tie strut X1700 Z2238 far"
  face = grp.entities.add_face([1678.mm,2262.mm,2238.mm], [1722.mm,2262.mm,2238.mm], [1722.mm,2362.mm,2238.mm], [1678.mm,2362.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP inside plate X1700 Z2238 far
  grp = ents.add_group
  grp.name = "FP inside plate X1700 Z2238 far"
  face = grp.entities.add_face([1650.mm,2354.mm,2218.mm], [1750.mm,2354.mm,2218.mm], [1750.mm,2362.mm,2218.mm], [1650.mm,2362.mm,2218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP OUTSIDE plate X1700 Z2238 far
  grp = ents.add_group
  grp.name = "FP OUTSIDE plate X1700 Z2238 far"
  face = grp.entities.add_face([1650.mm,2402.mm,2218.mm], [1750.mm,2402.mm,2218.mm], [1750.mm,2410.mm,2218.mm], [1650.mm,2410.mm,2218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X1670 Z2238 far
  grp = ents.add_group
  grp.name = "FP wall bolt X1670 Z2238 far"
  face = grp.entities.add_face([1664.mm,2354.mm,2257.mm], [1676.mm,2354.mm,2257.mm], [1676.mm,2410.mm,2257.mm], [1664.mm,2410.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X1730 Z2238 far
  grp = ents.add_group
  grp.name = "FP wall bolt X1730 Z2238 far"
  face = grp.entities.add_face([1724.mm,2354.mm,2257.mm], [1736.mm,2354.mm,2257.mm], [1736.mm,2410.mm,2257.mm], [1724.mm,2410.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall-tie strut X2800 Z150 far
  grp = ents.add_group
  grp.name = "FP wall-tie strut X2800 Z150 far"
  face = grp.entities.add_face([2778.mm,2262.mm,150.mm], [2822.mm,2262.mm,150.mm], [2822.mm,2362.mm,150.mm], [2778.mm,2362.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP inside plate X2800 Z150 far
  grp = ents.add_group
  grp.name = "FP inside plate X2800 Z150 far"
  face = grp.entities.add_face([2750.mm,2354.mm,130.mm], [2850.mm,2354.mm,130.mm], [2850.mm,2362.mm,130.mm], [2750.mm,2362.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP OUTSIDE plate X2800 Z150 far
  grp = ents.add_group
  grp.name = "FP OUTSIDE plate X2800 Z150 far"
  face = grp.entities.add_face([2750.mm,2402.mm,130.mm], [2850.mm,2402.mm,130.mm], [2850.mm,2410.mm,130.mm], [2750.mm,2410.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X2770 Z150 far
  grp = ents.add_group
  grp.name = "FP wall bolt X2770 Z150 far"
  face = grp.entities.add_face([2764.mm,2354.mm,169.mm], [2776.mm,2354.mm,169.mm], [2776.mm,2410.mm,169.mm], [2764.mm,2410.mm,169.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X2830 Z150 far
  grp = ents.add_group
  grp.name = "FP wall bolt X2830 Z150 far"
  face = grp.entities.add_face([2824.mm,2354.mm,169.mm], [2836.mm,2354.mm,169.mm], [2836.mm,2410.mm,169.mm], [2824.mm,2410.mm,169.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall-tie strut X2800 Z2238 far
  grp = ents.add_group
  grp.name = "FP wall-tie strut X2800 Z2238 far"
  face = grp.entities.add_face([2778.mm,2262.mm,2238.mm], [2822.mm,2262.mm,2238.mm], [2822.mm,2362.mm,2238.mm], [2778.mm,2362.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP inside plate X2800 Z2238 far
  grp = ents.add_group
  grp.name = "FP inside plate X2800 Z2238 far"
  face = grp.entities.add_face([2750.mm,2354.mm,2218.mm], [2850.mm,2354.mm,2218.mm], [2850.mm,2362.mm,2218.mm], [2750.mm,2362.mm,2218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP OUTSIDE plate X2800 Z2238 far
  grp = ents.add_group
  grp.name = "FP OUTSIDE plate X2800 Z2238 far"
  face = grp.entities.add_face([2750.mm,2402.mm,2218.mm], [2850.mm,2402.mm,2218.mm], [2850.mm,2410.mm,2218.mm], [2750.mm,2410.mm,2218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X2770 Z2238 far
  grp = ents.add_group
  grp.name = "FP wall bolt X2770 Z2238 far"
  face = grp.entities.add_face([2764.mm,2354.mm,2257.mm], [2776.mm,2354.mm,2257.mm], [2776.mm,2410.mm,2257.mm], [2764.mm,2410.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X2830 Z2238 far
  grp = ents.add_group
  grp.name = "FP wall bolt X2830 Z2238 far"
  face = grp.entities.add_face([2824.mm,2354.mm,2257.mm], [2836.mm,2354.mm,2257.mm], [2836.mm,2410.mm,2257.mm], [2824.mm,2410.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall-tie strut X4200 Z150 far
  grp = ents.add_group
  grp.name = "FP wall-tie strut X4200 Z150 far"
  face = grp.entities.add_face([4178.mm,2262.mm,150.mm], [4222.mm,2262.mm,150.mm], [4222.mm,2362.mm,150.mm], [4178.mm,2362.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP inside plate X4200 Z150 far
  grp = ents.add_group
  grp.name = "FP inside plate X4200 Z150 far"
  face = grp.entities.add_face([4150.mm,2354.mm,130.mm], [4250.mm,2354.mm,130.mm], [4250.mm,2362.mm,130.mm], [4150.mm,2362.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP OUTSIDE plate X4200 Z150 far
  grp = ents.add_group
  grp.name = "FP OUTSIDE plate X4200 Z150 far"
  face = grp.entities.add_face([4150.mm,2402.mm,130.mm], [4250.mm,2402.mm,130.mm], [4250.mm,2410.mm,130.mm], [4150.mm,2410.mm,130.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X4170 Z150 far
  grp = ents.add_group
  grp.name = "FP wall bolt X4170 Z150 far"
  face = grp.entities.add_face([4164.mm,2354.mm,169.mm], [4176.mm,2354.mm,169.mm], [4176.mm,2410.mm,169.mm], [4164.mm,2410.mm,169.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X4230 Z150 far
  grp = ents.add_group
  grp.name = "FP wall bolt X4230 Z150 far"
  face = grp.entities.add_face([4224.mm,2354.mm,169.mm], [4236.mm,2354.mm,169.mm], [4236.mm,2410.mm,169.mm], [4224.mm,2410.mm,169.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall-tie strut X4200 Z2238 far
  grp = ents.add_group
  grp.name = "FP wall-tie strut X4200 Z2238 far"
  face = grp.entities.add_face([4178.mm,2262.mm,2238.mm], [4222.mm,2262.mm,2238.mm], [4222.mm,2362.mm,2238.mm], [4178.mm,2362.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP inside plate X4200 Z2238 far
  grp = ents.add_group
  grp.name = "FP inside plate X4200 Z2238 far"
  face = grp.entities.add_face([4150.mm,2354.mm,2218.mm], [4250.mm,2354.mm,2218.mm], [4250.mm,2362.mm,2218.mm], [4150.mm,2362.mm,2218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP OUTSIDE plate X4200 Z2238 far
  grp = ents.add_group
  grp.name = "FP OUTSIDE plate X4200 Z2238 far"
  face = grp.entities.add_face([4150.mm,2402.mm,2218.mm], [4250.mm,2402.mm,2218.mm], [4250.mm,2410.mm,2218.mm], [4150.mm,2410.mm,2218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X4170 Z2238 far
  grp = ents.add_group
  grp.name = "FP wall bolt X4170 Z2238 far"
  face = grp.entities.add_face([4164.mm,2354.mm,2257.mm], [4176.mm,2354.mm,2257.mm], [4176.mm,2410.mm,2257.mm], [4164.mm,2410.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP wall bolt X4230 Z2238 far
  grp = ents.add_group
  grp.name = "FP wall bolt X4230 Z2238 far"
  face = grp.entities.add_face([4224.mm,2354.mm,2257.mm], [4236.mm,2354.mm,2257.mm], [4236.mm,2410.mm,2257.mm], [4224.mm,2410.mm,2257.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Corner Mechanism"
  inst.layer = model.layers["Corner Mechanism"]

  # ═══ Walkways ═══
  defn = model.definitions.add("Walkways")
  ents = defn.entities
  # Walkway Near (left section)
  grp = ents.add_group
  grp.name = "Walkway Near (left section)"
  face = grp.entities.add_face([470.mm,0.mm,115.mm], [1155.mm,0.mm,115.mm], [1155.mm,300.mm,115.mm], [470.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near (widened)
  grp = ents.add_group
  grp.name = "Walkway Near (widened)"
  face = grp.entities.add_face([1155.mm,0.mm,115.mm], [2629.mm,0.mm,115.mm], [2629.mm,500.mm,115.mm], [1155.mm,500.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near (right section)
  grp = ents.add_group
  grp.name = "Walkway Near (right section)"
  face = grp.entities.add_face([2629.mm,0.mm,115.mm], [4329.mm,0.mm,115.mm], [4329.mm,300.mm,115.mm], [2629.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far
  grp = ents.add_group
  grp.name = "Walkway Far"
  face = grp.entities.add_face([470.mm,2062.mm,115.mm], [4329.mm,2062.mm,115.mm], [4329.mm,2362.mm,115.mm], [470.mm,2362.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Right (IBC end)
  grp = ents.add_group
  grp.name = "Walkway Right (IBC end)"
  face = grp.entities.add_face([4329.mm,0.mm,115.mm], [4629.mm,0.mm,115.mm], [4629.mm,2362.mm,115.mm], [4329.mm,2362.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (left section)"] || model.materials.add("Walkway Near (left section)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Left (REMOVABLE — transport)
  grp = ents.add_group
  grp.name = "Walkway Left (REMOVABLE — transport)"
  face = grp.entities.add_face([170.mm,0.mm,115.mm], [470.mm,0.mm,115.mm], [470.mm,2362.mm,115.mm], [170.mm,2362.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Left (REMOVABLE — transport)"] || model.materials.add("Walkway Left (REMOVABLE — transport)")
  mat.color = Sketchup::Color.new(192, 96, 0)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Left punch-out (drum exit)
  grp = ents.add_group
  grp.name = "Walkway Left punch-out (drum exit)"
  face = grp.entities.add_face([470.mm,800.mm,115.mm], [770.mm,800.mm,115.mm], [770.mm,1560.mm,115.mm], [470.mm,1560.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Left (REMOVABLE — transport)"] || model.materials.add("Walkway Left (REMOVABLE — transport)")
  mat.color = Sketchup::Color.new(192, 96, 0)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 1 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 plate"
  face = grp.entities.add_face([638.mm,0.mm,0.mm], [758.mm,0.mm,0.mm], [758.mm,8.mm,0.mm], [638.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([698.mm,-6.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([663.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([733.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 1 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 arm"
  face = grp.entities.add_face([694.mm,8.mm,105.mm], [702.mm,8.mm,105.mm], [702.mm,300.mm,105.mm], [694.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 1 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 gusset"
  ge = grp.entities
  f = ge.add_face([694.mm,8.mm,0.mm], [694.mm,8.mm,105.mm], [694.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) plate"
  face = grp.entities.add_face([1095.mm,0.mm,0.mm], [1215.mm,0.mm,0.mm], [1215.mm,10.mm,0.mm], [1095.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1120.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1190.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1120.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1190.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) arm"
  face = grp.entities.add_face([1150.mm,10.mm,103.mm], [1160.mm,10.mm,103.mm], [1160.mm,500.mm,103.mm], [1150.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 2 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([1150.mm,10.mm,0.mm], [1150.mm,10.mm,103.mm], [1150.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) plate"
  face = grp.entities.add_face([1552.mm,0.mm,0.mm], [1672.mm,0.mm,0.mm], [1672.mm,10.mm,0.mm], [1552.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1577.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1647.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1577.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1647.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) arm"
  face = grp.entities.add_face([1607.mm,10.mm,103.mm], [1617.mm,10.mm,103.mm], [1617.mm,500.mm,103.mm], [1607.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 3 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([1607.mm,10.mm,0.mm], [1607.mm,10.mm,103.mm], [1607.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) plate"
  face = grp.entities.add_face([2009.mm,0.mm,0.mm], [2129.mm,0.mm,0.mm], [2129.mm,10.mm,0.mm], [2009.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2034.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2104.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2034.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2104.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) arm"
  face = grp.entities.add_face([2064.mm,10.mm,103.mm], [2074.mm,10.mm,103.mm], [2074.mm,500.mm,103.mm], [2064.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 4 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([2064.mm,10.mm,0.mm], [2064.mm,10.mm,103.mm], [2064.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) plate"
  face = grp.entities.add_face([2466.mm,0.mm,0.mm], [2586.mm,0.mm,0.mm], [2586.mm,10.mm,0.mm], [2466.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2491.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2561.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2491.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2561.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) arm"
  face = grp.entities.add_face([2521.mm,10.mm,103.mm], [2531.mm,10.mm,103.mm], [2531.mm,500.mm,103.mm], [2521.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 5 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([2521.mm,10.mm,0.mm], [2521.mm,10.mm,103.mm], [2521.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 plate"
  face = grp.entities.add_face([2923.mm,0.mm,0.mm], [3043.mm,0.mm,0.mm], [3043.mm,8.mm,0.mm], [2923.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2983.mm,-6.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2948.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3018.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 arm"
  face = grp.entities.add_face([2979.mm,8.mm,105.mm], [2987.mm,8.mm,105.mm], [2987.mm,300.mm,105.mm], [2979.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 6 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 gusset"
  ge = grp.entities
  f = ge.add_face([2979.mm,8.mm,0.mm], [2979.mm,8.mm,105.mm], [2979.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 7 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 plate"
  face = grp.entities.add_face([3380.mm,0.mm,0.mm], [3500.mm,0.mm,0.mm], [3500.mm,8.mm,0.mm], [3380.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3440.mm,-6.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3405.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3475.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 7 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 arm"
  face = grp.entities.add_face([3436.mm,8.mm,105.mm], [3444.mm,8.mm,105.mm], [3444.mm,300.mm,105.mm], [3436.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 7 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 gusset"
  ge = grp.entities
  f = ge.add_face([3436.mm,8.mm,0.mm], [3436.mm,8.mm,105.mm], [3436.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 8 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 plate"
  face = grp.entities.add_face([3837.mm,0.mm,0.mm], [3957.mm,0.mm,0.mm], [3957.mm,8.mm,0.mm], [3837.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3897.mm,-6.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3862.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3932.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 8 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 arm"
  face = grp.entities.add_face([3893.mm,8.mm,105.mm], [3901.mm,8.mm,105.mm], [3901.mm,300.mm,105.mm], [3893.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Near bracket 8 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 gusset"
  ge = grp.entities
  f = ge.add_face([3893.mm,8.mm,0.mm], [3893.mm,8.mm,105.mm], [3893.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 1 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 plate"
  face = grp.entities.add_face([638.mm,2354.mm,0.mm], [758.mm,2354.mm,0.mm], [758.mm,2362.mm,0.mm], [638.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([698.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([663.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([733.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 1 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 arm"
  face = grp.entities.add_face([694.mm,2062.mm,105.mm], [702.mm,2062.mm,105.mm], [702.mm,2354.mm,105.mm], [694.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 1 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 gusset"
  ge = grp.entities
  f = ge.add_face([694.mm,2354.mm,0.mm], [694.mm,2354.mm,105.mm], [694.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 2 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 plate"
  face = grp.entities.add_face([1095.mm,2354.mm,0.mm], [1215.mm,2354.mm,0.mm], [1215.mm,2362.mm,0.mm], [1095.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 2 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1155.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 2 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1120.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 2 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1190.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 2 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 arm"
  face = grp.entities.add_face([1151.mm,2062.mm,105.mm], [1159.mm,2062.mm,105.mm], [1159.mm,2354.mm,105.mm], [1151.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 2 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 gusset"
  ge = grp.entities
  f = ge.add_face([1151.mm,2354.mm,0.mm], [1151.mm,2354.mm,105.mm], [1151.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 3 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 plate"
  face = grp.entities.add_face([1552.mm,2354.mm,0.mm], [1672.mm,2354.mm,0.mm], [1672.mm,2362.mm,0.mm], [1552.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 3 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1612.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 3 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1577.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 3 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1647.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 3 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 arm"
  face = grp.entities.add_face([1608.mm,2062.mm,105.mm], [1616.mm,2062.mm,105.mm], [1616.mm,2354.mm,105.mm], [1608.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 3 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 gusset"
  ge = grp.entities
  f = ge.add_face([1608.mm,2354.mm,0.mm], [1608.mm,2354.mm,105.mm], [1608.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 4 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 plate"
  face = grp.entities.add_face([2009.mm,2354.mm,0.mm], [2129.mm,2354.mm,0.mm], [2129.mm,2362.mm,0.mm], [2009.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 4 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2069.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 4 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2034.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 4 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2104.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 4 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 arm"
  face = grp.entities.add_face([2065.mm,2062.mm,105.mm], [2073.mm,2062.mm,105.mm], [2073.mm,2354.mm,105.mm], [2065.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 4 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 gusset"
  ge = grp.entities
  f = ge.add_face([2065.mm,2354.mm,0.mm], [2065.mm,2354.mm,105.mm], [2065.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 5 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 plate"
  face = grp.entities.add_face([2466.mm,2354.mm,0.mm], [2586.mm,2354.mm,0.mm], [2586.mm,2362.mm,0.mm], [2466.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 5 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2526.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 5 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2491.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 5 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2561.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 5 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 arm"
  face = grp.entities.add_face([2522.mm,2062.mm,105.mm], [2530.mm,2062.mm,105.mm], [2530.mm,2354.mm,105.mm], [2522.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 5 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 gusset"
  ge = grp.entities
  f = ge.add_face([2522.mm,2354.mm,0.mm], [2522.mm,2354.mm,105.mm], [2522.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 6 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 plate"
  face = grp.entities.add_face([2923.mm,2354.mm,0.mm], [3043.mm,2354.mm,0.mm], [3043.mm,2362.mm,0.mm], [2923.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 6 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2983.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 6 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2948.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 6 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3018.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 6 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 arm"
  face = grp.entities.add_face([2979.mm,2062.mm,105.mm], [2987.mm,2062.mm,105.mm], [2987.mm,2354.mm,105.mm], [2979.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 6 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 gusset"
  ge = grp.entities
  f = ge.add_face([2979.mm,2354.mm,0.mm], [2979.mm,2354.mm,105.mm], [2979.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 7 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 plate"
  face = grp.entities.add_face([3380.mm,2354.mm,0.mm], [3500.mm,2354.mm,0.mm], [3500.mm,2362.mm,0.mm], [3380.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3440.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3405.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3475.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 7 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 arm"
  face = grp.entities.add_face([3436.mm,2062.mm,105.mm], [3444.mm,2062.mm,105.mm], [3444.mm,2354.mm,105.mm], [3436.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 7 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 gusset"
  ge = grp.entities
  f = ge.add_face([3436.mm,2354.mm,0.mm], [3436.mm,2354.mm,105.mm], [3436.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 8 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 plate"
  face = grp.entities.add_face([3837.mm,2354.mm,0.mm], [3957.mm,2354.mm,0.mm], [3957.mm,2362.mm,0.mm], [3837.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3897.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3862.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3932.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(80, 80, 88)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 8 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 arm"
  face = grp.entities.add_face([3893.mm,2062.mm,105.mm], [3901.mm,2062.mm,105.mm], [3901.mm,2354.mm,105.mm], [3893.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far bracket 8 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 gusset"
  ge = grp.entities
  f = ge.add_face([3893.mm,2354.mm,0.mm], [3893.mm,2354.mm,105.mm], [3893.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 1 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 1 foot plate"
  face = grp.entities.add_face([38.mm,220.mm,0.mm], [166.mm,220.mm,0.mm], [166.mm,280.mm,0.mm], [38.mm,280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 1 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 1 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,220.mm,0.mm], [165.mm,220.mm,0.mm], [165.mm,280.mm,0.mm], [115.mm,280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 1 arm (to X470)
  grp = ents.add_group
  grp.name = "Left cantilever 1 arm (to X470)"
  face = grp.entities.add_face([165.mm,230.mm,75.mm], [470.mm,230.mm,75.mm], [470.mm,270.mm,75.mm], [165.mm,270.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 2 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 2 foot plate"
  face = grp.entities.add_face([38.mm,770.mm,0.mm], [166.mm,770.mm,0.mm], [166.mm,830.mm,0.mm], [38.mm,830.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 2 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 2 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,770.mm,0.mm], [165.mm,770.mm,0.mm], [165.mm,830.mm,0.mm], [115.mm,830.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 2 arm (to X770)
  grp = ents.add_group
  grp.name = "Left cantilever 2 arm (to X770)"
  face = grp.entities.add_face([165.mm,770.mm,75.mm], [770.mm,770.mm,75.mm], [770.mm,830.mm,75.mm], [165.mm,830.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 3 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 3 foot plate"
  face = grp.entities.add_face([38.mm,1150.mm,0.mm], [166.mm,1150.mm,0.mm], [166.mm,1210.mm,0.mm], [38.mm,1210.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 3 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 3 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,1150.mm,0.mm], [165.mm,1150.mm,0.mm], [165.mm,1210.mm,0.mm], [115.mm,1210.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 3 arm (to X770)
  grp = ents.add_group
  grp.name = "Left cantilever 3 arm (to X770)"
  face = grp.entities.add_face([165.mm,1150.mm,75.mm], [770.mm,1150.mm,75.mm], [770.mm,1210.mm,75.mm], [165.mm,1210.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 4 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 4 foot plate"
  face = grp.entities.add_face([38.mm,1530.mm,0.mm], [166.mm,1530.mm,0.mm], [166.mm,1590.mm,0.mm], [38.mm,1590.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 4 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 4 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,1530.mm,0.mm], [165.mm,1530.mm,0.mm], [165.mm,1590.mm,0.mm], [115.mm,1590.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 4 arm (to X770)
  grp = ents.add_group
  grp.name = "Left cantilever 4 arm (to X770)"
  face = grp.entities.add_face([165.mm,1530.mm,75.mm], [770.mm,1530.mm,75.mm], [770.mm,1590.mm,75.mm], [165.mm,1590.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 5 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 5 foot plate"
  face = grp.entities.add_face([38.mm,2080.mm,0.mm], [166.mm,2080.mm,0.mm], [166.mm,2140.mm,0.mm], [38.mm,2140.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 5 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 5 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,2080.mm,0.mm], [165.mm,2080.mm,0.mm], [165.mm,2140.mm,0.mm], [115.mm,2140.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left cantilever 5 arm (to X470)
  grp = ents.add_group
  grp.name = "Left cantilever 5 arm (to X470)"
  face = grp.entities.add_face([165.mm,2090.mm,75.mm], [470.mm,2090.mm,75.mm], [470.mm,2130.mm,75.mm], [165.mm,2130.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Walkways"
  inst.layer = model.layers["Walkways"]

  # ═══ Corner Detail (TR) ═══
  defn = model.definitions.add("Corner Detail (TR)")
  ents = defn.entities
  # Detail Rail TR
  grp = ents.add_group
  grp.name = "Detail Rail TR"
  face = grp.entities.add_face([4637.mm,100.mm,2280.mm], [4661.mm,100.mm,2280.mm], [4661.mm,2300.mm,2280.mm], [4637.mm,2300.mm,2280.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Detail Rail TR"] || model.materials.add("Detail Rail TR")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Detail Leadscrew TR
  grp = ents.add_group
  grp.name = "Detail Leadscrew TR"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 2200.mm, 0.mm)
  circle = ge.add_circle([4683.mm,100.mm,2288.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Detail Carriage TR
  grp = ents.add_group
  grp.name = "Detail Carriage TR"
  face = grp.entities.add_face([4623.mm,1378.0520922298629.mm,2270.mm], [4675.mm,1378.0520922298629.mm,2270.mm], [4675.mm,1442.0520922298629.mm,2270.mm], [4623.mm,1442.0520922298629.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Detail Drive Nut TR
  grp = ents.add_group
  grp.name = "Detail Drive Nut TR"
  face = grp.entities.add_face([4669.mm,1396.0520922298629.mm,2276.mm], [4697.mm,1396.0520922298629.mm,2276.mm], [4697.mm,1424.0520922298629.mm,2276.mm], [4669.mm,1424.0520922298629.mm,2276.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Detail X cross-slide TR (SWING)
  grp = ents.add_group
  grp.name = "Detail X cross-slide TR (SWING)"
  face = grp.entities.add_face([4633.mm,1394.0520922298629.mm,2294.mm], [4682.979444694831.mm,1394.0520922298629.mm,2294.mm], [4682.979444694831.mm,1426.0520922298629.mm,2294.mm], [4633.mm,1426.0520922298629.mm,2294.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Detail X cross-slide TR (SWING)"] || model.materials.add("Detail X cross-slide TR (SWING)")
  mat.color = Sketchup::Color.new(31, 119, 180)
  mat.alpha = 1.0
  grp.material = mat

  # Detail X slider TR
  grp = ents.add_group
  grp.name = "Detail X slider TR"
  face = grp.entities.add_face([4650.979444694831.mm,1390.0520922298629.mm,2292.mm], [4682.979444694831.mm,1390.0520922298629.mm,2292.mm], [4682.979444694831.mm,1430.0520922298629.mm,2292.mm], [4650.979444694831.mm,1430.0520922298629.mm,2292.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Detail Z cross-slide TR (TILT)
  grp = ents.add_group
  grp.name = "Detail Z cross-slide TR (TILT)"
  face = grp.entities.add_face([4657.979444694831.mm,1395.0520922298629.mm,2207.531411620136.mm], [4675.979444694831.mm,1395.0520922298629.mm,2207.531411620136.mm], [4675.979444694831.mm,1425.0520922298629.mm,2207.531411620136.mm], [4657.979444694831.mm,1425.0520922298629.mm,2207.531411620136.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(96.46858837986383.mm)
  mat = model.materials["Detail Z cross-slide TR (TILT)"] || model.materials.add("Detail Z cross-slide TR (TILT)")
  mat.color = Sketchup::Color.new(44, 160, 44)
  mat.alpha = 1.0
  grp.material = mat

  # Detail Z slider TR
  grp = ents.add_group
  grp.name = "Detail Z slider TR"
  face = grp.entities.add_face([4653.979444694831.mm,1392.0520922298629.mm,2207.531411620136.mm], [4679.979444694831.mm,1392.0520922298629.mm,2207.531411620136.mm], [4679.979444694831.mm,1428.0520922298629.mm,2207.531411620136.mm], [4653.979444694831.mm,1428.0520922298629.mm,2207.531411620136.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Detail Rod-End TR
  grp = ents.add_group
  grp.name = "Detail Rod-End TR"
  face = grp.entities.add_face([4649.979444694831.mm,1393.0520922298629.mm,2206.531411620136.mm], [4683.979444694831.mm,1393.0520922298629.mm,2206.531411620136.mm], [4683.979444694831.mm,1427.0520922298629.mm,2206.531411620136.mm], [4649.979444694831.mm,1427.0520922298629.mm,2206.531411620136.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(34.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Detail Flat-corner ghost TR
  grp = ents.add_group
  grp.name = "Detail Flat-corner ghost TR"
  face = grp.entities.add_face([4636.mm,1397.0520922298629.mm,2275.mm], [4662.mm,1397.0520922298629.mm,2275.mm], [4662.mm,1423.0520922298629.mm,2275.mm], [4636.mm,1423.0520922298629.mm,2275.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Detail Flat-corner ghost TR"] || model.materials.add("Detail Flat-corner ghost TR")
  mat.color = Sketchup::Color.new(154, 166, 178)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Corner Detail (TR)"
  inst.layer = model.layers["Corner Detail"]


# ── Film Plane (Dynamic Component — click to tilt+swing) ──

# ═══ Film Plane — DYNAMIC COMPONENT (click to tilt+swing) ═══
fp_defn = model.definitions.add("Film Plane")
ents = fp_defn.entities
  # Film Plane Screen (muslin)
  grp = ents.add_group
  grp.name = "Film Plane Screen (muslin)"
  face = grp.entities.add_face([-2249.5.mm,-6.mm,-1069.mm], [2249.5.mm,-6.mm,-1069.mm], [2249.5.mm,6.mm,-1069.mm], [-2249.5.mm,6.mm,-1069.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2138.mm)
  mat = model.materials["Film Plane Screen (muslin)"] || model.materials.add("Film Plane Screen (muslin)")
  mat.color = Sketchup::Color.new(32, 96, 160)
  mat.alpha = 0.3
  grp.material = mat

  # FP Frame Top
  grp = ents.add_group
  grp.name = "FP Frame Top"
  ge = grp.entities
  vec = Geom::Vector3d.new(4499.mm, 0.mm, 0.mm)
  circle = ge.add_circle([-2249.5.mm,0.mm,1069.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Frame Bottom
  grp = ents.add_group
  grp.name = "FP Frame Bottom"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4499.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2249.5.mm,0.mm,-1069.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Frame Left
  grp = ents.add_group
  grp.name = "FP Frame Left"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -2138.mm)
  circle = ge.add_circle([-2249.5.mm,0.mm,1069.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Frame Right
  grp = ents.add_group
  grp.name = "FP Frame Right"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -2138.mm)
  circle = ge.add_circle([2249.5.mm,0.mm,1069.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage TL (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage TL (HGH20CA)"
  face = grp.entities.add_face([-2275.5.mm,-32.mm,1057.mm], [-2223.5.mm,-32.mm,1057.mm], [-2223.5.mm,32.mm,1057.mm], [-2275.5.mm,32.mm,1057.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Drive Nut TL
  grp = ents.add_group
  grp.name = "Drive Nut TL"
  face = grp.entities.add_face([-2229.5.mm,-14.mm,1056.mm], [-2201.5.mm,-14.mm,1056.mm], [-2201.5.mm,14.mm,1056.mm], [-2229.5.mm,14.mm,1056.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Rod-End TL
  grp = ents.add_group
  grp.name = "Rod-End TL"
  face = grp.entities.add_face([-2265.5.mm,-16.mm,1053.mm], [-2233.5.mm,-16.mm,1053.mm], [-2233.5.mm,16.mm,1053.mm], [-2265.5.mm,16.mm,1053.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage TR (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage TR (HGH20CA)"
  face = grp.entities.add_face([2223.5.mm,-32.mm,1057.mm], [2275.5.mm,-32.mm,1057.mm], [2275.5.mm,32.mm,1057.mm], [2223.5.mm,32.mm,1057.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Drive Nut TR
  grp = ents.add_group
  grp.name = "Drive Nut TR"
  face = grp.entities.add_face([2269.5.mm,-14.mm,1056.mm], [2297.5.mm,-14.mm,1056.mm], [2297.5.mm,14.mm,1056.mm], [2269.5.mm,14.mm,1056.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Rod-End TR
  grp = ents.add_group
  grp.name = "Rod-End TR"
  face = grp.entities.add_face([2233.5.mm,-16.mm,1053.mm], [2265.5.mm,-16.mm,1053.mm], [2265.5.mm,16.mm,1053.mm], [2233.5.mm,16.mm,1053.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage BL (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage BL (HGH20CA)"
  face = grp.entities.add_face([-2275.5.mm,-32.mm,-1081.mm], [-2223.5.mm,-32.mm,-1081.mm], [-2223.5.mm,32.mm,-1081.mm], [-2275.5.mm,32.mm,-1081.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Drive Nut BL
  grp = ents.add_group
  grp.name = "Drive Nut BL"
  face = grp.entities.add_face([-2229.5.mm,-14.mm,-1082.mm], [-2201.5.mm,-14.mm,-1082.mm], [-2201.5.mm,14.mm,-1082.mm], [-2229.5.mm,14.mm,-1082.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Rod-End BL
  grp = ents.add_group
  grp.name = "Rod-End BL"
  face = grp.entities.add_face([-2265.5.mm,-16.mm,-1085.mm], [-2233.5.mm,-16.mm,-1085.mm], [-2233.5.mm,16.mm,-1085.mm], [-2265.5.mm,16.mm,-1085.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage BR (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage BR (HGH20CA)"
  face = grp.entities.add_face([2223.5.mm,-32.mm,-1081.mm], [2275.5.mm,-32.mm,-1081.mm], [2275.5.mm,32.mm,-1081.mm], [2223.5.mm,32.mm,-1081.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Drive Nut BR
  grp = ents.add_group
  grp.name = "Drive Nut BR"
  face = grp.entities.add_face([2269.5.mm,-14.mm,-1082.mm], [2297.5.mm,-14.mm,-1082.mm], [2297.5.mm,14.mm,-1082.mm], [2269.5.mm,14.mm,-1082.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Rod-End BR
  grp = ents.add_group
  grp.name = "Rod-End BR"
  face = grp.entities.add_face([2233.5.mm,-16.mm,-1085.mm], [2265.5.mm,-16.mm,-1085.mm], [2265.5.mm,16.mm,-1085.mm], [2233.5.mm,16.mm,-1085.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

fp_inst = entities.add_instance(fp_defn, Geom::Transformation.translation([2399.5.mm, 1181.mm, 1219.mm]))
fp_inst.name = "Film Plane"
fp_inst.layer = model.layers["Film Plane"]
fda = "dynamic_attributes"
[fp_defn, fp_inst].each do |e|
  e.set_attribute(fda, "_name", "FilmPlane")
  e.set_attribute(fda, "_lengthunits", "MILLIMETERS")
  e.set_attribute(fda, "pose", 0.0)
  e.set_attribute(fda, "rotx", 0.0)
  e.set_attribute(fda, "rotz", 0.0)
end
fp_inst.set_attribute(fda, "_pose_access", "VIEW")
fp_inst.set_attribute(fda, "_pose_label", "Pose (0 flat / 1 tilt+swing)")
fp_inst.set_attribute(fda, "_rotx_formula", "20.0*pose")
fp_inst.set_attribute(fda, "_rotz_formula", "15.0*pose")
fp_inst.set_attribute(fda, "onclick", 'ANIMATE("pose", 0, 1)')
fp_inst.set_attribute(fda, "_onclick_access", "NONE")


# ── Corner-detail callouts (Labels tag — shown only in the corner-detail scene) ──
t=entities.add_text("HGR20 rail - FIXED (depth guide)", Geom::Point3d.new(4649.mm,1160.0520922298629.mm,2288.mm), Geom::Vector3d.new(10,0,11.0)); t.layer=model.layers["Labels"] rescue nil
t=entities.add_text("Leadscrew - DEPTH / focus drive", Geom::Point3d.new(4683.mm,710.0520922298629.mm,2288.mm), Geom::Vector3d.new(4.0,0,19.0)); t.layer=model.layers["Labels"] rescue nil
t=entities.add_text("Carriage + drive nut", Geom::Point3d.new(4629.mm,1410.0520922298629.mm,2276.mm), Geom::Vector3d.new(-10.0,0,-15.0)); t.layer=model.layers["Labels"] rescue nil
t=entities.add_text("X cross-slide = SWING float (blue)", Geom::Point3d.new(4657.989722347415.mm,1410.0520922298629.mm,2302.mm), Geom::Vector3d.new(-12.0,0,4.0)); t.layer=model.layers["Labels"] rescue nil
t=entities.add_text("Z cross-slide = TILT float (green)", Geom::Point3d.new(4666.979444694831.mm,1410.0520922298629.mm,2255.765705810068.mm), Geom::Vector3d.new(17.0,0,-12.0)); t.layer=model.layers["Labels"] rescue nil
t=entities.add_text("Rod-end -> rigid frame corner", Geom::Point3d.new(4666.979444694831.mm,1410.0520922298629.mm,2223.531411620136.mm), Geom::Vector3d.new(17.0,0,5.0)); t.layer=model.layers["Labels"] rescue nil
t=entities.add_text("ghost = corner if it stayed on rail", Geom::Point3d.new(4649.mm,1410.0520922298629.mm,2288.mm), Geom::Vector3d.new(-17.0,0,13.0)); t.layer=model.layers["Labels"] rescue nil

# ── In-model © + license credit (default layer → shown in every scene) ──
lbb = model.bounds
lanc = Geom::Point3d.new(lbb.min.x, lbb.min.y - 400.mm, lbb.min.z)
entities.add_text("© 2026 Alvin Richards
Licensed under GNU AGPLv3
alvinr.github.io/tbs", lanc)

model.definitions.purge_unused
model.materials.purge_unused
keep_tags = ["Context", "Film Plane", "Corner Mechanism", "Processing Tray", "Walkways", "Corner Detail", "Labels"]; dl = model.layers[0]
model.layers.to_a.each { |l| next if l==dl||keep_tags.include?(l.name); model.layers.remove(l,true) rescue nil }

model.layers.each { |l| l.visible = true }
bb = model.bounds; ctr = bb.center
dir = Geom::Vector3d.new(0.6, -0.74, 0.42); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.4)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

[["Combined", ["Context", "Film Plane", "Corner Mechanism", "Processing Tray", "Walkways"], nil, 0], ["No Container", ["Film Plane", "Corner Mechanism", "Processing Tray"], nil, 0], ["Corner detail (TR)", ["Corner Detail", "Labels"], [4666.979444694831.mm, 1410.0520922298629.mm, 2223.531411620136.mm], 95]].each { |name, tags, tgt, so|
  model.layers.each { |l| l.visible = (l == dl || tags.include?(l.name)) }
  if tgt
    t = Geom::Point3d.new(tgt[0], tgt[1], tgt[2])
    cam = Sketchup::Camera.new(t.offset(dir, so), t, Z_AXIS); cam.fov = 35
    model.active_view.camera = cam
  else
    model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
    model.active_view.zoom_extents
  end
  page = model.pages.add(name); page.use_camera = true
}
model.layers.each { |l| l.visible = true }
model.layers["Corner Detail"].visible = false
model.layers["Labels"].visible = false

model.commit_operation

# Register the DC AFTER committing (redraw_with_undo opens its own operation).
if defined?($dc_observers) && $dc_observers.respond_to?(:get_latest_class)
  cls = $dc_observers.get_latest_class
  cls.redraw_with_undo(fp_inst) rescue nil if cls
end

{ success: true, model: "film-plane", scenes: model.pages.count,
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tilt: 20.0, swing: 15.0 }.to_json
