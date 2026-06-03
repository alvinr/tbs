model = Sketchup.active_model
model.start_operation("TBS-001 Light Trap", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# Idempotent rebuild: erase prior generated instances (keep 'Sree'), purge defs.
to_erase = entities.to_a.select { |e|
  (e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance)) &&
  !(e.is_a?(Sketchup::ComponentInstance) && e.definition.name == "Sree")
}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each { |p| model.pages.erase(p) }

# ── Tags (layers) ──
  model.layers.add("Context") unless model.layers["Context"]
  model.layers.add("Door Frame") unless model.layers["Door Frame"]
  model.layers.add("Hinge Panel") unless model.layers["Hinge Panel"]
  model.layers.add("Light Trap") unless model.layers["Light Trap"]
  model.layers.add("Sliding Carriage") unless model.layers["Sliding Carriage"]
  model.layers.add("Fan B") unless model.layers["Fan B"]

# ── Subsystems (each a component on its tag) ──
  # ═══ Context ═══
  defn = model.definitions.add("Context")
  ents = defn.entities
  # Floor (context)
  grp = ents.add_group
  grp.name = "Floor (context)"
  face = grp.entities.add_face([-400.mm,0.mm,-40.mm], [1600.mm,0.mm,-40.mm], [1600.mm,2362.mm,-40.mm], [-400.mm,2362.mm,-40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Floor (context)"] || model.materials.add("Floor (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.25
  grp.material = mat

  # Ceiling (context)
  grp = ents.add_group
  grp.name = "Ceiling (context)"
  face = grp.entities.add_face([-400.mm,0.mm,2388.mm], [1600.mm,0.mm,2388.mm], [1600.mm,2362.mm,2388.mm], [-400.mm,2362.mm,2388.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Ceiling (context)"] || model.materials.add("Ceiling (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.1
  grp.material = mat

  # Side Wall near (context)
  grp = ents.add_group
  grp.name = "Side Wall near (context)"
  face = grp.entities.add_face([-400.mm,-40.mm,0.mm], [1600.mm,-40.mm,0.mm], [1600.mm,0.mm,0.mm], [-400.mm,0.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Side Wall near (context)"] || model.materials.add("Side Wall near (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.16
  grp.material = mat

  # Side Wall far (context)
  grp = ents.add_group
  grp.name = "Side Wall far (context)"
  face = grp.entities.add_face([-400.mm,2362.mm,0.mm], [1600.mm,2362.mm,0.mm], [1600.mm,2402.mm,0.mm], [-400.mm,2402.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Side Wall near (context)"] || model.materials.add("Side Wall near (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.16
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Context"
  inst.layer = model.layers["Context"]

  # ═══ Fixed Door Frame ═══
  defn = model.definitions.add("Fixed Door Frame")
  ents = defn.entities
  # Door Frame bottom
  grp = ents.add_group
  grp.name = "Door Frame bottom"
  face = grp.entities.add_face([-50.mm,0.mm,0.mm], [0.mm,0.mm,0.mm], [0.mm,2362.mm,0.mm], [-50.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Door Frame bottom"] || model.materials.add("Door Frame bottom")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame top
  grp = ents.add_group
  grp.name = "Door Frame top"
  face = grp.entities.add_face([-50.mm,0.mm,2338.mm], [0.mm,0.mm,2338.mm], [0.mm,2362.mm,2338.mm], [-50.mm,2362.mm,2338.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Door Frame bottom"] || model.materials.add("Door Frame bottom")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame left stile
  grp = ents.add_group
  grp.name = "Door Frame left stile"
  face = grp.entities.add_face([-50.mm,0.mm,0.mm], [0.mm,0.mm,0.mm], [0.mm,50.mm,0.mm], [-50.mm,50.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Door Frame bottom"] || model.materials.add("Door Frame bottom")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame right stile
  grp = ents.add_group
  grp.name = "Door Frame right stile"
  face = grp.entities.add_face([-50.mm,2312.mm,0.mm], [0.mm,2312.mm,0.mm], [0.mm,2362.mm,0.mm], [-50.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Door Frame bottom"] || model.materials.add("Door Frame bottom")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Fixed Door Frame"
  inst.layer = model.layers["Door Frame"]

  # ═══ Hinged Light-Trap Panel ═══
  defn = model.definitions.add("Hinged Light-Trap Panel")
  ents = defn.entities
  # Panel near corner (40mm)
  grp = ents.add_group
  grp.name = "Panel near corner (40mm)"
  face = grp.entities.add_face([0.mm,0.mm,80.mm], [40.mm,0.mm,80.mm], [40.mm,756.mm,80.mm], [0.mm,756.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2220.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Panel far corner (40mm)
  grp = ents.add_group
  grp.name = "Panel far corner (40mm)"
  face = grp.entities.add_face([0.mm,1606.mm,80.mm], [40.mm,1606.mm,80.mm], [40.mm,2362.mm,80.mm], [0.mm,2362.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2220.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Panel center jamb L (120mm)
  grp = ents.add_group
  grp.name = "Panel center jamb L (120mm)"
  face = grp.entities.add_face([0.mm,756.mm,80.mm], [120.mm,756.mm,80.mm], [120.mm,806.mm,80.mm], [0.mm,806.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2220.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Panel center jamb R (120mm)
  grp = ents.add_group
  grp.name = "Panel center jamb R (120mm)"
  face = grp.entities.add_face([0.mm,1556.mm,80.mm], [120.mm,1556.mm,80.mm], [120.mm,1606.mm,80.mm], [0.mm,1606.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2220.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Panel header over drum (120mm)
  grp = ents.add_group
  grp.name = "Panel header over drum (120mm)"
  face = grp.entities.add_face([0.mm,756.mm,2200.mm], [120.mm,756.mm,2200.mm], [120.mm,1606.mm,2200.mm], [0.mm,1606.mm,2200.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Drum aperture seal L
  grp = ents.add_group
  grp.name = "Drum aperture seal L"
  face = grp.entities.add_face([0.mm,806.mm,80.mm], [120.mm,806.mm,80.mm], [120.mm,826.mm,80.mm], [0.mm,826.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2200.mm)
  mat = model.materials["Drum aperture seal L"] || model.materials.add("Drum aperture seal L")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Drum aperture seal R
  grp = ents.add_group
  grp.name = "Drum aperture seal R"
  face = grp.entities.add_face([0.mm,1536.mm,80.mm], [120.mm,1536.mm,80.mm], [120.mm,1556.mm,80.mm], [0.mm,1556.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2200.mm)
  mat = model.materials["Drum aperture seal L"] || model.materials.add("Drum aperture seal L")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM seal bottom
  grp = ents.add_group
  grp.name = "EPDM seal bottom"
  face = grp.entities.add_face([-20.mm,0.mm,80.mm], [0.mm,0.mm,80.mm], [0.mm,2362.mm,80.mm], [-20.mm,2362.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Drum aperture seal L"] || model.materials.add("Drum aperture seal L")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM seal top
  grp = ents.add_group
  grp.name = "EPDM seal top"
  face = grp.entities.add_face([-20.mm,0.mm,2268.mm], [0.mm,0.mm,2268.mm], [0.mm,2362.mm,2268.mm], [-20.mm,2362.mm,2268.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Drum aperture seal L"] || model.materials.add("Drum aperture seal L")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM seal left
  grp = ents.add_group
  grp.name = "EPDM seal left"
  face = grp.entities.add_face([-20.mm,0.mm,80.mm], [0.mm,0.mm,80.mm], [0.mm,40.mm,80.mm], [-20.mm,40.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2228.mm)
  mat = model.materials["Drum aperture seal L"] || model.materials.add("Drum aperture seal L")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM seal right
  grp = ents.add_group
  grp.name = "EPDM seal right"
  face = grp.entities.add_face([-20.mm,2322.mm,80.mm], [0.mm,2322.mm,80.mm], [0.mm,2362.mm,80.mm], [-20.mm,2362.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2228.mm)
  mat = model.materials["Drum aperture seal L"] || model.materials.add("Drum aperture seal L")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Piano hinge
  grp = ents.add_group
  grp.name = "Piano hinge"
  face = grp.entities.add_face([-30.mm,0.mm,220.mm], [30.mm,0.mm,220.mm], [30.mm,30.mm,220.mm], [-30.mm,30.mm,220.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Piano hinge
  grp = ents.add_group
  grp.name = "Piano hinge"
  face = grp.entities.add_face([-30.mm,0.mm,1190.mm], [30.mm,0.mm,1190.mm], [30.mm,30.mm,1190.mm], [-30.mm,30.mm,1190.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Piano hinge
  grp = ents.add_group
  grp.name = "Piano hinge"
  face = grp.entities.add_face([-30.mm,0.mm,2158.mm], [30.mm,0.mm,2158.mm], [30.mm,30.mm,2158.mm], [-30.mm,30.mm,2158.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Southco cam latch
  grp = ents.add_group
  grp.name = "Southco cam latch"
  face = grp.entities.add_face([40.mm,175.mm,195.mm], [95.mm,175.mm,195.mm], [95.mm,245.mm,195.mm], [40.mm,245.mm,195.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Southco cam latch"] || model.materials.add("Southco cam latch")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Southco cam latch
  grp = ents.add_group
  grp.name = "Southco cam latch"
  face = grp.entities.add_face([40.mm,175.mm,2143.mm], [95.mm,175.mm,2143.mm], [95.mm,245.mm,2143.mm], [40.mm,245.mm,2143.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Southco cam latch"] || model.materials.add("Southco cam latch")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Southco cam latch
  grp = ents.add_group
  grp.name = "Southco cam latch"
  face = grp.entities.add_face([40.mm,2117.mm,195.mm], [95.mm,2117.mm,195.mm], [95.mm,2187.mm,195.mm], [40.mm,2187.mm,195.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Southco cam latch"] || model.materials.add("Southco cam latch")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # Southco cam latch
  grp = ents.add_group
  grp.name = "Southco cam latch"
  face = grp.entities.add_face([40.mm,2117.mm,2143.mm], [95.mm,2117.mm,2143.mm], [95.mm,2187.mm,2143.mm], [40.mm,2187.mm,2143.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Southco cam latch"] || model.materials.add("Southco cam latch")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Hinged Light-Trap Panel"
  inst.layer = model.layers["Hinge Panel"]

  # ═══ Revolving Light-Trap Drum ═══
  defn = model.definitions.add("Revolving Light-Trap Drum")
  ents = defn.entities
  # LT Drum Shell (3 segments walled)
  grp = ents.add_group
  grp.name = "LT Drum Shell (3 segments walled)"
  ge = grp.entities
  face = ge.add_face([[-265.17.mm,915.83.mm,0], [-237.9.mm,891.12.mm,0], [-208.34.mm,869.2.mm,0], [-176.77.mm,850.28.mm,0], [-143.51.mm,834.55.mm,0], [-108.86.mm,822.15.mm,0], [-73.16.mm,813.21.mm,0], [-36.76.mm,807.81.mm,0], [0.mm,806.mm,0], [36.76.mm,807.81.mm,0], [73.16.mm,813.21.mm,0], [108.86.mm,822.15.mm,0], [143.51.mm,834.55.mm,0], [176.77.mm,850.28.mm,0], [208.34.mm,869.2.mm,0], [237.9.mm,891.12.mm,0], [265.17.mm,915.83.mm,0], [289.88.mm,943.1.mm,0], [311.8.mm,972.66.mm,0], [330.72.mm,1004.23.mm,0], [346.45.mm,1037.49.mm,0], [358.85.mm,1072.14.mm,0], [367.79.mm,1107.84.mm,0], [373.19.mm,1144.24.mm,0], [375.mm,1181.mm,0], [373.19.mm,1217.76.mm,0], [367.79.mm,1254.16.mm,0], [358.85.mm,1289.86.mm,0], [346.45.mm,1324.51.mm,0], [330.72.mm,1357.77.mm,0], [311.8.mm,1389.34.mm,0], [289.88.mm,1418.9.mm,0], [265.17.mm,1446.17.mm,0], [237.9.mm,1470.88.mm,0], [208.34.mm,1492.8.mm,0], [176.77.mm,1511.72.mm,0], [143.51.mm,1527.45.mm,0], [108.86.mm,1539.85.mm,0], [73.16.mm,1548.79.mm,0], [36.76.mm,1554.19.mm,0], [0.mm,1556.mm,0], [-36.76.mm,1554.19.mm,0], [-73.16.mm,1548.79.mm,0], [-108.86.mm,1539.85.mm,0], [-143.51.mm,1527.45.mm,0], [-176.77.mm,1511.72.mm,0], [-208.34.mm,1492.8.mm,0], [-237.9.mm,1470.88.mm,0], [-265.17.mm,1446.17.mm,0], [-256.68.mm,1437.68.mm,0], [-230.28.mm,1461.6.mm,0], [-201.67.mm,1482.82.mm,0], [-171.12.mm,1501.14.mm,0], [-138.91.mm,1516.37.mm,0], [-105.37.mm,1528.37.mm,0], [-70.82.mm,1537.03.mm,0], [-35.58.mm,1542.25.mm,0], [0.mm,1544.mm,0], [35.58.mm,1542.25.mm,0], [70.82.mm,1537.03.mm,0], [105.37.mm,1528.37.mm,0], [138.91.mm,1516.37.mm,0], [171.12.mm,1501.14.mm,0], [201.67.mm,1482.82.mm,0], [230.28.mm,1461.6.mm,0], [256.68.mm,1437.68.mm,0], [280.6.mm,1411.28.mm,0], [301.82.mm,1382.67.mm,0], [320.14.mm,1352.12.mm,0], [335.37.mm,1319.91.mm,0], [347.37.mm,1286.37.mm,0], [356.03.mm,1251.82.mm,0], [361.25.mm,1216.58.mm,0], [363.mm,1181.mm,0], [361.25.mm,1145.42.mm,0], [356.03.mm,1110.18.mm,0], [347.37.mm,1075.63.mm,0], [335.37.mm,1042.09.mm,0], [320.14.mm,1009.88.mm,0], [301.82.mm,979.33.mm,0], [280.6.mm,950.72.mm,0], [256.68.mm,924.32.mm,0], [230.28.mm,900.4.mm,0], [201.67.mm,879.18.mm,0], [171.12.mm,860.86.mm,0], [138.91.mm,845.63.mm,0], [105.37.mm,833.63.mm,0], [70.82.mm,824.97.mm,0], [35.58.mm,819.75.mm,0], [0.mm,818.mm,0], [-35.58.mm,819.75.mm,0], [-70.82.mm,824.97.mm,0], [-105.37.mm,833.63.mm,0], [-138.91.mm,845.63.mm,0], [-171.12.mm,860.86.mm,0], [-201.67.mm,879.18.mm,0], [-230.28.mm,900.4.mm,0], [-256.68.mm,924.32.mm,0]])
  face.reverse! if face.normal.z < 0
  face.pushpull(2200.mm)
  mat = model.materials["LT Drum Shell (3 segments walled)"] || model.materials.add("LT Drum Shell (3 segments walled)")
  mat.color = Sketchup::Color.new(232, 224, 208)
  mat.alpha = 0.18
  grp.material = mat

  # LT Drum Vane A
  grp = ents.add_group
  grp.name = "LT Drum Vane A"
  ge = grp.entities
  face = ge.add_face([[267.29.mm,1444.04.mm,0], [-263.04.mm,913.71.mm,0], [-267.29.mm,917.96.mm,0], [263.04.mm,1448.29.mm,0]])
  face.reverse! if face.normal.z < 0
  face.pushpull(2200.mm)
  mat = model.materials["LT Drum Vane A"] || model.materials.add("LT Drum Vane A")
  mat.color = Sketchup::Color.new(119, 128, 136)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum Vane B
  grp = ents.add_group
  grp.name = "LT Drum Vane B"
  ge = grp.entities
  face = ge.add_face([[-263.04.mm,1448.29.mm,0], [267.29.mm,917.96.mm,0], [263.04.mm,913.71.mm,0], [-267.29.mm,1444.04.mm,0]])
  face.reverse! if face.normal.z < 0
  face.pushpull(2200.mm)
  mat = model.materials["LT Drum Vane A"] || model.materials.add("LT Drum Vane A")
  mat.color = Sketchup::Color.new(119, 128, 136)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum top cap
  grp = ents.add_group
  grp.name = "LT Drum top cap"
  ge = grp.entities
  circle = ge.add_circle([0.mm,1181.mm,2195.mm], [0,0,1], 375.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["LT Drum top cap"] || model.materials.add("LT Drum top cap")
  mat.color = Sketchup::Color.new(232, 224, 208)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum bottom cap
  grp = ents.add_group
  grp.name = "LT Drum bottom cap"
  ge = grp.entities
  circle = ge.add_circle([0.mm,1181.mm,0.mm], [0,0,1], 375.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["LT Drum top cap"] || model.materials.add("LT Drum top cap")
  mat.color = Sketchup::Color.new(232, 224, 208)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum top shaft
  grp = ents.add_group
  grp.name = "LT Drum top shaft"
  ge = grp.entities
  circle = ge.add_circle([0.mm,1181.mm,2200.mm], [0,0,1], 37.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(150.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum bottom shaft
  grp = ents.add_group
  grp.name = "LT Drum bottom shaft"
  ge = grp.entities
  circle = ge.add_circle([0.mm,1181.mm,-150.mm], [0,0,1], 37.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(150.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Upper bearing (SKF 6215)
  grp = ents.add_group
  grp.name = "LT Upper bearing (SKF 6215)"
  ge = grp.entities
  circle = ge.add_circle([0.mm,1181.mm,2200.mm], [0,0,1], 65.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(45.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Lower bearing collar
  grp = ents.add_group
  grp.name = "LT Lower bearing collar"
  ge = grp.entities
  circle = ge.add_circle([0.mm,1181.mm,-45.mm], [0,0,1], 75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(45.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Upper mount plate
  grp = ents.add_group
  grp.name = "LT Upper mount plate"
  face = grp.entities.add_face([-110.mm,1071.mm,2245.mm], [110.mm,1071.mm,2245.mm], [110.mm,1291.mm,2245.mm], [-110.mm,1291.mm,2245.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Floor collar plate
  grp = ents.add_group
  grp.name = "LT Floor collar plate"
  face = grp.entities.add_face([-120.mm,1061.mm,-40.mm], [120.mm,1061.mm,-40.mm], [120.mm,1301.mm,-40.mm], [-120.mm,1301.mm,-40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Grab rail
  grp = ents.add_group
  grp.name = "LT Grab rail"
  ge = grp.entities
  circle = ge.add_circle([435.mm,1181.mm,700.mm], [0,0,1], 15.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(400.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Grab rail standoff
  grp = ents.add_group
  grp.name = "LT Grab rail standoff"
  face = grp.entities.add_face([370.mm,1175.mm,720.mm], [440.mm,1175.mm,720.mm], [440.mm,1187.mm,720.mm], [370.mm,1187.mm,720.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Grab rail standoff
  grp = ents.add_group
  grp.name = "LT Grab rail standoff"
  face = grp.entities.add_face([370.mm,1175.mm,1080.mm], [440.mm,1175.mm,1080.mm], [440.mm,1187.mm,1080.mm], [370.mm,1187.mm,1080.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Revolving Light-Trap Drum"
  inst.layer = model.layers["Light Trap"]

  # ═══ Sliding Carriage System ═══
  defn = model.definitions.add("Sliding Carriage System")
  ents = defn.entities
  # HGR20 rail L
  grp = ents.add_group
  grp.name = "HGR20 rail L"
  face = grp.entities.add_face([-30.mm,746.mm,2358.mm], [480.mm,746.mm,2358.mm], [480.mm,766.mm,2358.mm], [-30.mm,766.mm,2358.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Door Frame bottom"] || model.materials.add("Door Frame bottom")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # HGH20CA carriage L
  grp = ents.add_group
  grp.name = "HGH20CA carriage L"
  face = grp.entities.add_face([18.mm,734.mm,2330.mm], [62.mm,734.mm,2330.mm], [62.mm,778.mm,2330.mm], [18.mm,778.mm,2330.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["HGH20CA carriage L"] || model.materials.add("HGH20CA carriage L")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Suspension bracket L
  grp = ents.add_group
  grp.name = "Suspension bracket L"
  face = grp.entities.add_face([15.mm,736.mm,2300.mm], [75.mm,736.mm,2300.mm], [75.mm,776.mm,2300.mm], [15.mm,776.mm,2300.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # HGR20 rail R
  grp = ents.add_group
  grp.name = "HGR20 rail R"
  face = grp.entities.add_face([-30.mm,1596.mm,2358.mm], [480.mm,1596.mm,2358.mm], [480.mm,1616.mm,2358.mm], [-30.mm,1616.mm,2358.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Door Frame bottom"] || model.materials.add("Door Frame bottom")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # HGH20CA carriage R
  grp = ents.add_group
  grp.name = "HGH20CA carriage R"
  face = grp.entities.add_face([18.mm,1584.mm,2330.mm], [62.mm,1584.mm,2330.mm], [62.mm,1628.mm,2330.mm], [18.mm,1628.mm,2330.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["HGH20CA carriage L"] || model.materials.add("HGH20CA carriage L")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Suspension bracket R
  grp = ents.add_group
  grp.name = "Suspension bracket R"
  face = grp.entities.add_face([15.mm,1586.mm,2300.mm], [75.mm,1586.mm,2300.mm], [75.mm,1626.mm,2300.mm], [15.mm,1626.mm,2300.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left carriage beam (60×60 SHS)
  grp = ents.add_group
  grp.name = "Left carriage beam (60×60 SHS)"
  face = grp.entities.add_face([0.mm,0.mm,80.mm], [60.mm,0.mm,80.mm], [60.mm,60.mm,80.mm], [0.mm,60.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2220.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Destaco clamp (operational) base
  grp = ents.add_group
  grp.name = "Destaco clamp (operational) base"
  face = grp.entities.add_face([-10.mm,738.mm,2288.mm], [50.mm,738.mm,2288.mm], [50.mm,774.mm,2288.mm], [-10.mm,774.mm,2288.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Destaco clamp (operational) handle
  grp = ents.add_group
  grp.name = "Destaco clamp (operational) handle"
  face = grp.entities.add_face([0.mm,750.mm,2312.mm], [70.mm,750.mm,2312.mm], [70.mm,762.mm,2312.mm], [0.mm,762.mm,2312.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["HGH20CA carriage L"] || model.materials.add("HGH20CA carriage L")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Destaco clamp (operational) base
  grp = ents.add_group
  grp.name = "Destaco clamp (operational) base"
  face = grp.entities.add_face([-10.mm,1588.mm,2288.mm], [50.mm,1588.mm,2288.mm], [50.mm,1624.mm,2288.mm], [-10.mm,1624.mm,2288.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Destaco clamp (operational) handle
  grp = ents.add_group
  grp.name = "Destaco clamp (operational) handle"
  face = grp.entities.add_face([0.mm,1600.mm,2312.mm], [70.mm,1600.mm,2312.mm], [70.mm,1612.mm,2312.mm], [0.mm,1612.mm,2312.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["HGH20CA carriage L"] || model.materials.add("HGH20CA carriage L")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Destaco clamp (transport) base
  grp = ents.add_group
  grp.name = "Destaco clamp (transport) base"
  face = grp.entities.add_face([290.mm,738.mm,2288.mm], [350.mm,738.mm,2288.mm], [350.mm,774.mm,2288.mm], [290.mm,774.mm,2288.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Destaco clamp (transport) handle
  grp = ents.add_group
  grp.name = "Destaco clamp (transport) handle"
  face = grp.entities.add_face([300.mm,750.mm,2312.mm], [370.mm,750.mm,2312.mm], [370.mm,762.mm,2312.mm], [300.mm,762.mm,2312.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["HGH20CA carriage L"] || model.materials.add("HGH20CA carriage L")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Destaco clamp (transport) base
  grp = ents.add_group
  grp.name = "Destaco clamp (transport) base"
  face = grp.entities.add_face([290.mm,1588.mm,2288.mm], [350.mm,1588.mm,2288.mm], [350.mm,1624.mm,2288.mm], [290.mm,1624.mm,2288.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Destaco clamp (transport) handle
  grp = ents.add_group
  grp.name = "Destaco clamp (transport) handle"
  face = grp.entities.add_face([300.mm,1600.mm,2312.mm], [370.mm,1600.mm,2312.mm], [370.mm,1612.mm,2312.mm], [300.mm,1612.mm,2312.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["HGH20CA carriage L"] || model.materials.add("HGH20CA carriage L")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Sliding Carriage System"
  inst.layer = model.layers["Sliding Carriage"]

  # ═══ Fan B (intake) ═══
  defn = model.definitions.add("Fan B (intake)")
  ents = defn.entities
  # Fan B (intake) baffle duct
  grp = ents.add_group
  grp.name = "Fan B (intake) baffle duct"
  face = grp.entities.add_face([0.mm,1859.mm,500.mm], [300.mm,1859.mm,500.mm], [300.mm,2059.mm,500.mm], [0.mm,2059.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan B (intake) baffle duct"] || model.materials.add("Fan B (intake) baffle duct")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 0.5
  grp.material = mat

  # Fan B (intake) baffle plate 1
  grp = ents.add_group
  grp.name = "Fan B (intake) baffle plate 1"
  face = grp.entities.add_face([96.mm,1859.mm,500.mm], [104.mm,1859.mm,500.mm], [104.mm,1984.mm,500.mm], [96.mm,1984.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan B (intake) baffle plate 1"] || model.materials.add("Fan B (intake) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) baffle plate 2
  grp = ents.add_group
  grp.name = "Fan B (intake) baffle plate 2"
  face = grp.entities.add_face([196.mm,1934.mm,500.mm], [204.mm,1934.mm,500.mm], [204.mm,2059.mm,500.mm], [196.mm,2059.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan B (intake) baffle plate 1"] || model.materials.add("Fan B (intake) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan frame top
  grp = ents.add_group
  grp.name = "Fan B (intake) fan frame top"
  face = grp.entities.add_face([250.mm,1859.mm,675.mm], [300.mm,1859.mm,675.mm], [300.mm,2059.mm,675.mm], [250.mm,2059.mm,675.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Fan B (intake) baffle plate 1"] || model.materials.add("Fan B (intake) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan frame bottom
  grp = ents.add_group
  grp.name = "Fan B (intake) fan frame bottom"
  face = grp.entities.add_face([250.mm,1859.mm,500.mm], [300.mm,1859.mm,500.mm], [300.mm,2059.mm,500.mm], [250.mm,2059.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Fan B (intake) baffle plate 1"] || model.materials.add("Fan B (intake) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan frame left
  grp = ents.add_group
  grp.name = "Fan B (intake) fan frame left"
  face = grp.entities.add_face([250.mm,1859.mm,525.mm], [300.mm,1859.mm,525.mm], [300.mm,1884.mm,525.mm], [250.mm,1884.mm,525.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Fan B (intake) baffle plate 1"] || model.materials.add("Fan B (intake) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan frame right
  grp = ents.add_group
  grp.name = "Fan B (intake) fan frame right"
  face = grp.entities.add_face([250.mm,2034.mm,525.mm], [300.mm,2034.mm,525.mm], [300.mm,2059.mm,525.mm], [250.mm,2059.mm,525.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Fan B (intake) baffle plate 1"] || model.materials.add("Fan B (intake) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan hub
  grp = ents.add_group
  grp.name = "Fan B (intake) fan hub"
  ge = grp.entities
  circle = ge.add_circle([250.mm,1959.mm,600.mm], [1,0,0], 19.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(50.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade up
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade up"
  face = grp.entities.add_face([272.5.mm,1944.mm,619.5.mm], [278.5.mm,1944.mm,619.5.mm], [278.5.mm,1974.mm,619.5.mm], [272.5.mm,1974.mm,619.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.5.mm)
  mat = model.materials["Fan B (intake) fan blade up"] || model.materials.add("Fan B (intake) fan blade up")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade down
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade down"
  face = grp.entities.add_face([272.5.mm,1944.mm,534.mm], [278.5.mm,1944.mm,534.mm], [278.5.mm,1974.mm,534.mm], [272.5.mm,1974.mm,534.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.5.mm)
  mat = model.materials["Fan B (intake) fan blade up"] || model.materials.add("Fan B (intake) fan blade up")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade left
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade left"
  face = grp.entities.add_face([272.5.mm,1893.mm,585.mm], [278.5.mm,1893.mm,585.mm], [278.5.mm,1939.5.mm,585.mm], [272.5.mm,1939.5.mm,585.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Fan B (intake) fan blade up"] || model.materials.add("Fan B (intake) fan blade up")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade right
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade right"
  face = grp.entities.add_face([272.5.mm,1978.5.mm,585.mm], [278.5.mm,1978.5.mm,585.mm], [278.5.mm,2025.mm,585.mm], [272.5.mm,2025.mm,585.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Fan B (intake) fan blade up"] || model.materials.add("Fan B (intake) fan blade up")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) wall flange
  grp = ents.add_group
  grp.name = "Fan B (intake) wall flange"
  face = grp.entities.add_face([0.mm,1829.mm,470.mm], [5.mm,1829.mm,470.mm], [5.mm,2089.mm,470.mm], [0.mm,2089.mm,470.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(260.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) flange bolt M10
  grp = ents.add_group
  grp.name = "Fan B (intake) flange bolt M10"
  ge = grp.entities
  circle = ge.add_circle([-6.5.mm,1844.mm,485.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(13.mm)
  mat = model.materials["Fan B (intake) flange bolt M10"] || model.materials.add("Fan B (intake) flange bolt M10")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) flange bolt M10
  grp = ents.add_group
  grp.name = "Fan B (intake) flange bolt M10"
  ge = grp.entities
  circle = ge.add_circle([-6.5.mm,1844.mm,715.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(13.mm)
  mat = model.materials["Fan B (intake) flange bolt M10"] || model.materials.add("Fan B (intake) flange bolt M10")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) flange bolt M10
  grp = ents.add_group
  grp.name = "Fan B (intake) flange bolt M10"
  ge = grp.entities
  circle = ge.add_circle([-6.5.mm,2074.mm,485.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(13.mm)
  mat = model.materials["Fan B (intake) flange bolt M10"] || model.materials.add("Fan B (intake) flange bolt M10")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) flange bolt M10
  grp = ents.add_group
  grp.name = "Fan B (intake) flange bolt M10"
  ge = grp.entities
  circle = ge.add_circle([-6.5.mm,2074.mm,715.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(13.mm)
  mat = model.materials["Fan B (intake) flange bolt M10"] || model.materials.add("Fan B (intake) flange bolt M10")
  mat.color = Sketchup::Color.new(58, 58, 66)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre grille
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre grille"
  face = grp.entities.add_face([-40.mm,1859.mm,535.mm], [0.mm,1859.mm,535.mm], [0.mm,2059.mm,535.mm], [-40.mm,2059.mm,535.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(130.mm)
  mat = model.materials["Fan B (intake) louvre grille"] || model.materials.add("Fan B (intake) louvre grille")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 0.55
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,1863.mm,546.5.mm], [-2.mm,1863.mm,546.5.mm], [-2.mm,2055.mm,546.5.mm], [-38.mm,2055.mm,546.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,1863.mm,572.5.mm], [-2.mm,1863.mm,572.5.mm], [-2.mm,2055.mm,572.5.mm], [-38.mm,2055.mm,572.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,1863.mm,598.5.mm], [-2.mm,1863.mm,598.5.mm], [-2.mm,2055.mm,598.5.mm], [-38.mm,2055.mm,598.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,1863.mm,624.5.mm], [-2.mm,1863.mm,624.5.mm], [-2.mm,2055.mm,624.5.mm], [-38.mm,2055.mm,624.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,1863.mm,650.5.mm], [-2.mm,1863.mm,650.5.mm], [-2.mm,2055.mm,650.5.mm], [-38.mm,2055.mm,650.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Fan B (intake)"
  inst.layer = model.layers["Fan B"]


model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags from earlier generator versions ──
keep_tags = ["Context", "Door Frame", "Hinge Panel", "Light Trap", "Sliding Carriage", "Fan B"]
default_layer = model.layers[0]
model.layers.to_a.each { |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}

# ── Scenes — one shared iso camera; scenes only toggle visibility ──
model.layers.each { |l| l.visible = true }
bb = model.bounds
ctr = bb.center
dir = Geom::Vector3d.new(-0.6, -0.72, 0.45); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.5)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

model.pages.add("Overview")
[["Light-Trap Drum", ["Light Trap", "Hinge Panel"]], ["Hinge Panel & Seal", ["Hinge Panel", "Door Frame"]], ["Sliding Carriage", ["Sliding Carriage", "Hinge Panel"]], ["Fan B", ["Fan B", "Hinge Panel"]]].each { |name, tags|
  model.layers.each { |l| l.visible = (l == default_layer || l.name == "Context" || tags.include?(l.name)) }
  page = model.pages.add(name)
  page.use_camera = true
}
model.layers.each { |l| l.visible = true }

model.commit_operation
{ success: true, model: "Light Trap",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
