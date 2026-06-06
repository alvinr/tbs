model = Sketchup.active_model
model.start_operation("TBS-001 Film Plane Option A", true)
entities = model.active_entities
opts = model.options["UnitsOptions"]; opts["LengthUnit"]=2; opts["LengthFormat"]=0; opts["LengthPrecision"]=1

to_erase = entities.to_a.select { |e| e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text) }
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each { |p| model.pages.erase(p) }

  model.layers.add("Plane") unless model.layers["Plane"]
  model.layers.add("Mechanism") unless model.layers["Mechanism"]
  model.layers.add("Labels") unless model.layers["Labels"]

  # ═══ Floating-corner mechanism ═══
  defn = model.definitions.add("Floating-corner mechanism")
  ents = defn.entities
  # HGR20 Rail TL (fixed)
  grp = ents.add_group
  grp.name = "HGR20 Rail TL (fixed)"
  face = grp.entities.add_face([138.mm,100.mm,2380.mm], [162.mm,100.mm,2380.mm], [162.mm,2300.mm,2380.mm], [138.mm,2300.mm,2380.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["HGR20 Rail TL (fixed)"] || model.materials.add("HGR20 Rail TL (fixed)")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Leadscrew TL (depth drive)
  grp = ents.add_group
  grp.name = "Leadscrew TL (depth drive)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 2200.mm, 0.mm)
  circle = ge.add_circle([184.mm,100.mm,2388.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Leadscrew TL (depth drive)"] || model.materials.add("Leadscrew TL (depth drive)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage TL (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage TL (HGH20CA)"
  face = grp.entities.add_face([124.mm,172.32944711995322.mm,2370.mm], [176.mm,172.32944711995322.mm,2370.mm], [176.mm,236.32944711995322.mm,2370.mm], [124.mm,236.32944711995322.mm,2370.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Carriage TL (HGH20CA)"] || model.materials.add("Carriage TL (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Drive Nut TL
  grp = ents.add_group
  grp.name = "Drive Nut TL"
  face = grp.entities.add_face([170.mm,190.32944711995322.mm,2376.mm], [198.mm,190.32944711995322.mm,2376.mm], [198.mm,218.32944711995322.mm,2376.mm], [170.mm,218.32944711995322.mm,2376.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Carriage TL (HGH20CA)"] || model.materials.add("Carriage TL (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # X cross-slide TL (SWING)
  grp = ents.add_group
  grp.name = "X cross-slide TL (SWING)"
  face = grp.entities.add_face([134.mm,188.32944711995322.mm,2394.mm], [348.34431808298496.mm,188.32944711995322.mm,2394.mm], [348.34431808298496.mm,220.32944711995322.mm,2394.mm], [134.mm,220.32944711995322.mm,2394.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["X cross-slide TL (SWING)"] || model.materials.add("X cross-slide TL (SWING)")
  mat.color = Sketchup::Color.new(31, 119, 180)
  mat.alpha = 1.0
  grp.material = mat

  # X slider block TL
  grp = ents.add_group
  grp.name = "X slider block TL"
  face = grp.entities.add_face([316.34431808298496.mm,184.32944711995322.mm,2392.mm], [348.34431808298496.mm,184.32944711995322.mm,2392.mm], [348.34431808298496.mm,224.32944711995322.mm,2392.mm], [316.34431808298496.mm,224.32944711995322.mm,2392.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Carriage TL (HGH20CA)"] || model.materials.add("Carriage TL (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Z cross-slide TL (TILT)
  grp = ents.add_group
  grp.name = "Z cross-slide TL (TILT)"
  face = grp.entities.add_face([323.34431808298496.mm,189.32944711995322.mm,2299.9929892183745.mm], [341.34431808298496.mm,189.32944711995322.mm,2299.9929892183745.mm], [341.34431808298496.mm,219.32944711995322.mm,2299.9929892183745.mm], [323.34431808298496.mm,219.32944711995322.mm,2299.9929892183745.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(104.00701078162547.mm)
  mat = model.materials["Z cross-slide TL (TILT)"] || model.materials.add("Z cross-slide TL (TILT)")
  mat.color = Sketchup::Color.new(44, 160, 44)
  mat.alpha = 1.0
  grp.material = mat

  # Z slider block TL
  grp = ents.add_group
  grp.name = "Z slider block TL"
  face = grp.entities.add_face([319.34431808298496.mm,186.32944711995322.mm,2299.9929892183745.mm], [345.34431808298496.mm,186.32944711995322.mm,2299.9929892183745.mm], [345.34431808298496.mm,222.32944711995322.mm,2299.9929892183745.mm], [319.34431808298496.mm,222.32944711995322.mm,2299.9929892183745.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Carriage TL (HGH20CA)"] || model.materials.add("Carriage TL (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Rod-End TL (-> frame)
  grp = ents.add_group
  grp.name = "Rod-End TL (-> frame)"
  face = grp.entities.add_face([315.34431808298496.mm,187.32944711995322.mm,2298.9929892183745.mm], [349.34431808298496.mm,187.32944711995322.mm,2298.9929892183745.mm], [349.34431808298496.mm,221.32944711995322.mm,2298.9929892183745.mm], [315.34431808298496.mm,221.32944711995322.mm,2298.9929892183745.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(34.mm)
  mat = model.materials["Leadscrew TL (depth drive)"] || model.materials.add("Leadscrew TL (depth drive)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Flat-corner ghost TL
  grp = ents.add_group
  grp.name = "Flat-corner ghost TL"
  face = grp.entities.add_face([137.mm,191.32944711995322.mm,2375.mm], [163.mm,191.32944711995322.mm,2375.mm], [163.mm,217.32944711995322.mm,2375.mm], [137.mm,217.32944711995322.mm,2375.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Flat-corner ghost TL"] || model.materials.add("Flat-corner ghost TL")
  mat.color = Sketchup::Color.new(154, 166, 178)
  mat.alpha = 1.0
  grp.material = mat

  # HGR20 Rail TR (fixed)
  grp = ents.add_group
  grp.name = "HGR20 Rail TR (fixed)"
  face = grp.entities.add_face([4637.mm,100.mm,2380.mm], [4661.mm,100.mm,2380.mm], [4661.mm,2300.mm,2380.mm], [4637.mm,2300.mm,2380.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["HGR20 Rail TL (fixed)"] || model.materials.add("HGR20 Rail TL (fixed)")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Leadscrew TR (depth drive)
  grp = ents.add_group
  grp.name = "Leadscrew TR (depth drive)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 2200.mm, 0.mm)
  circle = ge.add_circle([4683.mm,100.mm,2388.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Leadscrew TL (depth drive)"] || model.materials.add("Leadscrew TL (depth drive)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage TR (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage TR (HGH20CA)"
  face = grp.entities.add_face([4623.mm,1336.7563310361938.mm,2370.mm], [4675.mm,1336.7563310361938.mm,2370.mm], [4675.mm,1400.7563310361938.mm,2370.mm], [4623.mm,1400.7563310361938.mm,2370.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Carriage TL (HGH20CA)"] || model.materials.add("Carriage TL (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Drive Nut TR
  grp = ents.add_group
  grp.name = "Drive Nut TR"
  face = grp.entities.add_face([4669.mm,1354.7563310361938.mm,2376.mm], [4697.mm,1354.7563310361938.mm,2376.mm], [4697.mm,1382.7563310361938.mm,2376.mm], [4669.mm,1382.7563310361938.mm,2376.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Carriage TL (HGH20CA)"] || model.materials.add("Carriage TL (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # X cross-slide TR (SWING)
  grp = ents.add_group
  grp.name = "X cross-slide TR (SWING)"
  face = grp.entities.add_face([4633.mm,1352.7563310361938.mm,2394.mm], [4694.044610557503.mm,1352.7563310361938.mm,2394.mm], [4694.044610557503.mm,1384.7563310361938.mm,2394.mm], [4633.mm,1384.7563310361938.mm,2394.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["X cross-slide TL (SWING)"] || model.materials.add("X cross-slide TL (SWING)")
  mat.color = Sketchup::Color.new(31, 119, 180)
  mat.alpha = 1.0
  grp.material = mat

  # X slider block TR
  grp = ents.add_group
  grp.name = "X slider block TR"
  face = grp.entities.add_face([4662.044610557503.mm,1348.7563310361938.mm,2392.mm], [4694.044610557503.mm,1348.7563310361938.mm,2392.mm], [4694.044610557503.mm,1388.7563310361938.mm,2392.mm], [4662.044610557503.mm,1388.7563310361938.mm,2392.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Carriage TL (HGH20CA)"] || model.materials.add("Carriage TL (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Z cross-slide TR (TILT)
  grp = ents.add_group
  grp.name = "Z cross-slide TR (TILT)"
  face = grp.entities.add_face([4669.044610557503.mm,1353.7563310361938.mm,2299.9929892183745.mm], [4687.044610557503.mm,1353.7563310361938.mm,2299.9929892183745.mm], [4687.044610557503.mm,1383.7563310361938.mm,2299.9929892183745.mm], [4669.044610557503.mm,1383.7563310361938.mm,2299.9929892183745.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(104.00701078162547.mm)
  mat = model.materials["Z cross-slide TL (TILT)"] || model.materials.add("Z cross-slide TL (TILT)")
  mat.color = Sketchup::Color.new(44, 160, 44)
  mat.alpha = 1.0
  grp.material = mat

  # Z slider block TR
  grp = ents.add_group
  grp.name = "Z slider block TR"
  face = grp.entities.add_face([4665.044610557503.mm,1350.7563310361938.mm,2299.9929892183745.mm], [4691.044610557503.mm,1350.7563310361938.mm,2299.9929892183745.mm], [4691.044610557503.mm,1386.7563310361938.mm,2299.9929892183745.mm], [4665.044610557503.mm,1386.7563310361938.mm,2299.9929892183745.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Carriage TL (HGH20CA)"] || model.materials.add("Carriage TL (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Rod-End TR (-> frame)
  grp = ents.add_group
  grp.name = "Rod-End TR (-> frame)"
  face = grp.entities.add_face([4661.044610557503.mm,1351.7563310361938.mm,2298.9929892183745.mm], [4695.044610557503.mm,1351.7563310361938.mm,2298.9929892183745.mm], [4695.044610557503.mm,1385.7563310361938.mm,2298.9929892183745.mm], [4661.044610557503.mm,1385.7563310361938.mm,2298.9929892183745.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(34.mm)
  mat = model.materials["Leadscrew TL (depth drive)"] || model.materials.add("Leadscrew TL (depth drive)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Flat-corner ghost TR
  grp = ents.add_group
  grp.name = "Flat-corner ghost TR"
  face = grp.entities.add_face([4636.mm,1355.7563310361938.mm,2375.mm], [4662.mm,1355.7563310361938.mm,2375.mm], [4662.mm,1381.7563310361938.mm,2375.mm], [4636.mm,1381.7563310361938.mm,2375.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Flat-corner ghost TL"] || model.materials.add("Flat-corner ghost TL")
  mat.color = Sketchup::Color.new(154, 166, 178)
  mat.alpha = 1.0
  grp.material = mat

  # HGR20 Rail BL (fixed)
  grp = ents.add_group
  grp.name = "HGR20 Rail BL (fixed)"
  face = grp.entities.add_face([138.mm,100.mm,-8.mm], [162.mm,100.mm,-8.mm], [162.mm,2300.mm,-8.mm], [138.mm,2300.mm,-8.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["HGR20 Rail TL (fixed)"] || model.materials.add("HGR20 Rail TL (fixed)")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Leadscrew BL (depth drive)
  grp = ents.add_group
  grp.name = "Leadscrew BL (depth drive)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 2200.mm, 0.mm)
  circle = ge.add_circle([184.mm,100.mm,0.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Leadscrew TL (depth drive)"] || model.materials.add("Leadscrew TL (depth drive)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage BL (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage BL (HGH20CA)"
  face = grp.entities.add_face([124.mm,961.243668963806.mm,-18.mm], [176.mm,961.243668963806.mm,-18.mm], [176.mm,1025.2436689638062.mm,-18.mm], [124.mm,1025.2436689638062.mm,-18.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Carriage TL (HGH20CA)"] || model.materials.add("Carriage TL (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Drive Nut BL
  grp = ents.add_group
  grp.name = "Drive Nut BL"
  face = grp.entities.add_face([170.mm,979.243668963806.mm,-12.mm], [198.mm,979.243668963806.mm,-12.mm], [198.mm,1007.243668963806.mm,-12.mm], [170.mm,1007.243668963806.mm,-12.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Carriage TL (HGH20CA)"] || model.materials.add("Carriage TL (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # X cross-slide BL (SWING)
  grp = ents.add_group
  grp.name = "X cross-slide BL (SWING)"
  face = grp.entities.add_face([104.95538944249665.mm,977.243668963806.mm,6.mm], [166.mm,977.243668963806.mm,6.mm], [166.mm,1009.243668963806.mm,6.mm], [104.95538944249665.mm,1009.243668963806.mm,6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["X cross-slide TL (SWING)"] || model.materials.add("X cross-slide TL (SWING)")
  mat.color = Sketchup::Color.new(31, 119, 180)
  mat.alpha = 1.0
  grp.material = mat

  # X slider block BL
  grp = ents.add_group
  grp.name = "X slider block BL"
  face = grp.entities.add_face([104.95538944249665.mm,973.243668963806.mm,4.mm], [136.95538944249665.mm,973.243668963806.mm,4.mm], [136.95538944249665.mm,1013.243668963806.mm,4.mm], [104.95538944249665.mm,1013.243668963806.mm,4.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Carriage TL (HGH20CA)"] || model.materials.add("Carriage TL (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Z cross-slide BL (TILT)
  grp = ents.add_group
  grp.name = "Z cross-slide BL (TILT)"
  face = grp.entities.add_face([111.95538944249665.mm,978.243668963806.mm,-16.mm], [129.95538944249665.mm,978.243668963806.mm,-16.mm], [129.95538944249665.mm,1008.243668963806.mm,-16.mm], [111.95538944249665.mm,1008.243668963806.mm,-16.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(104.00701078162524.mm)
  mat = model.materials["Z cross-slide TL (TILT)"] || model.materials.add("Z cross-slide TL (TILT)")
  mat.color = Sketchup::Color.new(44, 160, 44)
  mat.alpha = 1.0
  grp.material = mat

  # Z slider block BL
  grp = ents.add_group
  grp.name = "Z slider block BL"
  face = grp.entities.add_face([107.95538944249665.mm,975.243668963806.mm,56.00701078162524.mm], [133.95538944249665.mm,975.243668963806.mm,56.00701078162524.mm], [133.95538944249665.mm,1011.243668963806.mm,56.00701078162524.mm], [107.95538944249665.mm,1011.243668963806.mm,56.00701078162524.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Carriage TL (HGH20CA)"] || model.materials.add("Carriage TL (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Rod-End BL (-> frame)
  grp = ents.add_group
  grp.name = "Rod-End BL (-> frame)"
  face = grp.entities.add_face([103.95538944249665.mm,976.243668963806.mm,55.00701078162524.mm], [137.95538944249665.mm,976.243668963806.mm,55.00701078162524.mm], [137.95538944249665.mm,1010.243668963806.mm,55.00701078162524.mm], [103.95538944249665.mm,1010.243668963806.mm,55.00701078162524.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(34.mm)
  mat = model.materials["Leadscrew TL (depth drive)"] || model.materials.add("Leadscrew TL (depth drive)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Flat-corner ghost BL
  grp = ents.add_group
  grp.name = "Flat-corner ghost BL"
  face = grp.entities.add_face([137.mm,980.243668963806.mm,-13.mm], [163.mm,980.243668963806.mm,-13.mm], [163.mm,1006.243668963806.mm,-13.mm], [137.mm,1006.243668963806.mm,-13.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Flat-corner ghost TL"] || model.materials.add("Flat-corner ghost TL")
  mat.color = Sketchup::Color.new(154, 166, 178)
  mat.alpha = 1.0
  grp.material = mat

  # HGR20 Rail BR (fixed)
  grp = ents.add_group
  grp.name = "HGR20 Rail BR (fixed)"
  face = grp.entities.add_face([4637.mm,100.mm,-8.mm], [4661.mm,100.mm,-8.mm], [4661.mm,2300.mm,-8.mm], [4637.mm,2300.mm,-8.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["HGR20 Rail TL (fixed)"] || model.materials.add("HGR20 Rail TL (fixed)")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Leadscrew BR (depth drive)
  grp = ents.add_group
  grp.name = "Leadscrew BR (depth drive)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 2200.mm, 0.mm)
  circle = ge.add_circle([4683.mm,100.mm,0.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Leadscrew TL (depth drive)"] || model.materials.add("Leadscrew TL (depth drive)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage BR (HGH20CA)
  grp = ents.add_group
  grp.name = "Carriage BR (HGH20CA)"
  face = grp.entities.add_face([4623.mm,2125.6705528800467.mm,-18.mm], [4675.mm,2125.6705528800467.mm,-18.mm], [4675.mm,2189.6705528800467.mm,-18.mm], [4623.mm,2189.6705528800467.mm,-18.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Carriage TL (HGH20CA)"] || model.materials.add("Carriage TL (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Drive Nut BR
  grp = ents.add_group
  grp.name = "Drive Nut BR"
  face = grp.entities.add_face([4669.mm,2143.6705528800467.mm,-12.mm], [4697.mm,2143.6705528800467.mm,-12.mm], [4697.mm,2171.6705528800467.mm,-12.mm], [4669.mm,2171.6705528800467.mm,-12.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Carriage TL (HGH20CA)"] || model.materials.add("Carriage TL (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # X cross-slide BR (SWING)
  grp = ents.add_group
  grp.name = "X cross-slide BR (SWING)"
  face = grp.entities.add_face([4450.655681917015.mm,2141.6705528800467.mm,6.mm], [4665.mm,2141.6705528800467.mm,6.mm], [4665.mm,2173.6705528800467.mm,6.mm], [4450.655681917015.mm,2173.6705528800467.mm,6.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["X cross-slide TL (SWING)"] || model.materials.add("X cross-slide TL (SWING)")
  mat.color = Sketchup::Color.new(31, 119, 180)
  mat.alpha = 1.0
  grp.material = mat

  # X slider block BR
  grp = ents.add_group
  grp.name = "X slider block BR"
  face = grp.entities.add_face([4450.655681917015.mm,2137.6705528800467.mm,4.mm], [4482.655681917015.mm,2137.6705528800467.mm,4.mm], [4482.655681917015.mm,2177.6705528800467.mm,4.mm], [4450.655681917015.mm,2177.6705528800467.mm,4.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Carriage TL (HGH20CA)"] || model.materials.add("Carriage TL (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Z cross-slide BR (TILT)
  grp = ents.add_group
  grp.name = "Z cross-slide BR (TILT)"
  face = grp.entities.add_face([4457.655681917015.mm,2142.6705528800467.mm,-16.mm], [4475.655681917015.mm,2142.6705528800467.mm,-16.mm], [4475.655681917015.mm,2172.6705528800467.mm,-16.mm], [4457.655681917015.mm,2172.6705528800467.mm,-16.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(104.00701078162524.mm)
  mat = model.materials["Z cross-slide TL (TILT)"] || model.materials.add("Z cross-slide TL (TILT)")
  mat.color = Sketchup::Color.new(44, 160, 44)
  mat.alpha = 1.0
  grp.material = mat

  # Z slider block BR
  grp = ents.add_group
  grp.name = "Z slider block BR"
  face = grp.entities.add_face([4453.655681917015.mm,2139.6705528800467.mm,56.00701078162524.mm], [4479.655681917015.mm,2139.6705528800467.mm,56.00701078162524.mm], [4479.655681917015.mm,2175.6705528800467.mm,56.00701078162524.mm], [4453.655681917015.mm,2175.6705528800467.mm,56.00701078162524.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(32.mm)
  mat = model.materials["Carriage TL (HGH20CA)"] || model.materials.add("Carriage TL (HGH20CA)")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Rod-End BR (-> frame)
  grp = ents.add_group
  grp.name = "Rod-End BR (-> frame)"
  face = grp.entities.add_face([4449.655681917015.mm,2140.6705528800467.mm,55.00701078162524.mm], [4483.655681917015.mm,2140.6705528800467.mm,55.00701078162524.mm], [4483.655681917015.mm,2174.6705528800467.mm,55.00701078162524.mm], [4449.655681917015.mm,2174.6705528800467.mm,55.00701078162524.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(34.mm)
  mat = model.materials["Leadscrew TL (depth drive)"] || model.materials.add("Leadscrew TL (depth drive)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Flat-corner ghost BR
  grp = ents.add_group
  grp.name = "Flat-corner ghost BR"
  face = grp.entities.add_face([4636.mm,2144.6705528800467.mm,-13.mm], [4662.mm,2144.6705528800467.mm,-13.mm], [4662.mm,2170.6705528800467.mm,-13.mm], [4636.mm,2170.6705528800467.mm,-13.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(26.mm)
  mat = model.materials["Flat-corner ghost TL"] || model.materials.add("Flat-corner ghost TL")
  mat.color = Sketchup::Color.new(154, 166, 178)
  mat.alpha = 1.0
  grp.material = mat

  # Floor (ref)
  grp = ents.add_group
  grp.name = "Floor (ref)"
  face = grp.entities.add_face([-250.mm,-219.mm,-8.mm], [5049.mm,-219.mm,-8.mm], [5049.mm,2781.mm,-8.mm], [-250.mm,2781.mm,-8.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["Floor (ref)"] || model.materials.add("Floor (ref)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.16
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Floating-corner mechanism"
  inst.layer = model.layers["Mechanism"]

  # ═══ Film Plane (rigid, fixed size) ═══
  defn = model.definitions.add("Film Plane (rigid, fixed size)")
  ents = defn.entities
  # Film Plane Screen (muslin)
  grp = ents.add_group
  grp.name = "Film Plane Screen (muslin)"
  ge = grp.entities
  f = ge.add_face([332.34431808298496.mm,204.32944711995322.mm,2315.9929892183745.mm], [4678.044610557503.mm,1368.7563310361938.mm,2315.9929892183745.mm], [4466.655681917015.mm,2157.6705528800467.mm,72.00701078162524.mm], [120.95538944249665.mm,993.243668963806.mm,72.00701078162524.mm])
  mat = model.materials["Film Plane Screen (muslin)"] || model.materials.add("Film Plane Screen (muslin)")
  mat.color = Sketchup::Color.new(32, 96, 160)
  mat.alpha = 0.22
  grp.material = mat

  # FP Frame Top
  grp = ents.add_group
  grp.name = "FP Frame Top"
  ge = grp.entities
  vec = Geom::Vector3d.new(4345.7002924745175.mm, 1164.4268839162405.mm, 0.mm)
  circle = ge.add_circle([332.34431808298496.mm,204.32944711995322.mm,2315.9929892183745.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Leadscrew TL (depth drive)"] || model.materials.add("Leadscrew TL (depth drive)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Frame Bottom
  grp = ents.add_group
  grp.name = "FP Frame Bottom"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4345.7002924745175.mm, -1164.4268839162405.mm, 0.mm)
  circle = ge.add_circle([4466.655681917015.mm,2157.6705528800467.mm,72.00701078162524.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Leadscrew TL (depth drive)"] || model.materials.add("Leadscrew TL (depth drive)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Frame Left
  grp = ents.add_group
  grp.name = "FP Frame Left"
  ge = grp.entities
  vec = Geom::Vector3d.new(-211.3889286404883.mm, 788.9142218438528.mm, -2243.985978436749.mm)
  circle = ge.add_circle([332.34431808298496.mm,204.32944711995322.mm,2315.9929892183745.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Leadscrew TL (depth drive)"] || model.materials.add("Leadscrew TL (depth drive)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP Frame Right
  grp = ents.add_group
  grp.name = "FP Frame Right"
  ge = grp.entities
  vec = Geom::Vector3d.new(-211.3889286404883.mm, 788.9142218438528.mm, -2243.985978436749.mm)
  circle = ge.add_circle([4678.044610557503.mm,1368.7563310361938.mm,2315.9929892183745.mm], vec, 25.4.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Leadscrew TL (depth drive)"] || model.materials.add("Leadscrew TL (depth drive)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Film Plane (rigid, fixed size)"
  inst.layer = model.layers["Plane"]


# ── Annotation notes (Labels tag — shown only in the corner-detail scene) ──
t=entities.add_text("HGR20 rail - FIXED (depth guide)", Geom::Point3d.new(4649.mm,1118.7563310361938.mm,2388.mm), Geom::Vector3d.new(10,0,11.0)); t.layer=model.layers["Labels"] rescue nil
t=entities.add_text("Leadscrew - DEPTH / focus drive", Geom::Point3d.new(4683.mm,668.7563310361938.mm,2388.mm), Geom::Vector3d.new(4.0,0,19.0)); t.layer=model.layers["Labels"] rescue nil
t=entities.add_text("Carriage + drive nut", Geom::Point3d.new(4629.mm,1368.7563310361938.mm,2376.mm), Geom::Vector3d.new(-10.0,0,-15.0)); t.layer=model.layers["Labels"] rescue nil
t=entities.add_text("X cross-slide = SWING float (blue)", Geom::Point3d.new(4663.522305278751.mm,1368.7563310361938.mm,2402.mm), Geom::Vector3d.new(-12.0,0,4.0)); t.layer=model.layers["Labels"] rescue nil
t=entities.add_text("Z cross-slide = TILT float (green)", Geom::Point3d.new(4678.044610557503.mm,1368.7563310361938.mm,2351.9964946091873.mm), Geom::Vector3d.new(17.0,0,-12.0)); t.layer=model.layers["Labels"] rescue nil
t=entities.add_text("Rod-end -> rigid frame corner", Geom::Point3d.new(4678.044610557503.mm,1368.7563310361938.mm,2315.9929892183745.mm), Geom::Vector3d.new(17.0,0,5.0)); t.layer=model.layers["Labels"] rescue nil
t=entities.add_text("ghost = corner if it stayed on rail", Geom::Point3d.new(4649.mm,1368.7563310361938.mm,2388.mm), Geom::Vector3d.new(-17.0,0,13.0)); t.layer=model.layers["Labels"] rescue nil

model.definitions.purge_unused
model.materials.purge_unused
keep_tags = ["Plane", "Mechanism", "Labels"]; dl = model.layers[0]
model.layers.to_a.each { |l| next if l==dl||keep_tags.include?(l.name); model.layers.remove(l,true) rescue nil }

dir = Geom::Vector3d.new(0.55, -0.82, 0.40); dir.normalize!
# Scene 1: full assembly, Labels OFF
model.layers["Labels"].visible = false
ac = Geom::Point3d.new(2399.5.mm, 1181.mm, 1194.mm)
cam = Sketchup::Camera.new(ac.offset(dir,330), ac, Z_AXIS); cam.fov=35; cam.aspect_ratio=1.4444444444444444
model.active_view.camera = cam
p1 = model.pages.add("Assembly"); p1.use_camera = true
# Scene 2: zoomed TR corner, Labels ON
model.layers["Labels"].visible = true
tc = Geom::Point3d.new(*[4678.044610557503.mm, 1368.7563310361938.mm, 2315.9929892183745.mm])
dir2 = Geom::Vector3d.new(0.5, -0.84, 0.38); dir2.normalize!
cam2 = Sketchup::Camera.new(tc.offset(dir2,95), tc, Z_AXIS); cam2.fov=35; cam2.aspect_ratio=1.4444444444444444
model.active_view.camera = cam2
p2 = model.pages.add("Corner detail (TR)"); p2.use_camera = true

model.commit_operation
{ success: true, model: "film-plane-optA", scenes: model.pages.count,
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tilt: 20.0, swing: 15.0 }.to_json
