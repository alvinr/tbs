model = Sketchup.active_model
model.start_operation("TBS-001 Film Plane", true)
entities = model.active_entities

# Display in millimeters (UI readout only).
opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# ── Idempotent rebuild: erase all prior groups/instances so the model frames
# tightly on the film-plane assembly. ──
to_erase = entities.to_a.select { |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance)
}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each { |p| model.pages.erase(p) }

# ── Tags (layers) ──
  model.layers.add("Context") unless model.layers["Context"]
  model.layers.add("Film Plane") unless model.layers["Film Plane"]
  model.layers.add("Corner Mechanism") unless model.layers["Corner Mechanism"]
  model.layers.add("Processing Tray") unless model.layers["Processing Tray"]

# ── Subsystems (each a component on its tag) ──
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
  mat = model.materials["HGR20 Rail TL"] || model.materials.add("HGR20 Rail TL")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Leadscrew TL
  grp = ents.add_group
  grp.name = "Leadscrew TL"
  ge = grp.entities
  circle = ge.add_circle([176.mm,100.mm,2288.mm], [0,1,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(2200.mm)
  mat = model.materials["Leadscrew TL"] || model.materials.add("Leadscrew TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Drive Nut TL
  grp = ents.add_group
  grp.name = "Drive Nut TL"
  face = grp.entities.add_face([165.mm,2251.mm,2277.mm], [187.mm,2251.mm,2277.mm], [187.mm,2273.mm,2277.mm], [165.mm,2273.mm,2277.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Drive Nut TL"] || model.materials.add("Drive Nut TL")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage TL (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage TL (HGH20CA)"
  face = grp.entities.add_face([128.mm,2240.mm,2274.mm], [172.mm,2240.mm,2274.mm], [172.mm,2284.mm,2274.mm], [128.mm,2284.mm,2274.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Drive Nut TL"] || model.materials.add("Drive Nut TL")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Corner Bracket TL
  grp = ents.add_group
  grp.name = "Corner Bracket TL"
  face = grp.entities.add_face([142.mm,2232.mm,2288.mm], [158.mm,2232.mm,2288.mm], [158.mm,2292.mm,2288.mm], [142.mm,2292.mm,2288.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Corner Bracket TL"] || model.materials.add("Corner Bracket TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.9
  grp.material = mat

  # UJoint Yoke TL
  grp = ents.add_group
  grp.name = "UJoint Yoke TL"
  face = grp.entities.add_face([136.mm,2246.mm,2324.mm], [164.mm,2246.mm,2324.mm], [164.mm,2252.mm,2324.mm], [136.mm,2252.mm,2324.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Leadscrew TL"] || model.materials.add("Leadscrew TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # UJoint Yoke TL
  grp = ents.add_group
  grp.name = "UJoint Yoke TL"
  face = grp.entities.add_face([136.mm,2272.mm,2324.mm], [164.mm,2272.mm,2324.mm], [164.mm,2278.mm,2324.mm], [136.mm,2278.mm,2324.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Leadscrew TL"] || model.materials.add("Leadscrew TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # UJoint Cross Pin TL
  grp = ents.add_group
  grp.name = "UJoint Cross Pin TL"
  ge = grp.entities
  circle = ge.add_circle([134.mm,2262.mm,2338.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(32.mm)
  mat = model.materials["UJoint Cross Pin TL"] || model.materials.add("UJoint Cross Pin TL")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # UJoint Spider TL
  grp = ents.add_group
  grp.name = "UJoint Spider TL"
  ge = grp.entities
  circle = ge.add_circle([150.mm,2262.mm,2338.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(1.mm)
  mat = model.materials["UJoint Cross Pin TL"] || model.materials.add("UJoint Cross Pin TL")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # UJoint Link TL
  grp = ents.add_group
  grp.name = "UJoint Link TL"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 50.mm)
  circle = ge.add_circle([150.mm,2262.mm,2338.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Leadscrew TL"] || model.materials.add("Leadscrew TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # HGR20 Rail TR
  grp = ents.add_group
  grp.name = "HGR20 Rail TR"
  face = grp.entities.add_face([4637.mm,100.mm,2280.mm], [4661.mm,100.mm,2280.mm], [4661.mm,2300.mm,2280.mm], [4637.mm,2300.mm,2280.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["HGR20 Rail TL"] || model.materials.add("HGR20 Rail TL")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Leadscrew TR
  grp = ents.add_group
  grp.name = "Leadscrew TR"
  ge = grp.entities
  circle = ge.add_circle([4675.mm,100.mm,2288.mm], [0,1,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(2200.mm)
  mat = model.materials["Leadscrew TL"] || model.materials.add("Leadscrew TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Drive Nut TR
  grp = ents.add_group
  grp.name = "Drive Nut TR"
  face = grp.entities.add_face([4664.mm,1951.mm,2277.mm], [4686.mm,1951.mm,2277.mm], [4686.mm,1973.mm,2277.mm], [4664.mm,1973.mm,2277.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Drive Nut TL"] || model.materials.add("Drive Nut TL")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage TR (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage TR (HGH20CA)"
  face = grp.entities.add_face([4627.mm,1940.mm,2274.mm], [4671.mm,1940.mm,2274.mm], [4671.mm,1984.mm,2274.mm], [4627.mm,1984.mm,2274.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Drive Nut TL"] || model.materials.add("Drive Nut TL")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Corner Bracket TR
  grp = ents.add_group
  grp.name = "Corner Bracket TR"
  face = grp.entities.add_face([4641.mm,1932.mm,2288.mm], [4657.mm,1932.mm,2288.mm], [4657.mm,1992.mm,2288.mm], [4641.mm,1992.mm,2288.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Corner Bracket TL"] || model.materials.add("Corner Bracket TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.9
  grp.material = mat

  # UJoint Yoke TR
  grp = ents.add_group
  grp.name = "UJoint Yoke TR"
  face = grp.entities.add_face([4635.mm,1946.mm,2324.mm], [4663.mm,1946.mm,2324.mm], [4663.mm,1952.mm,2324.mm], [4635.mm,1952.mm,2324.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Leadscrew TL"] || model.materials.add("Leadscrew TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # UJoint Yoke TR
  grp = ents.add_group
  grp.name = "UJoint Yoke TR"
  face = grp.entities.add_face([4635.mm,1972.mm,2324.mm], [4663.mm,1972.mm,2324.mm], [4663.mm,1978.mm,2324.mm], [4635.mm,1978.mm,2324.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Leadscrew TL"] || model.materials.add("Leadscrew TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # UJoint Cross Pin TR
  grp = ents.add_group
  grp.name = "UJoint Cross Pin TR"
  ge = grp.entities
  circle = ge.add_circle([4633.mm,1962.mm,2338.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(32.mm)
  mat = model.materials["UJoint Cross Pin TL"] || model.materials.add("UJoint Cross Pin TL")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # UJoint Spider TR
  grp = ents.add_group
  grp.name = "UJoint Spider TR"
  ge = grp.entities
  circle = ge.add_circle([4649.mm,1962.mm,2338.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(1.mm)
  mat = model.materials["UJoint Cross Pin TL"] || model.materials.add("UJoint Cross Pin TL")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # UJoint Link TR
  grp = ents.add_group
  grp.name = "UJoint Link TR"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 50.mm)
  circle = ge.add_circle([4649.mm,1962.mm,2338.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Leadscrew TL"] || model.materials.add("Leadscrew TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # HGR20 Rail BL
  grp = ents.add_group
  grp.name = "HGR20 Rail BL"
  face = grp.entities.add_face([138.mm,100.mm,92.mm], [162.mm,100.mm,92.mm], [162.mm,2300.mm,92.mm], [138.mm,2300.mm,92.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["HGR20 Rail TL"] || model.materials.add("HGR20 Rail TL")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Leadscrew BL
  grp = ents.add_group
  grp.name = "Leadscrew BL"
  ge = grp.entities
  circle = ge.add_circle([176.mm,100.mm,100.mm], [0,1,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(2200.mm)
  mat = model.materials["Leadscrew TL"] || model.materials.add("Leadscrew TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Drive Nut BL
  grp = ents.add_group
  grp.name = "Drive Nut BL"
  face = grp.entities.add_face([165.mm,1851.mm,89.mm], [187.mm,1851.mm,89.mm], [187.mm,1873.mm,89.mm], [165.mm,1873.mm,89.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Drive Nut TL"] || model.materials.add("Drive Nut TL")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage BL (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage BL (HGH20CA)"
  face = grp.entities.add_face([128.mm,1840.mm,86.mm], [172.mm,1840.mm,86.mm], [172.mm,1884.mm,86.mm], [128.mm,1884.mm,86.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Drive Nut TL"] || model.materials.add("Drive Nut TL")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Corner Bracket BL
  grp = ents.add_group
  grp.name = "Corner Bracket BL"
  face = grp.entities.add_face([142.mm,1832.mm,0.mm], [158.mm,1832.mm,0.mm], [158.mm,1892.mm,0.mm], [142.mm,1892.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Corner Bracket TL"] || model.materials.add("Corner Bracket TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.9
  grp.material = mat

  # UJoint Yoke BL
  grp = ents.add_group
  grp.name = "UJoint Yoke BL"
  face = grp.entities.add_face([136.mm,1846.mm,36.mm], [164.mm,1846.mm,36.mm], [164.mm,1852.mm,36.mm], [136.mm,1852.mm,36.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Leadscrew TL"] || model.materials.add("Leadscrew TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # UJoint Yoke BL
  grp = ents.add_group
  grp.name = "UJoint Yoke BL"
  face = grp.entities.add_face([136.mm,1872.mm,36.mm], [164.mm,1872.mm,36.mm], [164.mm,1878.mm,36.mm], [136.mm,1878.mm,36.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Leadscrew TL"] || model.materials.add("Leadscrew TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # UJoint Cross Pin BL
  grp = ents.add_group
  grp.name = "UJoint Cross Pin BL"
  ge = grp.entities
  circle = ge.add_circle([134.mm,1862.mm,50.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(32.mm)
  mat = model.materials["UJoint Cross Pin TL"] || model.materials.add("UJoint Cross Pin TL")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # UJoint Spider BL
  grp = ents.add_group
  grp.name = "UJoint Spider BL"
  ge = grp.entities
  circle = ge.add_circle([150.mm,1862.mm,50.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(1.mm)
  mat = model.materials["UJoint Cross Pin TL"] || model.materials.add("UJoint Cross Pin TL")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # UJoint Link BL
  grp = ents.add_group
  grp.name = "UJoint Link BL"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -50.mm)
  circle = ge.add_circle([150.mm,1862.mm,50.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Leadscrew TL"] || model.materials.add("Leadscrew TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # HGR20 Rail BR
  grp = ents.add_group
  grp.name = "HGR20 Rail BR"
  face = grp.entities.add_face([4637.mm,100.mm,92.mm], [4661.mm,100.mm,92.mm], [4661.mm,2300.mm,92.mm], [4637.mm,2300.mm,92.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["HGR20 Rail TL"] || model.materials.add("HGR20 Rail TL")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Leadscrew BR
  grp = ents.add_group
  grp.name = "Leadscrew BR"
  ge = grp.entities
  circle = ge.add_circle([4675.mm,100.mm,100.mm], [0,1,0], 8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(2200.mm)
  mat = model.materials["Leadscrew TL"] || model.materials.add("Leadscrew TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Drive Nut BR
  grp = ents.add_group
  grp.name = "Drive Nut BR"
  face = grp.entities.add_face([4664.mm,1551.mm,89.mm], [4686.mm,1551.mm,89.mm], [4686.mm,1573.mm,89.mm], [4664.mm,1573.mm,89.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Drive Nut TL"] || model.materials.add("Drive Nut TL")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage BR (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage BR (HGH20CA)"
  face = grp.entities.add_face([4627.mm,1540.mm,86.mm], [4671.mm,1540.mm,86.mm], [4671.mm,1584.mm,86.mm], [4627.mm,1584.mm,86.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Drive Nut TL"] || model.materials.add("Drive Nut TL")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Corner Bracket BR
  grp = ents.add_group
  grp.name = "Corner Bracket BR"
  face = grp.entities.add_face([4641.mm,1532.mm,0.mm], [4657.mm,1532.mm,0.mm], [4657.mm,1592.mm,0.mm], [4641.mm,1592.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Corner Bracket TL"] || model.materials.add("Corner Bracket TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.9
  grp.material = mat

  # UJoint Yoke BR
  grp = ents.add_group
  grp.name = "UJoint Yoke BR"
  face = grp.entities.add_face([4635.mm,1546.mm,36.mm], [4663.mm,1546.mm,36.mm], [4663.mm,1552.mm,36.mm], [4635.mm,1552.mm,36.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Leadscrew TL"] || model.materials.add("Leadscrew TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # UJoint Yoke BR
  grp = ents.add_group
  grp.name = "UJoint Yoke BR"
  face = grp.entities.add_face([4635.mm,1572.mm,36.mm], [4663.mm,1572.mm,36.mm], [4663.mm,1578.mm,36.mm], [4635.mm,1578.mm,36.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Leadscrew TL"] || model.materials.add("Leadscrew TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # UJoint Cross Pin BR
  grp = ents.add_group
  grp.name = "UJoint Cross Pin BR"
  ge = grp.entities
  circle = ge.add_circle([4633.mm,1562.mm,50.mm], [1,0,0], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(32.mm)
  mat = model.materials["UJoint Cross Pin TL"] || model.materials.add("UJoint Cross Pin TL")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # UJoint Spider BR
  grp = ents.add_group
  grp.name = "UJoint Spider BR"
  ge = grp.entities
  circle = ge.add_circle([4649.mm,1562.mm,50.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(1.mm)
  mat = model.materials["UJoint Cross Pin TL"] || model.materials.add("UJoint Cross Pin TL")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # UJoint Link BR
  grp = ents.add_group
  grp.name = "UJoint Link BR"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -50.mm)
  circle = ge.add_circle([4649.mm,1562.mm,50.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Leadscrew TL"] || model.materials.add("Leadscrew TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Corner Mechanism"
  inst.layer = model.layers["Corner Mechanism"]


# ── Film Plane (Dynamic Component — click to tilt+swing) ──

# ═══ Film Plane — DYNAMIC COMPONENT (click to tilt+swing) ═══
# Child: the flat framed screen, built in LOCAL coords (TL at the child origin).
fp_screen_defn = model.definitions.add("Film Plane Screen")
ents = fp_screen_defn.entities
  # Film Plane Screen (muslin)
  grp = ents.add_group
  grp.name = "Film Plane Screen (muslin)"
  ge = grp.entities
  f = ge.add_face([0.mm,0.mm,0.mm], [4499.mm,0.mm,0.mm], [4499.mm,0.mm,-2388.mm], [0.mm,0.mm,-2388.mm])
  mat = model.materials["Film Plane Screen (muslin)"] || model.materials.add("Film Plane Screen (muslin)")
  mat.color = Sketchup::Color.new(32, 96, 160)
  mat.alpha = 0.3
  grp.material = mat

  # FP Frame Top
  grp = ents.add_group
  grp.name = "FP Frame Top"
  ge = grp.entities
  vec = Geom::Vector3d.new(4499.mm, 0.mm, 0.mm)
  circle = ge.add_circle([0.mm,0.mm,0.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Leadscrew TL"] || model.materials.add("Leadscrew TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Frame Bottom
  grp = ents.add_group
  grp.name = "FP Frame Bottom"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4499.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4499.mm,0.mm,-2388.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Leadscrew TL"] || model.materials.add("Leadscrew TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Frame Left
  grp = ents.add_group
  grp.name = "FP Frame Left"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -2388.mm)
  circle = ge.add_circle([0.mm,0.mm,0.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Leadscrew TL"] || model.materials.add("Leadscrew TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Frame Right
  grp = ents.add_group
  grp.name = "FP Frame Right"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -2388.mm)
  circle = ge.add_circle([4499.mm,0.mm,0.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Leadscrew TL"] || model.materials.add("Leadscrew TL")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

# Parent: empty driver placed at the TL pivot; the child is nested at the parent
# origin so its RotX/RotZ pivot on the fixed TL corner.
fp_defn = model.definitions.add("Film Plane")
fp_screen_inst = fp_defn.entities.add_instance(fp_screen_defn, Geom::Transformation.new)
fp_screen_inst.name = "Film Plane Screen"
fp_inst = entities.add_instance(fp_defn, Geom::Transformation.translation([150.mm, 2262.mm, 2388.mm]))
fp_inst.name = "Film Plane"
fp_inst.layer = model.layers["Film Plane"]
fp_screen_inst.layer = model.layers["Film Plane"]
fda = "dynamic_attributes"
[fp_defn, fp_inst].each do |e|
  e.set_attribute(fda, "_name", "FilmPlane")
  e.set_attribute(fda, "_lengthunits", "MILLIMETERS")
  e.set_attribute(fda, "pose", 0.0)
end
fp_inst.set_attribute(fda, "_pose_access", "VIEW")
fp_inst.set_attribute(fda, "_pose_label", "Pose (0 flat / 1 tilt+swing)")
fp_inst.set_attribute(fda, "onclick", 'ANIMATE("pose", 0, 1)')
fp_inst.set_attribute(fda, "_onclick_access", "NONE")
# Child rotation formulas read the parent's pose (updates during the animation).
fp_screen_inst.set_attribute(fda, "_name", "FilmPlaneScreen")
fp_screen_inst.set_attribute(fda, "_lengthunits", "MILLIMETERS")
fp_screen_inst.set_attribute(fda, "rotx", 0.0)
fp_screen_inst.set_attribute(fda, "rotz", 0.0)
fp_screen_inst.set_attribute(fda, "_rotx_formula", "9.51*FilmPlane!pose")
fp_screen_inst.set_attribute(fda, "_rotz_formula", "-3.81*FilmPlane!pose")


model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags from earlier versions ──
keep_tags = ["Context", "Film Plane", "Corner Mechanism", "Processing Tray"]
default_layer = model.layers[0]
model.layers.to_a.each { |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}

# ── Scenes ── Combined/Tray use one iso extents camera; each corner scene zooms
# its own iso camera onto that corner's mechanism.
model.layers.each { |l| l.visible = true }
bb = model.bounds
ctr = bb.center
dir = Geom::Vector3d.new(0.72, -0.7, 0.5); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.5)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

[["Combined", ["Context", "Film Plane", "Corner Mechanism", "Processing Tray"], nil], ["Processing Tray", ["Processing Tray"], nil], ["Corner TL", ["Film Plane", "Corner Mechanism"], [150.mm, 2262.mm, 2388.mm]], ["Corner TR", ["Film Plane", "Corner Mechanism"], [4649.mm, 1962.mm, 2388.mm]], ["Corner BL", ["Film Plane", "Corner Mechanism"], [150.mm, 1862.mm, 0.mm]], ["Corner BR", ["Film Plane", "Corner Mechanism"], [4649.mm, 1562.mm, 0.mm]]].each { |name, tags, tgt|
  model.layers.each { |l| l.visible = (l == default_layer || l.name == "Context" || tags.include?(l.name)) }
  if tgt
    t = Geom::Point3d.new(tgt[0], tgt[1], tgt[2])
    e = t.offset(dir, 70.0)        # ~1.8m iso standoff (inches)
    model.active_view.camera = Sketchup::Camera.new(e, t, Z_AXIS)
  else
    model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
    model.active_view.zoom_extents
  end
  page = model.pages.add(name)
  page.use_camera = true
}
model.layers.each { |l| l.visible = true }

# Register the Dynamic Component so its formulas evaluate (else pose/RotX/RotZ
# stay inert until first opened in the DC editor).
if defined?($dc_observers) && $dc_observers.respond_to?(:get_latest_class)
  cls = $dc_observers.get_latest_class
  cls.redraw_with_undo(fp_inst) rescue nil if cls
end

model.commit_operation
{ success: true, model: "Film Plane",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
