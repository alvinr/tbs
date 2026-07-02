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

  # ═══ IBC Frame ═══
  defn = model.definitions.add("IBC Frame")
  ents = defn.entities
  # Front Portal Upright
  grp = ents.add_group
  grp.name = "Front Portal Upright"
  face = grp.entities.add_face([4734.mm,1046.mm,0.mm], [4784.mm,1046.mm,0.mm], [4784.mm,1096.mm,0.mm], [4734.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Portal Upright
  grp = ents.add_group
  grp.name = "Front Portal Upright"
  face = grp.entities.add_face([4734.mm,1266.mm,0.mm], [4784.mm,1266.mm,0.mm], [4784.mm,1316.mm,0.mm], [4734.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Portal Top Tie
  grp = ents.add_group
  grp.name = "Front Portal Top Tie"
  face = grp.entities.add_face([4734.mm,1046.mm,2246.mm], [4784.mm,1046.mm,2246.mm], [4784.mm,1316.mm,2246.mm], [4734.mm,1316.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Portal Floor Beam
  grp = ents.add_group
  grp.name = "Front Portal Floor Beam"
  face = grp.entities.add_face([4734.mm,1046.mm,0.mm], [4784.mm,1046.mm,0.mm], [4784.mm,1316.mm,0.mm], [4734.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Panel Mount Rail
  grp = ents.add_group
  grp.name = "Panel Mount Rail"
  face = grp.entities.add_face([4734.mm,1046.mm,2260.mm], [4892.mm,1046.mm,2260.mm], [4892.mm,1316.mm,2260.mm], [4734.mm,1316.mm,2260.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Flange Plate
  grp = ents.add_group
  grp.name = "Foot Flange Plate"
  face = grp.entities.add_face([4684.mm,996.mm,0.mm], [4834.mm,996.mm,0.mm], [4834.mm,1146.mm,0.mm], [4684.mm,1146.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4709.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4709.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4809.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4809.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Flange Plate
  grp = ents.add_group
  grp.name = "Foot Flange Plate"
  face = grp.entities.add_face([4684.mm,1216.mm,0.mm], [4834.mm,1216.mm,0.mm], [4834.mm,1366.mm,0.mm], [4684.mm,1366.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4709.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4709.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4809.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4809.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,0.mm,560.mm], [4674.mm,0.mm,560.mm], [4674.mm,1096.mm,560.mm], [4654.mm,1096.mm,560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,0.mm,1760.mm], [4674.mm,0.mm,1760.mm], [4674.mm,1096.mm,1760.mm], [4654.mm,1096.mm,1760.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,1266.mm,560.mm], [4674.mm,1266.mm,560.mm], [4674.mm,2362.mm,560.mm], [4654.mm,2362.mm,560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,1266.mm,1760.mm], [4674.mm,1266.mm,1760.mm], [4674.mm,2362.mm,1760.mm], [4654.mm,2362.mm,1760.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Bar Stub
  grp = ents.add_group
  grp.name = "Front Bar Stub"
  face = grp.entities.add_face([4654.mm,1046.mm,560.mm], [4784.mm,1046.mm,560.mm], [4784.mm,1096.mm,560.mm], [4654.mm,1096.mm,560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Bar Stub
  grp = ents.add_group
  grp.name = "Front Bar Stub"
  face = grp.entities.add_face([4654.mm,1046.mm,1760.mm], [4784.mm,1046.mm,1760.mm], [4784.mm,1096.mm,1760.mm], [4654.mm,1096.mm,1760.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Bar Stub
  grp = ents.add_group
  grp.name = "Front Bar Stub"
  face = grp.entities.add_face([4654.mm,1266.mm,560.mm], [4784.mm,1266.mm,560.mm], [4784.mm,1316.mm,560.mm], [4654.mm,1316.mm,560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Bar Stub
  grp = ents.add_group
  grp.name = "Front Bar Stub"
  face = grp.entities.add_face([4654.mm,1266.mm,1760.mm], [4784.mm,1266.mm,1760.mm], [4784.mm,1316.mm,1760.mm], [4654.mm,1316.mm,1760.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
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
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
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
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
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
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
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
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4646.mm,0.mm,530.mm], [4712.mm,0.mm,530.mm], [4712.mm,4.mm,530.mm], [4646.mm,4.mm,530.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,0.mm,556.mm], [4708.mm,0.mm,556.mm], [4708.mm,70.mm,556.mm], [4650.mm,70.mm,556.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.mm,-48.mm,517.5.mm], [4729.mm,-48.mm,517.5.mm], [4729.mm,-40.mm,517.5.mm], [4629.mm,-40.mm,517.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4646.mm,0.mm,1730.mm], [4712.mm,0.mm,1730.mm], [4712.mm,4.mm,1730.mm], [4646.mm,4.mm,1730.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,0.mm,1756.mm], [4708.mm,0.mm,1756.mm], [4708.mm,70.mm,1756.mm], [4650.mm,70.mm,1756.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.mm,-48.mm,1717.5.mm], [4729.mm,-48.mm,1717.5.mm], [4729.mm,-40.mm,1717.5.mm], [4629.mm,-40.mm,1717.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4646.mm,2358.mm,530.mm], [4712.mm,2358.mm,530.mm], [4712.mm,2362.mm,530.mm], [4646.mm,2362.mm,530.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,2292.mm,556.mm], [4708.mm,2292.mm,556.mm], [4708.mm,2362.mm,556.mm], [4650.mm,2362.mm,556.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.mm,2402.mm,517.5.mm], [4729.mm,2402.mm,517.5.mm], [4729.mm,2410.mm,517.5.mm], [4629.mm,2410.mm,517.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4646.mm,2358.mm,1730.mm], [4712.mm,2358.mm,1730.mm], [4712.mm,2362.mm,1730.mm], [4646.mm,2362.mm,1730.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,2292.mm,1756.mm], [4708.mm,2292.mm,1756.mm], [4708.mm,2362.mm,1756.mm], [4650.mm,2362.mm,1756.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.mm,2402.mm,1717.5.mm], [4729.mm,2402.mm,1717.5.mm], [4729.mm,2410.mm,1717.5.mm], [4629.mm,2410.mm,1717.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
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
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "IBC Frame"
  inst.layer = model.layers["IBC Frame"]

  # ═══ Plumbing Panel ═══
  defn = model.definitions.add("Plumbing Panel")
  ents = defn.entities
  # Plumbing Panel (ply)
  grp = ents.add_group
  grp.name = "Plumbing Panel (ply)"
  face = grp.entities.add_face([4874.mm,1046.mm,250.mm], [4892.mm,1046.mm,250.mm], [4892.mm,1316.mm,250.mm], [4874.mm,1316.mm,250.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2060.mm)
  mat = model.materials["Plumbing Panel (ply)"] || model.materials.add("Plumbing Panel (ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-01 (Blue)
  grp = ents.add_group
  grp.name = "Pump P-01 (Blue)"
  face = grp.entities.add_face([4760.mm,1045.5.mm,1370.mm], [4874.mm,1045.5.mm,1370.mm], [4874.mm,1172.5.mm,1370.mm], [4760.mm,1172.5.mm,1370.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-02 (Brown)
  grp = ents.add_group
  grp.name = "Pump P-02 (Brown)"
  face = grp.entities.add_face([4760.mm,1189.5.mm,1370.mm], [4874.mm,1189.5.mm,1370.mm], [4874.mm,1316.5.mm,1370.mm], [4760.mm,1316.5.mm,1370.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-04 (Tray drain)
  grp = ents.add_group
  grp.name = "Pump P-04 (Tray drain)"
  face = grp.entities.add_face([4760.mm,1045.5.mm,1628.mm], [4874.mm,1045.5.mm,1628.mm], [4874.mm,1172.5.mm,1628.mm], [4760.mm,1172.5.mm,1628.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-03 (Waste evac)
  grp = ents.add_group
  grp.name = "Pump P-03 (Waste evac)"
  face = grp.entities.add_face([4760.mm,1189.5.mm,1628.mm], [4874.mm,1189.5.mm,1628.mm], [4874.mm,1316.5.mm,1628.mm], [4760.mm,1316.5.mm,1628.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-05 (Brown drain)
  grp = ents.add_group
  grp.name = "Pump P-05 (Brown drain)"
  face = grp.entities.add_face([4760.mm,1189.5.mm,1996.mm], [4874.mm,1189.5.mm,1996.mm], [4874.mm,1316.5.mm,1996.mm], [4760.mm,1316.5.mm,1996.mm])
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
  circle = ge.add_circle([4811.mm,1109.mm,1996.mm], [0,0,1], 63.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(200.mm)
  mat = model.materials["ACC-01 Accumulator"] || model.materials.add("ACC-01 Accumulator")
  mat.color = Sketchup::Color.new(90, 154, 204)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F1 (50µ)
  grp = ents.add_group
  grp.name = "Filter F1 (50µ)"
  ge = grp.entities
  circle = ge.add_circle([4782.mm,1181.mm,250.mm], [0,0,1], 92.mm, 24)
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
  circle = ge.add_circle([4782.mm,1181.mm,620.mm], [0,0,1], 92.mm, 24)
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
  circle = ge.add_circle([4782.mm,1181.mm,990.mm], [0,0,1], 92.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(340.mm)
  mat = model.materials["Filter F1 (50µ)"] || model.materials.add("Filter F1 (50µ)")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 drop (filtered line -> tap)
  grp = ents.add_group
  grp.name = "SV-01 drop (filtered line -> tap)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -80.mm)
  circle = ge.add_circle([4831.mm,1291.mm,1330.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 (50µ)"] || model.materials.add("Filter F1 (50µ)")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 pH sample tap
  grp = ents.add_group
  grp.name = "SV-01 pH sample tap"
  face = grp.entities.add_face([4814.mm,1275.mm,1220.mm], [4848.mm,1275.mm,1220.mm], [4848.mm,1307.mm,1220.mm], [4814.mm,1307.mm,1220.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(34.mm)
  mat = model.materials["SV-01 pH sample tap"] || model.materials.add("SV-01 pH sample tap")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 spout
  grp = ents.add_group
  grp.name = "SV-01 spout"
  ge = grp.entities
  circle = ge.add_circle([4831.mm,1291.mm,1180.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["SV-01 pH sample tap"] || model.materials.add("SV-01 pH sample tap")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Drain-riser spine (ply)
  grp = ents.add_group
  grp.name = "Drain-riser spine (ply)"
  face = grp.entities.add_face([4874.mm,1223.mm,250.mm], [5420.mm,1223.mm,250.mm], [5420.mm,1241.mm,250.mm], [4874.mm,1241.mm,250.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2060.mm)
  mat = model.materials["Plumbing Panel (ply)"] || model.materials.add("Plumbing Panel (ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Drain-riser spine flange (ply)
  grp = ents.add_group
  grp.name = "Drain-riser spine flange (ply)"
  face = grp.entities.add_face([5402.mm,1226.mm,250.mm], [5420.mm,1226.mm,250.mm], [5420.mm,1280.mm,250.mm], [5402.mm,1280.mm,250.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2060.mm)
  mat = model.materials["Plumbing Panel (ply)"] || model.materials.add("Plumbing Panel (ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Riser pipe clamp
  grp = ents.add_group
  grp.name = "Riser pipe clamp"
  face = grp.entities.add_face([5324.mm,1241.mm,500.mm], [5356.mm,1241.mm,500.mm], [5356.mm,1271.mm,500.mm], [5324.mm,1271.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Riser pipe clamp
  grp = ents.add_group
  grp.name = "Riser pipe clamp"
  face = grp.entities.add_face([5324.mm,1241.mm,900.mm], [5356.mm,1241.mm,900.mm], [5356.mm,1271.mm,900.mm], [5324.mm,1271.mm,900.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Riser pipe clamp
  grp = ents.add_group
  grp.name = "Riser pipe clamp"
  face = grp.entities.add_face([5324.mm,1241.mm,1300.mm], [5356.mm,1241.mm,1300.mm], [5356.mm,1271.mm,1300.mm], [5324.mm,1271.mm,1300.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Riser pipe clamp
  grp = ents.add_group
  grp.name = "Riser pipe clamp"
  face = grp.entities.add_face([5384.mm,1241.mm,500.mm], [5416.mm,1241.mm,500.mm], [5416.mm,1271.mm,500.mm], [5384.mm,1271.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Riser pipe clamp
  grp = ents.add_group
  grp.name = "Riser pipe clamp"
  face = grp.entities.add_face([5384.mm,1241.mm,900.mm], [5416.mm,1241.mm,900.mm], [5416.mm,1271.mm,900.mm], [5384.mm,1271.mm,900.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Riser pipe clamp
  grp = ents.add_group
  grp.name = "Riser pipe clamp"
  face = grp.entities.add_face([5384.mm,1241.mm,1300.mm], [5416.mm,1241.mm,1300.mm], [5416.mm,1271.mm,1300.mm], [5384.mm,1271.mm,1300.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Riser pipe clamp
  grp = ents.add_group
  grp.name = "Riser pipe clamp"
  face = grp.entities.add_face([5384.mm,1241.mm,1700.mm], [5416.mm,1241.mm,1700.mm], [5416.mm,1271.mm,1700.mm], [5384.mm,1271.mm,1700.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Plumbing Panel"
  inst.layer = model.layers["Plumbing & Panel"]

  # ═══ Water Plumbing ═══
  defn = model.definitions.add("Water Plumbing")
  ents = defn.entities
  # X1 Blue Fill Trunk
  grp = ents.add_group
  grp.name = "X1 Blue Fill Trunk"
  ge = grp.entities
  vec = Geom::Vector3d.new(-240.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5893.mm,1181.mm,2250.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue Fill Tee
  grp = ents.add_group
  grp.name = "Blue Fill Tee"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 45.59999999999991.mm, 0.mm)
  circle = ge.add_circle([5653.mm,1158.2.mm,2250.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue Fill Tee
  grp = ents.add_group
  grp.name = "Blue Fill Tee"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -22.800000000000182.mm)
  circle = ge.add_circle([5653.mm,1181.mm,2250.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill → Blue #1 side
  grp = ents.add_group
  grp.name = "Fill → Blue #1 side"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -70.mm)
  circle = ge.add_circle([5653.mm,1181.mm,2250.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill → Blue #1 side elbow
  grp = ents.add_group
  grp.name = "Fill → Blue #1 side elbow"
  ge = grp.entities
  arc = ge.add_arc([5653.mm,1157.mm,2180.mm], [0.000000,1.000000,0.000000], [-1.000000,-0.000000,-0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5653.mm,1181.mm,2180.mm], [0.000000,0.000000,-1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill → Blue #1 side
  grp = ents.add_group
  grp.name = "Fill → Blue #1 side"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -261.mm, 0.mm)
  circle = ge.add_circle([5653.mm,1157.mm,2156.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill → Blue #2 side
  grp = ents.add_group
  grp.name = "Fill → Blue #2 side"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 285.mm, 0.mm)
  circle = ge.add_circle([5653.mm,1181.mm,2156.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill Flange Blue #1
  grp = ents.add_group
  grp.name = "Fill Flange Blue #1"
  ge = grp.entities
  circle = ge.add_circle([5653.mm,1038.mm,2156.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(16.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fill Flange Blue #2
  grp = ents.add_group
  grp.name = "Fill Flange Blue #2"
  ge = grp.entities
  circle = ge.add_circle([5653.mm,1308.mm,2156.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(16.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 → X3 (Brown drain-out)
  grp = ents.add_group
  grp.name = "P-05 → X3 (Brown drain-out)"
  ge = grp.entities
  vec = Geom::Vector3d.new(522.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4854.mm,1253.mm,1996.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-05 → X3 (Brown drain-out)"] || model.materials.add("P-05 → X3 (Brown drain-out)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 → X3 (Brown drain-out) elbow
  grp = ents.add_group
  grp.name = "P-05 → X3 (Brown drain-out) elbow"
  ge = grp.entities
  arc = ge.add_arc([5376.mm,1253.mm,1972.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5376.mm,1253.mm,1996.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-05 → X3 (Brown drain-out)"] || model.materials.add("P-05 → X3 (Brown drain-out)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 → X3 (Brown drain-out)
  grp = ents.add_group
  grp.name = "P-05 → X3 (Brown drain-out)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1548.mm)
  circle = ge.add_circle([5400.mm,1253.mm,1972.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-05 → X3 (Brown drain-out)"] || model.materials.add("P-05 → X3 (Brown drain-out)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 → X3 (Brown drain-out) elbow
  grp = ents.add_group
  grp.name = "P-05 → X3 (Brown drain-out) elbow"
  ge = grp.entities
  arc = ge.add_arc([5400.mm,1229.mm,424.mm], [0.000000,1.000000,0.000000], [-1.000000,-0.000000,-0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5400.mm,1253.mm,424.mm], [0.000000,0.000000,-1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-05 → X3 (Brown drain-out)"] || model.materials.add("P-05 → X3 (Brown drain-out)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 → X3 (Brown drain-out)
  grp = ents.add_group
  grp.name = "P-05 → X3 (Brown drain-out)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -24.480000000000018.mm, 0.mm)
  circle = ge.add_circle([5400.mm,1229.mm,400.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-05 → X3 (Brown drain-out)"] || model.materials.add("P-05 → X3 (Brown drain-out)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 → X3 (Brown drain-out) elbow
  grp = ents.add_group
  grp.name = "P-05 → X3 (Brown drain-out) elbow"
  ge = grp.entities
  arc = ge.add_arc([5423.52.mm,1204.52.mm,400.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.000000,1.000000], 23.520000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5400.mm,1204.52.mm,400.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-05 → X3 (Brown drain-out)"] || model.materials.add("P-05 → X3 (Brown drain-out)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 → X3 (Brown drain-out)
  grp = ents.add_group
  grp.name = "P-05 → X3 (Brown drain-out)"
  ge = grp.entities
  vec = Geom::Vector3d.new(469.47999999999956.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5423.52.mm,1181.mm,400.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-05 → X3 (Brown drain-out)"] || model.materials.add("P-05 → X3 (Brown drain-out)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 → X4 (Waste drain-out)
  grp = ents.add_group
  grp.name = "P-03 → X4 (Waste drain-out)"
  ge = grp.entities
  vec = Geom::Vector3d.new(462.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4854.mm,1253.mm,1628.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 → X4 (Waste drain-out) elbow
  grp = ents.add_group
  grp.name = "P-03 → X4 (Waste drain-out) elbow"
  ge = grp.entities
  arc = ge.add_arc([5316.mm,1253.mm,1604.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5316.mm,1253.mm,1628.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 → X4 (Waste drain-out)
  grp = ents.add_group
  grp.name = "P-03 → X4 (Waste drain-out)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1380.mm)
  circle = ge.add_circle([5340.mm,1253.mm,1604.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 → X4 (Waste drain-out) elbow
  grp = ents.add_group
  grp.name = "P-03 → X4 (Waste drain-out) elbow"
  ge = grp.entities
  arc = ge.add_arc([5340.mm,1229.mm,224.mm], [0.000000,1.000000,0.000000], [-1.000000,-0.000000,-0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5340.mm,1253.mm,224.mm], [0.000000,0.000000,-1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 → X4 (Waste drain-out)
  grp = ents.add_group
  grp.name = "P-03 → X4 (Waste drain-out)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -24.480000000000018.mm, 0.mm)
  circle = ge.add_circle([5340.mm,1229.mm,200.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 → X4 (Waste drain-out) elbow
  grp = ents.add_group
  grp.name = "P-03 → X4 (Waste drain-out) elbow"
  ge = grp.entities
  arc = ge.add_arc([5363.52.mm,1204.52.mm,200.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.000000,1.000000], 23.520000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5340.mm,1204.52.mm,200.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-03 → X4 (Waste drain-out)
  grp = ents.add_group
  grp.name = "P-03 → X4 (Waste drain-out)"
  ge = grp.entities
  vec = Geom::Vector3d.new(529.4799999999996.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5363.52.mm,1181.mm,200.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Blue Manifold Tee
  grp = ents.add_group
  grp.name = "Blue Manifold Tee"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 45.59999999999991.mm, 0.mm)
  circle = ge.add_circle([4814.mm,1158.2.mm,1353.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue Manifold Tee
  grp = ents.add_group
  grp.name = "Blue Manifold Tee"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.800000000000182.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4814.mm,1181.mm,1353.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 → manifold
  grp = ents.add_group
  grp.name = "Blue #1 → manifold"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 285.mm, 0.mm)
  circle = ge.add_circle([4814.mm,896.mm,1353.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #2 → manifold
  grp = ents.add_group
  grp.name = "Blue #2 → manifold"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -285.mm, 0.mm)
  circle = ge.add_circle([4814.mm,1466.mm,1353.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Manifold → P-01
  grp = ents.add_group
  grp.name = "Manifold → P-01"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -63.67000000000007.mm, 0.mm)
  circle = ge.add_circle([4814.mm,1181.mm,1353.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Manifold → P-01 elbow
  grp = ents.add_group
  grp.name = "Manifold → P-01 elbow"
  ge = grp.entities
  arc = ge.add_arc([4814.mm,1117.33.mm,1361.33.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 8.330000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4814.mm,1117.33.mm,1353.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Manifold → P-01
  grp = ents.add_group
  grp.name = "Manifold → P-01"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 8.670000000000073.mm)
  circle = ge.add_circle([4814.mm,1109.mm,1361.33.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 Suction Flange
  grp = ents.add_group
  grp.name = "Blue #1 Suction Flange"
  ge = grp.entities
  circle = ge.add_circle([4814.mm,1037.mm,1353.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #2 Suction Flange
  grp = ents.add_group
  grp.name = "Blue #2 Suction Flange"
  ge = grp.entities
  circle = ge.add_circle([4814.mm,1307.mm,1353.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Brown → P-02
  grp = ents.add_group
  grp.name = "Brown → P-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 333.mm, 0.mm)
  circle = ge.add_circle([4814.mm,896.mm,185.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-05 → X3 (Brown drain-out)"] || model.materials.add("P-05 → X3 (Brown drain-out)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown → P-02 elbow
  grp = ents.add_group
  grp.name = "Brown → P-02 elbow"
  ge = grp.entities
  arc = ge.add_arc([4814.mm,1229.mm,209.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4814.mm,1229.mm,185.mm], [0.000000,1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-05 → X3 (Brown drain-out)"] || model.materials.add("P-05 → X3 (Brown drain-out)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown → P-02
  grp = ents.add_group
  grp.name = "Brown → P-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1161.mm)
  circle = ge.add_circle([4814.mm,1253.mm,209.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-05 → X3 (Brown drain-out)"] || model.materials.add("P-05 → X3 (Brown drain-out)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown Suction Flange
  grp = ents.add_group
  grp.name = "Brown Suction Flange"
  ge = grp.entities
  circle = ge.add_circle([4814.mm,1037.mm,185.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Waste → P-03
  grp = ents.add_group
  grp.name = "Waste → P-03"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -189.mm, 0.mm)
  circle = ge.add_circle([4854.mm,1466.mm,185.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste → P-03 elbow
  grp = ents.add_group
  grp.name = "Waste → P-03 elbow"
  ge = grp.entities
  arc = ge.add_arc([4854.mm,1277.mm,209.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4854.mm,1277.mm,185.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste → P-03
  grp = ents.add_group
  grp.name = "Waste → P-03"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1419.mm)
  circle = ge.add_circle([4854.mm,1253.mm,209.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste Suction Flange
  grp = ents.add_group
  grp.name = "Waste Suction Flange"
  ge = grp.entities
  circle = ge.add_circle([4854.mm,1307.mm,185.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 151.mm)
  circle = ge.add_circle([4550.mm,155.mm,20.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4526.mm,155.mm,171.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4550.mm,155.mm,171.mm], [0.000000,0.000000,1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(-23.460000000000036.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4526.mm,155.mm,195.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4502.54.mm,132.46.mm,195.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 22.540000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4502.54.mm,155.mm,195.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -58.46000000000001.mm, 0.mm)
  circle = ge.add_circle([4480.mm,132.46.mm,195.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4480.mm,74.mm,171.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4480.mm,74.mm,195.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -117.mm)
  circle = ge.add_circle([4480.mm,50.mm,171.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4504.mm,50.mm,54.mm], [-1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4480.mm,50.mm,54.mm], [0.000000,0.000000,-1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(123.5.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4504.mm,50.mm,30.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4627.5.mm,74.mm,30.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4627.5.mm,50.mm,30.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 1095.975.mm, 0.mm)
  circle = ge.add_circle([4651.5.mm,74.mm,30.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4662.525.mm,1169.975.mm,30.mm], [-1.000000,0.000000,0.000000], [0.000000,0.000000,-1.000000], 11.025000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4651.5.mm,1169.975.mm,30.mm], [0.000000,1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(5.852249999999913.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4662.525.mm,1181.mm,30.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4668.37725.mm,1181.mm,35.62275000000018.mm], [0.000000,0.000000,-1.000000], [0.000000,-1.000000,0.000000], 5.622750000000179.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4668.37725.mm,1181.mm,30.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 30.37724999999982.mm)
  circle = ge.add_circle([4674.mm,1181.mm,35.62275000000018.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4698.mm,1181.mm,66.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4674.mm,1181.mm,66.mm], [0.000000,0.000000,1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(132.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4698.mm,1181.mm,90.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4830.mm,1157.mm,90.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,-1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4830.mm,1181.mm,90.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -24.480000000000018.mm, 0.mm)
  circle = ge.add_circle([4854.mm,1157.mm,90.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04 elbow
  grp = ents.add_group
  grp.name = "Tray Sump → P-04 elbow"
  ge = grp.entities
  arc = ge.add_arc([4854.mm,1132.52.mm,113.52000000000001.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 23.520000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4854.mm,1132.52.mm,90.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1514.48.mm)
  circle = ge.add_circle([4854.mm,1109.mm,113.52.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1096.mm)
  circle = ge.add_circle([4814.mm,1109.mm,1370.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar elbow
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar elbow"
  ge = grp.entities
  arc = ge.add_arc([4790.mm,1109.mm,274.mm], [1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4814.mm,1109.mm,274.mm], [0.000000,0.000000,-1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar"
  ge = grp.entities
  vec = Geom::Vector3d.new(-92.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4790.mm,1109.mm,250.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar elbow
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar elbow"
  ge = grp.entities
  arc = ge.add_arc([4698.mm,1109.mm,226.mm], [0.000000,0.000000,1.000000], [-0.000000,-1.000000,-0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4698.mm,1109.mm,250.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -153.75.mm)
  circle = ge.add_circle([4674.mm,1109.mm,226.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar elbow
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar elbow"
  ge = grp.entities
  arc = ge.add_arc([4661.75.mm,1109.mm,72.25.mm], [1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 12.250000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4674.mm,1109.mm,72.25.mm], [0.000000,0.000000,-1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar"
  ge = grp.entities
  vec = Geom::Vector3d.new(-6.5024999999996.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4661.75.mm,1109.mm,60.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar elbow
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar elbow"
  ge = grp.entities
  arc = ge.add_arc([4655.2475.mm,1102.7525.mm,60.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 6.2475000000000005.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4655.2475.mm,1109.mm,60.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -1081.4425.mm, 0.mm)
  circle = ge.add_circle([4649.mm,1102.7525.mm,60.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar elbow
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar elbow"
  ge = grp.entities
  arc = ge.add_arc([4649.mm,21.310000000000002.mm,50.69.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 9.310000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4649.mm,21.310000000000002.mm,60.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 → Spray Bar
  grp = ents.add_group
  grp.name = "P-01 → Spray Bar"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -9.689999999999998.mm)
  circle = ge.add_circle([4649.mm,12.mm,50.69.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-02 Diverter
  grp = ents.add_group
  grp.name = "3W-DV-02 Diverter"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -45.59999999999991.mm, 0.mm)
  circle = ge.add_circle([4854.mm,1081.8.mm,1088.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["SV-01 pH sample tap"] || model.materials.add("SV-01 pH sample tap")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-02 Diverter
  grp = ents.add_group
  grp.name = "3W-DV-02 Diverter"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 22.799999999999955.mm)
  circle = ge.add_circle([4854.mm,1059.mm,1088.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["SV-01 pH sample tap"] || model.materials.add("SV-01 pH sample tap")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # P-04 → DV-02
  grp = ents.add_group
  grp.name = "P-04 → DV-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -26.mm, 0.mm)
  circle = ge.add_circle([4854.mm,1109.mm,1628.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-05 → X3 (Brown drain-out)"] || model.materials.add("P-05 → X3 (Brown drain-out)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-04 → DV-02 elbow
  grp = ents.add_group
  grp.name = "P-04 → DV-02 elbow"
  ge = grp.entities
  arc = ge.add_arc([4854.mm,1083.mm,1604.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4854.mm,1083.mm,1628.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-05 → X3 (Brown drain-out)"] || model.materials.add("P-05 → X3 (Brown drain-out)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-04 → DV-02
  grp = ents.add_group
  grp.name = "P-04 → DV-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -516.mm)
  circle = ge.add_circle([4854.mm,1059.mm,1604.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-05 → X3 (Brown drain-out)"] || model.materials.add("P-05 → X3 (Brown drain-out)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 → IBC-3 side-entry
  grp = ents.add_group
  grp.name = "DV-02 → IBC-3 side-entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -163.mm, 0.mm)
  circle = ge.add_circle([4854.mm,1059.mm,1088.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-05 → X3 (Brown drain-out)"] || model.materials.add("P-05 → X3 (Brown drain-out)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 Recycle Flange
  grp = ents.add_group
  grp.name = "IBC-3 Recycle Flange"
  ge = grp.entities
  circle = ge.add_circle([4854.mm,1037.mm,1088.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 → Filters
  grp = ents.add_group
  grp.name = "P-02 → Filters"
  ge = grp.entities
  vec = Geom::Vector3d.new(-22.252676814717233.mm, -50.068522833113775.mm, 0.mm)
  circle = ge.add_circle([4814.mm,1253.mm,1370.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-05 → X3 (Brown drain-out)"] || model.materials.add("P-05 → X3 (Brown drain-out)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 → Filters elbow
  grp = ents.add_group
  grp.name = "P-02 → Filters elbow"
  ge = grp.entities
  arc = ge.add_arc([4791.747323185283.mm,1202.9314771668862.mm,1346.mm], [0.000000,0.000000,1.000000], [0.913812,-0.406138,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4791.747323185283.mm,1202.9314771668862.mm,1370.mm], [-0.406138,-0.913812,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-05 → X3 (Brown drain-out)"] || model.materials.add("P-05 → X3 (Brown drain-out)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 → Filters
  grp = ents.add_group
  grp.name = "P-02 → Filters"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1096.mm)
  circle = ge.add_circle([4782.mm,1181.mm,1346.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-05 → X3 (Brown drain-out)"] || model.materials.add("P-05 → X3 (Brown drain-out)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-01 Diverter
  grp = ents.add_group
  grp.name = "3W-DV-01 Diverter"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 45.59999999999991.mm, 0.mm)
  circle = ge.add_circle([4782.mm,1158.2.mm,2156.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["SV-01 pH sample tap"] || model.materials.add("SV-01 pH sample tap")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-01 Diverter
  grp = ents.add_group
  grp.name = "3W-DV-01 Diverter"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -22.800000000000182.mm)
  circle = ge.add_circle([4782.mm,1181.mm,2156.mm], vec, 16.200000000000003.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["SV-01 pH sample tap"] || model.materials.add("SV-01 pH sample tap")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Filters → DV-01 → IBC-2 side-entry
  grp = ents.add_group
  grp.name = "Filters → DV-01 → IBC-2 side-entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 972.mm)
  circle = ge.add_circle([4782.mm,1181.mm,1160.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 (50µ)"] || model.materials.add("Filter F1 (50µ)")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # Filters → DV-01 → IBC-2 side-entry elbow
  grp = ents.add_group
  grp.name = "Filters → DV-01 → IBC-2 side-entry elbow"
  ge = grp.entities
  arc = ge.add_arc([4782.mm,1205.mm,2132.mm], [0.000000,-1.000000,0.000000], [-1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4782.mm,1181.mm,2132.mm], [0.000000,0.000000,1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Filter F1 (50µ)"] || model.materials.add("Filter F1 (50µ)")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # Filters → DV-01 → IBC-2 side-entry
  grp = ents.add_group
  grp.name = "Filters → DV-01 → IBC-2 side-entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 261.mm, 0.mm)
  circle = ge.add_circle([4782.mm,1205.mm,2156.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 (50µ)"] || model.materials.add("Filter F1 (50µ)")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-2 Recycle Flange
  grp = ents.add_group
  grp.name = "IBC-2 Recycle Flange"
  ge = grp.entities
  circle = ge.add_circle([4782.mm,1307.mm,2156.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 → IBC-4 reject
  grp = ents.add_group
  grp.name = "DV-01 → IBC-4 reject"
  ge = grp.entities
  vec = Geom::Vector3d.new(17.850000000000364.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4782.mm,1181.mm,2156.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 → IBC-4 reject elbow
  grp = ents.add_group
  grp.name = "DV-01 → IBC-4 reject elbow"
  ge = grp.entities
  arc = ge.add_arc([4799.85.mm,1181.mm,2138.85.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 17.150000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4799.85.mm,1181.mm,2156.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 → IBC-4 reject
  grp = ents.add_group
  grp.name = "DV-01 → IBC-4 reject"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1026.85.mm)
  circle = ge.add_circle([4817.mm,1181.mm,2138.85.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 → IBC-4 reject elbow
  grp = ents.add_group
  grp.name = "DV-01 → IBC-4 reject elbow"
  ge = grp.entities
  arc = ge.add_arc([4817.mm,1205.mm,1112.mm], [0.000000,-1.000000,0.000000], [1.000000,-0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4817.mm,1181.mm,1112.mm], [0.000000,0.000000,-1.000000], 12.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 → IBC-4 reject
  grp = ents.add_group
  grp.name = "DV-01 → IBC-4 reject"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 261.mm, 0.mm)
  circle = ge.add_circle([4817.mm,1205.mm,1088.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-4 Reject Flange
  grp = ents.add_group
  grp.name = "IBC-4 Reject Flange"
  ge = grp.entities
  circle = ge.add_circle([4817.mm,1307.mm,1088.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(18.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue Supply Trunk (along pinhole wall)
  grp = ents.add_group
  grp.name = "Blue Supply Trunk (along pinhole wall)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-349.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4649.mm,12.mm,41.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
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
  mat = model.materials["P-05 → X3 (Brown drain-out)"] || model.materials.add("P-05 → X3 (Brown drain-out)")
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
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Water/Waste Hookups"
  inst.layer = model.layers["Plumbing & Panel"]

  # ═══ Walkway Cantilever Arms ═══
  defn = model.definitions.add("Walkway Cantilever Arms")
  ents = defn.entities
  # RWk center cantilever Yd1046 lower
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 lower"
  face = grp.entities.add_face([4329.mm,1046.mm,70.mm], [4734.mm,1046.mm,70.mm], [4734.mm,1086.mm,70.mm], [4329.mm,1086.mm,70.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1046 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 upper"
  face = grp.entities.add_face([4369.mm,1046.mm,95.mm], [4589.mm,1046.mm,95.mm], [4589.mm,1086.mm,95.mm], [4369.mm,1086.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1046 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 upper"
  face = grp.entities.add_face([4629.mm,1046.mm,95.mm], [4734.mm,1046.mm,95.mm], [4734.mm,1086.mm,95.mm], [4629.mm,1086.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1046 Y1038
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1046 Y1038"
  face = grp.entities.add_face([4730.mm,1038.mm,45.mm], [4788.mm,1038.mm,45.mm], [4788.mm,1046.mm,45.mm], [4730.mm,1046.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1046 Y1086
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1046 Y1086"
  face = grp.entities.add_face([4730.mm,1086.mm,45.mm], [4788.mm,1086.mm,45.mm], [4788.mm,1094.mm,45.mm], [4730.mm,1094.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1046 Z76
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1046 Z76"
  ge = grp.entities
  circle = ge.add_circle([4759.mm,1034.mm,76.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(64.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1046 Z133
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1046 Z133"
  ge = grp.entities
  circle = ge.add_circle([4759.mm,1034.mm,133.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(64.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1266 lower
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 lower"
  face = grp.entities.add_face([4329.mm,1266.mm,70.mm], [4734.mm,1266.mm,70.mm], [4734.mm,1306.mm,70.mm], [4329.mm,1306.mm,70.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1266 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 upper"
  face = grp.entities.add_face([4369.mm,1266.mm,95.mm], [4589.mm,1266.mm,95.mm], [4589.mm,1306.mm,95.mm], [4369.mm,1306.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk center cantilever Yd1266 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 upper"
  face = grp.entities.add_face([4629.mm,1266.mm,95.mm], [4734.mm,1266.mm,95.mm], [4734.mm,1306.mm,95.mm], [4629.mm,1306.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1266 Y1258
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1266 Y1258"
  face = grp.entities.add_face([4730.mm,1258.mm,45.mm], [4788.mm,1258.mm,45.mm], [4788.mm,1266.mm,45.mm], [4730.mm,1266.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright clamp Yd1266 Y1306
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1266 Y1306"
  face = grp.entities.add_face([4730.mm,1306.mm,45.mm], [4788.mm,1306.mm,45.mm], [4788.mm,1314.mm,45.mm], [4730.mm,1314.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1266 Z76
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1266 Z76"
  ge = grp.entities
  circle = ge.add_circle([4759.mm,1254.mm,76.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(64.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk upright bolt M12 Yd1266 Z133
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1266 Z133"
  ge = grp.entities
  circle = ge.add_circle([4759.mm,1254.mm,133.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(64.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
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
anc = Geom::Point3d.new(4814.mm, 1109.mm, 2021.mm)
txt = entities.add_text("ACC-01 (accumulator)", anc, Geom::Vector3d.new(-227.mm, -1759.mm, 329.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4814.mm, 1109.mm, 1687.mm)
txt = entities.add_text("P-04 (Tray-drain pump)", anc, Geom::Vector3d.new(-240.mm, -1759.mm, 263.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4814.mm, 1109.mm, 1429.mm)
txt = entities.add_text("P-01 (Blue-feed pump)", anc, Geom::Vector3d.new(-240.mm, -1759.mm, 121.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4854.mm, 1253.mm, 2055.mm)
txt = entities.add_text("P-05 (Brown drain pump)", anc, Geom::Vector3d.new(260.mm, -1903.mm, 295.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4854.mm, 1253.mm, 1687.mm)
txt = entities.add_text("P-03 (Waste-evac pump)", anc, Geom::Vector3d.new(260.mm, -1903.mm, 263.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4854.mm, 1253.mm, 1429.mm)
txt = entities.add_text("P-02 (Brown pump)", anc, Geom::Vector3d.new(260.mm, -1903.mm, 121.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4809.mm, 1181.mm, 1110.mm)
txt = entities.add_text("F3 (GAC filter)", anc, Geom::Vector3d.new(5.mm, -1831.mm, 40.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4809.mm, 1181.mm, 740.mm)
txt = entities.add_text("F2 (5um filter)", anc, Geom::Vector3d.new(5.mm, -1831.mm, 60.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4809.mm, 1181.mm, 370.mm)
txt = entities.add_text("F1 (50um filter)", anc, Geom::Vector3d.new(5.mm, -1831.mm, 80.mm))
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

[["IBC Tanks", ["IBC Tanks"]], ["IBC Frame", ["IBC Frame", "Walkway Cantilever"]], ["Plumbing & Panel", ["Plumbing & Panel"]], ["Combined", ["Context", "IBC Tanks", "IBC Frame", "Plumbing & Panel", "Walkway Cantilever"]], ["Labeled", ["Context", "IBC Tanks", "IBC Frame", "Plumbing & Panel", "Walkway Cantilever", "Labels"]]].each { |name, tags|
  model.layers.each { |l| l.visible = (l == default_layer || l.name == "Context" || tags.include?(l.name)) }
  page = model.pages.add(name)
  page.use_camera = true
}
model.layers.each { |l| l.visible = true }

model.commit_operation
{ success: true, model: "IBC Stack",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
