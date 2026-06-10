model = Sketchup.active_model
model.start_operation("TBS-001 Right Cantilever Study", true)
entities = model.active_entities
opts = model.options["UnitsOptions"]; opts["LengthUnit"]=2; opts["LengthFormat"]=0; opts["LengthPrecision"]=1
to_erase = entities.to_a.select { |e| e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text) }
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each { |p| model.pages.erase(p) }

  model.layers.add("Context") unless model.layers["Context"]
  model.layers.add("IBC Frame") unless model.layers["IBC Frame"]
  model.layers.add("Tray + Spray") unless model.layers["Tray + Spray"]
  model.layers.add("Film Rail + Saddle") unless model.layers["Film Rail + Saddle"]
  model.layers.add("Cantilever Walkway") unless model.layers["Cantilever Walkway"]
  model.layers.add("Labels") unless model.layers["Labels"]

  # ═══ Container (ghost) ═══
  defn = model.definitions.add("Container (ghost)")
  ents = defn.entities
  # Floor (context)
  grp = ents.add_group
  grp.name = "Floor (context)"
  face = grp.entities.add_face([3900.mm,0.mm,-40.mm], [5893.mm,0.mm,-40.mm], [5893.mm,2362.mm,-40.mm], [3900.mm,2362.mm,-40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Floor (context)"] || model.materials.add("Floor (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.22
  grp.material = mat

  # Ceiling (context)
  grp = ents.add_group
  grp.name = "Ceiling (context)"
  face = grp.entities.add_face([3900.mm,0.mm,2388.mm], [5893.mm,0.mm,2388.mm], [5893.mm,2362.mm,2388.mm], [3900.mm,2362.mm,2388.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Ceiling (context)"] || model.materials.add("Ceiling (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.1
  grp.material = mat

  # Near wall (context)
  grp = ents.add_group
  grp.name = "Near wall (context)"
  face = grp.entities.add_face([3900.mm,-40.mm,0.mm], [5893.mm,-40.mm,0.mm], [5893.mm,0.mm,0.mm], [3900.mm,0.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Near wall (context)"] || model.materials.add("Near wall (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.14
  grp.material = mat

  # Far wall (context)
  grp = ents.add_group
  grp.name = "Far wall (context)"
  face = grp.entities.add_face([3900.mm,2362.mm,0.mm], [5893.mm,2362.mm,0.mm], [5893.mm,2402.mm,0.mm], [3900.mm,2402.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Near wall (context)"] || model.materials.add("Near wall (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.14
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Container (ghost)"
  inst.layer = model.layers["Context"]

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
  face.pushpull(1300.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Panel Frame Upright
  grp = ents.add_group
  grp.name = "Panel Frame Upright"
  face = grp.entities.add_face([5258.5.mm,1266.mm,1010.mm], [5308.5.mm,1266.mm,1010.mm], [5308.5.mm,1316.mm,1010.mm], [5258.5.mm,1316.mm,1010.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1300.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Panel Frame Top Rail
  grp = ents.add_group
  grp.name = "Panel Frame Top Rail"
  face = grp.entities.add_face([5258.5.mm,1046.mm,2260.mm], [5308.5.mm,1046.mm,2260.mm], [5308.5.mm,1316.mm,2260.mm], [5258.5.mm,1316.mm,2260.mm])
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
  face = grp.entities.add_face([4684.mm,996.mm,0.mm], [4834.mm,996.mm,0.mm], [4834.mm,1146.mm,0.mm], [4684.mm,1146.mm,0.mm])
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
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
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

  # Foot Flange Plate
  grp = ents.add_group
  grp.name = "Foot Flange Plate"
  face = grp.entities.add_face([5208.5.mm,996.mm,0.mm], [5358.5.mm,996.mm,0.mm], [5358.5.mm,1146.mm,0.mm], [5208.5.mm,1146.mm,0.mm])
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
  circle = ge.add_circle([5233.5.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5233.5.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5333.5.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5333.5.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
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
  face = grp.entities.add_face([5208.5.mm,1216.mm,0.mm], [5358.5.mm,1216.mm,0.mm], [5358.5.mm,1366.mm,0.mm], [5208.5.mm,1366.mm,0.mm])
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
  circle = ge.add_circle([5233.5.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5233.5.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5333.5.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5333.5.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
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
  face = grp.entities.add_face([5733.mm,996.mm,0.mm], [5883.mm,996.mm,0.mm], [5883.mm,1146.mm,0.mm], [5733.mm,1146.mm,0.mm])
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
  circle = ge.add_circle([5758.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5758.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5858.mm,1021.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5858.mm,1121.mm,0.mm], [0,0,1], 7.mm, 24)
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
  face = grp.entities.add_face([5733.mm,1216.mm,0.mm], [5883.mm,1216.mm,0.mm], [5883.mm,1366.mm,0.mm], [5733.mm,1366.mm,0.mm])
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
  circle = ge.add_circle([5758.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5758.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5858.mm,1241.mm,0.mm], [0,0,1], 7.mm, 24)
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
  circle = ge.add_circle([5858.mm,1341.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
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

  # ═══ Tray + Spray bar ═══
  defn = model.definitions.add("Tray + Spray bar")
  ents = defn.entities
  # Processing tray (right end)
  grp = ents.add_group
  grp.name = "Processing tray (right end)"
  face = grp.entities.add_face([3900.mm,80.mm,0.mm], [4629.mm,80.mm,0.mm], [4629.mm,2280.mm,0.mm], [3900.mm,2280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Processing tray (right end)"] || model.materials.add("Processing tray (right end)")
  mat.color = Sketchup::Color.new(232, 245, 233)
  mat.alpha = 0.5
  grp.material = mat

  # Spray bar beam (Z20-60, sweeps Yd)
  grp = ents.add_group
  grp.name = "Spray bar beam (Z20-60, sweeps Yd)"
  face = grp.entities.add_face([3900.mm,1160.mm,20.mm], [4629.mm,1160.mm,20.mm], [4629.mm,1200.mm,20.mm], [3900.mm,1200.mm,20.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Spray bar beam (Z20-60, sweeps Yd)"] || model.materials.add("Spray bar beam (Z20-60, sweeps Yd)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.6
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Tray + Spray bar"
  inst.layer = model.layers["Tray + Spray"]

  # ═══ Film Rail + Saddles ═══
  defn = model.definitions.add("Film Rail + Saddles")
  ents = defn.entities
  # FP Rail TR (X4649)
  grp = ents.add_group
  grp.name = "FP Rail TR (X4649)"
  face = grp.entities.add_face([4649.mm,0.mm,2288.mm], [4689.mm,0.mm,2288.mm], [4689.mm,2362.mm,2288.mm], [4649.mm,2362.mm,2288.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["FP Rail TR (X4649)"] || model.materials.add("FP Rail TR (X4649)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.85
  grp.material = mat

  # FP Rail BR (X4649)
  grp = ents.add_group
  grp.name = "FP Rail BR (X4649)"
  face = grp.entities.add_face([4649.mm,0.mm,150.mm], [4689.mm,0.mm,150.mm], [4689.mm,2362.mm,150.mm], [4649.mm,2362.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["FP Rail TR (X4649)"] || model.materials.add("FP Rail TR (X4649)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.85
  grp.material = mat

  # Saddle back-plate TR near
  grp = ents.add_group
  grp.name = "Saddle back-plate TR near"
  face = grp.entities.add_face([4574.mm,0.mm,2213.mm], [4724.mm,0.mm,2213.mm], [4724.mm,8.mm,2213.mm], [4574.mm,8.mm,2213.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle OUTSIDE plate TR near
  grp = ents.add_group
  grp.name = "Saddle OUTSIDE plate TR near"
  face = grp.entities.add_face([4574.mm,-48.mm,2213.mm], [4724.mm,-48.mm,2213.mm], [4724.mm,-40.mm,2213.mm], [4574.mm,-40.mm,2213.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle seat TR near
  grp = ents.add_group
  grp.name = "Saddle seat TR near"
  face = grp.entities.add_face([4625.mm,0.mm,2278.mm], [4673.mm,0.mm,2278.mm], [4673.mm,110.mm,2278.mm], [4625.mm,110.mm,2278.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle gusset TR near
  grp = ents.add_group
  grp.name = "Saddle gusset TR near"
  ge = grp.entities
  f = ge.add_face([4649.mm,110.mm,2278.mm], [4649.mm,0.mm,2278.mm], [4649.mm,0.mm,2158.mm])
  f.pushpull(8.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TR near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR near"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,-48.mm,2238.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TR near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR near"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,-48.mm,2338.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TR near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR near"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,-48.mm,2238.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TR near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR near"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,-48.mm,2338.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail fixing bolt TR near
  grp = ents.add_group
  grp.name = "Rail fixing bolt TR near"
  ge = grp.entities
  circle = ge.add_circle([4649.mm,25.mm,2288.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail fixing bolt TR near
  grp = ents.add_group
  grp.name = "Rail fixing bolt TR near"
  ge = grp.entities
  circle = ge.add_circle([4649.mm,85.mm,2288.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle back-plate TR far
  grp = ents.add_group
  grp.name = "Saddle back-plate TR far"
  face = grp.entities.add_face([4574.mm,2354.mm,2213.mm], [4724.mm,2354.mm,2213.mm], [4724.mm,2362.mm,2213.mm], [4574.mm,2362.mm,2213.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle OUTSIDE plate TR far
  grp = ents.add_group
  grp.name = "Saddle OUTSIDE plate TR far"
  face = grp.entities.add_face([4574.mm,2402.mm,2213.mm], [4724.mm,2402.mm,2213.mm], [4724.mm,2410.mm,2213.mm], [4574.mm,2410.mm,2213.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle seat TR far
  grp = ents.add_group
  grp.name = "Saddle seat TR far"
  face = grp.entities.add_face([4625.mm,2252.mm,2278.mm], [4673.mm,2252.mm,2278.mm], [4673.mm,2362.mm,2278.mm], [4625.mm,2362.mm,2278.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle gusset TR far
  grp = ents.add_group
  grp.name = "Saddle gusset TR far"
  ge = grp.entities
  f = ge.add_face([4649.mm,2252.mm,2278.mm], [4649.mm,2362.mm,2278.mm], [4649.mm,2362.mm,2158.mm])
  f.pushpull(8.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TR far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR far"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,2354.mm,2238.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TR far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR far"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,2354.mm,2338.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TR far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR far"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,2354.mm,2238.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 TR far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR far"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,2354.mm,2338.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail fixing bolt TR far
  grp = ents.add_group
  grp.name = "Rail fixing bolt TR far"
  ge = grp.entities
  circle = ge.add_circle([4649.mm,2277.mm,2288.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail fixing bolt TR far
  grp = ents.add_group
  grp.name = "Rail fixing bolt TR far"
  ge = grp.entities
  circle = ge.add_circle([4649.mm,2337.mm,2288.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle back-plate BR near
  grp = ents.add_group
  grp.name = "Saddle back-plate BR near"
  face = grp.entities.add_face([4574.mm,0.mm,75.mm], [4724.mm,0.mm,75.mm], [4724.mm,8.mm,75.mm], [4574.mm,8.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle OUTSIDE plate BR near
  grp = ents.add_group
  grp.name = "Saddle OUTSIDE plate BR near"
  face = grp.entities.add_face([4574.mm,-48.mm,75.mm], [4724.mm,-48.mm,75.mm], [4724.mm,-40.mm,75.mm], [4574.mm,-40.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle seat BR near
  grp = ents.add_group
  grp.name = "Saddle seat BR near"
  face = grp.entities.add_face([4625.mm,0.mm,140.mm], [4673.mm,0.mm,140.mm], [4673.mm,110.mm,140.mm], [4625.mm,110.mm,140.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle gusset BR near
  grp = ents.add_group
  grp.name = "Saddle gusset BR near"
  ge = grp.entities
  f = ge.add_face([4649.mm,110.mm,140.mm], [4649.mm,0.mm,140.mm], [4649.mm,0.mm,20.mm])
  f.pushpull(8.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BR near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BR near"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,-48.mm,100.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BR near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BR near"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,-48.mm,200.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BR near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BR near"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,-48.mm,100.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BR near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BR near"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,-48.mm,200.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail fixing bolt BR near
  grp = ents.add_group
  grp.name = "Rail fixing bolt BR near"
  ge = grp.entities
  circle = ge.add_circle([4649.mm,25.mm,150.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail fixing bolt BR near
  grp = ents.add_group
  grp.name = "Rail fixing bolt BR near"
  ge = grp.entities
  circle = ge.add_circle([4649.mm,85.mm,150.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle back-plate BR far
  grp = ents.add_group
  grp.name = "Saddle back-plate BR far"
  face = grp.entities.add_face([4574.mm,2354.mm,75.mm], [4724.mm,2354.mm,75.mm], [4724.mm,2362.mm,75.mm], [4574.mm,2362.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle OUTSIDE plate BR far
  grp = ents.add_group
  grp.name = "Saddle OUTSIDE plate BR far"
  face = grp.entities.add_face([4574.mm,2402.mm,75.mm], [4724.mm,2402.mm,75.mm], [4724.mm,2410.mm,75.mm], [4574.mm,2410.mm,75.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle seat BR far
  grp = ents.add_group
  grp.name = "Saddle seat BR far"
  face = grp.entities.add_face([4625.mm,2252.mm,140.mm], [4673.mm,2252.mm,140.mm], [4673.mm,2362.mm,140.mm], [4625.mm,2362.mm,140.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle gusset BR far
  grp = ents.add_group
  grp.name = "Saddle gusset BR far"
  ge = grp.entities
  f = ge.add_face([4649.mm,2252.mm,140.mm], [4649.mm,2362.mm,140.mm], [4649.mm,2362.mm,20.mm])
  f.pushpull(8.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BR far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BR far"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,2354.mm,100.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BR far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BR far"
  ge = grp.entities
  circle = ge.add_circle([4599.mm,2354.mm,200.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BR far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BR far"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,2354.mm,100.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Saddle wall bolt M12 BR far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BR far"
  ge = grp.entities
  circle = ge.add_circle([4699.mm,2354.mm,200.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail fixing bolt BR far
  grp = ents.add_group
  grp.name = "Rail fixing bolt BR far"
  ge = grp.entities
  circle = ge.add_circle([4649.mm,2277.mm,150.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Rail fixing bolt BR far
  grp = ents.add_group
  grp.name = "Rail fixing bolt BR far"
  ge = grp.entities
  circle = ge.add_circle([4649.mm,2337.mm,150.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Film plane (right edge, ghost)
  grp = ents.add_group
  grp.name = "Film plane (right edge, ghost)"
  face = grp.entities.add_face([4329.mm,2262.mm,150.mm], [4649.mm,2262.mm,150.mm], [4649.mm,2278.mm,150.mm], [4329.mm,2278.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2138.mm)
  mat = model.materials["Film plane (right edge, ghost)"] || model.materials.add("Film plane (right edge, ghost)")
  mat.color = Sketchup::Color.new(32, 96, 160)
  mat.alpha = 0.18
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Film Rail + Saddles"
  inst.layer = model.layers["Film Rail + Saddle"]

  # ═══ Cantilever Right Walkway ═══
  defn = model.definitions.add("Cantilever Right Walkway")
  ents = defn.entities
  # Cantilever arm (off IBC upright) Yd1046
  grp = ents.add_group
  grp.name = "Cantilever arm (off IBC upright) Yd1046"
  face = grp.entities.add_face([4329.mm,1046.mm,70.mm], [4734.mm,1046.mm,70.mm], [4734.mm,1086.mm,70.mm], [4329.mm,1086.mm,70.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(45.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Upright clamp plate Yd1046 Y1038
  grp = ents.add_group
  grp.name = "Upright clamp plate Yd1046 Y1038"
  face = grp.entities.add_face([4730.mm,1038.mm,45.mm], [4788.mm,1038.mm,45.mm], [4788.mm,1046.mm,45.mm], [4730.mm,1046.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Upright clamp plate Yd1046 Y1086
  grp = ents.add_group
  grp.name = "Upright clamp plate Yd1046 Y1086"
  face = grp.entities.add_face([4730.mm,1086.mm,45.mm], [4788.mm,1086.mm,45.mm], [4788.mm,1094.mm,45.mm], [4730.mm,1094.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Upright bolt M12 Yd1046 Z76
  grp = ents.add_group
  grp.name = "Upright bolt M12 Yd1046 Z76"
  ge = grp.entities
  circle = ge.add_circle([4759.mm,1034.mm,76.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(64.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Upright bolt M12 Yd1046 Z133
  grp = ents.add_group
  grp.name = "Upright bolt M12 Yd1046 Z133"
  ge = grp.entities
  circle = ge.add_circle([4759.mm,1034.mm,133.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(64.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Cantilever arm (off IBC upright) Yd1266
  grp = ents.add_group
  grp.name = "Cantilever arm (off IBC upright) Yd1266"
  face = grp.entities.add_face([4329.mm,1266.mm,70.mm], [4734.mm,1266.mm,70.mm], [4734.mm,1306.mm,70.mm], [4329.mm,1306.mm,70.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(45.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Upright clamp plate Yd1266 Y1258
  grp = ents.add_group
  grp.name = "Upright clamp plate Yd1266 Y1258"
  face = grp.entities.add_face([4730.mm,1258.mm,45.mm], [4788.mm,1258.mm,45.mm], [4788.mm,1266.mm,45.mm], [4730.mm,1266.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Upright clamp plate Yd1266 Y1306
  grp = ents.add_group
  grp.name = "Upright clamp plate Yd1266 Y1306"
  face = grp.entities.add_face([4730.mm,1306.mm,45.mm], [4788.mm,1306.mm,45.mm], [4788.mm,1314.mm,45.mm], [4730.mm,1314.mm,45.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Upright bolt M12 Yd1266 Z76
  grp = ents.add_group
  grp.name = "Upright bolt M12 Yd1266 Z76"
  ge = grp.entities
  circle = ge.add_circle([4759.mm,1254.mm,76.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(64.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Upright bolt M12 Yd1266 Z133
  grp = ents.add_group
  grp.name = "Upright bolt M12 Yd1266 Z133"
  ge = grp.entities
  circle = ge.add_circle([4759.mm,1254.mm,133.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(64.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall ledger (near wall)
  grp = ents.add_group
  grp.name = "Wall ledger (near wall)"
  face = grp.entities.add_face([4329.mm,0.mm,70.mm], [4629.mm,0.mm,70.mm], [4629.mm,40.mm,70.mm], [4329.mm,40.mm,70.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(45.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall bracket plate (near wall) X4389
  grp = ents.add_group
  grp.name = "Wall bracket plate (near wall) X4389"
  face = grp.entities.add_face([4349.mm,0.mm,52.mm], [4429.mm,0.mm,52.mm], [4429.mm,8.mm,52.mm], [4349.mm,8.mm,52.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(81.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall ext. plate (near wall) X4389
  grp = ents.add_group
  grp.name = "Wall ext. plate (near wall) X4389"
  face = grp.entities.add_face([4349.mm,-48.mm,52.mm], [4429.mm,-48.mm,52.mm], [4429.mm,-40.mm,52.mm], [4349.mm,-40.mm,52.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(81.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall bolt (near wall) X4389 Z70
  grp = ents.add_group
  grp.name = "Wall bolt (near wall) X4389 Z70"
  ge = grp.entities
  circle = ge.add_circle([4389.mm,-48.mm,70.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall bolt (near wall) X4389 Z123
  grp = ents.add_group
  grp.name = "Wall bolt (near wall) X4389 Z123"
  ge = grp.entities
  circle = ge.add_circle([4389.mm,-48.mm,123.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall bracket plate (near wall) X4569
  grp = ents.add_group
  grp.name = "Wall bracket plate (near wall) X4569"
  face = grp.entities.add_face([4529.mm,0.mm,52.mm], [4609.mm,0.mm,52.mm], [4609.mm,8.mm,52.mm], [4529.mm,8.mm,52.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(81.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall ext. plate (near wall) X4569
  grp = ents.add_group
  grp.name = "Wall ext. plate (near wall) X4569"
  face = grp.entities.add_face([4529.mm,-48.mm,52.mm], [4609.mm,-48.mm,52.mm], [4609.mm,-40.mm,52.mm], [4529.mm,-40.mm,52.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(81.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall bolt (near wall) X4569 Z70
  grp = ents.add_group
  grp.name = "Wall bolt (near wall) X4569 Z70"
  ge = grp.entities
  circle = ge.add_circle([4569.mm,-48.mm,70.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall bolt (near wall) X4569 Z123
  grp = ents.add_group
  grp.name = "Wall bolt (near wall) X4569 Z123"
  ge = grp.entities
  circle = ge.add_circle([4569.mm,-48.mm,123.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall ledger (far wall)
  grp = ents.add_group
  grp.name = "Wall ledger (far wall)"
  face = grp.entities.add_face([4329.mm,2322.mm,70.mm], [4629.mm,2322.mm,70.mm], [4629.mm,2362.mm,70.mm], [4329.mm,2362.mm,70.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(45.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall bracket plate (far wall) X4389
  grp = ents.add_group
  grp.name = "Wall bracket plate (far wall) X4389"
  face = grp.entities.add_face([4349.mm,2354.mm,52.mm], [4429.mm,2354.mm,52.mm], [4429.mm,2362.mm,52.mm], [4349.mm,2362.mm,52.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(81.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall ext. plate (far wall) X4389
  grp = ents.add_group
  grp.name = "Wall ext. plate (far wall) X4389"
  face = grp.entities.add_face([4349.mm,2402.mm,52.mm], [4429.mm,2402.mm,52.mm], [4429.mm,2410.mm,52.mm], [4349.mm,2410.mm,52.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(81.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall bolt (far wall) X4389 Z70
  grp = ents.add_group
  grp.name = "Wall bolt (far wall) X4389 Z70"
  ge = grp.entities
  circle = ge.add_circle([4389.mm,2354.mm,70.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall bolt (far wall) X4389 Z123
  grp = ents.add_group
  grp.name = "Wall bolt (far wall) X4389 Z123"
  ge = grp.entities
  circle = ge.add_circle([4389.mm,2354.mm,123.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall bracket plate (far wall) X4569
  grp = ents.add_group
  grp.name = "Wall bracket plate (far wall) X4569"
  face = grp.entities.add_face([4529.mm,2354.mm,52.mm], [4609.mm,2354.mm,52.mm], [4609.mm,2362.mm,52.mm], [4529.mm,2362.mm,52.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(81.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall ext. plate (far wall) X4569
  grp = ents.add_group
  grp.name = "Wall ext. plate (far wall) X4569"
  face = grp.entities.add_face([4529.mm,2402.mm,52.mm], [4609.mm,2402.mm,52.mm], [4609.mm,2410.mm,52.mm], [4529.mm,2410.mm,52.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(81.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall bolt (far wall) X4569 Z70
  grp = ents.add_group
  grp.name = "Wall bolt (far wall) X4569 Z70"
  ge = grp.entities
  circle = ge.add_circle([4569.mm,2354.mm,70.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Wall bolt (far wall) X4569 Z123
  grp = ents.add_group
  grp.name = "Wall bolt (far wall) X4569 Z123"
  ge = grp.entities
  circle = ge.add_circle([4569.mm,2354.mm,123.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right bearer X4329
  grp = ents.add_group
  grp.name = "Right bearer X4329"
  face = grp.entities.add_face([4329.mm,0.mm,80.mm], [4369.mm,0.mm,80.mm], [4369.mm,2362.mm,80.mm], [4329.mm,2362.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(35.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right bearer X4589
  grp = ents.add_group
  grp.name = "Right bearer X4589"
  face = grp.entities.add_face([4589.mm,0.mm,80.mm], [4629.mm,0.mm,80.mm], [4629.mm,2362.mm,80.mm], [4589.mm,2362.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(35.mm)
  mat = model.materials["Rack Upright"] || model.materials.add("Rack Upright")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Right walkway grate (cantilevered — NO ceiling rods)
  grp = ents.add_group
  grp.name = "Right walkway grate (cantilevered — NO ceiling rods)"
  face = grp.entities.add_face([4329.mm,0.mm,115.mm], [4629.mm,0.mm,115.mm], [4629.mm,2362.mm,115.mm], [4329.mm,2362.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Right walkway grate (cantilevered — NO ceiling rods)"] || model.materials.add("Right walkway grate (cantilevered — NO ceiling rods)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Cantilever Right Walkway"
  inst.layer = model.layers["Cantilever Walkway"]


anc = Geom::Point3d.new(4734.mm, 1046.mm, 900.mm)
txt = entities.add_text("IBC CORRIDOR UPRIGHT (X4734)
← INNER arms U-clamp here (2× M12)", anc, Geom::Vector3d.new(400.mm, -350.mm, 600.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4531.5.mm, 1046.mm, 115.mm)
txt = entities.add_text("INNER CANTILEVER ARM ×2
off the IBC corridor uprights", anc, Geom::Vector3d.new(-300.mm, -650.mm, 650.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4449.mm, 40.mm, 115.mm)
txt = entities.add_text("NEAR-WALL LEDGER
through-bolted to the wall (int+ext plate)", anc, Geom::Vector3d.new(-250.mm, -650.mm, 700.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4449.mm, 2322.mm, 115.mm)
txt = entities.add_text("FAR-WALL LEDGER
through-bolted to the wall", anc, Geom::Vector3d.new(-250.mm, 650.mm, 700.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4479.mm, 600.mm, 130.mm)
txt = entities.add_text("RIGHT WALKWAY GRATE
(no ceiling rods)", anc, Geom::Vector3d.new(-250.mm, -700.mm, 800.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4649.mm, 1700.mm, 1200.mm)
txt = entities.add_text("FILM-PLANE RIGHT RAIL + SADDLES
(old rods used to clash here)", anc, Geom::Vector3d.new(400.mm, -300.mm, 500.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4200.mm, 1181.mm, 60.mm)
txt = entities.add_text("SPRAY BAR (Z20-60, low)
55mm clear under the grate", anc, Geom::Vector3d.new(-200.mm, -750.mm, 850.mm))
txt.layer = model.layers["Labels"] rescue nil

# ── In-model © + license credit (default layer → shown in every scene) ──
lbb = model.bounds
lanc = Geom::Point3d.new(lbb.min.x, lbb.min.y - 400.mm, lbb.min.z)
entities.add_text("© 2026 Alvin Richards
Licensed under GNU AGPLv3
alvinr.github.io/tbs", lanc)

model.definitions.purge_unused
model.materials.purge_unused
keep_tags = ["Context", "IBC Frame", "Tray + Spray", "Film Rail + Saddle", "Cantilever Walkway", "Labels"]
default_layer = model.layers[0]
model.layers.to_a.each { |l| model.layers.remove(l, true) rescue nil unless l == default_layer || keep_tags.include?(l.name) }

model.layers.each { |l| l.visible = (l.name != "Labels") }
bb = model.bounds; ctr = bb.center
dir = Geom::Vector3d.new(-0.6, -0.7, 0.45); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.4)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents
[["Combined", ["Context", "IBC Frame", "Tray + Spray", "Film Rail + Saddle", "Cantilever Walkway"]], ["Anchors (frame + walls)", ["Cantilever Walkway", "IBC Frame", "Context"]], ["Clearance (film + spray)", ["Cantilever Walkway", "Film Rail + Saddle", "Tray + Spray"]], ["Labeled", ["Context", "IBC Frame", "Tray + Spray", "Film Rail + Saddle", "Cantilever Walkway", "Labels"]]].each { |name, tags|
  model.layers.each { |l| l.visible = (l == default_layer || tags.include?(l.name)) }
  page = model.pages.add(name); page.use_camera = true
}
model.layers.each { |l| l.visible = true }
model.commit_operation
{ success: true, model: "Right Cantilever Study",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   scenes: model.pages.count }.to_json
