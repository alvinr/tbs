model = Sketchup.active_model
model.start_operation("TBS-001 Light Trap", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# Idempotent rebuild: erase ALL prior instances (no scale figure in this model).
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

  # Left walkway (ghost, partial)
  grp = ents.add_group
  grp.name = "Left walkway (ghost, partial)"
  face = grp.entities.add_face([170.mm,481.mm,65.mm], [470.mm,481.mm,65.mm], [470.mm,1881.mm,65.mm], [170.mm,1881.mm,65.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(15.mm)
  mat = model.materials["Left walkway (ghost, partial)"] || model.materials.add("Left walkway (ghost, partial)")
  mat.color = Sketchup::Color.new(128, 128, 128)
  mat.alpha = 0.28
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Context"
  inst.layer = model.layers["Context"]

  # ═══ Fixed Door Frame ═══
  defn = model.definitions.add("Fixed Door Frame")
  ents = defn.entities
  # Door Frame threshold L
  grp = ents.add_group
  grp.name = "Door Frame threshold L"
  face = grp.entities.add_face([-50.mm,0.mm,0.mm], [0.mm,0.mm,0.mm], [0.mm,716.mm,0.mm], [-50.mm,716.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Door Frame threshold L"] || model.materials.add("Door Frame threshold L")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame threshold R
  grp = ents.add_group
  grp.name = "Door Frame threshold R"
  face = grp.entities.add_face([-50.mm,1646.mm,0.mm], [0.mm,1646.mm,0.mm], [0.mm,2362.mm,0.mm], [-50.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Door Frame threshold L"] || model.materials.add("Door Frame threshold L")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame top
  grp = ents.add_group
  grp.name = "Door Frame top"
  face = grp.entities.add_face([-50.mm,0.mm,2338.mm], [0.mm,0.mm,2338.mm], [0.mm,2362.mm,2338.mm], [-50.mm,2362.mm,2338.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Door Frame threshold L"] || model.materials.add("Door Frame threshold L")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame left stile
  grp = ents.add_group
  grp.name = "Door Frame left stile"
  face = grp.entities.add_face([-50.mm,0.mm,0.mm], [0.mm,0.mm,0.mm], [0.mm,50.mm,0.mm], [-50.mm,50.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Door Frame threshold L"] || model.materials.add("Door Frame threshold L")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame right stile
  grp = ents.add_group
  grp.name = "Door Frame right stile"
  face = grp.entities.add_face([-50.mm,2312.mm,0.mm], [0.mm,2312.mm,0.mm], [0.mm,2362.mm,0.mm], [-50.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Door Frame threshold L"] || model.materials.add("Door Frame threshold L")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame bottom seal lip L
  grp = ents.add_group
  grp.name = "Door Frame bottom seal lip L"
  face = grp.entities.add_face([-32.mm,0.mm,0.mm], [-20.mm,0.mm,0.mm], [-20.mm,716.mm,0.mm], [-32.mm,716.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(110.mm)
  mat = model.materials["Door Frame threshold L"] || model.materials.add("Door Frame threshold L")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame bottom seal lip R
  grp = ents.add_group
  grp.name = "Door Frame bottom seal lip R"
  face = grp.entities.add_face([-32.mm,1646.mm,0.mm], [-20.mm,1646.mm,0.mm], [-20.mm,2362.mm,0.mm], [-32.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(110.mm)
  mat = model.materials["Door Frame threshold L"] || model.materials.add("Door Frame threshold L")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # Door Frame top seal lip
  grp = ents.add_group
  grp.name = "Door Frame top seal lip"
  face = grp.entities.add_face([-32.mm,0.mm,2270.mm], [-20.mm,0.mm,2270.mm], [-20.mm,2362.mm,2270.mm], [-32.mm,2362.mm,2270.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(118.mm)
  mat = model.materials["Door Frame threshold L"] || model.materials.add("Door Frame threshold L")
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

  # ═══ Revolving Light-Trap Drum ═══
  defn = model.definitions.add("Revolving Light-Trap Drum")
  ents = defn.entities
  # LT Housing arc (near Yd)
  grp = ents.add_group
  grp.name = "LT Housing arc (near Yd)"
  ge = grp.entities
  face = ge.add_face([[344.72.mm,1470.25.mm,0], [333.98.mm,1482.59.mm,0], [322.79.mm,1494.54.mm,0], [311.18.mm,1506.06.mm,0], [299.16.mm,1517.16.mm,0], [286.74.mm,1527.81.mm,0], [273.94.mm,1538.01.mm,0], [260.78.mm,1547.73.mm,0], [247.28.mm,1556.97.mm,0], [233.45.mm,1565.71.mm,0], [219.31.mm,1573.94.mm,0], [204.88.mm,1581.66.mm,0], [190.18.mm,1588.84.mm,0], [175.23.mm,1595.48.mm,0], [160.04.mm,1601.58.mm,0], [144.65.mm,1607.12.mm,0], [129.06.mm,1612.1.mm,0], [113.3.mm,1616.5.mm,0], [97.4.mm,1620.33.mm,0], [81.36.mm,1623.58.mm,0], [65.22.mm,1626.25.mm,0], [48.99.mm,1628.33.mm,0], [32.7.mm,1629.81.mm,0], [16.36.mm,1630.7.mm,0], [0.mm,1631.mm,0], [-16.36.mm,1630.7.mm,0], [-32.7.mm,1629.81.mm,0], [-48.99.mm,1628.33.mm,0], [-65.22.mm,1626.25.mm,0], [-81.36.mm,1623.58.mm,0], [-97.4.mm,1620.33.mm,0], [-113.3.mm,1616.5.mm,0], [-129.06.mm,1612.1.mm,0], [-144.65.mm,1607.12.mm,0], [-160.04.mm,1601.58.mm,0], [-175.23.mm,1595.48.mm,0], [-190.18.mm,1588.84.mm,0], [-204.88.mm,1581.66.mm,0], [-219.31.mm,1573.94.mm,0], [-233.45.mm,1565.71.mm,0], [-247.28.mm,1556.97.mm,0], [-260.78.mm,1547.73.mm,0], [-273.94.mm,1538.01.mm,0], [-286.74.mm,1527.81.mm,0], [-299.16.mm,1517.16.mm,0], [-311.18.mm,1506.06.mm,0], [-322.79.mm,1494.54.mm,0], [-333.98.mm,1482.59.mm,0], [-344.72.mm,1470.25.mm,0], [-342.42.mm,1468.33.mm,0], [-331.75.mm,1480.58.mm,0], [-320.64.mm,1492.45.mm,0], [-309.11.mm,1503.9.mm,0], [-297.16.mm,1514.92.mm,0], [-284.83.mm,1525.5.mm,0], [-272.12.mm,1535.63.mm,0], [-259.04.mm,1545.29.mm,0], [-245.63.mm,1554.46.mm,0], [-231.89.mm,1563.15.mm,0], [-217.85.mm,1571.32.mm,0], [-203.51.mm,1578.98.mm,0], [-188.91.mm,1586.12.mm,0], [-174.06.mm,1592.72.mm,0], [-158.98.mm,1598.77.mm,0], [-143.68.mm,1604.28.mm,0], [-128.2.mm,1609.22.mm,0], [-112.55.mm,1613.6.mm,0], [-96.75.mm,1617.4.mm,0], [-80.82.mm,1620.63.mm,0], [-64.78.mm,1623.28.mm,0], [-48.66.mm,1625.34.mm,0], [-32.48.mm,1626.82.mm,0], [-16.25.mm,1627.7.mm,0], [0.mm,1628.mm,0], [16.25.mm,1627.7.mm,0], [32.48.mm,1626.82.mm,0], [48.66.mm,1625.34.mm,0], [64.78.mm,1623.28.mm,0], [80.82.mm,1620.63.mm,0], [96.75.mm,1617.4.mm,0], [112.55.mm,1613.6.mm,0], [128.2.mm,1609.22.mm,0], [143.68.mm,1604.28.mm,0], [158.98.mm,1598.77.mm,0], [174.06.mm,1592.72.mm,0], [188.91.mm,1586.12.mm,0], [203.51.mm,1578.98.mm,0], [217.85.mm,1571.32.mm,0], [231.89.mm,1563.15.mm,0], [245.63.mm,1554.46.mm,0], [259.04.mm,1545.29.mm,0], [272.12.mm,1535.63.mm,0], [284.83.mm,1525.5.mm,0], [297.16.mm,1514.92.mm,0], [309.11.mm,1503.9.mm,0], [320.64.mm,1492.45.mm,0], [331.75.mm,1480.58.mm,0], [342.42.mm,1468.33.mm,0]])
  face.reverse! if face.normal.z < 0
  face.pushpull(2200.mm)
  mat = model.materials["LT Housing arc (near Yd)"] || model.materials.add("LT Housing arc (near Yd)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.42
  grp.material = mat

  # LT Housing arc (far Yd)
  grp = ents.add_group
  grp.name = "LT Housing arc (far Yd)"
  ge = grp.entities
  face = ge.add_face([[-344.72.mm,891.75.mm,0], [-333.98.mm,879.41.mm,0], [-322.79.mm,867.46.mm,0], [-311.18.mm,855.94.mm,0], [-299.16.mm,844.84.mm,0], [-286.74.mm,834.19.mm,0], [-273.94.mm,823.99.mm,0], [-260.78.mm,814.27.mm,0], [-247.28.mm,805.03.mm,0], [-233.45.mm,796.29.mm,0], [-219.31.mm,788.06.mm,0], [-204.88.mm,780.34.mm,0], [-190.18.mm,773.16.mm,0], [-175.23.mm,766.52.mm,0], [-160.04.mm,760.42.mm,0], [-144.65.mm,754.88.mm,0], [-129.06.mm,749.9.mm,0], [-113.3.mm,745.5.mm,0], [-97.4.mm,741.67.mm,0], [-81.36.mm,738.42.mm,0], [-65.22.mm,735.75.mm,0], [-48.99.mm,733.67.mm,0], [-32.7.mm,732.19.mm,0], [-16.36.mm,731.3.mm,0], [0.mm,731.mm,0], [16.36.mm,731.3.mm,0], [32.7.mm,732.19.mm,0], [48.99.mm,733.67.mm,0], [65.22.mm,735.75.mm,0], [81.36.mm,738.42.mm,0], [97.4.mm,741.67.mm,0], [113.3.mm,745.5.mm,0], [129.06.mm,749.9.mm,0], [144.65.mm,754.88.mm,0], [160.04.mm,760.42.mm,0], [175.23.mm,766.52.mm,0], [190.18.mm,773.16.mm,0], [204.88.mm,780.34.mm,0], [219.31.mm,788.06.mm,0], [233.45.mm,796.29.mm,0], [247.28.mm,805.03.mm,0], [260.78.mm,814.27.mm,0], [273.94.mm,823.99.mm,0], [286.74.mm,834.19.mm,0], [299.16.mm,844.84.mm,0], [311.18.mm,855.94.mm,0], [322.79.mm,867.46.mm,0], [333.98.mm,879.41.mm,0], [344.72.mm,891.75.mm,0], [342.42.mm,893.67.mm,0], [331.75.mm,881.42.mm,0], [320.64.mm,869.55.mm,0], [309.11.mm,858.1.mm,0], [297.16.mm,847.08.mm,0], [284.83.mm,836.5.mm,0], [272.12.mm,826.37.mm,0], [259.04.mm,816.71.mm,0], [245.63.mm,807.54.mm,0], [231.89.mm,798.85.mm,0], [217.85.mm,790.68.mm,0], [203.51.mm,783.02.mm,0], [188.91.mm,775.88.mm,0], [174.06.mm,769.28.mm,0], [158.98.mm,763.23.mm,0], [143.68.mm,757.72.mm,0], [128.2.mm,752.78.mm,0], [112.55.mm,748.4.mm,0], [96.75.mm,744.6.mm,0], [80.82.mm,741.37.mm,0], [64.78.mm,738.72.mm,0], [48.66.mm,736.66.mm,0], [32.48.mm,735.18.mm,0], [16.25.mm,734.3.mm,0], [0.mm,734.mm,0], [-16.25.mm,734.3.mm,0], [-32.48.mm,735.18.mm,0], [-48.66.mm,736.66.mm,0], [-64.78.mm,738.72.mm,0], [-80.82.mm,741.37.mm,0], [-96.75.mm,744.6.mm,0], [-112.55.mm,748.4.mm,0], [-128.2.mm,752.78.mm,0], [-143.68.mm,757.72.mm,0], [-158.98.mm,763.23.mm,0], [-174.06.mm,769.28.mm,0], [-188.91.mm,775.88.mm,0], [-203.51.mm,783.02.mm,0], [-217.85.mm,790.68.mm,0], [-231.89.mm,798.85.mm,0], [-245.63.mm,807.54.mm,0], [-259.04.mm,816.71.mm,0], [-272.12.mm,826.37.mm,0], [-284.83.mm,836.5.mm,0], [-297.16.mm,847.08.mm,0], [-309.11.mm,858.1.mm,0], [-320.64.mm,869.55.mm,0], [-331.75.mm,881.42.mm,0], [-342.42.mm,893.67.mm,0]])
  face.reverse! if face.normal.z < 0
  face.pushpull(2200.mm)
  mat = model.materials["LT Housing arc (near Yd)"] || model.materials.add("LT Housing arc (near Yd)")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 0.42
  grp.material = mat

  # LT Drum C-shell
  grp = ents.add_group
  grp.name = "LT Drum C-shell"
  ge = grp.entities
  face = ge.add_face([[-330.93.mm,903.32.mm,0], [-301.mm,871.12.mm,0], [-267.94.mm,842.13.mm,0], [-232.11.mm,816.65.mm,0], [-193.88.mm,794.95.mm,0], [-153.64.mm,777.24.mm,0], [-111.81.mm,763.72.mm,0], [-68.82.mm,754.52.mm,0], [-25.12.mm,749.73.mm,0], [18.84.mm,749.41.mm,0], [62.61.mm,753.56.mm,0], [105.73.mm,762.14.mm,0], [147.75.mm,775.05.mm,0], [188.25.mm,792.17.mm,0], [226.79.mm,813.32.mm,0], [262.98.mm,838.27.mm,0], [296.46.mm,866.77.mm,0], [326.86.mm,898.53.mm,0], [353.87.mm,933.21.mm,0], [377.22.mm,970.46.mm,0], [396.67.mm,1009.89.mm,0], [412.01.mm,1051.1.mm,0], [423.08.mm,1093.64.mm,0], [429.76.mm,1137.09.mm,0], [432.mm,1181.mm,0], [429.76.mm,1224.91.mm,0], [423.08.mm,1268.36.mm,0], [412.01.mm,1310.9.mm,0], [396.67.mm,1352.11.mm,0], [377.22.mm,1391.54.mm,0], [353.87.mm,1428.79.mm,0], [326.86.mm,1463.47.mm,0], [296.46.mm,1495.23.mm,0], [262.98.mm,1523.73.mm,0], [226.79.mm,1548.68.mm,0], [188.25.mm,1569.83.mm,0], [147.75.mm,1586.95.mm,0], [105.73.mm,1599.86.mm,0], [62.61.mm,1608.44.mm,0], [18.84.mm,1612.59.mm,0], [-25.12.mm,1612.27.mm,0], [-68.82.mm,1607.48.mm,0], [-111.81.mm,1598.28.mm,0], [-153.64.mm,1584.76.mm,0], [-193.88.mm,1567.05.mm,0], [-232.11.mm,1545.35.mm,0], [-267.94.mm,1519.87.mm,0], [-301.mm,1490.88.mm,0], [-330.93.mm,1458.68.mm,0], [-328.63.mm,1456.76.mm,0], [-298.9.mm,1488.73.mm,0], [-266.08.mm,1517.51.mm,0], [-230.5.mm,1542.81.mm,0], [-192.53.mm,1564.37.mm,0], [-152.57.mm,1581.95.mm,0], [-111.03.mm,1595.38.mm,0], [-68.34.mm,1604.52.mm,0], [-24.94.mm,1609.27.mm,0], [18.71.mm,1609.59.mm,0], [62.18.mm,1605.47.mm,0], [104.99.mm,1596.95.mm,0], [146.73.mm,1584.13.mm,0], [186.94.mm,1567.13.mm,0], [225.21.mm,1546.13.mm,0], [261.16.mm,1521.35.mm,0], [294.4.mm,1493.04.mm,0], [324.59.mm,1461.51.mm,0], [351.42.mm,1427.06.mm,0], [374.61.mm,1390.07.mm,0], [393.91.mm,1350.92.mm,0], [409.14.mm,1310.mm,0], [420.14.mm,1267.75.mm,0], [426.78.mm,1224.6.mm,0], [429.mm,1181.mm,0], [426.78.mm,1137.4.mm,0], [420.14.mm,1094.25.mm,0], [409.14.mm,1052.mm,0], [393.91.mm,1011.08.mm,0], [374.61.mm,971.93.mm,0], [351.42.mm,934.94.mm,0], [324.59.mm,900.49.mm,0], [294.4.mm,868.96.mm,0], [261.16.mm,840.65.mm,0], [225.21.mm,815.87.mm,0], [186.94.mm,794.87.mm,0], [146.73.mm,777.87.mm,0], [104.99.mm,765.05.mm,0], [62.18.mm,756.53.mm,0], [18.71.mm,752.41.mm,0], [-24.94.mm,752.73.mm,0], [-68.34.mm,757.48.mm,0], [-111.03.mm,766.62.mm,0], [-152.57.mm,780.05.mm,0], [-192.53.mm,797.63.mm,0], [-230.5.mm,819.19.mm,0], [-266.08.mm,844.49.mm,0], [-298.9.mm,873.27.mm,0], [-328.63.mm,905.24.mm,0]])
  face.reverse! if face.normal.z < 0
  face.pushpull(2200.mm)
  mat = model.materials["LT Drum C-shell"] || model.materials.add("LT Drum C-shell")
  mat.color = Sketchup::Color.new(232, 224, 208)
  mat.alpha = 0.85
  grp.material = mat

  # LT Drum top cap
  grp = ents.add_group
  grp.name = "LT Drum top cap"
  ge = grp.entities
  circle = ge.add_circle([0.mm,1181.mm,2195.mm], [0,0,1], 432.mm, 24)
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
  circle = ge.add_circle([0.mm,1181.mm,0.mm], [0,0,1], 432.mm, 24)
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
  cface.pushpull(65.mm)
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
  circle = ge.add_circle([0.mm,1181.mm,0.mm], [0,0,1], 75.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(45.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Floor collar plate
  grp = ents.add_group
  grp.name = "LT Floor collar plate"
  face = grp.entities.add_face([-120.mm,1061.mm,0.mm], [120.mm,1061.mm,0.mm], [120.mm,1301.mm,0.mm], [-120.mm,1301.mm,0.mm])
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
  circle = ge.add_circle([357.mm,1181.mm,700.mm], [0,0,1], 15.mm, 24)
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
  face = grp.entities.add_face([357.mm,1175.mm,720.mm], [429.mm,1175.mm,720.mm], [429.mm,1187.mm,720.mm], [357.mm,1187.mm,720.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # LT Grab rail standoff
  grp = ents.add_group
  grp.name = "LT Grab rail standoff"
  face = grp.entities.add_face([357.mm,1175.mm,1080.mm], [429.mm,1175.mm,1080.mm], [429.mm,1187.mm,1080.mm], [357.mm,1187.mm,1080.mm])
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
  circle = ge.add_circle([-336.6765327507908.mm,1463.505154457234.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2200.mm)
  mat = model.materials["LT Drum opening brush seal"] || model.materials.add("LT Drum opening brush seal")
  mat.color = Sketchup::Color.new(126, 126, 118)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum opening brush seal
  grp = ents.add_group
  grp.name = "LT Drum opening brush seal"
  ge = grp.entities
  circle = ge.add_circle([-336.6765327507909.mm,898.4948455427659.mm,0.mm], [0,0,1], 7.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2200.mm)
  mat = model.materials["LT Drum opening brush seal"] || model.materials.add("LT Drum opening brush seal")
  mat.color = Sketchup::Color.new(126, 126, 118)
  mat.alpha = 1.0
  grp.material = mat

  # LT Drum top felt seal
  grp = ents.add_group
  grp.name = "LT Drum top felt seal"
  ge = grp.entities
  circle = ge.add_circle([0.mm,1181.mm,2192.mm], [0,0,1], 446.mm, 24)
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
  circle = ge.add_circle([0.mm,1181.mm,0.mm], [0,0,1], 446.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(8.mm)
  mat = model.materials["LT Drum opening brush seal"] || model.materials.add("LT Drum opening brush seal")
  mat.color = Sketchup::Color.new(126, 126, 118)
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
  mat = model.materials["Door Frame threshold L"] || model.materials.add("Door Frame threshold L")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # HGH20CA carriage L
  grp = ents.add_group
  grp.name = "HGH20CA carriage L"
  face = grp.entities.add_face([18.mm,631.mm,2330.mm], [62.mm,631.mm,2330.mm], [62.mm,675.mm,2330.mm], [18.mm,675.mm,2330.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["HGH20CA carriage L"] || model.materials.add("HGH20CA carriage L")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Suspension bracket L
  grp = ents.add_group
  grp.name = "Suspension bracket L"
  face = grp.entities.add_face([15.mm,633.mm,2300.mm], [75.mm,633.mm,2300.mm], [75.mm,673.mm,2300.mm], [15.mm,673.mm,2300.mm])
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
  mat = model.materials["Door Frame threshold L"] || model.materials.add("Door Frame threshold L")
  mat.color = Sketchup::Color.new(96, 96, 104)
  mat.alpha = 1.0
  grp.material = mat

  # HGH20CA carriage R
  grp = ents.add_group
  grp.name = "HGH20CA carriage R"
  face = grp.entities.add_face([18.mm,1687.mm,2330.mm], [62.mm,1687.mm,2330.mm], [62.mm,1731.mm,2330.mm], [18.mm,1731.mm,2330.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["HGH20CA carriage L"] || model.materials.add("HGH20CA carriage L")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Suspension bracket R
  grp = ents.add_group
  grp.name = "Suspension bracket R"
  face = grp.entities.add_face([15.mm,1689.mm,2300.mm], [75.mm,1689.mm,2300.mm], [75.mm,1729.mm,2300.mm], [15.mm,1729.mm,2300.mm])
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
  face = grp.entities.add_face([490.mm,635.mm,2288.mm], [550.mm,635.mm,2288.mm], [550.mm,671.mm,2288.mm], [490.mm,671.mm,2288.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Destaco clamp (transport) handle
  grp = ents.add_group
  grp.name = "Destaco clamp (transport) handle"
  face = grp.entities.add_face([500.mm,647.mm,2312.mm], [570.mm,647.mm,2312.mm], [570.mm,659.mm,2312.mm], [500.mm,659.mm,2312.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["HGH20CA carriage L"] || model.materials.add("HGH20CA carriage L")
  mat.color = Sketchup::Color.new(192, 64, 16)
  mat.alpha = 1.0
  grp.material = mat

  # Destaco clamp (transport) base
  grp = ents.add_group
  grp.name = "Destaco clamp (transport) base"
  face = grp.entities.add_face([490.mm,1691.mm,2288.mm], [550.mm,1691.mm,2288.mm], [550.mm,1727.mm,2288.mm], [490.mm,1727.mm,2288.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(24.mm)
  mat = model.materials["Piano hinge"] || model.materials.add("Piano hinge")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Destaco clamp (transport) handle
  grp = ents.add_group
  grp.name = "Destaco clamp (transport) handle"
  face = grp.entities.add_face([500.mm,1703.mm,2312.mm], [570.mm,1703.mm,2312.mm], [570.mm,1715.mm,2312.mm], [500.mm,1715.mm,2312.mm])
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
  mat = model.materials["Fan B (intake) fan blade up"] || model.materials.add("Fan B (intake) fan blade up")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade down
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade down"
  face = grp.entities.add_face([272.5.mm,1981.mm,534.mm], [278.5.mm,1981.mm,534.mm], [278.5.mm,2011.mm,534.mm], [272.5.mm,2011.mm,534.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.5.mm)
  mat = model.materials["Fan B (intake) fan blade up"] || model.materials.add("Fan B (intake) fan blade up")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade left
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade left"
  face = grp.entities.add_face([272.5.mm,1930.mm,585.mm], [278.5.mm,1930.mm,585.mm], [278.5.mm,1976.5.mm,585.mm], [272.5.mm,1976.5.mm,585.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Fan B (intake) fan blade up"] || model.materials.add("Fan B (intake) fan blade up")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Fan B (intake) fan blade right
  grp = ents.add_group
  grp.name = "Fan B (intake) fan blade right"
  face = grp.entities.add_face([272.5.mm,2015.5.mm,585.mm], [278.5.mm,2015.5.mm,585.mm], [278.5.mm,2062.mm,585.mm], [272.5.mm,2062.mm,585.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["Fan B (intake) fan blade up"] || model.materials.add("Fan B (intake) fan blade up")
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
