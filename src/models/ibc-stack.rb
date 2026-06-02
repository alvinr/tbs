model = Sketchup.active_model
model.start_operation("TBS-001 IBC Stack", true)
entities = model.active_entities

# Display in millimeters (UI readout only).
opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# ── Idempotent rebuild: erase all prior groups/instances (incl. any template
# scale figure) so this focused model frames tightly on the IBC assembly. ──
to_erase = entities.to_a.select { |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance)
}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each { |p| model.pages.erase(p) }

# ── Tags (layers) ──
  model.layers.add("IBC Tanks") unless model.layers["IBC Tanks"]
  model.layers.add("IBC Frame") unless model.layers["IBC Frame"]
  model.layers.add("Plumbing & Panel") unless model.layers["Plumbing & Panel"]

# ── Subsystems (each a component on its tag) ──
  # ═══ IBC Tanks ═══
  defn = model.definitions.add("IBC Tanks")
  ents = defn.entities
  # IBC Brown (developer) pallet
  grp = ents.add_group
  grp.name = "IBC Brown (developer) pallet"
  face = grp.entities.add_face([4674.mm,30.mm,0.mm], [5893.mm,30.mm,0.mm], [5893.mm,1046.mm,0.mm], [4674.mm,1046.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(168.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Brown (developer) bottle
  grp = ents.add_group
  grp.name = "IBC Brown (developer) bottle"
  face = grp.entities.add_face([4704.mm,60.mm,168.mm], [5863.mm,60.mm,168.mm], [5863.mm,1016.mm,168.mm], [4704.mm,1016.mm,168.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(822.mm)
  mat = model.materials["IBC Brown (developer) bottle"] || model.materials.add("IBC Brown (developer) bottle")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 0.4
  grp.material = mat

  # IBC Blue #1 pallet
  grp = ents.add_group
  grp.name = "IBC Blue #1 pallet"
  face = grp.entities.add_face([4674.mm,30.mm,1010.mm], [5893.mm,30.mm,1010.mm], [5893.mm,1046.mm,1010.mm], [4674.mm,1046.mm,1010.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(168.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Blue #1 bottle
  grp = ents.add_group
  grp.name = "IBC Blue #1 bottle"
  face = grp.entities.add_face([4704.mm,60.mm,1178.mm], [5863.mm,60.mm,1178.mm], [5863.mm,1016.mm,1178.mm], [4704.mm,1016.mm,1178.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(822.mm)
  mat = model.materials["IBC Blue #1 bottle"] || model.materials.add("IBC Blue #1 bottle")
  mat.color = Sketchup::Color.new(46, 109, 180)
  mat.alpha = 0.4
  grp.material = mat

  # IBC Waste pallet
  grp = ents.add_group
  grp.name = "IBC Waste pallet"
  face = grp.entities.add_face([4674.mm,1316.mm,0.mm], [5893.mm,1316.mm,0.mm], [5893.mm,2332.mm,0.mm], [4674.mm,2332.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(168.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Waste bottle
  grp = ents.add_group
  grp.name = "IBC Waste bottle"
  face = grp.entities.add_face([4704.mm,1346.mm,168.mm], [5863.mm,1346.mm,168.mm], [5863.mm,2302.mm,168.mm], [4704.mm,2302.mm,168.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(822.mm)
  mat = model.materials["IBC Waste bottle"] || model.materials.add("IBC Waste bottle")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 0.4
  grp.material = mat

  # IBC Blue #2 pallet
  grp = ents.add_group
  grp.name = "IBC Blue #2 pallet"
  face = grp.entities.add_face([4674.mm,1316.mm,1010.mm], [5893.mm,1316.mm,1010.mm], [5893.mm,2332.mm,1010.mm], [4674.mm,2332.mm,1010.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(168.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Blue #2 bottle
  grp = ents.add_group
  grp.name = "IBC Blue #2 bottle"
  face = grp.entities.add_face([4704.mm,1346.mm,1178.mm], [5863.mm,1346.mm,1178.mm], [5863.mm,2302.mm,1178.mm], [4704.mm,2302.mm,1178.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(822.mm)
  mat = model.materials["IBC Blue #1 bottle"] || model.materials.add("IBC Blue #1 bottle")
  mat.color = Sketchup::Color.new(46, 109, 180)
  mat.alpha = 0.4
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "IBC Tanks"
  inst.layer = model.layers["IBC Tanks"]

  # ═══ IBC Frame ═══
  defn = model.definitions.add("IBC Frame")
  ents = defn.entities
  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([4734.mm,1046.mm,0.mm], [4784.mm,1046.mm,0.mm], [4784.mm,1096.mm,0.mm], [4734.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([4734.mm,1266.mm,0.mm], [4784.mm,1266.mm,0.mm], [4784.mm,1316.mm,0.mm], [4734.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([5258.5.mm,1046.mm,0.mm], [5308.5.mm,1046.mm,0.mm], [5308.5.mm,1096.mm,0.mm], [5258.5.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([5258.5.mm,1266.mm,0.mm], [5308.5.mm,1266.mm,0.mm], [5308.5.mm,1316.mm,0.mm], [5258.5.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([5783.mm,1046.mm,0.mm], [5833.mm,1046.mm,0.mm], [5833.mm,1096.mm,0.mm], [5783.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Upright
  grp = ents.add_group
  grp.name = "Rack Upright"
  face = grp.entities.add_face([5783.mm,1266.mm,0.mm], [5833.mm,1266.mm,0.mm], [5833.mm,1316.mm,0.mm], [5783.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1010.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Spine
  grp = ents.add_group
  grp.name = "Rack Spine"
  face = grp.entities.add_face([4734.mm,1046.mm,960.mm], [5833.mm,1046.mm,960.mm], [5833.mm,1096.mm,960.mm], [4734.mm,1096.mm,960.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Spine
  grp = ents.add_group
  grp.name = "Rack Spine"
  face = grp.entities.add_face([4734.mm,1266.mm,960.mm], [5833.mm,1266.mm,960.mm], [5833.mm,1316.mm,960.mm], [4734.mm,1316.mm,960.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Platform Beam
  grp = ents.add_group
  grp.name = "Rack Platform Beam"
  face = grp.entities.add_face([4734.mm,30.mm,960.mm], [4784.mm,30.mm,960.mm], [4784.mm,2332.mm,960.mm], [4734.mm,2332.mm,960.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Platform Beam
  grp = ents.add_group
  grp.name = "Rack Platform Beam"
  face = grp.entities.add_face([5258.5.mm,30.mm,960.mm], [5308.5.mm,30.mm,960.mm], [5308.5.mm,2332.mm,960.mm], [5258.5.mm,2332.mm,960.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rack Platform Beam
  grp = ents.add_group
  grp.name = "Rack Platform Beam"
  face = grp.entities.add_face([5783.mm,30.mm,960.mm], [5833.mm,30.mm,960.mm], [5833.mm,2332.mm,960.mm], [5783.mm,2332.mm,960.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "IBC Frame"
  inst.layer = model.layers["IBC Frame"]

  # ═══ Equipment Panel ═══
  defn = model.definitions.add("Equipment Panel")
  ents = defn.entities
  # Equipment Panel (ply)
  grp = ents.add_group
  grp.name = "Equipment Panel (ply)"
  face = grp.entities.add_face([5000.mm,1046.mm,200.mm], [5018.mm,1046.mm,200.mm], [5018.mm,1316.mm,200.mm], [5000.mm,1316.mm,200.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2060.mm)
  mat = model.materials["Equipment Panel (ply)"] || model.materials.add("Equipment Panel (ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-01 (Blue)
  grp = ents.add_group
  grp.name = "Pump P-01 (Blue)"
  face = grp.entities.add_face([4900.mm,1045.5.mm,1320.mm], [5000.mm,1045.5.mm,1320.mm], [5000.mm,1172.5.mm,1320.mm], [4900.mm,1172.5.mm,1320.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-02 (Brown)
  grp = ents.add_group
  grp.name = "Pump P-02 (Brown)"
  face = grp.entities.add_face([4900.mm,1189.5.mm,1320.mm], [5000.mm,1189.5.mm,1320.mm], [5000.mm,1316.5.mm,1320.mm], [4900.mm,1316.5.mm,1320.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-04 (Tray drain)
  grp = ents.add_group
  grp.name = "Pump P-04 (Tray drain)"
  face = grp.entities.add_face([4900.mm,1045.5.mm,1578.mm], [5000.mm,1045.5.mm,1578.mm], [5000.mm,1172.5.mm,1578.mm], [4900.mm,1172.5.mm,1578.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-03 (Waste evac)
  grp = ents.add_group
  grp.name = "Pump P-03 (Waste evac)"
  face = grp.entities.add_face([4900.mm,1189.5.mm,1578.mm], [5000.mm,1189.5.mm,1578.mm], [5000.mm,1316.5.mm,1578.mm], [4900.mm,1316.5.mm,1578.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-05 (Brown drain)
  grp = ents.add_group
  grp.name = "Pump P-05 (Brown drain)"
  face = grp.entities.add_face([4900.mm,1189.5.mm,1946.mm], [5000.mm,1189.5.mm,1946.mm], [5000.mm,1316.5.mm,1946.mm], [4900.mm,1316.5.mm,1946.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # ACC-01 Accumulator
  grp = ents.add_group
  grp.name = "ACC-01 Accumulator"
  ge = grp.entities
  circle = ge.add_circle([4937.mm,1109.mm,1946.mm], [0,0,1], 63.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(150.mm)
  mat = model.materials["ACC-01 Accumulator"] || model.materials.add("ACC-01 Accumulator")
  mat.color = Sketchup::Color.new(90, 154, 204)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F1 (50µ)
  grp = ents.add_group
  grp.name = "Filter F1 (50µ)"
  ge = grp.entities
  circle = ge.add_circle([4935.mm,1181.mm,200.mm], [0,0,1], 65.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(340.mm)
  mat = model.materials["Filter F1 (50µ)"] || model.materials.add("Filter F1 (50µ)")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F2 (5µ)
  grp = ents.add_group
  grp.name = "Filter F2 (5µ)"
  ge = grp.entities
  circle = ge.add_circle([4935.mm,1181.mm,570.mm], [0,0,1], 65.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(340.mm)
  mat = model.materials["Filter F1 (50µ)"] || model.materials.add("Filter F1 (50µ)")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F3 (GAC)
  grp = ents.add_group
  grp.name = "Filter F3 (GAC)"
  ge = grp.entities
  circle = ge.add_circle([4935.mm,1181.mm,940.mm], [0,0,1], 65.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(340.mm)
  mat = model.materials["Filter F1 (50µ)"] || model.materials.add("Filter F1 (50µ)")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Equipment Panel"
  inst.layer = model.layers["Plumbing & Panel"]

  # ═══ Water Plumbing ═══
  defn = model.definitions.add("Water Plumbing")
  ents = defn.entities
  # Fill Trunk
  grp = ents.add_group
  grp.name = "Fill Trunk"
  ge = grp.entities
  vec = Geom::Vector3d.new(-609.5.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5893.mm,1181.mm,2250.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill Tee
  grp = ents.add_group
  grp.name = "Fill Tee"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 45.59999999999991.mm, 0.mm)
  circle = ge.add_circle([5283.5.mm,1158.2.mm,2250.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill Tee
  grp = ents.add_group
  grp.name = "Fill Tee"
  ge = grp.entities
  vec = Geom::Vector3d.new(22.800000000000182.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5283.5.mm,1181.mm,2250.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill → Blue #1
  grp = ents.add_group
  grp.name = "Fill → Blue #1"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -619.mm, 0.mm)
  circle = ge.add_circle([5283.5.mm,1181.mm,2250.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill → Blue #1 elbow
  grp = ents.add_group
  grp.name = "Fill → Blue #1 elbow"
  ge = grp.entities
  arc = ge.add_arc([5283.5.mm,562.mm,2226.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5283.5.mm,562.mm,2250.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill → Blue #1
  grp = ents.add_group
  grp.name = "Fill → Blue #1"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -186.mm)
  circle = ge.add_circle([5283.5.mm,538.mm,2226.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill → Blue #2
  grp = ents.add_group
  grp.name = "Fill → Blue #2"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 619.mm, 0.mm)
  circle = ge.add_circle([5283.5.mm,1181.mm,2250.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill → Blue #2 elbow
  grp = ents.add_group
  grp.name = "Fill → Blue #2 elbow"
  ge = grp.entities
  arc = ge.add_arc([5283.5.mm,1800.mm,2226.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5283.5.mm,1800.mm,2250.mm], [0.000000,1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill → Blue #2
  grp = ents.add_group
  grp.name = "Fill → Blue #2"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -186.mm)
  circle = ge.add_circle([5283.5.mm,1824.mm,2226.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Drain → Brown IBC
  grp = ents.add_group
  grp.name = "Drain → Brown IBC"
  ge = grp.entities
  vec = Geom::Vector3d.new(-569.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5893.mm,1181.mm,400.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Drain → Brown IBC"] || model.materials.add("Drain → Brown IBC")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Drain → Brown IBC elbow
  grp = ents.add_group
  grp.name = "Drain → Brown IBC elbow"
  ge = grp.entities
  arc = ge.add_arc([5324.mm,1157.mm,400.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5324.mm,1181.mm,400.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Drain → Brown IBC"] || model.materials.add("Drain → Brown IBC")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Drain → Brown IBC
  grp = ents.add_group
  grp.name = "Drain → Brown IBC"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -87.mm, 0.mm)
  circle = ge.add_circle([5300.mm,1157.mm,400.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Drain → Brown IBC"] || model.materials.add("Drain → Brown IBC")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Drain → Brown IBC elbow
  grp = ents.add_group
  grp.name = "Drain → Brown IBC elbow"
  ge = grp.entities
  arc = ge.add_arc([5300.mm,1070.mm,376.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5300.mm,1070.mm,400.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Drain → Brown IBC"] || model.materials.add("Drain → Brown IBC")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Drain → Brown IBC
  grp = ents.add_group
  grp.name = "Drain → Brown IBC"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -76.mm)
  circle = ge.add_circle([5300.mm,1046.mm,376.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Drain → Brown IBC"] || model.materials.add("Drain → Brown IBC")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Drain → Waste IBC
  grp = ents.add_group
  grp.name = "Drain → Waste IBC"
  ge = grp.entities
  vec = Geom::Vector3d.new(-569.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5893.mm,1181.mm,200.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Drain → Waste IBC elbow
  grp = ents.add_group
  grp.name = "Drain → Waste IBC elbow"
  ge = grp.entities
  arc = ge.add_arc([5324.mm,1205.mm,200.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,-1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5324.mm,1181.mm,200.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Drain → Waste IBC
  grp = ents.add_group
  grp.name = "Drain → Waste IBC"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 87.mm, 0.mm)
  circle = ge.add_circle([5300.mm,1205.mm,200.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Drain → Waste IBC elbow
  grp = ents.add_group
  grp.name = "Drain → Waste IBC elbow"
  ge = grp.entities
  arc = ge.add_arc([5300.mm,1292.mm,224.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5300.mm,1292.mm,200.mm], [0.000000,1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Drain → Waste IBC
  grp = ents.add_group
  grp.name = "Drain → Waste IBC"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 76.mm)
  circle = ge.add_circle([5300.mm,1316.mm,224.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Blue Suction Manifold
  grp = ents.add_group
  grp.name = "Blue Suction Manifold"
  ge = grp.entities
  vec = Geom::Vector3d.new(-159.5.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5283.5.mm,1046.mm,1195.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue Suction Manifold elbow
  grp = ents.add_group
  grp.name = "Blue Suction Manifold elbow"
  ge = grp.entities
  arc = ge.add_arc([5124.mm,1070.mm,1195.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,-1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5124.mm,1046.mm,1195.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue Suction Manifold
  grp = ents.add_group
  grp.name = "Blue Suction Manifold"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 222.mm, 0.mm)
  circle = ge.add_circle([5100.mm,1070.mm,1195.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue Suction Manifold elbow
  grp = ents.add_group
  grp.name = "Blue Suction Manifold elbow"
  ge = grp.entities
  arc = ge.add_arc([5124.mm,1292.mm,1195.mm], [-1.000000,0.000000,0.000000], [0.000000,0.000000,-1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5100.mm,1292.mm,1195.mm], [0.000000,1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue Suction Manifold
  grp = ents.add_group
  grp.name = "Blue Suction Manifold"
  ge = grp.entities
  vec = Geom::Vector3d.new(159.5.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5124.mm,1316.mm,1195.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue Manifold Tee
  grp = ents.add_group
  grp.name = "Blue Manifold Tee"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 45.59999999999991.mm, 0.mm)
  circle = ge.add_circle([5100.mm,1158.2.mm,1195.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue Manifold Tee
  grp = ents.add_group
  grp.name = "Blue Manifold Tee"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.800000000000182.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5100.mm,1181.mm,1195.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Manifold → P-01
  grp = ents.add_group
  grp.name = "Manifold → P-01"
  ge = grp.entities
  vec = Geom::Vector3d.new(-136.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5100.mm,1181.mm,1195.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Manifold → P-01 elbow
  grp = ents.add_group
  grp.name = "Manifold → P-01 elbow"
  ge = grp.entities
  arc = ge.add_arc([4964.mm,1157.mm,1195.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4964.mm,1181.mm,1195.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Manifold → P-01
  grp = ents.add_group
  grp.name = "Manifold → P-01"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -24.480000000000018.mm, 0.mm)
  circle = ge.add_circle([4940.mm,1157.mm,1195.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Manifold → P-01 elbow
  grp = ents.add_group
  grp.name = "Manifold → P-01 elbow"
  ge = grp.entities
  arc = ge.add_arc([4940.mm,1132.52.mm,1218.52.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 23.520000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4940.mm,1132.52.mm,1195.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Manifold → P-01
  grp = ents.add_group
  grp.name = "Manifold → P-01"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 101.48000000000002.mm)
  circle = ge.add_circle([4940.mm,1109.mm,1218.52.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Brown → P-02
  grp = ents.add_group
  grp.name = "Brown → P-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(-319.5.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5283.5.mm,1046.mm,185.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Drain → Brown IBC"] || model.materials.add("Drain → Brown IBC")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown → P-02 elbow
  grp = ents.add_group
  grp.name = "Brown → P-02 elbow"
  ge = grp.entities
  arc = ge.add_arc([4964.mm,1070.mm,185.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,-1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4964.mm,1046.mm,185.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Drain → Brown IBC"] || model.materials.add("Drain → Brown IBC")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown → P-02
  grp = ents.add_group
  grp.name = "Brown → P-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 159.mm, 0.mm)
  circle = ge.add_circle([4940.mm,1070.mm,185.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Drain → Brown IBC"] || model.materials.add("Drain → Brown IBC")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown → P-02 elbow
  grp = ents.add_group
  grp.name = "Brown → P-02 elbow"
  ge = grp.entities
  arc = ge.add_arc([4940.mm,1229.mm,209.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4940.mm,1229.mm,185.mm], [0.000000,1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Drain → Brown IBC"] || model.materials.add("Drain → Brown IBC")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown → P-02
  grp = ents.add_group
  grp.name = "Brown → P-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1111.mm)
  circle = ge.add_circle([4940.mm,1253.mm,209.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Drain → Brown IBC"] || model.materials.add("Drain → Brown IBC")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Waste → P-03
  grp = ents.add_group
  grp.name = "Waste → P-03"
  ge = grp.entities
  vec = Geom::Vector3d.new(-279.5.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5283.5.mm,1316.mm,185.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste → P-03 elbow
  grp = ents.add_group
  grp.name = "Waste → P-03 elbow"
  ge = grp.entities
  arc = ge.add_arc([5004.mm,1292.mm,185.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5004.mm,1316.mm,185.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste → P-03
  grp = ents.add_group
  grp.name = "Waste → P-03"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -19.8900000000001.mm, 0.mm)
  circle = ge.add_circle([4980.mm,1292.mm,185.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste → P-03 elbow
  grp = ents.add_group
  grp.name = "Waste → P-03 elbow"
  ge = grp.entities
  arc = ge.add_arc([4980.mm,1272.11.mm,204.11.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 19.110000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4980.mm,1272.11.mm,185.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste → P-03
  grp = ents.add_group
  grp.name = "Waste → P-03"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1373.8899999999999.mm)
  circle = ge.add_circle([4980.mm,1253.mm,204.11.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 86.mm)
  circle = ge.add_circle([4550.mm,80.mm,20.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4574.mm,80.mm,106.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4550.mm,80.mm,106.mm], [0.000000,0.000000,1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(23.460000000000036.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4574.mm,80.mm,130.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4597.46.mm,80.mm,107.46.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 22.540000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4597.46.mm,80.mm,130.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -62.025000000000006.mm)
  circle = ge.add_circle([4620.mm,80.mm,107.46000000000001.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4635.435.mm,80.mm,45.435.mm], [-1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 15.435000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4620.mm,80.mm,45.435.mm], [0.000000,0.000000,-1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.19315000000006.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4635.435.mm,80.mm,30.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4643.6281500000005.mm,87.87184999999981.mm,30.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 7.871849999999805.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4643.6281500000005.mm,80.mm,30.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 1069.1281500000002.mm, 0.mm)
  circle = ge.add_circle([4651.5.mm,87.87184999999981.mm,30.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4675.5.mm,1157.mm,30.mm], [-1.000000,0.000000,0.000000], [0.000000,0.000000,-1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4651.5.mm,1157.mm,30.mm], [0.000000,1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(280.5.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4675.5.mm,1181.mm,30.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4956.mm,1157.mm,30.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,-1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4956.mm,1181.mm,30.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -24.480000000000018.mm, 0.mm)
  circle = ge.add_circle([4980.mm,1157.mm,30.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4980.mm,1132.52.mm,53.52.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 23.520000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4980.mm,1132.52.mm,30.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1524.48.mm)
  circle = ge.add_circle([4980.mm,1109.mm,53.519999999999996.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Pump → Filters
  grp = ents.add_group
  grp.name = "Pump → Filters"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -620.mm)
  circle = ge.add_circle([4950.mm,1181.mm,1320.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Filters → Spray Trunk
  grp = ents.add_group
  grp.name = "Filters → Spray Trunk"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -616.mm)
  circle = ge.add_circle([4950.mm,1181.mm,700.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Filters → Spray Trunk elbow
  grp = ents.add_group
  grp.name = "Filters → Spray Trunk elbow"
  ge = grp.entities
  arc = ge.add_arc([4926.mm,1181.mm,84.mm], [1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4950.mm,1181.mm,84.mm], [0.000000,0.000000,-1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Filters → Spray Trunk
  grp = ents.add_group
  grp.name = "Filters → Spray Trunk"
  ge = grp.entities
  vec = Geom::Vector3d.new(-253.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4926.mm,1181.mm,60.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Filters → Spray Trunk elbow
  grp = ents.add_group
  grp.name = "Filters → Spray Trunk elbow"
  ge = grp.entities
  arc = ge.add_arc([4673.mm,1157.mm,60.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4673.mm,1181.mm,60.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Filters → Spray Trunk
  grp = ents.add_group
  grp.name = "Filters → Spray Trunk"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -1130.3.mm, 0.mm)
  circle = ge.add_circle([4649.mm,1157.mm,60.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Filters → Spray Trunk elbow
  grp = ents.add_group
  grp.name = "Filters → Spray Trunk elbow"
  ge = grp.entities
  arc = ge.add_arc([4649.mm,26.7.mm,45.3.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 14.700000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4649.mm,26.7.mm,60.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Filters → Spray Trunk
  grp = ents.add_group
  grp.name = "Filters → Spray Trunk"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -15.299999999999997.mm)
  circle = ge.add_circle([4649.mm,12.mm,45.3.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Water Plumbing"
  inst.layer = model.layers["Plumbing & Panel"]

  # ═══ Water/Waste Hookups ═══
  defn = model.definitions.add("Water/Waste Hookups")
  ents = defn.entities
  # Water Fill Hookup (2in NPT)
  grp = ents.add_group
  grp.name = "Water Fill Hookup (2in NPT)"
  ge = grp.entities
  circle = ge.add_circle([5893.mm,1181.mm,2250.mm], [1,0,0], 30.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(120.mm)
  mat = model.materials["Water Fill Hookup (2in NPT)"] || model.materials.add("Water Fill Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(46, 109, 180)
  mat.alpha = 1.0
  grp.material = mat

  # Waste Drain Hookup (2in NPT)
  grp = ents.add_group
  grp.name = "Waste Drain Hookup (2in NPT)"
  ge = grp.entities
  circle = ge.add_circle([5893.mm,1181.mm,400.mm], [1,0,0], 30.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(120.mm)
  mat = model.materials["Drain → Brown IBC"] || model.materials.add("Drain → Brown IBC")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Waste Drain Hookup (2in NPT)
  grp = ents.add_group
  grp.name = "Waste Drain Hookup (2in NPT)"
  ge = grp.entities
  circle = ge.add_circle([5893.mm,1181.mm,200.mm], [1,0,0], 30.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(120.mm)
  mat = model.materials["Drain → Waste IBC"] || model.materials.add("Drain → Waste IBC")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Water/Waste Hookups"
  inst.layer = model.layers["Plumbing & Panel"]


model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags from earlier versions ──
keep_tags = ["IBC Tanks", "IBC Frame", "Plumbing & Panel"]
default_layer = model.layers[0]
model.layers.to_a.each { |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}

# ── Scenes ── one consistent iso camera, shared by every scene.
model.layers.each { |l| l.visible = true }
bb = model.bounds
ctr = bb.center
dir = Geom::Vector3d.new(0.72, -0.7, 0.5); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.5)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

[["IBC Tanks", ["IBC Tanks"]], ["IBC Frame", ["IBC Frame"]], ["Plumbing & Panel", ["Plumbing & Panel"]], ["Combined", ["IBC Tanks", "IBC Frame", "Plumbing & Panel"]]].each { |name, tags|
  model.layers.each { |l| l.visible = (l == default_layer || tags.include?(l.name)) }
  page = model.pages.add(name)
  page.use_camera = true
}
model.layers.each { |l| l.visible = true }

model.commit_operation
{ success: true, model: "IBC Stack",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
