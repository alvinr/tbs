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
  model.layers.add("Context") unless model.layers["Context"]
  model.layers.add("IBC Tanks") unless model.layers["IBC Tanks"]
  model.layers.add("IBC Frame") unless model.layers["IBC Frame"]
  model.layers.add("Plumbing & Panel") unless model.layers["Plumbing & Panel"]

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
  face.pushpull(822.mm)
  mat = model.materials["IBC Brown (developer) bottle"] || model.materials.add("IBC Brown (developer) bottle")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 0.25
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
  face.pushpull(822.mm)
  mat = model.materials["IBC Waste bottle"] || model.materials.add("IBC Waste bottle")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 0.25
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
  mat.alpha = 0.25
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

  # Panel Frame Upright
  grp = ents.add_group
  grp.name = "Panel Frame Upright"
  face = grp.entities.add_face([5258.5.mm,1046.mm,1010.mm], [5308.5.mm,1046.mm,1010.mm], [5308.5.mm,1096.mm,1010.mm], [5258.5.mm,1096.mm,1010.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1250.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Panel Frame Upright
  grp = ents.add_group
  grp.name = "Panel Frame Upright"
  face = grp.entities.add_face([5258.5.mm,1266.mm,1010.mm], [5308.5.mm,1266.mm,1010.mm], [5308.5.mm,1316.mm,1010.mm], [5258.5.mm,1316.mm,1010.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1250.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Panel Frame Top Rail
  grp = ents.add_group
  grp.name = "Panel Frame Top Rail"
  face = grp.entities.add_face([5258.5.mm,1046.mm,2210.mm], [5308.5.mm,1046.mm,2210.mm], [5308.5.mm,1316.mm,2210.mm], [5258.5.mm,1316.mm,2210.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Panel Frame Floor Beam
  grp = ents.add_group
  grp.name = "Panel Frame Floor Beam"
  face = grp.entities.add_face([5258.5.mm,1046.mm,0.mm], [5308.5.mm,1046.mm,0.mm], [5308.5.mm,1316.mm,0.mm], [5258.5.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Flange Plate
  grp = ents.add_group
  grp.name = "Foot Flange Plate"
  face = grp.entities.add_face([4684.mm,996.mm,-12.mm], [4834.mm,996.mm,-12.mm], [4834.mm,1146.mm,-12.mm], [4684.mm,1146.mm,-12.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4709.mm,1021.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4709.mm,1121.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4809.mm,1021.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4809.mm,1121.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Flange Plate
  grp = ents.add_group
  grp.name = "Foot Flange Plate"
  face = grp.entities.add_face([4684.mm,1216.mm,-12.mm], [4834.mm,1216.mm,-12.mm], [4834.mm,1366.mm,-12.mm], [4684.mm,1366.mm,-12.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4709.mm,1241.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4709.mm,1341.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4809.mm,1241.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4809.mm,1341.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Flange Plate
  grp = ents.add_group
  grp.name = "Foot Flange Plate"
  face = grp.entities.add_face([5208.5.mm,996.mm,-12.mm], [5358.5.mm,996.mm,-12.mm], [5358.5.mm,1146.mm,-12.mm], [5208.5.mm,1146.mm,-12.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5233.5.mm,1021.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5233.5.mm,1121.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5333.5.mm,1021.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5333.5.mm,1121.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Flange Plate
  grp = ents.add_group
  grp.name = "Foot Flange Plate"
  face = grp.entities.add_face([5208.5.mm,1216.mm,-12.mm], [5358.5.mm,1216.mm,-12.mm], [5358.5.mm,1366.mm,-12.mm], [5208.5.mm,1366.mm,-12.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5233.5.mm,1241.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5233.5.mm,1341.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5333.5.mm,1241.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5333.5.mm,1341.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Flange Plate
  grp = ents.add_group
  grp.name = "Foot Flange Plate"
  face = grp.entities.add_face([5733.mm,996.mm,-12.mm], [5883.mm,996.mm,-12.mm], [5883.mm,1146.mm,-12.mm], [5733.mm,1146.mm,-12.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5758.mm,1021.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5758.mm,1121.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5858.mm,1021.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5858.mm,1121.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Flange Plate
  grp = ents.add_group
  grp.name = "Foot Flange Plate"
  face = grp.entities.add_face([5733.mm,1216.mm,-12.mm], [5883.mm,1216.mm,-12.mm], [5883.mm,1366.mm,-12.mm], [5733.mm,1366.mm,-12.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5758.mm,1241.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5758.mm,1341.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5858.mm,1241.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Foot Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Foot Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5858.mm,1341.mm,-12.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(20.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Plate
  grp = ents.add_group
  grp.name = "Wall Bracket Plate"
  face = grp.entities.add_face([4684.mm,0.mm,750.mm], [4834.mm,0.mm,750.mm], [4834.mm,8.mm,750.mm], [4684.mm,8.mm,750.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(270.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Seat
  grp = ents.add_group
  grp.name = "Wall Bracket Seat"
  face = grp.entities.add_face([4724.mm,0.mm,950.mm], [4794.mm,0.mm,950.mm], [4794.mm,110.mm,950.mm], [4724.mm,110.mm,950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Gusset
  grp = ents.add_group
  grp.name = "Wall Bracket Gusset"
  ge = grp.entities
  f = ge.add_face([4755.mm,110.mm,950.mm], [4755.mm,0.mm,950.mm], [4755.mm,0.mm,750.mm])
  f.pushpull(8.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4704.mm,-10.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4704.mm,-10.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4814.mm,-10.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4814.mm,-10.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Plate
  grp = ents.add_group
  grp.name = "Wall Bracket Plate"
  face = grp.entities.add_face([4684.mm,2354.mm,750.mm], [4834.mm,2354.mm,750.mm], [4834.mm,2362.mm,750.mm], [4684.mm,2362.mm,750.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(270.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Seat
  grp = ents.add_group
  grp.name = "Wall Bracket Seat"
  face = grp.entities.add_face([4724.mm,2252.mm,950.mm], [4794.mm,2252.mm,950.mm], [4794.mm,2362.mm,950.mm], [4724.mm,2362.mm,950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Gusset
  grp = ents.add_group
  grp.name = "Wall Bracket Gusset"
  ge = grp.entities
  f = ge.add_face([4755.mm,2252.mm,950.mm], [4755.mm,2362.mm,950.mm], [4755.mm,2362.mm,750.mm])
  f.pushpull(8.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4704.mm,2344.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4704.mm,2344.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4814.mm,2344.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([4814.mm,2344.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Plate
  grp = ents.add_group
  grp.name = "Wall Bracket Plate"
  face = grp.entities.add_face([5208.5.mm,0.mm,750.mm], [5358.5.mm,0.mm,750.mm], [5358.5.mm,8.mm,750.mm], [5208.5.mm,8.mm,750.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(270.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Seat
  grp = ents.add_group
  grp.name = "Wall Bracket Seat"
  face = grp.entities.add_face([5248.5.mm,0.mm,950.mm], [5318.5.mm,0.mm,950.mm], [5318.5.mm,110.mm,950.mm], [5248.5.mm,110.mm,950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Gusset
  grp = ents.add_group
  grp.name = "Wall Bracket Gusset"
  ge = grp.entities
  f = ge.add_face([5279.5.mm,110.mm,950.mm], [5279.5.mm,0.mm,950.mm], [5279.5.mm,0.mm,750.mm])
  f.pushpull(8.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5228.5.mm,-10.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5228.5.mm,-10.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5338.5.mm,-10.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5338.5.mm,-10.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Plate
  grp = ents.add_group
  grp.name = "Wall Bracket Plate"
  face = grp.entities.add_face([5208.5.mm,2354.mm,750.mm], [5358.5.mm,2354.mm,750.mm], [5358.5.mm,2362.mm,750.mm], [5208.5.mm,2362.mm,750.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(270.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Seat
  grp = ents.add_group
  grp.name = "Wall Bracket Seat"
  face = grp.entities.add_face([5248.5.mm,2252.mm,950.mm], [5318.5.mm,2252.mm,950.mm], [5318.5.mm,2362.mm,950.mm], [5248.5.mm,2362.mm,950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Gusset
  grp = ents.add_group
  grp.name = "Wall Bracket Gusset"
  ge = grp.entities
  f = ge.add_face([5279.5.mm,2252.mm,950.mm], [5279.5.mm,2362.mm,950.mm], [5279.5.mm,2362.mm,750.mm])
  f.pushpull(8.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5228.5.mm,2344.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5228.5.mm,2344.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5338.5.mm,2344.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5338.5.mm,2344.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Plate
  grp = ents.add_group
  grp.name = "Wall Bracket Plate"
  face = grp.entities.add_face([5733.mm,0.mm,750.mm], [5883.mm,0.mm,750.mm], [5883.mm,8.mm,750.mm], [5733.mm,8.mm,750.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(270.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Seat
  grp = ents.add_group
  grp.name = "Wall Bracket Seat"
  face = grp.entities.add_face([5773.mm,0.mm,950.mm], [5843.mm,0.mm,950.mm], [5843.mm,110.mm,950.mm], [5773.mm,110.mm,950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Gusset
  grp = ents.add_group
  grp.name = "Wall Bracket Gusset"
  ge = grp.entities
  f = ge.add_face([5804.mm,110.mm,950.mm], [5804.mm,0.mm,950.mm], [5804.mm,0.mm,750.mm])
  f.pushpull(8.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5753.mm,-10.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5753.mm,-10.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5863.mm,-10.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5863.mm,-10.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Plate
  grp = ents.add_group
  grp.name = "Wall Bracket Plate"
  face = grp.entities.add_face([5733.mm,2354.mm,750.mm], [5883.mm,2354.mm,750.mm], [5883.mm,2362.mm,750.mm], [5733.mm,2362.mm,750.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(270.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Seat
  grp = ents.add_group
  grp.name = "Wall Bracket Seat"
  face = grp.entities.add_face([5773.mm,2252.mm,950.mm], [5843.mm,2252.mm,950.mm], [5843.mm,2362.mm,950.mm], [5773.mm,2362.mm,950.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall Bracket Gusset
  grp = ents.add_group
  grp.name = "Wall Bracket Gusset"
  ge = grp.entities
  f = ge.add_face([5804.mm,2252.mm,950.mm], [5804.mm,2362.mm,950.mm], [5804.mm,2362.mm,750.mm])
  f.pushpull(8.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5753.mm,2344.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5753.mm,2344.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5863.mm,2344.mm,790.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Bracket Anchor Bolt M12
  grp = ents.add_group
  grp.name = "Bracket Anchor Bolt M12"
  ge = grp.entities
  circle = ge.add_circle([5863.mm,2344.mm,975.mm], [0,1,0], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["Foot Anchor Bolt M12"] || model.materials.add("Foot Anchor Bolt M12")
  mat.color = Sketchup::Color.new(58, 58, 66)
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
  face = grp.entities.add_face([5240.mm,1046.mm,200.mm], [5258.mm,1046.mm,200.mm], [5258.mm,1316.mm,200.mm], [5240.mm,1316.mm,200.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2060.mm)
  mat = model.materials["Equipment Panel (ply)"] || model.materials.add("Equipment Panel (ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-01 (Blue)
  grp = ents.add_group
  grp.name = "Pump P-01 (Blue)"
  face = grp.entities.add_face([5140.mm,1045.5.mm,1320.mm], [5240.mm,1045.5.mm,1320.mm], [5240.mm,1172.5.mm,1320.mm], [5140.mm,1172.5.mm,1320.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-02 (Brown)
  grp = ents.add_group
  grp.name = "Pump P-02 (Brown)"
  face = grp.entities.add_face([5140.mm,1189.5.mm,1320.mm], [5240.mm,1189.5.mm,1320.mm], [5240.mm,1316.5.mm,1320.mm], [5140.mm,1316.5.mm,1320.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-04 (Tray drain)
  grp = ents.add_group
  grp.name = "Pump P-04 (Tray drain)"
  face = grp.entities.add_face([5140.mm,1045.5.mm,1578.mm], [5240.mm,1045.5.mm,1578.mm], [5240.mm,1172.5.mm,1578.mm], [5140.mm,1172.5.mm,1578.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-03 (Waste evac)
  grp = ents.add_group
  grp.name = "Pump P-03 (Waste evac)"
  face = grp.entities.add_face([5140.mm,1189.5.mm,1578.mm], [5240.mm,1189.5.mm,1578.mm], [5240.mm,1316.5.mm,1578.mm], [5140.mm,1316.5.mm,1578.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(218.mm)
  mat = model.materials["Pump P-01 (Blue)"] || model.materials.add("Pump P-01 (Blue)")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-05 (Brown drain)
  grp = ents.add_group
  grp.name = "Pump P-05 (Brown drain)"
  face = grp.entities.add_face([5140.mm,1189.5.mm,1946.mm], [5240.mm,1189.5.mm,1946.mm], [5240.mm,1316.5.mm,1946.mm], [5140.mm,1316.5.mm,1946.mm])
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
  circle = ge.add_circle([5177.mm,1109.mm,1946.mm], [0,0,1], 63.5.mm, 24)
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
  circle = ge.add_circle([5175.mm,1181.mm,200.mm], [0,0,1], 65.mm, 24)
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
  circle = ge.add_circle([5175.mm,1181.mm,570.mm], [0,0,1], 65.mm, 24)
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
  circle = ge.add_circle([5175.mm,1181.mm,940.mm], [0,0,1], 65.mm, 24)
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
  face = grp.entities.add_face([5240.mm,1223.mm,200.mm], [5420.mm,1223.mm,200.mm], [5420.mm,1241.mm,200.mm], [5240.mm,1241.mm,200.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2020.mm)
  mat = model.materials["Equipment Panel (ply)"] || model.materials.add("Equipment Panel (ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Drain-riser spine flange (ply)
  grp = ents.add_group
  grp.name = "Drain-riser spine flange (ply)"
  face = grp.entities.add_face([5402.mm,1226.mm,200.mm], [5420.mm,1226.mm,200.mm], [5420.mm,1280.mm,200.mm], [5402.mm,1280.mm,200.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2020.mm)
  mat = model.materials["Equipment Panel (ply)"] || model.materials.add("Equipment Panel (ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Drain-riser spine top shelf (ply)
  grp = ents.add_group
  grp.name = "Drain-riser spine top shelf (ply)"
  face = grp.entities.add_face([5240.mm,1160.mm,2220.mm], [5460.mm,1160.mm,2220.mm], [5460.mm,1241.mm,2220.mm], [5240.mm,1241.mm,2220.mm])
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
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Riser pipe clamp
  grp = ents.add_group
  grp.name = "Riser pipe clamp"
  face = grp.entities.add_face([5324.mm,1241.mm,500.mm], [5356.mm,1241.mm,500.mm], [5356.mm,1271.mm,500.mm], [5324.mm,1271.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Riser pipe clamp
  grp = ents.add_group
  grp.name = "Riser pipe clamp"
  face = grp.entities.add_face([5324.mm,1241.mm,900.mm], [5356.mm,1241.mm,900.mm], [5356.mm,1271.mm,900.mm], [5324.mm,1271.mm,900.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Riser pipe clamp
  grp = ents.add_group
  grp.name = "Riser pipe clamp"
  face = grp.entities.add_face([5324.mm,1241.mm,1300.mm], [5356.mm,1241.mm,1300.mm], [5356.mm,1271.mm,1300.mm], [5324.mm,1271.mm,1300.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Riser pipe clamp
  grp = ents.add_group
  grp.name = "Riser pipe clamp"
  face = grp.entities.add_face([5384.mm,1241.mm,500.mm], [5416.mm,1241.mm,500.mm], [5416.mm,1271.mm,500.mm], [5384.mm,1271.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Riser pipe clamp
  grp = ents.add_group
  grp.name = "Riser pipe clamp"
  face = grp.entities.add_face([5384.mm,1241.mm,900.mm], [5416.mm,1241.mm,900.mm], [5416.mm,1271.mm,900.mm], [5384.mm,1271.mm,900.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Riser pipe clamp
  grp = ents.add_group
  grp.name = "Riser pipe clamp"
  face = grp.entities.add_face([5384.mm,1241.mm,1300.mm], [5416.mm,1241.mm,1300.mm], [5416.mm,1271.mm,1300.mm], [5384.mm,1271.mm,1300.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Riser pipe clamp
  grp = ents.add_group
  grp.name = "Riser pipe clamp"
  face = grp.entities.add_face([5384.mm,1241.mm,1700.mm], [5416.mm,1241.mm,1700.mm], [5416.mm,1271.mm,1700.mm], [5384.mm,1271.mm,1700.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
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
  vec = Geom::Vector3d.new(-485.mm, 0.mm, 0.mm)
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
  circle = ge.add_circle([5408.mm,1158.2.mm,2250.mm], vec, 16.200000000000003.mm, 16)
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
  circle = ge.add_circle([5408.mm,1181.mm,2250.mm], vec, 16.200000000000003.mm, 16)
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
  circle = ge.add_circle([5408.mm,1181.mm,2250.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([5408.mm,562.mm,2226.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5408.mm,562.mm,2250.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
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
  circle = ge.add_circle([5408.mm,538.mm,2226.mm], vec, 12.mm, 16)
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
  circle = ge.add_circle([5408.mm,1181.mm,2250.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([5408.mm,1800.mm,2226.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5408.mm,1800.mm,2250.mm], [0.000000,1.000000,0.000000], 12.mm, 16)
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
  circle = ge.add_circle([5408.mm,1824.mm,2226.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Fill Trunk"] || model.materials.add("Fill Trunk")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-05 → X3 (Brown drain-out)
  grp = ents.add_group
  grp.name = "P-05 → X3 (Brown drain-out)"
  ge = grp.entities
  vec = Geom::Vector3d.new(156.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5220.mm,1253.mm,1946.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([5376.mm,1253.mm,1922.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5376.mm,1253.mm,1946.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1498.mm)
  circle = ge.add_circle([5400.mm,1253.mm,1922.mm], vec, 12.mm, 16)
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
  vec = Geom::Vector3d.new(96.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5220.mm,1253.mm,1578.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([5316.mm,1253.mm,1554.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5316.mm,1253.mm,1578.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1330.mm)
  circle = ge.add_circle([5340.mm,1253.mm,1554.mm], vec, 12.mm, 16)
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

  # Blue Suction Manifold
  grp = ents.add_group
  grp.name = "Blue Suction Manifold"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 430.mm, 0.mm)
  circle = ge.add_circle([5533.5.mm,966.mm,1195.mm], vec, 12.mm, 16)
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
  circle = ge.add_circle([5533.5.mm,1158.2.mm,1195.mm], vec, 16.200000000000003.mm, 16)
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
  circle = ge.add_circle([5533.5.mm,1181.mm,1195.mm], vec, 16.200000000000003.mm, 16)
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
  vec = Geom::Vector3d.new(-329.5.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5533.5.mm,1181.mm,1195.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([5204.mm,1157.mm,1195.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5204.mm,1181.mm,1195.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
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
  circle = ge.add_circle([5180.mm,1157.mm,1195.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([5180.mm,1132.52.mm,1218.52.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 23.520000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5180.mm,1132.52.mm,1195.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
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
  circle = ge.add_circle([5180.mm,1109.mm,1218.52.mm], vec, 12.mm, 16)
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
  vec = Geom::Vector3d.new(-79.5.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5283.5.mm,1046.mm,185.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([5204.mm,1070.mm,185.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,-1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5204.mm,1046.mm,185.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 159.mm, 0.mm)
  circle = ge.add_circle([5180.mm,1070.mm,185.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([5180.mm,1229.mm,209.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5180.mm,1229.mm,185.mm], [0.000000,1.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1111.mm)
  circle = ge.add_circle([5180.mm,1253.mm,209.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-05 → X3 (Brown drain-out)"] || model.materials.add("P-05 → X3 (Brown drain-out)")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # Waste → P-03
  grp = ents.add_group
  grp.name = "Waste → P-03"
  ge = grp.entities
  vec = Geom::Vector3d.new(-39.5.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5283.5.mm,1316.mm,185.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([5244.mm,1292.mm,185.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5244.mm,1316.mm,185.mm], [-1.000000,0.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, -19.8900000000001.mm, 0.mm)
  circle = ge.add_circle([5220.mm,1292.mm,185.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([5220.mm,1272.11.mm,204.11.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 19.110000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5220.mm,1272.11.mm,185.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1373.8899999999999.mm)
  circle = ge.add_circle([5220.mm,1253.mm,204.11.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Sump → P-04
  grp = ents.add_group
  grp.name = "Tray Sump → P-04"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 101.mm)
  circle = ge.add_circle([4550.mm,80.mm,20.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([4574.mm,80.mm,121.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4550.mm,80.mm,121.mm], [0.000000,0.000000,1.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(23.460000000000036.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4574.mm,80.mm,145.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([4597.46.mm,80.mm,122.46.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 22.540000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4597.46.mm,80.mm,145.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -77.025.mm)
  circle = ge.add_circle([4620.mm,80.mm,122.46000000000001.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([4635.435.mm,80.mm,45.435.mm], [-1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 15.435000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4620.mm,80.mm,45.435.mm], [0.000000,0.000000,-1.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(8.19315000000006.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4635.435.mm,80.mm,30.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([4643.6281500000005.mm,87.87184999999981.mm,30.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 7.871849999999805.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4643.6281500000005.mm,80.mm,30.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 1069.1281500000002.mm, 0.mm)
  circle = ge.add_circle([4651.5.mm,87.87184999999981.mm,30.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([4675.5.mm,1157.mm,30.mm], [-1.000000,0.000000,0.000000], [0.000000,0.000000,-1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4651.5.mm,1157.mm,30.mm], [0.000000,1.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(520.5.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4675.5.mm,1181.mm,30.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([5196.mm,1157.mm,30.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,-1.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5196.mm,1181.mm,30.mm], [1.000000,0.000000,0.000000], 12.mm, 16)
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
  circle = ge.add_circle([5220.mm,1157.mm,30.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([5220.mm,1132.52.mm,53.52.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 23.520000000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5220.mm,1132.52.mm,30.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1524.48.mm)
  circle = ge.add_circle([5220.mm,1109.mm,53.519999999999996.mm], vec, 12.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["P-03 → X4 (Waste drain-out)"] || model.materials.add("P-03 → X4 (Waste drain-out)")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # Pump → Filters
  grp = ents.add_group
  grp.name = "Pump → Filters"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -620.mm)
  circle = ge.add_circle([5190.mm,1181.mm,1320.mm], vec, 12.mm, 16)
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
  circle = ge.add_circle([5190.mm,1181.mm,700.mm], vec, 12.mm, 16)
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
  arc = ge.add_arc([5166.mm,1181.mm,84.mm], [1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 24.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5190.mm,1181.mm,84.mm], [0.000000,0.000000,-1.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(-493.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5166.mm,1181.mm,60.mm], vec, 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, -1135.2.mm, 0.mm)
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
  arc = ge.add_arc([4649.mm,21.8.mm,50.199999999999996.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 9.800000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4649.mm,21.8.mm,60.mm], [0.000000,-1.000000,0.000000], 12.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -10.200000000000003.mm)
  circle = ge.add_circle([4649.mm,12.mm,50.2.mm], vec, 12.mm, 16)
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


model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags from earlier versions ──
keep_tags = ["Context", "IBC Tanks", "IBC Frame", "Plumbing & Panel"]
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

[["IBC Tanks", ["IBC Tanks"]], ["IBC Frame", ["IBC Frame"]], ["Plumbing & Panel", ["Plumbing & Panel"]], ["Combined", ["Context", "IBC Tanks", "IBC Frame", "Plumbing & Panel"]]].each { |name, tags|
  model.layers.each { |l| l.visible = (l == default_layer || l.name == "Context" || tags.include?(l.name)) }
  page = model.pages.add(name)
  page.use_camera = true
}
model.layers.each { |l| l.visible = true }

model.commit_operation
{ success: true, model: "IBC Stack",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
