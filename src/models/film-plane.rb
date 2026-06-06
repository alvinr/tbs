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
  face = grp.entities.add_face([138.mm,100.mm,92.mm], [162.mm,100.mm,92.mm], [162.mm,2300.mm,92.mm], [138.mm,2300.mm,92.mm])
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
  circle = ge.add_circle([184.mm,100.mm,100.mm], vec, 7.mm, 16)
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
  face = grp.entities.add_face([4637.mm,100.mm,92.mm], [4661.mm,100.mm,92.mm], [4661.mm,2300.mm,92.mm], [4637.mm,2300.mm,92.mm])
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
  circle = ge.add_circle([4683.mm,100.mm,100.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Corner Mechanism"
  inst.layer = model.layers["Corner Mechanism"]

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
  face = grp.entities.add_face([4623.mm,1369.792939991129.mm,2270.mm], [4675.mm,1369.792939991129.mm,2270.mm], [4675.mm,1433.792939991129.mm,2270.mm], [4623.mm,1433.792939991129.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Detail Drive Nut TR
  grp = ents.add_group
  grp.name = "Detail Drive Nut TR"
  face = grp.entities.add_face([4669.mm,1387.792939991129.mm,2276.mm], [4697.mm,1387.792939991129.mm,2276.mm], [4697.mm,1415.792939991129.mm,2276.mm], [4669.mm,1415.792939991129.mm,2276.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Detail X cross-slide TR (SWING)
  grp = ents.add_group
  grp.name = "Detail X cross-slide TR (SWING)"
  face = grp.entities.add_face([4633.mm,1385.792939991129.mm,2294.mm], [4685.192477867366.mm,1385.792939991129.mm,2294.mm], [4685.192477867366.mm,1417.792939991129.mm,2294.mm], [4633.mm,1417.792939991129.mm,2294.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["Detail X cross-slide TR (SWING)"] || model.materials.add("Detail X cross-slide TR (SWING)")
  mat.color = Sketchup::Color.new(31, 119, 180)
  mat.alpha = 1.0
  grp.material = mat

  # Detail X slider TR
  grp = ents.add_group
  grp.name = "Detail X slider TR"
  face = grp.entities.add_face([4653.192477867366.mm,1381.792939991129.mm,2292.mm], [4685.192477867366.mm,1381.792939991129.mm,2292.mm], [4685.192477867366.mm,1421.792939991129.mm,2292.mm], [4653.192477867366.mm,1421.792939991129.mm,2292.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Detail Z cross-slide TR (TILT)
  grp = ents.add_group
  grp.name = "Detail Z cross-slide TR (TILT)"
  face = grp.entities.add_face([4660.192477867366.mm,1386.792939991129.mm,2206.0237271397837.mm], [4678.192477867366.mm,1386.792939991129.mm,2206.0237271397837.mm], [4678.192477867366.mm,1416.792939991129.mm,2206.0237271397837.mm], [4660.192477867366.mm,1416.792939991129.mm,2206.0237271397837.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(97.97627286021634.mm)
  mat = model.materials["Detail Z cross-slide TR (TILT)"] || model.materials.add("Detail Z cross-slide TR (TILT)")
  mat.color = Sketchup::Color.new(44, 160, 44)
  mat.alpha = 1.0
  grp.material = mat

  # Detail Z slider TR
  grp = ents.add_group
  grp.name = "Detail Z slider TR"
  face = grp.entities.add_face([4656.192477867366.mm,1383.792939991129.mm,2206.0237271397837.mm], [4682.192477867366.mm,1383.792939991129.mm,2206.0237271397837.mm], [4682.192477867366.mm,1419.792939991129.mm,2206.0237271397837.mm], [4656.192477867366.mm,1419.792939991129.mm,2206.0237271397837.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Detail Rod-End TR
  grp = ents.add_group
  grp.name = "Detail Rod-End TR"
  face = grp.entities.add_face([4652.192477867366.mm,1384.792939991129.mm,2205.0237271397837.mm], [4686.192477867366.mm,1384.792939991129.mm,2205.0237271397837.mm], [4686.192477867366.mm,1418.792939991129.mm,2205.0237271397837.mm], [4652.192477867366.mm,1418.792939991129.mm,2205.0237271397837.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(34.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Detail Flat-corner ghost TR
  grp = ents.add_group
  grp.name = "Detail Flat-corner ghost TR"
  face = grp.entities.add_face([4636.mm,1388.792939991129.mm,2275.mm], [4662.mm,1388.792939991129.mm,2275.mm], [4662.mm,1414.792939991129.mm,2275.mm], [4636.mm,1414.792939991129.mm,2275.mm])
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
  face = grp.entities.add_face([-2249.5.mm,-6.mm,-1094.mm], [2249.5.mm,-6.mm,-1094.mm], [2249.5.mm,6.mm,-1094.mm], [-2249.5.mm,6.mm,-1094.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2188.mm)
  mat = model.materials["Film Plane Screen (muslin)"] || model.materials.add("Film Plane Screen (muslin)")
  mat.color = Sketchup::Color.new(32, 96, 160)
  mat.alpha = 0.3
  grp.material = mat

  # FP Frame Top
  grp = ents.add_group
  grp.name = "FP Frame Top"
  ge = grp.entities
  vec = Geom::Vector3d.new(4499.mm, 0.mm, 0.mm)
  circle = ge.add_circle([-2249.5.mm,0.mm,1094.mm], vec, 25.4.mm, 16)
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
  circle = ge.add_circle([2249.5.mm,0.mm,-1094.mm], vec, 25.4.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -2188.mm)
  circle = ge.add_circle([-2249.5.mm,0.mm,1094.mm], vec, 25.4.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -2188.mm)
  circle = ge.add_circle([2249.5.mm,0.mm,1094.mm], vec, 25.4.mm, 16)
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
  face = grp.entities.add_face([-2275.5.mm,-32.mm,1082.mm], [-2223.5.mm,-32.mm,1082.mm], [-2223.5.mm,32.mm,1082.mm], [-2275.5.mm,32.mm,1082.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Drive Nut TL
  grp = ents.add_group
  grp.name = "Drive Nut TL"
  face = grp.entities.add_face([-2229.5.mm,-14.mm,1081.mm], [-2201.5.mm,-14.mm,1081.mm], [-2201.5.mm,14.mm,1081.mm], [-2229.5.mm,14.mm,1081.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Rod-End TL
  grp = ents.add_group
  grp.name = "Rod-End TL"
  face = grp.entities.add_face([-2265.5.mm,-16.mm,1078.mm], [-2233.5.mm,-16.mm,1078.mm], [-2233.5.mm,16.mm,1078.mm], [-2265.5.mm,16.mm,1078.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage TR (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage TR (HGH20CA)"
  face = grp.entities.add_face([2223.5.mm,-32.mm,1082.mm], [2275.5.mm,-32.mm,1082.mm], [2275.5.mm,32.mm,1082.mm], [2223.5.mm,32.mm,1082.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Drive Nut TR
  grp = ents.add_group
  grp.name = "Drive Nut TR"
  face = grp.entities.add_face([2269.5.mm,-14.mm,1081.mm], [2297.5.mm,-14.mm,1081.mm], [2297.5.mm,14.mm,1081.mm], [2269.5.mm,14.mm,1081.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Rod-End TR
  grp = ents.add_group
  grp.name = "Rod-End TR"
  face = grp.entities.add_face([2233.5.mm,-16.mm,1078.mm], [2265.5.mm,-16.mm,1078.mm], [2265.5.mm,16.mm,1078.mm], [2233.5.mm,16.mm,1078.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage BL (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage BL (HGH20CA)"
  face = grp.entities.add_face([-2275.5.mm,-32.mm,-1106.mm], [-2223.5.mm,-32.mm,-1106.mm], [-2223.5.mm,32.mm,-1106.mm], [-2275.5.mm,32.mm,-1106.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Drive Nut BL
  grp = ents.add_group
  grp.name = "Drive Nut BL"
  face = grp.entities.add_face([-2229.5.mm,-14.mm,-1107.mm], [-2201.5.mm,-14.mm,-1107.mm], [-2201.5.mm,14.mm,-1107.mm], [-2229.5.mm,14.mm,-1107.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Rod-End BL
  grp = ents.add_group
  grp.name = "Rod-End BL"
  face = grp.entities.add_face([-2265.5.mm,-16.mm,-1110.mm], [-2233.5.mm,-16.mm,-1110.mm], [-2233.5.mm,16.mm,-1110.mm], [-2265.5.mm,16.mm,-1110.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage BR (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage BR (HGH20CA)"
  face = grp.entities.add_face([2223.5.mm,-32.mm,-1106.mm], [2275.5.mm,-32.mm,-1106.mm], [2275.5.mm,32.mm,-1106.mm], [2223.5.mm,32.mm,-1106.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Drive Nut BR
  grp = ents.add_group
  grp.name = "Drive Nut BR"
  face = grp.entities.add_face([2269.5.mm,-14.mm,-1107.mm], [2297.5.mm,-14.mm,-1107.mm], [2297.5.mm,14.mm,-1107.mm], [2269.5.mm,14.mm,-1107.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Detail Carriage TR"] || model.materials.add("Detail Carriage TR")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Rod-End BR
  grp = ents.add_group
  grp.name = "Rod-End BR"
  face = grp.entities.add_face([2233.5.mm,-16.mm,-1110.mm], [2265.5.mm,-16.mm,-1110.mm], [2265.5.mm,16.mm,-1110.mm], [2233.5.mm,16.mm,-1110.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Detail Leadscrew TR"] || model.materials.add("Detail Leadscrew TR")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

fp_inst = entities.add_instance(fp_defn, Geom::Transformation.translation([2399.5.mm, 1181.mm, 1194.mm]))
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
t=entities.add_text("HGR20 rail - FIXED (depth guide)", Geom::Point3d.new(4649.mm,1151.792939991129.mm,2288.mm), Geom::Vector3d.new(10,0,11.0)); t.layer=model.layers["Labels"] rescue nil
t=entities.add_text("Leadscrew - DEPTH / focus drive", Geom::Point3d.new(4683.mm,701.7929399911291.mm,2288.mm), Geom::Vector3d.new(4.0,0,19.0)); t.layer=model.layers["Labels"] rescue nil
t=entities.add_text("Carriage + drive nut", Geom::Point3d.new(4629.mm,1401.792939991129.mm,2276.mm), Geom::Vector3d.new(-10.0,0,-15.0)); t.layer=model.layers["Labels"] rescue nil
t=entities.add_text("X cross-slide = SWING float (blue)", Geom::Point3d.new(4659.096238933683.mm,1401.792939991129.mm,2302.mm), Geom::Vector3d.new(-12.0,0,4.0)); t.layer=model.layers["Labels"] rescue nil
t=entities.add_text("Z cross-slide = TILT float (green)", Geom::Point3d.new(4669.192477867366.mm,1401.792939991129.mm,2255.011863569892.mm), Geom::Vector3d.new(17.0,0,-12.0)); t.layer=model.layers["Labels"] rescue nil
t=entities.add_text("Rod-end -> rigid frame corner", Geom::Point3d.new(4669.192477867366.mm,1401.792939991129.mm,2222.0237271397837.mm), Geom::Vector3d.new(17.0,0,5.0)); t.layer=model.layers["Labels"] rescue nil
t=entities.add_text("ghost = corner if it stayed on rail", Geom::Point3d.new(4649.mm,1401.792939991129.mm,2288.mm), Geom::Vector3d.new(-17.0,0,13.0)); t.layer=model.layers["Labels"] rescue nil

model.definitions.purge_unused
model.materials.purge_unused
keep_tags = ["Context", "Film Plane", "Corner Mechanism", "Processing Tray", "Corner Detail", "Labels"]; dl = model.layers[0]
model.layers.to_a.each { |l| next if l==dl||keep_tags.include?(l.name); model.layers.remove(l,true) rescue nil }

model.layers.each { |l| l.visible = true }
bb = model.bounds; ctr = bb.center
dir = Geom::Vector3d.new(0.6, -0.74, 0.42); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.4)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

[["Combined", ["Context", "Film Plane", "Corner Mechanism", "Processing Tray"], nil, 0], ["No Container", ["Film Plane", "Corner Mechanism", "Processing Tray"], nil, 0], ["Corner detail (TR)", ["Corner Detail", "Labels"], [4669.192477867366.mm, 1401.792939991129.mm, 2222.0237271397837.mm], 95]].each { |name, tags, tgt, so|
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
