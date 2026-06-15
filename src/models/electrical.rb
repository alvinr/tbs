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

  # Far Wall (context)
  grp = ents.add_group
  grp.name = "Far Wall (context)"
  face = grp.entities.add_face([0.mm,2362.mm,0.mm], [5893.mm,2362.mm,0.mm], [5893.mm,2402.mm,0.mm], [0.mm,2402.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Far Wall (context)"] || model.materials.add("Far Wall (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.14
  grp.material = mat

  # End Wall door (context)
  grp = ents.add_group
  grp.name = "End Wall door (context)"
  face = grp.entities.add_face([-40.mm,0.mm,0.mm], [0.mm,0.mm,0.mm], [0.mm,2362.mm,0.mm], [-40.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Far Wall (context)"] || model.materials.add("Far Wall (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.14
  grp.material = mat

  # End Wall sealed (context)
  grp = ents.add_group
  grp.name = "End Wall sealed (context)"
  face = grp.entities.add_face([5893.mm,0.mm,0.mm], [5933.mm,0.mm,0.mm], [5933.mm,2362.mm,0.mm], [5893.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Far Wall (context)"] || model.materials.add("Far Wall (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.14
  grp.material = mat

  # Fan A ghost (exhaust)
  grp = ents.add_group
  grp.name = "Fan A ghost (exhaust)"
  face = grp.entities.add_face([5693.mm,1106.mm,1925.mm], [5813.mm,1106.mm,1925.mm], [5813.mm,1256.mm,1925.mm], [5693.mm,1256.mm,1925.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Fan A ghost (exhaust)"] || model.materials.add("Fan A ghost (exhaust)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 0.18
  grp.material = mat

  # Fan B ghost (intake)
  grp = ents.add_group
  grp.name = "Fan B ghost (intake)"
  face = grp.entities.add_face([220.mm,290.mm,525.mm], [340.mm,290.mm,525.mm], [340.mm,440.mm,525.mm], [220.mm,440.mm,525.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Fan B ghost (intake)"] || model.materials.add("Fan B ghost (intake)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 0.18
  grp.material = mat

  # Pump cluster ghost
  grp = ents.add_group
  grp.name = "Pump cluster ghost"
  face = grp.entities.add_face([4744.mm,1050.mm,1300.mm], [4894.mm,1050.mm,1300.mm], [4894.mm,1310.mm,1300.mm], [4744.mm,1310.mm,1300.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(420.mm)
  mat = model.materials["Pump cluster ghost"] || model.materials.add("Pump cluster ghost")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 0.16
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
  face = grp.entities.add_face([4550.mm,1031.mm,2348.mm], [5150.mm,1031.mm,2348.mm], [5150.mm,1331.mm,2348.mm], [4550.mm,1331.mm,2348.mm])
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
  mat.alpha = 1.0
  grp.material = mat

  # Solar Panel 2 (200W)
  grp = ents.add_group
  grp.name = "Solar Panel 2 (200W)"
  face = grp.entities.add_face([960.mm,-900.mm,120.mm], [1640.mm,-900.mm,120.mm], [1640.mm,-2181.7175976009694.mm,859.9999999999999.mm], [960.mm,-2181.7175976009694.mm,859.9999999999999.mm])
  face.pushpull(35.mm)
  mat = model.materials["Solar Panel 1 (200W)"] || model.materials.add("Solar Panel 1 (200W)")
  mat.color = Sketchup::Color.new(27, 58, 107)
  mat.alpha = 1.0
  grp.material = mat

  # Solar Panel 3 (200W)
  grp = ents.add_group
  grp.name = "Solar Panel 3 (200W)"
  face = grp.entities.add_face([1670.mm,-900.mm,120.mm], [2350.mm,-900.mm,120.mm], [2350.mm,-2181.7175976009694.mm,859.9999999999999.mm], [1670.mm,-2181.7175976009694.mm,859.9999999999999.mm])
  face.pushpull(35.mm)
  mat = model.materials["Solar Panel 1 (200W)"] || model.materials.add("Solar Panel 1 (200W)")
  mat.color = Sketchup::Color.new(27, 58, 107)
  mat.alpha = 1.0
  grp.material = mat

  # Tilt Frame front rail
  grp = ents.add_group
  grp.name = "Tilt Frame front rail"
  face = grp.entities.add_face([250.mm,-920.mm,0.mm], [2350.mm,-920.mm,0.mm], [2350.mm,-880.mm,0.mm], [250.mm,-880.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Tilt Frame front rail"] || model.materials.add("Tilt Frame front rail")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Tilt Frame back rail
  grp = ents.add_group
  grp.name = "Tilt Frame back rail"
  face = grp.entities.add_face([250.mm,-2201.7175976009694.mm,0.mm], [2350.mm,-2201.7175976009694.mm,0.mm], [2350.mm,-2161.7175976009694.mm,0.mm], [250.mm,-2161.7175976009694.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Tilt Frame front rail"] || model.materials.add("Tilt Frame front rail")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Tilt Frame back leg
  grp = ents.add_group
  grp.name = "Tilt Frame back leg"
  face = grp.entities.add_face([250.mm,-2201.7175976009694.mm,0.mm], [290.mm,-2201.7175976009694.mm,0.mm], [290.mm,-2161.7175976009694.mm,0.mm], [250.mm,-2161.7175976009694.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(859.9999999999999.mm)
  mat = model.materials["Tilt Frame front rail"] || model.materials.add("Tilt Frame front rail")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Tilt Frame back leg
  grp = ents.add_group
  grp.name = "Tilt Frame back leg"
  face = grp.entities.add_face([2310.mm,-2201.7175976009694.mm,0.mm], [2350.mm,-2201.7175976009694.mm,0.mm], [2350.mm,-2161.7175976009694.mm,0.mm], [2310.mm,-2161.7175976009694.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(859.9999999999999.mm)
  mat = model.materials["Tilt Frame front rail"] || model.materials.add("Tilt Frame front rail")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # PV run (array -> panel)
  grp = ents.add_group
  grp.name = "PV run (array -> panel)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 830.mm, 0.mm)
  circle = ge.add_circle([1300.mm,-920.mm,60.mm], vec, 10.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV run (array -> panel)"] || model.materials.add("PV run (array -> panel)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV run (array -> panel) elbow
  grp = ents.add_group
  grp.name = "PV run (array -> panel) elbow"
  ge = grp.entities
  arc = ge.add_arc([1300.mm,-90.mm,80.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 20.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1300.mm,-90.mm,60.mm], [0.000000,1.000000,0.000000], 10.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["PV run (array -> panel)"] || model.materials.add("PV run (array -> panel)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV run (array -> panel)
  grp = ents.add_group
  grp.name = "PV run (array -> panel)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1860.2.mm)
  circle = ge.add_circle([1300.mm,-70.mm,80.mm], vec, 10.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV run (array -> panel)"] || model.materials.add("PV run (array -> panel)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV run (array -> panel) elbow
  grp = ents.add_group
  grp.name = "PV run (array -> panel) elbow"
  ge = grp.entities
  arc = ge.add_arc([1309.8.mm,-70.mm,1940.2.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 9.800000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1300.mm,-70.mm,1940.2.mm], [0.000000,0.000000,1.000000], 10.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["PV run (array -> panel)"] || model.materials.add("PV run (array -> panel)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV run (array -> panel)
  grp = ents.add_group
  grp.name = "PV run (array -> panel)"
  ge = grp.entities
  vec = Geom::Vector3d.new(10.200000000000045.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1309.8.mm,-70.mm,1950.mm], vec, 10.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV run (array -> panel)"] || model.materials.add("PV run (array -> panel)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Solar Array"
  inst.layer = model.layers["Solar Array"]

  # ═══ Power Core ═══
  defn = model.definitions.add("Power Core")
  ents = defn.entities
  # Enclosure (IP65, ghosted)
  grp = ents.add_group
  grp.name = "Enclosure (IP65, ghosted)"
  face = grp.entities.add_face([1898.mm,0.mm,1488.mm], [2222.mm,0.mm,1488.mm], [2222.mm,171.mm,1488.mm], [1898.mm,171.mm,1488.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(624.mm)
  mat = model.materials["Enclosure (IP65, ghosted)"] || model.materials.add("Enclosure (IP65, ghosted)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.12
  grp.material = mat

  # MPPT Controller (100/50)
  grp = ents.add_group
  grp.name = "MPPT Controller (100/50)"
  face = grp.entities.add_face([1925.mm,25.mm,1970.mm], [2110.mm,25.mm,1970.mm], [2110.mm,95.mm,1970.mm], [1925.mm,95.mm,1970.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["MPPT Controller (100/50)"] || model.materials.add("MPPT Controller (100/50)")
  mat.color = Sketchup::Color.new(58, 91, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse Block (Blue Sea 5026)
  grp = ents.add_group
  grp.name = "Fuse Block (Blue Sea 5026)"
  face = grp.entities.add_face([1925.mm,25.mm,1770.mm], [2075.mm,25.mm,1770.mm], [2075.mm,70.mm,1770.mm], [1925.mm,70.mm,1770.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(75.mm)
  mat = model.materials["Fuse Block (Blue Sea 5026)"] || model.materials.add("Fuse Block (Blue Sea 5026)")
  mat.color = Sketchup::Color.new(43, 43, 48)
  mat.alpha = 1.0
  grp.material = mat

  # Busbar (+)
  grp = ents.add_group
  grp.name = "Busbar (+)"
  face = grp.entities.add_face([1925.mm,30.mm,1705.mm], [2045.mm,30.mm,1705.mm], [2045.mm,50.mm,1705.mm], [1925.mm,50.mm,1705.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Busbar (+)"] || model.materials.add("Busbar (+)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Busbar (-)
  grp = ents.add_group
  grp.name = "Busbar (-)"
  face = grp.entities.add_face([1925.mm,30.mm,1675.mm], [2045.mm,30.mm,1675.mm], [2045.mm,50.mm,1675.mm], [1925.mm,50.mm,1675.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Busbar (-)"] || model.materials.add("Busbar (-)")
  mat.color = Sketchup::Color.new(44, 44, 44)
  mat.alpha = 1.0
  grp.material = mat

  # Main Disconnect (m-Series)
  grp = ents.add_group
  grp.name = "Main Disconnect (m-Series)"
  ge = grp.entities
  circle = ge.add_circle([2150.mm,165.mm,1620.mm], [0,1,0], 35.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Main Disconnect (m-Series)"] || model.materials.add("Main Disconnect (m-Series)")
  mat.color = Sketchup::Color.new(212, 58, 47)
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
  face = grp.entities.add_face([1540.mm,0.mm,150.mm], [1870.mm,0.mm,150.mm], [1870.mm,172.mm,150.mm], [1540.mm,172.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(214.mm)
  mat = model.materials["Battery 1 (12V 100Ah LiFePO4)"] || model.materials.add("Battery 1 (12V 100Ah LiFePO4)")
  mat.color = Sketchup::Color.new(106, 90, 205)
  mat.alpha = 1.0
  grp.material = mat

  # Battery 2 (optional 2nd pack, ghosted)
  grp = ents.add_group
  grp.name = "Battery 2 (optional 2nd pack, ghosted)"
  face = grp.entities.add_face([1890.mm,0.mm,150.mm], [2220.mm,0.mm,150.mm], [2220.mm,172.mm,150.mm], [1890.mm,172.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(214.mm)
  mat = model.materials["Battery 2 (optional 2nd pack, ghosted)"] || model.materials.add("Battery 2 (optional 2nd pack, ghosted)")
  mat.color = Sketchup::Color.new(106, 90, 205)
  mat.alpha = 0.28
  grp.material = mat

  # Battery Contactor (ML-RBS)
  grp = ents.add_group
  grp.name = "Battery Contactor (ML-RBS)"
  face = grp.entities.add_face([1560.mm,15.mm,364.mm], [1680.mm,15.mm,364.mm], [1680.mm,105.mm,364.mm], [1560.mm,105.mm,364.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Battery Contactor (ML-RBS)"] || model.materials.add("Battery Contactor (ML-RBS)")
  mat.color = Sketchup::Color.new(196, 43, 28)
  mat.alpha = 1.0
  grp.material = mat

  # MRBF Main Fuse (on + post)
  grp = ents.add_group
  grp.name = "MRBF Main Fuse (on + post)"
  face = grp.entities.add_face([1695.mm,20.mm,364.mm], [1735.mm,20.mm,364.mm], [1735.mm,60.mm,364.mm], [1695.mm,60.mm,364.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(38.mm)
  mat = model.materials["MRBF Main Fuse (on + post)"] || model.materials.add("MRBF Main Fuse (on + post)")
  mat.color = Sketchup::Color.new(34, 34, 34)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Battery Bank"
  inst.layer = model.layers["Battery"]

  # ═══ External Power Panel ═══
  defn = model.definitions.add("External Power Panel")
  ents = defn.entities
  # Ext. Power Panel (exterior)
  grp = ents.add_group
  grp.name = "Ext. Power Panel (exterior)"
  face = grp.entities.add_face([1250.mm,-65.mm,1830.mm], [1590.mm,-65.mm,1830.mm], [1590.mm,-40.mm,1830.mm], [1250.mm,-40.mm,1830.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(240.mm)
  mat = model.materials["Ext. Power Panel (exterior)"] || model.materials.add("Ext. Power Panel (exterior)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.55
  grp.material = mat

  # Ext. Power Panel (interior face)
  grp = ents.add_group
  grp.name = "Ext. Power Panel (interior face)"
  face = grp.entities.add_face([1250.mm,0.mm,1830.mm], [1590.mm,0.mm,1830.mm], [1590.mm,20.mm,1830.mm], [1250.mm,20.mm,1830.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(240.mm)
  mat = model.materials["Ext. Power Panel (interior face)"] || model.materials.add("Ext. Power Panel (interior face)")
  mat.color = Sketchup::Color.new(245, 197, 24)
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
  mat = model.materials["PV run (array -> panel)"] || model.materials.add("PV run (array -> panel)")
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
  mat = model.materials["PV run (array -> panel)"] || model.materials.add("PV run (array -> panel)")
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
  mat = model.materials["PV run (array -> panel)"] || model.materials.add("PV run (array -> panel)")
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

  # NEMA 5-15R shore inlet
  grp = ents.add_group
  grp.name = "NEMA 5-15R shore inlet"
  face = grp.entities.add_face([1472.28.mm,-95.mm,2018.72.mm], [1532.28.mm,-95.mm,2018.72.mm], [1532.28.mm,-65.mm,2018.72.mm], [1472.28.mm,-65.mm,2018.72.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(45.mm)
  mat = model.materials["NEMA 5-15R shore inlet"] || model.materials.add("NEMA 5-15R shore inlet")
  mat.color = Sketchup::Color.new(255, 240, 204)
  mat.alpha = 1.0
  grp.material = mat

  # GFCI AC outlet (Cct E cooler)
  grp = ents.add_group
  grp.name = "GFCI AC outlet (Cct E cooler)"
  ge = grp.entities
  circle = ge.add_circle([1510.78.mm,-85.mm,1908.mm], [0,1,0], 12.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop collar (safety yellow)
  grp = ents.add_group
  grp.name = "E-stop collar (safety yellow)"
  ge = grp.entities
  circle = ge.add_circle([1420.mm,-77.mm,1950.mm], [0,1,0], 35.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(12.mm)
  mat = model.materials["E-stop collar (safety yellow)"] || model.materials.add("E-stop collar (safety yellow)")
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
  mat = model.materials["Battery Contactor (ML-RBS)"] || model.materials.add("Battery Contactor (ML-RBS)")
  mat.color = Sketchup::Color.new(196, 43, 28)
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
  face = grp.entities.add_face([1910.mm,0.mm,1180.mm], [2030.mm,0.mm,1180.mm], [2030.mm,72.mm,1180.mm], [1910.mm,72.mm,1180.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(235.mm)
  mat = model.materials["Cct E Inverter (12->120V AC)"] || model.materials.add("Cct E Inverter (12->120V AC)")
  mat.color = Sketchup::Color.new(64, 72, 72)
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
  face = grp.entities.add_face([0.mm,0.mm,2363.mm], [5893.mm,0.mm,2363.mm], [5893.mm,40.mm,2363.mm], [0.mm,40.mm,2363.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Cable Trunking (40x25 PVC)"] || model.materials.add("Cable Trunking (40x25 PVC)")
  mat.color = Sketchup::Color.new(154, 160, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit A (exhaust fan)
  grp = ents.add_group
  grp.name = "Circuit A (exhaust fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -150.8356070868639.mm, 559.5514456448177.mm)
  circle = ge.add_circle([2005.mm,175.mm,1800.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Busbar (+)"] || model.materials.add("Busbar (+)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit A (exhaust fan) elbow
  grp = ents.add_group
  grp.name = "Circuit A (exhaust fan) elbow"
  ge = grp.entities
  arc = ge.add_arc([2021.mm,24.164392913136098.mm,2359.5514456448177.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.965535,0.260275], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2005.mm,24.164392913136098.mm,2359.5514456448177.mm], [0.000000,-0.260275,0.965535], 8.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Busbar (+)"] || model.materials.add("Busbar (+)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit A (exhaust fan)
  grp = ents.add_group
  grp.name = "Circuit A (exhaust fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3696.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2021.mm,20.mm,2375.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Busbar (+)"] || model.materials.add("Busbar (+)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit A (exhaust fan) elbow
  grp = ents.add_group
  grp.name = "Circuit A (exhaust fan) elbow"
  ge = grp.entities
  arc = ge.add_arc([5717.mm,35.22548277815922.mm,2370.0822084049873.mm], [0.000000,-0.951593,0.307362], [-0.000000,0.307362,0.951593], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5717.mm,20.mm,2375.mm], [1.000000,0.000000,0.000000], 8.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Busbar (+)"] || model.materials.add("Busbar (+)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit A (exhaust fan)
  grp = ents.add_group
  grp.name = "Circuit A (exhaust fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 1145.7745172218408.mm, -370.08220840498734.mm)
  circle = ge.add_circle([5733.mm,35.22548277815921.mm,2370.0822084049873.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Busbar (+)"] || model.materials.add("Busbar (+)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit B (intake fan)
  grp = ents.add_group
  grp.name = "Circuit B (intake fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -150.8356070868639.mm, 559.5514456448177.mm)
  circle = ge.add_circle([2005.mm,175.mm,1800.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Circuit B (intake fan)"] || model.materials.add("Circuit B (intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit B (intake fan) elbow
  grp = ents.add_group
  grp.name = "Circuit B (intake fan) elbow"
  ge = grp.entities
  arc = ge.add_arc([1989.mm,24.164392913136098.mm,2359.5514456448177.mm], [1.000000,0.000000,0.000000], [-0.000000,-0.965535,-0.260275], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2005.mm,24.164392913136098.mm,2359.5514456448177.mm], [0.000000,-0.260275,0.965535], 8.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Circuit B (intake fan)"] || model.materials.add("Circuit B (intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit B (intake fan)
  grp = ents.add_group
  grp.name = "Circuit B (intake fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1643.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1989.mm,20.mm,2375.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Circuit B (intake fan)"] || model.materials.add("Circuit B (intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit B (intake fan) elbow
  grp = ents.add_group
  grp.name = "Circuit B (intake fan) elbow"
  ge = grp.entities
  arc = ge.add_arc([346.mm,23.05273035191477.mm,2359.293923551743.mm], [0.000000,-0.190796,0.981630], [-0.000000,-0.981630,-0.190796], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([346.mm,20.mm,2375.mm], [-1.000000,0.000000,0.000000], 8.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Circuit B (intake fan)"] || model.materials.add("Circuit B (intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit B (intake fan)
  grp = ents.add_group
  grp.name = "Circuit B (intake fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 341.94726964808524.mm, -1759.2939235517429.mm)
  circle = ge.add_circle([330.mm,23.05273035191477.mm,2359.293923551743.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Circuit B (intake fan)"] || model.materials.add("Circuit B (intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit C (water pumps)
  grp = ents.add_group
  grp.name = "Circuit C (water pumps)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -150.8356070868639.mm, 559.5514456448177.mm)
  circle = ge.add_circle([2005.mm,175.mm,1800.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Circuit C (water pumps)"] || model.materials.add("Circuit C (water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit C (water pumps) elbow
  grp = ents.add_group
  grp.name = "Circuit C (water pumps) elbow"
  ge = grp.entities
  arc = ge.add_arc([2021.mm,24.164392913136098.mm,2359.5514456448177.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.965535,0.260275], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2005.mm,24.164392913136098.mm,2359.5514456448177.mm], [0.000000,-0.260275,0.965535], 8.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Circuit C (water pumps)"] || model.materials.add("Circuit C (water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit C (water pumps)
  grp = ents.add_group
  grp.name = "Circuit C (water pumps)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2777.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2021.mm,20.mm,2375.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Circuit C (water pumps)"] || model.materials.add("Circuit C (water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit C (water pumps) elbow
  grp = ents.add_group
  grp.name = "Circuit C (water pumps) elbow"
  ge = grp.entities
  arc = ge.add_arc([4798.mm,32.7775135502749.mm,2365.3700909935483.mm], [0.000000,-0.798595,0.601869], [-0.000000,0.601869,0.798595], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4798.mm,20.mm,2375.mm], [1.000000,0.000000,0.000000], 8.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Circuit C (water pumps)"] || model.materials.add("Circuit C (water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit C (water pumps)
  grp = ents.add_group
  grp.name = "Circuit C (water pumps)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 1148.222486449725.mm, -865.3700909935483.mm)
  circle = ge.add_circle([4814.mm,32.7775135502749.mm,2365.3700909935483.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Circuit C (water pumps)"] || model.materials.add("Circuit C (water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D (safelight)
  grp = ents.add_group
  grp.name = "Circuit D (safelight)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -150.8356070868639.mm, 559.5514456448177.mm)
  circle = ge.add_circle([2005.mm,175.mm,1800.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Circuit D (safelight)"] || model.materials.add("Circuit D (safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D (safelight) elbow
  grp = ents.add_group
  grp.name = "Circuit D (safelight) elbow"
  ge = grp.entities
  arc = ge.add_arc([1989.mm,24.164392913136098.mm,2359.5514456448177.mm], [1.000000,0.000000,0.000000], [-0.000000,-0.965535,-0.260275], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2005.mm,24.164392913136098.mm,2359.5514456448177.mm], [0.000000,-0.260275,0.965535], 8.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Circuit D (safelight)"] || model.materials.add("Circuit D (safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D (safelight)
  grp = ents.add_group
  grp.name = "Circuit D (safelight)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1473.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1989.mm,20.mm,2375.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Circuit D (safelight)"] || model.materials.add("Circuit D (safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D (safelight) elbow
  grp = ents.add_group
  grp.name = "Circuit D (safelight) elbow"
  ge = grp.entities
  arc = ge.add_arc([516.mm,35.998285041712805.mm,2374.7657443189414.mm], [0.000000,-0.999893,0.014641], [-0.000000,-0.014641,-0.999893], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([516.mm,20.mm,2375.mm], [-1.000000,0.000000,0.000000], 8.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Circuit D (safelight)"] || model.materials.add("Circuit D (safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D (safelight)
  grp = ents.add_group
  grp.name = "Circuit D (safelight)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 1145.0017149582873.mm, -16.765744318941415.mm)
  circle = ge.add_circle([500.mm,35.998285041712805.mm,2374.7657443189414.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Circuit D (safelight)"] || model.materials.add("Circuit D (safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit E (cooler / inverter)
  grp = ents.add_group
  grp.name = "Circuit E (cooler / inverter)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -150.8356070868639.mm, 559.5514456448177.mm)
  circle = ge.add_circle([2005.mm,175.mm,1800.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Circuit E (cooler / inverter)"] || model.materials.add("Circuit E (cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit E (cooler / inverter) elbow
  grp = ents.add_group
  grp.name = "Circuit E (cooler / inverter) elbow"
  ge = grp.entities
  arc = ge.add_arc([1989.mm,24.164392913136098.mm,2359.5514456448177.mm], [1.000000,0.000000,0.000000], [-0.000000,-0.965535,-0.260275], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2005.mm,24.164392913136098.mm,2359.5514456448177.mm], [0.000000,-0.260275,0.965535], 8.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Circuit E (cooler / inverter)"] || model.materials.add("Circuit E (cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit E (cooler / inverter)
  grp = ents.add_group
  grp.name = "Circuit E (cooler / inverter)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.690000000000055.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1989.mm,20.mm,2375.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Circuit E (cooler / inverter)"] || model.materials.add("Circuit E (cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit E (cooler / inverter) elbow
  grp = ents.add_group
  grp.name = "Circuit E (cooler / inverter) elbow"
  ge = grp.entities
  arc = ge.add_arc([1979.31.mm,20.138230700692226.mm,2365.691026250258.mm], [0.000000,-0.014848,0.999890], [-0.000000,-0.999890,-0.014848], 9.310000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1979.31.mm,20.mm,2375.mm], [-1.000000,0.000000,0.000000], 8.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Circuit E (cooler / inverter)"] || model.materials.add("Circuit E (cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit E (cooler / inverter)
  grp = ents.add_group
  grp.name = "Circuit E (cooler / inverter)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 15.861769299307774.mm, -1068.191026250258.mm)
  circle = ge.add_circle([1970.mm,20.138230700692226.mm,2365.691026250258.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Circuit E (cooler / inverter)"] || model.materials.add("Circuit E (cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit F (actuators (spare))
  grp = ents.add_group
  grp.name = "Circuit F (actuators (spare))"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -150.8356070868639.mm, 559.5514456448177.mm)
  circle = ge.add_circle([2005.mm,175.mm,1800.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Circuit F (actuators (spare))"] || model.materials.add("Circuit F (actuators (spare))")
  mat.color = Sketchup::Color.new(127, 140, 141)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit F (actuators (spare)) elbow
  grp = ents.add_group
  grp.name = "Circuit F (actuators (spare)) elbow"
  ge = grp.entities
  arc = ge.add_arc([1989.mm,24.164392913136098.mm,2359.5514456448177.mm], [1.000000,0.000000,0.000000], [-0.000000,-0.965535,-0.260275], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2005.mm,24.164392913136098.mm,2359.5514456448177.mm], [0.000000,-0.260275,0.965535], 8.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Circuit F (actuators (spare))"] || model.materials.add("Circuit F (actuators (spare))")
  mat.color = Sketchup::Color.new(127, 140, 141)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit F (actuators (spare))
  grp = ents.add_group
  grp.name = "Circuit F (actuators (spare))"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1713.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1989.mm,20.mm,2375.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Circuit F (actuators (spare))"] || model.materials.add("Circuit F (actuators (spare))")
  mat.color = Sketchup::Color.new(127, 140, 141)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit F (actuators (spare)) elbow
  grp = ents.add_group
  grp.name = "Circuit F (actuators (spare)) elbow"
  ge = grp.entities
  arc = ge.add_arc([276.mm,22.92652665892788.mm,2359.2699192082628.mm], [0.000000,-0.182908,0.983130], [-0.000000,-0.983130,-0.182908], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([276.mm,20.mm,2375.mm], [-1.000000,0.000000,0.000000], 8.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Circuit F (actuators (spare))"] || model.materials.add("Circuit F (actuators (spare))")
  mat.color = Sketchup::Color.new(127, 140, 141)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit F (actuators (spare))
  grp = ents.add_group
  grp.name = "Circuit F (actuators (spare))"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 197.07347334107212.mm, -1059.2699192082628.mm)
  circle = ge.add_circle([260.mm,22.92652665892788.mm,2359.2699192082628.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Circuit F (actuators (spare))"] || model.materials.add("Circuit F (actuators (spare))")
  mat.color = Sketchup::Color.new(127, 140, 141)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G (white LED)
  grp = ents.add_group
  grp.name = "Circuit G (white LED)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -150.8356070868639.mm, 559.5514456448177.mm)
  circle = ge.add_circle([2005.mm,175.mm,1800.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Circuit G (white LED)"] || model.materials.add("Circuit G (white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G (white LED) elbow
  grp = ents.add_group
  grp.name = "Circuit G (white LED) elbow"
  ge = grp.entities
  arc = ge.add_arc([1989.mm,24.164392913136098.mm,2359.5514456448177.mm], [1.000000,0.000000,0.000000], [-0.000000,-0.965535,-0.260275], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2005.mm,24.164392913136098.mm,2359.5514456448177.mm], [0.000000,-0.260275,0.965535], 8.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Circuit G (white LED)"] || model.materials.add("Circuit G (white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G (white LED)
  grp = ents.add_group
  grp.name = "Circuit G (white LED)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-973.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1989.mm,20.mm,2375.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Circuit G (white LED)"] || model.materials.add("Circuit G (white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G (white LED) elbow
  grp = ents.add_group
  grp.name = "Circuit G (white LED) elbow"
  ge = grp.entities
  arc = ge.add_arc([1016.mm,35.995675091149536.mm,2374.62800755602.mm], [0.000000,-0.999730,0.023250], [-0.000000,-0.023250,-0.999730], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1016.mm,20.mm,2375.mm], [-1.000000,0.000000,0.000000], 8.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Circuit G (white LED)"] || model.materials.add("Circuit G (white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G (white LED)
  grp = ents.add_group
  grp.name = "Circuit G (white LED)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 1145.0043249088505.mm, -26.62800755601984.mm)
  circle = ge.add_circle([1000.mm,35.995675091149536.mm,2374.62800755602.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Circuit G (white LED)"] || model.materials.add("Circuit G (white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
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
anc = Geom::Point3d.new(2000.mm, 40.mm, 2040.mm)
txt = entities.add_text("MPPT 100/50", anc, Geom::Vector3d.new(-380.mm, -700.mm, 280.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(2000.mm, 40.mm, 1800.mm)
txt = entities.add_text("FUSE BLOCK
(Cct A-G)", anc, Geom::Vector3d.new(420.mm, -700.mm, 240.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(2000.mm, 40.mm, 1710.mm)
txt = entities.add_text("+/- BUSBARS", anc, Geom::Vector3d.new(420.mm, -640.mm, -120.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(2150.mm, 165.mm, 1620.mm)
txt = entities.add_text("MAIN DISCONNECT", anc, Geom::Vector3d.new(360.mm, -760.mm, -260.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1620.mm, 40.mm, 414.mm)
txt = entities.add_text("BATTERY CONTACTOR
+ MRBF main fuse", anc, Geom::Vector3d.new(-300.mm, -760.mm, 900.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1660.mm, 60.mm, 250.mm)
txt = entities.add_text("BATTERY 1x 100Ah
(2nd pack ghosted)", anc, Geom::Vector3d.new(-320.mm, -640.mm, 760.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1970.mm, 36.mm, 1415.mm)
txt = entities.add_text("CCT-E INVERTER
12->120V AC (cooler)", anc, Geom::Vector3d.new(-430.mm, -820.mm, 480.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1420.mm, -80.mm, 2090.mm)
txt = entities.add_text("EXTERNAL PANEL
MC4 PV / shore / GFCI cooler / E-STOP", anc, Geom::Vector3d.new(220.mm, -520.mm, 380.mm))
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

zoom = {"Power Core" => [2060.mm, 90.mm, 1800.mm, 1400.mm], "External Panel" => [1420.mm, -65.mm, 1950.mm, 1600.mm]}
[["Combined", ["Context", "Solar Array", "Power Core", "Battery", "External Panel", "Inverter", "Circuit Runs"]], ["Power Core", ["Power Core", "Battery", "Inverter"]], ["Distribution", ["Circuit Runs", "Power Core", "Battery"]], ["External Panel", ["External Panel", "Solar Array"]], ["Labeled", ["Context", "Solar Array", "Power Core", "Battery", "External Panel", "Inverter", "Circuit Runs", "Labels"]]].each { |name, tags|
  model.layers.each { |l| l.visible = (l == default_layer || l.name == "Context" || tags.include?(l.name)) }
  page = model.pages.add(name)
  if zoom[name]
    zx, zy, zz, zd = zoom[name]
    tgt = Geom::Point3d.new(zx, zy, zz)
    zeye = tgt.offset(dir, zd)
    page.camera = Sketchup::Camera.new(zeye, tgt, Z_AXIS)
  else
    page.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
  end
  page.use_camera = true
}
model.layers.each { |l| l.visible = true }

model.commit_operation
{ success: true, model: "Electrical",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
