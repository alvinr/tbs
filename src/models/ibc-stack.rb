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
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text)
}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each { |p| model.pages.erase(p) }

# ── Tags (layers) ──
  model.layers.add("Context") unless model.layers["Context"]
  model.layers.add("IBC Tanks") unless model.layers["IBC Tanks"]
  model.layers.add("IBC Frame") unless model.layers["IBC Frame"]
  model.layers.add("Plumbing & Panel") unless model.layers["Plumbing & Panel"]
  model.layers.add("Walkway Cantilever") unless model.layers["Walkway Cantilever"]
  model.layers.add("Labels") unless model.layers["Labels"]

# ── Subsystems (each a component on its tag) ──
  # ═══ Container (ghost) ═══
  defn = model.definitions.add("Container (ghost)")
  ents = defn.entities
  # Floor (context)
  grp = ents.add_group
  grp.name = "Floor (context)"
  face = grp.entities.add_face([4300.mm,0.mm,-40.mm], [5893.mm,0.mm,-40.mm], [5893.mm,2362.mm,-40.mm], [4300.mm,2362.mm,-40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Floor (context)"] || model.materials.add("Floor (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.25
  grp.material = mat

  # Ceiling (context)
  grp = ents.add_group
  grp.name = "Ceiling (context)"
  face = grp.entities.add_face([4300.mm,0.mm,2388.mm], [5893.mm,0.mm,2388.mm], [5893.mm,2362.mm,2388.mm], [4300.mm,2362.mm,2388.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Ceiling (context)"] || model.materials.add("Ceiling (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.1
  grp.material = mat

  # Side Wall near (context)
  grp = ents.add_group
  grp.name = "Side Wall near (context)"
  face = grp.entities.add_face([4300.mm,-40.mm,0.mm], [5893.mm,-40.mm,0.mm], [5893.mm,0.mm,0.mm], [4300.mm,0.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Side Wall near (context)"] || model.materials.add("Side Wall near (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.16
  grp.material = mat

  # Side Wall far (context)
  grp = ents.add_group
  grp.name = "Side Wall far (context)"
  face = grp.entities.add_face([4300.mm,2362.mm,0.mm], [5893.mm,2362.mm,0.mm], [5893.mm,2402.mm,0.mm], [4300.mm,2402.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Side Wall near (context)"] || model.materials.add("Side Wall near (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.16
  grp.material = mat

  # End Wall sealed (context)
  grp = ents.add_group
  grp.name = "End Wall sealed (context)"
  face = grp.entities.add_face([5893.mm,0.mm,0.mm], [5933.mm,0.mm,0.mm], [5933.mm,2362.mm,0.mm], [5893.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Side Wall near (context)"] || model.materials.add("Side Wall near (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.16
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Container (ghost)"
  inst.layer = model.layers["Context"]

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
  face.pushpull(980.mm)
  mat = model.materials["IBC Brown (developer) bottle"] || model.materials.add("IBC Brown (developer) bottle")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 0.25
  grp.material = mat

  # IBC Blue #1 pallet
  grp = ents.add_group
  grp.name = "IBC Blue #1 pallet"
  face = grp.entities.add_face([4674.mm,30.mm,1168.mm], [5893.mm,30.mm,1168.mm], [5893.mm,1046.mm,1168.mm], [4674.mm,1046.mm,1168.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(168.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Blue #1 bottle
  grp = ents.add_group
  grp.name = "IBC Blue #1 bottle"
  face = grp.entities.add_face([4704.mm,60.mm,1336.mm], [5863.mm,60.mm,1336.mm], [5863.mm,1016.mm,1336.mm], [4704.mm,1016.mm,1336.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(980.mm)
  mat = model.materials["IBC Blue #1 bottle"] || model.materials.add("IBC Blue #1 bottle")
  mat.color = Sketchup::Color.new(46, 109, 180)
  mat.alpha = 0.25
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
  face.pushpull(980.mm)
  mat = model.materials["IBC Waste bottle"] || model.materials.add("IBC Waste bottle")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 0.25
  grp.material = mat

  # IBC Blue #2 pallet
  grp = ents.add_group
  grp.name = "IBC Blue #2 pallet"
  face = grp.entities.add_face([4674.mm,1316.mm,1168.mm], [5893.mm,1316.mm,1168.mm], [5893.mm,2332.mm,1168.mm], [4674.mm,2332.mm,1168.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(168.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(58, 58, 58)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Blue #2 bottle
  grp = ents.add_group
  grp.name = "IBC Blue #2 bottle"
  face = grp.entities.add_face([4704.mm,1346.mm,1336.mm], [5863.mm,1346.mm,1336.mm], [5863.mm,2302.mm,1336.mm], [4704.mm,2302.mm,1336.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(980.mm)
  mat = model.materials["IBC Blue #1 bottle"] || model.materials.add("IBC Blue #1 bottle")
  mat.color = Sketchup::Color.new(46, 109, 180)
  mat.alpha = 0.25
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "IBC Tanks"
  inst.layer = model.layers["IBC Tanks"]

  # ═══ Corridor Frame (deep box) ═══
  defn = model.definitions.add("Corridor Frame (deep box)")
  ents = defn.entities
  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([4654.mm,1046.mm,0.mm], [4704.mm,1046.mm,0.mm], [4704.mm,1096.mm,0.mm], [4654.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([4654.mm,1266.mm,0.mm], [4704.mm,1266.mm,0.mm], [4704.mm,1316.mm,0.mm], [4654.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([5104.mm,1046.mm,0.mm], [5154.mm,1046.mm,0.mm], [5154.mm,1096.mm,0.mm], [5104.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([5104.mm,1266.mm,0.mm], [5154.mm,1266.mm,0.mm], [5154.mm,1316.mm,0.mm], [5104.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([4654.mm,1096.mm,0.mm], [4704.mm,1096.mm,0.mm], [4704.mm,1266.mm,0.mm], [4654.mm,1266.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([5104.mm,1096.mm,0.mm], [5154.mm,1096.mm,0.mm], [5154.mm,1266.mm,0.mm], [5104.mm,1266.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.mm,1046.mm,0.mm], [5104.mm,1046.mm,0.mm], [5104.mm,1096.mm,0.mm], [4704.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.mm,1266.mm,0.mm], [5104.mm,1266.mm,0.mm], [5104.mm,1316.mm,0.mm], [4704.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([4654.mm,1096.mm,2246.mm], [4704.mm,1096.mm,2246.mm], [4704.mm,1266.mm,2246.mm], [4654.mm,1266.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([5104.mm,1096.mm,2246.mm], [5154.mm,1096.mm,2246.mm], [5154.mm,1266.mm,2246.mm], [5104.mm,1266.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.mm,1046.mm,2246.mm], [5104.mm,1046.mm,2246.mm], [5104.mm,1096.mm,2246.mm], [4704.mm,1096.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.mm,1266.mm,2246.mm], [5104.mm,1266.mm,2246.mm], [5104.mm,1316.mm,2246.mm], [4704.mm,1316.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot plate
  grp = ents.add_group
  grp.name = "Foot plate"
  face = grp.entities.add_face([4604.mm,996.mm,0.mm], [4754.mm,996.mm,0.mm], [4754.mm,1146.mm,0.mm], [4604.mm,1146.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4629.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4629.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4729.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4729.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot plate
  grp = ents.add_group
  grp.name = "Foot plate"
  face = grp.entities.add_face([4604.mm,1216.mm,0.mm], [4754.mm,1216.mm,0.mm], [4754.mm,1366.mm,0.mm], [4604.mm,1366.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4629.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4629.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4729.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4729.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot plate
  grp = ents.add_group
  grp.name = "Foot plate"
  face = grp.entities.add_face([5054.mm,996.mm,0.mm], [5204.mm,996.mm,0.mm], [5204.mm,1146.mm,0.mm], [5054.mm,1146.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5079.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5079.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5179.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5179.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot plate
  grp = ents.add_group
  grp.name = "Foot plate"
  face = grp.entities.add_face([5054.mm,1216.mm,0.mm], [5204.mm,1216.mm,0.mm], [5204.mm,1366.mm,0.mm], [5054.mm,1366.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5079.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5079.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5179.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot anchor M12
  grp = ents.add_group
  grp.name = "Foot anchor M12"
  ge = grp.entities
  circle = ge.add_circle([5179.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1096.mm,90.mm], [5152.mm,1096.mm,90.mm], [5152.mm,1136.mm,90.mm], [5122.mm,1136.mm,90.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1096.mm,1118.mm], [5152.mm,1096.mm,1118.mm], [5152.mm,1136.mm,1118.mm], [5122.mm,1136.mm,1118.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1096.mm,2146.mm], [5152.mm,1096.mm,2146.mm], [5152.mm,1136.mm,2146.mm], [5122.mm,1136.mm,2146.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1226.mm,90.mm], [5152.mm,1226.mm,90.mm], [5152.mm,1266.mm,90.mm], [5122.mm,1266.mm,90.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1226.mm,1118.mm], [5152.mm,1226.mm,1118.mm], [5152.mm,1266.mm,1118.mm], [5122.mm,1266.mm,1118.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1226.mm,2146.mm], [5152.mm,1226.mm,2146.mm], [5152.mm,1266.mm,2146.mm], [5122.mm,1266.mm,2146.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Corridor Frame (deep box)"
  inst.layer = model.layers["IBC Frame"]

  # ═══ IBC Tote Restraint ═══
  defn = model.definitions.add("IBC Tote Restraint")
  ents = defn.entities
  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,0.mm,560.mm], [4674.mm,0.mm,560.mm], [4674.mm,1096.mm,560.mm], [4654.mm,1096.mm,560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,0.mm,1760.mm], [4674.mm,0.mm,1760.mm], [4674.mm,1096.mm,1760.mm], [4654.mm,1096.mm,1760.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,1266.mm,560.mm], [4674.mm,1266.mm,560.mm], [4674.mm,2362.mm,560.mm], [4654.mm,2362.mm,560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,1266.mm,1760.mm], [4674.mm,1266.mm,1760.mm], [4674.mm,2362.mm,1760.mm], [4654.mm,2362.mm,1760.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4646.mm,0.mm,530.mm], [4712.mm,0.mm,530.mm], [4712.mm,4.mm,530.mm], [4646.mm,4.mm,530.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,0.mm,556.mm], [4708.mm,0.mm,556.mm], [4708.mm,70.mm,556.mm], [4650.mm,70.mm,556.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.mm,-48.mm,517.5.mm], [4729.mm,-48.mm,517.5.mm], [4729.mm,-40.mm,517.5.mm], [4629.mm,-40.mm,517.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4647.mm,-48.mm,539.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4647.mm,-48.mm,630.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4711.mm,-48.mm,539.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4711.mm,-48.mm,630.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4646.mm,0.mm,1730.mm], [4712.mm,0.mm,1730.mm], [4712.mm,4.mm,1730.mm], [4646.mm,4.mm,1730.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,0.mm,1756.mm], [4708.mm,0.mm,1756.mm], [4708.mm,70.mm,1756.mm], [4650.mm,70.mm,1756.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.mm,-48.mm,1717.5.mm], [4729.mm,-48.mm,1717.5.mm], [4729.mm,-40.mm,1717.5.mm], [4629.mm,-40.mm,1717.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4647.mm,-48.mm,1739.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4647.mm,-48.mm,1830.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4711.mm,-48.mm,1739.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4711.mm,-48.mm,1830.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4646.mm,2358.mm,530.mm], [4712.mm,2358.mm,530.mm], [4712.mm,2362.mm,530.mm], [4646.mm,2362.mm,530.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,2292.mm,556.mm], [4708.mm,2292.mm,556.mm], [4708.mm,2362.mm,556.mm], [4650.mm,2362.mm,556.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.mm,2402.mm,517.5.mm], [4729.mm,2402.mm,517.5.mm], [4729.mm,2410.mm,517.5.mm], [4629.mm,2410.mm,517.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4647.mm,2352.mm,539.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4647.mm,2352.mm,630.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4711.mm,2352.mm,539.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4711.mm,2352.mm,630.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4646.mm,2358.mm,1730.mm], [4712.mm,2358.mm,1730.mm], [4712.mm,2362.mm,1730.mm], [4646.mm,2362.mm,1730.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,2292.mm,1756.mm], [4708.mm,2292.mm,1756.mm], [4708.mm,2362.mm,1756.mm], [4650.mm,2362.mm,1756.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.mm,2402.mm,1717.5.mm], [4729.mm,2402.mm,1717.5.mm], [4729.mm,2410.mm,1717.5.mm], [4629.mm,2410.mm,1717.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4647.mm,2352.mm,1739.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4647.mm,2352.mm,1830.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4711.mm,2352.mm,1739.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4711.mm,2352.mm,1830.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "IBC Tote Restraint"
  inst.layer = model.layers["IBC Frame"]

  # ═══ Corridor Rear Panel ═══
  defn = model.definitions.add("Corridor Rear Panel")
  ents = defn.entities
  # Rear panel (18mm marine ply)
  grp = ents.add_group
  grp.name = "Rear panel (18mm marine ply)"
  face = grp.entities.add_face([5104.mm,1096.mm,50.mm], [5122.mm,1096.mm,50.mm], [5122.mm,1266.mm,50.mm], [5104.mm,1266.mm,50.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2196.mm)
  mat = model.materials["Rear panel (18mm marine ply)"] || model.materials.add("Rear panel (18mm marine ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Pump-mount ply shirt (25mm)
  grp = ents.add_group
  grp.name = "Pump-mount ply shirt (25mm)"
  face = grp.entities.add_face([5051.5.mm,1096.mm,325.mm], [5076.5.mm,1096.mm,325.mm], [5076.5.mm,1266.mm,325.mm], [5051.5.mm,1266.mm,325.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1866.mm)
  mat = model.materials["Rear panel (18mm marine ply)"] || model.materials.add("Rear panel (18mm marine ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Shirt-to-panel spacer block
  grp = ents.add_group
  grp.name = "Shirt-to-panel spacer block"
  face = grp.entities.add_face([5076.5.mm,1096.mm,320.mm], [5104.mm,1096.mm,320.mm], [5104.mm,1136.mm,320.mm], [5076.5.mm,1136.mm,320.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Rear panel (18mm marine ply)"] || model.materials.add("Rear panel (18mm marine ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Shirt-to-panel spacer block
  grp = ents.add_group
  grp.name = "Shirt-to-panel spacer block"
  face = grp.entities.add_face([5076.5.mm,1096.mm,920.mm], [5104.mm,1096.mm,920.mm], [5104.mm,1136.mm,920.mm], [5076.5.mm,1136.mm,920.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Rear panel (18mm marine ply)"] || model.materials.add("Rear panel (18mm marine ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Shirt-to-panel spacer block
  grp = ents.add_group
  grp.name = "Shirt-to-panel spacer block"
  face = grp.entities.add_face([5076.5.mm,1096.mm,1560.mm], [5104.mm,1096.mm,1560.mm], [5104.mm,1136.mm,1560.mm], [5076.5.mm,1136.mm,1560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Rear panel (18mm marine ply)"] || model.materials.add("Rear panel (18mm marine ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Shirt-to-panel spacer block
  grp = ents.add_group
  grp.name = "Shirt-to-panel spacer block"
  face = grp.entities.add_face([5076.5.mm,1226.mm,320.mm], [5104.mm,1226.mm,320.mm], [5104.mm,1266.mm,320.mm], [5076.5.mm,1266.mm,320.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Rear panel (18mm marine ply)"] || model.materials.add("Rear panel (18mm marine ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Shirt-to-panel spacer block
  grp = ents.add_group
  grp.name = "Shirt-to-panel spacer block"
  face = grp.entities.add_face([5076.5.mm,1226.mm,920.mm], [5104.mm,1226.mm,920.mm], [5104.mm,1266.mm,920.mm], [5076.5.mm,1266.mm,920.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Rear panel (18mm marine ply)"] || model.materials.add("Rear panel (18mm marine ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Shirt-to-panel spacer block
  grp = ents.add_group
  grp.name = "Shirt-to-panel spacer block"
  face = grp.entities.add_face([5076.5.mm,1226.mm,1560.mm], [5104.mm,1226.mm,1560.mm], [5104.mm,1266.mm,1560.mm], [5076.5.mm,1266.mm,1560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Rear panel (18mm marine ply)"] || model.materials.add("Rear panel (18mm marine ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Drain-riser backing spine (18mm ply)
  grp = ents.add_group
  grp.name = "Drain-riser backing spine (18mm ply)"
  face = grp.entities.add_face([5104.mm,1206.mm,280.mm], [5560.mm,1206.mm,280.mm], [5560.mm,1224.mm,280.mm], [5104.mm,1224.mm,280.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1966.mm)
  mat = model.materials["Rear panel (18mm marine ply)"] || model.materials.add("Rear panel (18mm marine ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Corridor Rear Panel"
  inst.layer = model.layers["Plumbing & Panel"]

  # ═══ Corridor Equipment ═══
  defn = model.definitions.add("Corridor Equipment")
  ents = defn.entities
  # Pump P-01 (Blue supply) body
  grp = ents.add_group
  grp.name = "Pump P-01 (Blue supply) body"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1181.mm,615.mm], [0,0,1], 50.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(180.mm)
  mat = model.materials["Pump P-01 (Blue supply) body"] || model.materials.add("Pump P-01 (Blue supply) body")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-01 (Blue supply) head
  grp = ents.add_group
  grp.name = "Pump P-01 (Blue supply) head"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1181.mm,795.mm], [0,0,1], 53.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(30.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-01 (Blue supply) in port
  grp = ents.add_group
  grp.name = "Pump P-01 (Blue supply) in port"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1101.mm,777.mm], [0,1,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(30.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-01 (Blue supply) out port
  grp = ents.add_group
  grp.name = "Pump P-01 (Blue supply) out port"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1231.mm,777.mm], [0,1,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(30.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-04 (Tray drain) body
  grp = ents.add_group
  grp.name = "Pump P-04 (Tray drain) body"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1181.mm,940.mm], [0,0,1], 50.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(180.mm)
  mat = model.materials["Pump P-01 (Blue supply) body"] || model.materials.add("Pump P-01 (Blue supply) body")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-04 (Tray drain) head
  grp = ents.add_group
  grp.name = "Pump P-04 (Tray drain) head"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1181.mm,1120.mm], [0,0,1], 53.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(30.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-04 (Tray drain) in port
  grp = ents.add_group
  grp.name = "Pump P-04 (Tray drain) in port"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1101.mm,1102.mm], [0,1,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(30.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-04 (Tray drain) out port
  grp = ents.add_group
  grp.name = "Pump P-04 (Tray drain) out port"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1231.mm,1102.mm], [0,1,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(30.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-05 (Brown drain) body
  grp = ents.add_group
  grp.name = "Pump P-05 (Brown drain) body"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1181.mm,1340.mm], [0,0,1], 50.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(180.mm)
  mat = model.materials["Pump P-01 (Blue supply) body"] || model.materials.add("Pump P-01 (Blue supply) body")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-05 (Brown drain) head
  grp = ents.add_group
  grp.name = "Pump P-05 (Brown drain) head"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1181.mm,1520.mm], [0,0,1], 53.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(30.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-05 (Brown drain) in port
  grp = ents.add_group
  grp.name = "Pump P-05 (Brown drain) in port"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1101.mm,1502.mm], [0,1,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(30.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-05 (Brown drain) out port
  grp = ents.add_group
  grp.name = "Pump P-05 (Brown drain) out port"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1231.mm,1502.mm], [0,1,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(30.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-03 (Waste drain) body
  grp = ents.add_group
  grp.name = "Pump P-03 (Waste drain) body"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1181.mm,1740.mm], [0,0,1], 50.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(180.mm)
  mat = model.materials["Pump P-01 (Blue supply) body"] || model.materials.add("Pump P-01 (Blue supply) body")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-03 (Waste drain) head
  grp = ents.add_group
  grp.name = "Pump P-03 (Waste drain) head"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1181.mm,1920.mm], [0,0,1], 53.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(30.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-03 (Waste drain) in port
  grp = ents.add_group
  grp.name = "Pump P-03 (Waste drain) in port"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1101.mm,1902.mm], [0,1,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(30.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-03 (Waste drain) out port
  grp = ents.add_group
  grp.name = "Pump P-03 (Waste drain) out port"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1231.mm,1902.mm], [0,1,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(30.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # ACC-01 Accumulator
  grp = ents.add_group
  grp.name = "ACC-01 Accumulator"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1181.mm,355.mm], [0,0,1], 63.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(174.mm)
  mat = model.materials["ACC-01 Accumulator"] || model.materials.add("ACC-01 Accumulator")
  mat.color = Sketchup::Color.new(90, 154, 204)
  mat.alpha = 1.0
  grp.material = mat

  # ACC-01 head
  grp = ents.add_group
  grp.name = "ACC-01 head"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1181.mm,529.mm], [0,0,1], 65.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(26.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # ACC-01 in port
  grp = ents.add_group
  grp.name = "ACC-01 in port"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1244.5.mm,383.mm], [0,1,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(30.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # ACC-01 out port
  grp = ents.add_group
  grp.name = "ACC-01 out port"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1087.5.mm,383.mm], [0,1,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(30.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # SV-02 tap tee run
  grp = ents.add_group
  grp.name = "SV-02 tap tee run"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1311.mm,1145.mm], [0,0,1], 15.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(60.mm)
  mat = model.materials["SV-02 tap tee run"] || model.materials.add("SV-02 tap tee run")
  mat.color = Sketchup::Color.new(154, 160, 168)
  mat.alpha = 1.0
  grp.material = mat

  # SV-02 tap tee branch
  grp = ents.add_group
  grp.name = "SV-02 tap tee branch"
  ge = grp.entities
  circle = ge.add_circle([4948.mm,1311.mm,1175.mm], [1,0,0], 15.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(36.mm)
  mat = model.materials["SV-02 tap tee run"] || model.materials.add("SV-02 tap tee run")
  mat.color = Sketchup::Color.new(154, 160, 168)
  mat.alpha = 1.0
  grp.material = mat

  # SV-02 tap tee socket cuff
  grp = ents.add_group
  grp.name = "SV-02 tap tee socket cuff"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1311.mm,1145.mm], [0,0,1], 19.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["SV-02 tap tee run"] || model.materials.add("SV-02 tap tee run")
  mat.color = Sketchup::Color.new(154, 160, 168)
  mat.alpha = 1.0
  grp.material = mat

  # SV-02 tap tee socket cuff
  grp = ents.add_group
  grp.name = "SV-02 tap tee socket cuff"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1311.mm,1193.mm], [0,0,1], 19.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["SV-02 tap tee run"] || model.materials.add("SV-02 tap tee run")
  mat.color = Sketchup::Color.new(154, 160, 168)
  mat.alpha = 1.0
  grp.material = mat

  # SV-02 tap tee socket cuff
  grp = ents.add_group
  grp.name = "SV-02 tap tee socket cuff"
  ge = grp.entities
  circle = ge.add_circle([4948.mm,1311.mm,1175.mm], [1,0,0], 19.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["SV-02 tap tee run"] || model.materials.add("SV-02 tap tee run")
  mat.color = Sketchup::Color.new(154, 160, 168)
  mat.alpha = 1.0
  grp.material = mat

  # SV-02 tap
  grp = ents.add_group
  grp.name = "SV-02 tap"
  ge = grp.entities
  vec = Geom::Vector3d.new(-70.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4984.mm,1311.mm,1175.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["SV-02 tap"] || model.materials.add("SV-02 tap")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # SV-02 sample valve
  grp = ents.add_group
  grp.name = "SV-02 sample valve"
  face = grp.entities.add_face([4864.mm,1286.mm,1150.mm], [4914.mm,1286.mm,1150.mm], [4914.mm,1336.mm,1150.mm], [4864.mm,1336.mm,1150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["SV-02 tap"] || model.materials.add("SV-02 tap")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # SV-02 sample valve spout
  grp = ents.add_group
  grp.name = "SV-02 sample valve spout"
  ge = grp.entities
  circle = ge.add_circle([4889.mm,1311.mm,1060.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(90.mm)
  mat = model.materials["SV-02 tap"] || model.materials.add("SV-02 tap")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # SV-02 sample valve handwheel stem
  grp = ents.add_group
  grp.name = "SV-02 sample valve handwheel stem"
  ge = grp.entities
  circle = ge.add_circle([4889.mm,1311.mm,1210.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["SV-02 sample valve handwheel stem"] || model.materials.add("SV-02 sample valve handwheel stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # SV-02 sample valve handwheel
  grp = ents.add_group
  grp.name = "SV-02 sample valve handwheel"
  ge = grp.entities
  circle = ge.add_circle([4889.mm,1311.mm,1226.mm], [0,0,1], 30.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(10.mm)
  mat = model.materials["SV-02 sample valve handwheel stem"] || model.materials.add("SV-02 sample valve handwheel stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-02 body
  grp = ents.add_group
  grp.name = "3W-DV-02 body"
  face = grp.entities.add_face([5005.5.mm,1158.mm,2122.mm], [5051.5.mm,1158.mm,2122.mm], [5051.5.mm,1204.mm,2122.mm], [5005.5.mm,1204.mm,2122.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.mm)
  mat = model.materials["SV-02 tap"] || model.materials.add("SV-02 tap")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-02 run +
  grp = ents.add_group
  grp.name = "3W-DV-02 run +"
  ge = grp.entities
  circle = ge.add_circle([5028.5.mm,1204.mm,2145.mm], [0,1,0], 13.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(10.mm)
  mat = model.materials["SV-02 tap"] || model.materials.add("SV-02 tap")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-02 run -
  grp = ents.add_group
  grp.name = "3W-DV-02 run -"
  ge = grp.entities
  circle = ge.add_circle([5028.5.mm,1148.mm,2145.mm], [0,1,0], 13.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(10.mm)
  mat = model.materials["SV-02 tap"] || model.materials.add("SV-02 tap")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-02 branch
  grp = ents.add_group
  grp.name = "3W-DV-02 branch"
  ge = grp.entities
  circle = ge.add_circle([5028.5.mm,1181.mm,2112.mm], [0,0,1], 13.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(10.mm)
  mat = model.materials["SV-02 tap"] || model.materials.add("SV-02 tap")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-02 handle stem
  grp = ents.add_group
  grp.name = "3W-DV-02 handle stem"
  ge = grp.entities
  circle = ge.add_circle([4963.5.mm,1181.mm,2145.mm], [1,0,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(42.mm)
  mat = model.materials["SV-02 sample valve handwheel stem"] || model.materials.add("SV-02 sample valve handwheel stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-02 handle lever
  grp = ents.add_group
  grp.name = "3W-DV-02 handle lever"
  face = grp.entities.add_face([4949.5.mm,1149.mm,2138.mm], [4965.5.mm,1149.mm,2138.mm], [4965.5.mm,1213.mm,2138.mm], [4949.5.mm,1213.mm,2138.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["SV-02 sample valve handwheel stem"] || model.materials.add("SV-02 sample valve handwheel stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Corridor Equipment"
  inst.layer = model.layers["Plumbing & Panel"]

  # ═══ Pinhole-Wall Kit ═══
  defn = model.definitions.add("Pinhole-Wall Kit")
  ents = defn.entities
  # Filter F1 sump
  grp = ents.add_group
  grp.name = "Filter F1 sump"
  ge = grp.entities
  circle = ge.add_circle([3300.mm,104.mm,2000.mm], [0,0,1], 92.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(262.mm)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F1 cap
  grp = ents.add_group
  grp.name = "Filter F1 cap"
  ge = grp.entities
  circle = ge.add_circle([3300.mm,104.mm,2262.mm], [0,0,1], 95.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(78.mm)
  mat = model.materials["Filter F1 cap"] || model.materials.add("Filter F1 cap")
  mat.color = Sketchup::Color.new(34, 34, 40)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F1 in port
  grp = ents.add_group
  grp.name = "Filter F1 in port"
  ge = grp.entities
  vec = Geom::Vector3d.new(-36.mm, 0.mm, 0.mm)
  circle = ge.add_circle([3214.mm,104.mm,2301.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 cap"] || model.materials.add("Filter F1 cap")
  mat.color = Sketchup::Color.new(34, 34, 40)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F1 out port
  grp = ents.add_group
  grp.name = "Filter F1 out port"
  ge = grp.entities
  vec = Geom::Vector3d.new(36.mm, 0.mm, 0.mm)
  circle = ge.add_circle([3386.mm,104.mm,2301.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 cap"] || model.materials.add("Filter F1 cap")
  mat.color = Sketchup::Color.new(34, 34, 40)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F1 PR button
  grp = ents.add_group
  grp.name = "Filter F1 PR button"
  ge = grp.entities
  circle = ge.add_circle([3300.mm,104.mm,2340.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(9.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F2 sump
  grp = ents.add_group
  grp.name = "Filter F2 sump"
  ge = grp.entities
  circle = ge.add_circle([3638.mm,104.mm,2000.mm], [0,0,1], 92.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(262.mm)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F2 cap
  grp = ents.add_group
  grp.name = "Filter F2 cap"
  ge = grp.entities
  circle = ge.add_circle([3638.mm,104.mm,2262.mm], [0,0,1], 95.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(78.mm)
  mat = model.materials["Filter F1 cap"] || model.materials.add("Filter F1 cap")
  mat.color = Sketchup::Color.new(34, 34, 40)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F2 in port
  grp = ents.add_group
  grp.name = "Filter F2 in port"
  ge = grp.entities
  vec = Geom::Vector3d.new(-36.mm, 0.mm, 0.mm)
  circle = ge.add_circle([3552.mm,104.mm,2301.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 cap"] || model.materials.add("Filter F1 cap")
  mat.color = Sketchup::Color.new(34, 34, 40)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F2 out port
  grp = ents.add_group
  grp.name = "Filter F2 out port"
  ge = grp.entities
  vec = Geom::Vector3d.new(36.mm, 0.mm, 0.mm)
  circle = ge.add_circle([3724.mm,104.mm,2301.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 cap"] || model.materials.add("Filter F1 cap")
  mat.color = Sketchup::Color.new(34, 34, 40)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F2 PR button
  grp = ents.add_group
  grp.name = "Filter F2 PR button"
  ge = grp.entities
  circle = ge.add_circle([3638.mm,104.mm,2340.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(9.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F3 sump
  grp = ents.add_group
  grp.name = "Filter F3 sump"
  ge = grp.entities
  circle = ge.add_circle([3976.mm,104.mm,2000.mm], [0,0,1], 92.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(262.mm)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F3 cap
  grp = ents.add_group
  grp.name = "Filter F3 cap"
  ge = grp.entities
  circle = ge.add_circle([3976.mm,104.mm,2262.mm], [0,0,1], 95.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(78.mm)
  mat = model.materials["Filter F1 cap"] || model.materials.add("Filter F1 cap")
  mat.color = Sketchup::Color.new(34, 34, 40)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F3 in port
  grp = ents.add_group
  grp.name = "Filter F3 in port"
  ge = grp.entities
  vec = Geom::Vector3d.new(-36.mm, 0.mm, 0.mm)
  circle = ge.add_circle([3890.mm,104.mm,2301.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 cap"] || model.materials.add("Filter F1 cap")
  mat.color = Sketchup::Color.new(34, 34, 40)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F3 out port
  grp = ents.add_group
  grp.name = "Filter F3 out port"
  ge = grp.entities
  vec = Geom::Vector3d.new(36.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4062.mm,104.mm,2301.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 cap"] || model.materials.add("Filter F1 cap")
  mat.color = Sketchup::Color.new(34, 34, 40)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F3 PR button
  grp = ents.add_group
  grp.name = "Filter F3 PR button"
  ge = grp.entities
  circle = ge.add_circle([3976.mm,104.mm,2340.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(9.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-02 (Brown) body
  grp = ents.add_group
  grp.name = "Pump P-02 (Brown) body"
  ge = grp.entities
  circle = ge.add_circle([3058.mm,104.mm,2139.mm], [0,0,1], 50.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(180.mm)
  mat = model.materials["Pump P-01 (Blue supply) body"] || model.materials.add("Pump P-01 (Blue supply) body")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-02 (Brown) head
  grp = ents.add_group
  grp.name = "Pump P-02 (Brown) head"
  ge = grp.entities
  circle = ge.add_circle([3058.mm,104.mm,2319.mm], [0,0,1], 53.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(30.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-02 (Brown) in port
  grp = ents.add_group
  grp.name = "Pump P-02 (Brown) in port"
  ge = grp.entities
  circle = ge.add_circle([2978.mm,104.mm,2301.mm], [1,0,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(30.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-02 (Brown) out port
  grp = ents.add_group
  grp.name = "Pump P-02 (Brown) out port"
  ge = grp.entities
  circle = ge.add_circle([3108.mm,104.mm,2301.mm], [1,0,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(30.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 sample valve
  grp = ents.add_group
  grp.name = "SV-01 sample valve"
  face = grp.entities.add_face([4225.mm,85.mm,975.mm], [4275.mm,85.mm,975.mm], [4275.mm,135.mm,975.mm], [4225.mm,135.mm,975.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["SV-02 tap"] || model.materials.add("SV-02 tap")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 sample valve spout
  grp = ents.add_group
  grp.name = "SV-01 sample valve spout"
  ge = grp.entities
  circle = ge.add_circle([4250.mm,110.mm,885.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(90.mm)
  mat = model.materials["SV-02 tap"] || model.materials.add("SV-02 tap")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 sample valve handwheel stem
  grp = ents.add_group
  grp.name = "SV-01 sample valve handwheel stem"
  ge = grp.entities
  circle = ge.add_circle([4250.mm,110.mm,1045.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["SV-02 sample valve handwheel stem"] || model.materials.add("SV-02 sample valve handwheel stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 sample valve handwheel
  grp = ents.add_group
  grp.name = "SV-01 sample valve handwheel"
  ge = grp.entities
  circle = ge.add_circle([4250.mm,110.mm,1061.mm], [0,0,1], 30.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(10.mm)
  mat = model.materials["SV-02 sample valve handwheel stem"] || model.materials.add("SV-02 sample valve handwheel stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-01 body
  grp = ents.add_group
  grp.name = "3W-DV-01 body"
  face = grp.entities.add_face([4777.mm,1218.mm,212.mm], [4823.mm,1218.mm,212.mm], [4823.mm,1264.mm,212.mm], [4777.mm,1264.mm,212.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.mm)
  mat = model.materials["SV-02 tap"] || model.materials.add("SV-02 tap")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-01 run +
  grp = ents.add_group
  grp.name = "3W-DV-01 run +"
  ge = grp.entities
  circle = ge.add_circle([4823.mm,1241.mm,235.mm], [1,0,0], 13.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["SV-02 tap"] || model.materials.add("SV-02 tap")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-01 run -
  grp = ents.add_group
  grp.name = "3W-DV-01 run -"
  ge = grp.entities
  circle = ge.add_circle([4767.mm,1241.mm,235.mm], [1,0,0], 13.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["SV-02 tap"] || model.materials.add("SV-02 tap")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-01 branch
  grp = ents.add_group
  grp.name = "3W-DV-01 branch"
  ge = grp.entities
  circle = ge.add_circle([4800.mm,1208.mm,235.mm], [0,1,0], 13.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(10.mm)
  mat = model.materials["SV-02 tap"] || model.materials.add("SV-02 tap")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-01 handle stem
  grp = ents.add_group
  grp.name = "3W-DV-01 handle stem"
  ge = grp.entities
  circle = ge.add_circle([4800.mm,1241.mm,258.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(42.mm)
  mat = model.materials["SV-02 sample valve handwheel stem"] || model.materials.add("SV-02 sample valve handwheel stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-01 handle lever
  grp = ents.add_group
  grp.name = "3W-DV-01 handle lever"
  face = grp.entities.add_face([4768.mm,1233.mm,299.mm], [4832.mm,1233.mm,299.mm], [4832.mm,1249.mm,299.mm], [4768.mm,1249.mm,299.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["SV-02 sample valve handwheel stem"] || model.materials.add("SV-02 sample valve handwheel stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(-109.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4850.mm,1101.mm,308.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet elbow
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet elbow"
  ge = grp.entities
  arc = ge.add_arc([4741.mm,1101.mm,287.mm], [0.000000,0.000000,1.000000], [-0.000000,-1.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4741.mm,1101.mm,308.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -217.59.mm)
  circle = ge.add_circle([4720.mm,1101.mm,287.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet elbow
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet elbow"
  ge = grp.entities
  arc = ge.add_arc([4720.mm,1105.41.mm,69.41.mm], [0.000000,-1.000000,0.000000], [1.000000,-0.000000,0.000000], 4.410000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4720.mm,1101.mm,69.41.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 2.3408999999999196.mm, 0.mm)
  circle = ge.add_circle([4720.mm,1105.41.mm,65.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet elbow
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet elbow"
  ge = grp.entities
  arc = ge.add_arc([4717.7509.mm,1107.7509.mm,65.mm], [1.000000,0.000000,0.000000], [0.000000,-0.000000,1.000000], 2.2490999999999604.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4720.mm,1107.7509.mm,65.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(-140.7509.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4717.7509.mm,1110.mm,65.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet elbow
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet elbow"
  ge = grp.entities
  arc = ge.add_arc([4577.mm,1110.mm,86.mm], [0.000000,0.000000,-1.000000], [0.000000,1.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4577.mm,1110.mm,65.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 35.mm)
  circle = ge.add_circle([4556.mm,1110.mm,86.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet elbow
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet elbow"
  ge = grp.entities
  arc = ge.add_arc([4556.mm,1089.mm,121.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4556.mm,1110.mm,121.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -68.mm, 0.mm)
  circle = ge.add_circle([4556.mm,1089.mm,142.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet elbow
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet elbow"
  ge = grp.entities
  arc = ge.add_arc([4556.mm,1021.mm,121.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4556.mm,1021.mm,142.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -11.730000000000004.mm)
  circle = ge.add_circle([4556.mm,1000.mm,121.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet elbow
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet elbow"
  ge = grp.entities
  arc = ge.add_arc([4556.mm,988.73.mm,109.27.mm], [0.000000,1.000000,0.000000], [-1.000000,-0.000000,-0.000000], 11.270000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4556.mm,1000.mm,109.27.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -912.73.mm, 0.mm)
  circle = ge.add_circle([4556.mm,988.73.mm,98.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet elbow
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet elbow"
  ge = grp.entities
  arc = ge.add_arc([4556.mm,76.mm,77.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4556.mm,76.mm,98.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -31.mm)
  circle = ge.add_circle([4556.mm,55.mm,77.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet elbow
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet elbow"
  ge = grp.entities
  arc = ge.add_arc([4535.mm,55.mm,46.mm], [1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4556.mm,55.mm,46.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1554.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4535.mm,55.mm,25.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet elbow
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet elbow"
  ge = grp.entities
  arc = ge.add_arc([2981.mm,55.mm,46.mm], [0.000000,0.000000,-1.000000], [0.000000,1.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2981.mm,55.mm,25.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 2234.mm)
  circle = ge.add_circle([2960.mm,55.mm,46.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet elbow
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet elbow"
  ge = grp.entities
  arc = ge.add_arc([2960.mm,76.mm,2280.mm], [0.000000,-1.000000,0.000000], [-1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2960.mm,55.mm,2280.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 19.180000000000007.mm, 0.mm)
  circle = ge.add_circle([2960.mm,76.mm,2301.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet elbow
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet elbow"
  ge = grp.entities
  arc = ge.add_arc([2968.82.mm,95.18.mm,2301.mm], [-1.000000,0.000000,0.000000], [0.000000,0.000000,-1.000000], 8.820000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2960.mm,95.18.mm,2301.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.179999999999836.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2968.82.mm,104.mm,2301.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # BV-03 (P-02 suction)
  grp = ents.add_group
  grp.name = "BV-03 (P-02 suction)"
  ge = grp.entities
  circle = ge.add_circle([2960.mm,43.mm,978.mm], [0,0,1], 18.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["BV-03 (P-02 suction)"] || model.materials.add("BV-03 (P-02 suction)")
  mat.color = Sketchup::Color.new(122, 128, 136)
  mat.alpha = 1.0
  grp.material = mat

  # BV-03 (P-02 suction) handle stem
  grp = ents.add_group
  grp.name = "BV-03 (P-02 suction) handle stem"
  ge = grp.entities
  circle = ge.add_circle([2960.mm,61.5.mm,1000.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["SV-02 sample valve handwheel stem"] || model.materials.add("SV-02 sample valve handwheel stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # BV-03 (P-02 suction) handle
  grp = ents.add_group
  grp.name = "BV-03 (P-02 suction) handle"
  face = grp.entities.add_face([2953.mm,89.5.mm,976.mm], [2967.mm,89.5.mm,976.mm], [2967.mm,98.5.mm,976.mm], [2953.mm,98.5.mm,976.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["SV-02 sample valve handwheel stem"] || model.materials.add("SV-02 sample valve handwheel stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> F1
  grp = ents.add_group
  grp.name = "P-02 -> F1"
  ge = grp.entities
  vec = Geom::Vector3d.new(40.mm, 0.mm, 0.mm)
  circle = ge.add_circle([3138.mm,104.mm,2301.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # F1 out -> F2 in
  grp = ents.add_group
  grp.name = "F1 out -> F2 in"
  ge = grp.entities
  vec = Geom::Vector3d.new(94.mm, 0.mm, 0.mm)
  circle = ge.add_circle([3422.mm,104.mm,2301.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # F2 out -> F3 in
  grp = ents.add_group
  grp.name = "F2 out -> F3 in"
  ge = grp.entities
  vec = Geom::Vector3d.new(94.mm, 0.mm, 0.mm)
  circle = ge.add_circle([3760.mm,104.mm,2301.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # F3 -> SV-01 (wall-mounted drop)
  grp = ents.add_group
  grp.name = "F3 -> SV-01 (wall-mounted drop)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -48.mm, 0.mm)
  circle = ge.add_circle([4098.mm,104.mm,2301.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # F3 -> SV-01 (wall-mounted drop) elbow
  grp = ents.add_group
  grp.name = "F3 -> SV-01 (wall-mounted drop) elbow"
  ge = grp.entities
  arc = ge.add_arc([4119.mm,56.mm,2301.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.000000,1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4098.mm,56.mm,2301.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # F3 -> SV-01 (wall-mounted drop)
  grp = ents.add_group
  grp.name = "F3 -> SV-01 (wall-mounted drop)"
  ge = grp.entities
  vec = Geom::Vector3d.new(110.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4119.mm,35.mm,2301.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # F3 -> SV-01 (wall-mounted drop) elbow
  grp = ents.add_group
  grp.name = "F3 -> SV-01 (wall-mounted drop) elbow"
  ge = grp.entities
  arc = ge.add_arc([4229.mm,35.mm,2280.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4229.mm,35.mm,2301.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # F3 -> SV-01 (wall-mounted drop)
  grp = ents.add_group
  grp.name = "F3 -> SV-01 (wall-mounted drop)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1259.mm)
  circle = ge.add_circle([4250.mm,35.mm,2280.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # F3 -> SV-01 (wall-mounted drop) elbow
  grp = ents.add_group
  grp.name = "F3 -> SV-01 (wall-mounted drop) elbow"
  ge = grp.entities
  arc = ge.add_arc([4250.mm,56.mm,1021.mm], [0.000000,-1.000000,0.000000], [1.000000,-0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4250.mm,35.mm,1021.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # F3 -> SV-01 (wall-mounted drop)
  grp = ents.add_group
  grp.name = "F3 -> SV-01 (wall-mounted drop)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 54.mm, 0.mm)
  circle = ge.add_circle([4250.mm,56.mm,1000.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -54.mm, 0.mm)
  circle = ge.add_circle([4250.mm,110.mm,1000.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line) elbow
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line) elbow"
  ge = grp.entities
  arc = ge.add_arc([4250.mm,56.mm,979.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4250.mm,56.mm,1000.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -916.75.mm)
  circle = ge.add_circle([4250.mm,35.mm,979.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line) elbow
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line) elbow"
  ge = grp.entities
  arc = ge.add_arc([4250.mm,47.25.mm,62.25.mm], [0.000000,-1.000000,0.000000], [1.000000,-0.000000,0.000000], 12.250000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4250.mm,35.mm,62.25.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 6.502499999999998.mm, 0.mm)
  circle = ge.add_circle([4250.mm,47.25.mm,50.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line) elbow
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line) elbow"
  ge = grp.entities
  arc = ge.add_arc([4256.2475.mm,53.7525.mm,50.mm], [-1.000000,0.000000,0.000000], [0.000000,0.000000,-1.000000], 6.2475000000000005.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4250.mm,53.7525.mm,50.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(200.7524999999996.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4256.2475.mm,60.mm,50.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line) elbow
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line) elbow"
  ge = grp.entities
  arc = ge.add_arc([4457.mm,60.mm,71.mm], [0.000000,0.000000,-1.000000], [0.000000,-1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4457.mm,60.mm,50.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 13.769999999999996.mm)
  circle = ge.add_circle([4478.mm,60.mm,71.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line) elbow
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line) elbow"
  ge = grp.entities
  arc = ge.add_arc([4478.mm,73.23.mm,84.77.mm], [0.000000,-1.000000,0.000000], [-1.000000,0.000000,0.000000], 13.230000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4478.mm,60.mm,84.77.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 905.77.mm, 0.mm)
  circle = ge.add_circle([4478.mm,73.23.mm,98.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line) elbow
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line) elbow"
  ge = grp.entities
  arc = ge.add_arc([4478.mm,979.mm,119.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4478.mm,979.mm,98.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 11.72999999999999.mm)
  circle = ge.add_circle([4478.mm,1000.mm,119.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line) elbow
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line) elbow"
  ge = grp.entities
  arc = ge.add_arc([4478.mm,1011.27.mm,130.73.mm], [0.000000,-1.000000,0.000000], [-1.000000,0.000000,0.000000], 11.270000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4478.mm,1000.mm,130.73.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 87.73000000000002.mm, 0.mm)
  circle = ge.add_circle([4478.mm,1011.27.mm,142.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line) elbow
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line) elbow"
  ge = grp.entities
  arc = ge.add_arc([4478.mm,1099.mm,121.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4478.mm,1099.mm,142.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -35.mm)
  circle = ge.add_circle([4478.mm,1120.mm,121.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line) elbow
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line) elbow"
  ge = grp.entities
  arc = ge.add_arc([4478.mm,1141.mm,86.mm], [0.000000,-1.000000,0.000000], [1.000000,-0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4478.mm,1120.mm,86.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 79.mm, 0.mm)
  circle = ge.add_circle([4478.mm,1141.mm,65.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line) elbow
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line) elbow"
  ge = grp.entities
  arc = ge.add_arc([4499.mm,1220.mm,65.mm], [-1.000000,0.000000,0.000000], [0.000000,0.000000,-1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4478.mm,1220.mm,65.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(180.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4499.mm,1241.mm,65.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line) elbow
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line) elbow"
  ge = grp.entities
  arc = ge.add_arc([4679.mm,1241.mm,86.mm], [0.000000,0.000000,-1.000000], [0.000000,-1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4679.mm,1241.mm,65.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 128.mm)
  circle = ge.add_circle([4700.mm,1241.mm,86.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line) elbow
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line) elbow"
  ge = grp.entities
  arc = ge.add_arc([4721.mm,1241.mm,214.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4700.mm,1241.mm,214.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(46.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4721.mm,1241.mm,235.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 blue recycle -> X1 cross
  grp = ents.add_group
  grp.name = "DV-01 blue recycle -> X1 cross"
  ge = grp.entities
  vec = Geom::Vector3d.new(385.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4833.mm,1241.mm,235.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 blue recycle -> X1 cross elbow
  grp = ents.add_group
  grp.name = "DV-01 blue recycle -> X1 cross elbow"
  ge = grp.entities
  arc = ge.add_arc([5218.mm,1220.mm,235.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,-1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5218.mm,1241.mm,235.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 blue recycle -> X1 cross
  grp = ents.add_group
  grp.name = "DV-01 blue recycle -> X1 cross"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -12.49499999999989.mm, 0.mm)
  circle = ge.add_circle([5239.mm,1220.mm,235.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 blue recycle -> X1 cross elbow
  grp = ents.add_group
  grp.name = "DV-01 blue recycle -> X1 cross elbow"
  ge = grp.entities
  arc = ge.add_arc([5239.mm,1207.505.mm,247.005.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 12.005.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5239.mm,1207.505.mm,235.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 blue recycle -> X1 cross
  grp = ents.add_group
  grp.name = "DV-01 blue recycle -> X1 cross"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1981.995.mm)
  circle = ge.add_circle([5239.mm,1195.5.mm,247.005.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 blue recycle -> X1 cross elbow
  grp = ents.add_group
  grp.name = "DV-01 blue recycle -> X1 cross elbow"
  ge = grp.entities
  arc = ge.add_arc([5260.mm,1195.5.mm,2229.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5239.mm,1195.5.mm,2229.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 blue recycle -> X1 cross
  grp = ents.add_group
  grp.name = "DV-01 blue recycle -> X1 cross"
  ge = grp.entities
  vec = Geom::Vector3d.new(240.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5260.mm,1195.5.mm,2250.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 -> IBC-4 merge
  grp = ents.add_group
  grp.name = "DV-01 -> IBC-4 merge"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -22.mm, 0.mm)
  circle = ge.add_circle([4800.mm,1208.mm,235.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 -> IBC-4 merge elbow
  grp = ents.add_group
  grp.name = "DV-01 -> IBC-4 merge elbow"
  ge = grp.entities
  arc = ge.add_arc([4821.mm,1186.mm,235.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.000000,1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4800.mm,1186.mm,235.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 -> IBC-4 merge
  grp = ents.add_group
  grp.name = "DV-01 -> IBC-4 merge"
  ge = grp.entities
  vec = Geom::Vector3d.new(568.3000000000002.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4821.mm,1165.mm,235.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 -> IBC-4 merge elbow
  grp = ents.add_group
  grp.name = "DV-01 -> IBC-4 merge elbow"
  ge = grp.entities
  arc = ge.add_arc([5389.3.mm,1179.7.mm,235.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 14.700000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5389.3.mm,1165.mm,235.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 -> IBC-4 merge
  grp = ents.add_group
  grp.name = "DV-01 -> IBC-4 merge"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.802999999999884.mm, 0.mm)
  circle = ge.add_circle([5404.mm,1179.7.mm,235.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 -> IBC-4 merge elbow
  grp = ents.add_group
  grp.name = "DV-01 -> IBC-4 merge elbow"
  ge = grp.entities
  arc = ge.add_arc([5404.mm,1187.503.mm,242.49699999999999.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 7.496999999999979.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5404.mm,1187.503.mm,235.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 -> IBC-4 merge
  grp = ents.add_group
  grp.name = "DV-01 -> IBC-4 merge"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 987.503.mm)
  circle = ge.add_circle([5404.mm,1195.mm,242.49699999999999.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Pinhole-Wall Kit"
  inst.layer = model.layers["Plumbing & Panel"]

  # ═══ Pinhole-Wall Equipment ═══
  defn = model.definitions.add("Pinhole-Wall Equipment")
  ents = defn.entities
  # Electrical Panel (EP enclosure, IP65)
  grp = ents.add_group
  grp.name = "Electrical Panel (EP enclosure, IP65)"
  face = grp.entities.add_face([1898.mm,0.mm,1488.mm], [2222.mm,0.mm,1488.mm], [2222.mm,171.mm,1488.mm], [1898.mm,171.mm,1488.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(624.mm)
  mat = model.materials["Electrical Panel (EP enclosure, IP65)"] || model.materials.add("Electrical Panel (EP enclosure, IP65)")
  mat.color = Sketchup::Color.new(245, 197, 24)
  mat.alpha = 0.14
  grp.material = mat

  # MPPT Controller (Victron 100/50)
  grp = ents.add_group
  grp.name = "MPPT Controller (Victron 100/50)"
  face = grp.entities.add_face([1925.mm,25.mm,1970.mm], [2110.mm,25.mm,1970.mm], [2110.mm,95.mm,1970.mm], [1925.mm,95.mm,1970.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["MPPT Controller (Victron 100/50)"] || model.materials.add("MPPT Controller (Victron 100/50)")
  mat.color = Sketchup::Color.new(58, 91, 160)
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

  # Main Disconnect (Blue Sea m-Series)
  grp = ents.add_group
  grp.name = "Main Disconnect (Blue Sea m-Series)"
  ge = grp.entities
  circle = ge.add_circle([2150.mm,165.mm,1620.mm], [0,1,0], 35.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Main Disconnect (Blue Sea m-Series)"] || model.materials.add("Main Disconnect (Blue Sea m-Series)")
  mat.color = Sketchup::Color.new(212, 58, 47)
  mat.alpha = 1.0
  grp.material = mat

  # Main feed (disconnect -> busbar +)
  grp = ents.add_group
  grp.name = "Main feed (disconnect -> busbar +)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -63.mm, 0.mm)
  circle = ge.add_circle([2150.mm,130.mm,1655.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect -> busbar +)"] || model.materials.add("Main feed (disconnect -> busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Main feed (disconnect -> busbar +) elbow
  grp = ents.add_group
  grp.name = "Main feed (disconnect -> busbar +) elbow"
  ge = grp.entities
  arc = ge.add_arc([2150.mm,67.mm,1677.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 22.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2150.mm,67.mm,1655.mm], [0.000000,-1.000000,0.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Main feed (disconnect -> busbar +)"] || model.materials.add("Main feed (disconnect -> busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Main feed (disconnect -> busbar +)
  grp = ents.add_group
  grp.name = "Main feed (disconnect -> busbar +)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 14.279999999999973.mm)
  circle = ge.add_circle([2150.mm,45.mm,1677.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect -> busbar +)"] || model.materials.add("Main feed (disconnect -> busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Main feed (disconnect -> busbar +) elbow
  grp = ents.add_group
  grp.name = "Main feed (disconnect -> busbar +) elbow"
  ge = grp.entities
  arc = ge.add_arc([2136.28.mm,45.mm,1691.28.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 13.72.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2150.mm,45.mm,1691.28.mm], [0.000000,0.000000,1.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Main feed (disconnect -> busbar +)"] || model.materials.add("Main feed (disconnect -> busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Main feed (disconnect -> busbar +)
  grp = ents.add_group
  grp.name = "Main feed (disconnect -> busbar +)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-91.2800000000002.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2136.28.mm,45.mm,1705.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect -> busbar +)"] || model.materials.add("Main feed (disconnect -> busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

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

  # Battery 2 (optional 2nd pack — plug-in, ghosted)
  grp = ents.add_group
  grp.name = "Battery 2 (optional 2nd pack — plug-in, ghosted)"
  face = grp.entities.add_face([1890.mm,0.mm,150.mm], [2220.mm,0.mm,150.mm], [2220.mm,172.mm,150.mm], [1890.mm,172.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(214.mm)
  mat = model.materials["Battery 2 (optional 2nd pack — plug-in, ghosted)"] || model.materials.add("Battery 2 (optional 2nd pack — plug-in, ghosted)")
  mat.color = Sketchup::Color.new(106, 90, 205)
  mat.alpha = 0.28
  grp.material = mat

  # Ext. Power Panel (exterior)
  grp = ents.add_group
  grp.name = "Ext. Power Panel (exterior)"
  face = grp.entities.add_face([1250.mm,-65.mm,1830.mm], [1590.mm,-65.mm,1830.mm], [1590.mm,-40.mm,1830.mm], [1250.mm,-40.mm,1830.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(240.mm)
  mat = model.materials["Ext. Power Panel (exterior)"] || model.materials.add("Ext. Power Panel (exterior)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.5
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

  # Battery Contactor (ML-RBS, in + feed)
  grp = ents.add_group
  grp.name = "Battery Contactor (ML-RBS, in + feed)"
  face = grp.entities.add_face([1560.mm,15.mm,364.mm], [1680.mm,15.mm,364.mm], [1680.mm,105.mm,364.mm], [1560.mm,105.mm,364.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Battery Contactor (ML-RBS, in + feed)"] || model.materials.add("Battery Contactor (ML-RBS, in + feed)")
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

  # Battery + cable (2/0 AWG, MRBF -> main disconnect)
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF -> main disconnect)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1161.mm)
  circle = ge.add_circle([1715.mm,45.mm,402.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect -> busbar +)"] || model.materials.add("Main feed (disconnect -> busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF -> main disconnect) elbow
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF -> main disconnect) elbow"
  ge = grp.entities
  arc = ge.add_arc([1737.mm,45.mm,1563.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 22.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1715.mm,45.mm,1563.mm], [0.000000,0.000000,1.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Main feed (disconnect -> busbar +)"] || model.materials.add("Main feed (disconnect -> busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF -> main disconnect)
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF -> main disconnect)"
  ge = grp.entities
  vec = Geom::Vector3d.new(391.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1737.mm,45.mm,1585.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect -> busbar +)"] || model.materials.add("Main feed (disconnect -> busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF -> main disconnect) elbow
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF -> main disconnect) elbow"
  ge = grp.entities
  arc = ge.add_arc([2128.mm,67.mm,1585.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 22.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2128.mm,45.mm,1585.mm], [1.000000,0.000000,0.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Main feed (disconnect -> busbar +)"] || model.materials.add("Main feed (disconnect -> busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF -> main disconnect)
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF -> main disconnect)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 63.mm, 0.mm)
  circle = ge.add_circle([2150.mm,67.mm,1585.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect -> busbar +)"] || model.materials.add("Main feed (disconnect -> busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery - cable (2/0 AWG -> busbar -)
  grp = ents.add_group
  grp.name = "Battery - cable (2/0 AWG -> busbar -)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1300.mm)
  circle = ge.add_circle([1760.mm,60.mm,364.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Battery - cable (2/0 AWG -> busbar -)"] || model.materials.add("Battery - cable (2/0 AWG -> busbar -)")
  mat.color = Sketchup::Color.new(32, 32, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Battery - cable (2/0 AWG -> busbar -) elbow
  grp = ents.add_group
  grp.name = "Battery - cable (2/0 AWG -> busbar -) elbow"
  ge = grp.entities
  arc = ge.add_arc([1782.mm,60.mm,1664.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 22.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1760.mm,60.mm,1664.mm], [0.000000,0.000000,1.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Battery - cable (2/0 AWG -> busbar -)"] || model.materials.add("Battery - cable (2/0 AWG -> busbar -)")
  mat.color = Sketchup::Color.new(32, 32, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Battery - cable (2/0 AWG -> busbar -)
  grp = ents.add_group
  grp.name = "Battery - cable (2/0 AWG -> busbar -)"
  ge = grp.entities
  vec = Geom::Vector3d.new(163.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1782.mm,60.mm,1686.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Battery - cable (2/0 AWG -> busbar -)"] || model.materials.add("Battery - cable (2/0 AWG -> busbar -)")
  mat.color = Sketchup::Color.new(32, 32, 32)
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
  mat = model.materials["Battery Contactor (ML-RBS, in + feed)"] || model.materials.add("Battery Contactor (ML-RBS, in + feed)")
  mat.color = Sketchup::Color.new(196, 43, 28)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop control wire (2x 18 AWG)
  grp = ents.add_group
  grp.name = "E-stop control wire (2x 18 AWG)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-490.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1620.mm,60.mm,464.mm], vec, 5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["E-stop control wire (2x 18 AWG)"] || model.materials.add("E-stop control wire (2x 18 AWG)")
  mat.color = Sketchup::Color.new(106, 61, 168)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop control wire (2x 18 AWG) elbow
  grp = ents.add_group
  grp.name = "E-stop control wire (2x 18 AWG) elbow"
  ge = grp.entities
  arc = ge.add_arc([1130.mm,60.mm,474.mm], [0.000000,0.000000,-1.000000], [0.000000,1.000000,-0.000000], 10.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1130.mm,60.mm,464.mm], [-1.000000,0.000000,0.000000], 5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["E-stop control wire (2x 18 AWG)"] || model.materials.add("E-stop control wire (2x 18 AWG)")
  mat.color = Sketchup::Color.new(106, 61, 168)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop control wire (2x 18 AWG)
  grp = ents.add_group
  grp.name = "E-stop control wire (2x 18 AWG)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1466.mm)
  circle = ge.add_circle([1120.mm,60.mm,474.mm], vec, 5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["E-stop control wire (2x 18 AWG)"] || model.materials.add("E-stop control wire (2x 18 AWG)")
  mat.color = Sketchup::Color.new(106, 61, 168)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop control wire (2x 18 AWG) elbow
  grp = ents.add_group
  grp.name = "E-stop control wire (2x 18 AWG) elbow"
  ge = grp.entities
  arc = ge.add_arc([1130.mm,60.mm,1940.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 10.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1120.mm,60.mm,1940.mm], [0.000000,0.000000,1.000000], 5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["E-stop control wire (2x 18 AWG)"] || model.materials.add("E-stop control wire (2x 18 AWG)")
  mat.color = Sketchup::Color.new(106, 61, 168)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop control wire (2x 18 AWG)
  grp = ents.add_group
  grp.name = "E-stop control wire (2x 18 AWG)"
  ge = grp.entities
  vec = Geom::Vector3d.new(280.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1130.mm,60.mm,1950.mm], vec, 5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["E-stop control wire (2x 18 AWG)"] || model.materials.add("E-stop control wire (2x 18 AWG)")
  mat.color = Sketchup::Color.new(106, 61, 168)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop control wire (2x 18 AWG) elbow
  grp = ents.add_group
  grp.name = "E-stop control wire (2x 18 AWG) elbow"
  ge = grp.entities
  arc = ge.add_arc([1410.mm,50.mm,1950.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,-1.000000], 10.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1410.mm,60.mm,1950.mm], [1.000000,0.000000,0.000000], 5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["E-stop control wire (2x 18 AWG)"] || model.materials.add("E-stop control wire (2x 18 AWG)")
  mat.color = Sketchup::Color.new(106, 61, 168)
  mat.alpha = 1.0
  grp.material = mat

  # E-stop control wire (2x 18 AWG)
  grp = ents.add_group
  grp.name = "E-stop control wire (2x 18 AWG)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -40.mm, 0.mm)
  circle = ge.add_circle([1420.mm,50.mm,1950.mm], vec, 5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["E-stop control wire (2x 18 AWG)"] || model.materials.add("E-stop control wire (2x 18 AWG)")
  mat.color = Sketchup::Color.new(106, 61, 168)
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
  mat = model.materials["E-stop collar (safety yellow)"] || model.materials.add("E-stop collar (safety yellow)")
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
  mat = model.materials["Battery Contactor (ML-RBS, in + feed)"] || model.materials.add("Battery Contactor (ML-RBS, in + feed)")
  mat.color = Sketchup::Color.new(196, 43, 28)
  mat.alpha = 1.0
  grp.material = mat

  # Interior E-stop control wire (parallel)
  grp = ents.add_group
  grp.name = "Interior E-stop control wire (parallel)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -135.mm, 0.mm)
  circle = ge.add_circle([2060.mm,165.mm,1580.mm], vec, 5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["E-stop control wire (2x 18 AWG)"] || model.materials.add("E-stop control wire (2x 18 AWG)")
  mat.color = Sketchup::Color.new(106, 61, 168)
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
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
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
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
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
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
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

  # NEMA 5-15R inlet (panel)
  grp = ents.add_group
  grp.name = "NEMA 5-15R inlet (panel)"
  face = grp.entities.add_face([1472.28.mm,-95.mm,2018.72.mm], [1532.28.mm,-95.mm,2018.72.mm], [1532.28.mm,-65.mm,2018.72.mm], [1472.28.mm,-65.mm,2018.72.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(45.mm)
  mat = model.materials["NEMA 5-15R inlet (panel)"] || model.materials.add("NEMA 5-15R inlet (panel)")
  mat.color = Sketchup::Color.new(255, 240, 204)
  mat.alpha = 1.0
  grp.material = mat

  # GFCI AC outlet (Cct E cooler)
  grp = ents.add_group
  grp.name = "GFCI AC outlet (Cct E cooler)"
  ge = grp.entities
  circle = ge.add_circle([1510.78.mm,-85.mm,1908.mm], [0,1,0], 10.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["GFCI AC outlet (Cct E cooler)"] || model.materials.add("GFCI AC outlet (Cct E cooler)")
  mat.color = Sketchup::Color.new(232, 136, 74)
  mat.alpha = 1.0
  grp.material = mat

  # PV Array Disconnect (load-break isolator)
  grp = ents.add_group
  grp.name = "PV Array Disconnect (load-break isolator)"
  face = grp.entities.add_face([1386.mm,22.mm,1834.8.mm], [1456.mm,22.mm,1834.8.mm], [1456.mm,67.mm,1834.8.mm], [1386.mm,67.mm,1834.8.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["Main Disconnect (Blue Sea m-Series)"] || model.materials.add("Main Disconnect (Blue Sea m-Series)")
  mat.color = Sketchup::Color.new(212, 58, 47)
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
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
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
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
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
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
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
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
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
  mat = model.materials["MC4 PV1 (+)"] || model.materials.add("MC4 PV1 (+)")
  mat.color = Sketchup::Color.new(45, 122, 45)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Pinhole-Wall Equipment"
  inst.layer = model.layers["Plumbing & Panel"]

  # ═══ Corridor Plumbing ═══
  defn = model.definitions.add("Corridor Plumbing")
  ents = defn.entities
  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 94.mm)
  circle = ge.add_circle([4530.mm,155.mm,20.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction elbow
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction elbow"
  ge = grp.entities
  arc = ge.add_arc([4530.mm,176.mm,114.mm], [0.000000,-1.000000,0.000000], [-1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4530.mm,155.mm,114.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 133.87.mm, 0.mm)
  circle = ge.add_circle([4530.mm,176.mm,135.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction elbow
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction elbow"
  ge = grp.entities
  arc = ge.add_arc([4530.mm,309.87.mm,116.87.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 18.130000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4530.mm,309.87.mm,135.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -9.6237.mm)
  circle = ge.add_circle([4530.mm,328.mm,116.87.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction elbow
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction elbow"
  ge = grp.entities
  arc = ge.add_arc([4530.mm,337.2463.mm,107.2463.mm], [0.000000,-1.000000,0.000000], [1.000000,-0.000000,0.000000], 9.246300000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4530.mm,328.mm,107.2463.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 641.7537.mm, 0.mm)
  circle = ge.add_circle([4530.mm,337.2463.mm,98.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction elbow
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction elbow"
  ge = grp.entities
  arc = ge.add_arc([4530.mm,979.mm,119.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4530.mm,979.mm,98.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 11.72999999999999.mm)
  circle = ge.add_circle([4530.mm,1000.mm,119.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction elbow
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction elbow"
  ge = grp.entities
  arc = ge.add_arc([4530.mm,1011.27.mm,130.73.mm], [0.000000,-1.000000,0.000000], [-1.000000,0.000000,0.000000], 11.270000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4530.mm,1000.mm,130.73.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 87.73000000000002.mm, 0.mm)
  circle = ge.add_circle([4530.mm,1011.27.mm,142.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction elbow
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction elbow"
  ge = grp.entities
  arc = ge.add_arc([4530.mm,1099.mm,121.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4530.mm,1099.mm,142.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -11.730000000000004.mm)
  circle = ge.add_circle([4530.mm,1120.mm,121.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction elbow
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction elbow"
  ge = grp.entities
  arc = ge.add_arc([4530.mm,1131.27.mm,109.27.mm], [0.000000,-1.000000,0.000000], [1.000000,-0.000000,0.000000], 11.270000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4530.mm,1120.mm,109.27.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 46.559999999999945.mm, 0.mm)
  circle = ge.add_circle([4530.mm,1131.27.mm,98.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction elbow
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction elbow"
  ge = grp.entities
  arc = ge.add_arc([4530.mm,1177.83.mm,81.83.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 16.17.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4530.mm,1177.83.mm,98.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -8.583299999999994.mm)
  circle = ge.add_circle([4530.mm,1194.mm,81.83.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction elbow
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction elbow"
  ge = grp.entities
  arc = ge.add_arc([4538.2467.mm,1194.mm,73.2467.mm], [-1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 8.2467.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4530.mm,1194.mm,73.2467.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(340.7533000000003.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4538.2467.mm,1194.mm,65.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction elbow
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction elbow"
  ge = grp.entities
  arc = ge.add_arc([4879.mm,1194.mm,86.mm], [0.000000,0.000000,-1.000000], [0.000000,-1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4879.mm,1194.mm,65.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 995.mm)
  circle = ge.add_circle([4900.mm,1194.mm,86.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction elbow
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction elbow"
  ge = grp.entities
  arc = ge.add_arc([4900.mm,1173.mm,1081.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4900.mm,1194.mm,1081.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -55.mm, 0.mm)
  circle = ge.add_circle([4900.mm,1173.mm,1102.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction elbow
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction elbow"
  ge = grp.entities
  arc = ge.add_arc([4921.mm,1118.mm,1102.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.000000,1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4900.mm,1118.mm,1102.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(61.039999999999964.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4921.mm,1097.mm,1102.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction elbow
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction elbow"
  ge = grp.entities
  arc = ge.add_arc([4982.04.mm,1098.96.mm,1102.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 1.9600000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4982.04.mm,1097.mm,1102.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 2.0399999999999636.mm, 0.mm)
  circle = ge.add_circle([4984.mm,1098.96.mm,1102.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump strainer foot
  grp = ents.add_group
  grp.name = "Tray sump strainer foot"
  ge = grp.entities
  circle = ge.add_circle([4550.mm,155.mm,20.mm], [0,0,1], 14.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Foot anchor M12"] || model.materials.add("Foot anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # P-04 -> SV-02 -> DV-02
  grp = ents.add_group
  grp.name = "P-04 -> SV-02 -> DV-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 29.mm, 0.mm)
  circle = ge.add_circle([4984.mm,1261.mm,1102.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-04 -> SV-02 -> DV-02 elbow
  grp = ents.add_group
  grp.name = "P-04 -> SV-02 -> DV-02 elbow"
  ge = grp.entities
  arc = ge.add_arc([4984.mm,1290.mm,1123.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4984.mm,1290.mm,1102.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-04 -> SV-02 -> DV-02
  grp = ents.add_group
  grp.name = "P-04 -> SV-02 -> DV-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 891.mm)
  circle = ge.add_circle([4984.mm,1311.mm,1123.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-04 -> SV-02 -> DV-02 elbow
  grp = ents.add_group
  grp.name = "P-04 -> SV-02 -> DV-02 elbow"
  ge = grp.entities
  arc = ge.add_arc([4984.mm,1290.mm,2014.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4984.mm,1311.mm,2014.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-04 -> SV-02 -> DV-02
  grp = ents.add_group
  grp.name = "P-04 -> SV-02 -> DV-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -88.mm, 0.mm)
  circle = ge.add_circle([4984.mm,1290.mm,2035.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-04 -> SV-02 -> DV-02 elbow
  grp = ents.add_group
  grp.name = "P-04 -> SV-02 -> DV-02 elbow"
  ge = grp.entities
  arc = ge.add_arc([5005.mm,1202.mm,2035.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.000000,1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4984.mm,1202.mm,2035.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-04 -> SV-02 -> DV-02
  grp = ents.add_group
  grp.name = "P-04 -> SV-02 -> DV-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.984999999999673.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5005.mm,1181.mm,2035.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-04 -> SV-02 -> DV-02 elbow
  grp = ents.add_group
  grp.name = "P-04 -> SV-02 -> DV-02 elbow"
  ge = grp.entities
  arc = ge.add_arc([5016.985.mm,1181.mm,2046.515.mm], [0.000000,0.000000,-1.000000], [0.000000,-1.000000,0.000000], 11.515000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5016.985.mm,1181.mm,2035.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-04 -> SV-02 -> DV-02
  grp = ents.add_group
  grp.name = "P-04 -> SV-02 -> DV-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 65.4849999999999.mm)
  circle = ge.add_circle([5028.5.mm,1181.mm,2046.515.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) entry
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -39.mm, 0.mm)
  circle = ge.add_circle([5028.5.mm,1148.mm,2145.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) entry elbow
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) entry elbow"
  ge = grp.entities
  arc = ge.add_arc([5049.5.mm,1109.mm,2145.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.000000,1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5028.5.mm,1109.mm,2145.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) entry
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(20.654999999999745.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5049.5.mm,1088.mm,2145.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) entry elbow
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) entry elbow"
  ge = grp.entities
  arc = ge.add_arc([5070.155.mm,1107.845.mm,2145.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 19.845000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5070.155.mm,1088.mm,2145.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) entry
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 52.15499999999997.mm, 0.mm)
  circle = ge.add_circle([5090.mm,1107.845.mm,2145.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) entry elbow
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) entry elbow"
  ge = grp.entities
  arc = ge.add_arc([5090.mm,1160.mm,2124.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5090.mm,1160.mm,2145.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) entry
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -973.mm)
  circle = ge.add_circle([5090.mm,1181.mm,2124.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) entry elbow
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) entry elbow"
  ge = grp.entities
  arc = ge.add_arc([5090.mm,1160.mm,1151.mm], [0.000000,1.000000,0.000000], [-1.000000,-0.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5090.mm,1181.mm,1151.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) entry
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -21.420000000000073.mm, 0.mm)
  circle = ge.add_circle([5090.mm,1160.mm,1130.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) entry elbow
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) entry elbow"
  ge = grp.entities
  arc = ge.add_arc([5069.42.mm,1138.58.mm,1130.mm], [1.000000,0.000000,0.000000], [-0.000000,-0.000000,-1.000000], 20.580000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5090.mm,1138.58.mm,1130.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) entry
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(-20.86920000000009.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5069.42.mm,1118.mm,1130.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) entry elbow
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) entry elbow"
  ge = grp.entities
  arc = ge.add_arc([5048.5508.mm,1097.9492.mm,1130.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 20.050800000000038.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5048.5508.mm,1118.mm,1130.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) entry
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -180.94920000000002.mm, 0.mm)
  circle = ge.add_circle([5028.5.mm,1097.9492.mm,1130.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) entry elbow
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) entry elbow"
  ge = grp.entities
  arc = ge.add_arc([5028.5.mm,917.mm,1109.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5028.5.mm,917.mm,1130.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) entry
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -29.mm)
  circle = ge.add_circle([5028.5.mm,896.mm,1109.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) flange
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) flange"
  ge = grp.entities
  circle = ge.add_circle([5028.5.mm,1054.mm,1130.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(16.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-4 merge
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-4 merge"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 15.809999999999945.mm, 0.mm)
  circle = ge.add_circle([5028.5.mm,1214.mm,2145.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-4 merge elbow
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-4 merge elbow"
  ge = grp.entities
  arc = ge.add_arc([5028.5.mm,1229.81.mm,2129.81.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 15.190000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5028.5.mm,1229.81.mm,2145.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-4 merge
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-4 merge"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -15.203100000000177.mm)
  circle = ge.add_circle([5028.5.mm,1245.mm,2129.81.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-4 merge elbow
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-4 merge elbow"
  ge = grp.entities
  arc = ge.add_arc([5043.1069.mm,1245.mm,2114.6068999999998.mm], [-1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 14.606899999999975.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5028.5.mm,1245.mm,2114.6068999999998.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-4 merge
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-4 merge"
  ge = grp.entities
  vec = Geom::Vector3d.new(224.89310000000023.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5043.1069.mm,1245.mm,2100.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-4 merge elbow
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-4 merge elbow"
  ge = grp.entities
  arc = ge.add_arc([5268.mm,1224.mm,2100.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,-1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5268.mm,1245.mm,2100.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-4 merge
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-4 merge"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -14.789999999999964.mm, 0.mm)
  circle = ge.add_circle([5289.mm,1224.mm,2100.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-4 merge elbow
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-4 merge elbow"
  ge = grp.entities
  arc = ge.add_arc([5289.mm,1209.21.mm,2085.79.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 14.21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5289.mm,1209.21.mm,2100.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-4 merge
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-4 merge"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -834.79.mm)
  circle = ge.add_circle([5289.mm,1195.mm,2085.79.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-4 merge elbow
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-4 merge elbow"
  ge = grp.entities
  arc = ge.add_arc([5310.mm,1195.mm,1251.mm], [-1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5289.mm,1195.mm,1251.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-4 merge
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-4 merge"
  ge = grp.entities
  vec = Geom::Vector3d.new(94.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5310.mm,1195.mm,1230.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 waste merge tee run
  grp = ents.add_group
  grp.name = "IBC-4 waste merge tee run"
  ge = grp.entities
  circle = ge.add_circle([5374.mm,1195.mm,1230.mm], [1,0,0], 15.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(60.mm)
  mat = model.materials["SV-02 tap tee run"] || model.materials.add("SV-02 tap tee run")
  mat.color = Sketchup::Color.new(154, 160, 168)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 waste merge tee branch
  grp = ents.add_group
  grp.name = "IBC-4 waste merge tee branch"
  ge = grp.entities
  circle = ge.add_circle([5404.mm,1195.mm,1194.mm], [0,0,1], 15.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["SV-02 tap tee run"] || model.materials.add("SV-02 tap tee run")
  mat.color = Sketchup::Color.new(154, 160, 168)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 waste merge tee socket cuff
  grp = ents.add_group
  grp.name = "IBC-4 waste merge tee socket cuff"
  ge = grp.entities
  circle = ge.add_circle([5374.mm,1195.mm,1230.mm], [1,0,0], 19.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["SV-02 tap tee run"] || model.materials.add("SV-02 tap tee run")
  mat.color = Sketchup::Color.new(154, 160, 168)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 waste merge tee socket cuff
  grp = ents.add_group
  grp.name = "IBC-4 waste merge tee socket cuff"
  ge = grp.entities
  circle = ge.add_circle([5422.mm,1195.mm,1230.mm], [1,0,0], 19.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["SV-02 tap tee run"] || model.materials.add("SV-02 tap tee run")
  mat.color = Sketchup::Color.new(154, 160, 168)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 waste merge tee socket cuff
  grp = ents.add_group
  grp.name = "IBC-4 waste merge tee socket cuff"
  ge = grp.entities
  circle = ge.add_circle([5404.mm,1195.mm,1194.mm], [0,0,1], 19.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["SV-02 tap tee run"] || model.materials.add("SV-02 tap tee run")
  mat.color = Sketchup::Color.new(154, 160, 168)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 (Waste) entry
  grp = ents.add_group
  grp.name = "IBC-4 (Waste) entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(79.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5404.mm,1195.mm,1230.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 (Waste) entry elbow
  grp = ents.add_group
  grp.name = "IBC-4 (Waste) entry elbow"
  ge = grp.entities
  arc = ge.add_arc([5483.mm,1216.mm,1230.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5483.mm,1195.mm,1230.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 (Waste) entry
  grp = ents.add_group
  grp.name = "IBC-4 (Waste) entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 229.mm, 0.mm)
  circle = ge.add_circle([5504.mm,1216.mm,1230.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 (Waste) entry elbow
  grp = ents.add_group
  grp.name = "IBC-4 (Waste) entry elbow"
  ge = grp.entities
  arc = ge.add_arc([5504.mm,1445.mm,1209.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5504.mm,1445.mm,1230.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 (Waste) entry
  grp = ents.add_group
  grp.name = "IBC-4 (Waste) entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -129.mm)
  circle = ge.add_circle([5504.mm,1466.mm,1209.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 (Waste) flange
  grp = ents.add_group
  grp.name = "IBC-4 (Waste) flange"
  ge = grp.entities
  circle = ge.add_circle([5504.mm,1308.mm,1230.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(16.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction entry
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -15.299999999999955.mm, 0.mm)
  circle = ge.add_circle([4984.mm,1101.mm,777.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction entry elbow
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction entry elbow"
  ge = grp.entities
  arc = ge.add_arc([4969.3.mm,1085.7.mm,777.mm], [1.000000,0.000000,0.000000], [-0.000000,-0.000000,-1.000000], 14.700000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4984.mm,1085.7.mm,777.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction entry
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(-73.72000000000025.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4969.3.mm,1071.mm,777.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction entry elbow
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction entry elbow"
  ge = grp.entities
  arc = ge.add_arc([4895.58.mm,1091.58.mm,777.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,-1.000000], 20.580000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4895.58.mm,1071.mm,777.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction entry
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 10.924199999999928.mm, 0.mm)
  circle = ge.add_circle([4875.mm,1091.58.mm,777.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction entry elbow
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction entry elbow"
  ge = grp.entities
  arc = ge.add_arc([4875.mm,1102.5041999999999.mm,787.4958.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 10.495800000000036.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4875.mm,1102.5041999999999.mm,777.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction entry
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 401.50419999999997.mm)
  circle = ge.add_circle([4875.mm,1113.mm,787.4958.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction entry elbow
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction entry elbow"
  ge = grp.entities
  arc = ge.add_arc([4896.mm,1113.mm,1189.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4875.mm,1113.mm,1189.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction entry
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(283.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4896.mm,1113.mm,1210.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction entry elbow
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction entry elbow"
  ge = grp.entities
  arc = ge.add_arc([5179.mm,1113.mm,1231.mm], [0.000000,0.000000,-1.000000], [0.000000,-1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5179.mm,1113.mm,1210.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction entry
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 148.mm)
  circle = ge.add_circle([5200.mm,1113.mm,1231.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction entry elbow
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction entry elbow"
  ge = grp.entities
  arc = ge.add_arc([5200.mm,1092.mm,1379.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5200.mm,1113.mm,1379.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction entry
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -175.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1092.mm,1400.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction entry elbow
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction entry elbow"
  ge = grp.entities
  arc = ge.add_arc([5200.mm,917.mm,1379.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5200.mm,917.mm,1400.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction entry
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -29.mm)
  circle = ge.add_circle([5200.mm,896.mm,1379.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction flange
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction flange"
  ge = grp.entities
  circle = ge.add_circle([5200.mm,1054.mm,1400.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(16.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # BV-01 (P-01 suction)
  grp = ents.add_group
  grp.name = "BV-01 (P-01 suction)"
  ge = grp.entities
  circle = ge.add_circle([4875.mm,1113.mm,978.mm], [0,0,1], 18.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["BV-03 (P-02 suction)"] || model.materials.add("BV-03 (P-02 suction)")
  mat.color = Sketchup::Color.new(122, 128, 136)
  mat.alpha = 1.0
  grp.material = mat

  # BV-01 (P-01 suction) handle stem
  grp = ents.add_group
  grp.name = "BV-01 (P-01 suction) handle stem"
  ge = grp.entities
  circle = ge.add_circle([4828.5.mm,1113.mm,1000.mm], [1,0,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(28.mm)
  mat = model.materials["SV-02 sample valve handwheel stem"] || model.materials.add("SV-02 sample valve handwheel stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # BV-01 (P-01 suction) handle
  grp = ents.add_group
  grp.name = "BV-01 (P-01 suction) handle"
  face = grp.entities.add_face([4819.5.mm,1106.mm,976.mm], [4828.5.mm,1106.mm,976.mm], [4828.5.mm,1120.mm,976.mm], [4819.5.mm,1120.mm,976.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["SV-02 sample valve handwheel stem"] || model.materials.add("SV-02 sample valve handwheel stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 -> ACC-01 (in)
  grp = ents.add_group
  grp.name = "P-01 -> ACC-01 (in)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 37.5.mm, 0.mm)
  circle = ge.add_circle([4984.mm,1261.mm,777.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 -> ACC-01 (in) elbow
  grp = ents.add_group
  grp.name = "P-01 -> ACC-01 (in) elbow"
  ge = grp.entities
  arc = ge.add_arc([4984.mm,1298.5.mm,756.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4984.mm,1298.5.mm,777.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 -> ACC-01 (in)
  grp = ents.add_group
  grp.name = "P-01 -> ACC-01 (in)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -352.mm)
  circle = ge.add_circle([4984.mm,1319.5.mm,756.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 -> ACC-01 (in) elbow
  grp = ents.add_group
  grp.name = "P-01 -> ACC-01 (in) elbow"
  ge = grp.entities
  arc = ge.add_arc([4984.mm,1298.5.mm,404.mm], [0.000000,1.000000,0.000000], [-1.000000,-0.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4984.mm,1319.5.mm,404.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 -> ACC-01 (in)
  grp = ents.add_group
  grp.name = "P-01 -> ACC-01 (in)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -24.mm, 0.mm)
  circle = ge.add_circle([4984.mm,1298.5.mm,383.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue supply trunk -> spray bar / TAP-01 (off-panel)
  grp = ents.add_group
  grp.name = "Blue supply trunk -> spray bar / TAP-01 (off-panel)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -10.200000000000045.mm, 0.mm)
  circle = ge.add_circle([4984.mm,1087.5.mm,383.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue supply trunk -> spray bar / TAP-01 (off-panel) elbow
  grp = ents.add_group
  grp.name = "Blue supply trunk -> spray bar / TAP-01 (off-panel) elbow"
  ge = grp.entities
  arc = ge.add_arc([4984.mm,1077.3.mm,373.2.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 9.800000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4984.mm,1077.3.mm,383.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue supply trunk -> spray bar / TAP-01 (off-panel)
  grp = ents.add_group
  grp.name = "Blue supply trunk -> spray bar / TAP-01 (off-panel)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -117.19999999999999.mm)
  circle = ge.add_circle([4984.mm,1067.5.mm,373.2.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue supply trunk -> spray bar / TAP-01 (off-panel) elbow
  grp = ents.add_group
  grp.name = "Blue supply trunk -> spray bar / TAP-01 (off-panel) elbow"
  ge = grp.entities
  arc = ge.add_arc([4984.mm,1088.5.mm,256.mm], [0.000000,-1.000000,0.000000], [1.000000,-0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4984.mm,1067.5.mm,256.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue supply trunk -> spray bar / TAP-01 (off-panel)
  grp = ents.add_group
  grp.name = "Blue supply trunk -> spray bar / TAP-01 (off-panel)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 22.5.mm, 0.mm)
  circle = ge.add_circle([4984.mm,1088.5.mm,235.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue supply trunk -> spray bar / TAP-01 (off-panel) elbow
  grp = ents.add_group
  grp.name = "Blue supply trunk -> spray bar / TAP-01 (off-panel) elbow"
  ge = grp.entities
  arc = ge.add_arc([4963.mm,1111.mm,235.mm], [1.000000,0.000000,0.000000], [0.000000,-0.000000,1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4984.mm,1111.mm,235.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue supply trunk -> spray bar / TAP-01 (off-panel)
  grp = ents.add_group
  grp.name = "Blue supply trunk -> spray bar / TAP-01 (off-panel)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-282.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4963.mm,1132.mm,235.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue supply trunk -> spray bar / TAP-01 (off-panel) elbow
  grp = ents.add_group
  grp.name = "Blue supply trunk -> spray bar / TAP-01 (off-panel) elbow"
  ge = grp.entities
  arc = ge.add_arc([4681.mm,1132.mm,214.mm], [0.000000,0.000000,1.000000], [-0.000000,-1.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4681.mm,1132.mm,235.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue supply trunk -> spray bar / TAP-01 (off-panel)
  grp = ents.add_group
  grp.name = "Blue supply trunk -> spray bar / TAP-01 (off-panel)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -154.mm)
  circle = ge.add_circle([4660.mm,1132.mm,214.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Corridor Plumbing"
  inst.layer = model.layers["Plumbing & Panel"]

  # ═══ Corridor Drains + X-ports ═══
  defn = model.definitions.add("Corridor Drains + X-ports")
  ents = defn.entities
  # X1 fill camlock (end wall)
  grp = ents.add_group
  grp.name = "X1 fill camlock (end wall)"
  ge = grp.entities
  circle = ge.add_circle([5833.mm,1195.5.mm,2250.mm], [1,0,0], 26.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(60.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 one-way valve
  grp = ents.add_group
  grp.name = "X1 one-way valve"
  ge = grp.entities
  circle = ge.add_circle([5669.mm,1195.5.mm,2250.mm], [1,0,0], 17.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(48.mm)
  mat = model.materials["X1 one-way valve"] || model.materials.add("X1 one-way valve")
  mat.color = Sketchup::Color.new(138, 43, 226)
  mat.alpha = 1.0
  grp.material = mat

  # X1 camlock -> one-way -> cross (straight)
  grp = ents.add_group
  grp.name = "X1 camlock -> one-way -> cross (straight)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-333.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5833.mm,1195.5.mm,2250.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill cross run
  grp = ents.add_group
  grp.name = "X1 fill cross run"
  ge = grp.entities
  circle = ge.add_circle([5470.mm,1195.5.mm,2250.mm], [1,0,0], 15.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(60.mm)
  mat = model.materials["SV-02 tap tee run"] || model.materials.add("SV-02 tap tee run")
  mat.color = Sketchup::Color.new(154, 160, 168)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill cross run
  grp = ents.add_group
  grp.name = "X1 fill cross run"
  ge = grp.entities
  circle = ge.add_circle([5500.mm,1165.5.mm,2250.mm], [0,1,0], 15.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["SV-02 tap tee run"] || model.materials.add("SV-02 tap tee run")
  mat.color = Sketchup::Color.new(154, 160, 168)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill cross socket cuff
  grp = ents.add_group
  grp.name = "X1 fill cross socket cuff"
  ge = grp.entities
  circle = ge.add_circle([5470.mm,1195.5.mm,2250.mm], [1,0,0], 19.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["SV-02 tap tee run"] || model.materials.add("SV-02 tap tee run")
  mat.color = Sketchup::Color.new(154, 160, 168)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill cross socket cuff
  grp = ents.add_group
  grp.name = "X1 fill cross socket cuff"
  ge = grp.entities
  circle = ge.add_circle([5518.mm,1195.5.mm,2250.mm], [1,0,0], 19.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["SV-02 tap tee run"] || model.materials.add("SV-02 tap tee run")
  mat.color = Sketchup::Color.new(154, 160, 168)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill cross socket cuff
  grp = ents.add_group
  grp.name = "X1 fill cross socket cuff"
  ge = grp.entities
  circle = ge.add_circle([5500.mm,1165.5.mm,2250.mm], [0,1,0], 19.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(12.mm)
  mat = model.materials["SV-02 tap tee run"] || model.materials.add("SV-02 tap tee run")
  mat.color = Sketchup::Color.new(154, 160, 168)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill cross socket cuff
  grp = ents.add_group
  grp.name = "X1 fill cross socket cuff"
  ge = grp.entities
  circle = ge.add_circle([5500.mm,1213.5.mm,2250.mm], [0,1,0], 19.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(12.mm)
  mat = model.materials["SV-02 tap tee run"] || model.materials.add("SV-02 tap tee run")
  mat.color = Sketchup::Color.new(154, 160, 168)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #1 (IBC-1) entry
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #1 (IBC-1) entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -278.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1195.5.mm,2250.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #1 (IBC-1) entry elbow
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #1 (IBC-1) entry elbow"
  ge = grp.entities
  arc = ge.add_arc([5500.mm,917.mm,2229.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5500.mm,917.mm,2250.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #1 (IBC-1) entry
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #1 (IBC-1) entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -129.mm)
  circle = ge.add_circle([5500.mm,896.mm,2229.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #1 (IBC-1) flange
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #1 (IBC-1) flange"
  ge = grp.entities
  circle = ge.add_circle([5500.mm,1054.mm,2250.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(16.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #2 (IBC-2) entry
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #2 (IBC-2) entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 249.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1195.5.mm,2250.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #2 (IBC-2) entry elbow
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #2 (IBC-2) entry elbow"
  ge = grp.entities
  arc = ge.add_arc([5500.mm,1445.mm,2229.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5500.mm,1445.mm,2250.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #2 (IBC-2) entry
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #2 (IBC-2) entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -129.mm)
  circle = ge.add_circle([5500.mm,1466.mm,2229.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #2 (IBC-2) flange
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #2 (IBC-2) flange"
  ge = grp.entities
  circle = ge.add_circle([5500.mm,1308.mm,2250.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(16.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue equalization (IBC-1 <-> IBC-2)
  grp = ents.add_group
  grp.name = "Blue equalization (IBC-1 <-> IBC-2)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 570.mm, 0.mm)
  circle = ge.add_circle([5500.mm,896.mm,1376.mm], vec, 16.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue eq flange (IBC-1)
  grp = ents.add_group
  grp.name = "Blue eq flange (IBC-1)"
  ge = grp.entities
  circle = ge.add_circle([5500.mm,1038.mm,1376.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(16.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue eq flange (IBC-2)
  grp = ents.add_group
  grp.name = "Blue eq flange (IBC-2)"
  ge = grp.entities
  circle = ge.add_circle([5500.mm,1308.mm,1376.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(16.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) bottom tap (shared P-02/P-05)
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) bottom tap (shared P-02/P-05)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 79.mm)
  circle = ge.add_circle([4880.mm,896.mm,208.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) bottom tap (shared P-02/P-05) elbow
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) bottom tap (shared P-02/P-05) elbow"
  ge = grp.entities
  arc = ge.add_arc([4880.mm,917.mm,287.mm], [0.000000,-1.000000,0.000000], [-1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4880.mm,896.mm,287.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) bottom tap (shared P-02/P-05)
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) bottom tap (shared P-02/P-05)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 148.mm, 0.mm)
  circle = ge.add_circle([4880.mm,917.mm,308.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap flange
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap flange"
  ge = grp.entities
  circle = ge.add_circle([4880.mm,1038.mm,308.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(16.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap T run
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap T run"
  ge = grp.entities
  circle = ge.add_circle([4850.mm,1101.mm,308.mm], [1,0,0], 15.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(60.mm)
  mat = model.materials["SV-02 tap tee run"] || model.materials.add("SV-02 tap tee run")
  mat.color = Sketchup::Color.new(154, 160, 168)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap T branch
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap T branch"
  ge = grp.entities
  circle = ge.add_circle([4880.mm,1065.mm,308.mm], [0,1,0], 15.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(36.mm)
  mat = model.materials["SV-02 tap tee run"] || model.materials.add("SV-02 tap tee run")
  mat.color = Sketchup::Color.new(154, 160, 168)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap T socket cuff
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap T socket cuff"
  ge = grp.entities
  circle = ge.add_circle([4850.mm,1101.mm,308.mm], [1,0,0], 19.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["SV-02 tap tee run"] || model.materials.add("SV-02 tap tee run")
  mat.color = Sketchup::Color.new(154, 160, 168)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap T socket cuff
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap T socket cuff"
  ge = grp.entities
  circle = ge.add_circle([4898.mm,1101.mm,308.mm], [1,0,0], 19.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(12.mm)
  mat = model.materials["SV-02 tap tee run"] || model.materials.add("SV-02 tap tee run")
  mat.color = Sketchup::Color.new(154, 160, 168)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap T socket cuff
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap T socket cuff"
  ge = grp.entities
  circle = ge.add_circle([4880.mm,1065.mm,308.mm], [0,1,0], 19.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(12.mm)
  mat = model.materials["SV-02 tap tee run"] || model.materials.add("SV-02 tap tee run")
  mat.color = Sketchup::Color.new(154, 160, 168)
  mat.alpha = 1.0
  grp.material = mat

  # Brown tap -> P-05 inlet
  grp = ents.add_group
  grp.name = "Brown tap -> P-05 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(148.48499999999967.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4910.mm,1101.mm,308.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown tap -> P-05 inlet elbow
  grp = ents.add_group
  grp.name = "Brown tap -> P-05 inlet elbow"
  ge = grp.entities
  arc = ge.add_arc([5058.485.mm,1089.485.mm,308.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,-1.000000], 11.515000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5058.485.mm,1101.mm,308.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown tap -> P-05 inlet
  grp = ents.add_group
  grp.name = "Brown tap -> P-05 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -6.1123499999998785.mm, 0.mm)
  circle = ge.add_circle([5070.mm,1089.485.mm,308.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown tap -> P-05 inlet elbow
  grp = ents.add_group
  grp.name = "Brown tap -> P-05 inlet elbow"
  ge = grp.entities
  arc = ge.add_arc([5070.mm,1083.37265.mm,313.87264999999996.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 5.872649999999952.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5070.mm,1083.37265.mm,308.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown tap -> P-05 inlet
  grp = ents.add_group
  grp.name = "Brown tap -> P-05 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 965.12735.mm)
  circle = ge.add_circle([5070.mm,1077.5.mm,313.87264999999996.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown tap -> P-05 inlet elbow
  grp = ents.add_group
  grp.name = "Brown tap -> P-05 inlet elbow"
  ge = grp.entities
  arc = ge.add_arc([5049.mm,1077.5.mm,1279.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5070.mm,1077.5.mm,1279.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown tap -> P-05 inlet
  grp = ents.add_group
  grp.name = "Brown tap -> P-05 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(-130.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5049.mm,1077.5.mm,1300.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown tap -> P-05 inlet elbow
  grp = ents.add_group
  grp.name = "Brown tap -> P-05 inlet elbow"
  ge = grp.entities
  arc = ge.add_arc([4919.mm,1077.5.mm,1321.mm], [0.000000,0.000000,-1.000000], [0.000000,1.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4919.mm,1077.5.mm,1300.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown tap -> P-05 inlet
  grp = ents.add_group
  grp.name = "Brown tap -> P-05 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 160.mm)
  circle = ge.add_circle([4898.mm,1077.5.mm,1321.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown tap -> P-05 inlet elbow
  grp = ents.add_group
  grp.name = "Brown tap -> P-05 inlet elbow"
  ge = grp.entities
  arc = ge.add_arc([4919.mm,1077.5.mm,1481.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4898.mm,1077.5.mm,1481.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown tap -> P-05 inlet
  grp = ents.add_group
  grp.name = "Brown tap -> P-05 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(53.48499999999967.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4919.mm,1077.5.mm,1502.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown tap -> P-05 inlet elbow
  grp = ents.add_group
  grp.name = "Brown tap -> P-05 inlet elbow"
  ge = grp.entities
  arc = ge.add_arc([4972.485.mm,1089.015.mm,1502.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 11.515000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4972.485.mm,1077.5.mm,1502.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown tap -> P-05 inlet
  grp = ents.add_group
  grp.name = "Brown tap -> P-05 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 11.9849999999999.mm, 0.mm)
  circle = ge.add_circle([4984.mm,1089.015.mm,1502.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # BV-02 (P-05 suction)
  grp = ents.add_group
  grp.name = "BV-02 (P-05 suction)"
  ge = grp.entities
  circle = ge.add_circle([4898.mm,1077.5.mm,1395.mm], [0,0,1], 18.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["BV-03 (P-02 suction)"] || model.materials.add("BV-03 (P-02 suction)")
  mat.color = Sketchup::Color.new(122, 128, 136)
  mat.alpha = 1.0
  grp.material = mat

  # BV-02 (P-05 suction) handle stem
  grp = ents.add_group
  grp.name = "BV-02 (P-05 suction) handle stem"
  ge = grp.entities
  circle = ge.add_circle([4851.5.mm,1077.5.mm,1417.mm], [1,0,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(28.mm)
  mat = model.materials["SV-02 sample valve handwheel stem"] || model.materials.add("SV-02 sample valve handwheel stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # BV-02 (P-05 suction) handle
  grp = ents.add_group
  grp.name = "BV-02 (P-05 suction) handle"
  face = grp.entities.add_face([4842.5.mm,1070.5.mm,1393.mm], [4851.5.mm,1070.5.mm,1393.mm], [4851.5.mm,1084.5.mm,1393.mm], [4842.5.mm,1084.5.mm,1393.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["SV-02 sample valve handwheel stem"] || model.materials.add("SV-02 sample valve handwheel stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # X3 Brown drain port (end wall)
  grp = ents.add_group
  grp.name = "X3 Brown drain port (end wall)"
  ge = grp.entities
  circle = ge.add_circle([5833.mm,1109.mm,1700.mm], [1,0,0], 22.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(60.mm)
  mat = model.materials["X1 one-way valve"] || model.materials.add("X1 one-way valve")
  mat.color = Sketchup::Color.new(138, 43, 226)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 -> X3 end-wall port
  grp = ents.add_group
  grp.name = "P-05 -> X3 end-wall port"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.650000000000091.mm, 0.mm)
  circle = ge.add_circle([4984.mm,1261.mm,1502.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 -> X3 end-wall port elbow
  grp = ents.add_group
  grp.name = "P-05 -> X3 end-wall port elbow"
  ge = grp.entities
  arc = ge.add_arc([4991.35.mm,1268.65.mm,1502.mm], [-1.000000,0.000000,0.000000], [0.000000,0.000000,-1.000000], 7.3500000000000005.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4984.mm,1268.65.mm,1502.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 -> X3 end-wall port
  grp = ents.add_group
  grp.name = "P-05 -> X3 end-wall port"
  ge = grp.entities
  vec = Geom::Vector3d.new(23.460000000000036.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4991.35.mm,1276.mm,1502.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 -> X3 end-wall port elbow
  grp = ents.add_group
  grp.name = "P-05 -> X3 end-wall port elbow"
  ge = grp.entities
  arc = ge.add_arc([5014.81.mm,1260.81.mm,1502.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,-1.000000], 15.190000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5014.81.mm,1276.mm,1502.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 -> X3 end-wall port
  grp = ents.add_group
  grp.name = "P-05 -> X3 end-wall port"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -8.063100000000077.mm, 0.mm)
  circle = ge.add_circle([5030.mm,1260.81.mm,1502.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 -> X3 end-wall port elbow
  grp = ents.add_group
  grp.name = "P-05 -> X3 end-wall port elbow"
  ge = grp.entities
  arc = ge.add_arc([5037.7469.mm,1252.7468999999999.mm,1502.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.000000,1.000000], 7.746899999999974.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5030.mm,1252.7468999999999.mm,1502.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 -> X3 end-wall port
  grp = ents.add_group
  grp.name = "P-05 -> X3 end-wall port"
  ge = grp.entities
  vec = Geom::Vector3d.new(704.2530999999999.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5037.7469.mm,1245.mm,1502.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 -> X3 end-wall port elbow
  grp = ents.add_group
  grp.name = "P-05 -> X3 end-wall port elbow"
  ge = grp.entities
  arc = ge.add_arc([5742.mm,1224.mm,1502.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,-1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5742.mm,1245.mm,1502.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 -> X3 end-wall port
  grp = ents.add_group
  grp.name = "P-05 -> X3 end-wall port"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -94.mm, 0.mm)
  circle = ge.add_circle([5763.mm,1224.mm,1502.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 -> X3 end-wall port elbow
  grp = ents.add_group
  grp.name = "P-05 -> X3 end-wall port elbow"
  ge = grp.entities
  arc = ge.add_arc([5763.mm,1130.mm,1523.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5763.mm,1130.mm,1502.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 -> X3 end-wall port
  grp = ents.add_group
  grp.name = "P-05 -> X3 end-wall port"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 156.mm)
  circle = ge.add_circle([5763.mm,1109.mm,1523.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 -> X3 end-wall port elbow
  grp = ents.add_group
  grp.name = "P-05 -> X3 end-wall port elbow"
  ge = grp.entities
  arc = ge.add_arc([5784.mm,1109.mm,1679.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5763.mm,1109.mm,1679.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 -> X3 end-wall port
  grp = ents.add_group
  grp.name = "P-05 -> X3 end-wall port"
  ge = grp.entities
  vec = Geom::Vector3d.new(49.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5784.mm,1109.mm,1700.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) pickup
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) pickup"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 29.mm)
  circle = ge.add_circle([5200.mm,1466.mm,208.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) pickup elbow
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) pickup elbow"
  ge = grp.entities
  arc = ge.add_arc([5200.mm,1445.mm,237.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5200.mm,1466.mm,237.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) pickup
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) pickup"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -228.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1445.mm,258.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) pickup elbow
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) pickup elbow"
  ge = grp.entities
  arc = ge.add_arc([5200.mm,1217.mm,279.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5200.mm,1217.mm,258.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) pickup
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) pickup"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1400.mm)
  circle = ge.add_circle([5200.mm,1196.mm,279.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) pickup elbow
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) pickup elbow"
  ge = grp.entities
  arc = ge.add_arc([5179.mm,1196.mm,1679.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5200.mm,1196.mm,1679.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) pickup
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) pickup"
  ge = grp.entities
  vec = Geom::Vector3d.new(-138.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5179.mm,1196.mm,1700.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) pickup elbow
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) pickup elbow"
  ge = grp.entities
  arc = ge.add_arc([5041.mm,1175.mm,1700.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5041.mm,1196.mm,1700.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) pickup
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) pickup"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -76.5.mm, 0.mm)
  circle = ge.add_circle([5020.mm,1175.mm,1700.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) pickup elbow
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) pickup elbow"
  ge = grp.entities
  arc = ge.add_arc([4999.mm,1098.5.mm,1700.mm], [1.000000,0.000000,0.000000], [-0.000000,-0.000000,-1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5020.mm,1098.5.mm,1700.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) pickup
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) pickup"
  ge = grp.entities
  vec = Geom::Vector3d.new(-80.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4999.mm,1077.5.mm,1700.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) pickup elbow
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) pickup elbow"
  ge = grp.entities
  arc = ge.add_arc([4919.mm,1077.5.mm,1721.mm], [0.000000,0.000000,-1.000000], [0.000000,1.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4919.mm,1077.5.mm,1700.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) pickup
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) pickup"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 160.mm)
  circle = ge.add_circle([4898.mm,1077.5.mm,1721.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) pickup elbow
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) pickup elbow"
  ge = grp.entities
  arc = ge.add_arc([4919.mm,1077.5.mm,1881.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4898.mm,1077.5.mm,1881.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) pickup
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) pickup"
  ge = grp.entities
  vec = Geom::Vector3d.new(53.48499999999967.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4919.mm,1077.5.mm,1902.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) pickup elbow
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) pickup elbow"
  ge = grp.entities
  arc = ge.add_arc([4972.485.mm,1089.015.mm,1902.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 11.515000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4972.485.mm,1077.5.mm,1902.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) pickup
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) pickup"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 11.9849999999999.mm, 0.mm)
  circle = ge.add_circle([4984.mm,1089.015.mm,1902.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) pickup flange
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) pickup flange"
  ge = grp.entities
  circle = ge.add_circle([5200.mm,1308.mm,258.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(16.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # BV-06 (P-03 suction)
  grp = ents.add_group
  grp.name = "BV-06 (P-03 suction)"
  ge = grp.entities
  circle = ge.add_circle([4898.mm,1077.5.mm,1770.mm], [0,0,1], 18.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["BV-03 (P-02 suction)"] || model.materials.add("BV-03 (P-02 suction)")
  mat.color = Sketchup::Color.new(122, 128, 136)
  mat.alpha = 1.0
  grp.material = mat

  # BV-06 (P-03 suction) handle stem
  grp = ents.add_group
  grp.name = "BV-06 (P-03 suction) handle stem"
  ge = grp.entities
  circle = ge.add_circle([4851.5.mm,1077.5.mm,1792.mm], [1,0,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(28.mm)
  mat = model.materials["SV-02 sample valve handwheel stem"] || model.materials.add("SV-02 sample valve handwheel stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # BV-06 (P-03 suction) handle
  grp = ents.add_group
  grp.name = "BV-06 (P-03 suction) handle"
  face = grp.entities.add_face([4842.5.mm,1070.5.mm,1768.mm], [4851.5.mm,1070.5.mm,1768.mm], [4851.5.mm,1084.5.mm,1768.mm], [4842.5.mm,1084.5.mm,1768.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["SV-02 sample valve handwheel stem"] || model.materials.add("SV-02 sample valve handwheel stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste drain port (end wall)
  grp = ents.add_group
  grp.name = "X4 Waste drain port (end wall)"
  ge = grp.entities
  circle = ge.add_circle([5833.mm,1235.mm,1620.mm], [1,0,0], 22.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(60.mm)
  mat = model.materials["X1 one-way valve"] || model.materials.add("X1 one-way valve")
  mat.color = Sketchup::Color.new(138, 43, 226)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 -> X4 end-wall port
  grp = ents.add_group
  grp.name = "P-03 -> X4 end-wall port"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 15.299999999999955.mm, 0.mm)
  circle = ge.add_circle([4984.mm,1261.mm,1902.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 -> X4 end-wall port elbow
  grp = ents.add_group
  grp.name = "P-03 -> X4 end-wall port elbow"
  ge = grp.entities
  arc = ge.add_arc([4998.7.mm,1276.3.mm,1902.mm], [-1.000000,0.000000,0.000000], [0.000000,0.000000,-1.000000], 14.700000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4984.mm,1276.3.mm,1902.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 -> X4 end-wall port
  grp = ents.add_group
  grp.name = "P-03 -> X4 end-wall port"
  ge = grp.entities
  vec = Geom::Vector3d.new(70.30000000000018.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4998.7.mm,1291.mm,1902.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 -> X4 end-wall port elbow
  grp = ents.add_group
  grp.name = "P-03 -> X4 end-wall port elbow"
  ge = grp.entities
  arc = ge.add_arc([5069.mm,1270.mm,1902.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,-1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5069.mm,1291.mm,1902.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 -> X4 end-wall port
  grp = ents.add_group
  grp.name = "P-03 -> X4 end-wall port"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -17.84999999999991.mm, 0.mm)
  circle = ge.add_circle([5090.mm,1270.mm,1902.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 -> X4 end-wall port elbow
  grp = ents.add_group
  grp.name = "P-03 -> X4 end-wall port elbow"
  ge = grp.entities
  arc = ge.add_arc([5107.15.mm,1252.15.mm,1902.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.000000,1.000000], 17.150000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5090.mm,1252.15.mm,1902.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 -> X4 end-wall port
  grp = ents.add_group
  grp.name = "P-03 -> X4 end-wall port"
  ge = grp.entities
  vec = Geom::Vector3d.new(634.8500000000004.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5107.15.mm,1235.mm,1902.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 -> X4 end-wall port elbow
  grp = ents.add_group
  grp.name = "P-03 -> X4 end-wall port elbow"
  ge = grp.entities
  arc = ge.add_arc([5742.mm,1235.mm,1881.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5742.mm,1235.mm,1902.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 -> X4 end-wall port
  grp = ents.add_group
  grp.name = "P-03 -> X4 end-wall port"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -240.mm)
  circle = ge.add_circle([5763.mm,1235.mm,1881.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 -> X4 end-wall port elbow
  grp = ents.add_group
  grp.name = "P-03 -> X4 end-wall port elbow"
  ge = grp.entities
  arc = ge.add_arc([5784.mm,1235.mm,1641.mm], [-1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5763.mm,1235.mm,1641.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 -> X4 end-wall port
  grp = ents.add_group
  grp.name = "P-03 -> X4 end-wall port"
  ge = grp.entities
  vec = Geom::Vector3d.new(49.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5784.mm,1235.mm,1620.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Corridor Drains + X-ports"
  inst.layer = model.layers["Plumbing & Panel"]

  # ═══ TAP-01 + Spray Supply ═══
  defn = model.definitions.add("TAP-01 + Spray Supply")
  ents = defn.entities
  # Blue trunk: corridor -> ribbon -> outside-rim strip
  grp = ents.add_group
  grp.name = "Blue trunk: corridor -> ribbon -> outside-rim strip"
  ge = grp.entities
  vec = Geom::Vector3d.new(-135.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4660.mm,1132.mm,60.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue trunk: corridor -> ribbon -> outside-rim strip elbow
  grp = ents.add_group
  grp.name = "Blue trunk: corridor -> ribbon -> outside-rim strip elbow"
  ge = grp.entities
  arc = ge.add_arc([4525.mm,1132.mm,81.mm], [0.000000,0.000000,-1.000000], [0.000000,1.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4525.mm,1132.mm,60.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue trunk: corridor -> ribbon -> outside-rim strip
  grp = ents.add_group
  grp.name = "Blue trunk: corridor -> ribbon -> outside-rim strip"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 40.mm)
  circle = ge.add_circle([4504.mm,1132.mm,81.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue trunk: corridor -> ribbon -> outside-rim strip elbow
  grp = ents.add_group
  grp.name = "Blue trunk: corridor -> ribbon -> outside-rim strip elbow"
  ge = grp.entities
  arc = ge.add_arc([4504.mm,1111.mm,121.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4504.mm,1132.mm,121.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue trunk: corridor -> ribbon -> outside-rim strip
  grp = ents.add_group
  grp.name = "Blue trunk: corridor -> ribbon -> outside-rim strip"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -90.mm, 0.mm)
  circle = ge.add_circle([4504.mm,1111.mm,142.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue trunk: corridor -> ribbon -> outside-rim strip elbow
  grp = ents.add_group
  grp.name = "Blue trunk: corridor -> ribbon -> outside-rim strip elbow"
  ge = grp.entities
  arc = ge.add_arc([4504.mm,1021.mm,121.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4504.mm,1021.mm,142.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue trunk: corridor -> ribbon -> outside-rim strip
  grp = ents.add_group
  grp.name = "Blue trunk: corridor -> ribbon -> outside-rim strip"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -11.730000000000004.mm)
  circle = ge.add_circle([4504.mm,1000.mm,121.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue trunk: corridor -> ribbon -> outside-rim strip elbow
  grp = ents.add_group
  grp.name = "Blue trunk: corridor -> ribbon -> outside-rim strip elbow"
  ge = grp.entities
  arc = ge.add_arc([4504.mm,988.73.mm,109.27.mm], [0.000000,1.000000,0.000000], [-1.000000,-0.000000,-0.000000], 11.270000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4504.mm,1000.mm,109.27.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue trunk: corridor -> ribbon -> outside-rim strip
  grp = ents.add_group
  grp.name = "Blue trunk: corridor -> ribbon -> outside-rim strip"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -898.73.mm, 0.mm)
  circle = ge.add_circle([4504.mm,988.73.mm,98.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue trunk: corridor -> ribbon -> outside-rim strip elbow
  grp = ents.add_group
  grp.name = "Blue trunk: corridor -> ribbon -> outside-rim strip elbow"
  ge = grp.entities
  arc = ge.add_arc([4504.mm,90.mm,77.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4504.mm,90.mm,98.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue trunk: corridor -> ribbon -> outside-rim strip
  grp = ents.add_group
  grp.name = "Blue trunk: corridor -> ribbon -> outside-rim strip"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -36.mm)
  circle = ge.add_circle([4504.mm,69.mm,77.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue Supply Trunk (1/2in HDPE)
  grp = ents.add_group
  grp.name = "Blue Supply Trunk (1/2in HDPE)"
  ge = grp.entities
  circle = ge.add_circle([1130.mm,69.mm,41.mm], [1,0,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(3374.mm)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # BV-05 Riser
  grp = ents.add_group
  grp.name = "BV-05 Riser"
  ge = grp.entities
  circle = ge.add_circle([2399.mm,69.mm,41.mm], [0,0,1], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(909.mm)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # BV-05 (spray-bar isolation)
  grp = ents.add_group
  grp.name = "BV-05 (spray-bar isolation)"
  ge = grp.entities
  circle = ge.add_circle([2399.mm,69.mm,928.mm], [0,0,1], 18.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["BV-03 (P-02 suction)"] || model.materials.add("BV-03 (P-02 suction)")
  mat.color = Sketchup::Color.new(122, 128, 136)
  mat.alpha = 1.0
  grp.material = mat

  # BV-05 (spray-bar isolation) handle stem
  grp = ents.add_group
  grp.name = "BV-05 (spray-bar isolation) handle stem"
  ge = grp.entities
  circle = ge.add_circle([2399.mm,87.5.mm,950.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["SV-02 sample valve handwheel stem"] || model.materials.add("SV-02 sample valve handwheel stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # BV-05 (spray-bar isolation) handle
  grp = ents.add_group
  grp.name = "BV-05 (spray-bar isolation) handle"
  face = grp.entities.add_face([2392.mm,115.5.mm,926.mm], [2406.mm,115.5.mm,926.mm], [2406.mm,124.5.mm,926.mm], [2392.mm,124.5.mm,926.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["SV-02 sample valve handwheel stem"] || model.materials.add("SV-02 sample valve handwheel stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # TAP-01 Branch (3/4in)
  grp = ents.add_group
  grp.name = "TAP-01 Branch (3/4in)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1309.mm)
  circle = ge.add_circle([1130.mm,69.mm,41.mm], vec, 12.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # TAP-01 Branch (3/4in) elbow
  grp = ents.add_group
  grp.name = "TAP-01 Branch (3/4in) elbow"
  ge = grp.entities
  arc = ge.add_arc([1130.mm,94.mm,1350.mm], [0.000000,-1.000000,0.000000], [-1.000000,0.000000,0.000000], 25.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1130.mm,69.mm,1350.mm], [0.000000,0.000000,1.000000], 12.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # TAP-01 Branch (3/4in)
  grp = ents.add_group
  grp.name = "TAP-01 Branch (3/4in)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 50.mm, 0.mm)
  circle = ge.add_circle([1130.mm,94.mm,1375.mm], vec, 12.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # TAP-01 Branch (3/4in) elbow
  grp = ents.add_group
  grp.name = "TAP-01 Branch (3/4in) elbow"
  ge = grp.entities
  arc = ge.add_arc([1130.mm,144.mm,1350.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 25.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1130.mm,144.mm,1375.mm], [0.000000,1.000000,0.000000], 12.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # TAP-01 Branch (3/4in)
  grp = ents.add_group
  grp.name = "TAP-01 Branch (3/4in)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -200.mm)
  circle = ge.add_circle([1130.mm,169.mm,1350.mm], vec, 12.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # BV-04 (chem tap isolation)
  grp = ents.add_group
  grp.name = "BV-04 (chem tap isolation)"
  ge = grp.entities
  circle = ge.add_circle([1130.mm,69.mm,988.mm], [0,0,1], 18.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["BV-03 (P-02 suction)"] || model.materials.add("BV-03 (P-02 suction)")
  mat.color = Sketchup::Color.new(122, 128, 136)
  mat.alpha = 1.0
  grp.material = mat

  # BV-04 (chem tap isolation) handle stem
  grp = ents.add_group
  grp.name = "BV-04 (chem tap isolation) handle stem"
  ge = grp.entities
  circle = ge.add_circle([1130.mm,87.5.mm,1010.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["SV-02 sample valve handwheel stem"] || model.materials.add("SV-02 sample valve handwheel stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # BV-04 (chem tap isolation) handle
  grp = ents.add_group
  grp.name = "BV-04 (chem tap isolation) handle"
  face = grp.entities.add_face([1123.mm,115.5.mm,986.mm], [1137.mm,115.5.mm,986.mm], [1137.mm,124.5.mm,986.mm], [1123.mm,124.5.mm,986.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["SV-02 sample valve handwheel stem"] || model.materials.add("SV-02 sample valve handwheel stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "TAP-01 + Spray Supply"
  inst.layer = model.layers["Plumbing & Panel"]

  # ═══ Ribbon Support Cross-beams ═══
  defn = model.definitions.add("Ribbon Support Cross-beams")
  ents = defn.entities
  # Ribbon support cross-beam (welded 40x10)
  grp = ents.add_group
  grp.name = "Ribbon support cross-beam (welded 40x10)"
  face = grp.entities.add_face([4329.mm,197.mm,80.mm], [4629.mm,197.mm,80.mm], [4629.mm,203.mm,80.mm], [4329.mm,203.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Ribbon support cross-beam (welded 40x10)
  grp = ents.add_group
  grp.name = "Ribbon support cross-beam (welded 40x10)"
  face = grp.entities.add_face([4329.mm,447.mm,80.mm], [4629.mm,447.mm,80.mm], [4629.mm,453.mm,80.mm], [4329.mm,453.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Ribbon support cross-beam (welded 40x10)
  grp = ents.add_group
  grp.name = "Ribbon support cross-beam (welded 40x10)"
  face = grp.entities.add_face([4329.mm,697.mm,80.mm], [4629.mm,697.mm,80.mm], [4629.mm,703.mm,80.mm], [4329.mm,703.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Ribbon support cross-beam (welded 40x10)
  grp = ents.add_group
  grp.name = "Ribbon support cross-beam (welded 40x10)"
  face = grp.entities.add_face([4329.mm,947.mm,80.mm], [4629.mm,947.mm,80.mm], [4629.mm,953.mm,80.mm], [4329.mm,953.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Ribbon Support Cross-beams"
  inst.layer = model.layers["Plumbing & Panel"]

  # ═══ Walkway Cantilever Arms ═══
  defn = model.definitions.add("Walkway Cantilever Arms")
  ents = defn.entities
  # RWk center cantilever Yd1046 lower
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 lower"
  face = grp.entities.add_face([4329.mm,1046.mm,70.mm], [4654.mm,1046.mm,70.mm], [4654.mm,1086.mm,70.mm], [4329.mm,1086.mm,70.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1046 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 upper"
  face = grp.entities.add_face([4369.mm,1046.mm,95.mm], [4589.mm,1046.mm,95.mm], [4589.mm,1086.mm,95.mm], [4369.mm,1086.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1046 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 upper"
  face = grp.entities.add_face([4629.mm,1046.mm,95.mm], [4654.mm,1046.mm,95.mm], [4654.mm,1086.mm,95.mm], [4629.mm,1086.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1046 Y1038
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1046 Y1038"
  face = grp.entities.add_face([4650.mm,1038.mm,45.mm], [4708.mm,1038.mm,45.mm], [4708.mm,1046.mm,45.mm], [4650.mm,1046.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1046 Y1086
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1046 Y1086"
  face = grp.entities.add_face([4650.mm,1086.mm,45.mm], [4708.mm,1086.mm,45.mm], [4708.mm,1094.mm,45.mm], [4650.mm,1094.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1046 Z76
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1046 Z76"
  ge = grp.entities
  circle = ge.add_circle([4679.mm,1034.mm,76.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(64.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1046 Z133
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1046 Z133"
  ge = grp.entities
  circle = ge.add_circle([4679.mm,1034.mm,133.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(64.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1266 lower
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 lower"
  face = grp.entities.add_face([4329.mm,1266.mm,70.mm], [4654.mm,1266.mm,70.mm], [4654.mm,1306.mm,70.mm], [4329.mm,1306.mm,70.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1266 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 upper"
  face = grp.entities.add_face([4369.mm,1266.mm,95.mm], [4589.mm,1266.mm,95.mm], [4589.mm,1306.mm,95.mm], [4369.mm,1306.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1266 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 upper"
  face = grp.entities.add_face([4629.mm,1266.mm,95.mm], [4654.mm,1266.mm,95.mm], [4654.mm,1306.mm,95.mm], [4629.mm,1306.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1266 Y1258
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1266 Y1258"
  face = grp.entities.add_face([4650.mm,1258.mm,45.mm], [4708.mm,1258.mm,45.mm], [4708.mm,1266.mm,45.mm], [4650.mm,1266.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1266 Y1306
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1266 Y1306"
  face = grp.entities.add_face([4650.mm,1306.mm,45.mm], [4708.mm,1306.mm,45.mm], [4708.mm,1314.mm,45.mm], [4650.mm,1314.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1266 Z76
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1266 Z76"
  ge = grp.entities
  circle = ge.add_circle([4679.mm,1254.mm,76.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(64.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1266 Z133
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1266 Z133"
  ge = grp.entities
  circle = ge.add_circle([4679.mm,1254.mm,133.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(64.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Walkway Cantilever Arms"
  inst.layer = model.layers["Walkway Cantilever"]


# ── In-model labels (on the 'Labels' tag; visible only in the "Labeled" scene) ──
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "IBC Frame" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("IBC FRAME
(restraint front portal)", anc, Geom::Vector3d.new(-250.mm, 750.mm, 650.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Walkway Cantilever Arms" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("RIGHT-WALKWAY
CANTILEVER ARMS
(off the IBC corridor
uprights — rev12)", anc, Geom::Vector3d.new(-350.mm, -900.mm, 700.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
anc = Geom::Point3d.new(5284.mm, 538.mm, 579.mm)
txt = entities.add_text("BROWN IBC
(developer)", anc, Geom::Vector3d.new(-1550.mm, -900.mm, -500.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(5284.mm, 538.mm, 1589.mm)
txt = entities.add_text("BLUE IBC #1
(fresh water)", anc, Geom::Vector3d.new(-1550.mm, -900.mm, 550.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(5284.mm, 1824.mm, 579.mm)
txt = entities.add_text("WASTE IBC", anc, Geom::Vector3d.new(1550.mm, -250.mm, 250.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(5284.mm, 1824.mm, 1589.mm)
txt = entities.add_text("BLUE IBC #2
(fresh water)", anc, Geom::Vector3d.new(1550.mm, -250.mm, 400.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4550.mm, 155.mm, 20.mm)
txt = entities.add_text("SUMP PICKUP
(tray drain)", anc, Geom::Vector3d.new(-650.mm, -900.mm, 950.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4649.mm, 12.mm, 40.mm)
txt = entities.add_text("TO SPRAY BAR", anc, Geom::Vector3d.new(-1250.mm, -650.mm, -150.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(5893.mm, 1181.mm, 2250.mm)
txt = entities.add_text("X1 (fresh fill)", anc, Geom::Vector3d.new(1007.mm, -400.mm, 450.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(5893.mm, 1181.mm, 400.mm)
txt = entities.add_text("X3 (Brown drain-out)", anc, Geom::Vector3d.new(1007.mm, -500.mm, -50.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(5893.mm, 1181.mm, 200.mm)
txt = entities.add_text("X4 (Waste drain-out)", anc, Geom::Vector3d.new(1007.mm, -500.mm, -100.mm))
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
keep_tags = ["Context", "IBC Tanks", "IBC Frame", "Plumbing & Panel", "Walkway Cantilever", "Labels"]
default_layer = model.layers[0]
model.layers.to_a.each { |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}

# ── Scenes ── one consistent iso camera, shared by every scene.
# Frame on geometry only — hide the Labels tag so Text bounds don't skew extents.
model.layers.each { |l| l.visible = (l.name != "Labels") }
bb = model.bounds
ctr = bb.center
dir = Geom::Vector3d.new(0.72, -0.7, 0.5); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.5)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

[["Overview", ["Context", "IBC Tanks", "IBC Frame", "Plumbing & Panel", "Walkway Cantilever"]], ["IBC Tanks", ["IBC Tanks"]], ["IBC Frame", ["IBC Frame", "Walkway Cantilever"]], ["Plumbing & Panel", ["Plumbing & Panel"]], ["Labeled", ["Context", "IBC Tanks", "IBC Frame", "Plumbing & Panel", "Walkway Cantilever", "Labels"]]].each { |name, tags|
  model.layers.each { |l| l.visible = (l == default_layer || l.name == "Context" || tags.include?(l.name)) }
  page = model.pages.add(name)
  page.use_camera = true
}
model.layers.each { |l| l.visible = true }

model.commit_operation
{ success: true, model: "IBC Stack",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
