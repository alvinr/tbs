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
  face = grp.entities.add_face([1925.mm,25.mm,1970.mm], [2110.mm,25.mm,1970.mm], [2110.mm,95.mm,1970.mm], [1925.mm,95.mm,1970.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["MPPT Controller (100/50)"] || model.materials.add("MPPT Controller (100/50)")
  mat.color = Sketchup::Color.new(58, 91, 160)
  mat.alpha = 1.0
  grp.material = mat

  # PV feed (MC4 bulkheads -> MPPT)
  grp = ents.add_group
  grp.name = "PV feed (MC4 bulkheads -> MPPT)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 45.mm, 0.mm)
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
  arc = ge.add_arc([1346.2.mm,67.mm,1884.mm], [-1.000000,0.000000,0.000000], [0.000000,0.000000,-1.000000], 18.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1328.2.mm,67.mm,1884.mm], [0.000000,1.000000,0.000000], 9.mm, 16)
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
  circle = ge.add_circle([1346.2.mm,85.mm,1884.mm], vec, 9.mm, 16)
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
  arc = ge.add_arc([1932.mm,85.mm,1902.mm], [0.000000,0.000000,-1.000000], [0.000000,-1.000000,0.000000], 18.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1932.mm,85.mm,1884.mm], [1.000000,0.000000,0.000000], 9.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 66.mm)
  circle = ge.add_circle([1950.mm,85.mm,1902.mm], vec, 9.mm, 16)
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
  face = grp.entities.add_face([720.5.mm,-445.mm,0.mm], [1279.5.mm,-445.mm,0.mm], [1279.5.mm,-140.mm,0.mm], [720.5.mm,-140.mm,0.mm])
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
  vec = Geom::Vector3d.new(-31.12799999999993.mm, -21.75.mm, -126.70000000000005.mm)
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
  vec = Geom::Vector3d.new(-21.901326650630608.mm, -20.566527845868265.mm, -2.8402651823646465.mm)
  circle = ge.add_circle([1479.652.mm,-96.75.mm,1781.3.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-10.610611923501665.mm, 18.00578194965506.mm, -12.23572774020704.mm)
  circle = ge.add_circle([1457.7506733493694.mm,-117.31652784586826.mm,1778.4597348176353.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(5.349201903109588.mm, 17.33640082507287.mm, -16.041868587366935.mm)
  circle = ge.add_circle([1447.1400614258678.mm,-99.3107458962132.mm,1766.2240070774283.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.618233262568083.mm, 5.4142319997933726.mm, -16.76385150928786.mm)
  circle = ge.add_circle([1452.4892633289774.mm,-81.97434507114033.mm,1750.1821384900613.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.587583076153123.mm, -10.768782800898691.mm, -13.978258368658317.mm)
  circle = ge.add_circle([1469.1074965915454.mm,-76.56011307134696.mm,1733.4182869807735.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(5.275226623397657.mm, -21.72186232032992.mm, -9.318743678768442.mm)
  circle = ge.add_circle([1485.6950796676986.mm,-87.32889587224565.mm,1719.4400286121152.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-10.684528340752195.mm, -21.021402360756852.mm, -5.517952452222971.mm)
  circle = ge.add_circle([1490.9703062910962.mm,-109.05075819257557.mm,1710.1212849333467.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-21.931834770469095.mm, -9.078198582768067.mm, -4.804917942570455.mm)
  circle = ge.add_circle([1480.285777950344.mm,-130.07216055333242.mm,1704.6033324811237.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-21.870534510681864.mm, 7.103471012486693.mm, -7.597810351279804.mm)
  circle = ge.add_circle([1458.353943179875.mm,-139.1503591361005.mm,1699.7984145385533.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-10.53657805416151.mm, 18.033614085029072.mm, -12.258694395528437.mm)
  circle = ge.add_circle([1436.483408669193.mm,-132.0468881236138.mm,1692.2006041872735.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(5.423059185282455.mm, 17.30207787387853.mm, -16.05412198350723.mm)
  circle = ge.add_circle([1425.9468306150316.mm,-114.01327403858473.mm,1679.941909791745.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.64859920331105.mm, 5.337883191712649.mm, -16.75820545110082.mm)
  circle = ge.add_circle([1431.369889800314.mm,-96.7111961647062.mm,1663.8877878082378.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.55664909623715.mm, -10.842381517402174.mm, -13.95802407496626.mm)
  circle = ge.add_circle([1448.018489003625.mm,-91.37331297299355.mm,1647.129582357137.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(5.201134437478686.mm, -21.749547830860692.mm, -9.295787866476985.mm)
  circle = ge.add_circle([1464.5751380998622.mm,-102.21569449039572.mm,1633.1715582821707.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-10.758326215449642.mm, -20.986938066160562.mm, -5.505737915237205.mm)
  circle = ge.add_circle([1469.776272537341.mm,-123.96524232125641.mm,1623.8757704156938.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-21.962058420121593.mm, -9.001796605767709.mm, -4.810608086480215.mm)
  circle = ge.add_circle([1459.0179463218913.mm,-144.95218038741697.mm,1618.3700325004565.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-21.839458804888636.mm, 7.177003541685934.mm, -7.61806810250323.mm)
  circle = ge.add_circle([1437.0558879017697.mm,-153.95397699318468.mm,1613.5594244139763.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-10.462427824927772.mm, 18.061152868607735.mm, -12.281639280125319.mm)
  circle = ge.add_circle([1415.216429096881.mm,-146.77697345149875.mm,1605.941356311473.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(5.4967973803252335.mm, 17.267472362990418.mm, -16.066297616289376.mm)
  circle = ge.add_circle([1404.7540012719533.mm,-128.715820582891.mm,1593.6597170313478.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.67868045040359.mm, 5.261428327575942.mm, -16.752471242454476.mm)
  circle = ge.add_circle([1410.2507986522785.mm,-111.4483482199006.mm,1577.5934194150584.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.525431779179144.mm, -10.915847588096852.mm, -13.937742940925318.mm)
  circle = ge.add_circle([1426.929479102682.mm,-106.18691989232465.mm,1560.840948172604.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(5.126926438408191.mm, -21.77693978591975.mm, -9.272853994199295.mm)
  circle = ge.add_circle([1443.4549108818612.mm,-117.1027674804215.mm,1546.9032052316786.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-10.832004458878828.mm, -20.95219146661148.mm, -5.493601231564753.mm)
  circle = ge.add_circle([1448.5818373202694.mm,-138.87970726634126.mm,1537.6303512374793.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-21.991997153709463.mm, -8.92528913647294.mm, -4.81638633871421.mm)
  circle = ge.add_circle([1437.7498328613906.mm,-159.83189873295274.mm,1532.1367500059146.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-21.808099991700146.mm, 7.250402882920923.mm, -7.6383725445614346.mm)
  circle = ge.add_circle([1415.7578357076811.mm,-168.75718786942568.mm,1527.3203636672004.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-10.38816232971294.mm, 18.0883978941211.mm, -12.304562055500128.mm)
  circle = ge.add_circle([1393.949735715981.mm,-161.50678498650475.mm,1519.681991122639.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(5.57041540040359.mm, 17.23258480293157.mm, -16.07839530608976.mm)
  circle = ge.add_circle([1383.561573386268.mm,-143.41838709238365.mm,1507.3774290671388.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.70847656006754.mm, 5.184868535295422.mm, -16.746648967943884.mm)
  circle = ge.add_circle([1389.1319887866716.mm,-126.18580228945208.mm,1491.299033761049.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.493931585516748.mm, -10.989179929163086.mm, -13.917415265735826.mm)
  circle = ge.add_circle([1405.8404653467392.mm,-121.00093375415666.mm,1474.5523847931051.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(5.0526037209524475.mm, -21.80403778140314.mm, -9.249942400271038.mm)
  circle = ge.add_circle([1422.334396932256.mm,-131.99011368331975.mm,1460.6349695273693.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-10.905561984090355.mm, -20.91716307471404.mm, -5.4815425802541995.mm)
  circle = ge.add_circle([1427.3870006532084.mm,-153.7941514647229.mm,1451.3850271270983.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-22.021650529556382.mm, -8.84867730357206.mm, -4.822252614028002.mm)
  circle = ge.add_circle([1416.481438669118.mm,-174.71131453943693.mm,1445.903484546844.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-21.77645853374247.mm, 7.323667953356477.mm, -7.658723377910064.mm)
  circle = ge.add_circle([1394.4597881395616.mm,-183.559991843009.mm,1441.081231932816.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-10.313782664130258.mm, 18.115348759632553.mm, -12.327462383480452.mm)
  circle = ge.add_circle([1372.6833296058192.mm,-176.2363238896525.mm,1433.422508554906.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(5.643912159455795.mm, 17.19741570838619.mm, -16.090414874435737.mm)
  circle = ge.add_circle([1362.369546941689.mm,-158.12097513001996.mm,1421.0950461714256.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.737987092731146.mm, 5.108204944331419.mm, -16.740738713463315.mm)
  circle = ge.add_circle([1368.0134591011447.mm,-140.92355942163377.mm,1405.0046312969898.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.46214897996242.mm, -11.062377458754213.mm, -13.897041349284791.mm)
  circle = ge.add_circle([1384.7514461938758.mm,-135.81535447730235.mm,1388.2638925835265.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(4.978167381568028.mm, -21.83084141754324.mm, -9.227053422698646.mm)
  circle = ge.add_circle([1401.2135951738383.mm,-146.87773193605656.mm,1374.3668512342417.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-10.978997705915845.mm, -20.881853407230352.mm, -5.469562139203163.mm)
  circle = ge.add_circle([1406.1917625554063.mm,-168.7085733535998.mm,1365.139797811543.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-22.051018110196765.mm, -8.771962237292968.mm, -4.828206825877942.mm)
  circle = ge.add_circle([1395.2127648494904.mm,-189.59042676083016.mm,1359.67023567234.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-21.74453489781058.mm, 7.396797672138263.mm, -7.679120302320371.mm)
  circle = ge.add_circle([1373.1617467392937.mm,-198.36238899812312.mm,1354.842028846462.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-10.239289925477578.mm, 18.142005067545256.mm, -12.350339926226297.mm)
  circle = ge.add_circle([1351.417211841483.mm,-190.96559132598486.mm,1347.1629085441416.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(5.717286573210686.mm, 17.161965598192012.mm, -16.102356144006535.mm)
  circle = ge.add_circle([1341.1779219160055.mm,-172.8235862584396.mm,1334.8125686179153.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.767211613035442.mm, 5.031438685675283.mm, -16.73474056620421.mm)
  circle = ge.add_circle([1346.8952084892162.mm,-155.6616206602476.mm,1318.7102124739088.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.430084431393198.mm, -11.135439097012153.mm, -13.876621492142021.mm)
  circle = ge.add_circle([1363.6624201022516.mm,-150.6301819745723.mm,1301.9754719077046.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(4.9036185183883845.mm, -21.857350298915634.mm, -9.204187399156126.mm)
  circle = ge.add_circle([1380.0925045336448.mm,-161.76562107158446.mm,1288.0988504155625.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-11.052310540982717.mm, -20.846262985071462.mm, -5.457660085153748.mm)
  circle = ge.add_circle([1384.9961230520332.mm,-183.6229713705001.mm,1278.8946630164064.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-22.080099462380076.mm, -8.695145069386626.mm, -4.834248886423893.mm)
  circle = ge.add_circle([1373.9438125110505.mm,-204.46923435557156.mm,1273.4370029312527.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-21.712329554863345.mm, 7.469790960408915.mm, -7.699563016883758.mm)
  circle = ge.add_circle([1351.8637130486704.mm,-213.16437942495818.mm,1268.6027540448288.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-10.164685212720315.mm, 18.168366424607967.mm, -12.373194346232822.mm)
  circle = ge.add_circle([1330.151383493807.mm,-205.69458846454927.mm,1260.903191027945.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(5.790537559199947.mm, 17.12623499533177.mm, -16.114218938636895.mm)
  circle = ge.add_circle([1319.9866982810868.mm,-187.5262220399413.mm,1248.5299966817122.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.796149689841286.mm, 4.954570891833413.mm, -16.72865461465517.mm)
  circle = ge.add_circle([1325.7772358402867.mm,-170.39998704460953.mm,1232.4157777430753.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.39773841284682.mm, -11.20836376608392.mm, -13.856155995554673.mm)
  circle = ge.add_circle([1342.573385530128.mm,-165.44541615277612.mm,1215.6871231284201.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(4.828958231207707.mm, -21.88356403444365.mm, -9.181344666976884.mm)
  circle = ge.add_circle([1358.9711239429748.mm,-176.65377991886004.mm,1201.8309671328655.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-11.125499407732605.mm, -20.81039233329068.mm, -5.445836593694139.mm)
  circle = ge.add_circle([1363.8000821741825.mm,-198.5373439533037.mm,1192.6496224658886.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-22.108894157079703.mm, -8.618226933110236.mm, -4.840378706529464.mm)
  circle = ge.add_circle([1352.67458276645.mm,-219.34773628659437.mm,1187.2037858721944.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-21.67984298001511.mm, 7.542646741323523.mm, -7.720051220015421.mm)
  circle = ge.add_circle([1330.5656886093702.mm,-227.9659632197046.mm,1182.363407165665.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-10.089969626475977.mm, 18.19443244192064.mm, -12.396025306336696.mm)
  circle = ge.add_circle([1308.8858456293551.mm,-220.42331647838108.mm,1174.6433559456495.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(5.863664036777436.mm, 17.09022442692725.mm, -16.12600308331912.mm)
  circle = ge.add_circle([1298.7958760028791.mm,-202.22888403646044.mm,1162.2473306393128.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.824800896235047.mm, 4.877602696809504.mm, -16.722480948600378.mm)
  circle = ge.add_circle([1304.6595400396566.mm,-185.1386596095332.mm,1146.1213275559937.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.36511140151265.mm, -11.281150390136986.mm, -13.835645161442926.mm)
  circle = ge.add_circle([1321.4843409358916.mm,-180.2610569127237.mm,1129.3988466073934.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(4.754187621463643.mm, -21.909482237404944.mm, -9.158525563152352.mm)
  circle = ge.add_circle([1337.8494523374043.mm,-191.54220730286067.mm,1115.5632014459504.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-11.198563226435226.mm, -20.774241981075562.mm, -5.434091839251778.mm)
  circle = ge.add_circle([1342.603639958868.mm,-213.45168954026562.mm,1106.404675882798.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-22.137401769497274.mm, -8.541208963210465.mm, -4.846596195763823.mm)
  circle = ge.add_circle([1331.4050767324327.mm,-234.22593152134118.mm,1100.9705840435463.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-21.64707565252911.mm, 7.615363940065805.mm, -7.740584609460029.mm)
  circle = ge.add_circle([1309.2676749629354.mm,-242.76714048455165.mm,1096.1239878477825.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-10.015144268998256.mm, 18.2202027349403.mm, -12.418832469720428.mm)
  circle = ge.add_circle([1287.6205993104063.mm,-235.15177654448584.mm,1088.3834032383224.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(5.936664927133734.mm, 17.053934424229766.mm, -16.137708404205796.mm)
  circle = ge.add_circle([1277.605455041408.mm,-216.93157380954554.mm,1075.964570768602.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.853164809535656.mm, 4.8005352360890186.mm, -16.71621965911777.mm)
  circle = ge.add_circle([1283.5421199685418.mm,-199.87763938531577.mm,1059.8268623643962.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.332203878725522.mm, -11.353797895375436.mm, -13.815089292395896.mm)
  circle = ge.add_circle([1300.3952847780774.mm,-195.07710414922676.mm,1043.1106427052785.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(4.679307792220925.mm, -21.935104525437595.mm, -9.135730424325516.mm)
  circle = ge.add_circle([1316.727488656803.mm,-206.4309020446022.mm,1029.2955534128826.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-11.27150091920521.mm, -20.737812461739423.mm, -5.422425995092226.mm)
  circle = ge.add_circle([1321.406796449024.mm,-228.3660065700398.mm,1020.159822988557.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-22.16562187906993.mm, -8.464092295906937.mm, -4.8529012624023835.mm)
  circle = ge.add_circle([1310.1352955298187.mm,-249.1038190317792.mm,1014.7373969934648.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-21.61402805580974.mm, 7.687941483864051.mm, -7.76116288229548.mm)
  circle = ge.add_circle([1287.9696736507487.mm,-257.56791132768615.mm,1009.8844957310624.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-9.940210244159971.mm, 18.245676923486826.mm, -12.441615499918498.mm)
  circle = ge.add_circle([1266.355645594939.mm,-249.8799698438221.mm,1002.123332848767.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(6.00953915331138.mm, 17.017365522613147.mm, -16.149334728612075.mm)
  circle = ge.add_circle([1256.415435350779.mm,-231.63429292033527.mm,989.6817173488485.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.881241011299608.mm, 4.723369646621592.mm, -16.709870838577785.mm)
  circle = ge.add_circle([1262.4249745040904.mm,-214.61692739772212.mm,973.5323826202364.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.299016329959386.mm, -11.426305210055546.mm, -13.794488691667766.mm)
  circle = ge.add_circle([1279.30621551539.mm,-209.89355775110053.mm,956.8225117816586.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(4.604319848155683.mm, -21.96043052054472.mm, -9.112959586784427.mm)
  circle = ge.add_circle([1295.6052318453494.mm,-221.31986296115608.mm,943.0280230899908.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-11.344311410018008.mm, -20.70110431271459.mm, -5.410839233318711.mm)
  circle = ge.add_circle([1300.209551693505.mm,-243.2802934817008.mm,933.9150635032064.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-22.193554069476022.mm, -8.386878068875149.mm, -4.859293813428053.mm)
  circle = ge.add_circle([1288.865240283487.mm,-263.9813977944154.mm,928.5042242698877.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-21.580700677397317.mm, 7.7603783020068136.mm, -7.781785734938126.mm)
  circle = ge.add_circle([1266.671686214011.mm,-272.36827586329053.mm,923.6449304564596.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-9.865168657436243.mm, 18.270854631747937.mm, -12.464374060819978.mm)
  circle = ge.add_circle([1245.0909855366137.mm,-264.6078975612837.mm,915.8631447215215.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(6.082285640221926.mm, 16.980518261566147.mm, -16.160881885019307.mm)
  circle = ge.add_circle([1235.2258168791775.mm,-246.33704292953578.mm,903.3987706607015.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.909029087329145.mm, 4.646107066804433.mm, -16.703434580642465.mm)
  circle = ge.add_circle([1241.3081025193994.mm,-229.35652466796964.mm,887.2378887756822.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.265549244817976.mm, -11.498671264502008.mm, -13.773843663171533.mm)
  circle = ge.add_circle([1258.2171316067286.mm,-224.7104176011652.mm,870.5344541950398.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(4.529224895539528.mm, -21.985459849100522.mm, -9.090213386459709.mm)
  circle = ge.add_circle([1274.4826808515465.mm,-236.2090888656672.mm,856.7606105318682.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-11.416993624725137.mm, -20.6641180755434.mm, -5.399331724866215.mm)
  circle = ge.add_circle([1279.011905747086.mm,-258.19454871476773.mm,847.6703971454085.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-22.221197928641914.mm, -8.309567421230383.mm, -4.865773754534416.mm)
  circle = ge.add_circle([1267.594912122361.mm,-278.85866679031113.mm,842.2710654205423.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-21.54709400895922.mm, 7.832673325858593.mm, -7.802452863145845.mm)
  circle = ge.add_circle([1245.373714193719.mm,-287.1682342115415.mm,837.4052916660079.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-9.790020615890171.mm, 18.29573548828614.mm, -12.487107816675916.mm)
  circle = ge.add_circle([1223.8266201847598.mm,-279.3355608856829.mm,829.602838802862.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(6.154903314661851.mm, 16.943393184683117.mm, -16.17234970307561.mm)
  circle = ge.add_circle([1214.0365995688696.mm,-261.0398253973968.mm,817.1157309861861.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.936528627675898.mm, 4.568748636465898.mm, -16.69691098026442.mm)
  circle = ge.add_circle([1220.1915028835315.mm,-244.09643221271367.mm,800.9433812831105.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(16.23180311703004.mm, -11.570894991123339.mm, -13.753154511476168.mm)
  circle = ge.add_circle([1237.1280315112074.mm,-239.52768357624777.mm,784.2464703028461.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(4.454024042222045.mm, -22.010192141856038.mm, -9.067492158918185.mm)
  circle = ge.add_circle([1253.3598346282374.mm,-251.0985785673711.mm,770.4933157913699.mm], vec, 5.mm, 6)
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
  vec = Geom::Vector3d.new(-27.18585867045931.mm, 2.3587707092271444.mm, 6.274176367548307.mm)
  circle = ge.add_circle([1257.8138586704595.mm,-273.10877070922714.mm,761.4258236324517.mm], vec, 5.mm, 8)
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
  vec = Geom::Vector3d.new(-31.128000000000156.mm, -21.75.mm, -126.70000000000005.mm)
  circle = ge.add_circle([1230.6280000000002.mm,-270.75.mm,767.7.mm], vec, 5.mm, 10)
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
  vec = Geom::Vector3d.new(0.mm, 111.5.mm, 0.mm)
  circle = ge.add_circle([1935.7142857142858.mm,47.5.mm,1840.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([1935.7142857142858.mm,159.mm,1856.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1935.7142857142858.mm,159.mm,1840.mm], [0.000000,1.000000,0.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 503.mm)
  circle = ge.add_circle([1935.7142857142858.mm,175.mm,1856.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([1935.7142857142858.mm,159.mm,2359.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1935.7142857142858.mm,175.mm,2359.mm], [0.000000,0.000000,1.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, -123.mm, 0.mm)
  circle = ge.add_circle([1935.7142857142858.mm,159.mm,2375.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([1951.7142857142858.mm,36.mm,2375.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.000000,1.000000], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1935.7142857142858.mm,36.mm,2375.mm], [0.000000,-1.000000,0.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(3650.285714285714.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1951.7142857142858.mm,20.mm,2375.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([5602.mm,36.mm,2375.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5602.mm,20.mm,2375.mm], [1.000000,0.000000,0.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 1129.mm, 0.mm)
  circle = ge.add_circle([5618.mm,36.mm,2375.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([5618.mm,1165.mm,2359.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5618.mm,1165.mm,2375.mm], [0.000000,1.000000,0.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -259.mm)
  circle = ge.add_circle([5618.mm,1181.mm,2359.mm], vec, 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 111.5.mm, 0.mm)
  circle = ge.add_circle([1957.142857142857.mm,47.5.mm,1840.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([1957.142857142857.mm,159.mm,1856.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1957.142857142857.mm,159.mm,1840.mm], [0.000000,1.000000,0.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 503.mm)
  circle = ge.add_circle([1957.142857142857.mm,175.mm,1856.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([1957.142857142857.mm,159.mm,2359.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1957.142857142857.mm,175.mm,2359.mm], [0.000000,0.000000,1.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, -123.mm, 0.mm)
  circle = ge.add_circle([1957.142857142857.mm,159.mm,2375.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([1941.142857142857.mm,36.mm,2375.mm], [1.000000,0.000000,0.000000], [-0.000000,-0.000000,-1.000000], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1957.142857142857.mm,36.mm,2375.mm], [0.000000,-1.000000,0.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(-1640.162857142857.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1941.142857142857.mm,20.mm,2375.mm], vec, 8.mm, 16)
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
  circle = ge.add_circle([300.98.mm,20.mm,2375.mm], [-1.000000,0.000000,0.000000], 8.mm, 16)
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
  circle = ge.add_circle([300.mm,19.02.mm,2375.mm], vec, 8.mm, 16)
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
  circle = ge.add_circle([300.mm,18.4998.mm,2375.mm], [0.000000,-1.000000,0.000000], 8.mm, 16)
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
  circle = ge.add_circle([300.mm,18.mm,2374.5002.mm], vec, 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 111.5.mm, 0.mm)
  circle = ge.add_circle([2021.4285714285713.mm,47.5.mm,1840.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([2021.4285714285713.mm,159.mm,1856.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2021.4285714285713.mm,159.mm,1840.mm], [0.000000,1.000000,0.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 503.mm)
  circle = ge.add_circle([2021.4285714285713.mm,175.mm,1856.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([2021.4285714285713.mm,159.mm,2359.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2021.4285714285713.mm,175.mm,2359.mm], [0.000000,0.000000,1.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, -123.mm, 0.mm)
  circle = ge.add_circle([2021.4285714285713.mm,159.mm,2375.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([2005.4285714285713.mm,36.mm,2375.mm], [1.000000,0.000000,0.000000], [-0.000000,-0.000000,-1.000000], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2021.4285714285713.mm,36.mm,2375.mm], [0.000000,-1.000000,0.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(-27.588571428571413.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2005.4285714285713.mm,20.mm,2375.mm], vec, 8.mm, 16)
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
  circle = ge.add_circle([1977.84.mm,20.mm,2375.mm], [-1.000000,0.000000,0.000000], 8.mm, 16)
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
  circle = ge.add_circle([1970.mm,27.84.mm,2375.mm], vec, 8.mm, 16)
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
  circle = ge.add_circle([1970.mm,32.001599999999996.mm,2375.mm], [0.000000,1.000000,0.000000], 8.mm, 16)
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
  circle = ge.add_circle([1970.mm,36.mm,2371.0016.mm], vec, 8.mm, 16)
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
  face = grp.entities.add_face([4849.mm,1146.mm,1209.mm], [4899.mm,1146.mm,1209.mm], [4899.mm,1216.mm,1209.mm], [4849.mm,1216.mm,1209.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1061.mm)
  mat = model.materials["Fuse Block base (Blue Sea 5026)"] || model.materials.add("Fuse Block base (Blue Sea 5026)")
  mat.color = Sketchup::Color.new(43, 43, 48)
  mat.alpha = 1.0
  grp.material = mat

  # Circuit C (water pumps)
  grp = ents.add_group
  grp.name = "Circuit C (water pumps)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 111.5.mm, 0.mm)
  circle = ge.add_circle([1978.5714285714287.mm,47.5.mm,1840.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([1978.5714285714287.mm,159.mm,1856.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1978.5714285714287.mm,159.mm,1840.mm], [0.000000,1.000000,0.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 503.mm)
  circle = ge.add_circle([1978.5714285714287.mm,175.mm,1856.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([1978.5714285714287.mm,159.mm,2359.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1978.5714285714287.mm,175.mm,2359.mm], [0.000000,0.000000,1.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, -123.mm, 0.mm)
  circle = ge.add_circle([1978.5714285714287.mm,159.mm,2375.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([1994.5714285714287.mm,36.mm,2375.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.000000,1.000000], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1978.5714285714287.mm,36.mm,2375.mm], [0.000000,-1.000000,0.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(2863.4285714285716.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1994.5714285714287.mm,20.mm,2375.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([4858.mm,36.mm,2375.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4858.mm,20.mm,2375.mm], [1.000000,0.000000,0.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 1129.mm, 0.mm)
  circle = ge.add_circle([4874.mm,36.mm,2375.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([4874.mm,1165.mm,2359.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4874.mm,1165.mm,2375.mm], [0.000000,1.000000,0.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -114.mm)
  circle = ge.add_circle([4874.mm,1181.mm,2359.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Pump switch P-01 (Cct C)
  grp = ents.add_group
  grp.name = "Pump switch P-01 (Cct C)"
  face = grp.entities.add_face([4734.mm,1089.mm,1269.mm], [4774.mm,1089.mm,1269.mm], [4774.mm,1129.mm,1269.mm], [4734.mm,1129.mm,1269.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Battery − cable (2/0 AWG)"] || model.materials.add("Battery − cable (2/0 AWG)")
  mat.color = Sketchup::Color.new(32, 32, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-01
  grp = ents.add_group
  grp.name = "Cct C branch P-01"
  ge = grp.entities
  vec = Geom::Vector3d.new(-108.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4874.mm,1181.mm,1289.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-01 elbow
  grp = ents.add_group
  grp.name = "Cct C branch P-01 elbow"
  ge = grp.entities
  arc = ge.add_arc([4766.mm,1169.mm,1289.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4766.mm,1181.mm,1289.mm], [-1.000000,0.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-01
  grp = ents.add_group
  grp.name = "Cct C branch P-01"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -60.mm, 0.mm)
  circle = ge.add_circle([4754.mm,1169.mm,1289.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Pump switch P-04 (Cct C)
  grp = ents.add_group
  grp.name = "Pump switch P-04 (Cct C)"
  face = grp.entities.add_face([4734.mm,1089.mm,1527.mm], [4774.mm,1089.mm,1527.mm], [4774.mm,1129.mm,1527.mm], [4734.mm,1129.mm,1527.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Battery − cable (2/0 AWG)"] || model.materials.add("Battery − cable (2/0 AWG)")
  mat.color = Sketchup::Color.new(32, 32, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-04
  grp = ents.add_group
  grp.name = "Cct C branch P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(-108.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4874.mm,1181.mm,1547.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-04 elbow
  grp = ents.add_group
  grp.name = "Cct C branch P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4766.mm,1169.mm,1547.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4766.mm,1181.mm,1547.mm], [-1.000000,0.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-04
  grp = ents.add_group
  grp.name = "Cct C branch P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -60.mm, 0.mm)
  circle = ge.add_circle([4754.mm,1169.mm,1547.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Pump switch P-02 (Cct C)
  grp = ents.add_group
  grp.name = "Pump switch P-02 (Cct C)"
  face = grp.entities.add_face([4734.mm,1233.mm,1269.mm], [4774.mm,1233.mm,1269.mm], [4774.mm,1273.mm,1269.mm], [4734.mm,1273.mm,1269.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Battery − cable (2/0 AWG)"] || model.materials.add("Battery − cable (2/0 AWG)")
  mat.color = Sketchup::Color.new(32, 32, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-02
  grp = ents.add_group
  grp.name = "Cct C branch P-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(-108.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4874.mm,1181.mm,1289.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-02 elbow
  grp = ents.add_group
  grp.name = "Cct C branch P-02 elbow"
  ge = grp.entities
  arc = ge.add_arc([4766.mm,1193.mm,1289.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,-1.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4766.mm,1181.mm,1289.mm], [-1.000000,0.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-02
  grp = ents.add_group
  grp.name = "Cct C branch P-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 60.mm, 0.mm)
  circle = ge.add_circle([4754.mm,1193.mm,1289.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Pump switch P-03 (Cct C)
  grp = ents.add_group
  grp.name = "Pump switch P-03 (Cct C)"
  face = grp.entities.add_face([4734.mm,1233.mm,1527.mm], [4774.mm,1233.mm,1527.mm], [4774.mm,1273.mm,1527.mm], [4734.mm,1273.mm,1527.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Battery − cable (2/0 AWG)"] || model.materials.add("Battery − cable (2/0 AWG)")
  mat.color = Sketchup::Color.new(32, 32, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-03
  grp = ents.add_group
  grp.name = "Cct C branch P-03"
  ge = grp.entities
  vec = Geom::Vector3d.new(-108.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4874.mm,1181.mm,1547.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-03 elbow
  grp = ents.add_group
  grp.name = "Cct C branch P-03 elbow"
  ge = grp.entities
  arc = ge.add_arc([4766.mm,1193.mm,1547.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,-1.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4766.mm,1181.mm,1547.mm], [-1.000000,0.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-03
  grp = ents.add_group
  grp.name = "Cct C branch P-03"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 60.mm, 0.mm)
  circle = ge.add_circle([4754.mm,1193.mm,1547.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Pump switch P-05 (Cct C)
  grp = ents.add_group
  grp.name = "Pump switch P-05 (Cct C)"
  face = grp.entities.add_face([4734.mm,1233.mm,1895.mm], [4774.mm,1233.mm,1895.mm], [4774.mm,1273.mm,1895.mm], [4734.mm,1273.mm,1895.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Battery − cable (2/0 AWG)"] || model.materials.add("Battery − cable (2/0 AWG)")
  mat.color = Sketchup::Color.new(32, 32, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-05
  grp = ents.add_group
  grp.name = "Cct C branch P-05"
  ge = grp.entities
  vec = Geom::Vector3d.new(-108.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4874.mm,1181.mm,1915.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-05 elbow
  grp = ents.add_group
  grp.name = "Cct C branch P-05 elbow"
  ge = grp.entities
  arc = ge.add_arc([4766.mm,1193.mm,1915.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,-1.000000], 12.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4766.mm,1181.mm,1915.mm], [-1.000000,0.000000,0.000000], 6.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(41, 128, 185)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-05
  grp = ents.add_group
  grp.name = "Cct C branch P-05"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 60.mm, 0.mm)
  circle = ge.add_circle([4754.mm,1193.mm,1915.mm], vec, 6.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 111.5.mm, 0.mm)
  circle = ge.add_circle([2064.285714285714.mm,47.5.mm,1840.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([2064.285714285714.mm,159.mm,1856.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2064.285714285714.mm,159.mm,1840.mm], [0.000000,1.000000,0.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 503.mm)
  circle = ge.add_circle([2064.285714285714.mm,175.mm,1856.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([2064.285714285714.mm,159.mm,2359.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2064.285714285714.mm,175.mm,2359.mm], [0.000000,0.000000,1.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, -139.mm, 0.mm)
  circle = ge.add_circle([2064.285714285714.mm,159.mm,2375.mm], vec, 8.mm, 16)
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
  circle = ge.add_circle([1300.mm,20.mm,2375.mm], vec, 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 997.77.mm, 0.mm)
  circle = ge.add_circle([1300.mm,20.mm,2375.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([1300.mm,1017.77.mm,2361.77.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 13.230000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1300.mm,1017.77.mm,2375.mm], [0.000000,1.000000,0.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -13.769999999999982.mm)
  circle = ge.add_circle([1300.mm,1031.mm,2361.77.mm], vec, 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 997.77.mm, 0.mm)
  circle = ge.add_circle([3200.mm,20.mm,2375.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([3200.mm,1017.77.mm,2361.77.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 13.230000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([3200.mm,1017.77.mm,2375.mm], [0.000000,1.000000,0.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -13.769999999999982.mm)
  circle = ge.add_circle([3200.mm,1031.mm,2361.77.mm], vec, 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 847.77.mm, 0.mm)
  circle = ge.add_circle([4574.mm,20.mm,2375.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([4574.mm,867.77.mm,2361.77.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 13.230000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4574.mm,867.77.mm,2375.mm], [0.000000,1.000000,0.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -13.769999999999982.mm)
  circle = ge.add_circle([4574.mm,881.mm,2361.77.mm], vec, 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 111.5.mm, 0.mm)
  circle = ge.add_circle([2000.mm,47.5.mm,1840.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([2000.mm,159.mm,1856.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2000.mm,159.mm,1840.mm], [0.000000,1.000000,0.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 503.mm)
  circle = ge.add_circle([2000.mm,175.mm,1856.mm], vec, 8.mm, 16)
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
  arc = ge.add_arc([2000.mm,159.mm,2359.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 16.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2000.mm,175.mm,2359.mm], [0.000000,0.000000,1.000000], 8.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, -139.mm, 0.mm)
  circle = ge.add_circle([2000.mm,159.mm,2375.mm], vec, 8.mm, 16)
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
  circle = ge.add_circle([520.mm,20.mm,2375.mm], vec, 8.mm, 16)
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
  circle = ge.add_circle([520.mm,20.mm,2375.mm], vec, 8.mm, 16)
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
  circle = ge.add_circle([520.mm,94.12.mm,2375.mm], [0.000000,1.000000,0.000000], 8.mm, 16)
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
  circle = ge.add_circle([520.mm,100.mm,2369.12.mm], vec, 8.mm, 16)
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
  circle = ge.add_circle([2270.mm,20.mm,2375.mm], vec, 8.mm, 16)
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
  circle = ge.add_circle([2270.mm,94.12.mm,2375.mm], [0.000000,1.000000,0.000000], 8.mm, 16)
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
  circle = ge.add_circle([2270.mm,100.mm,2369.12.mm], vec, 8.mm, 16)
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
  circle = ge.add_circle([4170.mm,20.mm,2375.mm], vec, 8.mm, 16)
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
  circle = ge.add_circle([4170.mm,94.12.mm,2375.mm], [0.000000,1.000000,0.000000], 8.mm, 16)
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
  circle = ge.add_circle([4170.mm,100.mm,2369.12.mm], vec, 8.mm, 16)
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
anc = Geom::Point3d.new(1000.mm, -312.5.mm, 711.mm)
txt = entities.add_text("EVAP COOLER
(Hessaire MC18M, Cct E)", anc, Geom::Vector3d.new(-260.mm, -520.mm, 520.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4874.mm, 1181.mm, 2230.mm)
txt = entities.add_text("CCT-C PUMP DISTRIBUTION
5 switches — P-01..P-05 (one at a time)", anc, Geom::Vector3d.new(-350.mm, -700.mm, 250.mm))
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
[["Combined", ["Context", "Solar Array", "Power Core", "Battery", "External Panel", "Inverter", "Circuit Runs"]], ["Power Core", ["Power Core", "Battery", "Inverter"]], ["Distribution", ["Circuit Runs", "Power Core", "Battery"]], ["External Panel", ["External Panel", "Solar Array"]], ["Labeled", ["Context", "Solar Array", "Power Core", "Battery", "External Panel", "Inverter", "Circuit Runs", "Labels"]]].each { |name, tags|
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
