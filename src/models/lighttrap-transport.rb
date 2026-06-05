model = Sketchup.active_model
model.start_operation("TBS-001 Light Trap (Transport)", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# Idempotent rebuild: erase ALL prior instances.
to_erase = entities.to_a.select { |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance)
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
  model.layers.add("Processing Tray") unless model.layers["Processing Tray"]
  model.layers.add("Walkways") unless model.layers["Walkways"]
  model.layers.add("Cargo Doors") unless model.layers["Cargo Doors"]

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
  # Door Frame threshold
  grp = ents.add_group
  grp.name = "Door Frame threshold"
  face = grp.entities.add_face([-50.mm,0.mm,0.mm], [0.mm,0.mm,0.mm], [0.mm,2362.mm,0.mm], [-50.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Door Frame threshold"] || model.materials.add("Door Frame threshold")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame top
  grp = ents.add_group
  grp.name = "Door Frame top"
  face = grp.entities.add_face([-50.mm,0.mm,2338.mm], [0.mm,0.mm,2338.mm], [0.mm,2362.mm,2338.mm], [-50.mm,2362.mm,2338.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Door Frame threshold"] || model.materials.add("Door Frame threshold")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame left stile
  grp = ents.add_group
  grp.name = "Door Frame left stile"
  face = grp.entities.add_face([-50.mm,0.mm,0.mm], [0.mm,0.mm,0.mm], [0.mm,50.mm,0.mm], [-50.mm,50.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Door Frame threshold"] || model.materials.add("Door Frame threshold")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame right stile
  grp = ents.add_group
  grp.name = "Door Frame right stile"
  face = grp.entities.add_face([-50.mm,2312.mm,0.mm], [0.mm,2312.mm,0.mm], [0.mm,2362.mm,0.mm], [-50.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Door Frame threshold"] || model.materials.add("Door Frame threshold")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame bottom seal lip
  grp = ents.add_group
  grp.name = "Door Frame bottom seal lip"
  face = grp.entities.add_face([-32.mm,0.mm,0.mm], [-20.mm,0.mm,0.mm], [-20.mm,2362.mm,0.mm], [-32.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(110.mm)
  mat = model.materials["Door Frame threshold"] || model.materials.add("Door Frame threshold")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame top seal lip
  grp = ents.add_group
  grp.name = "Door Frame top seal lip"
  face = grp.entities.add_face([-32.mm,0.mm,2270.mm], [-20.mm,0.mm,2270.mm], [-20.mm,2362.mm,2270.mm], [-32.mm,2362.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(118.mm)
  mat = model.materials["Door Frame threshold"] || model.materials.add("Door Frame threshold")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Fixed Door Frame"
  inst.layer = model.layers["Door Frame"]

  # ═══ Closed Cargo Doors ═══
  defn = model.definitions.add("Closed Cargo Doors")
  ents = defn.entities
  # Cargo door leaf R
  grp = ents.add_group
  grp.name = "Cargo door leaf R"
  face = grp.entities.add_face([-115.mm,0.mm,0.mm], [-55.mm,0.mm,0.mm], [-55.mm,1178.mm,0.mm], [-115.mm,1178.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Cargo door leaf R"] || model.materials.add("Cargo door leaf R")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.2
  grp.material = mat

  # Locking bar R3
  grp = ents.add_group
  grp.name = "Locking bar R3"
  face = grp.entities.add_face([-133.mm,339.4.mm,60.mm], [-105.mm,339.4.mm,60.mm], [-105.mm,367.4.mm,60.mm], [-133.mm,367.4.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2268.mm)
  mat = model.materials["Locking bar R3"] || model.materials.add("Locking bar R3")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 0.55
  grp.material = mat

  # Locking bar R7
  grp = ents.add_group
  grp.name = "Locking bar R7"
  face = grp.entities.add_face([-133.mm,810.5999999999999.mm,60.mm], [-105.mm,810.5999999999999.mm,60.mm], [-105.mm,838.5999999999999.mm,60.mm], [-133.mm,838.5999999999999.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2268.mm)
  mat = model.materials["Locking bar R3"] || model.materials.add("Locking bar R3")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 0.55
  grp.material = mat

  # Door handle R
  grp = ents.add_group
  grp.name = "Door handle R"
  face = grp.entities.add_face([-145.mm,1071.76.mm,1050.mm], [-119.mm,1071.76.mm,1050.mm], [-119.mm,1095.76.mm,1050.mm], [-145.mm,1095.76.mm,1050.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(240.mm)
  mat = model.materials["Locking bar R3"] || model.materials.add("Locking bar R3")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 0.55
  grp.material = mat

  # Cargo door leaf L
  grp = ents.add_group
  grp.name = "Cargo door leaf L"
  face = grp.entities.add_face([-115.mm,1184.mm,0.mm], [-55.mm,1184.mm,0.mm], [-55.mm,2362.mm,0.mm], [-115.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Cargo door leaf R"] || model.materials.add("Cargo door leaf R")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.2
  grp.material = mat

  # Locking bar L3
  grp = ents.add_group
  grp.name = "Locking bar L3"
  face = grp.entities.add_face([-133.mm,1523.4.mm,60.mm], [-105.mm,1523.4.mm,60.mm], [-105.mm,1551.4.mm,60.mm], [-133.mm,1551.4.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2268.mm)
  mat = model.materials["Locking bar R3"] || model.materials.add("Locking bar R3")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 0.55
  grp.material = mat

  # Locking bar L7
  grp = ents.add_group
  grp.name = "Locking bar L7"
  face = grp.entities.add_face([-133.mm,1994.6.mm,60.mm], [-105.mm,1994.6.mm,60.mm], [-105.mm,2022.6.mm,60.mm], [-133.mm,2022.6.mm,60.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2268.mm)
  mat = model.materials["Locking bar R3"] || model.materials.add("Locking bar R3")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 0.55
  grp.material = mat

  # Door handle L
  grp = ents.add_group
  grp.name = "Door handle L"
  face = grp.entities.add_face([-145.mm,1266.24.mm,1050.mm], [-119.mm,1266.24.mm,1050.mm], [-119.mm,1290.24.mm,1050.mm], [-145.mm,1290.24.mm,1050.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(240.mm)
  mat = model.materials["Locking bar R3"] || model.materials.add("Locking bar R3")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 0.55
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Closed Cargo Doors"
  inst.layer = model.layers["Cargo Doors"]

  # ═══ Hinged Light-Trap Panel ═══
  defn = model.definitions.add("Hinged Light-Trap Panel")
  ents = defn.entities
  # Panel near corner (40mm)
  grp = ents.add_group
  grp.name = "Panel near corner (40mm)"
  face = grp.entities.add_face([0.mm,0.mm,80.mm], [40.mm,0.mm,80.mm], [40.mm,653.mm,80.mm], [0.mm,653.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2220.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Panel far corner (40mm)
  grp = ents.add_group
  grp.name = "Panel far corner (40mm)"
  face = grp.entities.add_face([0.mm,1709.mm,80.mm], [40.mm,1709.mm,80.mm], [40.mm,2362.mm,80.mm], [0.mm,2362.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2220.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Panel center jamb L (120mm)
  grp = ents.add_group
  grp.name = "Panel center jamb L (120mm)"
  face = grp.entities.add_face([0.mm,653.mm,80.mm], [120.mm,653.mm,80.mm], [120.mm,713.mm,80.mm], [0.mm,713.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2220.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Panel center jamb R (120mm)
  grp = ents.add_group
  grp.name = "Panel center jamb R (120mm)"
  face = grp.entities.add_face([0.mm,1649.mm,80.mm], [120.mm,1649.mm,80.mm], [120.mm,1709.mm,80.mm], [0.mm,1709.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2220.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Panel header over housing (120mm)
  grp = ents.add_group
  grp.name = "Panel header over housing (120mm)"
  face = grp.entities.add_face([0.mm,653.mm,2200.mm], [120.mm,653.mm,2200.mm], [120.mm,1709.mm,2200.mm], [0.mm,1709.mm,2200.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Housing aperture seal L
  grp = ents.add_group
  grp.name = "Housing aperture seal L"
  face = grp.entities.add_face([0.mm,713.mm,80.mm], [120.mm,713.mm,80.mm], [120.mm,733.mm,80.mm], [0.mm,733.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2200.mm)
  mat = model.materials["Housing aperture seal L"] || model.materials.add("Housing aperture seal L")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Housing aperture seal R
  grp = ents.add_group
  grp.name = "Housing aperture seal R"
  face = grp.entities.add_face([0.mm,1629.mm,80.mm], [120.mm,1629.mm,80.mm], [120.mm,1649.mm,80.mm], [0.mm,1649.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2200.mm)
  mat = model.materials["Housing aperture seal L"] || model.materials.add("Housing aperture seal L")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM seal bottom L
  grp = ents.add_group
  grp.name = "EPDM seal bottom L"
  face = grp.entities.add_face([-20.mm,0.mm,80.mm], [0.mm,0.mm,80.mm], [0.mm,716.mm,80.mm], [-20.mm,716.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Housing aperture seal L"] || model.materials.add("Housing aperture seal L")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM seal bottom R
  grp = ents.add_group
  grp.name = "EPDM seal bottom R"
  face = grp.entities.add_face([-20.mm,1646.mm,80.mm], [0.mm,1646.mm,80.mm], [0.mm,2362.mm,80.mm], [-20.mm,2362.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Housing aperture seal L"] || model.materials.add("Housing aperture seal L")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM seal top
  grp = ents.add_group
  grp.name = "EPDM seal top"
  face = grp.entities.add_face([-20.mm,0.mm,2260.mm], [0.mm,0.mm,2260.mm], [0.mm,2362.mm,2260.mm], [-20.mm,2362.mm,2260.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Housing aperture seal L"] || model.materials.add("Housing aperture seal L")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM seal left
  grp = ents.add_group
  grp.name = "EPDM seal left"
  face = grp.entities.add_face([-20.mm,0.mm,80.mm], [0.mm,0.mm,80.mm], [0.mm,40.mm,80.mm], [-20.mm,40.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2220.mm)
  mat = model.materials["Housing aperture seal L"] || model.materials.add("Housing aperture seal L")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # EPDM seal right
  grp = ents.add_group
  grp.name = "EPDM seal right"
  face = grp.entities.add_face([-20.mm,2322.mm,80.mm], [0.mm,2322.mm,80.mm], [0.mm,2362.mm,80.mm], [-20.mm,2362.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2220.mm)
  mat = model.materials["Housing aperture seal L"] || model.materials.add("Housing aperture seal L")
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

  # ═══ Punch-Out Bay ═══
  defn = model.definitions.add("Punch-Out Bay")
  ents = defn.entities
  # Bay wall near (Yd)
  grp = ents.add_group
  grp.name = "Bay wall near (Yd)"
  face = grp.entities.add_face([-890.mm,653.mm,80.mm], [0.mm,653.mm,80.mm], [0.mm,659.mm,80.mm], [-890.mm,659.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2220.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Bay wall far (Yd)
  grp = ents.add_group
  grp.name = "Bay wall far (Yd)"
  face = grp.entities.add_face([-890.mm,1703.mm,80.mm], [0.mm,1703.mm,80.mm], [0.mm,1709.mm,80.mm], [-890.mm,1709.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2220.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Bay wall top
  grp = ents.add_group
  grp.name = "Bay wall top"
  face = grp.entities.add_face([-890.mm,653.mm,2294.mm], [0.mm,653.mm,2294.mm], [0.mm,1709.mm,2294.mm], [-890.mm,1709.mm,2294.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  # Bay wall bottom
  grp = ents.add_group
  grp.name = "Bay wall bottom"
  face = grp.entities.add_face([-890.mm,653.mm,80.mm], [0.mm,653.mm,80.mm], [0.mm,1709.mm,80.mm], [-890.mm,1709.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(6.mm)
  mat = model.materials["Panel near corner (40mm)"] || model.materials.add("Panel near corner (40mm)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Punch-Out Bay"
  inst.layer = model.layers["Hinge Panel"]

  # ═══ Revolving Light-Trap Drum ═══
  defn = model.definitions.add("Revolving Light-Trap Drum")
  ents = defn.entities
  # LT Housing arc (near Yd)
  grp = ents.add_group
  grp.name = "LT Housing arc (near Yd)"
  ge = grp.entities
  face = ge.add_face([[-55.28.mm,1470.25.mm,80.mm], [-66.02.mm,1482.59.mm,80.mm], [-77.21.mm,1494.54.mm,80.mm], [-88.82.mm,1506.06.mm,80.mm], [-100.84.mm,1517.16.mm,80.mm], [-113.26.mm,1527.81.mm,80.mm], [-126.06.mm,1538.01.mm,80.mm], [-139.22.mm,1547.73.mm,80.mm], [-152.72.mm,1556.97.mm,80.mm], [-166.55.mm,1565.71.mm,80.mm], [-180.69.mm,1573.94.mm,80.mm], [-195.12.mm,1581.66.mm,80.mm], [-209.82.mm,1588.84.mm,80.mm], [-224.77.mm,1595.48.mm,80.mm], [-239.96.mm,1601.58.mm,80.mm], [-255.35.mm,1607.12.mm,80.mm], [-270.94.mm,1612.1.mm,80.mm], [-286.7.mm,1616.5.mm,80.mm], [-302.6.mm,1620.33.mm,80.mm], [-318.64.mm,1623.58.mm,80.mm], [-334.78.mm,1626.25.mm,80.mm], [-351.01.mm,1628.33.mm,80.mm], [-367.3.mm,1629.81.mm,80.mm], [-383.64.mm,1630.7.mm,80.mm], [-400.mm,1631.mm,80.mm], [-416.36.mm,1630.7.mm,80.mm], [-432.7.mm,1629.81.mm,80.mm], [-448.99.mm,1628.33.mm,80.mm], [-465.22.mm,1626.25.mm,80.mm], [-481.36.mm,1623.58.mm,80.mm], [-497.4.mm,1620.33.mm,80.mm], [-513.3.mm,1616.5.mm,80.mm], [-529.06.mm,1612.1.mm,80.mm], [-544.65.mm,1607.12.mm,80.mm], [-560.04.mm,1601.58.mm,80.mm], [-575.23.mm,1595.48.mm,80.mm], [-590.18.mm,1588.84.mm,80.mm], [-604.88.mm,1581.66.mm,80.mm], [-619.31.mm,1573.94.mm,80.mm], [-633.45.mm,1565.71.mm,80.mm], [-647.28.mm,1556.97.mm,80.mm], [-660.78.mm,1547.73.mm,80.mm], [-673.94.mm,1538.01.mm,80.mm], [-686.74.mm,1527.81.mm,80.mm], [-699.16.mm,1517.16.mm,80.mm], [-711.18.mm,1506.06.mm,80.mm], [-722.79.mm,1494.54.mm,80.mm], [-733.98.mm,1482.59.mm,80.mm], [-744.72.mm,1470.25.mm,80.mm], [-740.89.mm,1467.04.mm,80.mm], [-730.27.mm,1479.24.mm,80.mm], [-719.21.mm,1491.05.mm,80.mm], [-707.72.mm,1502.45.mm,80.mm], [-695.83.mm,1513.43.mm,80.mm], [-683.55.mm,1523.96.mm,80.mm], [-670.9.mm,1534.04.mm,80.mm], [-657.89.mm,1543.66.mm,80.mm], [-644.53.mm,1552.79.mm,80.mm], [-630.85.mm,1561.44.mm,80.mm], [-616.87.mm,1569.58.mm,80.mm], [-602.6.mm,1577.2.mm,80.mm], [-588.07.mm,1584.31.mm,80.mm], [-573.28.mm,1590.88.mm,80.mm], [-558.26.mm,1596.91.mm,80.mm], [-543.04.mm,1602.38.mm,80.mm], [-527.63.mm,1607.31.mm,80.mm], [-512.05.mm,1611.66.mm,80.mm], [-496.32.mm,1615.45.mm,80.mm], [-480.46.mm,1618.67.mm,80.mm], [-464.49.mm,1621.3.mm,80.mm], [-448.45.mm,1623.36.mm,80.mm], [-432.33.mm,1624.82.mm,80.mm], [-416.18.mm,1625.71.mm,80.mm], [-400.mm,1626.mm,80.mm], [-383.82.mm,1625.71.mm,80.mm], [-367.67.mm,1624.82.mm,80.mm], [-351.55.mm,1623.36.mm,80.mm], [-335.51.mm,1621.3.mm,80.mm], [-319.54.mm,1618.67.mm,80.mm], [-303.68.mm,1615.45.mm,80.mm], [-287.95.mm,1611.66.mm,80.mm], [-272.37.mm,1607.31.mm,80.mm], [-256.96.mm,1602.38.mm,80.mm], [-241.74.mm,1596.91.mm,80.mm], [-226.72.mm,1590.88.mm,80.mm], [-211.93.mm,1584.31.mm,80.mm], [-197.4.mm,1577.2.mm,80.mm], [-183.13.mm,1569.58.mm,80.mm], [-169.15.mm,1561.44.mm,80.mm], [-155.47.mm,1552.79.mm,80.mm], [-142.11.mm,1543.66.mm,80.mm], [-129.1.mm,1534.04.mm,80.mm], [-116.45.mm,1523.96.mm,80.mm], [-104.17.mm,1513.43.mm,80.mm], [-92.28.mm,1502.45.mm,80.mm], [-80.79.mm,1491.05.mm,80.mm], [-69.73.mm,1479.24.mm,80.mm], [-59.11.mm,1467.04.mm,80.mm]])
  face.reverse! if face.normal.z < 0
  face.pushpull(2120.mm)
  mat = model.materials["LT Housing arc (near Yd)"] || model.materials.add("LT Housing arc (near Yd)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.42
  grp.material = mat

  # LT Housing arc (far Yd)
  grp = ents.add_group
  grp.name = "LT Housing arc (far Yd)"
  ge = grp.entities
  face = ge.add_face([[-744.72.mm,891.75.mm,80.mm], [-733.98.mm,879.41.mm,80.mm], [-722.79.mm,867.46.mm,80.mm], [-711.18.mm,855.94.mm,80.mm], [-699.16.mm,844.84.mm,80.mm], [-686.74.mm,834.19.mm,80.mm], [-673.94.mm,823.99.mm,80.mm], [-660.78.mm,814.27.mm,80.mm], [-647.28.mm,805.03.mm,80.mm], [-633.45.mm,796.29.mm,80.mm], [-619.31.mm,788.06.mm,80.mm], [-604.88.mm,780.34.mm,80.mm], [-590.18.mm,773.16.mm,80.mm], [-575.23.mm,766.52.mm,80.mm], [-560.04.mm,760.42.mm,80.mm], [-544.65.mm,754.88.mm,80.mm], [-529.06.mm,749.9.mm,80.mm], [-513.3.mm,745.5.mm,80.mm], [-497.4.mm,741.67.mm,80.mm], [-481.36.mm,738.42.mm,80.mm], [-465.22.mm,735.75.mm,80.mm], [-448.99.mm,733.67.mm,80.mm], [-432.7.mm,732.19.mm,80.mm], [-416.36.mm,731.3.mm,80.mm], [-400.mm,731.mm,80.mm], [-383.64.mm,731.3.mm,80.mm], [-367.3.mm,732.19.mm,80.mm], [-351.01.mm,733.67.mm,80.mm], [-334.78.mm,735.75.mm,80.mm], [-318.64.mm,738.42.mm,80.mm], [-302.6.mm,741.67.mm,80.mm], [-286.7.mm,745.5.mm,80.mm], [-270.94.mm,749.9.mm,80.mm], [-255.35.mm,754.88.mm,80.mm], [-239.96.mm,760.42.mm,80.mm], [-224.77.mm,766.52.mm,80.mm], [-209.82.mm,773.16.mm,80.mm], [-195.12.mm,780.34.mm,80.mm], [-180.69.mm,788.06.mm,80.mm], [-166.55.mm,796.29.mm,80.mm], [-152.72.mm,805.03.mm,80.mm], [-139.22.mm,814.27.mm,80.mm], [-126.06.mm,823.99.mm,80.mm], [-113.26.mm,834.19.mm,80.mm], [-100.84.mm,844.84.mm,80.mm], [-88.82.mm,855.94.mm,80.mm], [-77.21.mm,867.46.mm,80.mm], [-66.02.mm,879.41.mm,80.mm], [-55.28.mm,891.75.mm,80.mm], [-59.11.mm,894.96.mm,80.mm], [-69.73.mm,882.76.mm,80.mm], [-80.79.mm,870.95.mm,80.mm], [-92.28.mm,859.55.mm,80.mm], [-104.17.mm,848.57.mm,80.mm], [-116.45.mm,838.04.mm,80.mm], [-129.1.mm,827.96.mm,80.mm], [-142.11.mm,818.34.mm,80.mm], [-155.47.mm,809.21.mm,80.mm], [-169.15.mm,800.56.mm,80.mm], [-183.13.mm,792.42.mm,80.mm], [-197.4.mm,784.8.mm,80.mm], [-211.93.mm,777.69.mm,80.mm], [-226.72.mm,771.12.mm,80.mm], [-241.74.mm,765.09.mm,80.mm], [-256.96.mm,759.62.mm,80.mm], [-272.37.mm,754.69.mm,80.mm], [-287.95.mm,750.34.mm,80.mm], [-303.68.mm,746.55.mm,80.mm], [-319.54.mm,743.33.mm,80.mm], [-335.51.mm,740.7.mm,80.mm], [-351.55.mm,738.64.mm,80.mm], [-367.67.mm,737.18.mm,80.mm], [-383.82.mm,736.29.mm,80.mm], [-400.mm,736.mm,80.mm], [-416.18.mm,736.29.mm,80.mm], [-432.33.mm,737.18.mm,80.mm], [-448.45.mm,738.64.mm,80.mm], [-464.49.mm,740.7.mm,80.mm], [-480.46.mm,743.33.mm,80.mm], [-496.32.mm,746.55.mm,80.mm], [-512.05.mm,750.34.mm,80.mm], [-527.63.mm,754.69.mm,80.mm], [-543.04.mm,759.62.mm,80.mm], [-558.26.mm,765.09.mm,80.mm], [-573.28.mm,771.12.mm,80.mm], [-588.07.mm,777.69.mm,80.mm], [-602.6.mm,784.8.mm,80.mm], [-616.87.mm,792.42.mm,80.mm], [-630.85.mm,800.56.mm,80.mm], [-644.53.mm,809.21.mm,80.mm], [-657.89.mm,818.34.mm,80.mm], [-670.9.mm,827.96.mm,80.mm], [-683.55.mm,838.04.mm,80.mm], [-695.83.mm,848.57.mm,80.mm], [-707.72.mm,859.55.mm,80.mm], [-719.21.mm,870.95.mm,80.mm], [-730.27.mm,882.76.mm,80.mm], [-740.89.mm,894.96.mm,80.mm]])
  face.reverse! if face.normal.z < 0
  face.pushpull(2120.mm)
  mat = model.materials["LT Housing arc (near Yd)"] || model.materials.add("LT Housing arc (near Yd)")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.42
  grp.material = mat

  # LT Drum C-shell
  grp = ents.add_group
  grp.name = "LT Drum C-shell"
  ge = grp.entities
  face = ge.add_face([[-730.93.mm,903.32.mm,80.mm], [-701.mm,871.12.mm,80.mm], [-667.94.mm,842.13.mm,80.mm], [-632.11.mm,816.65.mm,80.mm], [-593.88.mm,794.95.mm,80.mm], [-553.64.mm,777.24.mm,80.mm], [-511.81.mm,763.72.mm,80.mm], [-468.82.mm,754.52.mm,80.mm], [-425.12.mm,749.73.mm,80.mm], [-381.16.mm,749.41.mm,80.mm], [-337.39.mm,753.56.mm,80.mm], [-294.27.mm,762.14.mm,80.mm], [-252.25.mm,775.05.mm,80.mm], [-211.75.mm,792.17.mm,80.mm], [-173.21.mm,813.32.mm,80.mm], [-137.02.mm,838.27.mm,80.mm], [-103.54.mm,866.77.mm,80.mm], [-73.14.mm,898.53.mm,80.mm], [-46.13.mm,933.21.mm,80.mm], [-22.78.mm,970.46.mm,80.mm], [-3.33.mm,1009.89.mm,80.mm], [12.01.mm,1051.1.mm,80.mm], [23.08.mm,1093.64.mm,80.mm], [29.76.mm,1137.09.mm,80.mm], [32.mm,1181.mm,80.mm], [29.76.mm,1224.91.mm,80.mm], [23.08.mm,1268.36.mm,80.mm], [12.01.mm,1310.9.mm,80.mm], [-3.33.mm,1352.11.mm,80.mm], [-22.78.mm,1391.54.mm,80.mm], [-46.13.mm,1428.79.mm,80.mm], [-73.14.mm,1463.47.mm,80.mm], [-103.54.mm,1495.23.mm,80.mm], [-137.02.mm,1523.73.mm,80.mm], [-173.21.mm,1548.68.mm,80.mm], [-211.75.mm,1569.83.mm,80.mm], [-252.25.mm,1586.95.mm,80.mm], [-294.27.mm,1599.86.mm,80.mm], [-337.39.mm,1608.44.mm,80.mm], [-381.16.mm,1612.59.mm,80.mm], [-425.12.mm,1612.27.mm,80.mm], [-468.82.mm,1607.48.mm,80.mm], [-511.81.mm,1598.28.mm,80.mm], [-553.64.mm,1584.76.mm,80.mm], [-593.88.mm,1567.05.mm,80.mm], [-632.11.mm,1545.35.mm,80.mm], [-667.94.mm,1519.87.mm,80.mm], [-701.mm,1490.88.mm,80.mm], [-730.93.mm,1458.68.mm,80.mm], [-727.87.mm,1456.11.mm,80.mm], [-698.21.mm,1488.01.mm,80.mm], [-665.46.mm,1516.73.mm,80.mm], [-629.96.mm,1541.97.mm,80.mm], [-592.09.mm,1563.47.mm,80.mm], [-552.22.mm,1581.02.mm,80.mm], [-510.77.mm,1594.42.mm,80.mm], [-468.18.mm,1603.53.mm,80.mm], [-424.89.mm,1608.28.mm,80.mm], [-381.33.mm,1608.59.mm,80.mm], [-337.97.mm,1604.48.mm,80.mm], [-295.25.mm,1595.98.mm,80.mm], [-253.62.mm,1583.19.mm,80.mm], [-213.5.mm,1566.23.mm,80.mm], [-175.31.mm,1545.28.mm,80.mm], [-139.45.mm,1520.56.mm,80.mm], [-106.29.mm,1492.32.mm,80.mm], [-76.17.mm,1460.85.mm,80.mm], [-49.4.mm,1426.49.mm,80.mm], [-26.27.mm,1389.59.mm,80.mm], [-7.mm,1350.52.mm,80.mm], [8.19.mm,1309.7.mm,80.mm], [19.16.mm,1267.55.mm,80.mm], [25.78.mm,1224.5.mm,80.mm], [28.mm,1181.mm,80.mm], [25.78.mm,1137.5.mm,80.mm], [19.16.mm,1094.45.mm,80.mm], [8.19.mm,1052.3.mm,80.mm], [-7.mm,1011.48.mm,80.mm], [-26.27.mm,972.41.mm,80.mm], [-49.4.mm,935.51.mm,80.mm], [-76.17.mm,901.15.mm,80.mm], [-106.29.mm,869.68.mm,80.mm], [-139.45.mm,841.44.mm,80.mm], [-175.31.mm,816.72.mm,80.mm], [-213.5.mm,795.77.mm,80.mm], [-253.62.mm,778.81.mm,80.mm], [-295.25.mm,766.02.mm,80.mm], [-337.97.mm,757.52.mm,80.mm], [-381.33.mm,753.41.mm,80.mm], [-424.89.mm,753.72.mm,80.mm], [-468.18.mm,758.47.mm,80.mm], [-510.77.mm,767.58.mm,80.mm], [-552.22.mm,780.98.mm,80.mm], [-592.09.mm,798.53.mm,80.mm], [-629.96.mm,820.03.mm,80.mm], [-665.46.mm,845.27.mm,80.mm], [-698.21.mm,873.99.mm,80.mm], [-727.87.mm,905.89.mm,80.mm]])
  face.reverse! if face.normal.z < 0
  face.pushpull(2120.mm)
  mat = model.materials["LT Drum C-shell"] || model.materials.add("LT Drum C-shell")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 0.85
  grp.material = mat

  # LT Drum top cap
  grp = ents.add_group
  grp.name = "LT Drum top cap"
  ge = grp.entities
  circle = ge.add_circle([-400.mm,1181.mm,2195.mm], [0,0,1], 432.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["LT Drum top cap"] || model.materials.add("LT Drum top cap")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum bottom cap
  grp = ents.add_group
  grp.name = "LT Drum bottom cap"
  ge = grp.entities
  circle = ge.add_circle([-400.mm,1181.mm,80.mm], [0,0,1], 432.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(5.mm)
  mat = model.materials["LT Drum top cap"] || model.materials.add("LT Drum top cap")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum top shaft
  grp = ents.add_group
  grp.name = "LT Drum top shaft"
  ge = grp.entities
  circle = ge.add_circle([-400.mm,1181.mm,2200.mm], [0,0,1], 37.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(65.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Upper bearing (SKF 6215)
  grp = ents.add_group
  grp.name = "LT Upper bearing (SKF 6215)"
  ge = grp.entities
  circle = ge.add_circle([-400.mm,1181.mm,2200.mm], [0,0,1], 65.mm, 24)
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
  circle = ge.add_circle([-400.mm,1181.mm,80.mm], [0,0,1], 75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(45.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Lower bearing mount plate
  grp = ents.add_group
  grp.name = "LT Lower bearing mount plate"
  face = grp.entities.add_face([-520.mm,1061.mm,80.mm], [-280.mm,1061.mm,80.mm], [-280.mm,1301.mm,80.mm], [-520.mm,1301.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Grab rail
  grp = ents.add_group
  grp.name = "LT Grab rail"
  ge = grp.entities
  circle = ge.add_circle([-43.mm,1181.mm,700.mm], [0,0,1], 15.mm, 24)
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
  face = grp.entities.add_face([-43.mm,1175.mm,720.mm], [28.mm,1175.mm,720.mm], [28.mm,1187.mm,720.mm], [-43.mm,1187.mm,720.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Grab rail standoff
  grp = ents.add_group
  grp.name = "LT Grab rail standoff"
  face = grp.entities.add_face([-43.mm,1175.mm,1080.mm], [28.mm,1175.mm,1080.mm], [28.mm,1187.mm,1080.mm], [-43.mm,1187.mm,1080.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum opening brush seal
  grp = ents.add_group
  grp.name = "LT Drum opening brush seal"
  ge = grp.entities
  circle = ge.add_circle([-735.9104883076718.mm,1462.8623668475475.mm,80.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2120.mm)
  mat = model.materials["LT Drum opening brush seal"] || model.materials.add("LT Drum opening brush seal")
  mat.color = Sketchup::Color.new(126, 126, 118)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum opening brush seal
  grp = ents.add_group
  grp.name = "LT Drum opening brush seal"
  ge = grp.entities
  circle = ge.add_circle([-735.9104883076718.mm,899.1376331524525.mm,80.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2120.mm)
  mat = model.materials["LT Drum opening brush seal"] || model.materials.add("LT Drum opening brush seal")
  mat.color = Sketchup::Color.new(126, 126, 118)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum top felt seal
  grp = ents.add_group
  grp.name = "LT Drum top felt seal"
  ge = grp.entities
  circle = ge.add_circle([-400.mm,1181.mm,2192.mm], [0,0,1], 444.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(8.mm)
  mat = model.materials["LT Drum opening brush seal"] || model.materials.add("LT Drum opening brush seal")
  mat.color = Sketchup::Color.new(126, 126, 118)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum bottom felt seal
  grp = ents.add_group
  grp.name = "LT Drum bottom felt seal"
  ge = grp.entities
  circle = ge.add_circle([-400.mm,1181.mm,80.mm], [0,0,1], 444.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(8.mm)
  mat = model.materials["LT Drum opening brush seal"] || model.materials.add("LT Drum opening brush seal")
  mat.color = Sketchup::Color.new(126, 126, 118)
  mat.alpha = 1.0
  grp.material = mat

  # Housing surround seal bottom
  grp = ents.add_group
  grp.name = "Housing surround seal bottom"
  face = grp.entities.add_face([-20.mm,713.mm,80.mm], [0.mm,713.mm,80.mm], [0.mm,1649.mm,80.mm], [-20.mm,1649.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Housing aperture seal L"] || model.materials.add("Housing aperture seal L")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Housing surround seal top
  grp = ents.add_group
  grp.name = "Housing surround seal top"
  face = grp.entities.add_face([-20.mm,713.mm,2160.mm], [0.mm,713.mm,2160.mm], [0.mm,1649.mm,2160.mm], [-20.mm,1649.mm,2160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Housing aperture seal L"] || model.materials.add("Housing aperture seal L")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Housing surround seal left
  grp = ents.add_group
  grp.name = "Housing surround seal left"
  face = grp.entities.add_face([-20.mm,713.mm,80.mm], [0.mm,713.mm,80.mm], [0.mm,753.mm,80.mm], [-20.mm,753.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2120.mm)
  mat = model.materials["Housing aperture seal L"] || model.materials.add("Housing aperture seal L")
  mat.color = Sketchup::Color.new(90, 48, 32)
  mat.alpha = 1.0
  grp.material = mat

  # Housing surround seal right
  grp = ents.add_group
  grp.name = "Housing surround seal right"
  face = grp.entities.add_face([-20.mm,1609.mm,80.mm], [0.mm,1609.mm,80.mm], [0.mm,1649.mm,80.mm], [-20.mm,1649.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2120.mm)
  mat = model.materials["Housing aperture seal L"] || model.materials.add("Housing aperture seal L")
  mat.color = Sketchup::Color.new(90, 48, 32)
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
  face = grp.entities.add_face([-30.mm,643.mm,2358.mm], [730.mm,643.mm,2358.mm], [730.mm,663.mm,2358.mm], [-30.mm,663.mm,2358.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Door Frame threshold"] || model.materials.add("Door Frame threshold")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # HGH20CA carriage L
  grp = ents.add_group
  grp.name = "HGH20CA carriage L"
  face = grp.entities.add_face([898.mm,631.mm,2330.mm], [942.mm,631.mm,2330.mm], [942.mm,675.mm,2330.mm], [898.mm,675.mm,2330.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["HGH20CA carriage L"] || model.materials.add("HGH20CA carriage L")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Suspension bracket L
  grp = ents.add_group
  grp.name = "Suspension bracket L"
  face = grp.entities.add_face([895.mm,633.mm,2300.mm], [955.mm,633.mm,2300.mm], [955.mm,673.mm,2300.mm], [895.mm,673.mm,2300.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # HGR20 rail R
  grp = ents.add_group
  grp.name = "HGR20 rail R"
  face = grp.entities.add_face([-30.mm,1699.mm,2358.mm], [730.mm,1699.mm,2358.mm], [730.mm,1719.mm,2358.mm], [-30.mm,1719.mm,2358.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Door Frame threshold"] || model.materials.add("Door Frame threshold")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # HGH20CA carriage R
  grp = ents.add_group
  grp.name = "HGH20CA carriage R"
  face = grp.entities.add_face([898.mm,1687.mm,2330.mm], [942.mm,1687.mm,2330.mm], [942.mm,1731.mm,2330.mm], [898.mm,1731.mm,2330.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["HGH20CA carriage L"] || model.materials.add("HGH20CA carriage L")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Suspension bracket R
  grp = ents.add_group
  grp.name = "Suspension bracket R"
  face = grp.entities.add_face([895.mm,1689.mm,2300.mm], [955.mm,1689.mm,2300.mm], [955.mm,1729.mm,2300.mm], [895.mm,1729.mm,2300.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Left carriage beam (60×60 SHS)
  grp = ents.add_group
  grp.name = "Left carriage beam (60×60 SHS)"
  face = grp.entities.add_face([880.mm,0.mm,80.mm], [940.mm,0.mm,80.mm], [940.mm,60.mm,80.mm], [880.mm,60.mm,80.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2220.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Destaco clamp (operational) base
  grp = ents.add_group
  grp.name = "Destaco clamp (operational) base"
  face = grp.entities.add_face([-10.mm,635.mm,2288.mm], [50.mm,635.mm,2288.mm], [50.mm,671.mm,2288.mm], [-10.mm,671.mm,2288.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Destaco clamp (operational) handle
  grp = ents.add_group
  grp.name = "Destaco clamp (operational) handle"
  face = grp.entities.add_face([0.mm,647.mm,2312.mm], [70.mm,647.mm,2312.mm], [70.mm,659.mm,2312.mm], [0.mm,659.mm,2312.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["HGH20CA carriage L"] || model.materials.add("HGH20CA carriage L")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Destaco clamp (operational) base
  grp = ents.add_group
  grp.name = "Destaco clamp (operational) base"
  face = grp.entities.add_face([-10.mm,1691.mm,2288.mm], [50.mm,1691.mm,2288.mm], [50.mm,1727.mm,2288.mm], [-10.mm,1727.mm,2288.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Destaco clamp (operational) handle
  grp = ents.add_group
  grp.name = "Destaco clamp (operational) handle"
  face = grp.entities.add_face([0.mm,1703.mm,2312.mm], [70.mm,1703.mm,2312.mm], [70.mm,1715.mm,2312.mm], [0.mm,1715.mm,2312.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["HGH20CA carriage L"] || model.materials.add("HGH20CA carriage L")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Destaco clamp (transport) base
  grp = ents.add_group
  grp.name = "Destaco clamp (transport) base"
  face = grp.entities.add_face([870.mm,635.mm,2288.mm], [930.mm,635.mm,2288.mm], [930.mm,671.mm,2288.mm], [870.mm,671.mm,2288.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Destaco clamp (transport) handle
  grp = ents.add_group
  grp.name = "Destaco clamp (transport) handle"
  face = grp.entities.add_face([880.mm,647.mm,2312.mm], [950.mm,647.mm,2312.mm], [950.mm,659.mm,2312.mm], [880.mm,659.mm,2312.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["HGH20CA carriage L"] || model.materials.add("HGH20CA carriage L")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Destaco clamp (transport) base
  grp = ents.add_group
  grp.name = "Destaco clamp (transport) base"
  face = grp.entities.add_face([870.mm,1691.mm,2288.mm], [930.mm,1691.mm,2288.mm], [930.mm,1727.mm,2288.mm], [870.mm,1727.mm,2288.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Destaco clamp (transport) handle
  grp = ents.add_group
  grp.name = "Destaco clamp (transport) handle"
  face = grp.entities.add_face([880.mm,1703.mm,2312.mm], [950.mm,1703.mm,2312.mm], [950.mm,1715.mm,2312.mm], [880.mm,1715.mm,2312.mm])
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
  face = grp.entities.add_face([0.mm,1896.mm,500.mm], [300.mm,1896.mm,500.mm], [300.mm,2096.mm,500.mm], [0.mm,2096.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan B (intake) baffle duct"] || model.materials.add("Fan B (intake) baffle duct")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 0.5
  grp.material = mat

  # Fan B (intake) baffle plate 1
  grp = ents.add_group
  grp.name = "Fan B (intake) baffle plate 1"
  face = grp.entities.add_face([96.mm,1896.mm,500.mm], [104.mm,1896.mm,500.mm], [104.mm,2021.mm,500.mm], [96.mm,2021.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan B (intake) baffle plate 1"] || model.materials.add("Fan B (intake) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) baffle plate 2
  grp = ents.add_group
  grp.name = "Fan B (intake) baffle plate 2"
  face = grp.entities.add_face([196.mm,1971.mm,500.mm], [204.mm,1971.mm,500.mm], [204.mm,2096.mm,500.mm], [196.mm,2096.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["Fan B (intake) baffle plate 1"] || model.materials.add("Fan B (intake) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan frame top
  grp = ents.add_group
  grp.name = "Fan B (intake) fan frame top"
  face = grp.entities.add_face([250.mm,1896.mm,675.mm], [300.mm,1896.mm,675.mm], [300.mm,2096.mm,675.mm], [250.mm,2096.mm,675.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Fan B (intake) baffle plate 1"] || model.materials.add("Fan B (intake) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan frame bottom
  grp = ents.add_group
  grp.name = "Fan B (intake) fan frame bottom"
  face = grp.entities.add_face([250.mm,1896.mm,500.mm], [300.mm,1896.mm,500.mm], [300.mm,2096.mm,500.mm], [250.mm,2096.mm,500.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Fan B (intake) baffle plate 1"] || model.materials.add("Fan B (intake) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan frame left
  grp = ents.add_group
  grp.name = "Fan B (intake) fan frame left"
  face = grp.entities.add_face([250.mm,1896.mm,525.mm], [300.mm,1896.mm,525.mm], [300.mm,1921.mm,525.mm], [250.mm,1921.mm,525.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["Fan B (intake) baffle plate 1"] || model.materials.add("Fan B (intake) baffle plate 1")
  mat.color = Sketchup::Color.new(96, 96, 96)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan frame right
  grp = ents.add_group
  grp.name = "Fan B (intake) fan frame right"
  face = grp.entities.add_face([250.mm,2071.mm,525.mm], [300.mm,2071.mm,525.mm], [300.mm,2096.mm,525.mm], [250.mm,2096.mm,525.mm])
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
  circle = ge.add_circle([250.mm,1996.mm,600.mm], [1,0,0], 19.5.mm, 24)
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
  face = grp.entities.add_face([272.5.mm,1981.mm,619.5.mm], [278.5.mm,1981.mm,619.5.mm], [278.5.mm,2011.mm,619.5.mm], [272.5.mm,2011.mm,619.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.5.mm)
  mat = model.materials["LT Drum top cap"] || model.materials.add("LT Drum top cap")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade down
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade down"
  face = grp.entities.add_face([272.5.mm,1981.mm,534.mm], [278.5.mm,1981.mm,534.mm], [278.5.mm,2011.mm,534.mm], [272.5.mm,2011.mm,534.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.5.mm)
  mat = model.materials["LT Drum top cap"] || model.materials.add("LT Drum top cap")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade left
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade left"
  face = grp.entities.add_face([272.5.mm,1930.mm,585.mm], [278.5.mm,1930.mm,585.mm], [278.5.mm,1976.5.mm,585.mm], [272.5.mm,1976.5.mm,585.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["LT Drum top cap"] || model.materials.add("LT Drum top cap")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade right
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade right"
  face = grp.entities.add_face([272.5.mm,2015.5.mm,585.mm], [278.5.mm,2015.5.mm,585.mm], [278.5.mm,2062.mm,585.mm], [272.5.mm,2062.mm,585.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["LT Drum top cap"] || model.materials.add("LT Drum top cap")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) wall flange
  grp = ents.add_group
  grp.name = "Fan B (intake) wall flange"
  face = grp.entities.add_face([0.mm,1866.mm,470.mm], [5.mm,1866.mm,470.mm], [5.mm,2126.mm,470.mm], [0.mm,2126.mm,470.mm])
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
  circle = ge.add_circle([-6.5.mm,1881.mm,485.mm], [1,0,0], 5.mm, 24)
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
  circle = ge.add_circle([-6.5.mm,1881.mm,715.mm], [1,0,0], 5.mm, 24)
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
  circle = ge.add_circle([-6.5.mm,2111.mm,485.mm], [1,0,0], 5.mm, 24)
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
  circle = ge.add_circle([-6.5.mm,2111.mm,715.mm], [1,0,0], 5.mm, 24)
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
  face = grp.entities.add_face([-40.mm,1896.mm,535.mm], [0.mm,1896.mm,535.mm], [0.mm,2096.mm,535.mm], [-40.mm,2096.mm,535.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(130.mm)
  mat = model.materials["Fan B (intake) louvre grille"] || model.materials.add("Fan B (intake) louvre grille")
  mat.color = Sketchup::Color.new(128, 144, 160)
  mat.alpha = 0.55
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,1900.mm,546.5.mm], [-2.mm,1900.mm,546.5.mm], [-2.mm,2092.mm,546.5.mm], [-38.mm,2092.mm,546.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,1900.mm,572.5.mm], [-2.mm,1900.mm,572.5.mm], [-2.mm,2092.mm,572.5.mm], [-38.mm,2092.mm,572.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,1900.mm,598.5.mm], [-2.mm,1900.mm,598.5.mm], [-2.mm,2092.mm,598.5.mm], [-38.mm,2092.mm,598.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,1900.mm,624.5.mm], [-2.mm,1900.mm,624.5.mm], [-2.mm,2092.mm,624.5.mm], [-38.mm,2092.mm,624.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) louvre slat
  grp = ents.add_group
  grp.name = "Fan B (intake) louvre slat"
  face = grp.entities.add_face([-38.mm,1900.mm,650.5.mm], [-2.mm,1900.mm,650.5.mm], [-2.mm,2092.mm,650.5.mm], [-38.mm,2092.mm,650.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Fan B (intake)"
  inst.layer = model.layers["Fan B"]

  # ═══ Processing Tray (partial) ═══
  defn = model.definitions.add("Processing Tray (partial)")
  ents = defn.entities
  # Processing Tray Floor (partial)
  grp = ents.add_group
  grp.name = "Processing Tray Floor (partial)"
  face = grp.entities.add_face([170.mm,80.mm,0.mm], [1600.mm,80.mm,0.mm], [1600.mm,2280.mm,0.mm], [170.mm,2280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["Processing Tray Floor (partial)"] || model.materials.add("Processing Tray Floor (partial)")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Near (partial)
  grp = ents.add_group
  grp.name = "Tray Rim Near (partial)"
  face = grp.entities.add_face([170.mm,80.mm,2.mm], [1600.mm,80.mm,2.mm], [1600.mm,82.mm,2.mm], [170.mm,82.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Processing Tray Floor (partial)"] || model.materials.add("Processing Tray Floor (partial)")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Far (partial)
  grp = ents.add_group
  grp.name = "Tray Rim Far (partial)"
  face = grp.entities.add_face([170.mm,2278.mm,2.mm], [1600.mm,2278.mm,2.mm], [1600.mm,2280.mm,2.mm], [170.mm,2280.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Processing Tray Floor (partial)"] || model.materials.add("Processing Tray Floor (partial)")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Tray Rim Left (cargo end)
  grp = ents.add_group
  grp.name = "Tray Rim Left (cargo end)"
  face = grp.entities.add_face([170.mm,80.mm,2.mm], [172.mm,80.mm,2.mm], [172.mm,2280.mm,2.mm], [170.mm,2280.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["Processing Tray Floor (partial)"] || model.materials.add("Processing Tray Floor (partial)")
  mat.color = Sketchup::Color.new(159, 184, 200)
  mat.alpha = 1.0
  grp.material = mat

  # Chemistry Bath (partial)
  grp = ents.add_group
  grp.name = "Chemistry Bath (partial)"
  face = grp.entities.add_face([172.mm,82.mm,2.mm], [1598.mm,82.mm,2.mm], [1598.mm,2278.mm,2.mm], [172.mm,2278.mm,2.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Chemistry Bath (partial)"] || model.materials.add("Chemistry Bath (partial)")
  mat.color = Sketchup::Color.new(46, 111, 160)
  mat.alpha = 0.45
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Processing Tray (partial)"
  inst.layer = model.layers["Processing Tray"]

  # ═══ Walkways (near + far, partial) ═══
  defn = model.definitions.add("Walkways (near + far, partial)")
  ents = defn.entities
  # Walkway Near (partial)
  grp = ents.add_group
  grp.name = "Walkway Near (partial)"
  face = grp.entities.add_face([470.mm,0.mm,65.mm], [1600.mm,0.mm,65.mm], [1600.mm,300.mm,65.mm], [470.mm,300.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (partial)"] || model.materials.add("Walkway Near (partial)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  # Walkway Far (partial)
  grp = ents.add_group
  grp.name = "Walkway Far (partial)"
  face = grp.entities.add_face([470.mm,2062.mm,65.mm], [1600.mm,2062.mm,65.mm], [1600.mm,2362.mm,65.mm], [470.mm,2362.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Walkway Near (partial)"] || model.materials.add("Walkway Near (partial)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Walkways (near + far, partial)"
  inst.layer = model.layers["Walkways"]


# ── Transport pose: slide the panel-mounted components inward 880mm in X ──
# (the carriage's own moving parts are already offset via lt.sliding_carriage).
slide_tf = Geom::Transformation.translation([880.mm, 0, 0])
moving_tags = ["Hinge Panel", "Light Trap", "Fan B"]
entities.grep(Sketchup::ComponentInstance).each { |ci|
  ci.transform!(slide_tf) if moving_tags.include?(ci.layer.name)
}

model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags from earlier generator versions ──
keep_tags = ["Context", "Door Frame", "Hinge Panel", "Light Trap", "Sliding Carriage", "Fan B", "Processing Tray", "Walkways", "Cargo Doors"]
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
[["Transport — All", ["Context", "Door Frame", "Hinge Panel", "Light Trap", "Sliding Carriage", "Fan B", "Processing Tray", "Walkways", "Cargo Doors"]], ["Over Tray & Walkway", ["Hinge Panel", "Light Trap", "Sliding Carriage", "Processing Tray", "Walkways"]], ["Through the Doors", ["Cargo Doors", "Hinge Panel", "Light Trap", "Door Frame"]], ["Light-Trap Drum", ["Light Trap", "Hinge Panel"]]].each { |name, tags|
  model.layers.each { |l| l.visible = (l == default_layer || l.name == "Context" || tags.include?(l.name)) }
  page = model.pages.add(name)
  page.use_camera = true
}
model.layers.each { |l| l.visible = true }

model.commit_operation
{ success: true, model: "Light Trap (Transport)",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }.to_json
