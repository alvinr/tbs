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

# ── Sketchfab upload metadata (stamped every regen; keeps the stable model UID) ──
model.name = "TBS-001 Electrical Model"
model.description = "There are a number of discrete systems, color-coded in the diagram below. This view is shown from the optical axis, looking through the container wall. Each of these sub-systems, has a detailed breakdown of construction, schematic and other diagrams to show how each system it built, installed, used and maintained. The 3d model below provides a simply way to view the whole system."
model.set_attribute("sketchfab", "model_title", "TBS-001 Electrical Model")
model.set_attribute("sketchfab", "model_description", "There are a number of discrete systems, color-coded in the diagram below. This view is shown from the optical axis, looking through the container wall. Each of these sub-systems, has a detailed breakdown of construction, schematic and other diagrams to show how each system it built, installed, used and maintained. The 3d model below provides a simply way to view the whole system.")
model.set_attribute("sketchfab", "model_id", "6930c96be025469fb8ef702393d7c35f")
model.set_attribute("sketchfab", "model_tags", "sketchup")

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
  mat.color = Sketchup::Color.new(41, 128, 185)
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
  face = grp.entities.add_face([1925.mm,120.mm,1970.mm], [2110.mm,120.mm,1970.mm], [2110.mm,190.mm,1970.mm], [1925.mm,190.mm,1970.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["MPPT Controller (100/50)"] || model.materials.add("MPPT Controller (100/50)")
  mat.color = Sketchup::Color.new(58, 91, 160)
  mat.alpha = 1.0
  grp.material = mat

  # MPPT backing panel (18mm ply)
  grp = ents.add_group
  grp.name = "MPPT backing panel (18mm ply)"
  face = grp.entities.add_face([1918.mm,102.mm,1868.mm], [2123.mm,102.mm,1868.mm], [2123.mm,120.mm,1868.mm], [1918.mm,120.mm,1868.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(232.mm)
  mat = model.materials["MPPT backing panel (18mm ply)"] || model.materials.add("MPPT backing panel (18mm ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # PV feed (MC4 bulkheads -> MPPT)
  grp = ents.add_group
  grp.name = "PV feed (MC4 bulkheads -> MPPT)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 80.mm, 0.mm)
  circle = ge.add_circle([1328.2.mm,22.mm,1884.mm], vec, 9.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV feed (MC4 bulkheads -> MPPT) elbow
  grp = ents.add_group
  grp.name = "PV feed (MC4 bulkheads -> MPPT) elbow"
  ge = grp.entities
  arc = ge.add_arc([1346.2.mm,102.mm,1884.mm], [-1.000000,0.000000,0.000000], [0.000000,0.000000,-1.000000], 18.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1328.2.mm,102.mm,1884.mm], [0.000000,1.000000,0.000000], 9.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV feed (MC4 bulkheads -> MPPT)
  grp = ents.add_group
  grp.name = "PV feed (MC4 bulkheads -> MPPT)"
  ge = grp.entities
  vec = Geom::Vector3d.new(585.8.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1346.2.mm,120.mm,1884.mm], vec, 9.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV feed (MC4 bulkheads -> MPPT) elbow
  grp = ents.add_group
  grp.name = "PV feed (MC4 bulkheads -> MPPT) elbow"
  ge = grp.entities
  arc = ge.add_arc([1932.mm,120.mm,1902.mm], [0.000000,0.000000,-1.000000], [0.000000,-1.000000,0.000000], 18.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1932.mm,120.mm,1884.mm], [1.000000,0.000000,0.000000], 9.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV feed (MC4 bulkheads -> MPPT)
  grp = ents.add_group
  grp.name = "PV feed (MC4 bulkheads -> MPPT)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 52.4225745704216.mm)
  circle = ge.add_circle([1950.mm,120.mm,1902.mm], vec, 9.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV feed (MC4 bulkheads -> MPPT) elbow
  grp = ents.add_group
  grp.name = "PV feed (MC4 bulkheads -> MPPT) elbow"
  ge = grp.entities
  arc = ge.add_arc([1950.mm,138.mm,1954.4225745704216.mm], [0.000000,-1.000000,0.000000], [-1.000000,0.000000,0.000000], 18.mm, 0.0, 1.292497, 8)
  circle = ge.add_circle([1950.mm,120.mm,1954.4225745704216.mm], [0.000000,0.000000,1.000000], 9.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV feed (MC4 bulkheads -> MPPT)
  grp = ents.add_group
  grp.name = "PV feed (MC4 bulkheads -> MPPT)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 21.9449803021528.mm, 6.269994372043584.mm)
  circle = ge.add_circle([1950.mm,133.0550196978472.mm,1971.7300056279564.mm], vec, 9.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (+) (array -> panel MC4, bonded pair)"] || model.materials.add("PV cord (+) (array -> panel MC4, bonded pair)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse Block base (Blue Sea 5026)
  grp = ents.add_group
  grp.name = "Fuse Block base (Blue Sea 5026)"
  face = grp.entities.add_face([1925.mm,25.mm,1770.mm], [2075.mm,25.mm,1770.mm], [2075.mm,70.mm,1770.mm], [1925.mm,70.mm,1770.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Fuse Block base (Blue Sea 5026)"] || model.materials.add("Fuse Block base (Blue Sea 5026)")
  mat.color = Sketchup::Color.new(43, 43, 48)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse A (5A — exhaust fan)
  grp = ents.add_group
  grp.name = "Fuse A (5A — exhaust fan)"
  face = grp.entities.add_face([1929.2142857142858.mm,43.mm,1798.mm], [1942.2142857142858.mm,43.mm,1798.mm], [1942.2142857142858.mm,52.mm,1798.mm], [1929.2142857142858.mm,52.mm,1798.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse B (5A — intake fan)
  grp = ents.add_group
  grp.name = "Fuse B (5A — intake fan)"
  face = grp.entities.add_face([1950.642857142857.mm,43.mm,1798.mm], [1963.642857142857.mm,43.mm,1798.mm], [1963.642857142857.mm,52.mm,1798.mm], [1950.642857142857.mm,52.mm,1798.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse C (15A — water pumps)
  grp = ents.add_group
  grp.name = "Fuse C (15A — water pumps)"
  face = grp.entities.add_face([1972.0714285714287.mm,43.mm,1798.mm], [1985.0714285714287.mm,43.mm,1798.mm], [1985.0714285714287.mm,52.mm,1798.mm], [1972.0714285714287.mm,52.mm,1798.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse D (5A — safelight)
  grp = ents.add_group
  grp.name = "Fuse D (5A — safelight)"
  face = grp.entities.add_face([1993.5.mm,43.mm,1798.mm], [2006.5.mm,43.mm,1798.mm], [2006.5.mm,52.mm,1798.mm], [1993.5.mm,52.mm,1798.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse D (5A — safelight)"] || model.materials.add("Fuse D (5A — safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse E (40A — cooler / inverter)
  grp = ents.add_group
  grp.name = "Fuse E (40A — cooler / inverter)"
  face = grp.entities.add_face([2014.9285714285713.mm,43.mm,1798.mm], [2027.9285714285713.mm,43.mm,1798.mm], [2027.9285714285713.mm,52.mm,1798.mm], [2014.9285714285713.mm,52.mm,1798.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse E (40A — cooler / inverter)"] || model.materials.add("Fuse E (40A — cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse F (20A — actuators (spare))
  grp = ents.add_group
  grp.name = "Fuse F (20A — actuators (spare))"
  face = grp.entities.add_face([2036.357142857143.mm,43.mm,1798.mm], [2049.357142857143.mm,43.mm,1798.mm], [2049.357142857143.mm,52.mm,1798.mm], [2036.357142857143.mm,52.mm,1798.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse F (20A — actuators (spare))"] || model.materials.add("Fuse F (20A — actuators (spare))")
  mat.color = Sketchup::Color.new(127, 140, 141)
  mat.alpha = 1.0
  grp.material = mat

  # Fuse G (10A — white LED)
  grp = ents.add_group
  grp.name = "Fuse G (10A — white LED)"
  face = grp.entities.add_face([2057.785714285714.mm,43.mm,1798.mm], [2070.785714285714.mm,43.mm,1798.mm], [2070.785714285714.mm,52.mm,1798.mm], [2057.785714285714.mm,52.mm,1798.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse G (10A — white LED)"] || model.materials.add("Fuse G (10A — white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Busbar (+)
  grp = ents.add_group
  grp.name = "Busbar (+)"
  face = grp.entities.add_face([1925.mm,30.mm,1705.mm], [2045.mm,30.mm,1705.mm], [2045.mm,50.mm,1705.mm], [1925.mm,50.mm,1705.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
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

  # Main feed (disconnect → busbar +)
  grp = ents.add_group
  grp.name = "Main feed (disconnect → busbar +)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -63.mm, 0.mm)
  circle = ge.add_circle([2150.mm,130.mm,1655.mm], vec, 11.mm, 16)
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
  arc = ge.add_arc([2150.mm,67.mm,1677.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 22.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2150.mm,67.mm,1655.mm], [0.000000,-1.000000,0.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Main feed (disconnect → busbar +)
  grp = ents.add_group
  grp.name = "Main feed (disconnect → busbar +)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 14.279999999999973.mm)
  circle = ge.add_circle([2150.mm,45.mm,1677.mm], vec, 11.mm, 16)
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
  arc = ge.add_arc([2136.28.mm,45.mm,1691.28.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 13.72.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2150.mm,45.mm,1691.28.mm], [0.000000,0.000000,1.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Main feed (disconnect → busbar +)
  grp = ents.add_group
  grp.name = "Main feed (disconnect → busbar +)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-91.2800000000002.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2136.28.mm,45.mm,1705.mm], vec, 11.mm, 16)
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
  face = grp.entities.add_face([1925.mm,95.mm,1695.mm], [1970.mm,95.mm,1695.mm], [1970.mm,125.mm,1695.mm], [1925.mm,125.mm,1695.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(45.mm)
  mat = model.materials["Charge-line Fuse (60A, MPPT -> battery)"] || model.materials.add("Charge-line Fuse (60A, MPPT -> battery)")
  mat.color = Sketchup::Color.new(34, 34, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Interior E-stop collar (safety yellow)
  grp = ents.add_group
  grp.name = "Interior E-stop collar (safety yellow)"
  ge = grp.entities
  circle = ge.add_circle([2060.mm,165.mm,1580.mm], [0,1,0], 30.mm, 24)
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
  circle = ge.add_circle([2060.mm,177.mm,1580.mm], [0,1,0], 24.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(26.mm)
  mat = model.materials["Interior E-stop button (red mushroom)"] || model.materials.add("Interior E-stop button (red mushroom)")
  mat.color = Sketchup::Color.new(196, 43, 28)
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
  mat = model.materials["Interior E-stop button (red mushroom)"] || model.materials.add("Interior E-stop button (red mushroom)")
  mat.color = Sketchup::Color.new(196, 43, 28)
  mat.alpha = 1.0
  grp.material = mat

  # MRBF Main Fuse (on + post)
  grp = ents.add_group
  grp.name = "MRBF Main Fuse (on + post)"
  face = grp.entities.add_face([1695.mm,20.mm,364.mm], [1735.mm,20.mm,364.mm], [1735.mm,60.mm,364.mm], [1695.mm,60.mm,364.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(38.mm)
  mat = model.materials["Charge-line Fuse (60A, MPPT -> battery)"] || model.materials.add("Charge-line Fuse (60A, MPPT -> battery)")
  mat.color = Sketchup::Color.new(34, 34, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF → main disconnect)
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF → main disconnect)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1161.mm)
  circle = ge.add_circle([1715.mm,45.mm,402.mm], vec, 11.mm, 16)
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
  arc = ge.add_arc([1737.mm,45.mm,1563.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 22.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1715.mm,45.mm,1563.mm], [0.000000,0.000000,1.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF → main disconnect)
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF → main disconnect)"
  ge = grp.entities
  vec = Geom::Vector3d.new(391.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1737.mm,45.mm,1585.mm], vec, 11.mm, 16)
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
  arc = ge.add_arc([2128.mm,67.mm,1585.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 22.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2128.mm,45.mm,1585.mm], [1.000000,0.000000,0.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF → main disconnect)
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF → main disconnect)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 63.mm, 0.mm)
  circle = ge.add_circle([2150.mm,67.mm,1585.mm], vec, 11.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1300.mm)
  circle = ge.add_circle([1600.mm,60.mm,364.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Battery − cable (2/0 AWG)"] || model.materials.add("Battery − cable (2/0 AWG)")
  mat.color = Sketchup::Color.new(32, 32, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Battery − cable (2/0 AWG) elbow
  grp = ents.add_group
  grp.name = "Battery − cable (2/0 AWG) elbow"
  ge = grp.entities
  arc = ge.add_arc([1622.mm,60.mm,1664.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 22.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1600.mm,60.mm,1664.mm], [0.000000,0.000000,1.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Battery − cable (2/0 AWG)"] || model.materials.add("Battery − cable (2/0 AWG)")
  mat.color = Sketchup::Color.new(32, 32, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Battery − cable (2/0 AWG)
  grp = ents.add_group
  grp.name = "Battery − cable (2/0 AWG)"
  ge = grp.entities
  vec = Geom::Vector3d.new(328.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1622.mm,60.mm,1686.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Battery − cable (2/0 AWG)"] || model.materials.add("Battery − cable (2/0 AWG)")
  mat.color = Sketchup::Color.new(32, 32, 32)
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
  face = grp.entities.add_face([1386.mm,22.mm,1834.8.mm], [1456.mm,22.mm,1834.8.mm], [1456.mm,67.mm,1834.8.mm], [1386.mm,67.mm,1834.8.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Main Disconnect (m-Series)"] || model.materials.add("Main Disconnect (m-Series)")
  mat.color = Sketchup::Color.new(212, 58, 47)
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
  vec = Geom::Vector3d.new(-33.67800000000011.mm, -19.200000000000003.mm, -126.70000000000005.mm)
  circle = ge.add_circle([1510.78.mm,-75.mm,1908.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.050258649607485.mm, -20.41799152611219.mm, -2.8371845833123643.mm)
  circle = ge.add_circle([1477.1019999999999.mm,-94.2.mm,1781.3.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.762396429380487.mm, 18.318390346148945.mm, -11.70767515789953.mm)
  circle = ge.add_circle([1455.0517413503924.mm,-114.61799152611219.mm,1778.4628154166876.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.171567754890248.mm, 17.630856254124225.mm, -15.838877930046692.mm)
  circle = ge.add_circle([1444.289344921012.mm,-96.29960117996325.mm,1766.755140258788.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.376114608425723.mm, 5.607886209617149.mm, -16.995197614962308.mm)
  circle = ge.add_circle([1449.4609126759021.mm,-78.66874492583902.mm,1750.9162623287414.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.25850650487473.mm, -10.676223251416957.mm, -14.496257541061368.mm)
  circle = ge.add_circle([1465.8370272843279.mm,-73.06085871622187.mm,1733.921064713779.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.887943866135629.mm, -21.639927907802658.mm, -9.812430090784801.mm)
  circle = ge.add_circle([1482.0955337892026.mm,-83.73708196763883.mm,1719.4248071727177.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.04515225631053.mm, -20.83220130062095.mm, -5.699671919088587.mm)
  circle = ge.add_circle([1486.9834776553382.mm,-105.37700987544149.mm,1709.612377081933.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.165773333888183.mm, -8.728308486511821.mm, -4.577923421695459.mm)
  circle = ge.add_circle([1475.9383253990277.mm,-126.20921117606244.mm,1703.9127051628443.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.930563533923987.mm, 7.5498391690757956.mm, -7.107219638194692.mm)
  circle = ge.add_circle([1453.7725520651395.mm,-134.93751966257426.mm,1699.3347817411488.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.477919930264989.mm, 18.42420536185068.mm, -11.799326679909655.mm)
  circle = ge.add_circle([1431.8419885312155.mm,-127.38768049349846.mm,1692.2275621029542.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.453440115823014.mm, 17.496330243416097.mm, -15.89341619339234.mm)
  circle = ge.add_circle([1421.3640686009505.mm,-108.96347513164778.mm,1680.4282354230445.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.48952958034465.mm, 5.3121740641793735.mm, -16.98053239185174.mm)
  circle = ge.add_circle([1426.8175087167735.mm,-91.46714488823169.mm,1664.5348192296522.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.13673089789404.mm, -10.95912497346545.mm, -14.421017825550507.mm)
  circle = ge.add_circle([1443.3070382971182.mm,-86.15497082405231.mm,1647.5542868378004.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.602630254572659.mm, -21.743560281180137.mm, -9.720886812338904.mm)
  circle = ge.add_circle([1459.4437691950122.mm,-97.11409579751776.mm,1633.13326901225.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.326125795203325.mm, -20.695587200932792.mm, -5.645688997788056.mm)
  circle = ge.add_circle([1464.046399449585.mm,-118.8576560786979.mm,1623.412382199911.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.2770824147442.mm, -8.431831433687648.mm, -4.593264322951427.mm)
  circle = ge.add_circle([1452.7202736543816.mm,-139.5532432796307.mm,1617.766693202123.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.806714069824466.mm, 7.831732546622135.mm, -7.182857800000875.mm)
  circle = ge.add_circle([1430.4431912396374.mm,-147.98507471331834.mm,1613.1734288791715.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.191784749771614.mm, 18.525649447145852.mm, -11.890756727631242.mm)
  circle = ge.add_circle([1408.636477169813.mm,-140.1533421666962.mm,1605.9905710791706.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.733499525599427.mm, 17.35763549730781.mm, -15.946840831728423.mm)
  circle = ge.add_circle([1398.4446924200413.mm,-121.62769271955035.mm,1594.0998143515394.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.59872670616255.mm, 5.014948255656421.mm, -16.96451664820256.mm)
  circle = ge.add_circle([1404.1781919456407.mm,-104.27005722224254.mm,1578.152973519811.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.01081432383444.mm, -11.2399946493219.mm, -14.344985338118704.mm)
  circle = ge.add_circle([1420.7769186518033.mm,-99.25510896658612.mm,1561.1884568716084.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.31568909342468.mm, -21.84281055185005.mm, -9.629574976332606.mm)
  circle = ge.add_circle([1436.7877329756377.mm,-110.49510361590802.mm,1546.8434715334897.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.60525581858792.mm, -20.554819364315364.mm, -5.592825552922022.mm)
  circle = ge.add_circle([1441.1034220690624.mm,-132.33791416775807.mm,1537.213896557157.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.38416163660486.mm, -8.133873061944655.mm, -4.609954036476665.mm)
  circle = ge.add_circle([1429.4981662504745.mm,-152.89273353207344.mm,1531.621071004235.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.678737245577622.mm, 8.111563219370822.mm, -7.259280470906788.mm)
  circle = ge.add_circle([1407.1140046138696.mm,-161.0266065940181.mm,1527.0111169677584.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.904053240154099.mm, 18.62270049616356.mm, -11.981945377371176.mm)
  circle = ge.add_circle([1385.435267368292.mm,-152.91504337464727.mm,1519.7518364968516.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(6.011684955948567.mm, 17.21480223903177.mm, -15.999140203191473.mm)
  circle = ge.add_circle([1375.531214128138.mm,-134.2923428784837.mm,1507.7698911194805.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.703682190528752.mm, 4.716273553081294.mm, -16.94715387403562.mm)
  circle = ge.add_circle([1381.5428990840865.mm,-117.07754063945194.mm,1491.770750916289.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(15.880784221412796.mm, -11.518771074148674.mm, -14.268176647147584.mm)
  circle = ge.add_circle([1398.2465812746152.mm,-112.36126708637065.mm,1474.8235970422534.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.027182910578858.mm, -21.937657091999625.mm, -9.538514480699178.mm)
  circle = ge.add_circle([1414.127365496028.mm,-123.88003816051932.mm,1460.5554203951058.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.882481500717631.mm, -20.409928465752188.mm, -5.541093104063748.mm)
  circle = ge.add_circle([1418.1545484066069.mm,-145.81769525251894.mm,1451.0169059144066.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.48698766563757.mm, -7.834498299950155.mm, -4.627988925383988.mm)
  circle = ge.add_circle([1406.2720669058892.mm,-166.22762371827113.mm,1445.4758128103429.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.546660948853287.mm, 8.38927020889551.mm, -7.336470997504421.mm)
  circle = ge.add_circle([1383.7850792402517.mm,-174.0621220182213.mm,1440.8478238849589.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.614788101524482.mm, 18.71533736032785.mm, -12.072872758040148.mm)
  circle = ge.add_circle([1362.2384182913984.mm,-165.67285180932578.mm,1433.5113528874544.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(6.28793578696127.mm, 17.06786159365069.mm, -16.050302911127574.mm)
  circle = ge.add_circle([1352.623630189874.mm,-146.95751444899793.mm,1421.4384801294143.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.804373162397496.mm, 4.416215041218436.mm, -16.928447852905492.mm)
  circle = ge.add_circle([1358.9115659768352.mm,-129.88965285534724.mm,1405.3881772182867.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(15.746668925732365.mm, -11.79539349925247.mm, -14.190608490163186.mm)
  circle = ge.add_circle([1375.7159391392327.mm,-125.4734378141288.mm,1388.4597293653812.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.737174574957862.mm, -22.028079233441417.mm, -9.447725168602119.mm)
  circle = ge.add_circle([1391.462608064965.mm,-137.26883131338127.mm,1374.269120875218.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-12.157742430824555.mm, -20.260946078690495.mm, -5.490502924327757.mm)
  circle = ge.add_circle([1395.199782639923.mm,-159.2969105468227.mm,1364.821395706616.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.585538094828053.mm, -7.53377238501983.mm, -4.6473650596567495.mm)
  circle = ge.add_circle([1383.0420402090983.mm,-179.55785662551318.mm,1359.3308927822882.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.41051396064495.mm, 8.664792999545284.mm, -7.414412559062157.mm)
  circle = ge.add_circle([1360.4565021142703.mm,-187.091629010533.mm,1354.6835277226314.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.324052368192497.mm, 18.80353985296594.mm, -12.163519055481174.mm)
  circle = ge.add_circle([1339.0459881536253.mm,-178.42683601098773.mm,1347.2691151635693.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(6.562191820301905.mm, 16.916845581276448.mm, -16.10031780657596.mm)
  circle = ge.add_circle([1329.7219357854328.mm,-159.6232961580218.mm,1335.105596108088.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.900777680009696.mm, 4.11483810638066.mm, -16.908402661076252.mm)
  circle = ge.add_circle([1336.2841276057347.mm,-142.70645057674534.mm,1319.0052783015121.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(15.608497662108675.mm, -12.06980164532203.mm, -14.112297770188206.mm)
  circle = ge.add_circle([1353.1849052857444.mm,-138.59161247036468.mm,1302.0968756404359.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.4457272828217356.mm, -22.114057272117464.mm, -9.357226824109603.mm)
  circle = ge.add_circle([1368.793402947853.mm,-150.6614141156867.mm,1287.9845778702477.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-12.43097862628315.mm, -20.107904668161297.mm, -5.441066037915334.mm)
  circle = ge.add_circle([1372.2391302306748.mm,-172.77547138780417.mm,1278.627351046138.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.679791448867718.mm, -7.23176084890153.mm, -4.668078217005814.mm)
  circle = ge.add_circle([1359.8081516043917.mm,-192.88337605596547.mm,1273.1862850082227.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.27032594899856.mm, 8.938071551632532.mm, -7.493088171187765.mm)
  circle = ge.add_circle([1337.128360155524.mm,-200.115136904867.mm,1268.518206791217.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.031909394925606.mm, 18.887288753707054.mm, -12.2538645167906.mm)
  circle = ge.add_circle([1315.8580342065254.mm,-191.17706535323447.mm,1261.0251186200292.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(6.834393292323057.mm, 16.761787110091234.mm, -16.149173990695544.mm)
  circle = ge.add_circle([1306.8261248115998.mm,-172.2897765995274.mm,1248.7712541032386.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.992874735676196.mm, 3.812208422181044.mm, -16.887022666633584.mm)
  circle = ge.add_circle([1313.6605181039229.mm,-155.52798948943618.mm,1232.622080112543.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(15.466300539701024.mm, -12.341935715563608.mm, -14.033261552057866.mm)
  circle = ge.add_circle([1330.653392839599.mm,-151.71578106725514.mm,1215.7350574459094.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.1529045439970105.mm, -22.1955724723922.mm, -9.26703916788756.mm)
  circle = ge.add_circle([1346.1196933793.mm,-164.05771678281874.mm,1201.7017958938516.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-12.702130545682166.mm, -19.950837583705464.mm, -5.39279321771005.mm)
  circle = ge.add_circle([1349.272597923297.mm,-186.25328925521094.mm,1192.434756725964.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.76972718883212.mm, -6.928529503495241.mm, -4.690123883787692.mm)
  circle = ge.add_circle([1336.570467377615.mm,-206.2041268389164.mm,1187.041963508254.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.126127462545583.mm, 9.209046314515518.mm, -7.572480689531403.mm)
  circle = ge.add_circle([1313.8007401887828.mm,-213.13265634241165.mm,1182.3518396244663.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.738422843147646.mm, 18.966565812671746.mm, -12.343889454619102.mm)
  circle = ge.add_circle([1292.6746127262372.mm,-203.92361002789613.mm,1174.7793589349349.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(7.10448088709245.mm, 16.602719969177087.mm, -16.196860817144625.mm)
  circle = ge.add_circle([1283.9361898830896.mm,-184.95704421522439.mm,1162.4354694803158.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(17.080644260355257.mm, 3.508391935220999.mm, -16.864312528532082.mm)
  circle = ge.add_circle([1291.040670770182.mm,-168.3543242460473.mm,1146.2386086631711.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(15.320108544950472.mm, -12.611736408732071.mm, -13.953517058703255.mm)
  circle = ge.add_circle([1308.1213150305373.mm,-164.8459323108263.mm,1129.374296134639.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.85877016803488.mm, -22.272607071134843.mm, -9.177181852895046.mm)
  circle = ge.add_circle([1323.4414235754878.mm,-177.45766871955837.mm,1115.4207790759358.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-12.971139101797917.mm, -19.78977905210604.mm, -5.3456949829337645.mm)
  circle = ge.add_circle([1326.3001937435226.mm,-199.7302757906932.mm,1106.2435972230408.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.855325716655216.mm, -6.624144426511975.mm, -4.713497255990205.mm)
  circle = ge.add_circle([1313.3290546417247.mm,-219.52005484279925.mm,1100.897902240107.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-20.97794992384911.mm, 9.477658239575618.mm, -7.65257281352001.mm)
  circle = ge.add_circle([1290.4737289250695.mm,-226.14419926931123.mm,1096.1844049841168.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.443656667063124.mm, 19.041353754447215.mm, -12.433574251464506.mm)
  circle = ge.add_circle([1269.4957790012204.mm,-216.6665410297356.mm,1088.5318321705968.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(7.372395749315729.mm, 16.43967882115294.mm, -16.243367894397124.mm)
  circle = ge.add_circle([1261.0521223341573.mm,-197.6251872752884.mm,1076.0982579191323.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(17.16406712802518.mm, 3.2034548507211014.mm, -16.8402771955798.mm)
  circle = ge.add_circle([1268.424518083473.mm,-181.18550845413546.mm,1059.8548900247351.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(15.169953534828892.mm, -12.879144932052299.mm, -13.873081667396036.mm)
  circle = ge.add_circle([1285.5885852114982.mm,-177.98205360341436.mm,1043.0146128291553.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.563388250309117.mm, -22.345144281592383.mm, -9.087674460109383.mm)
  circle = ge.add_circle([1300.758538746327.mm,-190.86119853546666.mm,1029.1415311617593.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-13.237945674472485.mm, -19.624764169928937.mm, -5.299781596850721.mm)
  circle = ge.add_circle([1303.3219269966362.mm,-213.20634281705904.mm,1020.0538567016499.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.93656837940125.mm, -6.318671947074648.mm, -4.738193240277724.mm)
  circle = ge.add_circle([1290.0839813221637.mm,-232.83110698698798.mm,1014.7540751047992.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-20.825825622553793.mm, 9.743848793084396.mm, -7.733347090129087.mm)
  circle = ge.add_circle([1267.1474129427625.mm,-239.14977893406262.mm,1010.0158818645215.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.147675099722164.mm, 19.111636281853123.mm, -12.52289936394368.mm)
  circle = ge.add_circle([1246.3215873202087.mm,-229.40593014097823.mm,1002.2825347743924.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(7.638079497163062.mm, 16.27269919462117.mm, -16.288685088008606.mm)
  circle = ge.add_circle([1238.1739122204865.mm,-210.2942938591251.mm,989.7596354104487.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(17.243125159851843.mm, 2.89746361809307.mm, -16.814921905362098.mm)
  circle = ge.add_circle([1245.8119917176496.mm,-194.02159466450394.mm,973.4709503224401.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(15.015868229896569.mm, -13.144103014032112.mm, -13.791972905963462.mm)
  circle = ge.add_circle([1263.0551168775014.mm,-191.12413104641087.mm,956.656028417078.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.266823158046691.mm, -22.413168297044564.mm, -8.998536494253699.mm)
  circle = ge.add_circle([1278.070985107398.mm,-204.26823406044298.mm,942.8640555111145.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-13.502492123384627.mm, -19.45582889587729.mm, -5.255063064533033.mm)
  circle = ge.add_circle([1280.3378082654447.mm,-226.68140235748754.mm,933.8655190168608.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-23.01343747332976.mm, -6.012178631263652.mm, -4.764206455102112.mm)
  circle = ge.add_circle([1266.83531614206.mm,-246.13723125336483.mm,928.6104559523278.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-20.669787708352032.mm, 10.007559968960038.mm, -7.814785917684617.mm)
  circle = ge.add_circle([1243.8218786687303.mm,-252.14940988462848.mm,923.8462494972257.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-7.850542639022706.mm, 19.177398079491383.mm, -12.611845327054198.mm)
  circle = ge.add_circle([1223.1520909603782.mm,-242.14184991566844.mm,916.0314635795411.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(7.901474234990701.mm, 16.101817476425225.mm, -16.332802522824636.mm)
  circle = ge.add_circle([1215.3015483213555.mm,-222.96445183617706.mm,903.4196182524869.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(17.317801128152723.mm, 2.5904849164599.mm, -16.788252183097597.mm)
  circle = ge.add_circle([1223.2030225563462.mm,-206.86263435975184.mm,887.0868157296622.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(14.85788620716994.mm, -13.406552917158479.mm, -13.71020844896725.mm)
  circle = ge.add_circle([1240.520823684499.mm,-204.27214944329194.mm,870.2985635465647.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.9691395163033576.mm, -22.476664294251577.mm, -8.909787379549698.mm)
  circle = ge.add_circle([1255.378709891669.mm,-217.67870236045042.mm,856.5883550975974.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-13.764720800721761.mm, -19.28301004295247.mm, -5.2115491306796.mm)
  circle = ge.add_circle([1257.3478494079723.mm,-240.155366654702.mm,847.6785677180477.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-23.085916247752266.mm, -5.704731267612146.mm, -4.791531231875069.mm)
  circle = ge.add_circle([1243.5831286072505.mm,-259.43837669765446.mm,842.4670185873681.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-20.509870183758267.mm, 10.268734301405289.mm, -7.896871549699085.mm)
  circle = ge.add_circle([1220.4972123594982.mm,-265.1431079652666.mm,837.675487355493.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-7.5523240336560775.mm, 19.23862481708639.mm, -12.70039275841441.mm)
  circle = ge.add_circle([1199.98734217574.mm,-254.87437366386132.mm,829.778615805794.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.162522565957715.mm, 15.927070903720391.mm, -16.375710585132197.mm)
  circle = ge.add_circle([1192.435018142084.mm,-235.63574884677493.mm,817.0782230473795.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(17.388078760146072.mm, 2.282585640125916.mm, -16.760273840434934.mm)
  circle = ge.add_circle([1200.5975407080416.mm,-219.70867794305454.mm,800.7025124622473.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(14.69604189280949.mm, -13.666437450481851.mm, -13.627806113854149.mm)
  circle = ge.add_circle([1217.9856194681877.mm,-217.42609230292862.mm,783.9422386218124.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.6704021938789992.mm, -22.535618436680352.mm, -8.821446455483056.mm)
  circle = ge.add_circle([1232.6816613609972.mm,-231.09252975341047.mm,770.3144325079583.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-26.674063554876284.mm, 5.828148190090815.mm, 6.207013947524729.mm)
  circle = ge.add_circle([1234.3520635548762.mm,-253.62814819009083.mm,761.4929860524752.mm], vec, 5.mm, 8)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E cooler cord (panel GFCI -> cooler, flexible)
  grp = ents.add_group
  grp.name = "Cct E cooler cord (panel GFCI -> cooler, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-33.677999999999884.mm, -19.19999999999999.mm, -126.69999999999993.mm)
  circle = ge.add_circle([1207.6779999999999.mm,-247.8.mm,767.6999999999999.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
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
  face = grp.entities.add_face([1910.mm,0.mm,1180.mm], [2030.mm,0.mm,1180.mm], [2030.mm,72.mm,1180.mm], [1910.mm,72.mm,1180.mm])
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 479.mm)
  circle = ge.add_circle([1970.mm,30.mm,1415.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E AC line (inverter -> panel GFCI) elbow
  grp = ents.add_group
  grp.name = "Cct E AC line (inverter -> panel GFCI) elbow"
  ge = grp.entities
  arc = ge.add_arc([1956.mm,30.mm,1894.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 14.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1970.mm,30.mm,1894.mm], [0.000000,0.000000,1.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E AC line (inverter -> panel GFCI)
  grp = ents.add_group
  grp.name = "Cct E AC line (inverter -> panel GFCI)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-439.3399999999999.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1956.mm,30.mm,1908.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E AC line (inverter -> panel GFCI) elbow
  grp = ents.add_group
  grp.name = "Cct E AC line (inverter -> panel GFCI) elbow"
  ge = grp.entities
  arc = ge.add_arc([1516.66.mm,24.119999999999997.mm,1908.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 5.880000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1516.66.mm,30.mm,1908.mm], [-1.000000,0.000000,0.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # Cct E AC line (inverter -> panel GFCI)
  grp = ents.add_group
  grp.name = "Cct E AC line (inverter -> panel GFCI)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -6.120000000000001.mm, 0.mm)
  circle = ge.add_circle([1510.78.mm,24.12.mm,1908.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
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
  mat = model.materials["Cable Trunking (40x25 PVC)"] || model.materials.add("Cable Trunking (40x25 PVC)")
  mat.color = Sketchup::Color.new(154, 160, 160)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit A (exhaust fan)
  grp = ents.add_group
  grp.name = "Circuit A (exhaust fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 115.5.mm, 0.mm)
  circle = ge.add_circle([1935.7142857142858.mm,47.5.mm,1840.mm], vec, 6.mm, 16)
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
  arc = ge.add_arc([1935.7142857142858.mm,163.mm,1852.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1935.7142857142858.mm,163.mm,1840.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit A (exhaust fan)
  grp = ents.add_group
  grp.name = "Circuit A (exhaust fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 511.mm)
  circle = ge.add_circle([1935.7142857142858.mm,175.mm,1852.mm], vec, 6.mm, 16)
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
  arc = ge.add_arc([1935.7142857142858.mm,163.mm,2363.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1935.7142857142858.mm,175.mm,2363.mm], [0.000000,0.000000,1.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit A (exhaust fan)
  grp = ents.add_group
  grp.name = "Circuit A (exhaust fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -131.mm, 0.mm)
  circle = ge.add_circle([1935.7142857142858.mm,163.mm,2375.mm], vec, 6.mm, 16)
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
  arc = ge.add_arc([1947.7142857142858.mm,32.mm,2375.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.000000,1.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1935.7142857142858.mm,32.mm,2375.mm], [0.000000,-1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
  mat.color = Sketchup::Color.new(192, 57, 43)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit A (exhaust fan)
  grp = ents.add_group
  grp.name = "Circuit A (exhaust fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3658.285714285714.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1947.7142857142858.mm,20.mm,2375.mm], vec, 6.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 115.5.mm, 0.mm)
  circle = ge.add_circle([1957.142857142857.mm,47.5.mm,1840.mm], vec, 6.mm, 16)
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
  arc = ge.add_arc([1957.142857142857.mm,163.mm,1852.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1957.142857142857.mm,163.mm,1840.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit B (intake fan)
  grp = ents.add_group
  grp.name = "Circuit B (intake fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 511.mm)
  circle = ge.add_circle([1957.142857142857.mm,175.mm,1852.mm], vec, 6.mm, 16)
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
  arc = ge.add_arc([1957.142857142857.mm,163.mm,2363.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1957.142857142857.mm,175.mm,2363.mm], [0.000000,0.000000,1.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit B (intake fan)
  grp = ents.add_group
  grp.name = "Circuit B (intake fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -131.mm, 0.mm)
  circle = ge.add_circle([1957.142857142857.mm,163.mm,2375.mm], vec, 6.mm, 16)
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
  arc = ge.add_arc([1945.142857142857.mm,32.mm,2375.mm], [1.000000,0.000000,0.000000], [-0.000000,-0.000000,-1.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1957.142857142857.mm,32.mm,2375.mm], [0.000000,-1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(230, 126, 34)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit B (intake fan)
  grp = ents.add_group
  grp.name = "Circuit B (intake fan)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1644.162857142857.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1945.142857142857.mm,20.mm,2375.mm], vec, 6.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 115.5.mm, 0.mm)
  circle = ge.add_circle([2021.4285714285713.mm,47.5.mm,1840.mm], vec, 6.mm, 16)
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
  arc = ge.add_arc([2021.4285714285713.mm,163.mm,1852.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2021.4285714285713.mm,163.mm,1840.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse E (40A — cooler / inverter)"] || model.materials.add("Fuse E (40A — cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit E (cooler / inverter)
  grp = ents.add_group
  grp.name = "Circuit E (cooler / inverter)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 511.mm)
  circle = ge.add_circle([2021.4285714285713.mm,175.mm,1852.mm], vec, 6.mm, 16)
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
  arc = ge.add_arc([2021.4285714285713.mm,163.mm,2363.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2021.4285714285713.mm,175.mm,2363.mm], [0.000000,0.000000,1.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse E (40A — cooler / inverter)"] || model.materials.add("Fuse E (40A — cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit E (cooler / inverter)
  grp = ents.add_group
  grp.name = "Circuit E (cooler / inverter)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -131.mm, 0.mm)
  circle = ge.add_circle([2021.4285714285713.mm,163.mm,2375.mm], vec, 6.mm, 16)
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
  arc = ge.add_arc([2009.4285714285713.mm,32.mm,2375.mm], [1.000000,0.000000,0.000000], [-0.000000,-0.000000,-1.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2021.4285714285713.mm,32.mm,2375.mm], [0.000000,-1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse E (40A — cooler / inverter)"] || model.materials.add("Fuse E (40A — cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit E (cooler / inverter)
  grp = ents.add_group
  grp.name = "Circuit E (cooler / inverter)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-31.588571428571413.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2009.4285714285713.mm,20.mm,2375.mm], vec, 6.mm, 16)
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
  arc = ge.add_arc([1977.84.mm,27.84.mm,2375.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,-1.000000], 7.840000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1977.84.mm,20.mm,2375.mm], [-1.000000,0.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse E (40A — cooler / inverter)"] || model.materials.add("Fuse E (40A — cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit E (cooler / inverter)
  grp = ents.add_group
  grp.name = "Circuit E (cooler / inverter)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 4.161599999999996.mm, 0.mm)
  circle = ge.add_circle([1970.mm,27.84.mm,2375.mm], vec, 6.mm, 16)
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
  arc = ge.add_arc([1970.mm,32.001599999999996.mm,2371.0016.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 3.9984000000000006.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1970.mm,32.001599999999996.mm,2375.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse E (40A — cooler / inverter)"] || model.materials.add("Fuse E (40A — cooler / inverter)")
  mat.color = Sketchup::Color.new(22, 160, 133)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit E (cooler / inverter)
  grp = ents.add_group
  grp.name = "Circuit E (cooler / inverter)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1073.5016.mm)
  circle = ge.add_circle([1970.mm,36.mm,2371.0016.mm], vec, 6.mm, 16)
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
  mat.color = Sketchup::Color.new(43, 43, 48)
  mat.alpha = 1.0
  grp.material = mat

  # Master pump switch (Cct C, on EP)
  grp = ents.add_group
  grp.name = "Master pump switch (Cct C, on EP)"
  face = grp.entities.add_face([1953.5714285714287.mm,175.mm,1796.mm], [2003.5714285714287.mm,175.mm,1796.mm], [2003.5714285714287.mm,221.mm,1796.mm], [1953.5714285714287.mm,221.mm,1796.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(84.mm)
  mat = model.materials["Battery − cable (2/0 AWG)"] || model.materials.add("Battery − cable (2/0 AWG)")
  mat.color = Sketchup::Color.new(32, 32, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Master switch lever (OFF cutoff)
  grp = ents.add_group
  grp.name = "Master switch lever (OFF cutoff)"
  face = grp.entities.add_face([1970.5714285714287.mm,221.mm,1836.mm], [1986.5714285714287.mm,221.mm,1836.mm], [1986.5714285714287.mm,255.mm,1836.mm], [1970.5714285714287.mm,255.mm,1836.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Master switch lever (OFF cutoff)"] || model.materials.add("Master switch lever (OFF cutoff)")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit C (water pumps)
  grp = ents.add_group
  grp.name = "Circuit C (water pumps)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 115.5.mm, 0.mm)
  circle = ge.add_circle([1978.5714285714287.mm,47.5.mm,1840.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit C (water pumps) elbow
  grp = ents.add_group
  grp.name = "Circuit C (water pumps) elbow"
  ge = grp.entities
  arc = ge.add_arc([1978.5714285714287.mm,163.mm,1852.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1978.5714285714287.mm,163.mm,1840.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit C (water pumps)
  grp = ents.add_group
  grp.name = "Circuit C (water pumps)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 511.mm)
  circle = ge.add_circle([1978.5714285714287.mm,175.mm,1852.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit C (water pumps) elbow
  grp = ents.add_group
  grp.name = "Circuit C (water pumps) elbow"
  ge = grp.entities
  arc = ge.add_arc([1978.5714285714287.mm,163.mm,2363.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1978.5714285714287.mm,175.mm,2363.mm], [0.000000,0.000000,1.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit C (water pumps)
  grp = ents.add_group
  grp.name = "Circuit C (water pumps)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -131.mm, 0.mm)
  circle = ge.add_circle([1978.5714285714287.mm,163.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit C (water pumps) elbow
  grp = ents.add_group
  grp.name = "Circuit C (water pumps) elbow"
  ge = grp.entities
  arc = ge.add_arc([1990.5714285714287.mm,32.mm,2375.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.000000,1.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1978.5714285714287.mm,32.mm,2375.mm], [0.000000,-1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit C (water pumps)
  grp = ents.add_group
  grp.name = "Circuit C (water pumps)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2871.4285714285716.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1990.5714285714287.mm,20.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit C (water pumps) elbow
  grp = ents.add_group
  grp.name = "Circuit C (water pumps) elbow"
  ge = grp.entities
  arc = ge.add_arc([4862.mm,32.mm,2375.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4862.mm,20.mm,2375.mm], [1.000000,0.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit C (water pumps)
  grp = ents.add_group
  grp.name = "Circuit C (water pumps)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 1137.mm, 0.mm)
  circle = ge.add_circle([4874.mm,32.mm,2375.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit C (water pumps) elbow
  grp = ents.add_group
  grp.name = "Circuit C (water pumps) elbow"
  ge = grp.entities
  arc = ge.add_arc([4874.mm,1169.mm,2363.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4874.mm,1169.mm,2375.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit C (water pumps)
  grp = ents.add_group
  grp.name = "Circuit C (water pumps)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -118.mm)
  circle = ge.add_circle([4874.mm,1181.mm,2363.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
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
  mat.color = Sketchup::Color.new(41, 128, 185)
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
  mat.color = Sketchup::Color.new(41, 128, 185)
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
  mat.color = Sketchup::Color.new(41, 128, 185)
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
  mat.color = Sketchup::Color.new(41, 128, 185)
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
  mat.color = Sketchup::Color.new(41, 128, 185)
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
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
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
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G feed (white LED)
  grp = ents.add_group
  grp.name = "Circuit G feed (white LED)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 115.5.mm, 0.mm)
  circle = ge.add_circle([2064.285714285714.mm,47.5.mm,1840.mm], vec, 6.mm, 16)
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
  arc = ge.add_arc([2064.285714285714.mm,163.mm,1852.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2064.285714285714.mm,163.mm,1840.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse G (10A — white LED)"] || model.materials.add("Fuse G (10A — white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G feed (white LED)
  grp = ents.add_group
  grp.name = "Circuit G feed (white LED)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 511.mm)
  circle = ge.add_circle([2064.285714285714.mm,175.mm,1852.mm], vec, 6.mm, 16)
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
  arc = ge.add_arc([2064.285714285714.mm,163.mm,2363.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2064.285714285714.mm,175.mm,2363.mm], [0.000000,0.000000,1.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse G (10A — white LED)"] || model.materials.add("Fuse G (10A — white LED)")
  mat.color = Sketchup::Color.new(241, 196, 15)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit G feed (white LED)
  grp = ents.add_group
  grp.name = "Circuit G feed (white LED)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -143.mm, 0.mm)
  circle = ge.add_circle([2064.285714285714.mm,163.mm,2375.mm], vec, 6.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 115.5.mm, 0.mm)
  circle = ge.add_circle([2000.mm,47.5.mm,1840.mm], vec, 6.mm, 16)
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
  arc = ge.add_arc([2000.mm,163.mm,1852.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2000.mm,163.mm,1840.mm], [0.000000,1.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse D (5A — safelight)"] || model.materials.add("Fuse D (5A — safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D feed (safelight)
  grp = ents.add_group
  grp.name = "Circuit D feed (safelight)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 511.mm)
  circle = ge.add_circle([2000.mm,175.mm,1852.mm], vec, 6.mm, 16)
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
  arc = ge.add_arc([2000.mm,163.mm,2363.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2000.mm,175.mm,2363.mm], [0.000000,0.000000,1.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse D (5A — safelight)"] || model.materials.add("Fuse D (5A — safelight)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit D feed (safelight)
  grp = ents.add_group
  grp.name = "Circuit D feed (safelight)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -143.mm, 0.mm)
  circle = ge.add_circle([2000.mm,163.mm,2375.mm], vec, 6.mm, 16)
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
anc = Geom::Point3d.new(2000.mm, 40.mm, 2040.mm)
txt = entities.add_text("MPPT 100/50", anc, Geom::Vector3d.new(-380.mm, -700.mm, 280.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(2000.mm, 40.mm, 1840.mm)
txt = entities.add_text("FUSE STACK A-G
5/5/15/5/40/20/10 A", anc, Geom::Vector3d.new(420.mm, -700.mm, 240.mm))
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
anc = Geom::Point3d.new(1000.mm, -287.mm, 711.mm)
txt = entities.add_text("EVAP COOLER
(Hessaire MC18M, Cct E)", anc, Geom::Vector3d.new(-260.mm, -520.mm, 520.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4874.mm, 1181.mm, 2230.mm)
txt = entities.add_text("CCT-C PUMP DISTRIBUTION
dist block → pumps (master sw on EP)", anc, Geom::Vector3d.new(-350.mm, -700.mm, 250.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1392.8.mm, 35.mm, 1846.8.mm)
txt = entities.add_text("PV DISCONNECT
(load-break, array->MPPT)", anc, Geom::Vector3d.new(300.mm, -560.mm, 320.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1950.mm, 95.mm, 1715.mm)
txt = entities.add_text("60A CHARGE FUSE
(MPPT -> battery)", anc, Geom::Vector3d.new(440.mm, -680.mm, 160.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(2060.mm, 203.mm, 1580.mm)
txt = entities.add_text("INTERIOR E-STOP
(EP face, parallel)", anc, Geom::Vector3d.new(-340.mm, -560.mm, -160.mm))
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
