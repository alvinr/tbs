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

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 85.mm, 0.mm)
  circle = ge.add_circle([1300.mm,-920.mm,60.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(19.683469607918596.mm, 11.333333333333371.mm, -19.913840016283835.mm)
  circle = ge.add_circle([1300.mm,-835.mm,60.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-20.009257050357746.mm, 11.333333333333258.mm, -8.084264607821503.mm)
  circle = ge.add_circle([1319.6834696079186.mm,-823.6666666666666.mm,40.086159983716165.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-19.81572696704302.mm, 11.333333333333371.mm, 8.547670251253408.mm)
  circle = ge.add_circle([1299.6742125575608.mm,-812.3333333333334.mm,32.00189537589466.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-7.850904343542652.mm, 11.333333333333371.mm, 20.101965151325494.mm)
  circle = ge.add_circle([1279.8584855905178.mm,-801.mm,40.54956562714807.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.77765289270019.mm, 11.333333333333258.mm, 19.714931185571793.mm)
  circle = ge.add_circle([1272.0075812469752.mm,-789.6666666666666.mm,60.651530778473564.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(20.191951767994624.mm, 11.333333333333371.mm, 7.616481192489317.mm)
  circle = ge.add_circle([1280.7852341396754.mm,-778.3333333333334.mm,80.36646196404536.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(19.611466318005114.mm, 11.333333333333258.mm, -9.00644718045416.mm)
  circle = ge.add_circle([1300.97718590767.mm,-767.mm,87.98294315653467.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(7.381026891803685.mm, 11.333333333333371.mm, -20.279204717617397.mm)
  circle = ge.add_circle([1320.588652225675.mm,-755.6666666666667.mm,78.97649597608051.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.234022139430635.mm, 11.333333333333371.mm, -19.505346371830136.mm)
  circle = ge.add_circle([1327.9696791174788.mm,-744.3333333333334.mm,58.69729125846312.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-20.363712187541523.mm, 11.333333333333258.mm, -7.144573318228495.mm)
  circle = ge.add_circle([1318.7356569780482.mm,-733.mm,39.19194488663298.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-19.396585713988543.mm, 11.333333333333371.mm, 9.46034695962328.mm)
  circle = ge.add_circle([1298.3719447905066.mm,-721.6666666666667.mm,32.047371568404486.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-6.9071524837931975.mm, 11.333333333333371.mm, 20.445462736807713.mm)
  circle = ge.add_circle([1278.975359076518.mm,-710.3333333333334.mm,41.507718528027766.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.685391000274421.mm, 11.333333333333258.mm, 19.285199068932826.mm)
  circle = ge.add_circle([1272.068206592725.mm,-699.mm,61.95318126483548.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(20.524445297700595.mm, 11.333333333333371.mm, 6.6687965314778666.mm)
  circle = ge.add_circle([1281.7535975929993.mm,-687.6666666666667.mm,81.2383803337683.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(19.171201516631527.mm, 11.333333333333371.mm, -9.909123794023046.mm)
  circle = ge.add_circle([1302.2780428907.mm,-676.3333333333334.mm,87.90717686524617.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(6.429537730863103.mm, 11.333333333333258.mm, -20.600649177246062.mm)
  circle = ge.add_circle([1321.4492444073314.mm,-665.mm,77.99805307122313.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.131515051030647.mm, 11.333333333333371.mm, -19.054608490528018.mm)
  circle = ge.add_circle([1327.8787821381945.mm,-653.6666666666667.mm,57.397403893977064.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-20.674064058658132.mm, 11.333333333333371.mm, -6.1894084737607.mm)
  circle = ge.add_circle([1317.747267087164.mm,-642.3333333333334.mm,38.342795403449045.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-18.935435775452106.mm, 11.333333333333258.mm, 10.352534663080739.mm)
  circle = ge.add_circle([1297.0732030285058.mm,-631.mm,32.153386929688345.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.948441269827981.mm, 11.333333333333371.mm, 20.74468000273731.mm)
  circle = ge.add_circle([1278.1377672530537.mm,-619.6666666666667.mm,42.505921592769084.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(10.572152707655732.mm, 11.333333333333371.mm, 18.81369950548175.mm)
  circle = ge.add_circle([1272.1893259832257.mm,-608.3333333333334.mm,63.250601595506396.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(20.81248744921527.mm, 11.333333333333258.mm, 5.706668742167182.mm)
  circle = ge.add_circle([1282.7614786908814.mm,-597.mm,82.06430110098815.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(18.689416161759027.mm, 11.333333333333371.mm, -10.790339451988544.mm)
  circle = ge.add_circle([1303.5739661400967.mm,-585.6666666666667.mm,87.77096984315533.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.464123622908346.mm, 11.333333333333371.mm, -20.877477218048554.mm)
  circle = ge.add_circle([1322.2633823018557.mm,-574.3333333333334.mm,76.98063039116678.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.007065357086049.mm, 11.333333333333258.mm, -18.562602570259443.mm)
  circle = ge.add_circle([1327.727505924764.mm,-563.mm,56.10315317311823.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-20.939640510663367.mm, 11.333333333333371.mm, -5.220838748777922.mm)
  circle = ge.add_circle([1316.720440567678.mm,-551.6666666666667.mm,37.54055060285879.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-18.43327589951309.mm, 11.333333333333371.mm, 11.222301081729867.mm)
  circle = ge.add_circle([1295.7808000570146.mm,-540.3333333333334.mm,32.319711854080865.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.976847056653696.mm, 11.333333333333258.mm, 20.998968911145084.mm)
  circle = ge.add_circle([1277.3475241575015.mm,-529.mm,43.54201293581073.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.436017486448463.mm, 11.333333333333371.mm, 18.301453658280977.mm)
  circle = ge.add_circle([1272.3706771008478.mm,-517.6666666666667.mm,64.54098184695582.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(21.055454387377722.mm, 11.333333333333314.mm, 4.732181579105045.mm)
  circle = ge.add_circle([1283.8066945872963.mm,-506.33333333333337.mm,82.84243550523679.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(18.167153693184446.mm, 11.333333333333371.mm, -11.648185637461964.mm)
  circle = ge.add_circle([1304.862148974674.mm,-495.00000000000006.mm,87.57461708434184.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.48687543992105.mm, 11.333333333333314.mm, -21.1090892921318.mm)
  circle = ge.add_circle([1323.0293026678585.mm,-483.6666666666667.mm,75.92643144687987.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.858776810598556.mm, 11.333333333333371.mm, -18.030394186289215.mm)
  circle = ge.add_circle([1327.5161781077795.mm,-472.33333333333337.mm,54.817342154748076.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.159866364100026.mm, 11.333333333333258.mm, -4.240961849626302.mm)
  circle = ge.add_circle([1315.657401297181.mm,-461.mm,36.78694796845886.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-17.891193652643096.mm, 11.333333333333371.mm, 12.067762495184837.mm)
  circle = ge.add_circle([1294.497534933081.mm,-449.66666666666674.mm,32.54598611883256.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.994474100984462.mm, 11.333333333333314.mm, 21.207778728879774.mm)
  circle = ge.add_circle([1276.6063412804378.mm,-438.33333333333337.mm,44.613748614017396.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(12.27511439790419.mm, 11.333333333333371.mm, 17.749570937770002.mm)
  circle = ge.add_circle([1272.6118671794534.mm,-427.00000000000006.mm,65.82152734289717.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(21.25281989990367.mm, 11.333333333333258.mm, 3.747445564490846.mm)
  circle = ge.add_circle([1284.8869815773576.mm,-415.6666666666667.mm,83.57109828066717.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(17.605545215118582.mm, 11.333333333333371.mm, -12.480804446628227.mm)
  circle = ge.add_circle([1306.1398014772612.mm,-404.3333333333334.mm,87.31854384515802.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.4999096838553214.mm, 11.333333333333314.mm, -21.29498377931801.mm)
  circle = ge.add_circle([1323.7453466923798.mm,-393.00000000000006.mm,74.83773939852979.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-12.684804794216916.mm, 11.333333333333371.mm, -17.45913598346641.mm)
  circle = ge.add_circle([1327.2452563762351.mm,-381.66666666666674.mm,53.54275561921178.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.334264658808706.mm, 11.333333333333258.mm, -3.251899971473321.mm)
  circle = ge.add_circle([1314.5604515820182.mm,-370.33333333333337.mm,36.08361963574537.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-17.310363064279727.mm, 11.333333333333371.mm, 12.88708782228899.mm)
  circle = ge.add_circle([1293.2261869232095.mm,-359.0000000000001.mm,32.83171966427205.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.003450003890066.mm, 11.333333333333314.mm, 21.370657220373296.mm)
  circle = ge.add_circle([1275.9158238589298.mm,-347.66666666666674.mm,45.71880748656104.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(13.08762614496004.mm, 11.333333333333371.mm, 17.159246599029856.mm)
  circle = ge.add_circle([1272.9123738550397.mm,-336.3333333333334.mm,67.08946470693434.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(21.4041565370419.mm, 11.333333333333314.mm, 2.7545934172540996.mm)
  circle = ge.add_circle([1285.9999999999998.mm,-325.00000000000006.mm,84.24871130596419.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(17.00580704646768.mm, 11.333333333333258.mm, -13.286392612551793.mm)
  circle = ge.add_circle([1307.4041565370417.mm,-313.66666666666674.mm,87.00330472321829.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.50536390276352.mm, 11.333333333333371.mm, -21.434758073542348.mm)
  circle = ge.add_circle([1324.4099635835094.mm,-302.3333333333335.mm,73.7169121106665.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-13.483360315265827.mm, 11.333333333333371.mm, -16.850065179852358.mm)
  circle = ge.add_circle([1326.9153274862729.mm,-291.0000000000001.mm,52.28215403712415.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.46245768691756.mm, 11.333333333333371.mm, -2.255795202105489.mm)
  circle = ge.add_circle([1313.431967171007.mm,-279.66666666666674.mm,35.43208885727179.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-16.692042084139302.mm, 11.333333333333258.mm, 13.678502586828678.mm)
  circle = ge.add_circle([1291.9695094840895.mm,-268.33333333333337.mm,33.176293655166305.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.0059211028867594.mm, 11.333333333333371.mm, 21.48725162708238.mm)
  circle = ge.add_circle([1275.2774673999502.mm,-257.0000000000001.mm,46.85479624199498.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(13.871793008099985.mm, 11.333333333333258.mm, 16.531759153126657.mm)
  circle = ge.add_circle([1273.2715462970634.mm,-245.66666666666674.mm,68.34204786907736.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(21.509136537335053.mm, 11.333333333333371.mm, 1.755775434060297.mm)
  circle = ge.add_circle([1287.1433393051634.mm,-234.33333333333348.mm,84.87380702220402.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.36923808655706.mm, 11.333333333333258.mm, -14.063205410651292.mm)
  circle = ge.add_circle([1308.6524758424985.mm,-223.0000000000001.mm,86.62958245626432.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.505392061345674.mm, 11.333333333333371.mm, -21.52810945480808.mm)
  circle = ge.add_circle([1325.0217139290555.mm,-211.66666666666686.mm,72.56637704561302.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-14.252713880306828.mm, 11.333333333333371.mm, -16.204500887181524.mm)
  circle = ge.add_circle([1326.5271059904012.mm,-200.33333333333348.mm,51.03826759080494.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.544167810873205.mm, 11.333333333333371.mm, -1.254804882643775.mm)
  circle = ge.add_circle([1312.2743921100944.mm,-189.0000000000001.mm,34.83376670362342.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-16.037569857779545.mm, 11.333333333333258.mm, 14.440292760653762.mm)
  circle = ge.add_circle([1290.7302242992212.mm,-177.66666666666674.mm,33.57896182097964.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.004047823447081.mm, 11.333333333333371.mm, 21.557309431485166.mm)
  circle = ge.add_circle([1274.6926544414416.mm,-166.33333333333348.mm,48.019254581633405.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(26.311393382005463.mm, 0.mm, -9.57656401311857.mm)
  circle = ge.add_circle([1273.6886066179945.mm,-155.0000000000001.mm,69.57656401311857.mm], vec, 5.mm, 8)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 85.00000000000011.mm, 0.mm)
  circle = ge.add_circle([1300.mm,-155.0000000000001.mm,60.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.mm, 0.mm, 189.mm)
  circle = ge.add_circle([1300.mm,-70.mm,60.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-19.72571067309582.mm, 19.751642042856787.mm, 11.4935832922842.mm)
  circle = ge.add_circle([1302.mm,-70.mm,249.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.033596305039964.mm, -19.8854018007748.mm, 11.369857214315346.mm)
  circle = ge.add_circle([1282.2742893269042.mm,-50.24835795714321.mm,260.4935832922842.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.462007817958693.mm, -19.806594774805603.mm, 11.195300556929169.mm)
  circle = ge.add_circle([1274.2406930218642.mm,-70.13375975791801.mm,271.86344050659955.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(20.04241258691286.mm, -8.058367490645068.mm, 11.072756591120083.mm)
  circle = ge.add_circle([1282.702700839823.mm,-89.94035453272362.mm,283.0587410635287.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(19.884809157327027.mm, 8.437595480161633.mm, 11.07442435227972.mm)
  circle = ge.add_circle([1302.7451134267358.mm,-97.99872202336869.mm,294.1314976546488.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.08205249366506.mm, 19.962393606829295.mm, 11.199321248191438.mm)
  circle = ge.add_circle([1322.6299225840628.mm,-89.56112654320705.mm,305.2059220069285.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.412045843863098.mm, 19.725979722745876.mm, 11.37386197133992.mm)
  circle = ge.add_circle([1330.7119750777279.mm,-69.59873293637776.mm,316.40524325511996.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-19.87968390752485.mm, 7.867641423765534.mm, 11.495212638680357.mm)
  circle = ge.add_circle([1322.2999292338648.mm,-49.87275321363188.mm,327.7791052264599.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-19.564491435031414.mm, -8.626062785333794.mm, 11.491877268600945.mm)
  circle = ge.add_circle([1302.42024532634.mm,-42.00511178986635.mm,339.27431786514023.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-7.65216987913459.mm, -20.03756316484563.mm, 11.36582095584015.mm)
  circle = ge.add_circle([1282.8557538913085.mm,-50.63117457520014.mm,350.7661951337412.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.83891702490655.mm, -19.64356400346358.mm, 11.191312099712832.mm)
  circle = ge.add_circle([1275.203584012174.mm,-70.66873774004577.mm,362.1320160895813.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(20.19274157088512.mm, -7.676197166751507.mm, 11.071165808220826.mm)
  circle = ge.add_circle([1284.0425010370805.mm,-90.31230174350935.mm,373.32332818929416.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(19.719988827528596.mm, 8.81374266860169.mm, 11.076168482753815.mm)
  circle = ge.add_circle([1304.2352426079656.mm,-97.98849891026086.mm,384.394493997515.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(7.699189784295186.mm, 20.11090361304244.mm, 11.20337270543348.mm)
  circle = ge.add_circle([1323.9552314354942.mm,-89.17475624165917.mm,395.4706624802688.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.787380313138556.mm, 19.559355140199052.mm, 11.377833764665581.mm)
  circle = ge.add_circle([1331.6544212197894.mm,-69.06385262861673.mm,406.6740351857023.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-20.02635491840283.mm, 7.484052195409113.mm, 11.496764712869549.mm)
  circle = ge.add_circle([1322.8670409066508.mm,-49.50449748841768.mm,418.05186895036786.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-19.396085058965127.mm, -9.00061799778635.mm, 11.490095190547322.mm)
  circle = ge.add_circle([1302.840685988248.mm,-42.020445293008564.mm,429.5486336632374.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-7.267905835556803.mm, -20.18240825660699.mm, 11.36175466966472.mm)
  circle = ge.add_circle([1283.4446009292828.mm,-51.02106329079491.mm,441.03872885378473.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.212642494460397.mm, -19.47336081987784.mm, 11.187357332839213.mm)
  circle = ge.add_circle([1276.176695093726.mm,-71.2034715474019.mm,452.40048352344945.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(20.335741219946158.mm, -7.2912240495087275.mm, 11.069652584421249.mm)
  circle = ge.add_circle([1285.3893375881864.mm,-90.67683236727974.mm,463.58784085628866.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(19.548011778009595.mm, 9.186671714151856.mm, 11.07798834571173.mm)
  circle = ge.add_circle([1305.7250788081326.mm,-97.96805641678847.mm,474.6574934407099.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(7.313559483685822.mm, 20.252070568306138.mm, 11.207453449355285.mm)
  circle = ge.add_circle([1325.2730905861422.mm,-88.78138470263661.mm,485.73548178642164.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.159462667799062.mm, 19.38558889240948.mm, 11.381771144080005.mm)
  circle = ge.add_circle([1332.586650069828.mm,-68.52931413433048.mm,496.94293523577693.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-20.16567015205942.mm, 7.097730331183364.mm, 11.498238948146195.mm)
  circle = ge.add_circle([1323.427187402029.mm,-49.143725241921.mm,508.32470637985693.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-19.22055303475463.mm, -9.371886833962321.mm, 11.48823770880972.mm)
  circle = ge.add_circle([1303.2615172499695.mm,-42.04599491073763.mm,519.8229453280031.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-6.880944479809841.mm, -20.3198841890824.mm, 11.357659840503402.mm)
  circle = ge.add_circle([1284.040964215215.mm,-51.417881744699955.mm,531.3111830368128.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.583047769045152.mm, -19.296047369970466.mm, 11.183437700303898.mm)
  circle = ge.add_circle([1277.160019735405.mm,-71.73776593378236.mm,542.6688428773163.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(20.471359320940564.mm, -6.9035887033223275.mm, 11.068217472241486.mm)
  circle = ge.add_circle([1286.7430675044502.mm,-91.03381330375282.mm,553.8522805776201.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(19.36894080238062.mm, 9.556246450032418.mm, 11.079883276670671.mm)
  circle = ge.add_circle([1307.2144268253908.mm,-97.93740200707515.mm,564.9204980498616.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(6.925302396198958.mm, 20.385842928633977.mm, 11.21156198996357.mm)
  circle = ge.add_circle([1326.5833676277714.mm,-88.38115555704273.mm,576.0003813265323.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.528157050215896.mm, 19.204744426273237.mm, 11.385672671936277.mm)
  circle = ge.add_circle([1333.5086700239704.mm,-67.99531262840875.mm,587.2119433164959.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-20.297578740623067.mm, 6.708816887958861.mm, 11.499634806226368.mm)
  circle = ge.add_circle([1323.9805129737545.mm,-48.79056820213552.mm,598.5976159884322.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-19.03795945402976.mm, -9.739733733270668.mm, 11.486305501606353.mm)
  circle = ge.add_circle([1303.6829342331314.mm,-42.08175131417666.mm,610.0972507946585.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-6.491427102261014.mm, -20.449940765980372.mm, 11.353537963492158.mm)
  circle = ge.add_circle([1284.6449747791016.mm,-51.821485047447325.mm,621.5835562962649.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.949997603379416.mm, -19.11168839581974.mm, 11.179554633273824.mm)
  circle = ge.add_circle([1278.1535476768406.mm,-72.2714258134277.mm,632.937094259757.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(20.59954635592385.mm, -6.513432664652143.mm, 11.066860995680827.mm)
  circle = ge.add_circle([1288.10354528022.mm,-91.38311420924744.mm,644.1166488930309.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(19.18284128444111.mm, 9.922331934215691.mm, 11.081852583738964.mm)
  circle = ge.add_circle([1308.7030916361439.mm,-97.89654687389958.mm,655.1835098887117.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(6.534560285309226.mm, 20.512171850011555.mm, 11.215696827115949.mm)
  circle = ge.add_circle([1327.885932920585.mm,-87.97421493968389.mm,666.2653624724506.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.89332883980228.mm, 19.01688777314115.mm, 11.389536923677838.mm)
  circle = ge.add_circle([1334.4204932058942.mm,-67.46204308967233.mm,677.4810592995666.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-20.422032520594712.mm, 6.317453868864206.mm, 11.500951777442765.mm)
  circle = ge.add_circle([1324.527164366092.mm,-48.445155316531185.mm,688.8705962232444.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-18.848370986792588.mm, -10.104024384564838.mm, 11.484299274439763.mm)
  circle = ge.add_circle([1304.1051318454972.mm,-42.12770144766698.mm,700.3715480006872.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-6.099495926550844.mm, -20.572530500022978.mm, 11.349390543643608.mm)
  circle = ge.add_circle([1285.2567608587046.mm,-52.23172583223182.mm,711.855847275127.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(10.313358013860125.mm, -18.92035121202119.mm, 11.175709549565.mm)
  circle = ge.add_circle([1279.1572649321538.mm,-72.8042563322548.mm,723.2052378187706.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(20.72025552023956.mm, -6.120898390332584.mm, 11.065583650026724.mm)
  circle = ge.add_circle([1289.470622946014.mm,-91.72460754427598.mm,734.3809473683356.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(18.98978117430761.mm, 10.284794498696598.mm, 11.0838955478672.mm)
  circle = ge.add_circle([1310.1908784662535.mm,-97.84550593460857.mm,745.4465310183623.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(6.141475821842278.mm, 20.631011206232202.mm, 11.219856451067926.mm)
  circle = ge.add_circle([1329.180659640561.mm,-87.56071143591197.mm,756.5304265662295.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.254844702168839.mm, 18.82208752470835.mm, 11.393362488359116.mm)
  circle = ge.add_circle([1335.3221354624034.mm,-66.92970022967977.mm,767.7502830172974.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-20.538986050433778.mm, 5.923784171436154.mm, 11.50218938093326.mm)
  circle = ge.add_circle([1325.0672907602345.mm,-48.107612704971416.mm,779.1436455056565.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-18.651856857070698.mm, -10.464625775183421.mm, 11.482219759839495.mm)
  circle = ge.add_circle([1304.5283047098008.mm,-42.18382853353526.mm,790.6458348865898.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.705294057667061.mm, -20.687608630284515.mm, 11.345219095295533.mm)
  circle = ge.add_circle([1285.87644785273.mm,-52.648454308718684.mm,802.1280546464293.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(10.672996327482679.mm, -18.722105681108943.mm, 11.171903853124604.mm)
  circle = ge.add_circle([1280.171153795063.mm,-73.3360629390032.mm,813.4732737417248.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(20.83344273961052.mm, -5.7261292055582516.mm, 11.064385901673631.mm)
  circle = ge.add_circle([1290.8441501225457.mm,-92.05816862011214.mm,824.6451775948494.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(18.78983096360207.mm, 10.643501798299212.mm, 11.086011423112723.mm)
  circle = ge.add_circle([1311.6775928621562.mm,-97.7842978256704.mm,835.7095634965231.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.746192531882798.mm, 20.74231760573757.mm, 11.224039343025197.mm)
  circle = ge.add_circle([1330.4674238257583.mm,-87.14079602737118.mm,846.7955749196358.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.612572637807261.mm, 18.62041480797032.mm, 11.397147969159505.mm)
  circle = ge.add_circle([1336.213616357641.mm,-66.39847842163361.mm,858.019614262661.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-20.648396627149623.mm, 5.5279515354437905.mm, 11.503347164813817.mm)
  circle = ge.add_circle([1325.6010437198338.mm,-47.77806361366329.mm,869.4167622318205.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-18.448488817645966.mm, -10.82140623951694.mm, 11.480067717094244.mm)
  circle = ge.add_circle([1304.9526470926842.mm,-42.2501120782195.mm,880.9201093966343.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.308965429688897.mm, -20.795133138534787.mm, 11.341025141560408.mm)
  circle = ge.add_circle([1286.5041582750382.mm,-53.07151831773644.mm,892.4001771137285.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.028781230283585.mm, -18.517024188046776.mm, 11.168138933518208.mm)
  circle = ge.add_circle([1281.1951928453493.mm,-73.86665145627123.mm,903.741202255289.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(20.939066686230944.mm, -5.3292692515521765.mm, 11.063268187952758.mm)
  circle = ge.add_circle([1292.223974075633.mm,-92.383675644318.mm,914.9093411888072.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(18.583063659715435.mm, 10.99832285899933.mm, 11.088199436910486.mm)
  circle = ge.add_circle([1313.1630407618638.mm,-97.71294489587018.mm,925.9726093767599.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.34885474436669.mm, 20.84605040746122.mm, 11.228243975697296.mm)
  circle = ge.add_circle([1331.7461044215793.mm,-86.71462203687085.mm,937.0608088136704.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.966382030285786.mm, 18.41194325925217.mm, 11.40089198389478.mm)
  circle = ge.add_circle([1337.094959165946.mm,-65.86857162940963.mm,948.2890527893677.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-20.750224301893468.mm, 5.130100490405823.mm, 11.504424706345503.mm)
  circle = ge.add_circle([1326.1285771356602.mm,-47.45662837015746.mm,959.6899447732625.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-18.23834112385316.mm, -11.174235507082116.mm, 11.47784393197469.mm)
  circle = ge.add_circle([1305.3783528337667.mm,-42.32652787975164.mm,971.194369479608.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.910654753235576.mm, -20.895064764581875.mm, 11.336810213767194.mm)
  circle = ge.add_circle([1287.1400117099136.mm,-53.50076338683375.mm,982.6722134115827.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.380582815287198.mm, -18.305181613798922.mm, 11.16441616542295.mm)
  circle = ge.add_circle([1282.229356956678.mm,-74.39582815141563.mm,994.0090236253499.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(21.037088793856356.mm, -4.930463432935042.mm, 11.062230916972567.mm)
  circle = ge.add_circle([1293.6099397719652.mm,-92.70100976521455.mm,1005.1734397907728.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(18.36955475914806.mm, 11.349128125746958.mm, 11.090458790355797.mm)
  circle = ge.add_circle([1314.6470285658215.mm,-97.63147319814959.mm,1016.2356707077454.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.949607538385862.mm, 20.942171735668325.mm, 11.232468813855576.mm)
  circle = ge.add_circle([1333.0165833249696.mm,-86.28234507240263.mm,1027.3261294981012.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.316143693942877.mm, 18.196748997321805.mm, 11.404593165520737.mm)
  circle = ge.add_circle([1337.9661908633555.mm,-65.34017333673431.mm,1038.5585983119568.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-20.844431894546005.mm, 4.730376302817959.mm, 11.505421612087957.mm)
  circle = ge.add_circle([1326.6500471694126.mm,-47.143424339412505.mm,1049.9631914774775.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-18.02149050646699.mm, -11.52298475008807.mm, 11.475549216447007.mm)
  circle = ge.add_circle([1305.8056152748666.mm,-42.413048036594546.mm,1061.4686130895655.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.510507462627174.mm, -20.98736702060627.mm, 11.332575850903595.mm)
  circle = ge.add_circle([1287.7841247683996.mm,-53.93603278668262.mm,1072.9441623060125.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.72827262993792.mm, -18.08665530798828.mm, 11.160736908124818.mm)
  circle = ge.add_circle([1283.2736173057724.mm,-74.92339980728889.mm,1084.276738156916.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(21.12747327188572.mm, -4.5298573648171185.mm, 11.061274467469957.mm)
  circle = ge.add_circle([1295.0018899357103.mm,-93.01005511527717.mm,1095.4374750650409.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(18.149382219944982.mm, 11.69578950976964.mm, 11.092788658495238.mm)
  circle = ge.add_circle([1316.129363207596.mm,-97.53991248009429.mm,1106.4987495325108.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.548596690213117.mm, 21.030646493786335.mm, 11.236712314894703.mm)
  circle = ge.add_circle([1334.278745427541.mm,-85.84412297032465.mm,1117.591538191006.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.661729921054985.mm, 17.97491059559662.mm, 11.408250162633067.mm)
  circle = ge.add_circle([1338.8273421177541.mm,-64.81347647653831.mm,1128.8282505059008.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-20.930985007291383.mm, 4.3289249231120905.mm, 11.506337518042756.mm)
  circle = ge.add_circle([1327.1656121966992.mm,-46.838565880941694.mm,1140.2365006685338.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-17.79801614368671.mm, -11.86752663047433.mm, 11.473184408375118.mm)
  circle = ge.add_circle([1306.2346271894078.mm,-42.5096409578296.mm,1151.7428381865766.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.108669662782404.mm, -21.072006204483344.mm, 11.32832359905342.mm)
  circle = ge.add_circle([1288.436611045721.mm,-54.377167588303934.mm,1163.2160225949517.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(12.071723723002378.mm, -17.86152506065541.mm, 11.157102505023886.mm)
  circle = ge.add_circle([1284.3279413829387.mm,-75.44917379278728.mm,1174.5443461940051.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(21.210187118429303.mm, -4.127597319629373.mm, 11.060399188670317.mm)
  circle = ge.add_circle([1296.399665105941.mm,-93.31069885344269.mm,1185.701448699029.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(17.92262643323147.mm, 12.038180435342937.mm, 11.09518819062987.mm)
  circle = ge.add_circle([1317.6098522243703.mm,-97.43829617307206.mm,1196.7618478876993.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.145968620076019.mm, 21.11144237721578.mm, 11.240972929393365.mm)
  circle = ge.add_circle([1335.5324786576018.mm,-85.40011573772912.mm,1207.8570360783292.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-12.003014528466565.mm, 17.7465090534551.mm, 11.41186163996008.mm)
  circle = ge.add_circle([1339.6784472776778.mm,-64.28867336051334.mm,1219.0980090077226.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.00985203717846.mm, 3.925892932366864.mm, 11.507172089787673.mm)
  circle = ge.add_circle([1327.6754327492113.mm,-46.54216430705824.mm,1230.5098706476826.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-17.567999632225337.mm, -12.207735346405713.mm, 11.470750371217036.mm)
  circle = ge.add_circle([1306.6655807120328.mm,-42.61627137469138.mm,1242.0170427374703.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.7052880758724314.mm, -21.148951412090824.mm, 11.324055010831898.mm)
  circle = ge.add_circle([1289.0975810798075.mm,-54.82400672109709.mm,1253.4877931086874.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(12.410810690921835.mm, -17.629873073121743.mm, 11.153514283141021.mm)
  circle = ge.add_circle([1285.392293003935.mm,-75.97295813318792.mm,1264.8118481195193.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(21.285200132358113.mm, -3.723830173716877.mm, 11.059605400163036.mm)
  circle = ge.add_circle([1297.8031036948569.mm,-93.60283120630966.mm,1275.9653624026603.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(17.689370193860213.mm, 12.37617588600466.mm, 11.097656510623437.mm)
  circle = ge.add_circle([1319.088303827215.mm,-97.32666138002654.mm,1287.0249678028233.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.741870338695435.mm, 21.1845298851311.mm, 11.245249101683157.mm)
  circle = ge.add_circle([1336.7776740210752.mm,-84.95048549402188.mm,1298.1226243134467.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-12.339872903663718.mm, 17.511627766660382.mm, 11.4154262788511.mm)
  circle = ge.add_circle([1340.5195443597706.mm,-63.76595560889078.mm,1309.36787341513.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.0810041876573.mm, 3.5214274887851786.mm, 11.507925022596964.mm)
  circle = ge.add_circle([1328.179671456107.mm,-46.254327842230396.mm,1320.783299693981.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-17.33152495751733.mm, -12.543486678205923.mm, 11.468247993706655.mm)
  circle = ge.add_circle([1307.0986672684496.mm,-42.73290035344522.mm,1332.291224716578.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-3.300509987747546.mm, -21.21817454859007.mm, 11.319771644820321.mm)
  circle = ge.add_circle([1289.7671423109323.mm,-55.27638703165114.mm,1343.7594727102846.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(12.745409723602052.mm, -17.391783927980114.mm, 11.149973552636538.mm)
  circle = ge.add_circle([1286.4666323231847.mm,-76.49456158024121.mm,1355.079244355105.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(21.352484924331748.mm, -3.3187033537079174.mm, 11.058893391782476.mm)
  circle = ge.add_circle([1299.2120420467868.mm,-93.88634550822132.mm,1366.2292179077415.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(17.449698670179487.mm, 12.70965245020389.mm, 11.100192717222853.mm)
  circle = ge.add_circle([1320.5645269711185.mm,-97.20504886192924.mm,1377.288111299524.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.336449393607154.mm, 21.249882331246795.mm, 11.249539270414289.mm)
  circle = ge.add_circle([1338.014225641298.mm,-84.49539641172535.mm,1388.3883040167468.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-12.67218205027325.mm, 17.2703524969113.mm, 11.418942777757138.mm)
  circle = ge.add_circle([1341.3506750349052.mm,-63.24551408047856.mm,1399.637843287161.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.144415479097916.mm, 3.115676273963871.mm, 11.508596041554028.mm)
  circle = ge.add_circle([1328.678492984632.mm,-45.97516158356726.mm,1411.0567860649182.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-17.088678463050428.mm, -12.874658033714454.mm, 11.465678189532582.mm)
  circle = ge.add_circle([1307.534077505534.mm,-42.859485309603386.mm,1422.5653821064723.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.8944831941594202.mm, -21.27965033868618.mm, 11.315475064993507.mm)
  circle = ge.add_circle([1290.4453990424836.mm,-55.73414334331784.mm,1434.0310602960049.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(13.075398649618137.mm, -17.147344558206598.mm, 11.146481606329644.mm)
  circle = ge.add_circle([1287.5509158483242.mm,-77.01379368200402.mm,1445.3465353609984.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(21.412016926798742.mm, -2.912364782686609.mm, 11.05826342350224.mm)
  circle = ge.add_circle([1300.6263144979423.mm,-94.16113824021062.mm,1456.493016967328.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(17.203699372937308.mm, 13.03848836636027.mm, 11.102795884389707.mm)
  circle = ge.add_circle([1322.038331424741.mm,-97.07350302289723.mm,1467.5512803908302.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.9298538152881974.mm, 21.3074758535652.mm, 11.253841869126745.mm)
  circle = ge.add_circle([1339.2420307976784.mm,-84.03501465653696.mm,1478.65407627522.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-12.999820632971478.mm, 17.022771340527605.mm, 11.422409852706096.mm)
  circle = ge.add_circle([1342.1718846129666.mm,-62.72753880297176.mm,1489.9079181443467.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.200062758270406.mm, 2.7087874389712283.mm, 11.509184901651224.mm)
  circle = ge.add_circle([1329.172063979995.mm,-45.70476746244415.mm,1501.3303279970528.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-16.83954881884347.mm, -13.201128493046113.mm, 11.463041897001176.mm)
  circle = ge.add_circle([1307.9720012217247.mm,-42.995980023472924.mm,1512.839512898704.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.4873559467982886.mm, -21.33335633585719.mm, 11.311166840154101.mm)
  circle = ge.add_circle([1291.1324524028812.mm,-56.19710851651904.mm,1524.3025547957052.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(13.400656980823442.mm, -16.89664421542254.mm, 11.143039719226863.mm)
  circle = ge.add_circle([1288.645096456083.mm,-77.53046485237623.mm,1535.6137216358593.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(21.46377440296783.mm, -2.5049628261809147.mm, 11.057715725341723.mm)
  circle = ge.add_circle([1302.0457534369064.mm,-94.42710906779877.mm,1546.7567613550862.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.951462123327246.mm, 13.362563567323306.mm, 11.10546506163405.mm)
  circle = ge.add_circle([1323.5095278398742.mm,-96.93207189397968.mm,1557.8144770804279.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.522232063106685.mm, 21.357289423087437.mm, 11.25815532682168.mm)
  circle = ge.add_circle([1340.4609899632014.mm,-83.56950832665638.mm,1568.919942142062.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-13.322669021787988.mm, 16.7689746962848.mm, 11.425826237773208.mm)
  circle = ge.add_circle([1342.983222026308.mm,-62.21221890356894.mm,1580.1780974688836.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.24792570680438.mm, 2.300909550251099.mm, 11.509691387879002.mm)
  circle = ge.add_circle([1329.6605530045201.mm,-45.44324420728414.mm,1591.6039237066568.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-16.584226989066565.mm, -13.522778852745496.mm, 11.460340078696618.mm)
  circle = ge.add_circle([1308.4126272977157.mm,-43.14233465703304.mm,1603.1136150945358.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-2.079276899158913.mm, -21.379272930546577.mm, 11.306848543353453.mm)
  circle = ge.add_circle([1291.8284003086492.mm,-56.665113509778536.mm,1614.5739551732324.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(13.721065956343637.mm, -16.63977443730471.mm, 11.139649148057288.mm)
  circle = ge.add_circle([1289.7491234094903.mm,-78.04438644032511.mm,1625.880803716586.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(21.507738454743276.mm, -2.0966462379902424.mm, 11.057250497280847.mm)
  circle = ge.add_circle([1303.470189365834.mm,-94.68416087762982.mm,1637.0204528646432.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.69307902019318.mm, 13.681759724212867.mm, 11.108199274365688.mm)
  circle = ge.add_circle([1324.9779278205772.mm,-96.78080711562006.mm,1648.077703361924.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.113732971115951.mm, 21.399304851492168.mm, 11.262478068535984.mm)
  circle = ge.add_circle([1341.6710068407704.mm,-83.0990473914072.mm,1659.1859026362897.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-13.64060933578503.mm, 16.509055232404165.mm, 11.429190685540107.mm)
  circle = ge.add_circle([1343.7847398118863.mm,-61.69974253991503.mm,1670.4483807048257.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.287986848604078.mm, 1.8921915353796734.mm, 11.510115315305711.mm)
  circle = ge.add_circle([1330.1441304761013.mm,-45.19068730751086.mm,1681.8775713903658.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-16.322806198830676.mm, -13.839491669308622.mm, 11.457573721127801.mm)
  circle = ge.add_circle([1308.8561436274972.mm,-43.29849577213119.mm,1693.3876867056715.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.6703950522658033.mm, -21.41738335732837.mm, 11.302521751322956.mm)
  circle = ge.add_circle([1292.5333374286665.mm,-57.13798744143981.mm,1704.8452604267993.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(14.036508585939828.mm, -16.3768290141619.mm, 11.136311130813056.mm)
  circle = ge.add_circle([1290.8629423764007.mm,-78.55537079876818.mm,1716.1477821781223.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(21.543893029624087.mm, -1.6875641058714876.mm, 11.056867909186622.mm)
  circle = ge.add_circle([1304.8994509623406.mm,-94.93219981293008.mm,1727.2840933089353.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.4286444064021.mm, 13.995960289622772.mm, 11.110997524247068.mm)
  circle = ge.add_circle([1326.4433439919646.mm,-96.61976391880157.mm,1738.340961218122.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.7045056937099616.mm, 21.433506797776403.mm, 11.266808515915955.mm)
  circle = ge.add_circle([1342.8719883983667.mm,-82.6238036291788.mm,1749.451958742369.mm], vec, 5.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-26.5764940920767.mm, -8.809703168597608.mm, 0.28123274171503.mm)
  circle = ge.add_circle([1344.5764940920767.mm,-61.19029683140239.mm,1760.718767258285.mm], vec, 5.mm, 8)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  # PV cord (array -> panel, flexible)
  grp = ents.add_group
  grp.name = "PV cord (array -> panel, flexible)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.mm, 0.mm, 189.mm)
  circle = ge.add_circle([1318.mm,-70.mm,1761.mm], vec, 5.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
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

  # PV feed (MC4 bulkheads -> MPPT)
  grp = ents.add_group
  grp.name = "PV feed (MC4 bulkheads -> MPPT)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 45.mm, 0.mm)
  circle = ge.add_circle([1328.2.mm,22.mm,1884.mm], vec, 9.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
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
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
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
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
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
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
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
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
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
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
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
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
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
  mat = model.materials["PV cord (array -> panel, flexible)"] || model.materials.add("PV cord (array -> panel, flexible)")
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
