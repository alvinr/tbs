model = Sketchup.active_model
model.start_operation("TBS-001 IBC v2 study", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# ── Idempotent rebuild ──
to_erase = entities.to_a.select { |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text)
}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each { |p| model.pages.erase(p) }

# ── Tags ──
  model.layers.add("Context") unless model.layers["Context"]
  model.layers.add("IBC Tanks") unless model.layers["IBC Tanks"]
  model.layers.add("IBC Frame") unless model.layers["IBC Frame"]
  model.layers.add("Panel") unless model.layers["Panel"]
  model.layers.add("Walkway") unless model.layers["Walkway"]
  model.layers.add("Pipes") unless model.layers["Pipes"]
  model.layers.add("Labels") unless model.layers["Labels"]

# ── Subsystems ──
  # ═══ Container (ghost) ═══
  defn = model.definitions.add("Container (ghost)")
  ents = defn.entities
  # Floor (context)
  grp = ents.add_group
  grp.name = "Floor (context)"
  face = grp.entities.add_face([4200.mm,0.mm,-40.mm], [5893.mm,0.mm,-40.mm], [5893.mm,2362.mm,-40.mm], [4200.mm,2362.mm,-40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Floor (context)"] || model.materials.add("Floor (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.25
  grp.material = mat

  # Ceiling (context)
  grp = ents.add_group
  grp.name = "Ceiling (context)"
  face = grp.entities.add_face([4200.mm,0.mm,2388.mm], [5893.mm,0.mm,2388.mm], [5893.mm,2362.mm,2388.mm], [4200.mm,2362.mm,2388.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Ceiling (context)"] || model.materials.add("Ceiling (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.1
  grp.material = mat

  # Side Wall near (context)
  grp = ents.add_group
  grp.name = "Side Wall near (context)"
  face = grp.entities.add_face([4200.mm,-40.mm,0.mm], [5893.mm,-40.mm,0.mm], [5893.mm,0.mm,0.mm], [4200.mm,0.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Side Wall near (context)"] || model.materials.add("Side Wall near (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.16
  grp.material = mat

  # Side Wall far (context)
  grp = ents.add_group
  grp.name = "Side Wall far (context)"
  face = grp.entities.add_face([4200.mm,2362.mm,0.mm], [5893.mm,2362.mm,0.mm], [5893.mm,2402.mm,0.mm], [4200.mm,2402.mm,0.mm])
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

  # Film Right Rail near
  grp = ents.add_group
  grp.name = "Film Right Rail near"
  face = grp.entities.add_face([4649.mm,30.mm,0.mm], [4669.mm,30.mm,0.mm], [4669.mm,50.mm,0.mm], [4649.mm,50.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Film Right Rail near"] || model.materials.add("Film Right Rail near")
  mat.color = Sketchup::Color.new(32, 96, 160)
  mat.alpha = 0.6
  grp.material = mat

  # Film Right Rail far
  grp = ents.add_group
  grp.name = "Film Right Rail far"
  face = grp.entities.add_face([4649.mm,2312.mm,0.mm], [4669.mm,2312.mm,0.mm], [4669.mm,2332.mm,0.mm], [4649.mm,2332.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Film Right Rail near"] || model.materials.add("Film Right Rail near")
  mat.color = Sketchup::Color.new(32, 96, 160)
  mat.alpha = 0.6
  grp.material = mat

  # Film Plane no-go (X<4649)
  grp = ents.add_group
  grp.name = "Film Plane no-go (X<4649)"
  face = grp.entities.add_face([4649.mm,0.mm,0.mm], [4651.mm,0.mm,0.mm], [4651.mm,2362.mm,0.mm], [4649.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Film Plane no-go (X<4649)"] || model.materials.add("Film Plane no-go (X<4649)")
  mat.color = Sketchup::Color.new(32, 96, 160)
  mat.alpha = 0.06
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Container (ghost)"
  inst.layer = model.layers["Context"]

  # ═══ IBC Tanks ═══
  defn = model.definitions.add("IBC Tanks")
  ents = defn.entities
  # Brown cage
  grp = ents.add_group
  grp.name = "Brown cage"
  face = grp.entities.add_face([4674.mm,30.mm,0.mm], [5893.mm,30.mm,0.mm], [5893.mm,1046.mm,0.mm], [4674.mm,1046.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1168.mm)
  mat = model.materials["Brown cage"] || model.materials.add("Brown cage")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.1
  grp.material = mat

  # Brown pallet
  grp = ents.add_group
  grp.name = "Brown pallet"
  face = grp.entities.add_face([4674.mm,30.mm,0.mm], [5893.mm,30.mm,0.mm], [5893.mm,1046.mm,0.mm], [4674.mm,1046.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(168.mm)
  mat = model.materials["Brown pallet"] || model.materials.add("Brown pallet")
  mat.color = Sketchup::Color.new(154, 154, 154)
  mat.alpha = 0.55
  grp.material = mat

  # Brown contents
  grp = ents.add_group
  grp.name = "Brown contents"
  face = grp.entities.add_face([4714.mm,70.mm,168.mm], [5853.mm,70.mm,168.mm], [5853.mm,1006.mm,168.mm], [4714.mm,1006.mm,168.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(980.mm)
  mat = model.materials["Brown contents"] || model.materials.add("Brown contents")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 0.55
  grp.material = mat

  # Blue #1 cage
  grp = ents.add_group
  grp.name = "Blue #1 cage"
  face = grp.entities.add_face([4674.mm,30.mm,1168.mm], [5893.mm,30.mm,1168.mm], [5893.mm,1046.mm,1168.mm], [4674.mm,1046.mm,1168.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1168.mm)
  mat = model.materials["Brown cage"] || model.materials.add("Brown cage")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.1
  grp.material = mat

  # Blue #1 pallet
  grp = ents.add_group
  grp.name = "Blue #1 pallet"
  face = grp.entities.add_face([4674.mm,30.mm,1168.mm], [5893.mm,30.mm,1168.mm], [5893.mm,1046.mm,1168.mm], [4674.mm,1046.mm,1168.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(168.mm)
  mat = model.materials["Brown pallet"] || model.materials.add("Brown pallet")
  mat.color = Sketchup::Color.new(154, 154, 154)
  mat.alpha = 0.55
  grp.material = mat

  # Blue #1 contents
  grp = ents.add_group
  grp.name = "Blue #1 contents"
  face = grp.entities.add_face([4714.mm,70.mm,1336.mm], [5853.mm,70.mm,1336.mm], [5853.mm,1006.mm,1336.mm], [4714.mm,1006.mm,1336.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(784.mm)
  mat = model.materials["Blue #1 contents"] || model.materials.add("Blue #1 contents")
  mat.color = Sketchup::Color.new(46, 109, 180)
  mat.alpha = 0.55
  grp.material = mat

  # Waste cage
  grp = ents.add_group
  grp.name = "Waste cage"
  face = grp.entities.add_face([4674.mm,1316.mm,0.mm], [5893.mm,1316.mm,0.mm], [5893.mm,2332.mm,0.mm], [4674.mm,2332.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1168.mm)
  mat = model.materials["Brown cage"] || model.materials.add("Brown cage")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.1
  grp.material = mat

  # Waste pallet
  grp = ents.add_group
  grp.name = "Waste pallet"
  face = grp.entities.add_face([4674.mm,1316.mm,0.mm], [5893.mm,1316.mm,0.mm], [5893.mm,2332.mm,0.mm], [4674.mm,2332.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(168.mm)
  mat = model.materials["Brown pallet"] || model.materials.add("Brown pallet")
  mat.color = Sketchup::Color.new(154, 154, 154)
  mat.alpha = 0.55
  grp.material = mat

  # Waste contents
  grp = ents.add_group
  grp.name = "Waste contents"
  face = grp.entities.add_face([4714.mm,1356.mm,168.mm], [5853.mm,1356.mm,168.mm], [5853.mm,2292.mm,168.mm], [4714.mm,2292.mm,168.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(980.mm)
  mat = model.materials["Waste contents"] || model.materials.add("Waste contents")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 0.55
  grp.material = mat

  # Blue #2 cage
  grp = ents.add_group
  grp.name = "Blue #2 cage"
  face = grp.entities.add_face([4674.mm,1316.mm,1168.mm], [5893.mm,1316.mm,1168.mm], [5893.mm,2332.mm,1168.mm], [4674.mm,2332.mm,1168.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1168.mm)
  mat = model.materials["Brown cage"] || model.materials.add("Brown cage")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.1
  grp.material = mat

  # Blue #2 pallet
  grp = ents.add_group
  grp.name = "Blue #2 pallet"
  face = grp.entities.add_face([4674.mm,1316.mm,1168.mm], [5893.mm,1316.mm,1168.mm], [5893.mm,2332.mm,1168.mm], [4674.mm,2332.mm,1168.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(168.mm)
  mat = model.materials["Brown pallet"] || model.materials.add("Brown pallet")
  mat.color = Sketchup::Color.new(154, 154, 154)
  mat.alpha = 0.55
  grp.material = mat

  # Blue #2 contents
  grp = ents.add_group
  grp.name = "Blue #2 contents"
  face = grp.entities.add_face([4714.mm,1356.mm,1336.mm], [5853.mm,1356.mm,1336.mm], [5853.mm,2292.mm,1336.mm], [4714.mm,2292.mm,1336.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(784.mm)
  mat = model.materials["Blue #1 contents"] || model.materials.add("Blue #1 contents")
  mat.color = Sketchup::Color.new(46, 109, 180)
  mat.alpha = 0.55
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

  # Foot Anchor M12
  grp = ents.add_group
  grp.name = "Foot Anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4709.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor M12
  grp = ents.add_group
  grp.name = "Foot Anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4709.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor M12
  grp = ents.add_group
  grp.name = "Foot Anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4809.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor M12
  grp = ents.add_group
  grp.name = "Foot Anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4809.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
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

  # Foot Anchor M12
  grp = ents.add_group
  grp.name = "Foot Anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4709.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor M12
  grp = ents.add_group
  grp.name = "Foot Anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4709.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor M12
  grp = ents.add_group
  grp.name = "Foot Anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4809.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor M12
  grp = ents.add_group
  grp.name = "Foot Anchor M12"
  ge = grp.entities
  circle = ge.add_circle([4809.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
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
  face = grp.entities.add_face([4674.mm,1046.mm,560.mm], [4784.mm,1046.mm,560.mm], [4784.mm,1096.mm,560.mm], [4674.mm,1096.mm,560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Bar Stub
  grp = ents.add_group
  grp.name = "Front Bar Stub"
  face = grp.entities.add_face([4674.mm,1046.mm,1760.mm], [4784.mm,1046.mm,1760.mm], [4784.mm,1096.mm,1760.mm], [4674.mm,1096.mm,1760.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Bar Stub
  grp = ents.add_group
  grp.name = "Front Bar Stub"
  face = grp.entities.add_face([4674.mm,1266.mm,560.mm], [4784.mm,1266.mm,560.mm], [4784.mm,1316.mm,560.mm], [4674.mm,1316.mm,560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Front Bar Stub
  grp = ents.add_group
  grp.name = "Front Bar Stub"
  face = grp.entities.add_face([4674.mm,1266.mm,1760.mm], [4784.mm,1266.mm,1760.mm], [4784.mm,1316.mm,1760.mm], [4674.mm,1316.mm,1760.mm])
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
  circle = ge.add_circle([4668.mm,520.mm,585.mm], [1,0,0], 16.mm, 24)
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
  circle = ge.add_circle([4668.mm,520.mm,1785.mm], [1,0,0], 16.mm, 24)
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
  circle = ge.add_circle([4668.mm,1842.mm,585.mm], [1,0,0], 16.mm, 24)
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
  circle = ge.add_circle([4668.mm,1842.mm,1785.mm], [1,0,0], 16.mm, 24)
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
  face = grp.entities.add_face([4666.mm,0.mm,530.mm], [4732.mm,0.mm,530.mm], [4732.mm,4.mm,530.mm], [4666.mm,4.mm,530.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4670.mm,0.mm,556.mm], [4728.mm,0.mm,556.mm], [4728.mm,70.mm,556.mm], [4670.mm,70.mm,556.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4649.mm,-48.mm,517.5.mm], [4749.mm,-48.mm,517.5.mm], [4749.mm,-40.mm,517.5.mm], [4649.mm,-40.mm,517.5.mm])
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
  circle = ge.add_circle([4667.mm,-48.mm,539.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4667.mm,-48.mm,630.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4731.mm,-48.mm,539.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4731.mm,-48.mm,630.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4666.mm,2358.mm,530.mm], [4732.mm,2358.mm,530.mm], [4732.mm,2362.mm,530.mm], [4666.mm,2362.mm,530.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4670.mm,2292.mm,556.mm], [4728.mm,2292.mm,556.mm], [4728.mm,2362.mm,556.mm], [4670.mm,2362.mm,556.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4649.mm,2402.mm,517.5.mm], [4749.mm,2402.mm,517.5.mm], [4749.mm,2410.mm,517.5.mm], [4649.mm,2410.mm,517.5.mm])
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
  circle = ge.add_circle([4667.mm,2352.mm,539.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4667.mm,2352.mm,630.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4731.mm,2352.mm,539.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4731.mm,2352.mm,630.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4666.mm,0.mm,1730.mm], [4732.mm,0.mm,1730.mm], [4732.mm,4.mm,1730.mm], [4666.mm,4.mm,1730.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4670.mm,0.mm,1756.mm], [4728.mm,0.mm,1756.mm], [4728.mm,70.mm,1756.mm], [4670.mm,70.mm,1756.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4649.mm,-48.mm,1717.5.mm], [4749.mm,-48.mm,1717.5.mm], [4749.mm,-40.mm,1717.5.mm], [4649.mm,-40.mm,1717.5.mm])
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
  circle = ge.add_circle([4667.mm,-48.mm,1739.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4667.mm,-48.mm,1830.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4731.mm,-48.mm,1739.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4731.mm,-48.mm,1830.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4666.mm,2358.mm,1730.mm], [4732.mm,2358.mm,1730.mm], [4732.mm,2362.mm,1730.mm], [4666.mm,2362.mm,1730.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4670.mm,2292.mm,1756.mm], [4728.mm,2292.mm,1756.mm], [4728.mm,2362.mm,1756.mm], [4670.mm,2362.mm,1756.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4649.mm,2402.mm,1717.5.mm], [4749.mm,2402.mm,1717.5.mm], [4749.mm,2410.mm,1717.5.mm], [4649.mm,2410.mm,1717.5.mm])
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
  circle = ge.add_circle([4667.mm,2352.mm,1739.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4667.mm,2352.mm,1830.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4731.mm,2352.mm,1739.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # IBC Wall Through-Bolt M12
  grp = ents.add_group
  grp.name = "IBC Wall Through-Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4731.mm,2352.mm,1830.5.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(58.mm)
  mat = model.materials["Foot Anchor M12"] || model.materials.add("Foot Anchor M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "IBC Frame"
  inst.layer = model.layers["IBC Frame"]

  # ═══ Right Walkway ═══
  defn = model.definitions.add("Right Walkway")
  ents = defn.entities
  # RWk Long beam X4329 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 upper"
  face = grp.entities.add_face([4329.mm,0.mm,95.mm], [4369.mm,0.mm,95.mm], [4369.mm,2362.mm,95.mm], [4329.mm,2362.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4329 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 lower"
  face = grp.entities.add_face([4329.mm,0.mm,80.mm], [4369.mm,0.mm,80.mm], [4369.mm,1046.mm,80.mm], [4329.mm,1046.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4329 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 lower"
  face = grp.entities.add_face([4329.mm,1086.mm,80.mm], [4369.mm,1086.mm,80.mm], [4369.mm,1266.mm,80.mm], [4329.mm,1266.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4329 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 lower"
  face = grp.entities.add_face([4329.mm,1306.mm,80.mm], [4369.mm,1306.mm,80.mm], [4369.mm,2362.mm,80.mm], [4329.mm,2362.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 upper"
  face = grp.entities.add_face([4589.mm,0.mm,95.mm], [4629.mm,0.mm,95.mm], [4629.mm,2362.mm,95.mm], [4589.mm,2362.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 lower"
  face = grp.entities.add_face([4589.mm,0.mm,80.mm], [4629.mm,0.mm,80.mm], [4629.mm,1046.mm,80.mm], [4589.mm,1046.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 lower"
  face = grp.entities.add_face([4589.mm,1086.mm,80.mm], [4629.mm,1086.mm,80.mm], [4629.mm,1266.mm,80.mm], [4589.mm,1266.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk Long beam X4589 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4589 lower"
  face = grp.entities.add_face([4589.mm,1306.mm,80.mm], [4629.mm,1306.mm,80.mm], [4629.mm,2362.mm,80.mm], [4589.mm,2362.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk end beam Yd0
  grp = ents.add_group
  grp.name = "RWk end beam Yd0"
  face = grp.entities.add_face([4329.mm,0.mm,80.mm], [4629.mm,0.mm,80.mm], [4629.mm,40.mm,80.mm], [4329.mm,40.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(35.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk end beam Yd2322
  grp = ents.add_group
  grp.name = "RWk end beam Yd2322"
  face = grp.entities.add_face([4329.mm,2322.mm,80.mm], [4629.mm,2322.mm,80.mm], [4629.mm,2362.mm,80.mm], [4329.mm,2362.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(35.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

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

  # RWk wall cleat plate (near)
  grp = ents.add_group
  grp.name = "RWk wall cleat plate (near)"
  face = grp.entities.add_face([4304.mm,0.mm,60.mm], [4394.mm,0.mm,60.mm], [4394.mm,8.mm,60.mm], [4304.mm,8.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(65.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat ext plate (near)
  grp = ents.add_group
  grp.name = "RWk wall cleat ext plate (near)"
  face = grp.entities.add_face([4304.mm,-48.mm,60.mm], [4394.mm,-48.mm,60.mm], [4394.mm,-40.mm,60.mm], [4304.mm,-40.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(65.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat shelf (near)
  grp = ents.add_group
  grp.name = "RWk wall cleat shelf (near)"
  face = grp.entities.add_face([4304.mm,0.mm,60.mm], [4394.mm,0.mm,60.mm], [4394.mm,55.mm,60.mm], [4304.mm,55.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall bolt (near) Z76
  grp = ents.add_group
  grp.name = "RWk wall bolt (near) Z76"
  ge = grp.entities
  circle = ge.add_circle([4349.mm,-48.mm,76.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall bolt (near) Z109
  grp = ents.add_group
  grp.name = "RWk wall bolt (near) Z109"
  ge = grp.entities
  circle = ge.add_circle([4349.mm,-48.mm,109.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner plate (near)
  grp = ents.add_group
  grp.name = "FP combined corner plate (near)"
  face = grp.entities.add_face([4574.mm,0.mm,58.mm], [4724.mm,0.mm,58.mm], [4724.mm,10.mm,58.mm], [4574.mm,10.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(167.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner ext plate (near)
  grp = ents.add_group
  grp.name = "FP combined corner ext plate (near)"
  face = grp.entities.add_face([4574.mm,-50.mm,58.mm], [4724.mm,-50.mm,58.mm], [4724.mm,-40.mm,58.mm], [4574.mm,-40.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(167.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined right-beam seat (near)
  grp = ents.add_group
  grp.name = "FP combined right-beam seat (near)"
  face = grp.entities.add_face([4574.mm,0.mm,58.mm], [4724.mm,0.mm,58.mm], [4724.mm,55.mm,58.mm], [4574.mm,55.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined BR rail seat (near)
  grp = ents.add_group
  grp.name = "FP combined BR rail seat (near)"
  face = grp.entities.add_face([4619.mm,0.mm,138.mm], [4679.mm,0.mm,138.mm], [4679.mm,55.mm,138.mm], [4619.mm,55.mm,138.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X4599 Z84
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X4599 Z84"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,-50.mm,84.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X4599 Z178
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X4599 Z178"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,-50.mm,178.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X4699 Z84
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X4699 Z84"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,-50.mm,84.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (near) X4699 Z178
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (near) X4699 Z178"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,-50.mm,178.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat plate (far)
  grp = ents.add_group
  grp.name = "RWk wall cleat plate (far)"
  face = grp.entities.add_face([4304.mm,2354.mm,60.mm], [4394.mm,2354.mm,60.mm], [4394.mm,2362.mm,60.mm], [4304.mm,2362.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(65.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat ext plate (far)
  grp = ents.add_group
  grp.name = "RWk wall cleat ext plate (far)"
  face = grp.entities.add_face([4304.mm,2402.mm,60.mm], [4394.mm,2402.mm,60.mm], [4394.mm,2410.mm,60.mm], [4304.mm,2410.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(65.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall cleat shelf (far)
  grp = ents.add_group
  grp.name = "RWk wall cleat shelf (far)"
  face = grp.entities.add_face([4304.mm,2307.mm,60.mm], [4394.mm,2307.mm,60.mm], [4394.mm,2362.mm,60.mm], [4304.mm,2362.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall bolt (far) Z76
  grp = ents.add_group
  grp.name = "RWk wall bolt (far) Z76"
  ge = grp.entities
  circle = ge.add_circle([4349.mm,2354.mm,76.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # RWk wall bolt (far) Z109
  grp = ents.add_group
  grp.name = "RWk wall bolt (far) Z109"
  ge = grp.entities
  circle = ge.add_circle([4349.mm,2354.mm,109.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner plate (far)
  grp = ents.add_group
  grp.name = "FP combined corner plate (far)"
  face = grp.entities.add_face([4574.mm,2352.mm,58.mm], [4724.mm,2352.mm,58.mm], [4724.mm,2362.mm,58.mm], [4574.mm,2362.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(167.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined corner ext plate (far)
  grp = ents.add_group
  grp.name = "FP combined corner ext plate (far)"
  face = grp.entities.add_face([4574.mm,2402.mm,58.mm], [4724.mm,2402.mm,58.mm], [4724.mm,2412.mm,58.mm], [4574.mm,2412.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(167.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined right-beam seat (far)
  grp = ents.add_group
  grp.name = "FP combined right-beam seat (far)"
  face = grp.entities.add_face([4574.mm,2307.mm,58.mm], [4724.mm,2307.mm,58.mm], [4724.mm,2362.mm,58.mm], [4574.mm,2362.mm,58.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined BR rail seat (far)
  grp = ents.add_group
  grp.name = "FP combined BR rail seat (far)"
  face = grp.entities.add_face([4619.mm,2307.mm,138.mm], [4679.mm,2307.mm,138.mm], [4679.mm,2362.mm,138.mm], [4619.mm,2362.mm,138.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (far) X4599 Z84
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (far) X4599 Z84"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,2352.mm,84.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (far) X4599 Z178
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (far) X4599 Z178"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,2352.mm,178.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (far) X4699 Z84
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (far) X4699 Z84"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,2352.mm,84.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # FP combined bolt M12 (far) X4699 Z178
  grp = ents.add_group
  grp.name = "FP combined bolt M12 (far) X4699 Z178"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,2352.mm,178.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right walkway grate (cantilevered)
  grp = ents.add_group
  grp.name = "Right walkway grate (cantilevered)"
  face = grp.entities.add_face([4329.mm,0.mm,115.mm], [4629.mm,0.mm,115.mm], [4629.mm,2362.mm,115.mm], [4329.mm,2362.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Right walkway grate (cantilevered)"] || model.materials.add("Right walkway grate (cantilevered)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Right Walkway"
  inst.layer = model.layers["Walkway"]

  # ═══ Equipment Panel ═══
  defn = model.definitions.add("Equipment Panel")
  ents = defn.entities
  # Equipment Panel (ply)
  grp = ents.add_group
  grp.name = "Equipment Panel (ply)"
  face = grp.entities.add_face([4874.mm,1046.mm,250.mm], [4892.mm,1046.mm,250.mm], [4892.mm,1316.mm,250.mm], [4874.mm,1316.mm,250.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2060.mm)
  mat = model.materials["Equipment Panel (ply)"] || model.materials.add("Equipment Panel (ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-01 (Blue)
  grp = ents.add_group
  grp.name = "Pump P-01 (Blue)"
  face = grp.entities.add_face([4774.mm,1045.5.mm,1370.mm], [4874.mm,1045.5.mm,1370.mm], [4874.mm,1172.5.mm,1370.mm], [4774.mm,1172.5.mm,1370.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-02 (Brown)
  grp = ents.add_group
  grp.name = "Pump P-02 (Brown)"
  face = grp.entities.add_face([4774.mm,1189.5.mm,1370.mm], [4874.mm,1189.5.mm,1370.mm], [4874.mm,1316.5.mm,1370.mm], [4774.mm,1316.5.mm,1370.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-04 (Tray drain)
  grp = ents.add_group
  grp.name = "Pump P-04 (Tray drain)"
  face = grp.entities.add_face([4774.mm,1045.5.mm,1628.mm], [4874.mm,1045.5.mm,1628.mm], [4874.mm,1172.5.mm,1628.mm], [4774.mm,1172.5.mm,1628.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-03 (Waste evac)
  grp = ents.add_group
  grp.name = "Pump P-03 (Waste evac)"
  face = grp.entities.add_face([4774.mm,1189.5.mm,1628.mm], [4874.mm,1189.5.mm,1628.mm], [4874.mm,1316.5.mm,1628.mm], [4774.mm,1316.5.mm,1628.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-05 (Brown drain)
  grp = ents.add_group
  grp.name = "Pump P-05 (Brown drain)"
  face = grp.entities.add_face([4774.mm,1189.5.mm,1996.mm], [4874.mm,1189.5.mm,1996.mm], [4874.mm,1316.5.mm,1996.mm], [4774.mm,1316.5.mm,1996.mm])
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
  cface.pushpull(150.mm)
  mat = model.materials["ACC-01 Accumulator"] || model.materials.add("ACC-01 Accumulator")
  mat.color = Sketchup::Color.new(90, 154, 204)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F1 (50µ)
  grp = ents.add_group
  grp.name = "Filter F1 (50µ)"
  ge = grp.entities
  circle = ge.add_circle([4809.mm,1181.mm,250.mm], [0,0,1], 65.mm, 24)
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
  circle = ge.add_circle([4809.mm,1181.mm,620.mm], [0,0,1], 65.mm, 24)
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
  circle = ge.add_circle([4809.mm,1181.mm,990.mm], [0,0,1], 65.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(340.mm)
  mat = model.materials["Filter F1 (50µ)"] || model.materials.add("Filter F1 (50µ)")
  mat.color = Sketchup::Color.new(58, 110, 165)
  mat.alpha = 1.0
  grp.material = mat

  # Drain-riser spine (ply)
  grp = ents.add_group
  grp.name = "Drain-riser spine (ply)"
  face = grp.entities.add_face([4874.mm,1223.mm,250.mm], [5420.mm,1223.mm,250.mm], [5420.mm,1241.mm,250.mm], [4874.mm,1241.mm,250.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1970.mm)
  mat = model.materials["Equipment Panel (ply)"] || model.materials.add("Equipment Panel (ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Drain-riser spine flange (ply)
  grp = ents.add_group
  grp.name = "Drain-riser spine flange (ply)"
  face = grp.entities.add_face([5402.mm,1226.mm,250.mm], [5420.mm,1226.mm,250.mm], [5420.mm,1280.mm,250.mm], [5402.mm,1280.mm,250.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1970.mm)
  mat = model.materials["Equipment Panel (ply)"] || model.materials.add("Equipment Panel (ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Drain-riser spine top shelf (ply)
  grp = ents.add_group
  grp.name = "Drain-riser spine top shelf (ply)"
  face = grp.entities.add_face([4874.mm,1160.mm,2220.mm], [5460.mm,1160.mm,2220.mm], [5460.mm,1241.mm,2220.mm], [4874.mm,1241.mm,2220.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Equipment Panel (ply)"] || model.materials.add("Equipment Panel (ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Blue fill pipe clamp
  grp = ents.add_group
  grp.name = "Blue fill pipe clamp"
  face = grp.entities.add_face([5420.mm,1165.mm,2238.mm], [5456.mm,1165.mm,2238.mm], [5456.mm,1197.mm,2238.mm], [5420.mm,1197.mm,2238.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Front Portal Upright"] || model.materials.add("Front Portal Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
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
  inst.name = "Equipment Panel"
  inst.layer = model.layers["Panel"]

  # ═══ Water Hookups X1/X3/X4 ═══
  defn = model.definitions.add("Water Hookups X1/X3/X4")
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
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
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
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Water Hookups X1/X3/X4"
  inst.layer = model.layers["Pipes"]

  # ═══ Plumbing (first pass) ═══
  defn = model.definitions.add("Plumbing (first pass)")
  ents = defn.entities
  # X1 Blue Fill Trunk
  grp = ents.add_group
  grp.name = "X1 Blue Fill Trunk"
  ge = grp.entities
  vec = Geom::Vector3d.new(-240.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5893.mm,1181.mm,2250.mm], vec, 24.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 Fill Branch
  grp = ents.add_group
  grp.name = "Blue #1 Fill Branch"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -47.940000000000055.mm)
  circle = ge.add_circle([5653.mm,1181.mm,2250.mm], vec, 24.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 Fill Branch elbow
  grp = ents.add_group
  grp.name = "Blue #1 Fill Branch elbow"
  ge = grp.entities
  arc = ge.add_arc([5653.mm,1134.94.mm,2202.06.mm], [0.000000,1.000000,0.000000], [-1.000000,-0.000000,-0.000000], 46.06000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5653.mm,1181.mm,2202.06.mm], [0.000000,0.000000,-1.000000], 24.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 Fill Branch
  grp = ents.add_group
  grp.name = "Blue #1 Fill Branch"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -148.94000000000005.mm, 0.mm)
  circle = ge.add_circle([5653.mm,1134.94.mm,2156.mm], vec, 24.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #1 Fill Flange
  grp = ents.add_group
  grp.name = "Blue #1 Fill Flange"
  ge = grp.entities
  circle = ge.add_circle([5653.mm,1046.mm,2156.mm], [0,1,0], 38.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #2 Fill Branch
  grp = ents.add_group
  grp.name = "Blue #2 Fill Branch"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 195.mm, 0.mm)
  circle = ge.add_circle([5653.mm,1181.mm,2156.mm], vec, 24.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Blue #2 Fill Flange
  grp = ents.add_group
  grp.name = "Blue #2 Fill Flange"
  ge = grp.entities
  circle = ge.add_circle([5653.mm,1316.mm,2156.mm], [0,1,0], 38.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["X1 Blue Fill Trunk"] || model.materials.add("X1 Blue Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Brown drain suction (IBC-3 -> P-05)
  grp = ents.add_group
  grp.name = "Brown drain suction (IBC-3 -> P-05)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 30.600000000000023.mm, 0.mm)
  circle = ge.add_circle([4900.mm,986.mm,185.mm], vec, 24.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown drain suction (IBC-3 -> P-05) elbow
  grp = ents.add_group
  grp.name = "Brown drain suction (IBC-3 -> P-05) elbow"
  ge = grp.entities
  arc = ge.add_arc([4900.mm,1016.6.mm,214.4.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 29.400000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4900.mm,1016.6.mm,185.mm], [0.000000,1.000000,0.000000], 24.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown drain suction (IBC-3 -> P-05)
  grp = ents.add_group
  grp.name = "Brown drain suction (IBC-3 -> P-05)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1853.3600000000001.mm)
  circle = ge.add_circle([4900.mm,1046.mm,214.4.mm], vec, 24.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown drain suction (IBC-3 -> P-05) elbow
  grp = ents.add_group
  grp.name = "Brown drain suction (IBC-3 -> P-05) elbow"
  ge = grp.entities
  arc = ge.add_arc([4862.76.mm,1046.mm,2067.76.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 37.24000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4900.mm,1046.mm,2067.76.mm], [0.000000,0.000000,1.000000], 24.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown drain suction (IBC-3 -> P-05)
  grp = ents.add_group
  grp.name = "Brown drain suction (IBC-3 -> P-05)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-19.76760000000013.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4862.76.mm,1046.mm,2105.mm], vec, 24.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown drain suction (IBC-3 -> P-05) elbow
  grp = ents.add_group
  grp.name = "Brown drain suction (IBC-3 -> P-05) elbow"
  ge = grp.entities
  arc = ge.add_arc([4842.9924.mm,1064.9924.mm,2105.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,-1.000000], 18.99240000000011.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4842.9924.mm,1046.mm,2105.mm], [-1.000000,0.000000,0.000000], 24.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown drain suction (IBC-3 -> P-05)
  grp = ents.add_group
  grp.name = "Brown drain suction (IBC-3 -> P-05)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 188.0075999999999.mm, 0.mm)
  circle = ge.add_circle([4824.mm,1064.9924.mm,2105.mm], vec, 24.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown Drain Flange
  grp = ents.add_group
  grp.name = "Brown Drain Flange"
  ge = grp.entities
  circle = ge.add_circle([4900.mm,1046.mm,185.mm], [0,1,0], 38.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown drain discharge (P-05 -> X3)
  grp = ents.add_group
  grp.name = "Brown drain discharge (P-05 -> X3)"
  ge = grp.entities
  vec = Geom::Vector3d.new(564.7200000000003.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4824.mm,1253.mm,2235.mm], vec, 24.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown drain discharge (P-05 -> X3) elbow
  grp = ents.add_group
  grp.name = "Brown drain discharge (P-05 -> X3) elbow"
  ge = grp.entities
  arc = ge.add_arc([5388.72.mm,1217.72.mm,2235.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,-1.000000], 35.28000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5388.72.mm,1253.mm,2235.mm], [1.000000,0.000000,0.000000], 24.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown drain discharge (P-05 -> X3)
  grp = ents.add_group
  grp.name = "Brown drain discharge (P-05 -> X3)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -18.72720000000004.mm, 0.mm)
  circle = ge.add_circle([5424.mm,1217.72.mm,2235.mm], vec, 24.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown drain discharge (P-05 -> X3) elbow
  grp = ents.add_group
  grp.name = "Brown drain discharge (P-05 -> X3) elbow"
  ge = grp.entities
  arc = ge.add_arc([5424.mm,1198.9928.mm,2217.0072.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 17.992800000000017.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5424.mm,1198.9928.mm,2235.mm], [0.000000,-1.000000,0.000000], 24.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown drain discharge (P-05 -> X3)
  grp = ents.add_group
  grp.name = "Brown drain discharge (P-05 -> X3)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1769.0072.mm)
  circle = ge.add_circle([5424.mm,1181.mm,2217.0072.mm], vec, 24.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown drain discharge (P-05 -> X3) elbow
  grp = ents.add_group
  grp.name = "Brown drain discharge (P-05 -> X3) elbow"
  ge = grp.entities
  arc = ge.add_arc([5472.mm,1181.mm,448.mm], [-1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 48.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5424.mm,1181.mm,448.mm], [0.000000,0.000000,-1.000000], 24.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Brown drain discharge (P-05 -> X3)
  grp = ents.add_group
  grp.name = "Brown drain discharge (P-05 -> X3)"
  ge = grp.entities
  vec = Geom::Vector3d.new(421.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5472.mm,1181.mm,400.mm], vec, 24.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Waste drain suction (IBC-4 -> P-03)
  grp = ents.add_group
  grp.name = "Waste drain suction (IBC-4 -> P-03)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -30.59999999999991.mm, 0.mm)
  circle = ge.add_circle([4974.mm,1376.mm,185.mm], vec, 24.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste drain suction (IBC-4 -> P-03) elbow
  grp = ents.add_group
  grp.name = "Waste drain suction (IBC-4 -> P-03) elbow"
  ge = grp.entities
  arc = ge.add_arc([4974.mm,1345.4.mm,214.4.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 29.400000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4974.mm,1345.4.mm,185.mm], [0.000000,-1.000000,0.000000], 24.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste drain suction (IBC-4 -> P-03)
  grp = ents.add_group
  grp.name = "Waste drain suction (IBC-4 -> P-03)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1474.6.mm)
  circle = ge.add_circle([4974.mm,1316.mm,214.4.mm], vec, 24.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste drain suction (IBC-4 -> P-03) elbow
  grp = ents.add_group
  grp.name = "Waste drain suction (IBC-4 -> P-03) elbow"
  ge = grp.entities
  arc = ge.add_arc([4926.mm,1316.mm,1689.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 48.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4974.mm,1316.mm,1689.mm], [0.000000,0.000000,1.000000], 24.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste drain suction (IBC-4 -> P-03)
  grp = ents.add_group
  grp.name = "Waste drain suction (IBC-4 -> P-03)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-71.13000000000011.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4926.mm,1316.mm,1737.mm], vec, 24.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste drain suction (IBC-4 -> P-03) elbow
  grp = ents.add_group
  grp.name = "Waste drain suction (IBC-4 -> P-03) elbow"
  ge = grp.entities
  arc = ge.add_arc([4854.87.mm,1285.13.mm,1737.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 30.870000000000005.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4854.87.mm,1316.mm,1737.mm], [-1.000000,0.000000,0.000000], 24.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste drain suction (IBC-4 -> P-03)
  grp = ents.add_group
  grp.name = "Waste drain suction (IBC-4 -> P-03)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -32.13000000000011.mm, 0.mm)
  circle = ge.add_circle([4824.mm,1285.13.mm,1737.mm], vec, 24.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste Drain Flange
  grp = ents.add_group
  grp.name = "Waste Drain Flange"
  ge = grp.entities
  circle = ge.add_circle([4974.mm,1316.mm,185.mm], [0,1,0], 38.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste drain discharge (P-03 -> X4)
  grp = ents.add_group
  grp.name = "Waste drain discharge (P-03 -> X4)"
  ge = grp.entities
  vec = Geom::Vector3d.new(684.7200000000003.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4824.mm,1253.mm,1607.mm], vec, 24.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste drain discharge (P-03 -> X4) elbow
  grp = ents.add_group
  grp.name = "Waste drain discharge (P-03 -> X4) elbow"
  ge = grp.entities
  arc = ge.add_arc([5508.72.mm,1217.72.mm,1607.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,-1.000000], 35.28000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5508.72.mm,1253.mm,1607.mm], [1.000000,0.000000,0.000000], 24.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste drain discharge (P-03 -> X4)
  grp = ents.add_group
  grp.name = "Waste drain discharge (P-03 -> X4)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -18.72720000000004.mm, 0.mm)
  circle = ge.add_circle([5544.mm,1217.72.mm,1607.mm], vec, 24.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste drain discharge (P-03 -> X4) elbow
  grp = ents.add_group
  grp.name = "Waste drain discharge (P-03 -> X4) elbow"
  ge = grp.entities
  arc = ge.add_arc([5544.mm,1198.9928.mm,1589.0072.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 17.992800000000017.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5544.mm,1198.9928.mm,1607.mm], [0.000000,-1.000000,0.000000], 24.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste drain discharge (P-03 -> X4)
  grp = ents.add_group
  grp.name = "Waste drain discharge (P-03 -> X4)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1341.0072.mm)
  circle = ge.add_circle([5544.mm,1181.mm,1589.0072.mm], vec, 24.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste drain discharge (P-03 -> X4) elbow
  grp = ents.add_group
  grp.name = "Waste drain discharge (P-03 -> X4) elbow"
  ge = grp.entities
  arc = ge.add_arc([5592.mm,1181.mm,248.mm], [-1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 48.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5544.mm,1181.mm,248.mm], [0.000000,0.000000,-1.000000], 24.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Waste drain discharge (P-03 -> X4)
  grp = ents.add_group
  grp.name = "Waste drain discharge (P-03 -> X4)"
  ge = grp.entities
  vec = Geom::Vector3d.new(301.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5592.mm,1181.mm,200.mm], vec, 24.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Waste Drain Hookup (2in NPT)"] || model.materials.add("Waste Drain Hookup (2in NPT)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Plumbing (first pass)"
  inst.layer = model.layers["Pipes"]


# ── Slide the existing equipment panel forward to the film-safe position ──
pinst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Equipment Panel" }
pinst.transform!(Geom::Transformation.translation([0.mm,0,0])) if pinst

# ── In-model labels (Labels tag; visible in the "Labeled" scene) ──
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Blue #1 contents" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("Blue #1 (1000L tote, ~800L)
clean supply — TOP near", anc, Geom::Vector3d.new(-120.mm, -200.mm, 250.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Brown contents" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("Brown (1000L tote)
recycle — BOTTOM near", anc, Geom::Vector3d.new(-120.mm, -200.mm, 250.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Waste contents" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("Waste (1000L tote)
BOTTOM far", anc, Geom::Vector3d.new(120.mm, 200.mm, 250.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Blue #2 contents" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)
  txt = entities.add_text("Blue #2 (1000L tote, ~800L)
clean supply — TOP far", anc, Geom::Vector3d.new(120.mm, 200.mm, 250.mm))
  txt.layer = model.layers["Labels"] rescue nil
end
anc = Geom::Point3d.new(4649.mm, 60.mm, 1900.mm)
txt = entities.add_text("FILM PLANE RIGHT RAIL X=4649
(everything X<4649 is swept:
Yd 100..2262, full height —
NO equipment here)", anc, Geom::Vector3d.new(-700.mm, -400.mm, 250.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4674.mm, 1046.mm, 2336.mm)
txt = entities.add_text("DIRECT STACK — cage-on-cage
(52mm headroom, no deck)", anc, Geom::Vector3d.new(250.mm, -150.mm, 250.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4674.mm, 1181.mm, 1100.mm)
txt = entities.add_text("FORWARD PANEL at corridor mouth
(equipment X>=4674, reach-in
service from the walkway)", anc, Geom::Vector3d.new(-350.mm, 0.mm, 300.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4329.mm, 200.mm, 130.mm)
txt = entities.add_text("RIGHT WALKWAY — carried off
the frame FRONT BAY", anc, Geom::Vector3d.new(-300.mm, -200.mm, 400.mm))
txt.layer = model.layers["Labels"] rescue nil

# ── In-model © + license credit (default layer → shown in every scene) ──
lbb = model.bounds
lanc = Geom::Point3d.new(lbb.min.x, lbb.min.y - 400.mm, lbb.min.z)
entities.add_text("© 2026 Alvin Richards
Licensed under GNU AGPLv3
alvinr.github.io/tbs", lanc)

model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags ──
keep_tags = ["Context", "IBC Tanks", "IBC Frame", "Panel", "Walkway", "Pipes", "Labels"]
default_layer = model.layers[0]
model.layers.to_a.each { |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}

# ── Scenes — one shared iso camera, framed on geometry (Labels hidden for extents) ──
model.layers.each { |l| l.visible = (l.name != "Labels") }
bb = model.bounds
ctr = bb.center
dir = Geom::Vector3d.new(0.72, -0.7, 0.5); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.5)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

[["IBC Tanks", ["IBC Tanks"]], ["IBC Frame + Walkway", ["IBC Frame", "Walkway"]], ["Forward Panel", ["Panel", "IBC Frame"]], ["Plumbing", ["Pipes", "IBC Tanks"]], ["Combined", ["Context", "IBC Tanks", "IBC Frame", "Panel", "Walkway", "Pipes"]], ["Labeled", ["Context", "IBC Tanks", "IBC Frame", "Panel", "Walkway", "Pipes", "Labels"]]].each { |name, tags|
  model.layers.each { |l| l.visible = (l == default_layer || l.name == "Context" || tags.include?(l.name)) }
  page = model.pages.add(name)
  page.use_camera = true
}
model.layers.each { |l| l.visible = true }

model.commit_operation
{ success: true, model: "IBC v2 study",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
