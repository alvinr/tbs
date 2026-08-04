# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/ — do not edit this .rb directly.
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

# ── Sketchfab metadata — sketchfab dict fill-only-if-blank; name/desc forced when requested ──
model.name = "TBS-001 IBC Model" if model.name.to_s.strip.empty?
model.description = "Details of the IBC stack, frame and plumbing panel." if model.description.to_s.strip.empty?
model.set_attribute("sketchfab", "model_title", "TBS-001 IBC Model") if model.get_attribute("sketchfab", "model_title").to_s.strip.empty?
model.set_attribute("sketchfab", "model_description", "Details of the IBC stack, frame and plumbing panel.") if model.get_attribute("sketchfab", "model_description").to_s.strip.empty?
model.set_attribute("sketchfab", "model_id", "8d091c60e93848f38e26c9c89a08cbc8") if model.get_attribute("sketchfab", "model_id").to_s.strip.empty?
model.set_attribute("sketchfab", "model_tags", "sketchup") if model.get_attribute("sketchfab", "model_tags").to_s.strip.empty?

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
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,520.mm,585.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,520.mm,1785.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,940.mm,585.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,940.mm,1785.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,1422.mm,585.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,1422.mm,1785.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,1842.mm,585.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,1842.mm,1785.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat.color = Sketchup::Color.new(154, 160, 166)
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
  mat.color = Sketchup::Color.new(154, 160, 166)
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
  mat.color = Sketchup::Color.new(154, 160, 166)
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
  mat.color = Sketchup::Color.new(154, 160, 166)
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
  mat.color = Sketchup::Color.new(154, 160, 166)
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
  circle = ge.add_circle([3300.mm,104.mm,1746.mm], [0,0,1], 92.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(516.mm)
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
  mat.color = Sketchup::Color.new(26, 26, 26)
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
  mat.color = Sketchup::Color.new(26, 26, 26)
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
  mat.color = Sketchup::Color.new(26, 26, 26)
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
  circle = ge.add_circle([3638.mm,104.mm,1746.mm], [0,0,1], 92.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(516.mm)
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
  mat.color = Sketchup::Color.new(26, 26, 26)
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
  mat.color = Sketchup::Color.new(26, 26, 26)
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
  mat.color = Sketchup::Color.new(26, 26, 26)
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
  circle = ge.add_circle([3976.mm,104.mm,1746.mm], [0,0,1], 92.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(516.mm)
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
  mat.color = Sketchup::Color.new(26, 26, 26)
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
  mat.color = Sketchup::Color.new(26, 26, 26)
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
  mat.color = Sketchup::Color.new(26, 26, 26)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(-57.39590000000044.mm, 0.mm, 0.mm)
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
  arc = ge.add_arc([4660.355.mm,1110.mm,84.355.mm], [0.000000,0.000000,-1.000000], [0.000000,1.000000,-0.000000], 19.355000000000004.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4660.355.mm,1110.mm,65.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 10.27395.mm)
  circle = ge.add_circle([4641.mm,1110.mm,84.355.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4631.12895.mm,1110.mm,94.62895.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 9.87105.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4641.mm,1110.mm,94.62895.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(-54.12895000000026.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4631.12895.mm,1110.mm,104.5.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4577.mm,1110.mm,125.5.mm], [0.000000,0.000000,-1.000000], [0.000000,1.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4577.mm,1110.mm,104.5.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 13.514999999999986.mm)
  circle = ge.add_circle([4556.mm,1110.mm,125.5.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4556.mm,1097.015.mm,139.015.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 12.985000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4556.mm,1110.mm,139.015.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -76.0150000000001.mm, 0.mm)
  circle = ge.add_circle([4556.mm,1097.015.mm,152.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4556.mm,1021.mm,131.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4556.mm,1021.mm,152.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -13.515.mm)
  circle = ge.add_circle([4556.mm,1000.mm,131.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4556.mm,987.015.mm,117.485.mm], [0.000000,1.000000,0.000000], [-1.000000,-0.000000,-0.000000], 12.985000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4556.mm,1000.mm,117.485.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -911.015.mm, 0.mm)
  circle = ge.add_circle([4556.mm,987.015.mm,104.5.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4556.mm,76.mm,83.5.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4556.mm,76.mm,104.5.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 (Brown) tap -> P-02 inlet
  grp = ents.add_group
  grp.name = "IBC-3 (Brown) tap -> P-02 inlet"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -37.5.mm)
  circle = ge.add_circle([4556.mm,55.mm,83.5.mm], vec, 10.5.mm, 16)
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  mat.color = Sketchup::Color.new(128, 128, 138)
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 17.085000000000008.mm)
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
  arc = ge.add_arc([4478.mm,76.415.mm,88.08500000000001.mm], [0.000000,-1.000000,0.000000], [-1.000000,0.000000,0.000000], 16.415000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4478.mm,60.mm,88.08500000000001.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 902.585.mm, 0.mm)
  circle = ge.add_circle([4478.mm,76.41499999999999.mm,104.5.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4478.mm,979.mm,125.5.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4478.mm,979.mm,104.5.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 13.514999999999986.mm)
  circle = ge.add_circle([4478.mm,1000.mm,125.5.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4478.mm,1012.985.mm,139.015.mm], [0.000000,-1.000000,0.000000], [-1.000000,0.000000,0.000000], 12.985000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4478.mm,1000.mm,139.015.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 76.01499999999999.mm, 0.mm)
  circle = ge.add_circle([4478.mm,1012.985.mm,152.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4478.mm,1089.mm,131.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4478.mm,1089.mm,152.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -13.515.mm)
  circle = ge.add_circle([4478.mm,1110.mm,131.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4478.mm,1122.985.mm,117.485.mm], [0.000000,-1.000000,0.000000], [1.000000,-0.000000,0.000000], 12.985000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4478.mm,1110.mm,117.485.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 97.0150000000001.mm, 0.mm)
  circle = ge.add_circle([4478.mm,1122.985.mm,104.5.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4499.mm,1220.mm,104.5.mm], [-1.000000,0.000000,0.000000], [0.000000,0.000000,-1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4478.mm,1220.mm,104.5.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(122.64500000000044.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4499.mm,1241.mm,104.5.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4621.645.mm,1241.mm,85.145.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 19.355000000000004.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4621.645.mm,1241.mm,104.5.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -10.27395.mm)
  circle = ge.add_circle([4641.mm,1241.mm,85.145.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4650.87105.mm,1241.mm,74.87105.mm], [-1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 9.87105.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4641.mm,1241.mm,74.87105.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Filter F1 sump"] || model.materials.add("Filter F1 sump")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 -> DV-01 (single filtered line)
  grp = ents.add_group
  grp.name = "SV-01 -> DV-01 (single filtered line)"
  ge = grp.entities
  vec = Geom::Vector3d.new(28.12895000000026.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4650.87105.mm,1241.mm,65.mm], vec, 10.5.mm, 16)
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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

  # ═══ Corridor Plumbing ═══
  defn = model.definitions.add("Corridor Plumbing")
  ents = defn.entities
  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 80.5.mm)
  circle = ge.add_circle([2399.mm,155.mm,3.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([2420.mm,155.mm,83.5.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2399.mm,155.mm,83.5.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(2063.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2420.mm,155.mm,104.5.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4483.mm,176.mm,104.5.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4483.mm,155.mm,104.5.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 803.mm, 0.mm)
  circle = ge.add_circle([4504.mm,176.mm,104.5.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4504.mm,979.mm,125.5.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4504.mm,979.mm,104.5.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 13.514999999999986.mm)
  circle = ge.add_circle([4504.mm,1000.mm,125.5.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4504.mm,1012.985.mm,139.015.mm], [0.000000,-1.000000,0.000000], [-1.000000,0.000000,0.000000], 12.985000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4504.mm,1000.mm,139.015.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 76.01499999999999.mm, 0.mm)
  circle = ge.add_circle([4504.mm,1012.985.mm,152.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4504.mm,1089.mm,131.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4504.mm,1089.mm,152.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -13.515.mm)
  circle = ge.add_circle([4504.mm,1110.mm,131.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4504.mm,1122.985.mm,117.485.mm], [0.000000,-1.000000,0.000000], [1.000000,-0.000000,0.000000], 12.985000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4504.mm,1110.mm,117.485.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 50.0150000000001.mm, 0.mm)
  circle = ge.add_circle([4504.mm,1122.985.mm,104.5.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4525.mm,1173.mm,104.5.mm], [-1.000000,0.000000,0.000000], [0.000000,0.000000,-1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4504.mm,1173.mm,104.5.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(96.64500000000044.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4525.mm,1194.mm,104.5.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4621.645.mm,1194.mm,85.145.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 19.355000000000004.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4621.645.mm,1194.mm,104.5.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -10.27395.mm)
  circle = ge.add_circle([4641.mm,1194.mm,85.145.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4650.87105.mm,1194.mm,74.87105.mm], [-1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 9.87105.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4641.mm,1194.mm,74.87105.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(228.12895000000026.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4650.87105.mm,1194.mm,65.mm], vec, 10.5.mm, 16)
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  circle = ge.add_circle([2399.mm,155.mm,3.mm], [0,0,1], 14.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(51, 52, 58)
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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

  # DV-02 -> IBC-3 (Brown) flex jumper
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 6.mm, 0.mm)
  circle = ge.add_circle([5028.5.mm,1064.mm,1130.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) flex jumper
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 6.mm, 0.mm)
  circle = ge.add_circle([5028.5.mm,1070.mm,1130.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) flex jumper
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 6.mm, 0.mm)
  circle = ge.add_circle([5028.5.mm,1076.mm,1130.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) flex jumper
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 6.mm, 0.mm)
  circle = ge.add_circle([5028.5.mm,1082.mm,1130.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) flex jumper
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 6.mm, 0.mm)
  circle = ge.add_circle([5028.5.mm,1088.mm,1130.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) flex jumper
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 6.mm, 0.mm)
  circle = ge.add_circle([5028.5.mm,1094.mm,1130.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) flex jumper
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 6.mm, 0.mm)
  circle = ge.add_circle([5028.5.mm,1100.mm,1130.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 -> IBC-3 (Brown) flex jumper
  grp = ents.add_group
  grp.name = "DV-02 -> IBC-3 (Brown) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 6.mm, 0.mm)
  circle = ge.add_circle([5028.5.mm,1106.mm,1130.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  mat.color = Sketchup::Color.new(154, 160, 166)
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
  mat.color = Sketchup::Color.new(154, 160, 166)
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
  mat.color = Sketchup::Color.new(154, 160, 166)
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
  mat.color = Sketchup::Color.new(154, 160, 166)
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
  mat.color = Sketchup::Color.new(154, 160, 166)
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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

  # IBC-4 (Waste) flex jumper
  grp = ents.add_group
  grp.name = "IBC-4 (Waste) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5504.mm,1298.mm,1230.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 (Waste) flex jumper
  grp = ents.add_group
  grp.name = "IBC-4 (Waste) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5504.mm,1290.5.mm,1230.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 (Waste) flex jumper
  grp = ents.add_group
  grp.name = "IBC-4 (Waste) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5504.mm,1283.mm,1230.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 (Waste) flex jumper
  grp = ents.add_group
  grp.name = "IBC-4 (Waste) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5504.mm,1275.5.mm,1230.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 (Waste) flex jumper
  grp = ents.add_group
  grp.name = "IBC-4 (Waste) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5504.mm,1268.mm,1230.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 (Waste) flex jumper
  grp = ents.add_group
  grp.name = "IBC-4 (Waste) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5504.mm,1260.5.mm,1230.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 (Waste) flex jumper
  grp = ents.add_group
  grp.name = "IBC-4 (Waste) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5504.mm,1253.mm,1230.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 (Waste) flex jumper
  grp = ents.add_group
  grp.name = "IBC-4 (Waste) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5504.mm,1245.5.mm,1230.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 (Waste) flex jumper
  grp = ents.add_group
  grp.name = "IBC-4 (Waste) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5504.mm,1238.mm,1230.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 (Waste) flex jumper
  grp = ents.add_group
  grp.name = "IBC-4 (Waste) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5504.mm,1230.5.mm,1230.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 (Waste) flex jumper
  grp = ents.add_group
  grp.name = "IBC-4 (Waste) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5504.mm,1223.mm,1230.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 (Waste) flex jumper
  grp = ents.add_group
  grp.name = "IBC-4 (Waste) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5504.mm,1215.5.mm,1230.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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

  # Blue #1 -> P-01 suction flex jumper
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.375.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1064.mm,1400.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction flex jumper
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.375.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1069.375.mm,1400.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction flex jumper
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.375.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1074.75.mm,1400.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction flex jumper
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.375.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1080.125.mm,1400.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction flex jumper
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.375.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1085.5.mm,1400.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction flex jumper
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.375.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1090.875.mm,1400.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction flex jumper
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.375.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1096.25.mm,1400.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 -> P-01 suction flex jumper
  grp = ents.add_group
  grp.name = "Blue #1 -> P-01 suction flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.375.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1101.625.mm,1400.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
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
  mat.color = Sketchup::Color.new(128, 128, 138)
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue supply trunk -> spray bar / TAP-01 (off-panel)
  grp = ents.add_group
  grp.name = "Blue supply trunk -> spray bar / TAP-01 (off-panel)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-272.mm, 0.mm, 0.mm)
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
  arc = ge.add_arc([4691.mm,1132.mm,214.mm], [0.000000,0.000000,1.000000], [-0.000000,-1.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4691.mm,1132.mm,235.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue supply trunk -> spray bar / TAP-01 (off-panel)
  grp = ents.add_group
  grp.name = "Blue supply trunk -> spray bar / TAP-01 (off-panel)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -154.mm)
  circle = ge.add_circle([4670.mm,1132.mm,214.mm], vec, 10.5.mm, 16)
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
  mat.color = Sketchup::Color.new(154, 160, 166)
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
  mat.color = Sketchup::Color.new(154, 160, 166)
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
  mat.color = Sketchup::Color.new(154, 160, 166)
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
  mat.color = Sketchup::Color.new(154, 160, 166)
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
  mat.color = Sketchup::Color.new(154, 160, 166)
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
  mat.color = Sketchup::Color.new(154, 160, 166)
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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

  # X1 fill -> Blue #1 (IBC-1) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #1 (IBC-1) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1064.mm,2250.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #1 (IBC-1) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #1 (IBC-1) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1071.5.mm,2250.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #1 (IBC-1) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #1 (IBC-1) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1079.mm,2250.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #1 (IBC-1) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #1 (IBC-1) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1086.5.mm,2250.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #1 (IBC-1) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #1 (IBC-1) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1094.mm,2250.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #1 (IBC-1) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #1 (IBC-1) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1101.5.mm,2250.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #1 (IBC-1) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #1 (IBC-1) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1109.mm,2250.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #1 (IBC-1) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #1 (IBC-1) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1116.5.mm,2250.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #1 (IBC-1) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #1 (IBC-1) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1124.mm,2250.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #1 (IBC-1) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #1 (IBC-1) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1131.5.mm,2250.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #1 (IBC-1) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #1 (IBC-1) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1139.mm,2250.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #1 (IBC-1) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #1 (IBC-1) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1146.5.mm,2250.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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

  # X1 fill -> Blue #2 (IBC-2) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #2 (IBC-2) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1298.mm,2250.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #2 (IBC-2) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #2 (IBC-2) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1290.5.mm,2250.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #2 (IBC-2) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #2 (IBC-2) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1283.mm,2250.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #2 (IBC-2) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #2 (IBC-2) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1275.5.mm,2250.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #2 (IBC-2) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #2 (IBC-2) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1268.mm,2250.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #2 (IBC-2) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #2 (IBC-2) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1260.5.mm,2250.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #2 (IBC-2) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #2 (IBC-2) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1253.mm,2250.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #2 (IBC-2) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #2 (IBC-2) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1245.5.mm,2250.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #2 (IBC-2) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #2 (IBC-2) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1238.mm,2250.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #2 (IBC-2) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #2 (IBC-2) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1230.5.mm,2250.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #2 (IBC-2) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #2 (IBC-2) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1223.mm,2250.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # X1 fill -> Blue #2 (IBC-2) flex jumper
  grp = ents.add_group
  grp.name = "X1 fill -> Blue #2 (IBC-2) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5500.mm,1215.5.mm,2250.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  mat.color = Sketchup::Color.new(154, 160, 166)
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
  mat.color = Sketchup::Color.new(154, 160, 166)
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
  mat.color = Sketchup::Color.new(154, 160, 166)
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
  mat.color = Sketchup::Color.new(154, 160, 166)
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
  mat.color = Sketchup::Color.new(154, 160, 166)
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  mat.color = Sketchup::Color.new(128, 128, 138)
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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

  # X4 Waste (P-03) flex jumper
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1298.mm,258.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) flex jumper
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1290.5.mm,258.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) flex jumper
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1283.mm,258.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) flex jumper
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1275.5.mm,258.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) flex jumper
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1268.mm,258.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) flex jumper
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1260.5.mm,258.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) flex jumper
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1253.mm,258.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) flex jumper
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1245.5.mm,258.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) flex jumper
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1238.mm,258.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) flex jumper
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1230.5.mm,258.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) flex jumper
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1223.mm,258.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # X4 Waste (P-03) flex jumper
  grp = ents.add_group
  grp.name = "X4 Waste (P-03) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.5.mm, 0.mm)
  circle = ge.add_circle([5200.mm,1215.5.mm,258.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
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
  mat.color = Sketchup::Color.new(128, 128, 138)
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
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
  vec = Geom::Vector3d.new(-14.789999999999964.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4670.mm,1132.mm,60.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4655.21.mm,1132.mm,74.21000000000001.mm], [0.000000,0.000000,-1.000000], [0.000000,1.000000,-0.000000], 14.21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4655.21.mm,1132.mm,60.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue trunk: corridor -> ribbon -> outside-rim strip
  grp = ents.add_group
  grp.name = "Blue trunk: corridor -> ribbon -> outside-rim strip"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 15.447900000000004.mm)
  circle = ge.add_circle([4641.mm,1132.mm,74.21.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4626.1579.mm,1132.mm,89.6579.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 14.842100000000004.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4641.mm,1132.mm,89.6579.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue trunk: corridor -> ribbon -> outside-rim strip
  grp = ents.add_group
  grp.name = "Blue trunk: corridor -> ribbon -> outside-rim strip"
  ge = grp.entities
  vec = Geom::Vector3d.new(-85.37790000000041.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4626.1579.mm,1132.mm,104.5.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4540.78.mm,1121.22.mm,104.5.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 10.780000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4540.78.mm,1132.mm,104.5.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue trunk: corridor -> ribbon -> outside-rim strip
  grp = ents.add_group
  grp.name = "Blue trunk: corridor -> ribbon -> outside-rim strip"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -5.72219999999993.mm, 0.mm)
  circle = ge.add_circle([4530.mm,1121.22.mm,104.5.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4530.mm,1115.4978.mm,109.99780000000001.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 5.497800000000014.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4530.mm,1115.4978.mm,104.5.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue trunk: corridor -> ribbon -> outside-rim strip
  grp = ents.add_group
  grp.name = "Blue trunk: corridor -> ribbon -> outside-rim strip"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 21.421121999999997.mm)
  circle = ge.add_circle([4530.mm,1110.mm,109.99780000000001.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4530.mm,1089.418922.mm,131.418922.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 20.581077999999998.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4530.mm,1110.mm,131.418922.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue trunk: corridor -> ribbon -> outside-rim strip
  grp = ents.add_group
  grp.name = "Blue trunk: corridor -> ribbon -> outside-rim strip"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -68.41892200000007.mm, 0.mm)
  circle = ge.add_circle([4530.mm,1089.418922.mm,152.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4530.mm,1021.mm,131.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4530.mm,1021.mm,152.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue trunk: corridor -> ribbon -> outside-rim strip
  grp = ents.add_group
  grp.name = "Blue trunk: corridor -> ribbon -> outside-rim strip"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -13.515.mm)
  circle = ge.add_circle([4530.mm,1000.mm,131.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4530.mm,987.015.mm,117.485.mm], [0.000000,1.000000,0.000000], [-1.000000,-0.000000,-0.000000], 12.985000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4530.mm,1000.mm,117.485.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue trunk: corridor -> ribbon -> outside-rim strip
  grp = ents.add_group
  grp.name = "Blue trunk: corridor -> ribbon -> outside-rim strip"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -897.015.mm, 0.mm)
  circle = ge.add_circle([4530.mm,987.015.mm,104.5.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4530.mm,90.mm,83.5.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4530.mm,90.mm,104.5.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue trunk: corridor -> ribbon -> outside-rim strip
  grp = ents.add_group
  grp.name = "Blue trunk: corridor -> ribbon -> outside-rim strip"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -35.5.mm)
  circle = ge.add_circle([4530.mm,69.mm,83.5.mm], vec, 10.5.mm, 16)
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
  circle = ge.add_circle([1130.mm,69.mm,48.mm], [1,0,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(3400.mm)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # BV-05 Riser
  grp = ents.add_group
  grp.name = "BV-05 Riser"
  ge = grp.entities
  circle = ge.add_circle([2399.mm,69.mm,48.mm], [0,0,1], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(902.mm)
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
  mat.color = Sketchup::Color.new(128, 128, 138)
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

  # BV-05 top elbow (spray-bar supply, 90°)
  grp = ents.add_group
  grp.name = "BV-05 top elbow (spray-bar supply, 90°)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 56.mm)
  circle = ge.add_circle([2399.mm,69.mm,990.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # BV-05 top elbow (spray-bar supply, 90°) elbow
  grp = ents.add_group
  grp.name = "BV-05 top elbow (spray-bar supply, 90°) elbow"
  ge = grp.entities
  arc = ge.add_arc([2399.mm,83.mm,1046.mm], [0.000000,-1.000000,0.000000], [-1.000000,0.000000,0.000000], 14.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2399.mm,69.mm,1046.mm], [0.000000,0.000000,1.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # BV-05 top elbow (spray-bar supply, 90°)
  grp = ents.add_group
  grp.name = "BV-05 top elbow (spray-bar supply, 90°)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 77.mm, 0.mm)
  circle = ge.add_circle([2399.mm,83.mm,1060.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 24.mm, -81.mm)
  circle = ge.add_circle([2399.mm,160.mm,1060.mm], vec, 7.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-27.673422065754494.mm, -22.15464397755659.mm, -22.95710381419417.mm)
  circle = ge.add_circle([2399.mm,184.mm,979.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.52637013341382.mm, 30.962497150547307.mm, -7.218691628089346.mm)
  circle = ge.add_circle([2371.3265779342455.mm,161.8453560224434.mm,956.0428961858058.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.346156396661627.mm, 31.033903797789975.mm, -7.1975341029803985.mm)
  circle = ge.add_circle([2359.8002078008317.mm,192.80785317299072.mm,948.8242045577165.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(27.598360505677192.mm, 15.602797209598862.mm, -11.769713832814887.mm)
  circle = ge.add_circle([2371.1463641974933.mm,223.8417569707807.mm,941.6266704547361.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(27.74731004524483.mm, -6.326989302013999.mm, -18.26742835477421.mm)
  circle = ge.add_circle([2398.7447247031705.mm,239.44455418037955.mm,929.8569566219212.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.70609505731909.mm, -21.959734238392485.mm, -22.899352780367735.mm)
  circle = ge.add_circle([2426.4920347484153.mm,233.11756487836556.mm,911.589528267147.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.165461489606514.mm, -22.173951151891544.mm, -22.96282445844156.mm)
  circle = ge.add_circle([2438.1981298057344.mm,211.15783063997307.mm,888.6901754867793.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-27.522128548239834.mm, -6.844647491216364.mm, -18.42080855898223.mm)
  circle = ge.add_circle([2427.032668316128.mm,188.98387948808153.mm,865.7273510283377.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-27.82002131069021.mm, 15.083744005700993.mm, -11.923507374710653.mm)
  circle = ge.add_circle([2399.510539767888.mm,182.13923199686516.mm,847.3065424693555.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.885323546563086.mm, 30.816315811627163.mm, -7.262004617398929.mm)
  circle = ge.add_circle([2371.690518457198.mm,197.22297600256616.mm,835.3830350946448.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(10.984293075197002.mm, 31.17333390682458.mm, -7.1562214780813065.mm)
  circle = ge.add_circle([2359.805194910635.mm,228.03929181419332.mm,828.1210304772459.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(27.444729426305003.mm, 15.946483262156391.mm, -11.66788092835327.mm)
  circle = ge.add_circle([2370.789487985832.mm,259.2126257210179.mm,820.9648089991646.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(27.891552778535242.mm, -5.979583276001961.mm, -18.164493235955774.mm)
  circle = ge.add_circle([2398.234217412137.mm,275.1591089831743.mm,809.2969280708113.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(12.064048000384446.mm, -21.81131476110076.mm, -22.855376638947973.mm)
  circle = ge.add_circle([2426.125770190672.mm,269.17952570717233.mm,791.1324348348555.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.802658836464616.mm, -22.31111889749417.mm, -23.003466753434964.mm)
  circle = ge.add_circle([2438.1898181910565.mm,247.36821094607157.mm,768.2770581959076.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-27.366166422230435.mm, -7.187367012473686.mm, -18.52235508379931.mm)
  circle = ge.add_circle([2427.387159354592.mm,225.0570920485774.mm,745.2735914424726.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-27.961901415258126.mm, 14.735444721459487.mm, -12.026707162633897.mm)
  circle = ge.add_circle([2400.0209929323614.mm,217.86972503610372.mm,726.7512363586733.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-12.24226083939675.mm, 30.665664490169775.mm, -7.306642045979061.mm)
  circle = ge.add_circle([2372.0590915171033.mm,232.6051697575632.mm,714.7245291960394.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(10.620566476192835.mm, 31.30823347195519.mm, -7.116251236560856.mm)
  circle = ge.add_circle([2359.8168306777065.mm,263.270834247733.mm,707.4178871500603.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(27.286442867733967.mm, 16.28822171798845.mm, -11.566625089588456.mm)
  circle = ge.add_circle([2370.4373971538994.mm,294.57906771968817.mm,700.3016359134995.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(28.031064237497958.mm, -5.630405504283942.mm, -18.061033155446694.mm)
  circle = ge.add_circle([2397.7238400216334.mm,310.8672894376766.mm,688.735010823911.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(12.419954505911392.mm, -21.65843798433184.mm, -22.810079816201664.mm)
  circle = ge.add_circle([2425.7549042591313.mm,305.2368839333927.mm,670.6739776684643.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.43802371659558.mm, -22.44374456130248.mm, -23.04276324641512.mm)
  circle = ge.add_circle([2438.1748587650427.mm,283.57844594906084.mm,647.8638978522627.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-27.205562143749376.mm, -7.52810991036074.mm, -18.62331594243267.mm)
  circle = ge.add_circle([2427.736835048447.mm,261.13470138775835.mm,624.8211346058475.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-28.09903831218253.mm, 14.385403270272775.mm, -12.130423148170621.mm)
  circle = ge.add_circle([2400.5312729046977.mm,253.60659147739761.mm,606.1978186634149.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-12.597121464255906.mm, 30.510568741321663.mm, -7.352596341934031.mm)
  circle = ge.add_circle([2372.432234592515.mm,267.9919947476704.mm,594.0673955152442.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(10.255038298986165.mm, 31.43857961002277.mm, -7.077630158615079.mm)
  circle = ge.add_circle([2359.8351131282593.mm,298.50256348899205.mm,586.7147991733102.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(27.12352768028495.mm, 16.6279546076305.mm, -11.465963492657238.mm)
  circle = ge.add_circle([2370.0901514272455.mm,329.9411430990148.mm,579.6371690146951.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(28.165820756652465.mm, -5.279515218263725.mm, -17.95706566329261.mm)
  circle = ge.add_circle([2397.2136791075304.mm,346.5690977066453.mm,568.1712055220379.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(12.773754201094562.mm, -21.501129840739452.mm, -22.76346999587804.mm)
  circle = ge.add_circle([2425.379499864183.mm,341.2895824883816.mm,550.2141398587453.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.071617983450778.mm, -22.571805645881227.mm, -23.080707271475546.mm)
  circle = ge.add_circle([2438.1532540652775.mm,319.78845264764215.mm,527.4506698628672.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-27.04034295627571.mm, -7.866818384290468.mm, -18.72367400878204.mm)
  circle = ge.add_circle([2428.0816360818267.mm,297.2166470017609.mm,504.3699625913917.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-28.231408738782648.mm, 14.033679030051871.mm, -12.234637737865796.mm)
  circle = ge.add_circle([2401.041293125551.mm,289.34982861747045.mm,485.64628858260966.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-12.949845225747595.mm, 30.351054874143074.mm, -7.3998597099867425.mm)
  circle = ge.add_circle([2372.8098843867683.mm,303.3835076475223.mm,473.41165084474386.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.887770548518347.mm, 31.56435021027022.mm, -7.0403647955789666.mm)
  circle = ge.add_circle([2359.8600391610207.mm,333.7345625216654.mm,466.0117911347571.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(26.95601149943741.mm, 16.965624301824164.mm, -11.365913212896317.mm)
  circle = ge.add_circle([2369.747809709539.mm,365.2989127319356.mm,458.97142633917815.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(28.295799477104538.mm, -4.926971939840996.mm, -17.85260839561164.mm)
  circle = ge.add_circle([2396.7038212089765.mm,382.2645370337598.mm,447.60551312628183.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(13.125387070507713.mm, -21.339417014674154.mm, -22.71555508445124.mm)
  circle = ge.add_circle([2424.999620686081.mm,377.3375650939188.mm,429.7529047306702.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.703503790831292.mm, -22.695280428089973.mm, -23.117292392130025.mm)
  circle = ge.add_circle([2438.1250077565887.mm,355.99814807924463.mm,407.03734964621896.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-26.870536886118316.mm, -8.203434978777295.mm, -18.823412259000406.mm)
  circle = ge.add_circle([2428.4215039657574.mm,333.30286765115466.mm,383.92005725408893.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-28.35899024092032.mm, 13.68033166416052.mm, -12.339333253685425.mm)
  circle = ge.add_circle([2401.550967079639.mm,325.09943267237736.mm,365.0966449950885.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-13.300372290957512.mm, 30.18714994714429.mm, -7.448424132801335.mm)
  circle = ge.add_circle([2373.191976838719.mm,338.7797643365379.mm,352.7573117414031.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.518825524814929.mm, 31.68552393809432.mm, -7.004461468816146.mm)
  circle = ge.add_circle([2359.8916045477613.mm,368.9669142836822.mm,345.30888760860176.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(29.58956992742378.mm, -24.652438221776492.mm, -7.304426139785619.mm)
  circle = ge.add_circle([2369.410430072576.mm,400.6524382217765.mm,338.3044261397856.mm], vec, 7.mm, 8)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 24.mm, -81.mm)
  circle = ge.add_circle([2399.mm,376.mm,331.mm], vec, 7.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 24.mm, 105.mm)
  circle = ge.add_circle([2399.mm,400.mm,250.mm], vec, 7.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-27.603081244248187.mm, 30.62474162209861.mm, 9.070708408455346.mm)
  circle = ge.add_circle([2399.mm,424.mm,355.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.59556304131911.mm, -23.325104356190707.mm, 21.40210177492156.mm)
  circle = ge.add_circle([2371.396918755752.mm,454.6247416220986.mm,364.07070840845535.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.136428593205892.mm, -23.509413300862036.mm, 21.44422953370355.mm)
  circle = ge.add_circle([2359.8013557144327.mm,431.2996372659079.mm,385.4728101833769.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(27.410207036096836.mm, -8.035754631454324.mm, 17.907393266410338.mm)
  circle = ge.add_circle([2370.9377843076386.mm,407.79022396504587.mm,406.91703971708046.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(27.788318462906773.mm, 14.122421527943004.mm, 12.842667287119468.mm)
  circle = ge.add_circle([2398.3479913437354.mm,399.75446933359154.mm,424.8244329834908.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(12.051489326099272.mm, 30.11519436317508.mm, 9.187176353352186.mm)
  circle = ge.add_circle([2426.136309806642.mm,413.87689086153455.mm,437.66710027061026.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.674213011236588.mm, 30.66807020413279.mm, 9.060804732561849.mm)
  circle = ge.add_circle([2438.1877991327415.mm,443.9920852247096.mm,446.85427662396245.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-27.209749201273098.mm, 15.460426508362389.mm, 12.536837577309427.mm)
  circle = ge.add_circle([2427.513586121505.mm,474.6601554288424.mm,455.9150813565243.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-27.965867442188937.mm, -6.6885534188509155.mm, 17.599461560672466.mm)
  circle = ge.add_circle([2400.303836920232.mm,490.1205819372048.mm,468.4519189338337.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-12.504081305678937.mm, -22.934281822107266.mm, 21.312770909988103.mm)
  circle = ge.add_circle([2372.337969478043.mm,483.4320285183539.mm,486.0513804945062.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(10.209044177350279.mm, -23.85557159429095.mm, 21.52335142934436.mm)
  circle = ge.add_circle([2359.833888172364.mm,460.4977466962466.mm,507.3641514044943.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(27.001763200773894.mm, -8.918150395734585.mm, 18.10908372681729.mm)
  circle = ge.add_circle([2370.042932349714.mm,436.6421751019557.mm,528.8875028338387.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(28.13567905932905.mm, 13.215505304905605.mm, 13.049962423813781.mm)
  circle = ge.add_circle([2397.044695550488.mm,427.7240247062211.mm,546.9965865606559.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(12.953213760695235.mm, 29.709694544020806.mm, 9.279862026301657.mm)
  circle = ge.add_circle([2425.180374609817.mm,440.9395300111267.mm,560.0465489844697.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.741050790565168.mm, 30.999143352687327.mm, 8.985130870035164.mm)
  circle = ge.add_circle([2438.1335883705124.mm,470.6492245551475.mm,569.3264110107714.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-26.78630657842541.mm, 16.33607741202269.mm, 12.336688799329977.mm)
  circle = ge.add_circle([2428.392537579947.mm,501.6483679078348.mm,578.3115418808065.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-28.297706332269172.mm, -5.776130307433959.mm, 17.390907706634152.mm)
  circle = ge.add_circle([2401.606231001522.mm,517.9844453198575.mm,590.6482306801365.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-13.398762428942064.mm, -22.514216908178355.mm, 21.21675607251882.mm)
  circle = ge.add_circle([2373.3085246692526.mm,512.2083150124236.mm,608.0391383867707.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.270362331376418.mm, -24.171467999423328.mm, 21.595556321945992.mm)
  circle = ge.add_circle([2359.9097622403106.mm,489.6940981042452.mm,629.2558944592895.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(26.56343894496149.mm, -9.7868141710116.mm, 18.30763544688068.mm)
  circle = ge.add_circle([2369.180124571687.mm,465.52263010482187.mm,650.8514507812355.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(28.451904432661195.mm, 12.297827746698772.mm, 13.259717294261009.mm)
  circle = ge.add_circle([2395.7435635166485.mm,455.7358159338103.mm,669.1590862281162.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(13.84060403974081.mm, 29.275180755362214.mm, 9.37917946370942.mm)
  circle = ge.add_circle([2424.1954679493097.mm,468.03364368050904.mm,682.4188035223772.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.797109025925693.mm, 31.299775614824.mm, 8.916414924403853.mm)
  circle = ge.add_circle([2438.0360719890505.mm,497.30882443587126.mm,691.7979829860866.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-26.333221961534946.mm, 17.19751372429323.mm, 12.13978907081082.mm)
  circle = ge.add_circle([2429.238962963125.mm,528.6086000506953.mm,700.7143979104904.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-28.59823069826416.mm, -4.853452197783554.mm, 17.180009852999888.mm)
  circle = ge.add_circle([2402.90574100159.mm,545.8061137749885.mm,712.8541869813013.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-14.278616348054129.mm, -22.065374462428167.mm, 21.114163513490098.mm)
  circle = ge.add_circle([2374.3075103033257.mm,540.9526615772049.mm,730.0341968343012.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.321421809978347.mm, -24.456752942146238.mm, 21.660764308854255.mm)
  circle = ge.add_circle([2360.0288939552715.mm,518.8872871147768.mm,751.1483603477913.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(26.095719322652712.mm, -10.640784685286803.mm, 18.502828707286312.mm)
  circle = ge.add_circle([2368.35031576525.mm,494.43053417263053.mm,772.8091246566455.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(28.736644644752232.mm, 11.370404364461876.mm, 13.471699781629354.mm)
  circle = ge.add_circle([2394.4460350879026.mm,483.7897494873437.mm,791.3119533639318.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(14.712678168301409.mm, 28.81213383449176.mm, 9.485018759908485.mm)
  circle = ge.add_circle([2423.182679732655.mm,495.1601538518056.mm,804.7836531455612.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-7.8434322926905224.mm, 31.569634307882893.mm, 8.854732937419044.mm)
  circle = ge.add_circle([2437.8953579009562.mm,523.9722876862974.mm,814.2686719054697.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-25.85099673855848.mm, 18.043782171158682.mm, 11.94635628295589.mm)
  circle = ge.add_circle([2430.0519256082657.mm,555.5419219941803.mm,823.1234048428887.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-28.867107976912393.mm, -3.9215401346993985.mm, 16.967001381437854.mm)
  circle = ge.add_circle([2404.2009288697072.mm,573.5857041653389.mm,835.0697611258446.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-15.142669407891844.mm, -21.588251178384212.mm, 21.00510676285137.mm)
  circle = ge.add_circle([2375.333820892795.mm,569.6641640306395.mm,852.0367625072824.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(7.363272720202531.mm, -24.71111072329643.mm, 21.71890323025991.mm)
  circle = ge.add_circle([2360.191151484903.mm,548.0759128522553.mm,873.0418692701338.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(25.59912191704734.mm, -11.479116926271331.mm, 18.694447505225753.mm)
  circle = ge.add_circle([2367.5544242051055.mm,523.3648021289589.mm,894.7607725003937.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(28.989584599242335.mm, 10.434261454160492.mm, 13.685675303984112.mm)
  circle = ge.add_circle([2393.153546122153.mm,511.88568520268757.mm,913.4552200056195.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(15.568471100447823.mm, 28.32106619375088.mm, 9.597262792077572.mm)
  circle = ge.add_circle([2422.143130721395.mm,522.3199466568481.mm,927.1408953096036.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-6.881075939045331.mm, 31.80842080354239.mm, 8.800153166982568.mm)
  circle = ge.add_circle([2437.711601821843.mm,550.6410128505989.mm,936.7381581016812.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-25.34016454473749.mm, 18.873946263514313.mm, 11.756604490417544.mm)
  circle = ge.add_circle([2430.8305258827977.mm,582.4494336541413.mm,945.5383112686637.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-29.10404062593534.mm, -2.9814253813661935.mm, 16.752118009247397.mm)
  circle = ge.add_circle([2405.49036133806.mm,601.3233799176556.mm,957.2949157590813.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-15.989965438720446.mm, -21.083375045431012.mm, 20.889706503890693.mm)
  circle = ge.add_circle([2376.386320712125.mm,598.3419545362894.mm,974.0470337683287.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(6.396975359388762.mm, -24.934259868016397.mm, 21.769908749053116.mm)
  circle = ge.add_circle([2360.3963552734044.mm,577.2585794908584.mm,994.9367402722194.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(25.0741962677871.mm, -12.300883187145018.mm, 18.882279793425255.mm)
  circle = ge.add_circle([2366.793330632793.mm,552.324319622842.mm,1016.7066490212725.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(29.21044439025536.mm, 9.490434960876769.mm, 13.901407073877635.mm)
  circle = ge.add_circle([2391.8675269005803.mm,540.023436435697.mm,1035.5889288146977.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.40703580718491.mm, 27.80252125348875.mm, 9.71578734985178.mm)
  circle = ge.add_circle([2421.0779712908356.mm,549.5138713965738.mm,1049.4903358885754.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.911104918129695.mm, 32.01587085828464.mm, 8.752736011612797.mm)
  circle = ge.add_circle([2437.4850070980206.mm,577.3163926500625.mm,1059.2061232384272.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-24.80129067207281.mm, 19.68708733349513.mm, 11.57074367442192.mm)
  circle = ge.add_circle([2431.573902179891.mm,609.3322635083472.mm,1067.95885925004.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-29.308766453299995.mm, -2.034148278146631.mm, 16.535597528511744.mm)
  circle = ge.add_circle([2406.772611507818.mm,629.0193508418423.mm,1079.5296029244619.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-16.819566814302107.mm, -20.55130476453428.mm, 20.768090439685466.mm)
  circle = ge.add_circle([2377.463845054518.mm,626.9852025636957.mm,1096.0652004529736.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.423599041835132.mm, -25.125953437236262.mm, 21.813724422017913.mm)
  circle = ge.add_circle([2360.644278240216.mm,606.4338977991614.mm,1116.833290892659.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(24.521523262832034.mm, -13.105174093167193.mm, 19.06611771480152.mm)
  circle = ge.add_circle([2366.067877282051.mm,581.3079443619251.mm,1138.647015314677.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(29.398979612143194.mm, 8.539969332422402.mm, 14.118656360381692.mm)
  circle = ge.add_circle([2390.589400544883.mm,568.202770268758.mm,1157.7131330294785.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(17.227444324444605.mm, 27.257072840709156.mm, 9.840461272772927.mm)
  circle = ge.add_circle([2419.9883801570263.mm,576.7427396011803.mm,1171.8317893898602.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.934592609550691.mm, 32.19175490581006.mm, 8.712533943607013.mm)
  circle = ge.add_circle([2437.215824481471.mm,603.9998124418895.mm,1181.6722506626331.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-33.28123187192023.mm, -20.19156734769956.mm, 4.615215393759854.mm)
  circle = ge.add_circle([2432.28123187192.mm,636.1915673476996.mm,1190.3847846062401.mm], vec, 7.mm, 8)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (elbow -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (elbow -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 24.mm, 105.mm)
  circle = ge.add_circle([2399.mm,616.mm,1195.mm], vec, 7.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # TAP-01 Branch (3/4in)
  grp = ents.add_group
  grp.name = "TAP-01 Branch (3/4in)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1227.mm)
  circle = ge.add_circle([1130.mm,69.mm,48.mm], vec, 12.5.mm, 16)
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
  arc = ge.add_arc([1130.mm,94.mm,1275.mm], [0.000000,-1.000000,0.000000], [-1.000000,0.000000,0.000000], 25.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1130.mm,69.mm,1275.mm], [0.000000,0.000000,1.000000], 12.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # TAP-01 Branch (3/4in)
  grp = ents.add_group
  grp.name = "TAP-01 Branch (3/4in)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 50.mm, 0.mm)
  circle = ge.add_circle([1130.mm,94.mm,1300.mm], vec, 12.5.mm, 16)
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
  arc = ge.add_arc([1130.mm,144.mm,1275.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 25.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1130.mm,144.mm,1300.mm], [0.000000,1.000000,0.000000], 12.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 blue recycle -> X1 cross"] || model.materials.add("DV-01 blue recycle -> X1 cross")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # TAP-01 Branch (3/4in)
  grp = ents.add_group
  grp.name = "TAP-01 Branch (3/4in)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -125.mm)
  circle = ge.add_circle([1130.mm,169.mm,1275.mm], vec, 12.5.mm, 16)
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
  mat.color = Sketchup::Color.new(128, 128, 138)
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

  # ═══ Walkway Cantilever Arms ═══
  defn = model.definitions.add("Walkway Cantilever Arms")
  ents = defn.entities
  # RWk center cantilever Yd1046 lower
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 lower"
  face = grp.entities.add_face([4329.mm,1046.mm,93.mm], [4654.mm,1046.mm,93.mm], [4654.mm,1096.8.mm,93.mm], [4329.mm,1096.8.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1046 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 upper"
  face = grp.entities.add_face([4379.8.mm,1046.mm,95.mm], [4578.2.mm,1046.mm,95.mm], [4578.2.mm,1096.8.mm,95.mm], [4379.8.mm,1096.8.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1046 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 upper"
  face = grp.entities.add_face([4629.mm,1046.mm,95.mm], [4654.mm,1046.mm,95.mm], [4654.mm,1096.8.mm,95.mm], [4629.mm,1096.8.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1046 Y1038
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1046 Y1038"
  face = grp.entities.add_face([4650.mm,1038.mm,68.mm], [4708.mm,1038.mm,68.mm], [4708.mm,1046.mm,68.mm], [4650.mm,1046.mm,68.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(77.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1046 Y1096
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1046 Y1096"
  face = grp.entities.add_face([4650.mm,1096.8.mm,68.mm], [4708.mm,1096.8.mm,68.mm], [4708.mm,1104.8.mm,68.mm], [4650.mm,1104.8.mm,68.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(77.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1046 Z99
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1046 Z99"
  ge = grp.entities
  circle = ge.add_circle([4679.mm,1034.mm,99.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(74.8.mm)
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
  cface.pushpull(74.8.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1266 lower
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 lower"
  face = grp.entities.add_face([4329.mm,1266.mm,93.mm], [4654.mm,1266.mm,93.mm], [4654.mm,1316.8.mm,93.mm], [4329.mm,1316.8.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1266 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 upper"
  face = grp.entities.add_face([4379.8.mm,1266.mm,95.mm], [4578.2.mm,1266.mm,95.mm], [4578.2.mm,1316.8.mm,95.mm], [4379.8.mm,1316.8.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1266 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 upper"
  face = grp.entities.add_face([4629.mm,1266.mm,95.mm], [4654.mm,1266.mm,95.mm], [4654.mm,1316.8.mm,95.mm], [4629.mm,1316.8.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1266 Y1258
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1266 Y1258"
  face = grp.entities.add_face([4650.mm,1258.mm,68.mm], [4708.mm,1258.mm,68.mm], [4708.mm,1266.mm,68.mm], [4650.mm,1266.mm,68.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(77.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1266 Y1316
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1266 Y1316"
  face = grp.entities.add_face([4650.mm,1316.8.mm,68.mm], [4708.mm,1316.8.mm,68.mm], [4708.mm,1324.8.mm,68.mm], [4650.mm,1324.8.mm,68.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(77.mm)
  mat = model.materials["Frame upright"] || model.materials.add("Frame upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1266 Z99
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1266 Z99"
  ge = grp.entities
  circle = ge.add_circle([4679.mm,1254.mm,99.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(74.8.mm)
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
  cface.pushpull(74.8.mm)
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
