# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/ — do not edit this .rb directly.
model = Sketchup.active_model
model.start_operation("Pinhole-wall layout", true)
entities = model.active_entities
to_erase = entities.to_a.select { |e| e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text) || e.is_a?(Sketchup::ConstructionLine) || e.is_a?(Sketchup::ConstructionPoint) || e.is_a?(Sketchup::Edge) }
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each { |pg| model.pages.erase(pg) }
opts = model.options["UnitsOptions"]; opts["LengthUnit"]=2; opts["LengthFormat"]=0
# ── Sketchfab metadata — sketchfab dict fill-only-if-blank; name/desc forced when requested ──
model.name = "TBS-001 Water Model"
model.description = "The camera operates in remote locations with no municipal water or drainage. This document specifies a self-contained three-circuit water system that:\n\nStores sufficient clean water for 9\u201314 full-size prints between resupply runs on fresh Blue alone (~14 prints once Brown wash-2 recycling is counted \u2014 see \u00a7below) Recycles used wash water through a three-stage filter train, extending usable supply by approximately 40% Contains all waste water in a closed, transportable IBC for proper off-site disposal Runs entirely on 12V DC, compatible with a solar/battery off-grid power system."
model.set_attribute("sketchfab", "model_title", "TBS-001 Water Model") if model.get_attribute("sketchfab", "model_title").to_s.strip.empty?
model.set_attribute("sketchfab", "model_description", "The camera operates in remote locations with no municipal water or drainage. This document specifies a self-contained three-circuit water system that:\n\nStores sufficient clean water for 9\u201314 full-size prints between resupply runs on fresh Blue alone (~14 prints once Brown wash-2 recycling is counted \u2014 see \u00a7below) Recycles used wash water through a three-stage filter train, extending usable supply by approximately 40% Contains all waste water in a closed, transportable IBC for proper off-site disposal Runs entirely on 12V DC, compatible with a solar/battery off-grid power system.") if model.get_attribute("sketchfab", "model_description").to_s.strip.empty?
model.set_attribute("sketchfab", "model_id", "1dae932430924e9b993e153a16f485fc") if model.get_attribute("sketchfab", "model_id").to_s.strip.empty?
model.set_attribute("sketchfab", "model_tags", "sketchup") if model.get_attribute("sketchfab", "model_tags").to_s.strip.empty?

  model.layers.add('Backing') unless model.layers['Backing']
  model.layers.add('Backing Solid') unless model.layers['Backing Solid']
  model.layers.add('Context') unless model.layers['Context']
  model.layers.add('Corridor Drains') unless model.layers['Corridor Drains']
  model.layers.add('Corridor Equipment') unless model.layers['Corridor Equipment']
  model.layers.add('Corridor Frame') unless model.layers['Corridor Frame']
  model.layers.add('Corridor Panel') unless model.layers['Corridor Panel']
  model.layers.add('Corridor Panel Solid') unless model.layers['Corridor Panel Solid']
  model.layers.add('Corridor Plumbing') unless model.layers['Corridor Plumbing']
  model.layers.add('Film Plane') unless model.layers['Film Plane']
  model.layers.add('IBC') unless model.layers['IBC']
  model.layers.add('IBC Frame') unless model.layers['IBC Frame']
  model.layers.add('Kit') unless model.layers['Kit']
  model.layers.add('Labels') unless model.layers['Labels']
  model.layers.add('Labels Context') unless model.layers['Labels Context']
  model.layers.add('Pinhole') unless model.layers['Pinhole']
  model.layers.add('Pinhole Equipment') unless model.layers['Pinhole Equipment']
  model.layers.add('Power') unless model.layers['Power']
  model.layers.add('Processing Tray') unless model.layers['Processing Tray']
  model.layers.add('Ribbon Supports') unless model.layers['Ribbon Supports']
  model.layers.add('Scale') unless model.layers['Scale']
  model.layers.add('Spray Bar') unless model.layers['Spray Bar']
  model.layers.add('Supply') unless model.layers['Supply']
  model.layers.add('Walkway') unless model.layers['Walkway']
  # ═══ Context ═══
  defn = model.definitions.add("Context")
  ents = defn.entities
  # Pinhole wall
  grp = ents.add_group
  grp.name = "Pinhole wall"
  face = grp.entities.add_face([0.mm,-40.mm,0.mm], [5893.mm,-40.mm,0.mm], [5893.mm,0.mm,0.mm], [0.mm,0.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Pinhole wall"] || model.materials.add("Pinhole wall")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.3
  grp.material = mat

  # Floor
  grp = ents.add_group
  grp.name = "Floor"
  face = grp.entities.add_face([0.mm,0.mm,-40.mm], [5893.mm,0.mm,-40.mm], [5893.mm,2362.mm,-40.mm], [0.mm,2362.mm,-40.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Floor"] || model.materials.add("Floor")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.16
  grp.material = mat

  # Depth ref (Yd 600)
  grp = ents.add_group
  grp.name = "Depth ref (Yd 600)"
  face = grp.entities.add_face([0.mm,598.mm,0.mm], [5893.mm,598.mm,0.mm], [5893.mm,602.mm,0.mm], [0.mm,602.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["Depth ref (Yd 600)"] || model.materials.add("Depth ref (Yd 600)")
  mat.color = Sketchup::Color.new(32, 96, 160)
  mat.alpha = 0.1
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Context"
  inst.layer = model.layers["Context"]

  # ═══ Walkways + cantilevers + brackets ═══
  defn = model.definitions.add("Walkways + cantilevers + brackets")
  ents = defn.entities
  # Walkway Near (fixed, bump integral)
  grp = ents.add_group
  grp.name = "Walkway Near (fixed, bump integral)"
  face = grp.entities.add_face([470.mm,8.mm,115.mm], [4329.mm,8.mm,115.mm], [4329.mm,300.mm,115.mm], [3083.mm,300.mm,115.mm], [3083.mm,500.mm,115.mm], [1055.mm,500.mm,115.mm], [1055.mm,300.mm,115.mm], [470.mm,300.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (fixed, bump integral)"] || model.materials.add("Walkway Near (fixed, bump integral)")
  mat.color = Sketchup::Color.new(165, 165, 168)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far
  grp = ents.add_group
  grp.name = "Walkway Far"
  face = grp.entities.add_face([470.mm,2062.mm,115.mm], [4329.mm,2062.mm,115.mm], [4329.mm,2354.mm,115.mm], [470.mm,2354.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (fixed, bump integral)"] || model.materials.add("Walkway Near (fixed, bump integral)")
  mat.color = Sketchup::Color.new(165, 165, 168)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam X4329 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 upper"
  face = grp.entities.add_face([4329.mm,0.mm,95.mm], [4379.8.mm,0.mm,95.mm], [4379.8.mm,1812.mm,95.mm], [4329.mm,1812.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam X4329 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 lower"
  face = grp.entities.add_face([4329.mm,0.mm,93.mm], [4379.8.mm,0.mm,93.mm], [4379.8.mm,1046.mm,93.mm], [4329.mm,1046.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam X4329 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 lower"
  face = grp.entities.add_face([4329.mm,1096.8.mm,93.mm], [4379.8.mm,1096.8.mm,93.mm], [4379.8.mm,1266.mm,93.mm], [4329.mm,1266.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam X4329 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 lower"
  face = grp.entities.add_face([4329.mm,1316.8.mm,93.mm], [4379.8.mm,1316.8.mm,93.mm], [4379.8.mm,1812.mm,93.mm], [4329.mm,1812.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam inner ramp-out
  grp = ents.add_group
  grp.name = "RWk Long beam inner ramp-out"
  face = grp.entities.add_face([4329.mm,1812.mm,93.mm], [4379.8.mm,1812.mm,93.mm], [4479.8.mm,1912.mm,93.mm], [4429.mm,1912.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam X4429 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4429 upper"
  face = grp.entities.add_face([4429.mm,1912.mm,95.mm], [4479.8.mm,1912.mm,95.mm], [4479.8.mm,2062.mm,95.mm], [4429.mm,2062.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam X4429 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4429 lower"
  face = grp.entities.add_face([4429.mm,1912.mm,93.mm], [4479.8.mm,1912.mm,93.mm], [4479.8.mm,2062.mm,93.mm], [4429.mm,2062.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam inner ramp-in
  grp = ents.add_group
  grp.name = "RWk Long beam inner ramp-in"
  face = grp.entities.add_face([4429.mm,2062.mm,93.mm], [4479.8.mm,2062.mm,93.mm], [4379.8.mm,2162.mm,93.mm], [4329.mm,2162.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam X4329 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 upper"
  face = grp.entities.add_face([4329.mm,2162.mm,95.mm], [4379.8.mm,2162.mm,95.mm], [4379.8.mm,2362.mm,95.mm], [4329.mm,2362.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam X4329 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4329 lower"
  face = grp.entities.add_face([4329.mm,2162.mm,93.mm], [4379.8.mm,2162.mm,93.mm], [4379.8.mm,2362.mm,93.mm], [4329.mm,2362.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam X4578 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 upper"
  face = grp.entities.add_face([4578.2.mm,0.mm,95.mm], [4629.mm,0.mm,95.mm], [4629.mm,1093.mm,95.mm], [4578.2.mm,1093.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam X4578 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 upper"
  face = grp.entities.add_face([4578.2.mm,1149.mm,95.mm], [4629.mm,1149.mm,95.mm], [4629.mm,1177.mm,95.mm], [4578.2.mm,1177.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam X4578 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 upper"
  face = grp.entities.add_face([4578.2.mm,1211.mm,95.mm], [4629.mm,1211.mm,95.mm], [4629.mm,1224.mm,95.mm], [4578.2.mm,1224.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam X4578 upper
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 upper"
  face = grp.entities.add_face([4578.2.mm,1258.mm,95.mm], [4629.mm,1258.mm,95.mm], [4629.mm,2362.mm,95.mm], [4578.2.mm,2362.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam X4578 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 lower"
  face = grp.entities.add_face([4578.2.mm,0.mm,93.mm], [4629.mm,0.mm,93.mm], [4629.mm,1046.mm,93.mm], [4578.2.mm,1046.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam X4578 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 lower"
  face = grp.entities.add_face([4578.2.mm,1149.mm,93.mm], [4629.mm,1149.mm,93.mm], [4629.mm,1177.mm,93.mm], [4578.2.mm,1177.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam X4578 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 lower"
  face = grp.entities.add_face([4578.2.mm,1211.mm,93.mm], [4629.mm,1211.mm,93.mm], [4629.mm,1224.mm,93.mm], [4578.2.mm,1224.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam X4578 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 lower"
  face = grp.entities.add_face([4578.2.mm,1258.mm,93.mm], [4629.mm,1258.mm,93.mm], [4629.mm,1266.mm,93.mm], [4578.2.mm,1266.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam X4578 lower
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 lower"
  face = grp.entities.add_face([4578.2.mm,1316.8.mm,93.mm], [4629.mm,1316.8.mm,93.mm], [4629.mm,2362.mm,93.mm], [4578.2.mm,2362.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam X4578 notch web
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 notch web"
  face = grp.entities.add_face([4578.2.mm,1096.8.mm,93.mm], [4629.mm,1096.8.mm,93.mm], [4629.mm,1266.mm,93.mm], [4578.2.mm,1266.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(-1.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam X4578 notch web
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 notch web"
  face = grp.entities.add_face([4578.2.mm,1115.mm,93.mm], [4629.mm,1115.mm,93.mm], [4629.mm,1266.mm,93.mm], [4578.2.mm,1266.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(-1.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam X4578 notch web
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 notch web"
  face = grp.entities.add_face([4578.2.mm,1177.mm,93.mm], [4629.mm,1177.mm,93.mm], [4629.mm,1266.mm,93.mm], [4578.2.mm,1266.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(-1.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk Long beam X4578 notch web
  grp = ents.add_group
  grp.name = "RWk Long beam X4578 notch web"
  face = grp.entities.add_face([4578.2.mm,1224.mm,93.mm], [4629.mm,1224.mm,93.mm], [4629.mm,1266.mm,93.mm], [4578.2.mm,1266.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(-1.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk end beam Yd0
  grp = ents.add_group
  grp.name = "RWk end beam Yd0"
  face = grp.entities.add_face([4329.mm,0.mm,93.mm], [4629.mm,0.mm,93.mm], [4629.mm,50.8.mm,93.mm], [4329.mm,50.8.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk end beam Yd2311
  grp = ents.add_group
  grp.name = "RWk end beam Yd2311"
  face = grp.entities.add_face([4329.mm,2311.2.mm,93.mm], [4629.mm,2311.2.mm,93.mm], [4629.mm,2362.mm,93.mm], [4329.mm,2362.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk center cantilever Yd1046 lower
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 lower"
  face = grp.entities.add_face([4329.mm,1046.mm,93.mm], [4654.mm,1046.mm,93.mm], [4654.mm,1096.8.mm,93.mm], [4329.mm,1096.8.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk center cantilever Yd1046 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 upper"
  face = grp.entities.add_face([4379.8.mm,1046.mm,95.mm], [4578.2.mm,1046.mm,95.mm], [4578.2.mm,1096.8.mm,95.mm], [4379.8.mm,1096.8.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk center cantilever Yd1046 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 upper"
  face = grp.entities.add_face([4629.mm,1046.mm,95.mm], [4654.mm,1046.mm,95.mm], [4654.mm,1096.8.mm,95.mm], [4629.mm,1096.8.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk upright clamp Yd1046 Y1038
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1046 Y1038"
  face = grp.entities.add_face([4650.mm,1038.mm,68.mm], [4708.mm,1038.mm,68.mm], [4708.mm,1046.mm,68.mm], [4650.mm,1046.mm,68.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(77.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk upright clamp Yd1046 Y1096
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1046 Y1096"
  face = grp.entities.add_face([4650.mm,1096.8.mm,68.mm], [4708.mm,1096.8.mm,68.mm], [4708.mm,1104.8.mm,68.mm], [4650.mm,1104.8.mm,68.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(77.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk upright bolt M12 Yd1046 Z99
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1046 Z99"
  ge = grp.entities
  circle = ge.add_circle([4679.mm,1034.mm,99.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(74.8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk upright bolt M12 Yd1046 Z133
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1046 Z133"
  ge = grp.entities
  circle = ge.add_circle([4679.mm,1034.mm,133.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(74.8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk center cantilever Yd1266 lower
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 lower"
  face = grp.entities.add_face([4329.mm,1266.mm,93.mm], [4654.mm,1266.mm,93.mm], [4654.mm,1316.8.mm,93.mm], [4329.mm,1316.8.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk center cantilever Yd1266 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 upper"
  face = grp.entities.add_face([4379.8.mm,1266.mm,95.mm], [4578.2.mm,1266.mm,95.mm], [4578.2.mm,1316.8.mm,95.mm], [4379.8.mm,1316.8.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk center cantilever Yd1266 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 upper"
  face = grp.entities.add_face([4629.mm,1266.mm,95.mm], [4654.mm,1266.mm,95.mm], [4654.mm,1316.8.mm,95.mm], [4629.mm,1316.8.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk upright clamp Yd1266 Y1258
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1266 Y1258"
  face = grp.entities.add_face([4650.mm,1258.mm,68.mm], [4708.mm,1258.mm,68.mm], [4708.mm,1266.mm,68.mm], [4650.mm,1266.mm,68.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(77.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk upright clamp Yd1266 Y1316
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1266 Y1316"
  face = grp.entities.add_face([4650.mm,1316.8.mm,68.mm], [4708.mm,1316.8.mm,68.mm], [4708.mm,1324.8.mm,68.mm], [4650.mm,1324.8.mm,68.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(77.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk upright bolt M12 Yd1266 Z99
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1266 Z99"
  ge = grp.entities
  circle = ge.add_circle([4679.mm,1254.mm,99.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(74.8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk upright bolt M12 Yd1266 Z133
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1266 Z133"
  ge = grp.entities
  circle = ge.add_circle([4679.mm,1254.mm,133.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(74.8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk wall cleat plate (near)
  grp = ents.add_group
  grp.name = "RWk wall cleat plate (near)"
  face = grp.entities.add_face([4309.mm,0.mm,83.mm], [4399.mm,0.mm,83.mm], [4399.mm,8.mm,83.mm], [4309.mm,8.mm,83.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk wall cleat ext plate (near)
  grp = ents.add_group
  grp.name = "RWk wall cleat ext plate (near)"
  face = grp.entities.add_face([4309.mm,-48.mm,83.mm], [4399.mm,-48.mm,83.mm], [4399.mm,-40.mm,83.mm], [4309.mm,-40.mm,83.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk wall cleat shelf (near)
  grp = ents.add_group
  grp.name = "RWk wall cleat shelf (near)"
  face = grp.entities.add_face([4309.mm,0.mm,83.mm], [4399.mm,0.mm,83.mm], [4399.mm,55.mm,83.mm], [4309.mm,55.mm,83.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk wall bolt (near) Z99
  grp = ents.add_group
  grp.name = "RWk wall bolt (near) Z99"
  ge = grp.entities
  circle = ge.add_circle([4354.mm,-48.mm,99.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk wall bolt (near) Z109
  grp = ents.add_group
  grp.name = "RWk wall bolt (near) Z109"
  ge = grp.entities
  circle = ge.add_circle([4354.mm,-48.mm,109.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk wall cleat plate (far)
  grp = ents.add_group
  grp.name = "RWk wall cleat plate (far)"
  face = grp.entities.add_face([4309.mm,2354.mm,83.mm], [4399.mm,2354.mm,83.mm], [4399.mm,2362.mm,83.mm], [4309.mm,2362.mm,83.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk wall cleat ext plate (far)
  grp = ents.add_group
  grp.name = "RWk wall cleat ext plate (far)"
  face = grp.entities.add_face([4309.mm,2402.mm,83.mm], [4399.mm,2402.mm,83.mm], [4399.mm,2410.mm,83.mm], [4309.mm,2410.mm,83.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk wall cleat shelf (far)
  grp = ents.add_group
  grp.name = "RWk wall cleat shelf (far)"
  face = grp.entities.add_face([4309.mm,2307.mm,83.mm], [4399.mm,2307.mm,83.mm], [4399.mm,2362.mm,83.mm], [4309.mm,2362.mm,83.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk wall bolt (far) Z99
  grp = ents.add_group
  grp.name = "RWk wall bolt (far) Z99"
  ge = grp.entities
  circle = ge.add_circle([4354.mm,2354.mm,99.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk wall bolt (far) Z109
  grp = ents.add_group
  grp.name = "RWk wall bolt (far) Z109"
  ge = grp.entities
  circle = ge.add_circle([4354.mm,2354.mm,109.mm], [0,1,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Right walkway grate (cantilevered)
  grp = ents.add_group
  grp.name = "Right walkway grate (cantilevered)"
  face = grp.entities.add_face([4329.mm,0.mm,115.mm], [4629.mm,0.mm,115.mm], [4629.mm,2362.mm,115.mm], [4329.mm,2362.mm,115.mm], [4329.mm,2062.mm,115.mm], [4429.mm,2062.mm,115.mm], [4429.mm,1912.mm,115.mm], [4329.mm,1912.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Near (fixed, bump integral)"] || model.materials.add("Walkway Near (fixed, bump integral)")
  mat.color = Sketchup::Color.new(165, 165, 168)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Left (REMOVABLE — transport)
  grp = ents.add_group
  grp.name = "Walkway Left (REMOVABLE — transport)"
  face = grp.entities.add_face([170.mm,0.mm,115.mm], [170.mm,2362.mm,115.mm], [470.mm,2362.mm,115.mm], [470.mm,2062.mm,115.mm], [370.mm,2062.mm,115.mm], [370.mm,1912.mm,115.mm], [470.mm,1912.mm,115.mm], [470.mm,1560.mm,115.mm], [770.mm,1560.mm,115.mm], [770.mm,800.mm,115.mm], [470.mm,800.mm,115.mm], [470.mm,0.mm,115.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(25.mm)
  mat = model.materials["Walkway Left (REMOVABLE — transport)"] || model.materials.add("Walkway Left (REMOVABLE — transport)")
  mat.color = Sketchup::Color.new(191, 157, 127)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 1 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 plate"
  face = grp.entities.add_face([638.mm,0.mm,0.mm], [758.mm,0.mm,0.mm], [758.mm,8.mm,0.mm], [638.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([698.mm,-6.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([663.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([733.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 1 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 arm"
  face = grp.entities.add_face([694.mm,8.mm,105.mm], [702.mm,8.mm,105.mm], [702.mm,300.mm,105.mm], [694.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 1 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 gusset"
  ge = grp.entities
  f = ge.add_face([694.mm,8.mm,0.mm], [694.mm,8.mm,105.mm], [694.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 2 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) plate"
  face = grp.entities.add_face([1095.mm,0.mm,0.mm], [1215.mm,0.mm,0.mm], [1215.mm,10.mm,0.mm], [1095.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 2 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1120.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 2 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1190.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 2 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1120.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 2 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1190.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 2 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) arm"
  face = grp.entities.add_face([1150.mm,10.mm,103.mm], [1160.mm,10.mm,103.mm], [1160.mm,500.mm,103.mm], [1150.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 2 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([1150.mm,10.mm,0.mm], [1150.mm,10.mm,103.mm], [1150.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 3 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) plate"
  face = grp.entities.add_face([1552.mm,0.mm,0.mm], [1672.mm,0.mm,0.mm], [1672.mm,10.mm,0.mm], [1552.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 3 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1577.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 3 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1647.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 3 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1577.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 3 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1647.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 3 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) arm"
  face = grp.entities.add_face([1607.mm,10.mm,103.mm], [1617.mm,10.mm,103.mm], [1617.mm,500.mm,103.mm], [1607.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 3 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([1607.mm,10.mm,0.mm], [1607.mm,10.mm,103.mm], [1607.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 4 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) plate"
  face = grp.entities.add_face([2009.mm,0.mm,0.mm], [2129.mm,0.mm,0.mm], [2129.mm,10.mm,0.mm], [2009.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 4 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2034.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 4 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2104.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 4 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2034.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 4 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2104.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 4 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) arm"
  face = grp.entities.add_face([2064.mm,10.mm,103.mm], [2074.mm,10.mm,103.mm], [2074.mm,500.mm,103.mm], [2064.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 4 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([2064.mm,10.mm,0.mm], [2064.mm,10.mm,103.mm], [2064.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 5 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) plate"
  face = grp.entities.add_face([2466.mm,0.mm,0.mm], [2586.mm,0.mm,0.mm], [2586.mm,10.mm,0.mm], [2466.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 5 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2491.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 5 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2561.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 5 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2491.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 5 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2561.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 5 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) arm"
  face = grp.entities.add_face([2521.mm,10.mm,103.mm], [2531.mm,10.mm,103.mm], [2531.mm,500.mm,103.mm], [2521.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 5 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([2521.mm,10.mm,0.mm], [2521.mm,10.mm,103.mm], [2521.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 6 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 (widened) plate"
  face = grp.entities.add_face([2923.mm,0.mm,0.mm], [3043.mm,0.mm,0.mm], [3043.mm,10.mm,0.mm], [2923.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 6 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2948.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 6 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3018.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 6 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2948.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 6 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3018.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 6 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 (widened) arm"
  face = grp.entities.add_face([2978.mm,10.mm,103.mm], [2988.mm,10.mm,103.mm], [2988.mm,500.mm,103.mm], [2978.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 6 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([2978.mm,10.mm,0.mm], [2978.mm,10.mm,103.mm], [2978.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 7 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 plate"
  face = grp.entities.add_face([3380.mm,0.mm,0.mm], [3500.mm,0.mm,0.mm], [3500.mm,8.mm,0.mm], [3380.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3440.mm,-6.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3405.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3475.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 7 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 arm"
  face = grp.entities.add_face([3436.mm,8.mm,105.mm], [3444.mm,8.mm,105.mm], [3444.mm,300.mm,105.mm], [3436.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 7 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 gusset"
  ge = grp.entities
  f = ge.add_face([3436.mm,8.mm,0.mm], [3436.mm,8.mm,105.mm], [3436.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 8 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 plate"
  face = grp.entities.add_face([3837.mm,0.mm,0.mm], [3957.mm,0.mm,0.mm], [3957.mm,8.mm,0.mm], [3837.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3897.mm,-6.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3862.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3932.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 8 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 arm"
  face = grp.entities.add_face([3893.mm,8.mm,105.mm], [3901.mm,8.mm,105.mm], [3901.mm,300.mm,105.mm], [3893.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 8 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 gusset"
  ge = grp.entities
  f = ge.add_face([3893.mm,8.mm,0.mm], [3893.mm,8.mm,105.mm], [3893.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 1 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 plate"
  face = grp.entities.add_face([638.mm,2354.mm,0.mm], [758.mm,2354.mm,0.mm], [758.mm,2362.mm,0.mm], [638.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([698.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([663.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([733.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 1 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 arm"
  face = grp.entities.add_face([694.mm,2062.mm,105.mm], [702.mm,2062.mm,105.mm], [702.mm,2354.mm,105.mm], [694.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 1 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 gusset"
  ge = grp.entities
  f = ge.add_face([694.mm,2354.mm,0.mm], [694.mm,2354.mm,105.mm], [694.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 2 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 plate"
  face = grp.entities.add_face([1095.mm,2354.mm,0.mm], [1215.mm,2354.mm,0.mm], [1215.mm,2362.mm,0.mm], [1095.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 2 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1155.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 2 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1120.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 2 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1190.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 2 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 arm"
  face = grp.entities.add_face([1151.mm,2062.mm,105.mm], [1159.mm,2062.mm,105.mm], [1159.mm,2354.mm,105.mm], [1151.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 2 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 gusset"
  ge = grp.entities
  f = ge.add_face([1151.mm,2354.mm,0.mm], [1151.mm,2354.mm,105.mm], [1151.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 3 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 plate"
  face = grp.entities.add_face([1552.mm,2354.mm,0.mm], [1672.mm,2354.mm,0.mm], [1672.mm,2362.mm,0.mm], [1552.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 3 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1612.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 3 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1577.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 3 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1647.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 3 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 arm"
  face = grp.entities.add_face([1608.mm,2062.mm,105.mm], [1616.mm,2062.mm,105.mm], [1616.mm,2354.mm,105.mm], [1608.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 3 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 gusset"
  ge = grp.entities
  f = ge.add_face([1608.mm,2354.mm,0.mm], [1608.mm,2354.mm,105.mm], [1608.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 4 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 plate"
  face = grp.entities.add_face([2009.mm,2354.mm,0.mm], [2129.mm,2354.mm,0.mm], [2129.mm,2362.mm,0.mm], [2009.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 4 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2069.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 4 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2034.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 4 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2104.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 4 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 arm"
  face = grp.entities.add_face([2065.mm,2062.mm,105.mm], [2073.mm,2062.mm,105.mm], [2073.mm,2354.mm,105.mm], [2065.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 4 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 gusset"
  ge = grp.entities
  f = ge.add_face([2065.mm,2354.mm,0.mm], [2065.mm,2354.mm,105.mm], [2065.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 5 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 plate"
  face = grp.entities.add_face([2466.mm,2354.mm,0.mm], [2586.mm,2354.mm,0.mm], [2586.mm,2362.mm,0.mm], [2466.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 5 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2526.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 5 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2491.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 5 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2561.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 5 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 arm"
  face = grp.entities.add_face([2522.mm,2062.mm,105.mm], [2530.mm,2062.mm,105.mm], [2530.mm,2354.mm,105.mm], [2522.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 5 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 gusset"
  ge = grp.entities
  f = ge.add_face([2522.mm,2354.mm,0.mm], [2522.mm,2354.mm,105.mm], [2522.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 6 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 plate"
  face = grp.entities.add_face([2923.mm,2354.mm,0.mm], [3043.mm,2354.mm,0.mm], [3043.mm,2362.mm,0.mm], [2923.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 6 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2983.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 6 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2948.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 6 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3018.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 6 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 arm"
  face = grp.entities.add_face([2979.mm,2062.mm,105.mm], [2987.mm,2062.mm,105.mm], [2987.mm,2354.mm,105.mm], [2979.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 6 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 gusset"
  ge = grp.entities
  f = ge.add_face([2979.mm,2354.mm,0.mm], [2979.mm,2354.mm,105.mm], [2979.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 7 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 plate"
  face = grp.entities.add_face([3380.mm,2354.mm,0.mm], [3500.mm,2354.mm,0.mm], [3500.mm,2362.mm,0.mm], [3380.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3440.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3405.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3475.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 7 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 arm"
  face = grp.entities.add_face([3436.mm,2062.mm,105.mm], [3444.mm,2062.mm,105.mm], [3444.mm,2354.mm,105.mm], [3436.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 7 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 gusset"
  ge = grp.entities
  f = ge.add_face([3436.mm,2354.mm,0.mm], [3436.mm,2354.mm,105.mm], [3436.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 8 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 plate"
  face = grp.entities.add_face([3837.mm,2354.mm,0.mm], [3957.mm,2354.mm,0.mm], [3957.mm,2362.mm,0.mm], [3837.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3897.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3862.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3932.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 8 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 arm"
  face = grp.entities.add_face([3893.mm,2062.mm,105.mm], [3901.mm,2062.mm,105.mm], [3901.mm,2354.mm,105.mm], [3893.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 8 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 gusset"
  ge = grp.entities
  f = ge.add_face([3893.mm,2354.mm,0.mm], [3893.mm,2354.mm,105.mm], [3893.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Left cantilever 1 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 1 foot plate"
  face = grp.entities.add_face([38.mm,220.mm,0.mm], [166.mm,220.mm,0.mm], [166.mm,280.mm,0.mm], [38.mm,280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Left cantilever 1 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 1 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,220.mm,0.mm], [165.mm,220.mm,0.mm], [165.mm,280.mm,0.mm], [115.mm,280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Left cantilever 1 arm (to X470)
  grp = ents.add_group
  grp.name = "Left cantilever 1 arm (to X470)"
  face = grp.entities.add_face([165.mm,224.6.mm,93.mm], [470.mm,224.6.mm,93.mm], [470.mm,275.4.mm,93.mm], [165.mm,275.4.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Left cantilever 2 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 2 foot plate"
  face = grp.entities.add_face([38.mm,770.mm,0.mm], [166.mm,770.mm,0.mm], [166.mm,830.mm,0.mm], [38.mm,830.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Left cantilever 2 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 2 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,770.mm,0.mm], [165.mm,770.mm,0.mm], [165.mm,830.mm,0.mm], [115.mm,830.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Left cantilever 2 arm (to X770)
  grp = ents.add_group
  grp.name = "Left cantilever 2 arm (to X770)"
  face = grp.entities.add_face([165.mm,774.6.mm,93.mm], [770.mm,774.6.mm,93.mm], [770.mm,825.4.mm,93.mm], [165.mm,825.4.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Left cantilever 3 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 3 foot plate"
  face = grp.entities.add_face([38.mm,1150.mm,0.mm], [166.mm,1150.mm,0.mm], [166.mm,1210.mm,0.mm], [38.mm,1210.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Left cantilever 3 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 3 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,1150.mm,0.mm], [165.mm,1150.mm,0.mm], [165.mm,1210.mm,0.mm], [115.mm,1210.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Left cantilever 3 arm (to X770)
  grp = ents.add_group
  grp.name = "Left cantilever 3 arm (to X770)"
  face = grp.entities.add_face([165.mm,1154.6.mm,93.mm], [770.mm,1154.6.mm,93.mm], [770.mm,1205.3999999999999.mm,93.mm], [165.mm,1205.3999999999999.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Left cantilever 4 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 4 foot plate"
  face = grp.entities.add_face([38.mm,1530.mm,0.mm], [166.mm,1530.mm,0.mm], [166.mm,1590.mm,0.mm], [38.mm,1590.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Left cantilever 4 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 4 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,1530.mm,0.mm], [165.mm,1530.mm,0.mm], [165.mm,1590.mm,0.mm], [115.mm,1590.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Left cantilever 4 arm (to X770)
  grp = ents.add_group
  grp.name = "Left cantilever 4 arm (to X770)"
  face = grp.entities.add_face([165.mm,1534.6.mm,93.mm], [770.mm,1534.6.mm,93.mm], [770.mm,1585.3999999999999.mm,93.mm], [165.mm,1585.3999999999999.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Left cantilever 5 foot plate
  grp = ents.add_group
  grp.name = "Left cantilever 5 foot plate"
  face = grp.entities.add_face([38.mm,2080.mm,0.mm], [166.mm,2080.mm,0.mm], [166.mm,2140.mm,0.mm], [38.mm,2140.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Left cantilever 5 post (50x50x3 SHS)
  grp = ents.add_group
  grp.name = "Left cantilever 5 post (50x50x3 SHS)"
  face = grp.entities.add_face([115.mm,2080.mm,0.mm], [165.mm,2080.mm,0.mm], [165.mm,2140.mm,0.mm], [115.mm,2140.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(115.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Left cantilever 5 arm (to X470)
  grp = ents.add_group
  grp.name = "Left cantilever 5 arm (to X470)"
  face = grp.entities.add_face([165.mm,2084.6.mm,93.mm], [470.mm,2084.6.mm,93.mm], [470.mm,2135.4.mm,93.mm], [165.mm,2135.4.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 1 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 plate"
  face = grp.entities.add_face([638.mm,0.mm,0.mm], [758.mm,0.mm,0.mm], [758.mm,8.mm,0.mm], [638.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([698.mm,-6.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([663.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([733.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 1 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 arm"
  face = grp.entities.add_face([694.mm,8.mm,105.mm], [702.mm,8.mm,105.mm], [702.mm,300.mm,105.mm], [694.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 1 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 1 gusset"
  ge = grp.entities
  f = ge.add_face([694.mm,8.mm,0.mm], [694.mm,8.mm,105.mm], [694.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 2 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) plate"
  face = grp.entities.add_face([1095.mm,0.mm,0.mm], [1215.mm,0.mm,0.mm], [1215.mm,10.mm,0.mm], [1095.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 2 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1120.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 2 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1190.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 2 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1120.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 2 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1190.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 2 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) arm"
  face = grp.entities.add_face([1150.mm,10.mm,103.mm], [1160.mm,10.mm,103.mm], [1160.mm,500.mm,103.mm], [1150.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 2 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 2 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([1150.mm,10.mm,0.mm], [1150.mm,10.mm,103.mm], [1150.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 3 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) plate"
  face = grp.entities.add_face([1552.mm,0.mm,0.mm], [1672.mm,0.mm,0.mm], [1672.mm,10.mm,0.mm], [1552.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 3 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1577.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 3 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1647.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 3 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1577.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 3 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1647.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 3 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) arm"
  face = grp.entities.add_face([1607.mm,10.mm,103.mm], [1617.mm,10.mm,103.mm], [1617.mm,500.mm,103.mm], [1607.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 3 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 3 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([1607.mm,10.mm,0.mm], [1607.mm,10.mm,103.mm], [1607.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 4 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) plate"
  face = grp.entities.add_face([2009.mm,0.mm,0.mm], [2129.mm,0.mm,0.mm], [2129.mm,10.mm,0.mm], [2009.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 4 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2034.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 4 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2104.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 4 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2034.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 4 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2104.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 4 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) arm"
  face = grp.entities.add_face([2064.mm,10.mm,103.mm], [2074.mm,10.mm,103.mm], [2074.mm,500.mm,103.mm], [2064.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 4 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 4 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([2064.mm,10.mm,0.mm], [2064.mm,10.mm,103.mm], [2064.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 5 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) plate"
  face = grp.entities.add_face([2466.mm,0.mm,0.mm], [2586.mm,0.mm,0.mm], [2586.mm,10.mm,0.mm], [2466.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 5 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2491.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 5 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2561.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 5 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2491.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 5 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2561.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 5 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) arm"
  face = grp.entities.add_face([2521.mm,10.mm,103.mm], [2531.mm,10.mm,103.mm], [2531.mm,500.mm,103.mm], [2521.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 5 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 5 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([2521.mm,10.mm,0.mm], [2521.mm,10.mm,103.mm], [2521.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 6 (widened) plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 (widened) plate"
  face = grp.entities.add_face([2923.mm,0.mm,0.mm], [3043.mm,0.mm,0.mm], [3043.mm,10.mm,0.mm], [2923.mm,10.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(200.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 6 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2948.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 6 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3018.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 6 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2948.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 6 (widened) bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 (widened) bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3018.mm,-6.mm,160.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(22.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 6 (widened) arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 (widened) arm"
  face = grp.entities.add_face([2978.mm,10.mm,103.mm], [2988.mm,10.mm,103.mm], [2988.mm,500.mm,103.mm], [2978.mm,500.mm,103.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 6 (widened) gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 6 (widened) gusset"
  ge = grp.entities
  f = ge.add_face([2978.mm,10.mm,0.mm], [2978.mm,10.mm,103.mm], [2978.mm,70.mm,103.mm])
  f.pushpull(-10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 7 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 plate"
  face = grp.entities.add_face([3380.mm,0.mm,0.mm], [3500.mm,0.mm,0.mm], [3500.mm,8.mm,0.mm], [3380.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3440.mm,-6.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3405.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3475.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 7 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 arm"
  face = grp.entities.add_face([3436.mm,8.mm,105.mm], [3444.mm,8.mm,105.mm], [3444.mm,300.mm,105.mm], [3436.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 7 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 7 gusset"
  ge = grp.entities
  f = ge.add_face([3436.mm,8.mm,0.mm], [3436.mm,8.mm,105.mm], [3436.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 8 plate
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 plate"
  face = grp.entities.add_face([3837.mm,0.mm,0.mm], [3957.mm,0.mm,0.mm], [3957.mm,8.mm,0.mm], [3837.mm,8.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3897.mm,-6.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3862.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3932.mm,-6.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 8 arm
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 arm"
  face = grp.entities.add_face([3893.mm,8.mm,105.mm], [3901.mm,8.mm,105.mm], [3901.mm,300.mm,105.mm], [3893.mm,300.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Near bracket 8 gusset
  grp = ents.add_group
  grp.name = "Walkway Near bracket 8 gusset"
  ge = grp.entities
  f = ge.add_face([3893.mm,8.mm,0.mm], [3893.mm,8.mm,105.mm], [3893.mm,70.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 1 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 plate"
  face = grp.entities.add_face([638.mm,2354.mm,0.mm], [758.mm,2354.mm,0.mm], [758.mm,2362.mm,0.mm], [638.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([698.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([663.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 1 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([733.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 1 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 arm"
  face = grp.entities.add_face([694.mm,2062.mm,105.mm], [702.mm,2062.mm,105.mm], [702.mm,2354.mm,105.mm], [694.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 1 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 1 gusset"
  ge = grp.entities
  f = ge.add_face([694.mm,2354.mm,0.mm], [694.mm,2354.mm,105.mm], [694.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 2 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 plate"
  face = grp.entities.add_face([1095.mm,2354.mm,0.mm], [1215.mm,2354.mm,0.mm], [1215.mm,2362.mm,0.mm], [1095.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 2 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1155.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 2 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1120.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 2 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1190.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 2 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 arm"
  face = grp.entities.add_face([1151.mm,2062.mm,105.mm], [1159.mm,2062.mm,105.mm], [1159.mm,2354.mm,105.mm], [1151.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 2 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 2 gusset"
  ge = grp.entities
  f = ge.add_face([1151.mm,2354.mm,0.mm], [1151.mm,2354.mm,105.mm], [1151.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 3 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 plate"
  face = grp.entities.add_face([1552.mm,2354.mm,0.mm], [1672.mm,2354.mm,0.mm], [1672.mm,2362.mm,0.mm], [1552.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 3 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1612.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 3 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1577.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 3 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([1647.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 3 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 arm"
  face = grp.entities.add_face([1608.mm,2062.mm,105.mm], [1616.mm,2062.mm,105.mm], [1616.mm,2354.mm,105.mm], [1608.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 3 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 3 gusset"
  ge = grp.entities
  f = ge.add_face([1608.mm,2354.mm,0.mm], [1608.mm,2354.mm,105.mm], [1608.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 4 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 plate"
  face = grp.entities.add_face([2009.mm,2354.mm,0.mm], [2129.mm,2354.mm,0.mm], [2129.mm,2362.mm,0.mm], [2009.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 4 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2069.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 4 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2034.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 4 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2104.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 4 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 arm"
  face = grp.entities.add_face([2065.mm,2062.mm,105.mm], [2073.mm,2062.mm,105.mm], [2073.mm,2354.mm,105.mm], [2065.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 4 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 4 gusset"
  ge = grp.entities
  f = ge.add_face([2065.mm,2354.mm,0.mm], [2065.mm,2354.mm,105.mm], [2065.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 5 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 plate"
  face = grp.entities.add_face([2466.mm,2354.mm,0.mm], [2586.mm,2354.mm,0.mm], [2586.mm,2362.mm,0.mm], [2466.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 5 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2526.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 5 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2491.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 5 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2561.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 5 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 arm"
  face = grp.entities.add_face([2522.mm,2062.mm,105.mm], [2530.mm,2062.mm,105.mm], [2530.mm,2354.mm,105.mm], [2522.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 5 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 5 gusset"
  ge = grp.entities
  f = ge.add_face([2522.mm,2354.mm,0.mm], [2522.mm,2354.mm,105.mm], [2522.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 6 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 plate"
  face = grp.entities.add_face([2923.mm,2354.mm,0.mm], [3043.mm,2354.mm,0.mm], [3043.mm,2362.mm,0.mm], [2923.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 6 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2983.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 6 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([2948.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 6 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3018.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 6 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 arm"
  face = grp.entities.add_face([2979.mm,2062.mm,105.mm], [2987.mm,2062.mm,105.mm], [2987.mm,2354.mm,105.mm], [2979.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 6 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 6 gusset"
  ge = grp.entities
  f = ge.add_face([2979.mm,2354.mm,0.mm], [2979.mm,2354.mm,105.mm], [2979.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 7 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 plate"
  face = grp.entities.add_face([3380.mm,2354.mm,0.mm], [3500.mm,2354.mm,0.mm], [3500.mm,2362.mm,0.mm], [3380.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3440.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3405.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 7 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3475.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 7 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 arm"
  face = grp.entities.add_face([3436.mm,2062.mm,105.mm], [3444.mm,2062.mm,105.mm], [3444.mm,2354.mm,105.mm], [3436.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 7 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 7 gusset"
  ge = grp.entities
  f = ge.add_face([3436.mm,2354.mm,0.mm], [3436.mm,2354.mm,105.mm], [3436.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 8 plate
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 plate"
  face = grp.entities.add_face([3837.mm,2354.mm,0.mm], [3957.mm,2354.mm,0.mm], [3957.mm,2362.mm,0.mm], [3837.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3897.mm,2348.mm,120.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3862.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 8 bolt M12
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 bolt M12"
  ge = grp.entities
  circle = ge.add_circle([3932.mm,2348.mm,40.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(20.mm)
  mat = model.materials["Walkway Near bracket 1 bolt M12"] || model.materials.add("Walkway Near bracket 1 bolt M12")
  mat.color = Sketchup::Color.new(152, 152, 158)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 8 arm
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 arm"
  face = grp.entities.add_face([3893.mm,2062.mm,105.mm], [3901.mm,2062.mm,105.mm], [3901.mm,2354.mm,105.mm], [3893.mm,2354.mm,105.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Walkway Far bracket 8 gusset
  grp = ents.add_group
  grp.name = "Walkway Far bracket 8 gusset"
  ge = grp.entities
  f = ge.add_face([3893.mm,2354.mm,0.mm], [3893.mm,2354.mm,105.mm], [3893.mm,2292.mm,105.mm])
  f.pushpull(-8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk center cantilever Yd1046 lower
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 lower"
  face = grp.entities.add_face([4329.mm,1046.mm,93.mm], [4654.mm,1046.mm,93.mm], [4654.mm,1096.8.mm,93.mm], [4329.mm,1096.8.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk center cantilever Yd1046 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 upper"
  face = grp.entities.add_face([4379.8.mm,1046.mm,95.mm], [4578.2.mm,1046.mm,95.mm], [4578.2.mm,1096.8.mm,95.mm], [4379.8.mm,1096.8.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk center cantilever Yd1046 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1046 upper"
  face = grp.entities.add_face([4629.mm,1046.mm,95.mm], [4654.mm,1046.mm,95.mm], [4654.mm,1096.8.mm,95.mm], [4629.mm,1096.8.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk upright clamp Yd1046 Y1038
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1046 Y1038"
  face = grp.entities.add_face([4650.mm,1038.mm,68.mm], [4708.mm,1038.mm,68.mm], [4708.mm,1046.mm,68.mm], [4650.mm,1046.mm,68.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(77.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk upright clamp Yd1046 Y1096
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1046 Y1096"
  face = grp.entities.add_face([4650.mm,1096.8.mm,68.mm], [4708.mm,1096.8.mm,68.mm], [4708.mm,1104.8.mm,68.mm], [4650.mm,1104.8.mm,68.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(77.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk upright bolt M12 Yd1046 Z99
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1046 Z99"
  ge = grp.entities
  circle = ge.add_circle([4679.mm,1034.mm,99.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(74.8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk upright bolt M12 Yd1046 Z133
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1046 Z133"
  ge = grp.entities
  circle = ge.add_circle([4679.mm,1034.mm,133.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(74.8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk center cantilever Yd1266 lower
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 lower"
  face = grp.entities.add_face([4329.mm,1266.mm,93.mm], [4654.mm,1266.mm,93.mm], [4654.mm,1316.8.mm,93.mm], [4329.mm,1316.8.mm,93.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk center cantilever Yd1266 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 upper"
  face = grp.entities.add_face([4379.8.mm,1266.mm,95.mm], [4578.2.mm,1266.mm,95.mm], [4578.2.mm,1316.8.mm,95.mm], [4379.8.mm,1316.8.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk center cantilever Yd1266 upper
  grp = ents.add_group
  grp.name = "RWk center cantilever Yd1266 upper"
  face = grp.entities.add_face([4629.mm,1266.mm,95.mm], [4654.mm,1266.mm,95.mm], [4654.mm,1316.8.mm,95.mm], [4629.mm,1316.8.mm,95.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(20.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk upright clamp Yd1266 Y1258
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1266 Y1258"
  face = grp.entities.add_face([4650.mm,1258.mm,68.mm], [4708.mm,1258.mm,68.mm], [4708.mm,1266.mm,68.mm], [4650.mm,1266.mm,68.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(77.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk upright clamp Yd1266 Y1316
  grp = ents.add_group
  grp.name = "RWk upright clamp Yd1266 Y1316"
  face = grp.entities.add_face([4650.mm,1316.8.mm,68.mm], [4708.mm,1316.8.mm,68.mm], [4708.mm,1324.8.mm,68.mm], [4650.mm,1324.8.mm,68.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(77.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk upright bolt M12 Yd1266 Z99
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1266 Z99"
  ge = grp.entities
  circle = ge.add_circle([4679.mm,1254.mm,99.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(74.8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # RWk upright bolt M12 Yd1266 Z133
  grp = ents.add_group
  grp.name = "RWk upright bolt M12 Yd1266 Z133"
  ge = grp.entities
  circle = ge.add_circle([4679.mm,1254.mm,133.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(74.8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Walkways + cantilevers + brackets"
  inst.layer = model.layers["Walkway"]

  # ═══ Film-plane support beams ═══
  defn = model.definitions.add("Film-plane support beams")
  ents = defn.entities
  # FP support beam R-bot
  grp = ents.add_group
  grp.name = "FP support beam R-bot"
  face = grp.entities.add_face([4609.mm,0.mm,160.mm], [4649.mm,0.mm,160.mm], [4649.mm,2362.mm,160.mm], [4609.mm,2362.mm,160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # FP support beam R-top
  grp = ents.add_group
  grp.name = "FP support beam R-top"
  face = grp.entities.add_face([4609.mm,0.mm,2204.mm], [4649.mm,0.mm,2204.mm], [4649.mm,2362.mm,2204.mm], [4609.mm,2362.mm,2204.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle back-plate TR near
  grp = ents.add_group
  grp.name = "Saddle back-plate TR near"
  face = grp.entities.add_face([4534.mm,0.mm,2129.mm], [4684.mm,0.mm,2129.mm], [4684.mm,8.mm,2129.mm], [4534.mm,8.mm,2129.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle OUTSIDE plate TR near
  grp = ents.add_group
  grp.name = "Saddle OUTSIDE plate TR near"
  face = grp.entities.add_face([4534.mm,-48.mm,2129.mm], [4684.mm,-48.mm,2129.mm], [4684.mm,-40.mm,2129.mm], [4534.mm,-40.mm,2129.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle seat TR near
  grp = ents.add_group
  grp.name = "Saddle seat TR near"
  face = grp.entities.add_face([4585.mm,0.mm,2194.mm], [4633.mm,0.mm,2194.mm], [4633.mm,110.mm,2194.mm], [4585.mm,110.mm,2194.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle gusset TR near
  grp = ents.add_group
  grp.name = "Saddle gusset TR near"
  ge = grp.entities
  f = ge.add_face([4609.mm,110.mm,2194.mm], [4609.mm,0.mm,2194.mm], [4609.mm,0.mm,2074.mm])
  f.pushpull(8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle wall bolt M12 TR near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR near"
  ge = grp.entities
  circle = ge.add_circle([4559.mm,-48.mm,2154.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle wall bolt M12 TR near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR near"
  ge = grp.entities
  circle = ge.add_circle([4559.mm,-48.mm,2254.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle wall bolt M12 TR near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR near"
  ge = grp.entities
  circle = ge.add_circle([4659.mm,-48.mm,2154.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle wall bolt M12 TR near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR near"
  ge = grp.entities
  circle = ge.add_circle([4659.mm,-48.mm,2254.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Rail fixing bolt TR near
  grp = ents.add_group
  grp.name = "Rail fixing bolt TR near"
  ge = grp.entities
  circle = ge.add_circle([4609.mm,25.mm,2204.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Rail fixing bolt TR near
  grp = ents.add_group
  grp.name = "Rail fixing bolt TR near"
  ge = grp.entities
  circle = ge.add_circle([4609.mm,85.mm,2204.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle back-plate TR far
  grp = ents.add_group
  grp.name = "Saddle back-plate TR far"
  face = grp.entities.add_face([4534.mm,2354.mm,2129.mm], [4684.mm,2354.mm,2129.mm], [4684.mm,2362.mm,2129.mm], [4534.mm,2362.mm,2129.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle OUTSIDE plate TR far
  grp = ents.add_group
  grp.name = "Saddle OUTSIDE plate TR far"
  face = grp.entities.add_face([4534.mm,2402.mm,2129.mm], [4684.mm,2402.mm,2129.mm], [4684.mm,2410.mm,2129.mm], [4534.mm,2410.mm,2129.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle seat TR far
  grp = ents.add_group
  grp.name = "Saddle seat TR far"
  face = grp.entities.add_face([4585.mm,2252.mm,2194.mm], [4633.mm,2252.mm,2194.mm], [4633.mm,2362.mm,2194.mm], [4585.mm,2362.mm,2194.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle gusset TR far
  grp = ents.add_group
  grp.name = "Saddle gusset TR far"
  ge = grp.entities
  f = ge.add_face([4609.mm,2252.mm,2194.mm], [4609.mm,2362.mm,2194.mm], [4609.mm,2362.mm,2074.mm])
  f.pushpull(8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle wall bolt M12 TR far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR far"
  ge = grp.entities
  circle = ge.add_circle([4559.mm,2354.mm,2154.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle wall bolt M12 TR far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR far"
  ge = grp.entities
  circle = ge.add_circle([4559.mm,2354.mm,2254.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle wall bolt M12 TR far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR far"
  ge = grp.entities
  circle = ge.add_circle([4659.mm,2354.mm,2154.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle wall bolt M12 TR far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 TR far"
  ge = grp.entities
  circle = ge.add_circle([4659.mm,2354.mm,2254.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Rail fixing bolt TR far
  grp = ents.add_group
  grp.name = "Rail fixing bolt TR far"
  ge = grp.entities
  circle = ge.add_circle([4609.mm,2277.mm,2204.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Rail fixing bolt TR far
  grp = ents.add_group
  grp.name = "Rail fixing bolt TR far"
  ge = grp.entities
  circle = ge.add_circle([4609.mm,2337.mm,2204.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle back-plate BR near
  grp = ents.add_group
  grp.name = "Saddle back-plate BR near"
  face = grp.entities.add_face([4534.mm,0.mm,85.mm], [4684.mm,0.mm,85.mm], [4684.mm,8.mm,85.mm], [4534.mm,8.mm,85.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle OUTSIDE plate BR near
  grp = ents.add_group
  grp.name = "Saddle OUTSIDE plate BR near"
  face = grp.entities.add_face([4534.mm,-48.mm,85.mm], [4684.mm,-48.mm,85.mm], [4684.mm,-40.mm,85.mm], [4534.mm,-40.mm,85.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle seat BR near
  grp = ents.add_group
  grp.name = "Saddle seat BR near"
  face = grp.entities.add_face([4585.mm,0.mm,150.mm], [4633.mm,0.mm,150.mm], [4633.mm,110.mm,150.mm], [4585.mm,110.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle gusset BR near
  grp = ents.add_group
  grp.name = "Saddle gusset BR near"
  ge = grp.entities
  f = ge.add_face([4609.mm,110.mm,150.mm], [4609.mm,0.mm,150.mm], [4609.mm,0.mm,30.mm])
  f.pushpull(8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle wall bolt M12 BR near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BR near"
  ge = grp.entities
  circle = ge.add_circle([4559.mm,-48.mm,110.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle wall bolt M12 BR near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BR near"
  ge = grp.entities
  circle = ge.add_circle([4559.mm,-48.mm,210.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle wall bolt M12 BR near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BR near"
  ge = grp.entities
  circle = ge.add_circle([4659.mm,-48.mm,110.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle wall bolt M12 BR near
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BR near"
  ge = grp.entities
  circle = ge.add_circle([4659.mm,-48.mm,210.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Rail fixing bolt BR near
  grp = ents.add_group
  grp.name = "Rail fixing bolt BR near"
  ge = grp.entities
  circle = ge.add_circle([4609.mm,25.mm,160.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Rail fixing bolt BR near
  grp = ents.add_group
  grp.name = "Rail fixing bolt BR near"
  ge = grp.entities
  circle = ge.add_circle([4609.mm,85.mm,160.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle back-plate BR far
  grp = ents.add_group
  grp.name = "Saddle back-plate BR far"
  face = grp.entities.add_face([4534.mm,2354.mm,85.mm], [4684.mm,2354.mm,85.mm], [4684.mm,2362.mm,85.mm], [4534.mm,2362.mm,85.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle OUTSIDE plate BR far
  grp = ents.add_group
  grp.name = "Saddle OUTSIDE plate BR far"
  face = grp.entities.add_face([4534.mm,2402.mm,85.mm], [4684.mm,2402.mm,85.mm], [4684.mm,2410.mm,85.mm], [4534.mm,2410.mm,85.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(150.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle seat BR far
  grp = ents.add_group
  grp.name = "Saddle seat BR far"
  face = grp.entities.add_face([4585.mm,2252.mm,150.mm], [4633.mm,2252.mm,150.mm], [4633.mm,2362.mm,150.mm], [4585.mm,2362.mm,150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle gusset BR far
  grp = ents.add_group
  grp.name = "Saddle gusset BR far"
  ge = grp.entities
  f = ge.add_face([4609.mm,2252.mm,150.mm], [4609.mm,2362.mm,150.mm], [4609.mm,2362.mm,30.mm])
  f.pushpull(8.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle wall bolt M12 BR far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BR far"
  ge = grp.entities
  circle = ge.add_circle([4559.mm,2354.mm,110.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle wall bolt M12 BR far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BR far"
  ge = grp.entities
  circle = ge.add_circle([4559.mm,2354.mm,210.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle wall bolt M12 BR far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BR far"
  ge = grp.entities
  circle = ge.add_circle([4659.mm,2354.mm,110.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Saddle wall bolt M12 BR far
  grp = ents.add_group
  grp.name = "Saddle wall bolt M12 BR far"
  ge = grp.entities
  circle = ge.add_circle([4659.mm,2354.mm,210.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(56.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Rail fixing bolt BR far
  grp = ents.add_group
  grp.name = "Rail fixing bolt BR far"
  ge = grp.entities
  circle = ge.add_circle([4609.mm,2277.mm,160.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Rail fixing bolt BR far
  grp = ents.add_group
  grp.name = "Rail fixing bolt BR far"
  ge = grp.entities
  circle = ge.add_circle([4609.mm,2337.mm,160.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Film-plane support beams"
  inst.layer = model.layers["Film Plane"]

  # ═══ Processing tray (ghost) ═══
  defn = model.definitions.add("Processing tray (ghost)")
  ents = defn.entities
  # Tray Shim Base
  grp = ents.add_group
  grp.name = "Tray Shim Base"
  face = grp.entities.add_face([170.mm,80.mm,0.mm], [4629.mm,80.mm,0.mm], [4629.mm,2280.mm,0.mm], [170.mm,2280.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(18.mm)
  mat = model.materials["Tray Shim Base"] || model.materials.add("Tray Shim Base")
  mat.color = Sketchup::Color.new(199, 196, 193)
  mat.alpha = 0.9
  grp.material = mat

  # Processing Tray Floor A
  grp = ents.add_group
  grp.name = "Processing Tray Floor A"
  ge = grp.entities
  f = ge.add_face([170.mm,80.mm,20.mm], [4629.mm,80.mm,20.mm], [4629.mm,2280.mm,31.mm])
  f.pushpull(-2.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(179, 188, 197)
  mat.alpha = 0.18
  grp.material = mat

  # Processing Tray Floor B
  grp = ents.add_group
  grp.name = "Processing Tray Floor B"
  ge = grp.entities
  f = ge.add_face([170.mm,80.mm,20.mm], [4629.mm,2280.mm,31.mm], [170.mm,2280.mm,31.mm])
  f.pushpull(-2.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(179, 188, 197)
  mat.alpha = 0.18
  grp.material = mat

  # Tray Rim Near
  grp = ents.add_group
  grp.name = "Tray Rim Near"
  face = grp.entities.add_face([170.mm,80.mm,20.mm], [4629.mm,80.mm,20.mm], [4629.mm,82.mm,20.mm], [170.mm,82.mm,20.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(179, 188, 197)
  mat.alpha = 0.18
  grp.material = mat

  # Tray Rim Far
  grp = ents.add_group
  grp.name = "Tray Rim Far"
  face = grp.entities.add_face([170.mm,2278.mm,31.mm], [4629.mm,2278.mm,31.mm], [4629.mm,2280.mm,31.mm], [170.mm,2280.mm,31.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(179, 188, 197)
  mat.alpha = 0.18
  grp.material = mat

  # Tray Rim Left
  grp = ents.add_group
  grp.name = "Tray Rim Left"
  face = grp.entities.add_face([170.mm,80.mm,25.5.mm], [172.mm,80.mm,25.5.mm], [172.mm,2280.mm,25.5.mm], [170.mm,2280.mm,25.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(179, 188, 197)
  mat.alpha = 0.18
  grp.material = mat

  # Tray Rim Right
  grp = ents.add_group
  grp.name = "Tray Rim Right"
  face = grp.entities.add_face([4627.mm,80.mm,25.5.mm], [4629.mm,80.mm,25.5.mm], [4629.mm,2280.mm,25.5.mm], [4627.mm,2280.mm,25.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["Processing Tray Floor A"] || model.materials.add("Processing Tray Floor A")
  mat.color = Sketchup::Color.new(179, 188, 197)
  mat.alpha = 0.18
  grp.material = mat

  # Chemistry Bath
  grp = ents.add_group
  grp.name = "Chemistry Bath"
  face = grp.entities.add_face([172.mm,82.mm,25.5.mm], [4627.mm,82.mm,25.5.mm], [4627.mm,2278.mm,25.5.mm], [172.mm,2278.mm,25.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(40.mm)
  mat = model.materials["Chemistry Bath"] || model.materials.add("Chemistry Bath")
  mat.color = Sketchup::Color.new(140, 162, 183)
  mat.alpha = 0.45
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Processing tray (ghost)"
  inst.layer = model.layers["Processing Tray"]

  # ═══ Spray Bar ═══
  defn = model.definitions.add("Spray Bar")
  ents = defn.entities
  # Spray Beam 40x25x3 304-SS RHS
  grp = ents.add_group
  grp.name = "Spray Beam 40x25x3 304-SS RHS"
  face = grp.entities.add_face([200.mm,1160.95.mm,29.mm], [4599.mm,1160.95.mm,29.mm], [4599.mm,1199.05.mm,29.mm], [200.mm,1199.05.mm,29.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(38.1.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Beam End Cap (feed)
  grp = ents.add_group
  grp.name = "Beam End Cap (feed)"
  face = grp.entities.add_face([196.mm,1160.95.mm,29.mm], [200.mm,1160.95.mm,29.mm], [200.mm,1199.05.mm,29.mm], [196.mm,1199.05.mm,29.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(38.1.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Beam End Cap
  grp = ents.add_group
  grp.name = "Beam End Cap"
  face = grp.entities.add_face([4599.mm,1160.95.mm,29.mm], [4603.mm,1160.95.mm,29.mm], [4603.mm,1199.05.mm,29.mm], [4599.mm,1199.05.mm,29.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(38.1.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Side Poly Manifold (3/4 LDPE)
  grp = ents.add_group
  grp.name = "Side Poly Manifold (3/4 LDPE)"
  ge = grp.entities
  circle = ge.add_circle([200.mm,1211.55.mm,48.05.mm], [1,0,0], 12.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(4399.mm)
  mat = model.materials["Side Poly Manifold (3/4 LDPE)"] || model.materials.add("Side Poly Manifold (3/4 LDPE)")
  mat.color = Sketchup::Color.new(42, 42, 42)
  mat.alpha = 1.0
  grp.material = mat

  # Water in Manifold
  grp = ents.add_group
  grp.name = "Water in Manifold"
  ge = grp.entities
  circle = ge.add_circle([200.mm,1211.55.mm,48.05.mm], [1,0,0], 9.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(4399.mm)
  mat = model.materials["Water in Manifold"] || model.materials.add("Water in Manifold")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 0.55
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([249.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([249.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([349.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([349.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([449.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([449.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([549.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([549.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([649.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([649.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([749.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([749.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([849.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([849.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([949.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([949.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1049.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1049.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1149.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1149.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1249.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1249.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1349.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1349.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1449.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1449.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1549.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1549.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1649.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1649.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1749.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1749.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1849.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1849.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([1949.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([1949.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2049.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2049.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2149.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2149.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2249.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2249.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2349.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2349.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2449.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2449.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2549.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2549.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2649.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2649.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2749.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2749.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2849.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2849.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([2949.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([2949.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3049.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3049.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3149.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3149.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3249.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3249.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3349.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3349.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3449.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3449.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3549.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3549.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3649.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3649.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3749.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3749.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3849.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3849.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([3949.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([3949.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([4049.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([4049.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([4149.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([4149.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([4249.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([4249.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([4349.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([4349.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([4449.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([4449.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Body
  grp = ents.add_group
  grp.name = "Nozzle Body"
  ge = grp.entities
  circle = ge.add_circle([4549.5.mm,1211.55.mm,36.05.mm], [0,0,1], 4.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Nozzle Tip
  grp = ents.add_group
  grp.name = "Nozzle Tip"
  ge = grp.entities
  circle = ge.add_circle([4549.5.mm,1211.55.mm,30.049999999999997.mm], [0,0,1], 6.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(6.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage Plate L L
  grp = ents.add_group
  grp.name = "Carriage Plate L L"
  face = grp.entities.add_face([200.mm,1062.mm,38.mm], [238.1.mm,1062.mm,38.mm], [238.1.mm,1160.95.mm,38.mm], [200.mm,1160.95.mm,38.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["Carriage Plate L L"] || model.materials.add("Carriage Plate L L")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage Plate R L
  grp = ents.add_group
  grp.name = "Carriage Plate R L"
  face = grp.entities.add_face([200.mm,1199.05.mm,38.mm], [238.1.mm,1199.05.mm,38.mm], [238.1.mm,1298.mm,38.mm], [200.mm,1298.mm,38.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["Carriage Plate L L"] || model.materials.add("Carriage Plate L L")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel L
  grp = ents.add_group
  grp.name = "Wheel L"
  ge = grp.entities
  circle = ge.add_circle([209.05.mm,1080.mm,36.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Pin 10mm L
  grp = ents.add_group
  grp.name = "Axle Pin 10mm L"
  ge = grp.entities
  circle = ge.add_circle([186.05.mm,1080.mm,36.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(66.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle L
  grp = ents.add_group
  grp.name = "Axle Saddle L"
  ge = grp.entities
  face = ge.add_face([[188.05.mm,1070.82.mm,36.mm], [188.05.mm,1070.9.mm,34.8.mm], [188.05.mm,1071.13.mm,33.62.mm], [188.05.mm,1071.52.mm,32.49.mm], [188.05.mm,1072.05.mm,31.41.mm], [188.05.mm,1072.72.mm,30.41.mm], [188.05.mm,1073.51.mm,29.51.mm], [188.05.mm,1074.41.mm,28.72.mm], [188.05.mm,1075.41.mm,28.05.mm], [188.05.mm,1076.49.mm,27.52.mm], [188.05.mm,1077.62.mm,27.13.mm], [188.05.mm,1078.8.mm,26.9.mm], [188.05.mm,1080.mm,26.82.mm], [188.05.mm,1081.2.mm,26.9.mm], [188.05.mm,1082.38.mm,27.13.mm], [188.05.mm,1083.51.mm,27.52.mm], [188.05.mm,1084.59.mm,28.05.mm], [188.05.mm,1085.59.mm,28.72.mm], [188.05.mm,1086.49.mm,29.51.mm], [188.05.mm,1087.28.mm,30.41.mm], [188.05.mm,1087.95.mm,31.41.mm], [188.05.mm,1088.48.mm,32.49.mm], [188.05.mm,1088.87.mm,33.62.mm], [188.05.mm,1089.1.mm,34.8.mm], [188.05.mm,1089.18.mm,36.mm], [188.05.mm,1086.mm,36.mm], [188.05.mm,1085.95.mm,35.22.mm], [188.05.mm,1085.8.mm,34.45.mm], [188.05.mm,1085.54.mm,33.7.mm], [188.05.mm,1085.2.mm,33.mm], [188.05.mm,1084.76.mm,32.35.mm], [188.05.mm,1084.24.mm,31.76.mm], [188.05.mm,1083.65.mm,31.24.mm], [188.05.mm,1083.mm,30.8.mm], [188.05.mm,1082.3.mm,30.46.mm], [188.05.mm,1081.55.mm,30.2.mm], [188.05.mm,1080.78.mm,30.05.mm], [188.05.mm,1080.mm,30.mm], [188.05.mm,1079.22.mm,30.05.mm], [188.05.mm,1078.45.mm,30.2.mm], [188.05.mm,1077.7.mm,30.46.mm], [188.05.mm,1077.mm,30.8.mm], [188.05.mm,1076.35.mm,31.24.mm], [188.05.mm,1075.76.mm,31.76.mm], [188.05.mm,1075.24.mm,32.35.mm], [188.05.mm,1074.8.mm,33.mm], [188.05.mm,1074.46.mm,33.7.mm], [188.05.mm,1074.2.mm,34.45.mm], [188.05.mm,1074.05.mm,35.22.mm], [188.05.mm,1074.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(19.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([188.05.mm,1062.mm,34.82.mm], [207.05.mm,1062.mm,34.82.mm], [207.05.mm,1074.mm,34.82.mm], [188.05.mm,1074.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([197.55.mm,1068.mm,34.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([188.05.mm,1086.mm,34.82.mm], [207.05.mm,1086.mm,34.82.mm], [207.05.mm,1098.mm,34.82.mm], [188.05.mm,1098.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([197.55.mm,1092.mm,34.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle L
  grp = ents.add_group
  grp.name = "Axle Saddle L"
  ge = grp.entities
  face = ge.add_face([[231.05.mm,1070.82.mm,36.mm], [231.05.mm,1070.9.mm,34.8.mm], [231.05.mm,1071.13.mm,33.62.mm], [231.05.mm,1071.52.mm,32.49.mm], [231.05.mm,1072.05.mm,31.41.mm], [231.05.mm,1072.72.mm,30.41.mm], [231.05.mm,1073.51.mm,29.51.mm], [231.05.mm,1074.41.mm,28.72.mm], [231.05.mm,1075.41.mm,28.05.mm], [231.05.mm,1076.49.mm,27.52.mm], [231.05.mm,1077.62.mm,27.13.mm], [231.05.mm,1078.8.mm,26.9.mm], [231.05.mm,1080.mm,26.82.mm], [231.05.mm,1081.2.mm,26.9.mm], [231.05.mm,1082.38.mm,27.13.mm], [231.05.mm,1083.51.mm,27.52.mm], [231.05.mm,1084.59.mm,28.05.mm], [231.05.mm,1085.59.mm,28.72.mm], [231.05.mm,1086.49.mm,29.51.mm], [231.05.mm,1087.28.mm,30.41.mm], [231.05.mm,1087.95.mm,31.41.mm], [231.05.mm,1088.48.mm,32.49.mm], [231.05.mm,1088.87.mm,33.62.mm], [231.05.mm,1089.1.mm,34.8.mm], [231.05.mm,1089.18.mm,36.mm], [231.05.mm,1086.mm,36.mm], [231.05.mm,1085.95.mm,35.22.mm], [231.05.mm,1085.8.mm,34.45.mm], [231.05.mm,1085.54.mm,33.7.mm], [231.05.mm,1085.2.mm,33.mm], [231.05.mm,1084.76.mm,32.35.mm], [231.05.mm,1084.24.mm,31.76.mm], [231.05.mm,1083.65.mm,31.24.mm], [231.05.mm,1083.mm,30.8.mm], [231.05.mm,1082.3.mm,30.46.mm], [231.05.mm,1081.55.mm,30.2.mm], [231.05.mm,1080.78.mm,30.05.mm], [231.05.mm,1080.mm,30.mm], [231.05.mm,1079.22.mm,30.05.mm], [231.05.mm,1078.45.mm,30.2.mm], [231.05.mm,1077.7.mm,30.46.mm], [231.05.mm,1077.mm,30.8.mm], [231.05.mm,1076.35.mm,31.24.mm], [231.05.mm,1075.76.mm,31.76.mm], [231.05.mm,1075.24.mm,32.35.mm], [231.05.mm,1074.8.mm,33.mm], [231.05.mm,1074.46.mm,33.7.mm], [231.05.mm,1074.2.mm,34.45.mm], [231.05.mm,1074.05.mm,35.22.mm], [231.05.mm,1074.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(19.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([231.05.mm,1062.mm,34.82.mm], [250.05.mm,1062.mm,34.82.mm], [250.05.mm,1074.mm,34.82.mm], [231.05.mm,1074.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([240.55.mm,1068.mm,34.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([231.05.mm,1086.mm,34.82.mm], [250.05.mm,1086.mm,34.82.mm], [250.05.mm,1098.mm,34.82.mm], [231.05.mm,1098.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([240.55.mm,1092.mm,34.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel L
  grp = ents.add_group
  grp.name = "Wheel L"
  ge = grp.entities
  circle = ge.add_circle([209.05.mm,1280.mm,36.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Pin 10mm L
  grp = ents.add_group
  grp.name = "Axle Pin 10mm L"
  ge = grp.entities
  circle = ge.add_circle([186.05.mm,1280.mm,36.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(66.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle L
  grp = ents.add_group
  grp.name = "Axle Saddle L"
  ge = grp.entities
  face = ge.add_face([[188.05.mm,1270.82.mm,36.mm], [188.05.mm,1270.9.mm,34.8.mm], [188.05.mm,1271.13.mm,33.62.mm], [188.05.mm,1271.52.mm,32.49.mm], [188.05.mm,1272.05.mm,31.41.mm], [188.05.mm,1272.72.mm,30.41.mm], [188.05.mm,1273.51.mm,29.51.mm], [188.05.mm,1274.41.mm,28.72.mm], [188.05.mm,1275.41.mm,28.05.mm], [188.05.mm,1276.49.mm,27.52.mm], [188.05.mm,1277.62.mm,27.13.mm], [188.05.mm,1278.8.mm,26.9.mm], [188.05.mm,1280.mm,26.82.mm], [188.05.mm,1281.2.mm,26.9.mm], [188.05.mm,1282.38.mm,27.13.mm], [188.05.mm,1283.51.mm,27.52.mm], [188.05.mm,1284.59.mm,28.05.mm], [188.05.mm,1285.59.mm,28.72.mm], [188.05.mm,1286.49.mm,29.51.mm], [188.05.mm,1287.28.mm,30.41.mm], [188.05.mm,1287.95.mm,31.41.mm], [188.05.mm,1288.48.mm,32.49.mm], [188.05.mm,1288.87.mm,33.62.mm], [188.05.mm,1289.1.mm,34.8.mm], [188.05.mm,1289.18.mm,36.mm], [188.05.mm,1286.mm,36.mm], [188.05.mm,1285.95.mm,35.22.mm], [188.05.mm,1285.8.mm,34.45.mm], [188.05.mm,1285.54.mm,33.7.mm], [188.05.mm,1285.2.mm,33.mm], [188.05.mm,1284.76.mm,32.35.mm], [188.05.mm,1284.24.mm,31.76.mm], [188.05.mm,1283.65.mm,31.24.mm], [188.05.mm,1283.mm,30.8.mm], [188.05.mm,1282.3.mm,30.46.mm], [188.05.mm,1281.55.mm,30.2.mm], [188.05.mm,1280.78.mm,30.05.mm], [188.05.mm,1280.mm,30.mm], [188.05.mm,1279.22.mm,30.05.mm], [188.05.mm,1278.45.mm,30.2.mm], [188.05.mm,1277.7.mm,30.46.mm], [188.05.mm,1277.mm,30.8.mm], [188.05.mm,1276.35.mm,31.24.mm], [188.05.mm,1275.76.mm,31.76.mm], [188.05.mm,1275.24.mm,32.35.mm], [188.05.mm,1274.8.mm,33.mm], [188.05.mm,1274.46.mm,33.7.mm], [188.05.mm,1274.2.mm,34.45.mm], [188.05.mm,1274.05.mm,35.22.mm], [188.05.mm,1274.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(19.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([188.05.mm,1262.mm,34.82.mm], [207.05.mm,1262.mm,34.82.mm], [207.05.mm,1274.mm,34.82.mm], [188.05.mm,1274.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([197.55.mm,1268.mm,34.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([188.05.mm,1286.mm,34.82.mm], [207.05.mm,1286.mm,34.82.mm], [207.05.mm,1298.mm,34.82.mm], [188.05.mm,1298.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([197.55.mm,1292.mm,34.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle L
  grp = ents.add_group
  grp.name = "Axle Saddle L"
  ge = grp.entities
  face = ge.add_face([[231.05.mm,1270.82.mm,36.mm], [231.05.mm,1270.9.mm,34.8.mm], [231.05.mm,1271.13.mm,33.62.mm], [231.05.mm,1271.52.mm,32.49.mm], [231.05.mm,1272.05.mm,31.41.mm], [231.05.mm,1272.72.mm,30.41.mm], [231.05.mm,1273.51.mm,29.51.mm], [231.05.mm,1274.41.mm,28.72.mm], [231.05.mm,1275.41.mm,28.05.mm], [231.05.mm,1276.49.mm,27.52.mm], [231.05.mm,1277.62.mm,27.13.mm], [231.05.mm,1278.8.mm,26.9.mm], [231.05.mm,1280.mm,26.82.mm], [231.05.mm,1281.2.mm,26.9.mm], [231.05.mm,1282.38.mm,27.13.mm], [231.05.mm,1283.51.mm,27.52.mm], [231.05.mm,1284.59.mm,28.05.mm], [231.05.mm,1285.59.mm,28.72.mm], [231.05.mm,1286.49.mm,29.51.mm], [231.05.mm,1287.28.mm,30.41.mm], [231.05.mm,1287.95.mm,31.41.mm], [231.05.mm,1288.48.mm,32.49.mm], [231.05.mm,1288.87.mm,33.62.mm], [231.05.mm,1289.1.mm,34.8.mm], [231.05.mm,1289.18.mm,36.mm], [231.05.mm,1286.mm,36.mm], [231.05.mm,1285.95.mm,35.22.mm], [231.05.mm,1285.8.mm,34.45.mm], [231.05.mm,1285.54.mm,33.7.mm], [231.05.mm,1285.2.mm,33.mm], [231.05.mm,1284.76.mm,32.35.mm], [231.05.mm,1284.24.mm,31.76.mm], [231.05.mm,1283.65.mm,31.24.mm], [231.05.mm,1283.mm,30.8.mm], [231.05.mm,1282.3.mm,30.46.mm], [231.05.mm,1281.55.mm,30.2.mm], [231.05.mm,1280.78.mm,30.05.mm], [231.05.mm,1280.mm,30.mm], [231.05.mm,1279.22.mm,30.05.mm], [231.05.mm,1278.45.mm,30.2.mm], [231.05.mm,1277.7.mm,30.46.mm], [231.05.mm,1277.mm,30.8.mm], [231.05.mm,1276.35.mm,31.24.mm], [231.05.mm,1275.76.mm,31.76.mm], [231.05.mm,1275.24.mm,32.35.mm], [231.05.mm,1274.8.mm,33.mm], [231.05.mm,1274.46.mm,33.7.mm], [231.05.mm,1274.2.mm,34.45.mm], [231.05.mm,1274.05.mm,35.22.mm], [231.05.mm,1274.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(19.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([231.05.mm,1262.mm,34.82.mm], [250.05.mm,1262.mm,34.82.mm], [250.05.mm,1274.mm,34.82.mm], [231.05.mm,1274.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([240.55.mm,1268.mm,34.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot L
  grp = ents.add_group
  grp.name = "Axle Saddle Foot L"
  face = grp.entities.add_face([231.05.mm,1286.mm,34.82.mm], [250.05.mm,1286.mm,34.82.mm], [250.05.mm,1298.mm,34.82.mm], [231.05.mm,1298.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt L
  grp = ents.add_group
  grp.name = "Axle Bolt L"
  ge = grp.entities
  circle = ge.add_circle([240.55.mm,1292.mm,34.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Bottom Clamp L
  grp = ents.add_group
  grp.name = "Bottom Clamp L"
  face = grp.entities.add_face([200.mm,1148.mm,26.mm], [238.1.mm,1148.mm,26.mm], [238.1.mm,1212.mm,26.mm], [200.mm,1212.mm,26.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Top Clamp L
  grp = ents.add_group
  grp.name = "Top Clamp L"
  face = grp.entities.add_face([200.mm,1148.mm,67.1.mm], [238.1.mm,1148.mm,67.1.mm], [238.1.mm,1212.mm,67.1.mm], [200.mm,1212.mm,67.1.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Spacer L
  grp = ents.add_group
  grp.name = "Clamp Spacer L"
  face = grp.entities.add_face([204.mm,1152.95.mm,29.mm], [234.1.mm,1152.95.mm,29.mm], [234.1.mm,1160.95.mm,29.mm], [204.mm,1160.95.mm,29.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(38.099999999999994.mm)
  mat = model.materials["Carriage Plate L L"] || model.materials.add("Carriage Plate L L")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt L
  grp = ents.add_group
  grp.name = "Clamp Bolt L"
  ge = grp.entities
  circle = ge.add_circle([209.mm,1156.95.mm,26.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(48.099999999999994.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt CSK Head L
  grp = ents.add_group
  grp.name = "Clamp Bolt CSK Head L"
  ge = grp.entities
  ge.add_face([213.5.mm,1156.95.mm,26.mm], [212.89711431702997.mm,1159.2.mm,26.mm], [211.1650635094611.mm,1158.2.mm,29.mm], [211.5.mm,1156.95.mm,29.mm])
  ge.add_face([212.89711431702997.mm,1159.2.mm,26.mm], [211.25.mm,1160.84711431703.mm,26.mm], [210.25.mm,1159.1150635094612.mm,29.mm], [211.1650635094611.mm,1158.2.mm,29.mm])
  ge.add_face([211.25.mm,1160.84711431703.mm,26.mm], [209.mm,1161.45.mm,26.mm], [209.mm,1159.45.mm,29.mm], [210.25.mm,1159.1150635094612.mm,29.mm])
  ge.add_face([209.mm,1161.45.mm,26.mm], [206.75.mm,1160.84711431703.mm,26.mm], [207.75.mm,1159.1150635094612.mm,29.mm], [209.mm,1159.45.mm,29.mm])
  ge.add_face([206.75.mm,1160.84711431703.mm,26.mm], [205.10288568297003.mm,1159.2.mm,26.mm], [206.8349364905389.mm,1158.2.mm,29.mm], [207.75.mm,1159.1150635094612.mm,29.mm])
  ge.add_face([205.10288568297003.mm,1159.2.mm,26.mm], [204.5.mm,1156.95.mm,26.mm], [206.5.mm,1156.95.mm,29.mm], [206.8349364905389.mm,1158.2.mm,29.mm])
  ge.add_face([204.5.mm,1156.95.mm,26.mm], [205.10288568297003.mm,1154.7.mm,26.mm], [206.8349364905389.mm,1155.7.mm,29.mm], [206.5.mm,1156.95.mm,29.mm])
  ge.add_face([205.10288568297003.mm,1154.7.mm,26.mm], [206.75.mm,1153.05288568297.mm,26.mm], [207.75.mm,1154.784936490539.mm,29.mm], [206.8349364905389.mm,1155.7.mm,29.mm])
  ge.add_face([206.75.mm,1153.05288568297.mm,26.mm], [209.mm,1152.45.mm,26.mm], [209.mm,1154.45.mm,29.mm], [207.75.mm,1154.784936490539.mm,29.mm])
  ge.add_face([209.mm,1152.45.mm,26.mm], [211.25.mm,1153.05288568297.mm,26.mm], [210.25.mm,1154.784936490539.mm,29.mm], [209.mm,1154.45.mm,29.mm])
  ge.add_face([211.25.mm,1153.05288568297.mm,26.mm], [212.89711431702997.mm,1154.7.mm,26.mm], [211.1650635094611.mm,1155.7.mm,29.mm], [210.25.mm,1154.784936490539.mm,29.mm])
  ge.add_face([212.89711431702997.mm,1154.7.mm,26.mm], [213.5.mm,1156.95.mm,26.mm], [211.5.mm,1156.95.mm,29.mm], [211.1650635094611.mm,1155.7.mm,29.mm])
  ge.add_face([213.5.mm,1156.95.mm,26.mm], [212.89711431702997.mm,1159.2.mm,26.mm], [211.25.mm,1160.84711431703.mm,26.mm], [209.mm,1161.45.mm,26.mm], [206.75.mm,1160.84711431703.mm,26.mm], [205.10288568297003.mm,1159.2.mm,26.mm], [204.5.mm,1156.95.mm,26.mm], [205.10288568297003.mm,1154.7.mm,26.mm], [206.75.mm,1153.05288568297.mm,26.mm], [209.mm,1152.45.mm,26.mm], [211.25.mm,1153.05288568297.mm,26.mm], [212.89711431702997.mm,1154.7.mm,26.mm])
  mat = model.materials["Clamp Bolt CSK Head L"] || model.materials.add("Clamp Bolt CSK Head L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  grp.material = mat

  # Clamp Bolt L
  grp = ents.add_group
  grp.name = "Clamp Bolt L"
  ge = grp.entities
  circle = ge.add_circle([229.1.mm,1156.95.mm,26.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(48.099999999999994.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt CSK Head L
  grp = ents.add_group
  grp.name = "Clamp Bolt CSK Head L"
  ge = grp.entities
  ge.add_face([233.6.mm,1156.95.mm,26.mm], [232.99711431702997.mm,1159.2.mm,26.mm], [231.2650635094611.mm,1158.2.mm,29.mm], [231.6.mm,1156.95.mm,29.mm])
  ge.add_face([232.99711431702997.mm,1159.2.mm,26.mm], [231.35.mm,1160.84711431703.mm,26.mm], [230.35.mm,1159.1150635094612.mm,29.mm], [231.2650635094611.mm,1158.2.mm,29.mm])
  ge.add_face([231.35.mm,1160.84711431703.mm,26.mm], [229.1.mm,1161.45.mm,26.mm], [229.1.mm,1159.45.mm,29.mm], [230.35.mm,1159.1150635094612.mm,29.mm])
  ge.add_face([229.1.mm,1161.45.mm,26.mm], [226.85.mm,1160.84711431703.mm,26.mm], [227.85.mm,1159.1150635094612.mm,29.mm], [229.1.mm,1159.45.mm,29.mm])
  ge.add_face([226.85.mm,1160.84711431703.mm,26.mm], [225.20288568297002.mm,1159.2.mm,26.mm], [226.9349364905389.mm,1158.2.mm,29.mm], [227.85.mm,1159.1150635094612.mm,29.mm])
  ge.add_face([225.20288568297002.mm,1159.2.mm,26.mm], [224.6.mm,1156.95.mm,26.mm], [226.6.mm,1156.95.mm,29.mm], [226.9349364905389.mm,1158.2.mm,29.mm])
  ge.add_face([224.6.mm,1156.95.mm,26.mm], [225.20288568297002.mm,1154.7.mm,26.mm], [226.9349364905389.mm,1155.7.mm,29.mm], [226.6.mm,1156.95.mm,29.mm])
  ge.add_face([225.20288568297002.mm,1154.7.mm,26.mm], [226.85.mm,1153.05288568297.mm,26.mm], [227.85.mm,1154.784936490539.mm,29.mm], [226.9349364905389.mm,1155.7.mm,29.mm])
  ge.add_face([226.85.mm,1153.05288568297.mm,26.mm], [229.1.mm,1152.45.mm,26.mm], [229.1.mm,1154.45.mm,29.mm], [227.85.mm,1154.784936490539.mm,29.mm])
  ge.add_face([229.1.mm,1152.45.mm,26.mm], [231.35.mm,1153.05288568297.mm,26.mm], [230.35.mm,1154.784936490539.mm,29.mm], [229.1.mm,1154.45.mm,29.mm])
  ge.add_face([231.35.mm,1153.05288568297.mm,26.mm], [232.99711431702997.mm,1154.7.mm,26.mm], [231.2650635094611.mm,1155.7.mm,29.mm], [230.35.mm,1154.784936490539.mm,29.mm])
  ge.add_face([232.99711431702997.mm,1154.7.mm,26.mm], [233.6.mm,1156.95.mm,26.mm], [231.6.mm,1156.95.mm,29.mm], [231.2650635094611.mm,1155.7.mm,29.mm])
  ge.add_face([233.6.mm,1156.95.mm,26.mm], [232.99711431702997.mm,1159.2.mm,26.mm], [231.35.mm,1160.84711431703.mm,26.mm], [229.1.mm,1161.45.mm,26.mm], [226.85.mm,1160.84711431703.mm,26.mm], [225.20288568297002.mm,1159.2.mm,26.mm], [224.6.mm,1156.95.mm,26.mm], [225.20288568297002.mm,1154.7.mm,26.mm], [226.85.mm,1153.05288568297.mm,26.mm], [229.1.mm,1152.45.mm,26.mm], [231.35.mm,1153.05288568297.mm,26.mm], [232.99711431702997.mm,1154.7.mm,26.mm])
  mat = model.materials["Clamp Bolt CSK Head L"] || model.materials.add("Clamp Bolt CSK Head L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  grp.material = mat

  # Clamp Spacer L
  grp = ents.add_group
  grp.name = "Clamp Spacer L"
  face = grp.entities.add_face([204.mm,1199.05.mm,29.mm], [234.1.mm,1199.05.mm,29.mm], [234.1.mm,1207.05.mm,29.mm], [204.mm,1207.05.mm,29.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(38.099999999999994.mm)
  mat = model.materials["Carriage Plate L L"] || model.materials.add("Carriage Plate L L")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt L
  grp = ents.add_group
  grp.name = "Clamp Bolt L"
  ge = grp.entities
  circle = ge.add_circle([209.mm,1203.05.mm,26.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(48.099999999999994.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt CSK Head L
  grp = ents.add_group
  grp.name = "Clamp Bolt CSK Head L"
  ge = grp.entities
  ge.add_face([213.5.mm,1203.05.mm,26.mm], [212.89711431702997.mm,1205.3.mm,26.mm], [211.1650635094611.mm,1204.3.mm,29.mm], [211.5.mm,1203.05.mm,29.mm])
  ge.add_face([212.89711431702997.mm,1205.3.mm,26.mm], [211.25.mm,1206.94711431703.mm,26.mm], [210.25.mm,1205.215063509461.mm,29.mm], [211.1650635094611.mm,1204.3.mm,29.mm])
  ge.add_face([211.25.mm,1206.94711431703.mm,26.mm], [209.mm,1207.55.mm,26.mm], [209.mm,1205.55.mm,29.mm], [210.25.mm,1205.215063509461.mm,29.mm])
  ge.add_face([209.mm,1207.55.mm,26.mm], [206.75.mm,1206.94711431703.mm,26.mm], [207.75.mm,1205.215063509461.mm,29.mm], [209.mm,1205.55.mm,29.mm])
  ge.add_face([206.75.mm,1206.94711431703.mm,26.mm], [205.10288568297003.mm,1205.3.mm,26.mm], [206.8349364905389.mm,1204.3.mm,29.mm], [207.75.mm,1205.215063509461.mm,29.mm])
  ge.add_face([205.10288568297003.mm,1205.3.mm,26.mm], [204.5.mm,1203.05.mm,26.mm], [206.5.mm,1203.05.mm,29.mm], [206.8349364905389.mm,1204.3.mm,29.mm])
  ge.add_face([204.5.mm,1203.05.mm,26.mm], [205.10288568297003.mm,1200.8.mm,26.mm], [206.8349364905389.mm,1201.8.mm,29.mm], [206.5.mm,1203.05.mm,29.mm])
  ge.add_face([205.10288568297003.mm,1200.8.mm,26.mm], [206.75.mm,1199.15288568297.mm,26.mm], [207.75.mm,1200.8849364905388.mm,29.mm], [206.8349364905389.mm,1201.8.mm,29.mm])
  ge.add_face([206.75.mm,1199.15288568297.mm,26.mm], [209.mm,1198.55.mm,26.mm], [209.mm,1200.55.mm,29.mm], [207.75.mm,1200.8849364905388.mm,29.mm])
  ge.add_face([209.mm,1198.55.mm,26.mm], [211.25.mm,1199.15288568297.mm,26.mm], [210.25.mm,1200.8849364905388.mm,29.mm], [209.mm,1200.55.mm,29.mm])
  ge.add_face([211.25.mm,1199.15288568297.mm,26.mm], [212.89711431702997.mm,1200.8.mm,26.mm], [211.1650635094611.mm,1201.8.mm,29.mm], [210.25.mm,1200.8849364905388.mm,29.mm])
  ge.add_face([212.89711431702997.mm,1200.8.mm,26.mm], [213.5.mm,1203.05.mm,26.mm], [211.5.mm,1203.05.mm,29.mm], [211.1650635094611.mm,1201.8.mm,29.mm])
  ge.add_face([213.5.mm,1203.05.mm,26.mm], [212.89711431702997.mm,1205.3.mm,26.mm], [211.25.mm,1206.94711431703.mm,26.mm], [209.mm,1207.55.mm,26.mm], [206.75.mm,1206.94711431703.mm,26.mm], [205.10288568297003.mm,1205.3.mm,26.mm], [204.5.mm,1203.05.mm,26.mm], [205.10288568297003.mm,1200.8.mm,26.mm], [206.75.mm,1199.15288568297.mm,26.mm], [209.mm,1198.55.mm,26.mm], [211.25.mm,1199.15288568297.mm,26.mm], [212.89711431702997.mm,1200.8.mm,26.mm])
  mat = model.materials["Clamp Bolt CSK Head L"] || model.materials.add("Clamp Bolt CSK Head L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  grp.material = mat

  # Clamp Bolt L
  grp = ents.add_group
  grp.name = "Clamp Bolt L"
  ge = grp.entities
  circle = ge.add_circle([229.1.mm,1203.05.mm,26.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(48.099999999999994.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt CSK Head L
  grp = ents.add_group
  grp.name = "Clamp Bolt CSK Head L"
  ge = grp.entities
  ge.add_face([233.6.mm,1203.05.mm,26.mm], [232.99711431702997.mm,1205.3.mm,26.mm], [231.2650635094611.mm,1204.3.mm,29.mm], [231.6.mm,1203.05.mm,29.mm])
  ge.add_face([232.99711431702997.mm,1205.3.mm,26.mm], [231.35.mm,1206.94711431703.mm,26.mm], [230.35.mm,1205.215063509461.mm,29.mm], [231.2650635094611.mm,1204.3.mm,29.mm])
  ge.add_face([231.35.mm,1206.94711431703.mm,26.mm], [229.1.mm,1207.55.mm,26.mm], [229.1.mm,1205.55.mm,29.mm], [230.35.mm,1205.215063509461.mm,29.mm])
  ge.add_face([229.1.mm,1207.55.mm,26.mm], [226.85.mm,1206.94711431703.mm,26.mm], [227.85.mm,1205.215063509461.mm,29.mm], [229.1.mm,1205.55.mm,29.mm])
  ge.add_face([226.85.mm,1206.94711431703.mm,26.mm], [225.20288568297002.mm,1205.3.mm,26.mm], [226.9349364905389.mm,1204.3.mm,29.mm], [227.85.mm,1205.215063509461.mm,29.mm])
  ge.add_face([225.20288568297002.mm,1205.3.mm,26.mm], [224.6.mm,1203.05.mm,26.mm], [226.6.mm,1203.05.mm,29.mm], [226.9349364905389.mm,1204.3.mm,29.mm])
  ge.add_face([224.6.mm,1203.05.mm,26.mm], [225.20288568297002.mm,1200.8.mm,26.mm], [226.9349364905389.mm,1201.8.mm,29.mm], [226.6.mm,1203.05.mm,29.mm])
  ge.add_face([225.20288568297002.mm,1200.8.mm,26.mm], [226.85.mm,1199.15288568297.mm,26.mm], [227.85.mm,1200.8849364905388.mm,29.mm], [226.9349364905389.mm,1201.8.mm,29.mm])
  ge.add_face([226.85.mm,1199.15288568297.mm,26.mm], [229.1.mm,1198.55.mm,26.mm], [229.1.mm,1200.55.mm,29.mm], [227.85.mm,1200.8849364905388.mm,29.mm])
  ge.add_face([229.1.mm,1198.55.mm,26.mm], [231.35.mm,1199.15288568297.mm,26.mm], [230.35.mm,1200.8849364905388.mm,29.mm], [229.1.mm,1200.55.mm,29.mm])
  ge.add_face([231.35.mm,1199.15288568297.mm,26.mm], [232.99711431702997.mm,1200.8.mm,26.mm], [231.2650635094611.mm,1201.8.mm,29.mm], [230.35.mm,1200.8849364905388.mm,29.mm])
  ge.add_face([232.99711431702997.mm,1200.8.mm,26.mm], [233.6.mm,1203.05.mm,26.mm], [231.6.mm,1203.05.mm,29.mm], [231.2650635094611.mm,1201.8.mm,29.mm])
  ge.add_face([233.6.mm,1203.05.mm,26.mm], [232.99711431702997.mm,1205.3.mm,26.mm], [231.35.mm,1206.94711431703.mm,26.mm], [229.1.mm,1207.55.mm,26.mm], [226.85.mm,1206.94711431703.mm,26.mm], [225.20288568297002.mm,1205.3.mm,26.mm], [224.6.mm,1203.05.mm,26.mm], [225.20288568297002.mm,1200.8.mm,26.mm], [226.85.mm,1199.15288568297.mm,26.mm], [229.1.mm,1198.55.mm,26.mm], [231.35.mm,1199.15288568297.mm,26.mm], [232.99711431702997.mm,1200.8.mm,26.mm])
  mat = model.materials["Clamp Bolt CSK Head L"] || model.materials.add("Clamp Bolt CSK Head L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  grp.material = mat

  # Carriage Plate L R
  grp = ents.add_group
  grp.name = "Carriage Plate L R"
  face = grp.entities.add_face([4560.9.mm,1062.mm,38.mm], [4599.mm,1062.mm,38.mm], [4599.mm,1160.95.mm,38.mm], [4560.9.mm,1160.95.mm,38.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["Carriage Plate L L"] || model.materials.add("Carriage Plate L L")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Carriage Plate R R
  grp = ents.add_group
  grp.name = "Carriage Plate R R"
  face = grp.entities.add_face([4560.9.mm,1199.05.mm,38.mm], [4599.mm,1199.05.mm,38.mm], [4599.mm,1298.mm,38.mm], [4560.9.mm,1298.mm,38.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["Carriage Plate L L"] || model.materials.add("Carriage Plate L L")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel R
  grp = ents.add_group
  grp.name = "Wheel R"
  ge = grp.entities
  circle = ge.add_circle([4569.95.mm,1080.mm,36.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Pin 10mm R
  grp = ents.add_group
  grp.name = "Axle Pin 10mm R"
  ge = grp.entities
  circle = ge.add_circle([4546.95.mm,1080.mm,36.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(66.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle R
  grp = ents.add_group
  grp.name = "Axle Saddle R"
  ge = grp.entities
  face = ge.add_face([[4548.95.mm,1070.82.mm,36.mm], [4548.95.mm,1070.9.mm,34.8.mm], [4548.95.mm,1071.13.mm,33.62.mm], [4548.95.mm,1071.52.mm,32.49.mm], [4548.95.mm,1072.05.mm,31.41.mm], [4548.95.mm,1072.72.mm,30.41.mm], [4548.95.mm,1073.51.mm,29.51.mm], [4548.95.mm,1074.41.mm,28.72.mm], [4548.95.mm,1075.41.mm,28.05.mm], [4548.95.mm,1076.49.mm,27.52.mm], [4548.95.mm,1077.62.mm,27.13.mm], [4548.95.mm,1078.8.mm,26.9.mm], [4548.95.mm,1080.mm,26.82.mm], [4548.95.mm,1081.2.mm,26.9.mm], [4548.95.mm,1082.38.mm,27.13.mm], [4548.95.mm,1083.51.mm,27.52.mm], [4548.95.mm,1084.59.mm,28.05.mm], [4548.95.mm,1085.59.mm,28.72.mm], [4548.95.mm,1086.49.mm,29.51.mm], [4548.95.mm,1087.28.mm,30.41.mm], [4548.95.mm,1087.95.mm,31.41.mm], [4548.95.mm,1088.48.mm,32.49.mm], [4548.95.mm,1088.87.mm,33.62.mm], [4548.95.mm,1089.1.mm,34.8.mm], [4548.95.mm,1089.18.mm,36.mm], [4548.95.mm,1086.mm,36.mm], [4548.95.mm,1085.95.mm,35.22.mm], [4548.95.mm,1085.8.mm,34.45.mm], [4548.95.mm,1085.54.mm,33.7.mm], [4548.95.mm,1085.2.mm,33.mm], [4548.95.mm,1084.76.mm,32.35.mm], [4548.95.mm,1084.24.mm,31.76.mm], [4548.95.mm,1083.65.mm,31.24.mm], [4548.95.mm,1083.mm,30.8.mm], [4548.95.mm,1082.3.mm,30.46.mm], [4548.95.mm,1081.55.mm,30.2.mm], [4548.95.mm,1080.78.mm,30.05.mm], [4548.95.mm,1080.mm,30.mm], [4548.95.mm,1079.22.mm,30.05.mm], [4548.95.mm,1078.45.mm,30.2.mm], [4548.95.mm,1077.7.mm,30.46.mm], [4548.95.mm,1077.mm,30.8.mm], [4548.95.mm,1076.35.mm,31.24.mm], [4548.95.mm,1075.76.mm,31.76.mm], [4548.95.mm,1075.24.mm,32.35.mm], [4548.95.mm,1074.8.mm,33.mm], [4548.95.mm,1074.46.mm,33.7.mm], [4548.95.mm,1074.2.mm,34.45.mm], [4548.95.mm,1074.05.mm,35.22.mm], [4548.95.mm,1074.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(19.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4548.95.mm,1062.mm,34.82.mm], [4567.95.mm,1062.mm,34.82.mm], [4567.95.mm,1074.mm,34.82.mm], [4548.95.mm,1074.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4558.45.mm,1068.mm,34.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4548.95.mm,1086.mm,34.82.mm], [4567.95.mm,1086.mm,34.82.mm], [4567.95.mm,1098.mm,34.82.mm], [4548.95.mm,1098.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4558.45.mm,1092.mm,34.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle R
  grp = ents.add_group
  grp.name = "Axle Saddle R"
  ge = grp.entities
  face = ge.add_face([[4591.95.mm,1070.82.mm,36.mm], [4591.95.mm,1070.9.mm,34.8.mm], [4591.95.mm,1071.13.mm,33.62.mm], [4591.95.mm,1071.52.mm,32.49.mm], [4591.95.mm,1072.05.mm,31.41.mm], [4591.95.mm,1072.72.mm,30.41.mm], [4591.95.mm,1073.51.mm,29.51.mm], [4591.95.mm,1074.41.mm,28.72.mm], [4591.95.mm,1075.41.mm,28.05.mm], [4591.95.mm,1076.49.mm,27.52.mm], [4591.95.mm,1077.62.mm,27.13.mm], [4591.95.mm,1078.8.mm,26.9.mm], [4591.95.mm,1080.mm,26.82.mm], [4591.95.mm,1081.2.mm,26.9.mm], [4591.95.mm,1082.38.mm,27.13.mm], [4591.95.mm,1083.51.mm,27.52.mm], [4591.95.mm,1084.59.mm,28.05.mm], [4591.95.mm,1085.59.mm,28.72.mm], [4591.95.mm,1086.49.mm,29.51.mm], [4591.95.mm,1087.28.mm,30.41.mm], [4591.95.mm,1087.95.mm,31.41.mm], [4591.95.mm,1088.48.mm,32.49.mm], [4591.95.mm,1088.87.mm,33.62.mm], [4591.95.mm,1089.1.mm,34.8.mm], [4591.95.mm,1089.18.mm,36.mm], [4591.95.mm,1086.mm,36.mm], [4591.95.mm,1085.95.mm,35.22.mm], [4591.95.mm,1085.8.mm,34.45.mm], [4591.95.mm,1085.54.mm,33.7.mm], [4591.95.mm,1085.2.mm,33.mm], [4591.95.mm,1084.76.mm,32.35.mm], [4591.95.mm,1084.24.mm,31.76.mm], [4591.95.mm,1083.65.mm,31.24.mm], [4591.95.mm,1083.mm,30.8.mm], [4591.95.mm,1082.3.mm,30.46.mm], [4591.95.mm,1081.55.mm,30.2.mm], [4591.95.mm,1080.78.mm,30.05.mm], [4591.95.mm,1080.mm,30.mm], [4591.95.mm,1079.22.mm,30.05.mm], [4591.95.mm,1078.45.mm,30.2.mm], [4591.95.mm,1077.7.mm,30.46.mm], [4591.95.mm,1077.mm,30.8.mm], [4591.95.mm,1076.35.mm,31.24.mm], [4591.95.mm,1075.76.mm,31.76.mm], [4591.95.mm,1075.24.mm,32.35.mm], [4591.95.mm,1074.8.mm,33.mm], [4591.95.mm,1074.46.mm,33.7.mm], [4591.95.mm,1074.2.mm,34.45.mm], [4591.95.mm,1074.05.mm,35.22.mm], [4591.95.mm,1074.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(19.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4591.95.mm,1062.mm,34.82.mm], [4610.95.mm,1062.mm,34.82.mm], [4610.95.mm,1074.mm,34.82.mm], [4591.95.mm,1074.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4601.45.mm,1068.mm,34.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4591.95.mm,1086.mm,34.82.mm], [4610.95.mm,1086.mm,34.82.mm], [4610.95.mm,1098.mm,34.82.mm], [4591.95.mm,1098.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4601.45.mm,1092.mm,34.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Wheel R
  grp = ents.add_group
  grp.name = "Wheel R"
  ge = grp.entities
  circle = ge.add_circle([4569.95.mm,1280.mm,36.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(20.mm)
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Pin 10mm R
  grp = ents.add_group
  grp.name = "Axle Pin 10mm R"
  ge = grp.entities
  circle = ge.add_circle([4546.95.mm,1280.mm,36.mm], [1,0,0], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(66.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle R
  grp = ents.add_group
  grp.name = "Axle Saddle R"
  ge = grp.entities
  face = ge.add_face([[4548.95.mm,1270.82.mm,36.mm], [4548.95.mm,1270.9.mm,34.8.mm], [4548.95.mm,1271.13.mm,33.62.mm], [4548.95.mm,1271.52.mm,32.49.mm], [4548.95.mm,1272.05.mm,31.41.mm], [4548.95.mm,1272.72.mm,30.41.mm], [4548.95.mm,1273.51.mm,29.51.mm], [4548.95.mm,1274.41.mm,28.72.mm], [4548.95.mm,1275.41.mm,28.05.mm], [4548.95.mm,1276.49.mm,27.52.mm], [4548.95.mm,1277.62.mm,27.13.mm], [4548.95.mm,1278.8.mm,26.9.mm], [4548.95.mm,1280.mm,26.82.mm], [4548.95.mm,1281.2.mm,26.9.mm], [4548.95.mm,1282.38.mm,27.13.mm], [4548.95.mm,1283.51.mm,27.52.mm], [4548.95.mm,1284.59.mm,28.05.mm], [4548.95.mm,1285.59.mm,28.72.mm], [4548.95.mm,1286.49.mm,29.51.mm], [4548.95.mm,1287.28.mm,30.41.mm], [4548.95.mm,1287.95.mm,31.41.mm], [4548.95.mm,1288.48.mm,32.49.mm], [4548.95.mm,1288.87.mm,33.62.mm], [4548.95.mm,1289.1.mm,34.8.mm], [4548.95.mm,1289.18.mm,36.mm], [4548.95.mm,1286.mm,36.mm], [4548.95.mm,1285.95.mm,35.22.mm], [4548.95.mm,1285.8.mm,34.45.mm], [4548.95.mm,1285.54.mm,33.7.mm], [4548.95.mm,1285.2.mm,33.mm], [4548.95.mm,1284.76.mm,32.35.mm], [4548.95.mm,1284.24.mm,31.76.mm], [4548.95.mm,1283.65.mm,31.24.mm], [4548.95.mm,1283.mm,30.8.mm], [4548.95.mm,1282.3.mm,30.46.mm], [4548.95.mm,1281.55.mm,30.2.mm], [4548.95.mm,1280.78.mm,30.05.mm], [4548.95.mm,1280.mm,30.mm], [4548.95.mm,1279.22.mm,30.05.mm], [4548.95.mm,1278.45.mm,30.2.mm], [4548.95.mm,1277.7.mm,30.46.mm], [4548.95.mm,1277.mm,30.8.mm], [4548.95.mm,1276.35.mm,31.24.mm], [4548.95.mm,1275.76.mm,31.76.mm], [4548.95.mm,1275.24.mm,32.35.mm], [4548.95.mm,1274.8.mm,33.mm], [4548.95.mm,1274.46.mm,33.7.mm], [4548.95.mm,1274.2.mm,34.45.mm], [4548.95.mm,1274.05.mm,35.22.mm], [4548.95.mm,1274.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(19.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4548.95.mm,1262.mm,34.82.mm], [4567.95.mm,1262.mm,34.82.mm], [4567.95.mm,1274.mm,34.82.mm], [4548.95.mm,1274.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4558.45.mm,1268.mm,34.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4548.95.mm,1286.mm,34.82.mm], [4567.95.mm,1286.mm,34.82.mm], [4567.95.mm,1298.mm,34.82.mm], [4548.95.mm,1298.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4558.45.mm,1292.mm,34.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle R
  grp = ents.add_group
  grp.name = "Axle Saddle R"
  ge = grp.entities
  face = ge.add_face([[4591.95.mm,1270.82.mm,36.mm], [4591.95.mm,1270.9.mm,34.8.mm], [4591.95.mm,1271.13.mm,33.62.mm], [4591.95.mm,1271.52.mm,32.49.mm], [4591.95.mm,1272.05.mm,31.41.mm], [4591.95.mm,1272.72.mm,30.41.mm], [4591.95.mm,1273.51.mm,29.51.mm], [4591.95.mm,1274.41.mm,28.72.mm], [4591.95.mm,1275.41.mm,28.05.mm], [4591.95.mm,1276.49.mm,27.52.mm], [4591.95.mm,1277.62.mm,27.13.mm], [4591.95.mm,1278.8.mm,26.9.mm], [4591.95.mm,1280.mm,26.82.mm], [4591.95.mm,1281.2.mm,26.9.mm], [4591.95.mm,1282.38.mm,27.13.mm], [4591.95.mm,1283.51.mm,27.52.mm], [4591.95.mm,1284.59.mm,28.05.mm], [4591.95.mm,1285.59.mm,28.72.mm], [4591.95.mm,1286.49.mm,29.51.mm], [4591.95.mm,1287.28.mm,30.41.mm], [4591.95.mm,1287.95.mm,31.41.mm], [4591.95.mm,1288.48.mm,32.49.mm], [4591.95.mm,1288.87.mm,33.62.mm], [4591.95.mm,1289.1.mm,34.8.mm], [4591.95.mm,1289.18.mm,36.mm], [4591.95.mm,1286.mm,36.mm], [4591.95.mm,1285.95.mm,35.22.mm], [4591.95.mm,1285.8.mm,34.45.mm], [4591.95.mm,1285.54.mm,33.7.mm], [4591.95.mm,1285.2.mm,33.mm], [4591.95.mm,1284.76.mm,32.35.mm], [4591.95.mm,1284.24.mm,31.76.mm], [4591.95.mm,1283.65.mm,31.24.mm], [4591.95.mm,1283.mm,30.8.mm], [4591.95.mm,1282.3.mm,30.46.mm], [4591.95.mm,1281.55.mm,30.2.mm], [4591.95.mm,1280.78.mm,30.05.mm], [4591.95.mm,1280.mm,30.mm], [4591.95.mm,1279.22.mm,30.05.mm], [4591.95.mm,1278.45.mm,30.2.mm], [4591.95.mm,1277.7.mm,30.46.mm], [4591.95.mm,1277.mm,30.8.mm], [4591.95.mm,1276.35.mm,31.24.mm], [4591.95.mm,1275.76.mm,31.76.mm], [4591.95.mm,1275.24.mm,32.35.mm], [4591.95.mm,1274.8.mm,33.mm], [4591.95.mm,1274.46.mm,33.7.mm], [4591.95.mm,1274.2.mm,34.45.mm], [4591.95.mm,1274.05.mm,35.22.mm], [4591.95.mm,1274.mm,36.mm]])
  face.reverse! if face.normal.x < 0
  face.pushpull(19.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4591.95.mm,1262.mm,34.82.mm], [4610.95.mm,1262.mm,34.82.mm], [4610.95.mm,1274.mm,34.82.mm], [4591.95.mm,1274.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4601.45.mm,1268.mm,34.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Saddle Foot R
  grp = ents.add_group
  grp.name = "Axle Saddle Foot R"
  face = grp.entities.add_face([4591.95.mm,1286.mm,34.82.mm], [4610.95.mm,1286.mm,34.82.mm], [4610.95.mm,1298.mm,34.82.mm], [4591.95.mm,1298.mm,34.82.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.18.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Axle Bolt R
  grp = ents.add_group
  grp.name = "Axle Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4601.45.mm,1292.mm,34.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(12.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Bottom Clamp R
  grp = ents.add_group
  grp.name = "Bottom Clamp R"
  face = grp.entities.add_face([4560.9.mm,1148.mm,26.mm], [4599.mm,1148.mm,26.mm], [4599.mm,1212.mm,26.mm], [4560.9.mm,1212.mm,26.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Top Clamp R
  grp = ents.add_group
  grp.name = "Top Clamp R"
  face = grp.entities.add_face([4560.9.mm,1148.mm,67.1.mm], [4599.mm,1148.mm,67.1.mm], [4599.mm,1212.mm,67.1.mm], [4560.9.mm,1212.mm,67.1.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(3.mm)
  mat = model.materials["Spray Beam 40x25x3 304-SS RHS"] || model.materials.add("Spray Beam 40x25x3 304-SS RHS")
  mat.color = Sketchup::Color.new(184, 188, 196)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Spacer R
  grp = ents.add_group
  grp.name = "Clamp Spacer R"
  face = grp.entities.add_face([4564.9.mm,1152.95.mm,29.mm], [4595.mm,1152.95.mm,29.mm], [4595.mm,1160.95.mm,29.mm], [4564.9.mm,1160.95.mm,29.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(38.099999999999994.mm)
  mat = model.materials["Carriage Plate L L"] || model.materials.add("Carriage Plate L L")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt R
  grp = ents.add_group
  grp.name = "Clamp Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4569.9.mm,1156.95.mm,26.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(48.099999999999994.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt CSK Head R
  grp = ents.add_group
  grp.name = "Clamp Bolt CSK Head R"
  ge = grp.entities
  ge.add_face([4574.4.mm,1156.95.mm,26.mm], [4573.79711431703.mm,1159.2.mm,26.mm], [4572.065063509461.mm,1158.2.mm,29.mm], [4572.4.mm,1156.95.mm,29.mm])
  ge.add_face([4573.79711431703.mm,1159.2.mm,26.mm], [4572.15.mm,1160.84711431703.mm,26.mm], [4571.15.mm,1159.1150635094612.mm,29.mm], [4572.065063509461.mm,1158.2.mm,29.mm])
  ge.add_face([4572.15.mm,1160.84711431703.mm,26.mm], [4569.9.mm,1161.45.mm,26.mm], [4569.9.mm,1159.45.mm,29.mm], [4571.15.mm,1159.1150635094612.mm,29.mm])
  ge.add_face([4569.9.mm,1161.45.mm,26.mm], [4567.65.mm,1160.84711431703.mm,26.mm], [4568.65.mm,1159.1150635094612.mm,29.mm], [4569.9.mm,1159.45.mm,29.mm])
  ge.add_face([4567.65.mm,1160.84711431703.mm,26.mm], [4566.0028856829695.mm,1159.2.mm,26.mm], [4567.7349364905385.mm,1158.2.mm,29.mm], [4568.65.mm,1159.1150635094612.mm,29.mm])
  ge.add_face([4566.0028856829695.mm,1159.2.mm,26.mm], [4565.4.mm,1156.95.mm,26.mm], [4567.4.mm,1156.95.mm,29.mm], [4567.7349364905385.mm,1158.2.mm,29.mm])
  ge.add_face([4565.4.mm,1156.95.mm,26.mm], [4566.0028856829695.mm,1154.7.mm,26.mm], [4567.7349364905385.mm,1155.7.mm,29.mm], [4567.4.mm,1156.95.mm,29.mm])
  ge.add_face([4566.0028856829695.mm,1154.7.mm,26.mm], [4567.65.mm,1153.05288568297.mm,26.mm], [4568.65.mm,1154.784936490539.mm,29.mm], [4567.7349364905385.mm,1155.7.mm,29.mm])
  ge.add_face([4567.65.mm,1153.05288568297.mm,26.mm], [4569.9.mm,1152.45.mm,26.mm], [4569.9.mm,1154.45.mm,29.mm], [4568.65.mm,1154.784936490539.mm,29.mm])
  ge.add_face([4569.9.mm,1152.45.mm,26.mm], [4572.15.mm,1153.05288568297.mm,26.mm], [4571.15.mm,1154.784936490539.mm,29.mm], [4569.9.mm,1154.45.mm,29.mm])
  ge.add_face([4572.15.mm,1153.05288568297.mm,26.mm], [4573.79711431703.mm,1154.7.mm,26.mm], [4572.065063509461.mm,1155.7.mm,29.mm], [4571.15.mm,1154.784936490539.mm,29.mm])
  ge.add_face([4573.79711431703.mm,1154.7.mm,26.mm], [4574.4.mm,1156.95.mm,26.mm], [4572.4.mm,1156.95.mm,29.mm], [4572.065063509461.mm,1155.7.mm,29.mm])
  ge.add_face([4574.4.mm,1156.95.mm,26.mm], [4573.79711431703.mm,1159.2.mm,26.mm], [4572.15.mm,1160.84711431703.mm,26.mm], [4569.9.mm,1161.45.mm,26.mm], [4567.65.mm,1160.84711431703.mm,26.mm], [4566.0028856829695.mm,1159.2.mm,26.mm], [4565.4.mm,1156.95.mm,26.mm], [4566.0028856829695.mm,1154.7.mm,26.mm], [4567.65.mm,1153.05288568297.mm,26.mm], [4569.9.mm,1152.45.mm,26.mm], [4572.15.mm,1153.05288568297.mm,26.mm], [4573.79711431703.mm,1154.7.mm,26.mm])
  mat = model.materials["Clamp Bolt CSK Head R"] || model.materials.add("Clamp Bolt CSK Head R")
  mat.color = Sketchup::Color.new(128, 128, 138)
  grp.material = mat

  # Clamp Bolt R
  grp = ents.add_group
  grp.name = "Clamp Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4590.mm,1156.95.mm,26.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(48.099999999999994.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt CSK Head R
  grp = ents.add_group
  grp.name = "Clamp Bolt CSK Head R"
  ge = grp.entities
  ge.add_face([4594.5.mm,1156.95.mm,26.mm], [4593.89711431703.mm,1159.2.mm,26.mm], [4592.165063509461.mm,1158.2.mm,29.mm], [4592.5.mm,1156.95.mm,29.mm])
  ge.add_face([4593.89711431703.mm,1159.2.mm,26.mm], [4592.25.mm,1160.84711431703.mm,26.mm], [4591.25.mm,1159.1150635094612.mm,29.mm], [4592.165063509461.mm,1158.2.mm,29.mm])
  ge.add_face([4592.25.mm,1160.84711431703.mm,26.mm], [4590.mm,1161.45.mm,26.mm], [4590.mm,1159.45.mm,29.mm], [4591.25.mm,1159.1150635094612.mm,29.mm])
  ge.add_face([4590.mm,1161.45.mm,26.mm], [4587.75.mm,1160.84711431703.mm,26.mm], [4588.75.mm,1159.1150635094612.mm,29.mm], [4590.mm,1159.45.mm,29.mm])
  ge.add_face([4587.75.mm,1160.84711431703.mm,26.mm], [4586.10288568297.mm,1159.2.mm,26.mm], [4587.834936490539.mm,1158.2.mm,29.mm], [4588.75.mm,1159.1150635094612.mm,29.mm])
  ge.add_face([4586.10288568297.mm,1159.2.mm,26.mm], [4585.5.mm,1156.95.mm,26.mm], [4587.5.mm,1156.95.mm,29.mm], [4587.834936490539.mm,1158.2.mm,29.mm])
  ge.add_face([4585.5.mm,1156.95.mm,26.mm], [4586.10288568297.mm,1154.7.mm,26.mm], [4587.834936490539.mm,1155.7.mm,29.mm], [4587.5.mm,1156.95.mm,29.mm])
  ge.add_face([4586.10288568297.mm,1154.7.mm,26.mm], [4587.75.mm,1153.05288568297.mm,26.mm], [4588.75.mm,1154.784936490539.mm,29.mm], [4587.834936490539.mm,1155.7.mm,29.mm])
  ge.add_face([4587.75.mm,1153.05288568297.mm,26.mm], [4590.mm,1152.45.mm,26.mm], [4590.mm,1154.45.mm,29.mm], [4588.75.mm,1154.784936490539.mm,29.mm])
  ge.add_face([4590.mm,1152.45.mm,26.mm], [4592.25.mm,1153.05288568297.mm,26.mm], [4591.25.mm,1154.784936490539.mm,29.mm], [4590.mm,1154.45.mm,29.mm])
  ge.add_face([4592.25.mm,1153.05288568297.mm,26.mm], [4593.89711431703.mm,1154.7.mm,26.mm], [4592.165063509461.mm,1155.7.mm,29.mm], [4591.25.mm,1154.784936490539.mm,29.mm])
  ge.add_face([4593.89711431703.mm,1154.7.mm,26.mm], [4594.5.mm,1156.95.mm,26.mm], [4592.5.mm,1156.95.mm,29.mm], [4592.165063509461.mm,1155.7.mm,29.mm])
  ge.add_face([4594.5.mm,1156.95.mm,26.mm], [4593.89711431703.mm,1159.2.mm,26.mm], [4592.25.mm,1160.84711431703.mm,26.mm], [4590.mm,1161.45.mm,26.mm], [4587.75.mm,1160.84711431703.mm,26.mm], [4586.10288568297.mm,1159.2.mm,26.mm], [4585.5.mm,1156.95.mm,26.mm], [4586.10288568297.mm,1154.7.mm,26.mm], [4587.75.mm,1153.05288568297.mm,26.mm], [4590.mm,1152.45.mm,26.mm], [4592.25.mm,1153.05288568297.mm,26.mm], [4593.89711431703.mm,1154.7.mm,26.mm])
  mat = model.materials["Clamp Bolt CSK Head R"] || model.materials.add("Clamp Bolt CSK Head R")
  mat.color = Sketchup::Color.new(128, 128, 138)
  grp.material = mat

  # Clamp Spacer R
  grp = ents.add_group
  grp.name = "Clamp Spacer R"
  face = grp.entities.add_face([4564.9.mm,1199.05.mm,29.mm], [4595.mm,1199.05.mm,29.mm], [4595.mm,1207.05.mm,29.mm], [4564.9.mm,1207.05.mm,29.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(38.099999999999994.mm)
  mat = model.materials["Carriage Plate L L"] || model.materials.add("Carriage Plate L L")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt R
  grp = ents.add_group
  grp.name = "Clamp Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4569.9.mm,1203.05.mm,26.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(48.099999999999994.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt CSK Head R
  grp = ents.add_group
  grp.name = "Clamp Bolt CSK Head R"
  ge = grp.entities
  ge.add_face([4574.4.mm,1203.05.mm,26.mm], [4573.79711431703.mm,1205.3.mm,26.mm], [4572.065063509461.mm,1204.3.mm,29.mm], [4572.4.mm,1203.05.mm,29.mm])
  ge.add_face([4573.79711431703.mm,1205.3.mm,26.mm], [4572.15.mm,1206.94711431703.mm,26.mm], [4571.15.mm,1205.215063509461.mm,29.mm], [4572.065063509461.mm,1204.3.mm,29.mm])
  ge.add_face([4572.15.mm,1206.94711431703.mm,26.mm], [4569.9.mm,1207.55.mm,26.mm], [4569.9.mm,1205.55.mm,29.mm], [4571.15.mm,1205.215063509461.mm,29.mm])
  ge.add_face([4569.9.mm,1207.55.mm,26.mm], [4567.65.mm,1206.94711431703.mm,26.mm], [4568.65.mm,1205.215063509461.mm,29.mm], [4569.9.mm,1205.55.mm,29.mm])
  ge.add_face([4567.65.mm,1206.94711431703.mm,26.mm], [4566.0028856829695.mm,1205.3.mm,26.mm], [4567.7349364905385.mm,1204.3.mm,29.mm], [4568.65.mm,1205.215063509461.mm,29.mm])
  ge.add_face([4566.0028856829695.mm,1205.3.mm,26.mm], [4565.4.mm,1203.05.mm,26.mm], [4567.4.mm,1203.05.mm,29.mm], [4567.7349364905385.mm,1204.3.mm,29.mm])
  ge.add_face([4565.4.mm,1203.05.mm,26.mm], [4566.0028856829695.mm,1200.8.mm,26.mm], [4567.7349364905385.mm,1201.8.mm,29.mm], [4567.4.mm,1203.05.mm,29.mm])
  ge.add_face([4566.0028856829695.mm,1200.8.mm,26.mm], [4567.65.mm,1199.15288568297.mm,26.mm], [4568.65.mm,1200.8849364905388.mm,29.mm], [4567.7349364905385.mm,1201.8.mm,29.mm])
  ge.add_face([4567.65.mm,1199.15288568297.mm,26.mm], [4569.9.mm,1198.55.mm,26.mm], [4569.9.mm,1200.55.mm,29.mm], [4568.65.mm,1200.8849364905388.mm,29.mm])
  ge.add_face([4569.9.mm,1198.55.mm,26.mm], [4572.15.mm,1199.15288568297.mm,26.mm], [4571.15.mm,1200.8849364905388.mm,29.mm], [4569.9.mm,1200.55.mm,29.mm])
  ge.add_face([4572.15.mm,1199.15288568297.mm,26.mm], [4573.79711431703.mm,1200.8.mm,26.mm], [4572.065063509461.mm,1201.8.mm,29.mm], [4571.15.mm,1200.8849364905388.mm,29.mm])
  ge.add_face([4573.79711431703.mm,1200.8.mm,26.mm], [4574.4.mm,1203.05.mm,26.mm], [4572.4.mm,1203.05.mm,29.mm], [4572.065063509461.mm,1201.8.mm,29.mm])
  ge.add_face([4574.4.mm,1203.05.mm,26.mm], [4573.79711431703.mm,1205.3.mm,26.mm], [4572.15.mm,1206.94711431703.mm,26.mm], [4569.9.mm,1207.55.mm,26.mm], [4567.65.mm,1206.94711431703.mm,26.mm], [4566.0028856829695.mm,1205.3.mm,26.mm], [4565.4.mm,1203.05.mm,26.mm], [4566.0028856829695.mm,1200.8.mm,26.mm], [4567.65.mm,1199.15288568297.mm,26.mm], [4569.9.mm,1198.55.mm,26.mm], [4572.15.mm,1199.15288568297.mm,26.mm], [4573.79711431703.mm,1200.8.mm,26.mm])
  mat = model.materials["Clamp Bolt CSK Head R"] || model.materials.add("Clamp Bolt CSK Head R")
  mat.color = Sketchup::Color.new(128, 128, 138)
  grp.material = mat

  # Clamp Bolt R
  grp = ents.add_group
  grp.name = "Clamp Bolt R"
  ge = grp.entities
  circle = ge.add_circle([4590.mm,1203.05.mm,26.mm], [0,0,1], 2.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(48.099999999999994.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # Clamp Bolt CSK Head R
  grp = ents.add_group
  grp.name = "Clamp Bolt CSK Head R"
  ge = grp.entities
  ge.add_face([4594.5.mm,1203.05.mm,26.mm], [4593.89711431703.mm,1205.3.mm,26.mm], [4592.165063509461.mm,1204.3.mm,29.mm], [4592.5.mm,1203.05.mm,29.mm])
  ge.add_face([4593.89711431703.mm,1205.3.mm,26.mm], [4592.25.mm,1206.94711431703.mm,26.mm], [4591.25.mm,1205.215063509461.mm,29.mm], [4592.165063509461.mm,1204.3.mm,29.mm])
  ge.add_face([4592.25.mm,1206.94711431703.mm,26.mm], [4590.mm,1207.55.mm,26.mm], [4590.mm,1205.55.mm,29.mm], [4591.25.mm,1205.215063509461.mm,29.mm])
  ge.add_face([4590.mm,1207.55.mm,26.mm], [4587.75.mm,1206.94711431703.mm,26.mm], [4588.75.mm,1205.215063509461.mm,29.mm], [4590.mm,1205.55.mm,29.mm])
  ge.add_face([4587.75.mm,1206.94711431703.mm,26.mm], [4586.10288568297.mm,1205.3.mm,26.mm], [4587.834936490539.mm,1204.3.mm,29.mm], [4588.75.mm,1205.215063509461.mm,29.mm])
  ge.add_face([4586.10288568297.mm,1205.3.mm,26.mm], [4585.5.mm,1203.05.mm,26.mm], [4587.5.mm,1203.05.mm,29.mm], [4587.834936490539.mm,1204.3.mm,29.mm])
  ge.add_face([4585.5.mm,1203.05.mm,26.mm], [4586.10288568297.mm,1200.8.mm,26.mm], [4587.834936490539.mm,1201.8.mm,29.mm], [4587.5.mm,1203.05.mm,29.mm])
  ge.add_face([4586.10288568297.mm,1200.8.mm,26.mm], [4587.75.mm,1199.15288568297.mm,26.mm], [4588.75.mm,1200.8849364905388.mm,29.mm], [4587.834936490539.mm,1201.8.mm,29.mm])
  ge.add_face([4587.75.mm,1199.15288568297.mm,26.mm], [4590.mm,1198.55.mm,26.mm], [4590.mm,1200.55.mm,29.mm], [4588.75.mm,1200.8849364905388.mm,29.mm])
  ge.add_face([4590.mm,1198.55.mm,26.mm], [4592.25.mm,1199.15288568297.mm,26.mm], [4591.25.mm,1200.8849364905388.mm,29.mm], [4590.mm,1200.55.mm,29.mm])
  ge.add_face([4592.25.mm,1199.15288568297.mm,26.mm], [4593.89711431703.mm,1200.8.mm,26.mm], [4592.165063509461.mm,1201.8.mm,29.mm], [4591.25.mm,1200.8849364905388.mm,29.mm])
  ge.add_face([4593.89711431703.mm,1200.8.mm,26.mm], [4594.5.mm,1203.05.mm,26.mm], [4592.5.mm,1203.05.mm,29.mm], [4592.165063509461.mm,1201.8.mm,29.mm])
  ge.add_face([4594.5.mm,1203.05.mm,26.mm], [4593.89711431703.mm,1205.3.mm,26.mm], [4592.25.mm,1206.94711431703.mm,26.mm], [4590.mm,1207.55.mm,26.mm], [4587.75.mm,1206.94711431703.mm,26.mm], [4586.10288568297.mm,1205.3.mm,26.mm], [4585.5.mm,1203.05.mm,26.mm], [4586.10288568297.mm,1200.8.mm,26.mm], [4587.75.mm,1199.15288568297.mm,26.mm], [4590.mm,1198.55.mm,26.mm], [4592.25.mm,1199.15288568297.mm,26.mm], [4593.89711431703.mm,1200.8.mm,26.mm])
  mat = model.materials["Clamp Bolt CSK Head R"] || model.materials.add("Clamp Bolt CSK Head R")
  mat.color = Sketchup::Color.new(128, 128, 138)
  grp.material = mat

  # Pole Mount Flange
  grp = ents.add_group
  grp.name = "Pole Mount Flange"
  face = grp.entities.add_face([2377.5.mm,1158.mm,67.1.mm], [2421.5.mm,1158.mm,67.1.mm], [2421.5.mm,1202.mm,67.1.mm], [2377.5.mm,1202.mm,67.1.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(5.mm)
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Flange Self-Tapping Screw
  grp = ents.add_group
  grp.name = "Flange Self-Tapping Screw"
  ge = grp.entities
  circle = ge.add_circle([2383.5.mm,1164.mm,63.099999999999994.mm], [0,0,1], 1.8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(9.mm)
  mat = model.materials["Flange Self-Tapping Screw"] || model.materials.add("Flange Self-Tapping Screw")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Flange Screw Head
  grp = ents.add_group
  grp.name = "Flange Screw Head"
  ge = grp.entities
  circle = ge.add_circle([2383.5.mm,1164.mm,72.1.mm], [0,0,1], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2.5.mm)
  mat = model.materials["Flange Self-Tapping Screw"] || model.materials.add("Flange Self-Tapping Screw")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Flange Self-Tapping Screw
  grp = ents.add_group
  grp.name = "Flange Self-Tapping Screw"
  ge = grp.entities
  circle = ge.add_circle([2383.5.mm,1196.mm,63.099999999999994.mm], [0,0,1], 1.8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(9.mm)
  mat = model.materials["Flange Self-Tapping Screw"] || model.materials.add("Flange Self-Tapping Screw")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Flange Screw Head
  grp = ents.add_group
  grp.name = "Flange Screw Head"
  ge = grp.entities
  circle = ge.add_circle([2383.5.mm,1196.mm,72.1.mm], [0,0,1], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2.5.mm)
  mat = model.materials["Flange Self-Tapping Screw"] || model.materials.add("Flange Self-Tapping Screw")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Flange Self-Tapping Screw
  grp = ents.add_group
  grp.name = "Flange Self-Tapping Screw"
  ge = grp.entities
  circle = ge.add_circle([2415.5.mm,1164.mm,63.099999999999994.mm], [0,0,1], 1.8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(9.mm)
  mat = model.materials["Flange Self-Tapping Screw"] || model.materials.add("Flange Self-Tapping Screw")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Flange Screw Head
  grp = ents.add_group
  grp.name = "Flange Screw Head"
  ge = grp.entities
  circle = ge.add_circle([2415.5.mm,1164.mm,72.1.mm], [0,0,1], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2.5.mm)
  mat = model.materials["Flange Self-Tapping Screw"] || model.materials.add("Flange Self-Tapping Screw")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Flange Self-Tapping Screw
  grp = ents.add_group
  grp.name = "Flange Self-Tapping Screw"
  ge = grp.entities
  circle = ge.add_circle([2415.5.mm,1196.mm,63.099999999999994.mm], [0,0,1], 1.8.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(9.mm)
  mat = model.materials["Flange Self-Tapping Screw"] || model.materials.add("Flange Self-Tapping Screw")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Flange Screw Head
  grp = ents.add_group
  grp.name = "Flange Screw Head"
  ge = grp.entities
  circle = ge.add_circle([2415.5.mm,1196.mm,72.1.mm], [0,0,1], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(2.5.mm)
  mat = model.materials["Flange Self-Tapping Screw"] || model.materials.add("Flange Self-Tapping Screw")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Ball-Joint Socket (20mm)
  grp = ents.add_group
  grp.name = "Ball-Joint Socket (20mm)"
  ge = grp.entities
  circle = ge.add_circle([2399.5.mm,1180.mm,72.1.mm], [0,0,1], 18.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(28.mm)
  mat = model.materials["Ball-Joint Socket (20mm)"] || model.materials.add("Ball-Joint Socket (20mm)")
  mat.color = Sketchup::Color.new(200, 176, 112)
  mat.alpha = 1.0
  grp.material = mat

  # Ball-Joint Stud (M12)
  grp = ents.add_group
  grp.name = "Ball-Joint Stud (M12)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -28.mm, 24.mm)
  circle = ge.add_circle([2399.5.mm,1180.mm,88.1.mm], vec, 6.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Ball-Joint Stud (M12)"] || model.materials.add("Ball-Joint Stud (M12)")
  mat.color = Sketchup::Color.new(216, 208, 188)
  mat.alpha = 1.0
  grp.material = mat

  # Arm Tube (25 OD Al)
  grp = ents.add_group
  grp.name = "Arm Tube (25 OD Al)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -246.mm, 585.9499999999999.mm)
  circle = ge.add_circle([2399.5.mm,1156.mm,108.1.mm], vec, 12.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Carriage Plate L L"] || model.materials.add("Carriage Plate L L")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Pinch Bolt
  grp = ents.add_group
  grp.name = "Pinch Bolt"
  ge = grp.entities
  circle = ge.add_circle([2381.5.mm,1154.mm,114.1.mm], [1,0,0], 3.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(36.mm)
  mat = model.materials["Flange Self-Tapping Screw"] || model.materials.add("Flange Self-Tapping Screw")
  mat.color = Sketchup::Color.new(80, 80, 90)
  mat.alpha = 1.0
  grp.material = mat

  # Telescoping Pole
  grp = ents.add_group
  grp.name = "Telescoping Pole"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -270.mm, 605.95.mm)
  circle = ge.add_circle([2399.5.mm,910.mm,694.05.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Carriage Plate L L"] || model.materials.add("Carriage Plate L L")
  mat.color = Sketchup::Color.new(200, 216, 232)
  mat.alpha = 1.0
  grp.material = mat

  # Pole Handle
  grp = ents.add_group
  grp.name = "Pole Handle"
  ge = grp.entities
  circle = ge.add_circle([2309.5.mm,640.mm,1300.mm], [1,0,0], 9.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(180.mm)
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Hose (upper)
  grp = ents.add_group
  grp.name = "Feed Hose (upper)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 270.mm, -605.95.mm)
  circle = ge.add_circle([2419.5.mm,640.mm,1300.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Hose (lower)
  grp = ents.add_group
  grp.name = "Feed Hose (lower)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 246.mm, -585.9499999999999.mm)
  circle = ge.add_circle([2419.5.mm,910.mm,694.05.mm], vec, 8.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.061111111111131.mm, 0.mm)
  circle = ge.add_circle([2419.5.mm,1156.mm,108.1.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.061111111111131.mm, 0.mm)
  circle = ge.add_circle([2419.5.mm,1161.0611111111111.mm,108.1.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.061111111111131.mm, 0.mm)
  circle = ge.add_circle([2419.5.mm,1166.1222222222223.mm,108.1.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.061111111111131.mm, 0.mm)
  circle = ge.add_circle([2419.5.mm,1171.1833333333334.mm,108.1.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.061111111110904.mm, 0.mm)
  circle = ge.add_circle([2419.5.mm,1176.2444444444445.mm,108.1.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.061111111111131.mm, 0.mm)
  circle = ge.add_circle([2419.5.mm,1181.3055555555554.mm,108.1.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.061111111111131.mm, 0.mm)
  circle = ge.add_circle([2419.5.mm,1186.3666666666666.mm,108.1.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.061111111111131.mm, 0.mm)
  circle = ge.add_circle([2419.5.mm,1191.4277777777777.mm,108.1.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 5.061111111111131.mm, 0.mm)
  circle = ge.add_circle([2419.5.mm,1196.4888888888888.mm,108.1.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector elbow
  grp = ents.add_group
  grp.name = "Feed Flex Connector elbow"
  ge = grp.entities
  arc = ge.add_arc([2419.5.mm,1201.55.mm,98.1.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 10.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2419.5.mm,1201.55.mm,108.1.mm], [0.000000,1.000000,0.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -2.78125.mm)
  circle = ge.add_circle([2419.5.mm,1211.55.mm,98.1.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -2.78125.mm)
  circle = ge.add_circle([2419.5.mm,1211.55.mm,95.31875.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -2.78125.mm)
  circle = ge.add_circle([2419.5.mm,1211.55.mm,92.5375.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -2.78125.mm)
  circle = ge.add_circle([2419.5.mm,1211.55.mm,89.75625.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -2.78125.mm)
  circle = ge.add_circle([2419.5.mm,1211.55.mm,86.975.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -2.78125.mm)
  circle = ge.add_circle([2419.5.mm,1211.55.mm,84.19375.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -2.78125.mm)
  circle = ge.add_circle([2419.5.mm,1211.55.mm,81.4125.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -2.78125.mm)
  circle = ge.add_circle([2419.5.mm,1211.55.mm,78.63125.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector elbow
  grp = ents.add_group
  grp.name = "Feed Flex Connector elbow"
  ge = grp.entities
  arc = ge.add_arc([2409.7.mm,1211.55.mm,75.85.mm], [1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 9.800000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2419.5.mm,1211.55.mm,75.85.mm], [0.000000,0.000000,-1.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.275000000000091.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2409.7.mm,1211.55.mm,66.05.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.275000000000091.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2408.4249999999997.mm,1211.55.mm,66.05.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.2749999999996362.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2407.1499999999996.mm,1211.55.mm,66.05.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.275000000000091.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2405.875.mm,1211.55.mm,66.05.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.275000000000091.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2404.6.mm,1211.55.mm,66.05.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.2749999999996362.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2403.325.mm,1211.55.mm,66.05.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.275000000000091.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2402.05.mm,1211.55.mm,66.05.mm], vec, 7.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Feed Flex Connector
  grp = ents.add_group
  grp.name = "Feed Flex Connector"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1.275000000000091.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2400.775.mm,1211.55.mm,66.05.mm], vec, 5.6000000000000005.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Feed Hose (upper)"] || model.materials.add("Feed Hose (upper)")
  mat.color = Sketchup::Color.new(32, 96, 192)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -8.858819886353672.mm, -3.9473246461184317.mm)
  circle = ge.add_circle([2430.5.mm,685.mm,1199.0083333333332.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, -5.475051789980057.mm, -2.4395807959315334.mm)
  circle = ge.add_circle([2426.107390870624.mm,676.1411801136463.mm,1195.0610086872148.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2414.607390870624.mm,670.6661283236663.mm,1192.6214278912832.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, 5.475051789980057.mm, 2.4395807959315334.mm)
  circle = ge.add_circle([2400.392609129376.mm,670.6661283236663.mm,1192.6214278912832.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 8.858819886353672.mm, 3.9473246461184317.mm)
  circle = ge.add_circle([2388.892609129376.mm,676.1411801136463.mm,1195.0610086872148.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, 8.858819886353672.mm, 3.9473246461184317.mm)
  circle = ge.add_circle([2384.5.mm,685.mm,1199.0083333333332.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, 5.475051789980057.mm, 2.4395807959315334.mm)
  circle = ge.add_circle([2388.892609129376.mm,693.8588198863537.mm,1202.9556579794516.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2400.392609129376.mm,699.3338716763337.mm,1205.3952387753832.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, -5.475051789980057.mm, -2.4395807959315334.mm)
  circle = ge.add_circle([2414.607390870624.mm,699.3338716763337.mm,1205.3952387753832.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, -8.858819886353672.mm, -3.9473246461184317.mm)
  circle = ge.add_circle([2426.107390870624.mm,693.8588198863537.mm,1202.9556579794516.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -8.858819886353672.mm, -3.9473246461185454.mm)
  circle = ge.add_circle([2430.5.mm,775.mm,997.025.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, -5.475051789980057.mm, -2.439580795931306.mm)
  circle = ge.add_circle([2426.107390870624.mm,766.1411801136463.mm,993.0776753538814.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2414.607390870624.mm,760.6661283236663.mm,990.6380945579501.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, 5.475051789980057.mm, 2.439580795931306.mm)
  circle = ge.add_circle([2400.392609129376.mm,760.6661283236663.mm,990.6380945579501.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 8.858819886353672.mm, 3.9473246461185454.mm)
  circle = ge.add_circle([2388.892609129376.mm,766.1411801136463.mm,993.0776753538814.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, 8.858819886353672.mm, 3.9473246461185454.mm)
  circle = ge.add_circle([2384.5.mm,775.mm,997.025.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, 5.475051789980057.mm, 2.439580795931306.mm)
  circle = ge.add_circle([2388.892609129376.mm,783.8588198863537.mm,1000.9723246461185.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2400.392609129376.mm,789.3338716763337.mm,1003.4119054420498.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, -5.475051789980057.mm, -2.439580795931306.mm)
  circle = ge.add_circle([2414.607390870624.mm,789.3338716763337.mm,1003.4119054420498.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, -8.858819886353672.mm, -3.9473246461185454.mm)
  circle = ge.add_circle([2426.107390870624.mm,783.8588198863537.mm,1000.9723246461185.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -8.858819886353672.mm, -3.9473246461185454.mm)
  circle = ge.add_circle([2430.5.mm,865.mm,795.0416666666666.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, -5.475051789980057.mm, -2.439580795931306.mm)
  circle = ge.add_circle([2426.107390870624.mm,856.1411801136463.mm,791.0943420205481.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2414.607390870624.mm,850.6661283236663.mm,788.6547612246168.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, 5.475051789980057.mm, 2.439580795931306.mm)
  circle = ge.add_circle([2400.392609129376.mm,850.6661283236663.mm,788.6547612246168.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 8.858819886353672.mm, 3.9473246461185454.mm)
  circle = ge.add_circle([2388.892609129376.mm,856.1411801136463.mm,791.0943420205481.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, 8.858819886353672.mm, 3.9473246461185454.mm)
  circle = ge.add_circle([2384.5.mm,865.mm,795.0416666666666.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, 5.475051789980057.mm, 2.439580795931306.mm)
  circle = ge.add_circle([2388.892609129376.mm,873.8588198863537.mm,798.9889913127852.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2400.392609129376.mm,879.3338716763337.mm,801.4285721087165.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, -5.475051789980057.mm, -2.439580795931306.mm)
  circle = ge.add_circle([2414.607390870624.mm,879.3338716763337.mm,801.4285721087165.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, -8.858819886353672.mm, -3.9473246461185454.mm)
  circle = ge.add_circle([2426.107390870624.mm,873.8588198863537.mm,798.9889913127852.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -8.942342814431072.mm, -3.7542731160509675.mm)
  circle = ge.add_circle([2430.5.mm,951.mm,596.3916666666667.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, -5.526671798371808.mm, -2.3202683887694775.mm)
  circle = ge.add_circle([2426.107390870624.mm,942.0576571855689.mm,592.6373935506157.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2414.607390870624.mm,936.5309853871971.mm,590.3171251618462.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, 5.526671798371808.mm, 2.3202683887694775.mm)
  circle = ge.add_circle([2400.392609129376.mm,936.5309853871971.mm,590.3171251618462.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 8.942342814431072.mm, 3.7542731160509675.mm)
  circle = ge.add_circle([2388.892609129376.mm,942.0576571855689.mm,592.6373935506157.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, 8.942342814431072.mm, 3.7542731160509675.mm)
  circle = ge.add_circle([2384.5.mm,951.mm,596.3916666666667.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, 5.526671798371808.mm, 2.3202683887694775.mm)
  circle = ge.add_circle([2388.892609129376.mm,959.9423428144311.mm,600.1459397827176.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2400.392609129376.mm,965.4690146128029.mm,602.4662081714871.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, -5.526671798371808.mm, -2.3202683887694775.mm)
  circle = ge.add_circle([2414.607390870624.mm,965.4690146128029.mm,602.4662081714871.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, -8.942342814431072.mm, -3.7542731160509675.mm)
  circle = ge.add_circle([2426.107390870624.mm,959.9423428144311.mm,600.1459397827176.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -8.942342814431186.mm, -3.7542731160509675.mm)
  circle = ge.add_circle([2430.5.mm,1033.mm,401.075.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, -5.526671798371694.mm, -2.3202683887694207.mm)
  circle = ge.add_circle([2426.107390870624.mm,1024.0576571855688.mm,397.320726883949.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2414.607390870624.mm,1018.5309853871971.mm,395.0004584951796.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, 5.526671798371694.mm, 2.3202683887694207.mm)
  circle = ge.add_circle([2400.392609129376.mm,1018.5309853871971.mm,395.0004584951796.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 8.942342814431186.mm, 3.7542731160509675.mm)
  circle = ge.add_circle([2388.892609129376.mm,1024.0576571855688.mm,397.320726883949.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, 8.942342814431186.mm, 3.7542731160509675.mm)
  circle = ge.add_circle([2384.5.mm,1033.mm,401.075.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, 5.526671798371808.mm, 2.3202683887694207.mm)
  circle = ge.add_circle([2388.892609129376.mm,1041.9423428144312.mm,404.82927311605096.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2400.392609129376.mm,1047.469014612803.mm,407.1495415048204.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, -5.526671798371808.mm, -2.3202683887694207.mm)
  circle = ge.add_circle([2414.607390870624.mm,1047.469014612803.mm,407.1495415048204.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, -8.942342814431186.mm, -3.7542731160509675.mm)
  circle = ge.add_circle([2426.107390870624.mm,1041.9423428144312.mm,404.82927311605096.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, -8.942342814431186.mm, -3.754273116050939.mm)
  circle = ge.add_circle([2430.5.mm,1115.mm,205.75833333333333.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, -5.526671798371808.mm, -2.3202683887694775.mm)
  circle = ge.add_circle([2426.107390870624.mm,1106.0576571855688.mm,202.0040602172824.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2414.607390870624.mm,1100.530985387197.mm,199.6837918285129.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.5.mm, 5.526671798371808.mm, 2.3202683887694775.mm)
  circle = ge.add_circle([2400.392609129376.mm,1100.530985387197.mm,199.6837918285129.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(-4.392609129376069.mm, 8.942342814431186.mm, 3.754273116050939.mm)
  circle = ge.add_circle([2388.892609129376.mm,1106.0576571855688.mm,202.0040602172824.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, 8.942342814431186.mm, 3.754273116050939.mm)
  circle = ge.add_circle([2384.5.mm,1115.mm,205.75833333333333.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, 5.526671798371808.mm, 2.3202683887694775.mm)
  circle = ge.add_circle([2388.892609129376.mm,1123.9423428144312.mm,209.51260644938426.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(14.214781741247862.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2400.392609129376.mm,1129.469014612803.mm,211.83287483815374.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.5.mm, -5.526671798371808.mm, -2.3202683887694775.mm)
  circle = ge.add_circle([2414.607390870624.mm,1129.469014612803.mm,211.83287483815374.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Zip Tie
  grp = ents.add_group
  grp.name = "Zip Tie"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.392609129376069.mm, -8.942342814431186.mm, -3.754273116050939.mm)
  circle = ge.add_circle([2426.107390870624.mm,1123.9423428144312.mm,209.51260644938426.mm], vec, 1.2.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Zip Tie"] || model.materials.add("Zip Tie")
  mat.color = Sketchup::Color.new(136, 136, 136)
  mat.alpha = 1.0
  grp.material = mat

  # Center Feed Barb Tee
  grp = ents.add_group
  grp.name = "Center Feed Barb Tee"
  ge = grp.entities
  circle = ge.add_circle([2399.5.mm,1211.55.mm,46.05.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(18.mm)
  mat = model.materials["Nozzle Body"] || model.materials.add("Nozzle Body")
  mat.color = Sketchup::Color.new(59, 122, 59)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Spray Bar"
  inst.layer = model.layers["Spray Bar"]

  # ═══ IBC Tanks (full) ═══
  defn = model.definitions.add("IBC Tanks (full)")
  ents = defn.entities
  # IBC Brown (developer) pallet
  grp = ents.add_group
  grp.name = "IBC Brown (developer) pallet"
  face = grp.entities.add_face([4674.mm,30.mm,0.mm], [5893.mm,30.mm,0.mm], [5893.mm,1046.mm,0.mm], [4674.mm,1046.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(168.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
  grp.material = mat

  # IBC Brown (developer) bottle
  grp = ents.add_group
  grp.name = "IBC Brown (developer) bottle"
  face = grp.entities.add_face([4704.mm,60.mm,168.mm], [5863.mm,60.mm,168.mm], [5863.mm,1016.mm,168.mm], [4704.mm,1016.mm,168.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(980.mm)
  mat = model.materials["IBC Brown (developer) bottle"] || model.materials.add("IBC Brown (developer) bottle")
  mat.color = Sketchup::Color.new(161, 149, 143)
  mat.alpha = 0.18
  grp.material = mat

  # IBC Blue #1 pallet
  grp = ents.add_group
  grp.name = "IBC Blue #1 pallet"
  face = grp.entities.add_face([4674.mm,30.mm,1168.mm], [5893.mm,30.mm,1168.mm], [5893.mm,1046.mm,1168.mm], [4674.mm,1046.mm,1168.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(168.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
  grp.material = mat

  # IBC Blue #1 bottle
  grp = ents.add_group
  grp.name = "IBC Blue #1 bottle"
  face = grp.entities.add_face([4704.mm,60.mm,1336.mm], [5863.mm,60.mm,1336.mm], [5863.mm,1016.mm,1336.mm], [4704.mm,1016.mm,1336.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(980.mm)
  mat = model.materials["IBC Blue #1 bottle"] || model.materials.add("IBC Blue #1 bottle")
  mat.color = Sketchup::Color.new(140, 162, 190)
  mat.alpha = 0.18
  grp.material = mat

  # IBC Waste pallet
  grp = ents.add_group
  grp.name = "IBC Waste pallet"
  face = grp.entities.add_face([4674.mm,1316.mm,0.mm], [5893.mm,1316.mm,0.mm], [5893.mm,2332.mm,0.mm], [4674.mm,2332.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(168.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
  grp.material = mat

  # IBC Waste bottle
  grp = ents.add_group
  grp.name = "IBC Waste bottle"
  face = grp.entities.add_face([4704.mm,1346.mm,168.mm], [5863.mm,1346.mm,168.mm], [5863.mm,2302.mm,168.mm], [4704.mm,2302.mm,168.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(980.mm)
  mat = model.materials["Walkway Near (fixed, bump integral)"] || model.materials.add("Walkway Near (fixed, bump integral)")
  mat.color = Sketchup::Color.new(165, 165, 168)
  mat.alpha = 0.18
  grp.material = mat

  # IBC Blue #2 pallet
  grp = ents.add_group
  grp.name = "IBC Blue #2 pallet"
  face = grp.entities.add_face([4674.mm,1316.mm,1168.mm], [5893.mm,1316.mm,1168.mm], [5893.mm,2332.mm,1168.mm], [4674.mm,2332.mm,1168.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(168.mm)
  mat = model.materials["IBC Brown (developer) pallet"] || model.materials.add("IBC Brown (developer) pallet")
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
  grp.material = mat

  # IBC Blue #2 bottle
  grp = ents.add_group
  grp.name = "IBC Blue #2 bottle"
  face = grp.entities.add_face([4704.mm,1346.mm,1336.mm], [5863.mm,1346.mm,1336.mm], [5863.mm,2302.mm,1336.mm], [4704.mm,2302.mm,1336.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(980.mm)
  mat = model.materials["IBC Blue #1 bottle"] || model.materials.add("IBC Blue #1 bottle")
  mat.color = Sketchup::Color.new(140, 162, 190)
  mat.alpha = 0.18
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "IBC Tanks (full)"
  inst.layer = model.layers["IBC"]

  # ═══ IBC restraint (bars + wall anchors) ═══
  defn = model.definitions.add("IBC restraint (bars + wall anchors)")
  ents = defn.entities
  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,0.mm,560.mm], [4674.mm,0.mm,560.mm], [4674.mm,1096.mm,560.mm], [4654.mm,1096.mm,560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,0.mm,1760.mm], [4674.mm,0.mm,1760.mm], [4674.mm,1096.mm,1760.mm], [4654.mm,1096.mm,1760.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,1266.mm,560.mm], [4674.mm,1266.mm,560.mm], [4674.mm,2362.mm,560.mm], [4654.mm,2362.mm,560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Front Retaining Bar
  grp = ents.add_group
  grp.name = "Front Retaining Bar"
  face = grp.entities.add_face([4654.mm,1266.mm,1760.mm], [4674.mm,1266.mm,1760.mm], [4674.mm,2362.mm,1760.mm], [4654.mm,2362.mm,1760.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,520.mm,585.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,520.mm,1785.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,940.mm,585.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,940.mm,1785.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,1422.mm,585.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,1422.mm,1785.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,1842.mm,585.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # D-Ring Holder
  grp = ents.add_group
  grp.name = "D-Ring Holder"
  ge = grp.entities
  circle = ge.add_circle([4648.mm,1842.mm,1785.mm], [1,0,0], 16.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4646.mm,0.mm,530.mm], [4712.mm,0.mm,530.mm], [4712.mm,4.mm,530.mm], [4646.mm,4.mm,530.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,0.mm,556.mm], [4708.mm,0.mm,556.mm], [4708.mm,70.mm,556.mm], [4650.mm,70.mm,556.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.mm,-48.mm,517.5.mm], [4729.mm,-48.mm,517.5.mm], [4729.mm,-40.mm,517.5.mm], [4629.mm,-40.mm,517.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4646.mm,0.mm,1730.mm], [4712.mm,0.mm,1730.mm], [4712.mm,4.mm,1730.mm], [4646.mm,4.mm,1730.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,0.mm,1756.mm], [4708.mm,0.mm,1756.mm], [4708.mm,70.mm,1756.mm], [4650.mm,70.mm,1756.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.mm,-48.mm,1717.5.mm], [4729.mm,-48.mm,1717.5.mm], [4729.mm,-40.mm,1717.5.mm], [4629.mm,-40.mm,1717.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4646.mm,2358.mm,530.mm], [4712.mm,2358.mm,530.mm], [4712.mm,2362.mm,530.mm], [4646.mm,2362.mm,530.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,2292.mm,556.mm], [4708.mm,2292.mm,556.mm], [4708.mm,2362.mm,556.mm], [4650.mm,2362.mm,556.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.mm,2402.mm,517.5.mm], [4729.mm,2402.mm,517.5.mm], [4729.mm,2410.mm,517.5.mm], [4629.mm,2410.mm,517.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
  grp.material = mat

  # Wall Hanger Plate
  grp = ents.add_group
  grp.name = "Wall Hanger Plate"
  face = grp.entities.add_face([4646.mm,2358.mm,1730.mm], [4712.mm,2358.mm,1730.mm], [4712.mm,2362.mm,1730.mm], [4646.mm,2362.mm,1730.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Wall Hanger Seat
  grp = ents.add_group
  grp.name = "Wall Hanger Seat"
  face = grp.entities.add_face([4650.mm,2292.mm,1756.mm], [4708.mm,2292.mm,1756.mm], [4708.mm,2362.mm,1756.mm], [4650.mm,2362.mm,1756.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(4.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # IBC Wall Backing Plate (ext)
  grp = ents.add_group
  grp.name = "IBC Wall Backing Plate (ext)"
  face = grp.entities.add_face([4629.mm,2402.mm,1717.5.mm], [4729.mm,2402.mm,1717.5.mm], [4729.mm,2410.mm,1717.5.mm], [4629.mm,2410.mm,1717.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(135.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "IBC restraint (bars + wall anchors)"
  inst.layer = model.layers["IBC Frame"]

  # ═══ End wall (context) ═══
  defn = model.definitions.add("End wall (context)")
  ents = defn.entities
  # End wall (context)
  grp = ents.add_group
  grp.name = "End wall (context)"
  face = grp.entities.add_face([5893.mm,0.mm,0.mm], [5933.mm,0.mm,0.mm], [5933.mm,2362.mm,0.mm], [5893.mm,2362.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2388.mm)
  mat = model.materials["End wall (context)"] || model.materials.add("End wall (context)")
  mat.color = Sketchup::Color.new(239, 237, 228)
  mat.alpha = 0.12
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "End wall (context)"
  inst.layer = model.layers["Context"]

  # ═══ Pinhole Assembly ═══
  defn = model.definitions.add("Pinhole Assembly")
  ents = defn.entities
  # Pinhole Mount Plate
  grp = ents.add_group
  grp.name = "Pinhole Mount Plate"
  face = grp.entities.add_face([2349.mm,0.mm,1144.mm], [2449.mm,0.mm,1144.mm], [2449.mm,3.mm,1144.mm], [2349.mm,3.mm,1144.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Pinhole Aperture (Ø2.17)
  grp = ents.add_group
  grp.name = "Pinhole Aperture (Ø2.17)"
  face = grp.entities.add_face([2397.915.mm,3.mm,1192.915.mm], [2400.085.mm,3.mm,1192.915.mm], [2400.085.mm,4.mm,1192.915.mm], [2397.915.mm,4.mm,1192.915.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2.17.mm)
  mat = model.materials["Pinhole Aperture (Ø2.17)"] || model.materials.add("Pinhole Aperture (Ø2.17)")
  mat.color = Sketchup::Color.new(195, 159, 127)
  mat.alpha = 0.18
  grp.material = mat

  # TS Base Plate (wall mount)
  grp = ents.add_group
  grp.name = "TS Base Plate (wall mount)"
  face = grp.entities.add_face([2229.mm,-52.mm,1024.mm], [2569.mm,-52.mm,1024.mm], [2569.mm,-40.mm,1024.mm], [2229.mm,-40.mm,1024.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(340.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Pinhole Tilt-Swing Board
  grp = ents.add_group
  grp.name = "Pinhole Tilt-Swing Board"
  face = grp.entities.add_face([2259.mm,-80.mm,1054.mm], [2539.mm,-80.mm,1054.mm], [2539.mm,-64.mm,1054.mm], [2259.mm,-64.mm,1054.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(280.mm)
  mat = model.materials["Pinhole Tilt-Swing Board"] || model.materials.add("Pinhole Tilt-Swing Board")
  mat.color = Sketchup::Color.new(194, 199, 208)
  mat.alpha = 0.18
  grp.material = mat

  # TS Tilt Knob
  grp = ents.add_group
  grp.name = "TS Tilt Knob"
  face = grp.entities.add_face([2384.mm,-100.mm,1029.mm], [2414.mm,-100.mm,1029.mm], [2414.mm,-75.mm,1029.mm], [2384.mm,-75.mm,1029.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # TS Swing Knob
  grp = ents.add_group
  grp.name = "TS Swing Knob"
  face = grp.entities.add_face([2539.mm,-100.mm,1179.mm], [2564.mm,-100.mm,1179.mm], [2564.mm,-75.mm,1179.mm], [2539.mm,-75.mm,1179.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(30.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Pinhole Assembly"
  inst.layer = model.layers["Pinhole"]

  # ═══ Wall backing (ply) ═══
  defn = model.definitions.add("Wall backing (ply)")
  ents = defn.entities
  # Wall backing (18mm ply)
  grp = ents.add_group
  grp.name = "Wall backing (18mm ply)"
  face = grp.entities.add_face([2780.mm,0.mm,920.mm], [4575.mm,0.mm,920.mm], [4575.mm,18.mm,920.mm], [2780.mm,18.mm,920.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1440.mm)
  mat = model.materials["Wall backing (18mm ply)"] || model.materials.add("Wall backing (18mm ply)")
  mat.color = Sketchup::Color.new(178, 167, 154)
  mat.alpha = 0.18
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Wall backing (ply)"
  inst.layer = model.layers["Backing"]

  # ═══ TAP-01 + spray-bar supply ═══
  defn = model.definitions.add("TAP-01 + spray-bar supply")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-BV-05 (spray selector) body
  grp = ents.add_group
  grp.name = "3W-BV-05 (spray selector) body"
  face = grp.entities.add_face([2226.mm,46.mm,677.mm], [2272.mm,46.mm,677.mm], [2272.mm,92.mm,677.mm], [2226.mm,92.mm,677.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.mm)
  mat = model.materials["3W-BV-05 (spray selector) body"] || model.materials.add("3W-BV-05 (spray selector) body")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-BV-05 (spray selector) run +
  grp = ents.add_group
  grp.name = "3W-BV-05 (spray selector) run +"
  ge = grp.entities
  circle = ge.add_circle([2249.mm,69.mm,723.mm], [0,0,1], 13.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(10.mm)
  mat = model.materials["3W-BV-05 (spray selector) body"] || model.materials.add("3W-BV-05 (spray selector) body")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-BV-05 (spray selector) run -
  grp = ents.add_group
  grp.name = "3W-BV-05 (spray selector) run -"
  ge = grp.entities
  circle = ge.add_circle([2249.mm,69.mm,667.mm], [0,0,1], 13.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(10.mm)
  mat = model.materials["3W-BV-05 (spray selector) body"] || model.materials.add("3W-BV-05 (spray selector) body")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-BV-05 (spray selector) branch
  grp = ents.add_group
  grp.name = "3W-BV-05 (spray selector) branch"
  ge = grp.entities
  circle = ge.add_circle([2272.mm,69.mm,700.mm], [1,0,0], 13.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["3W-BV-05 (spray selector) body"] || model.materials.add("3W-BV-05 (spray selector) body")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-BV-05 (spray selector) handle stem
  grp = ents.add_group
  grp.name = "3W-BV-05 (spray selector) handle stem"
  ge = grp.entities
  circle = ge.add_circle([2249.mm,92.mm,700.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(42.mm)
  mat = model.materials["3W-BV-05 (spray selector) handle stem"] || model.materials.add("3W-BV-05 (spray selector) handle stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-BV-05 (spray selector) handle lever
  grp = ents.add_group
  grp.name = "3W-BV-05 (spray selector) handle lever"
  face = grp.entities.add_face([2241.mm,133.mm,668.mm], [2257.mm,133.mm,668.mm], [2257.mm,147.mm,668.mm], [2241.mm,147.mm,668.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(64.mm)
  mat = model.materials["3W-BV-05 (spray selector) handle stem"] || model.materials.add("3W-BV-05 (spray selector) handle stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # BV-05 fresh supply (trunk -> selector)
  grp = ents.add_group
  grp.name = "BV-05 fresh supply (trunk -> selector)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 619.mm)
  circle = ge.add_circle([2249.mm,69.mm,48.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(13.099999999999909.mm, 41.099999999999994.mm, -1.2999999999999545.mm)
  circle = ge.add_circle([2249.mm,69.mm,733.mm], vec, 7.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(30.994778088595467.mm, 5.710808891153519.mm, -28.100404037968133.mm)
  circle = ge.add_circle([2262.1.mm,110.1.mm,731.7.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.615204002314385.mm, 22.987856633323375.mm, -12.02663725929824.mm)
  circle = ge.add_circle([2293.0947780885954.mm,115.81080889115351.mm,703.5995959620319.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.52927301618729.mm, 23.681503268653614.mm, 10.769187840958239.mm)
  circle = ge.add_circle([2271.479574086281.mm,138.7986655244769.mm,691.5729587027337.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-6.146142164319372.mm, 19.292521678056943.mm, 27.024473060918353.mm)
  circle = ge.add_circle([2249.9503010700937.mm,162.4801687931305.mm,702.3421465436919.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(15.584291689368001.mm, 12.374418878521567.mm, 27.28190261661041.mm)
  circle = ge.add_circle([2243.8041589057743.mm,181.77269047118745.mm,729.3666196046103.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(31.01927437008453.mm, 6.952143181680469.mm, 11.391704137548686.mm)
  circle = ge.add_circle([2259.3884505951423.mm,194.147109349709.mm,756.6485222212207.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(31.178741649094263.mm, 6.180371533454974.mm, -11.401213852486649.mm)
  circle = ge.add_circle([2290.407724965227.mm,201.09925253138948.mm,768.0402263587694.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(15.96991555329987.mm, 10.508120244024838.mm, -27.835944506702276.mm)
  circle = ge.add_circle([2321.586466614321.mm,207.27962406484446.mm,756.6390125062827.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.758717462268578.mm, 17.417507551507356.mm, -28.35077078856193.mm)
  circle = ge.add_circle([2337.556382167621.mm,217.7877443088693.mm,728.8030679995804.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.365450949425394.mm, 22.888655812636358.mm, -12.646167057293837.mm)
  circle = ge.add_circle([2331.7976647053524.mm,235.20525186037665.mm,700.4522972110185.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.77029615699803.mm, 23.738454051118936.mm, 10.140937083038125.mm)
  circle = ge.add_circle([2310.432213755927.mm,258.093907673013.mm,687.8061301537247.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-6.737714371280163.mm, 19.47249013051794.mm, 26.75301728012289.mm)
  circle = ge.add_circle([2288.661917598929.mm,281.83236172413194.mm,697.9470672367628.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(14.986346793020402.mm, 12.572699456717203.mm, 27.525174633288543.mm)
  circle = ge.add_circle([2281.924203227649.mm,301.3048518546499.mm,724.7000845168857.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(30.76284078820754.mm, 7.053376356912736.mm, 12.008168429438115.mm)
  circle = ge.add_circle([2296.9105500206692.mm,313.8775513113671.mm,752.2252591501742.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(31.413012295168755.mm, 6.125659901400809.mm, -10.77021586313765.mm)
  circle = ge.add_circle([2327.673390808877.mm,320.9309276682798.mm,764.2334275796123.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.558591897410224.mm, 10.32929500139312.mm, -27.557527094640363.mm)
  circle = ge.add_circle([2359.0864031040455.mm,327.05658756968063.mm,753.4632117164747.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-5.15812698551008.mm, 17.21860912372449.mm, -28.58691704728517.mm)
  circle = ge.add_circle([2375.6449950014558.mm,337.38588257107375.mm,725.9056846218343.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.102369541069493.mm, 22.785403192942.mm, -13.259487226504461.mm)
  circle = ge.add_circle([2370.4868680159457.mm,354.60449169479824.mm,697.3187675745492.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-21.997784432226126.mm, 23.790919555486653.mm, 9.507272332288949.mm)
  circle = ge.add_circle([2349.384498474876.mm,377.38989488774024.mm,684.0592803480447.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-7.3234197797132765.mm, 19.650149358061583.mm, 26.467673742862075.mm)
  circle = ge.add_circle([2327.38671404265.mm,401.1808144432269.mm,693.5665526803336.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(14.38318732806465.mm, 12.772190368931774.mm, 27.754165018753497.mm)
  circle = ge.add_circle([2320.063294262937.mm,420.8309638012885.mm,720.0342264231957.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(30.493145103667757.mm, 7.158635253449802.mm, 12.618266260360997.mm)
  circle = ge.add_circle([2334.4464815910014.mm,433.60315417022025.mm,747.7883914419492.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.9603733053309043.mm, -1.861789423670075.mm, -39.106657702310144.mm)
  circle = ge.add_circle([2364.939626694669.mm,440.76178942367005.mm,760.4066577023102.mm], vec, 7.mm, 8)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(13.099999999999909.mm, 41.10000000000002.mm, -1.3000000000000682.mm)
  circle = ge.add_circle([2366.9.mm,438.9.mm,721.3000000000001.mm], vec, 7.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.mm, 18.mm, -28.mm)
  circle = ge.add_circle([2380.mm,480.mm,720.mm], vec, 7.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(24.97000885059242.mm, -18.972170521903422.mm, -28.294146488071874.mm)
  circle = ge.add_circle([2383.mm,498.mm,692.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-27.45985123689161.mm, 3.504902623379337.mm, -19.46208447547781.mm)
  circle = ge.add_circle([2407.9700088505924.mm,479.0278294780966.mm,663.7058535119281.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-24.355668455928026.mm, 22.438592715439142.mm, -6.95783554690729.mm)
  circle = ge.add_circle([2380.510157613701.mm,482.5327321014759.mm,644.2437690364503.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-6.197613036183611.mm, 33.21188285064022.mm, 1.9133569064084668.mm)
  circle = ge.add_circle([2356.154489157773.mm,504.97132481691506.mm,637.285933489543.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.405999792017155.mm, 29.530791918116165.mm, 1.9687569670934408.mm)
  circle = ge.add_circle([2349.956876121589.mm,538.1832076675553.mm,639.1992903959515.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(30.249667309207325.mm, 13.54589012491897.mm, -6.824001237405923.mm)
  circle = ge.add_circle([2366.3628759136063.mm,567.7139995856714.mm,641.1680473630449.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(27.245629809221555.mm, -5.404109036339378.mm, -19.328004716070495.mm)
  circle = ge.add_circle([2396.6125432228137.mm,581.2598897105904.mm,634.344046125639.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.14890874269986.mm, -16.24822026079073.mm, -28.23815347463085.mm)
  circle = ge.add_circle([2423.858173032035.mm,575.855780674251.mm,615.0160414095685.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-13.468013470236201.mm, -12.651087278041018.mm, -28.348952508534808.mm)
  circle = ge.add_circle([2433.007081774735.mm,559.6075604134603.mm,586.7778879349377.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-27.391858489569586.mm, 3.2857696926852213.mm, -19.595670707996646.mm)
  circle = ge.add_circle([2419.539068304499.mm,546.9564731354193.mm,558.4289354264029.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-24.488025237776583.mm, 22.25170594754036.mm, -7.092158124326147.mm)
  circle = ge.add_circle([2392.1472098149293.mm,550.2422428281045.mm,538.8332647184062.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-6.452993750807764.mm, 33.16642539871111.mm, 1.8567720393160698.mm)
  circle = ge.add_circle([2367.6591845771527.mm,572.4939487756449.mm,531.7411065940801.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(16.17679389205341.mm, 29.65332097501073.mm, 2.0229678715294312.mm)
  circle = ge.add_circle([2361.206190826345.mm,605.660374174356.mm,533.5978786333961.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(30.180543097919326.mm, 13.76482165642392.mm, -6.690665704076537.mm)
  circle = ge.add_circle([2377.3829847183983.mm,635.3136951493667.mm,535.6208465049256.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(27.376971094590772.mm, -5.216679403592934.mm, -19.193441957301047.mm)
  circle = ge.add_circle([2407.5635278163177.mm,649.0785168057906.mm,528.930180800849.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.403983202583731.mm, -16.201792832959995.mm, -28.180977864609247.mm)
  circle = ge.add_circle([2434.9404989109084.mm,643.8618374021977.mm,509.736738843548.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-13.238225662855712.mm, -12.772785928160488.mm, -28.4025672328209.mm)
  circle = ge.add_circle([2444.344482113492.mm,627.6600445692377.mm,481.55576097893874.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-24.106256450636465.mm, 27.11274135892279.mm, 14.846806253882164.mm)
  circle = ge.add_circle([2431.1062564506365.mm,614.8872586410772.mm,453.15319374611784.mm], vec, 7.mm, 8)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3.mm, 18.mm, -28.mm)
  circle = ge.add_circle([2407.mm,642.mm,468.mm], vec, 7.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.mm, -2.7000000000000455.mm, 86.29999999999995.mm)
  circle = ge.add_circle([2410.mm,660.mm,440.mm], vec, 7.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-27.46521617674125.mm, 27.273596242938652.mm, 16.879914870282846.mm)
  circle = ge.add_circle([2411.mm,657.3.mm,526.3.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.368024200198306.mm, -28.072821024295422.mm, 14.961809208659588.mm)
  circle = ge.add_circle([2383.5347838232587.mm,684.5735962429386.mm,543.1799148702828.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(11.453940774087641.mm, -28.179134091467745.mm, 14.694033887041428.mm)
  circle = ge.add_circle([2372.1667596230604.mm,656.5007752186432.mm,558.1417240789424.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(27.712832147146855.mm, -12.164272368487104.mm, 15.006678560030878.mm)
  circle = ge.add_circle([2383.620700397148.mm,628.3216411271754.mm,572.8357579659838.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(27.942083184783314.mm, 10.647281081138885.mm, 15.717709188957429.mm)
  circle = ge.add_circle([2411.333532544295.mm,616.1573687586883.mm,587.8424365260147.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(12.008214906365993.mm, 26.97374165803899.mm, 16.41313574557421.mm)
  circle = ge.add_circle([2439.2756157290783.mm,626.8046498398272.mm,603.5601457149721.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.81144719705344.mm, 27.309201177075693.mm, 16.6880535069281.mm)
  circle = ge.add_circle([2451.2838306354442.mm,653.7783914978662.mm,619.9732814605463.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-27.230397348596398.mm, 11.45834189789855.mm, 16.382394527759516.mm)
  circle = ge.add_circle([2440.472383438391.mm,681.0875926749419.mm,636.6613349674744.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-27.688876291088036.mm, -11.349841796190958.mm, 15.674125500742775.mm)
  circle = ge.add_circle([2413.2419860897944.mm,692.5459345728405.mm,653.043729495234.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-11.919939532080662.mm, -27.83552731017585.mm, 14.975628540757043.mm)
  circle = ge.add_circle([2385.5531097987064.mm,681.1960927766495.mm,668.7178549959767.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(10.895117061978453.mm, -28.40009943123266.mm, 14.693596080491602.mm)
  circle = ge.add_circle([2373.6331702666257.mm,653.3605654664736.mm,683.6934835367338.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(27.472469223098415.mm, -12.714842041046722.mm, 14.992238523045103.mm)
  circle = ge.add_circle([2384.528287328604.mm,624.960466035241.mm,698.3870796172254.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(28.160129807215526.mm, 10.087670417252298.mm, 15.697674479630336.mm)
  circle = ge.add_circle([2412.0007565517026.mm,612.2456239941943.mm,713.3793181402705.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(12.557715746340818.mm, 26.730917365423238.mm, 16.39917136052179.mm)
  circle = ge.add_circle([2440.160886358918.mm,622.3332944114466.mm,729.0769926199008.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-10.25043316458823.mm, 27.52454511984365.mm, 16.688290060960526.mm)
  circle = ge.add_circle([2452.718602105259.mm,649.0642117768698.mm,745.4761639804226.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-26.98451458268164.mm, 12.006472353628851.mm, 16.396694289805282.mm)
  circle = ge.add_circle([2442.4681689406707.mm,676.5887568967134.mm,762.1644540413831.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-27.90128741941544.mm, -10.788067960886679.mm, 15.694162586300763.mm)
  circle = ge.add_circle([2415.483654357989.mm,688.5952292503423.mm,778.5611483311884.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-12.46697043227232.mm, -27.58719694146737.mm, 14.989736569676097.mm)
  circle = ge.add_circle([2387.5823669385736.mm,677.8071612894556.mm,794.2553109174892.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(10.33196931878183.mm, -28.609800247529847.mm, 14.693560802845923.mm)
  circle = ge.add_circle([2375.1153965063013.mm,650.2199643479883.mm,809.2450474871653.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(27.221091426338262.mm, -13.260477970351758.mm, 14.978080478869515.mm)
  circle = ge.add_circle([2385.447365825083.mm,621.6101641004584.mm,823.9386082900112.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(28.366884007902627.mm, 9.523790096823518.mm, 15.677637039701608.mm)
  circle = ge.add_circle([2412.6684572514214.mm,608.3496861301066.mm,838.9166887688807.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(13.102221508105231.mm, 26.477105978620784.mm, 16.38492111131984.mm)
  circle = ge.add_circle([2441.035341259324.mm,617.8734762269302.mm,854.5943258085823.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.685208535589481.mm, 27.728581649620992.mm, 16.68812405865924.mm)
  circle = ge.add_circle([2454.1375627674292.mm,644.350582205551.mm,870.9792469199022.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-26.727667120577735.mm, 12.549558698625333.mm, 16.410709187480734.mm)
  circle = ge.add_circle([2444.4523542318398.mm,672.0791638551719.mm,887.6673709785614.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-28.10236382974381.mm, -10.222138054183347.mm, 15.71419835870438.mm)
  circle = ge.add_circle([2417.724687111262.mm,684.6287225537973.mm,904.0780801660421.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-13.008896111767172.mm, -27.32793014763672.mm, 15.004127601226742.mm)
  circle = ge.add_circle([2389.622323281518.mm,674.4065844996139.mm,919.7922785247465.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.764724838479651.mm, -28.808151902298164.mm, 14.693928068343553.mm)
  circle = ge.add_circle([2376.613427169751.mm,647.0786543519772.mm,934.7964061259732.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(26.958800216315012.mm, -13.800959930424483.mm, 14.964210141880244.mm)
  circle = ge.add_circle([2386.3781520082307.mm,618.270502449679.mm,949.4903341943168.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(28.562262338076835.mm, 8.955867709510926.mm, 15.6576049565507.mm)
  circle = ge.add_circle([2413.3369522245457.mm,604.4695425192546.mm,964.454544336197.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(13.641512421831976.mm, 26.212409939310646.mm, 16.3703907495601.mm)
  circle = ge.add_circle([2441.8992145626225.mm,613.4254102287655.mm,980.1121492927477.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-9.116001442296238.mm, 27.921228414528514.mm, 16.687555567025015.mm)
  circle = ge.add_circle([2455.5407269844545.mm,639.6378201680761.mm,996.4825400423078.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-26.4599586293657.mm, 13.087381735956797.mm, 16.42443356418505.mm)
  circle = ge.add_circle([2446.4247255421583.mm,667.5590485826046.mm,1013.1700956093329.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-28.292024364937333.mm, -9.652280492980253.mm, 15.734224731246968.mm)
  circle = ge.add_circle([2419.9647669127926.mm,680.6464303185614.mm,1029.594529173518.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-13.545497842092573.mm, -27.05783157223857.mm, 15.018795826996211.mm)
  circle = ge.add_circle([2391.6727425478553.mm,670.9941498255812.mm,1045.3287539047649.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(9.19361256854836.mm, -28.995074338149834.mm, 14.694697728750725.mm)
  circle = ge.add_circle([2378.1272447057627.mm,643.9363182533426.mm,1060.347549731761.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(26.68570145727972.mm, -14.336069775498231.mm, 14.950633110331182.mm)
  circle = ge.add_circle([2387.320857274311.mm,614.9412439151928.mm,1075.0422474605118.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(28.746185940422947.mm, 8.384132476406307.mm, 15.637586315395538.mm)
  circle = ge.add_circle([2414.0065587315908.mm,600.6051741396946.mm,1089.992880570843.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(14.175370822477362.mm, 25.936936082363673.mm, 16.355586139891102.mm)
  circle = ge.add_circle([2442.7527446720137.mm,608.9893066161009.mm,1105.6304668862385.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-8.54304162432436.mm, 28.102407659747996.mm, 16.686584815508468.mm)
  circle = ge.add_circle([2456.928115494491.mm,634.9262426984645.mm,1121.9860530261296.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-26.18149715978143.mm, 13.619724393033493.mm, 16.437861880576065.mm)
  circle = ge.add_circle([2448.3850738701667.mm,663.0286503582125.mm,1138.672637841638.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-28.470192475461772.mm, -9.078725279430614.mm, 15.754233621016283.mm)
  circle = ge.add_circle([2422.2035767103853.mm,676.648374751246.mm,1155.1104997222142.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-14.076559043594898.mm, -26.777010230679707.mm, 15.033735326691612.mm)
  circle = ge.add_circle([2393.7333842349235.mm,667.5696494718154.mm,1170.8647333432305.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(8.618863017559761.mm, -29.1704921106832.mm, 14.695869473422135.mm)
  circle = ge.add_circle([2379.6568251913286.mm,640.7926392411357.mm,1185.898468669922.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(26.401905375551905.mm, -14.865591528064101.mm, 14.937354864094914.mm)
  circle = ge.add_circle([2388.2756882088884.mm,611.6221471304525.mm,1200.5943381433442.mm], vec, 7.mm, 6)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(4.322406415559726.mm, 38.94344439761153.mm, 1.1683069925607015.mm)
  circle = ge.add_circle([2414.6775935844403.mm,596.7565556023884.mm,1215.5316930074391.mm], vec, 7.mm, 8)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Spray-bar supply hose (selector -> spray bar, coiled)
  grp = ents.add_group
  grp.name = "Spray-bar supply hose (selector -> spray bar, coiled)"
  ge = grp.entities
  vec = Geom::Vector3d.new(1.mm, -2.699999999999932.mm, 86.30000000000018.mm)
  circle = ge.add_circle([2419.mm,635.6999999999999.mm,1216.6999999999998.mm], vec, 7.mm, 10)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
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
  mat = model.materials["3W-BV-05 (spray selector) handle stem"] || model.materials.add("3W-BV-05 (spray selector) handle stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # BV-04 (chem tap isolation) handle
  grp = ents.add_group
  grp.name = "BV-04 (chem tap isolation) handle"
  face = grp.entities.add_face([1123.mm,115.5.mm,986.mm], [1137.mm,115.5.mm,986.mm], [1137.mm,124.5.mm,986.mm], [1123.mm,124.5.mm,986.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["3W-BV-05 (spray selector) handle stem"] || model.materials.add("3W-BV-05 (spray selector) handle stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "TAP-01 + spray-bar supply"
  inst.layer = model.layers["Supply"]

  # ═══ Wet-end kit (raked) ═══
  defn = model.definitions.add("Wet-end kit (raked)")
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
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
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
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
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

  # Filter F3 PR button
  grp = ents.add_group
  grp.name = "Filter F3 PR button"
  ge = grp.entities
  circle = ge.add_circle([3976.mm,104.mm,2340.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(9.mm)
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 sample valve
  grp = ents.add_group
  grp.name = "SV-01 sample valve"
  face = grp.entities.add_face([4225.mm,85.mm,1575.mm], [4275.mm,85.mm,1575.mm], [4275.mm,135.mm,1575.mm], [4225.mm,135.mm,1575.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(70.mm)
  mat = model.materials["3W-BV-05 (spray selector) body"] || model.materials.add("3W-BV-05 (spray selector) body")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 sample valve spout
  grp = ents.add_group
  grp.name = "SV-01 sample valve spout"
  ge = grp.entities
  circle = ge.add_circle([4250.mm,110.mm,1485.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(90.mm)
  mat = model.materials["3W-BV-05 (spray selector) body"] || model.materials.add("3W-BV-05 (spray selector) body")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 sample valve handwheel stem
  grp = ents.add_group
  grp.name = "SV-01 sample valve handwheel stem"
  ge = grp.entities
  circle = ge.add_circle([4250.mm,110.mm,1645.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["3W-BV-05 (spray selector) handle stem"] || model.materials.add("3W-BV-05 (spray selector) handle stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # SV-01 sample valve handwheel
  grp = ents.add_group
  grp.name = "SV-01 sample valve handwheel"
  ge = grp.entities
  circle = ge.add_circle([4250.mm,110.mm,1661.mm], [0,0,1], 30.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(10.mm)
  mat = model.materials["3W-BV-05 (spray selector) handle stem"] || model.materials.add("3W-BV-05 (spray selector) handle stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-01 body
  grp = ents.add_group
  grp.name = "3W-DV-01 body"
  face = grp.entities.add_face([4777.mm,1218.mm,212.mm], [4823.mm,1218.mm,212.mm], [4823.mm,1264.mm,212.mm], [4777.mm,1264.mm,212.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.mm)
  mat = model.materials["3W-BV-05 (spray selector) body"] || model.materials.add("3W-BV-05 (spray selector) body")
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
  mat = model.materials["3W-BV-05 (spray selector) body"] || model.materials.add("3W-BV-05 (spray selector) body")
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
  mat = model.materials["3W-BV-05 (spray selector) body"] || model.materials.add("3W-BV-05 (spray selector) body")
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
  mat = model.materials["3W-BV-05 (spray selector) body"] || model.materials.add("3W-BV-05 (spray selector) body")
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
  mat = model.materials["3W-BV-05 (spray selector) handle stem"] || model.materials.add("3W-BV-05 (spray selector) handle stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-01 handle lever
  grp = ents.add_group
  grp.name = "3W-DV-01 handle lever"
  face = grp.entities.add_face([4768.mm,1233.mm,299.mm], [4832.mm,1233.mm,299.mm], [4832.mm,1249.mm,299.mm], [4768.mm,1249.mm,299.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["3W-BV-05 (spray selector) handle stem"] || model.materials.add("3W-BV-05 (spray selector) handle stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
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

  # Filter F3 out port
  grp = ents.add_group
  grp.name = "Filter F3 out port"
  ge = grp.entities
  vec = Geom::Vector3d.new(18.360000000000127.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4062.mm,104.mm,2301.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 cap"] || model.materials.add("Filter F1 cap")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F3 out port elbow
  grp = ents.add_group
  grp.name = "Filter F3 out port elbow"
  ge = grp.entities
  arc = ge.add_arc([4080.36.mm,86.36.mm,2301.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,-1.000000], 17.640000000000004.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4080.36.mm,104.mm,2301.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Filter F1 cap"] || model.materials.add("Filter F1 cap")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Filter F3 out port
  grp = ents.add_group
  grp.name = "Filter F3 out port"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -22.36.mm, 0.mm)
  circle = ge.add_circle([4098.mm,86.36.mm,2301.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 cap"] || model.materials.add("Filter F1 cap")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # F3 -> SV-01 (wall-mounted drop)
  grp = ents.add_group
  grp.name = "F3 -> SV-01 (wall-mounted drop)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -14.79.mm, 0.mm)
  circle = ge.add_circle([4098.mm,64.mm,2301.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4112.21.mm,49.21.mm,2301.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.000000,1.000000], 14.21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4098.mm,49.21.mm,2301.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
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
  vec = Geom::Vector3d.new(56.789999999999964.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4112.21.mm,35.mm,2301.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4169.mm,35.mm,2280.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4169.mm,35.mm,2301.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -649.mm)
  circle = ge.add_circle([4190.mm,35.mm,2280.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4190.mm,56.mm,1631.mm], [0.000000,-1.000000,0.000000], [1.000000,-0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4190.mm,35.mm,1631.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 33.mm, 0.mm)
  circle = ge.add_circle([4190.mm,56.mm,1610.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4211.mm,89.mm,1610.mm], [-1.000000,0.000000,0.000000], [0.000000,0.000000,-1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4190.mm,89.mm,1610.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
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
  vec = Geom::Vector3d.new(64.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4211.mm,110.mm,1610.mm], vec, 10.5.mm, 16)
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
  vec = Geom::Vector3d.new(182.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4275.mm,110.mm,1610.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4457.mm,89.mm,1610.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,-1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4457.mm,110.mm,1610.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, -14.790000000000006.mm, 0.mm)
  circle = ge.add_circle([4478.mm,89.mm,1610.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4478.mm,74.21.mm,1595.79.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 14.21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4478.mm,74.21.mm,1610.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1470.29.mm)
  circle = ge.add_circle([4478.mm,60.mm,1595.79.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([4478.mm,81.mm,125.5.mm], [0.000000,-1.000000,0.000000], [1.000000,-0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4478.mm,60.mm,125.5.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
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
  vec = Geom::Vector3d.new(0.mm, 898.mm, 0.mm)
  circle = ge.add_circle([4478.mm,81.mm,104.5.mm], vec, 10.5.mm, 16)
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

  # DV-01 recycle -> IBC-3 (buffer) entry
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(20.399999999999636.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4833.mm,1241.mm,235.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 recycle -> IBC-3 (buffer) entry elbow
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) entry elbow"
  ge = grp.entities
  arc = ge.add_arc([4853.4.mm,1241.mm,254.6.mm], [0.000000,0.000000,-1.000000], [0.000000,-1.000000,0.000000], 19.600000000000005.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4853.4.mm,1241.mm,235.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 recycle -> IBC-3 (buffer) entry
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 854.4.mm)
  circle = ge.add_circle([4873.mm,1241.mm,254.6.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 recycle -> IBC-3 (buffer) entry elbow
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) entry elbow"
  ge = grp.entities
  arc = ge.add_arc([4852.mm,1241.mm,1109.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4873.mm,1241.mm,1109.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 recycle -> IBC-3 (buffer) entry
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(-71.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4852.mm,1241.mm,1130.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 recycle -> IBC-3 (buffer) entry elbow
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) entry elbow"
  ge = grp.entities
  arc = ge.add_arc([4781.mm,1220.mm,1130.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4781.mm,1241.mm,1130.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 recycle -> IBC-3 (buffer) entry
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -303.mm, 0.mm)
  circle = ge.add_circle([4760.mm,1220.mm,1130.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 recycle -> IBC-3 (buffer) entry elbow
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) entry elbow"
  ge = grp.entities
  arc = ge.add_arc([4760.mm,917.mm,1109.mm], [0.000000,0.000000,1.000000], [1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4760.mm,917.mm,1130.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 recycle -> IBC-3 (buffer) entry
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) entry"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -29.mm)
  circle = ge.add_circle([4760.mm,896.mm,1109.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 recycle -> IBC-3 (buffer) flange
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) flange"
  ge = grp.entities
  circle = ge.add_circle([4760.mm,1054.mm,1130.mm], [0,1,0], 36.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(16.mm)
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 recycle -> IBC-3 (buffer) flex jumper
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([4760.mm,1064.mm,1130.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 recycle -> IBC-3 (buffer) flex jumper
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([4760.mm,1071.5.mm,1130.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 recycle -> IBC-3 (buffer) flex jumper
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([4760.mm,1079.mm,1130.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 recycle -> IBC-3 (buffer) flex jumper
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([4760.mm,1086.5.mm,1130.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 recycle -> IBC-3 (buffer) flex jumper
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([4760.mm,1094.mm,1130.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 recycle -> IBC-3 (buffer) flex jumper
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([4760.mm,1101.5.mm,1130.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 recycle -> IBC-3 (buffer) flex jumper
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([4760.mm,1109.mm,1130.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 recycle -> IBC-3 (buffer) flex jumper
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([4760.mm,1116.5.mm,1130.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 recycle -> IBC-3 (buffer) flex jumper
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([4760.mm,1124.mm,1130.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 recycle -> IBC-3 (buffer) flex jumper
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([4760.mm,1131.5.mm,1130.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 recycle -> IBC-3 (buffer) flex jumper
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([4760.mm,1139.mm,1130.mm], vec, 10.5.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # DV-01 recycle -> IBC-3 (buffer) flex jumper
  grp = ents.add_group
  grp.name = "DV-01 recycle -> IBC-3 (buffer) flex jumper"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.5.mm, 0.mm)
  circle = ge.add_circle([4760.mm,1146.5.mm,1130.mm], vec, 8.4.mm, 14)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  inst.name = "Wet-end kit (raked)"
  inst.layer = model.layers["Kit"]

  # ═══ Skid row (P-04 · SV-02 · DV-02) ═══
  defn = model.definitions.add("Skid row (P-04 · SV-02 · DV-02)")
  ents = defn.entities
  # Pump P-04 (Tray drain) body
  grp = ents.add_group
  grp.name = "Pump P-04 (Tray drain) body"
  ge = grp.entities
  circle = ge.add_circle([3300.mm,104.mm,1150.mm], [0,0,1], 50.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(180.mm)
  mat = model.materials["Pump P-04 (Tray drain) body"] || model.materials.add("Pump P-04 (Tray drain) body")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-04 (Tray drain) head
  grp = ents.add_group
  grp.name = "Pump P-04 (Tray drain) head"
  ge = grp.entities
  circle = ge.add_circle([3300.mm,104.mm,1330.mm], [0,0,1], 53.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(30.mm)
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-04 (Tray drain) in port
  grp = ents.add_group
  grp.name = "Pump P-04 (Tray drain) in port"
  ge = grp.entities
  circle = ge.add_circle([3220.mm,104.mm,1312.mm], [1,0,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(30.mm)
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-04 (Tray drain) out port
  grp = ents.add_group
  grp.name = "Pump P-04 (Tray drain) out port"
  ge = grp.entities
  circle = ge.add_circle([3350.mm,104.mm,1312.mm], [1,0,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(30.mm)
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # SV-02 sample valve
  grp = ents.add_group
  grp.name = "SV-02 sample valve"
  face = grp.entities.add_face([3613.mm,79.mm,1282.mm], [3663.mm,79.mm,1282.mm], [3663.mm,129.mm,1282.mm], [3613.mm,129.mm,1282.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["3W-BV-05 (spray selector) body"] || model.materials.add("3W-BV-05 (spray selector) body")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # SV-02 sample valve spout
  grp = ents.add_group
  grp.name = "SV-02 sample valve spout"
  ge = grp.entities
  circle = ge.add_circle([3638.mm,104.mm,1192.mm], [0,0,1], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(90.mm)
  mat = model.materials["3W-BV-05 (spray selector) body"] || model.materials.add("3W-BV-05 (spray selector) body")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # SV-02 sample valve handwheel stem
  grp = ents.add_group
  grp.name = "SV-02 sample valve handwheel stem"
  ge = grp.entities
  circle = ge.add_circle([3638.mm,104.mm,1342.mm], [0,0,1], 5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(16.mm)
  mat = model.materials["3W-BV-05 (spray selector) handle stem"] || model.materials.add("3W-BV-05 (spray selector) handle stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # SV-02 sample valve handwheel
  grp = ents.add_group
  grp.name = "SV-02 sample valve handwheel"
  ge = grp.entities
  circle = ge.add_circle([3638.mm,104.mm,1358.mm], [0,0,1], 30.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(10.mm)
  mat = model.materials["3W-BV-05 (spray selector) handle stem"] || model.materials.add("3W-BV-05 (spray selector) handle stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-02 body
  grp = ents.add_group
  grp.name = "3W-DV-02 body"
  face = grp.entities.add_face([3953.mm,81.mm,1289.mm], [3999.mm,81.mm,1289.mm], [3999.mm,127.mm,1289.mm], [3953.mm,127.mm,1289.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(46.mm)
  mat = model.materials["3W-BV-05 (spray selector) body"] || model.materials.add("3W-BV-05 (spray selector) body")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-02 run +
  grp = ents.add_group
  grp.name = "3W-DV-02 run +"
  ge = grp.entities
  circle = ge.add_circle([3999.mm,104.mm,1312.mm], [1,0,0], 13.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["3W-BV-05 (spray selector) body"] || model.materials.add("3W-BV-05 (spray selector) body")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-02 run -
  grp = ents.add_group
  grp.name = "3W-DV-02 run -"
  ge = grp.entities
  circle = ge.add_circle([3943.mm,104.mm,1312.mm], [1,0,0], 13.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(10.mm)
  mat = model.materials["3W-BV-05 (spray selector) body"] || model.materials.add("3W-BV-05 (spray selector) body")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-02 branch
  grp = ents.add_group
  grp.name = "3W-DV-02 branch"
  ge = grp.entities
  circle = ge.add_circle([3976.mm,104.mm,1335.mm], [0,0,1], 13.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(10.mm)
  mat = model.materials["3W-BV-05 (spray selector) body"] || model.materials.add("3W-BV-05 (spray selector) body")
  mat.color = Sketchup::Color.new(184, 184, 64)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-02 handle stem
  grp = ents.add_group
  grp.name = "3W-DV-02 handle stem"
  ge = grp.entities
  circle = ge.add_circle([3976.mm,127.mm,1312.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(42.mm)
  mat = model.materials["3W-BV-05 (spray selector) handle stem"] || model.materials.add("3W-BV-05 (spray selector) handle stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # 3W-DV-02 handle lever
  grp = ents.add_group
  grp.name = "3W-DV-02 handle lever"
  face = grp.entities.add_face([3944.mm,167.mm,1305.mm], [4008.mm,167.mm,1305.mm], [4008.mm,183.mm,1305.mm], [3944.mm,183.mm,1305.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(14.mm)
  mat = model.materials["3W-BV-05 (spray selector) handle stem"] || model.materials.add("3W-BV-05 (spray selector) handle stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # ACC-02 Accumulator
  grp = ents.add_group
  grp.name = "ACC-02 Accumulator"
  ge = grp.entities
  circle = ge.add_circle([3857.mm,104.mm,920.mm], [0,0,1], 63.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(174.mm)
  mat = model.materials["ACC-02 Accumulator"] || model.materials.add("ACC-02 Accumulator")
  mat.color = Sketchup::Color.new(90, 154, 204)
  mat.alpha = 1.0
  grp.material = mat

  # ACC-02 head
  grp = ents.add_group
  grp.name = "ACC-02 head"
  ge = grp.entities
  circle = ge.add_circle([3857.mm,104.mm,1094.mm], [0,0,1], 65.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(26.mm)
  mat = model.materials["Filter F1 cap"] || model.materials.add("Filter F1 cap")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # ACC-02 in port
  grp = ents.add_group
  grp.name = "ACC-02 in port"
  ge = grp.entities
  circle = ge.add_circle([3920.5.mm,104.mm,948.mm], [1,0,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(30.mm)
  mat = model.materials["Filter F1 cap"] || model.materials.add("Filter F1 cap")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # ACC-02 out port
  grp = ents.add_group
  grp.name = "ACC-02 out port"
  ge = grp.entities
  circle = ge.add_circle([3763.5.mm,104.mm,948.mm], [1,0,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(30.mm)
  mat = model.materials["Filter F1 cap"] || model.materials.add("Filter F1 cap")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Skid row (P-04 · SV-02 · DV-02)"
  inst.layer = model.layers["Kit"]

  # ═══ Skid plumbing ═══
  defn = model.definitions.add("Skid plumbing")
  ents = defn.entities
  # Tray sump -> P-04 suction
  grp = ents.add_group
  grp.name = "Tray sump -> P-04 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1288.mm)
  circle = ge.add_circle([2386.mm,104.mm,3.mm], vec, 10.5.mm, 16)
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
  arc = ge.add_arc([2407.mm,104.mm,1291.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2386.mm,104.mm,1291.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
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
  vec = Geom::Vector3d.new(813.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2407.mm,104.mm,1312.mm], vec, 10.5.mm, 16)
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
  circle = ge.add_circle([2386.mm,104.mm,3.mm], [0,0,1], 14.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(36.mm)
  mat = model.materials["Filter F1 cap"] || model.materials.add("Filter F1 cap")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # P-04 -> SV-02 -> DV-02
  grp = ents.add_group
  grp.name = "P-04 -> SV-02 -> DV-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(563.mm, 0.mm, 0.mm)
  circle = ge.add_circle([3380.mm,104.mm,1312.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 feed -> F1 (recycle)
  grp = ents.add_group
  grp.name = "DV-02 feed -> F1 (recycle)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 84.mm)
  circle = ge.add_circle([3976.mm,104.mm,1345.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 feed -> F1 (recycle) elbow
  grp = ents.add_group
  grp.name = "DV-02 feed -> F1 (recycle) elbow"
  ge = grp.entities
  arc = ge.add_arc([3955.mm,104.mm,1429.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([3976.mm,104.mm,1429.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 feed -> F1 (recycle)
  grp = ents.add_group
  grp.name = "DV-02 feed -> F1 (recycle)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1104.mm, 0.mm, 0.mm)
  circle = ge.add_circle([3955.mm,104.mm,1450.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 feed -> F1 (recycle) elbow
  grp = ents.add_group
  grp.name = "DV-02 feed -> F1 (recycle) elbow"
  ge = grp.entities
  arc = ge.add_arc([2851.mm,104.mm,1471.mm], [0.000000,0.000000,-1.000000], [0.000000,1.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2851.mm,104.mm,1450.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 feed -> F1 (recycle)
  grp = ents.add_group
  grp.name = "DV-02 feed -> F1 (recycle)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 809.mm)
  circle = ge.add_circle([2830.mm,104.mm,1471.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 feed -> F1 (recycle) elbow
  grp = ents.add_group
  grp.name = "DV-02 feed -> F1 (recycle) elbow"
  ge = grp.entities
  arc = ge.add_arc([2851.mm,104.mm,2280.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2830.mm,104.mm,2280.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 feed -> F1 (recycle)
  grp = ents.add_group
  grp.name = "DV-02 feed -> F1 (recycle)"
  ge = grp.entities
  vec = Geom::Vector3d.new(327.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2851.mm,104.mm,2301.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4"
  ge = grp.entities
  vec = Geom::Vector3d.new(18.360000000000127.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4009.mm,104.mm,1312.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4 elbow
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4 elbow"
  ge = grp.entities
  arc = ge.add_arc([4027.36.mm,104.mm,1294.36.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 17.640000000000004.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4027.36.mm,104.mm,1312.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -223.3599999999999.mm)
  circle = ge.add_circle([4045.mm,104.mm,1294.36.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4 elbow
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4 elbow"
  ge = grp.entities
  arc = ge.add_arc([4045.mm,83.mm,1071.mm], [0.000000,1.000000,0.000000], [-1.000000,-0.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4045.mm,104.mm,1071.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -27.mm, 0.mm)
  circle = ge.add_circle([4045.mm,83.mm,1050.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4 elbow
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4 elbow"
  ge = grp.entities
  arc = ge.add_arc([4066.mm,56.mm,1050.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.000000,1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4045.mm,56.mm,1050.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4"
  ge = grp.entities
  vec = Geom::Vector3d.new(423.3000000000002.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4066.mm,35.mm,1050.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4 elbow
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4 elbow"
  ge = grp.entities
  arc = ge.add_arc([4489.3.mm,49.7.mm,1050.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 14.700000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4489.3.mm,35.mm,1050.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.802999999999997.mm, 0.mm)
  circle = ge.add_circle([4504.mm,49.7.mm,1050.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4 elbow
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4 elbow"
  ge = grp.entities
  arc = ge.add_arc([4504.mm,57.503.mm,1042.503.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 7.496999999999999.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4504.mm,57.503.mm,1050.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -917.0029999999999.mm)
  circle = ge.add_circle([4504.mm,65.mm,1042.503.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4 elbow
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4 elbow"
  ge = grp.entities
  arc = ge.add_arc([4504.mm,86.mm,125.5.mm], [0.000000,-1.000000,0.000000], [1.000000,-0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4504.mm,65.mm,125.5.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 893.mm, 0.mm)
  circle = ge.add_circle([4504.mm,86.mm,104.5.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4 elbow
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4 elbow"
  ge = grp.entities
  arc = ge.add_arc([4504.mm,979.mm,125.5.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4504.mm,979.mm,104.5.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 13.514999999999986.mm)
  circle = ge.add_circle([4504.mm,1000.mm,125.5.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4 elbow
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4 elbow"
  ge = grp.entities
  arc = ge.add_arc([4504.mm,1012.985.mm,139.015.mm], [0.000000,-1.000000,0.000000], [-1.000000,0.000000,0.000000], 12.985000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4504.mm,1000.mm,139.015.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 76.01499999999999.mm, 0.mm)
  circle = ge.add_circle([4504.mm,1012.985.mm,152.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4 elbow
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4 elbow"
  ge = grp.entities
  arc = ge.add_arc([4504.mm,1089.mm,131.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4504.mm,1089.mm,152.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -13.515.mm)
  circle = ge.add_circle([4504.mm,1110.mm,131.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4 elbow
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4 elbow"
  ge = grp.entities
  arc = ge.add_arc([4504.mm,1122.985.mm,117.485.mm], [0.000000,-1.000000,0.000000], [1.000000,-0.000000,0.000000], 12.985000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4504.mm,1110.mm,117.485.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 50.0150000000001.mm, 0.mm)
  circle = ge.add_circle([4504.mm,1122.985.mm,104.5.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4 elbow
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4 elbow"
  ge = grp.entities
  arc = ge.add_arc([4525.mm,1173.mm,104.5.mm], [-1.000000,0.000000,0.000000], [0.000000,0.000000,-1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4504.mm,1173.mm,104.5.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4"
  ge = grp.entities
  vec = Geom::Vector3d.new(96.64500000000044.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4525.mm,1194.mm,104.5.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4 elbow
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4 elbow"
  ge = grp.entities
  arc = ge.add_arc([4621.645.mm,1194.mm,85.145.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 19.355000000000004.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4621.645.mm,1194.mm,104.5.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -10.27395.mm)
  circle = ge.add_circle([4641.mm,1194.mm,85.145.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4 elbow
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4 elbow"
  ge = grp.entities
  arc = ge.add_arc([4650.87105.mm,1194.mm,74.87105.mm], [-1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 9.87105.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4641.mm,1194.mm,74.87105.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4"
  ge = grp.entities
  vec = Geom::Vector3d.new(178.12895000000026.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4650.87105.mm,1194.mm,65.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4 elbow
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4 elbow"
  ge = grp.entities
  arc = ge.add_arc([4829.mm,1194.mm,86.mm], [0.000000,0.000000,-1.000000], [0.000000,-1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4829.mm,1194.mm,65.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 12.239999999999995.mm)
  circle = ge.add_circle([4850.mm,1194.mm,86.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4 elbow
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4 elbow"
  ge = grp.entities
  arc = ge.add_arc([4861.76.mm,1194.mm,98.24.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 11.760000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4850.mm,1194.mm,98.24.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4"
  ge = grp.entities
  vec = Geom::Vector3d.new(47.23999999999978.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4861.76.mm,1194.mm,110.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4 elbow
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4 elbow"
  ge = grp.entities
  arc = ge.add_arc([4909.mm,1194.mm,89.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4909.mm,1194.mm,110.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -12.239999999999995.mm)
  circle = ge.add_circle([4930.mm,1194.mm,89.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4 elbow
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4 elbow"
  ge = grp.entities
  arc = ge.add_arc([4941.76.mm,1194.mm,76.76.mm], [-1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 11.760000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4930.mm,1194.mm,76.76.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4"
  ge = grp.entities
  vec = Geom::Vector3d.new(346.75.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4941.76.mm,1194.mm,65.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4 elbow
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4 elbow"
  ge = grp.entities
  arc = ge.add_arc([5288.51.mm,1194.49.mm,65.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 0.49000000000000005.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5288.51.mm,1194.mm,65.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4 elbow
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4 elbow"
  ge = grp.entities
  arc = ge.add_arc([5289.mm,1194.7501.mm,65.2499.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 0.24989999999999557.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5289.mm,1194.7501.mm,65.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1143.7501.mm)
  circle = ge.add_circle([5289.mm,1195.mm,65.2499.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4 elbow
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4 elbow"
  ge = grp.entities
  arc = ge.add_arc([5310.mm,1195.mm,1209.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5289.mm,1195.mm,1209.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["DV-01 -> IBC-4 merge"] || model.materials.add("DV-01 -> IBC-4 merge")
  mat.color = Sketchup::Color.new(119, 119, 119)
  mat.alpha = 1.0
  grp.material = mat

  # DV-02 waste -> IBC-4
  grp = ents.add_group
  grp.name = "DV-02 waste -> IBC-4"
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

  # P-02 -> ACC-02 (recycle spray)
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 15.299999999999955.mm, 0.mm)
  circle = ge.add_circle([4984.mm,1261.mm,1102.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray) elbow
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray) elbow"
  ge = grp.entities
  arc = ge.add_arc([4969.3.mm,1276.3.mm,1102.mm], [1.000000,0.000000,0.000000], [0.000000,-0.000000,1.000000], 14.700000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4984.mm,1276.3.mm,1102.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray)
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-48.30000000000018.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4969.3.mm,1291.mm,1102.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray) elbow
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray) elbow"
  ge = grp.entities
  arc = ge.add_arc([4921.mm,1291.mm,1081.mm], [0.000000,0.000000,1.000000], [-0.000000,-1.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4921.mm,1291.mm,1102.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray)
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -995.mm)
  circle = ge.add_circle([4900.mm,1291.mm,1081.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray) elbow
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray) elbow"
  ge = grp.entities
  arc = ge.add_arc([4900.mm,1270.mm,86.mm], [0.000000,1.000000,0.000000], [-1.000000,-0.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4900.mm,1291.mm,86.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray)
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -68.mm, 0.mm)
  circle = ge.add_circle([4900.mm,1270.mm,65.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray) elbow
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray) elbow"
  ge = grp.entities
  arc = ge.add_arc([4879.mm,1202.mm,65.mm], [1.000000,0.000000,0.000000], [-0.000000,-0.000000,-1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4900.mm,1202.mm,65.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray)
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-228.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4879.mm,1181.mm,65.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray) elbow
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray) elbow"
  ge = grp.entities
  arc = ge.add_arc([4651.mm,1160.mm,65.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4651.mm,1181.mm,65.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray)
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -44.6099999999999.mm, 0.mm)
  circle = ge.add_circle([4630.mm,1160.mm,65.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray) elbow
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray) elbow"
  ge = grp.entities
  arc = ge.add_arc([4635.39.mm,1115.39.mm,65.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.000000,1.000000], 5.390000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4630.mm,1115.39.mm,65.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray)
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray)"
  ge = grp.entities
  vec = Geom::Vector3d.new(2.8611000000000786.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4635.39.mm,1110.mm,65.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray) elbow
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray) elbow"
  ge = grp.entities
  arc = ge.add_arc([4638.2511.mm,1110.mm,67.74889999999984.mm], [0.000000,0.000000,-1.000000], [0.000000,-1.000000,0.000000], 2.74889999999984.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4638.2511.mm,1110.mm,65.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray)
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 18.743061000000083.mm)
  circle = ge.add_circle([4641.mm,1110.mm,67.74889999999984.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray) elbow
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray) elbow"
  ge = grp.entities
  arc = ge.add_arc([4622.991961.mm,1110.mm,86.49196099999992.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 18.008039000000085.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4641.mm,1110.mm,86.49196099999992.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray)
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-45.99196099999972.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4622.991961.mm,1110.mm,104.5.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray) elbow
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray) elbow"
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

  # P-02 -> ACC-02 (recycle spray)
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray)"
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

  # P-02 -> ACC-02 (recycle spray) elbow
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray) elbow"
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

  # P-02 -> ACC-02 (recycle spray)
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray)"
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

  # P-02 -> ACC-02 (recycle spray) elbow
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray) elbow"
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

  # P-02 -> ACC-02 (recycle spray)
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray)"
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

  # P-02 -> ACC-02 (recycle spray) elbow
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray) elbow"
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

  # P-02 -> ACC-02 (recycle spray)
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -901.015.mm, 0.mm)
  circle = ge.add_circle([4556.mm,987.015.mm,104.5.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray) elbow
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray) elbow"
  ge = grp.entities
  arc = ge.add_arc([4556.mm,86.mm,125.5.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4556.mm,86.mm,104.5.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray)
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 807.8.mm)
  circle = ge.add_circle([4556.mm,65.mm,125.5.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray) elbow
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray) elbow"
  ge = grp.entities
  arc = ge.add_arc([4556.mm,50.3.mm,933.3.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 14.700000000000001.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4556.mm,65.mm,933.3.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray)
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.802999999999997.mm, 0.mm)
  circle = ge.add_circle([4556.mm,50.3.mm,948.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray) elbow
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray) elbow"
  ge = grp.entities
  arc = ge.add_arc([4548.503.mm,42.497.mm,948.mm], [1.000000,0.000000,0.000000], [-0.000000,-0.000000,-1.000000], 7.496999999999999.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4556.mm,42.497.mm,948.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray)
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-522.0029999999997.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4548.503.mm,35.mm,948.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray) elbow
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray) elbow"
  ge = grp.entities
  arc = ge.add_arc([4026.5.mm,56.mm,948.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,-1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4026.5.mm,35.mm,948.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray)
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 27.mm, 0.mm)
  circle = ge.add_circle([4005.5.mm,56.mm,948.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray) elbow
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray) elbow"
  ge = grp.entities
  arc = ge.add_arc([3984.5.mm,83.mm,948.mm], [1.000000,0.000000,0.000000], [0.000000,-0.000000,1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4005.5.mm,83.mm,948.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # P-02 -> ACC-02 (recycle spray)
  grp = ents.add_group
  grp.name = "P-02 -> ACC-02 (recycle spray)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-34.mm, 0.mm, 0.mm)
  circle = ge.add_circle([3984.5.mm,104.mm,948.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # ACC-02 -> BV-05 (recycled spray)
  grp = ents.add_group
  grp.name = "ACC-02 -> BV-05 (recycled spray)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-34.mm, 0.mm, 0.mm)
  circle = ge.add_circle([3763.5.mm,104.mm,948.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # ACC-02 -> BV-05 (recycled spray) elbow
  grp = ents.add_group
  grp.name = "ACC-02 -> BV-05 (recycled spray) elbow"
  ge = grp.entities
  arc = ge.add_arc([3729.5.mm,83.mm,948.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([3729.5.mm,104.mm,948.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # ACC-02 -> BV-05 (recycled spray)
  grp = ents.add_group
  grp.name = "ACC-02 -> BV-05 (recycled spray)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -27.mm, 0.mm)
  circle = ge.add_circle([3708.5.mm,83.mm,948.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # ACC-02 -> BV-05 (recycled spray) elbow
  grp = ents.add_group
  grp.name = "ACC-02 -> BV-05 (recycled spray) elbow"
  ge = grp.entities
  arc = ge.add_arc([3687.5.mm,56.mm,948.mm], [1.000000,0.000000,0.000000], [-0.000000,-0.000000,-1.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([3708.5.mm,56.mm,948.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # ACC-02 -> BV-05 (recycled spray)
  grp = ents.add_group
  grp.name = "ACC-02 -> BV-05 (recycled spray)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-1344.5.mm, 0.mm, 0.mm)
  circle = ge.add_circle([3687.5.mm,35.mm,948.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # ACC-02 -> BV-05 (recycled spray) elbow
  grp = ents.add_group
  grp.name = "ACC-02 -> BV-05 (recycled spray) elbow"
  ge = grp.entities
  arc = ge.add_arc([2343.mm,35.mm,927.mm], [0.000000,0.000000,1.000000], [-0.000000,-1.000000,-0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2343.mm,35.mm,948.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # ACC-02 -> BV-05 (recycled spray)
  grp = ents.add_group
  grp.name = "ACC-02 -> BV-05 (recycled spray)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -210.34000000000003.mm)
  circle = ge.add_circle([2322.mm,35.mm,927.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # ACC-02 -> BV-05 (recycled spray) elbow
  grp = ents.add_group
  grp.name = "ACC-02 -> BV-05 (recycled spray) elbow"
  ge = grp.entities
  arc = ge.add_arc([2322.mm,51.660000000000004.mm,716.66.mm], [0.000000,-1.000000,0.000000], [1.000000,-0.000000,0.000000], 16.660000000000004.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2322.mm,35.mm,716.66.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # ACC-02 -> BV-05 (recycled spray)
  grp = ents.add_group
  grp.name = "ACC-02 -> BV-05 (recycled spray)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 8.843400000000003.mm, 0.mm)
  circle = ge.add_circle([2322.mm,51.66.mm,700.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # ACC-02 -> BV-05 (recycled spray) elbow
  grp = ents.add_group
  grp.name = "ACC-02 -> BV-05 (recycled spray) elbow"
  ge = grp.entities
  arc = ge.add_arc([2313.5034.mm,60.5034.mm,700.mm], [1.000000,0.000000,0.000000], [0.000000,-0.000000,1.000000], 8.496600000000003.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2322.mm,60.5034.mm,700.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # ACC-02 -> BV-05 (recycled spray)
  grp = ents.add_group
  grp.name = "ACC-02 -> BV-05 (recycled spray)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-31.503400000000056.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2313.5034.mm,69.mm,700.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Skid plumbing"
  inst.layer = model.layers["Kit"]

  # ═══ Person (scale) ═══
  defn = model.definitions.add("Person (scale)")
  ents = defn.entities
  # Person legs
  grp = ents.add_group
  grp.name = "Person legs"
  face = grp.entities.add_face([2950.mm,120.mm,140.mm], [3150.mm,120.mm,140.mm], [3150.mm,280.mm,140.mm], [2950.mm,280.mm,140.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(850.mm)
  mat = model.materials["Person legs"] || model.materials.add("Person legs")
  mat.color = Sketchup::Color.new(128, 96, 64)
  mat.alpha = 0.28
  grp.material = mat

  # Person torso
  grp = ents.add_group
  grp.name = "Person torso"
  face = grp.entities.add_face([2960.mm,50.mm,990.mm], [3140.mm,50.mm,990.mm], [3140.mm,350.mm,990.mm], [2960.mm,350.mm,990.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(600.mm)
  mat = model.materials["Person legs"] || model.materials.add("Person legs")
  mat.color = Sketchup::Color.new(128, 96, 64)
  mat.alpha = 0.28
  grp.material = mat

  # Person head (scale 1.75m)
  grp = ents.add_group
  grp.name = "Person head (scale 1.75m)"
  ge = grp.entities
  circle = ge.add_circle([3050.mm,200.mm,1590.mm], [0,0,1], 100.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(230.mm)
  mat = model.materials["Person head (scale 1.75m)"] || model.materials.add("Person head (scale 1.75m)")
  mat.color = Sketchup::Color.new(128, 96, 64)
  mat.alpha = 0.32
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Person (scale)"
  inst.layer = model.layers["Scale"]

  # ═══ Other pinhole-wall equipment ═══
  defn = model.definitions.add("Other pinhole-wall equipment")
  ents = defn.entities
  # EP plywood backing panel (18mm)
  grp = ents.add_group
  grp.name = "EP plywood backing panel (18mm)"
  face = grp.entities.add_face([1817.mm,-18.mm,148.mm], [2181.mm,-18.mm,148.mm], [2181.mm,0.mm,148.mm], [1817.mm,0.mm,148.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1424.mm)
  mat = model.materials["Wall backing (18mm ply)"] || model.materials.add("Wall backing (18mm ply)")
  mat.color = Sketchup::Color.new(178, 167, 154)
  mat.alpha = 0.18
  grp.material = mat

  # Plywood side lip (left, 18mm)
  grp = ents.add_group
  grp.name = "Plywood side lip (left, 18mm)"
  face = grp.entities.add_face([1817.mm,0.mm,148.mm], [1835.mm,0.mm,148.mm], [1835.mm,100.mm,148.mm], [1817.mm,100.mm,148.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1424.mm)
  mat = model.materials["Wall backing (18mm ply)"] || model.materials.add("Wall backing (18mm ply)")
  mat.color = Sketchup::Color.new(178, 167, 154)
  mat.alpha = 0.18
  grp.material = mat

  # Plywood side lip (right, 18mm)
  grp = ents.add_group
  grp.name = "Plywood side lip (right, 18mm)"
  face = grp.entities.add_face([2163.mm,0.mm,148.mm], [2181.mm,0.mm,148.mm], [2181.mm,100.mm,148.mm], [2163.mm,100.mm,148.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1424.mm)
  mat = model.materials["Wall backing (18mm ply)"] || model.materials.add("Wall backing (18mm ply)")
  mat.color = Sketchup::Color.new(178, 167, 154)
  mat.alpha = 0.18
  grp.material = mat

  # IP65 enclosure (ghosted, fuse block + busbars)
  grp = ents.add_group
  grp.name = "IP65 enclosure (ghosted, fuse block + busbars)"
  face = grp.entities.add_face([1834.mm,12.mm,1150.mm], [2034.mm,12.mm,1150.mm], [2034.mm,152.mm,1150.mm], [1834.mm,152.mm,1150.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(220.mm)
  mat = model.materials["IP65 enclosure (ghosted, fuse block + busbars)"] || model.materials.add("IP65 enclosure (ghosted, fuse block + busbars)")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.12
  grp.material = mat

  # MPPT Controller (100/50)
  grp = ents.add_group
  grp.name = "MPPT Controller (100/50)"
  face = grp.entities.add_face([1844.mm,120.mm,1460.mm], [2029.mm,120.mm,1460.mm], [2029.mm,190.mm,1460.mm], [1844.mm,190.mm,1460.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["MPPT Controller (100/50)"] || model.materials.add("MPPT Controller (100/50)")
  mat.color = Sketchup::Color.new(144, 155, 183)
  mat.alpha = 0.18
  grp.material = mat

  # MPPT backing panel (18mm ply)
  grp = ents.add_group
  grp.name = "MPPT backing panel (18mm ply)"
  face = grp.entities.add_face([1837.mm,102.mm,1430.mm], [2042.mm,102.mm,1430.mm], [2042.mm,120.mm,1430.mm], [1837.mm,120.mm,1430.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(130.mm)
  mat = model.materials["Wall backing (18mm ply)"] || model.materials.add("Wall backing (18mm ply)")
  mat.color = Sketchup::Color.new(178, 167, 154)
  mat.alpha = 0.18
  grp.material = mat

  # MPPT sub-panel gusset (ply)
  grp = ents.add_group
  grp.name = "MPPT sub-panel gusset (ply)"
  face = grp.entities.add_face([1837.mm,0.mm,1430.mm], [1855.mm,0.mm,1430.mm], [1855.mm,120.mm,1430.mm], [1837.mm,120.mm,1430.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(130.mm)
  mat = model.materials["Wall backing (18mm ply)"] || model.materials.add("Wall backing (18mm ply)")
  mat.color = Sketchup::Color.new(178, 167, 154)
  mat.alpha = 0.18
  grp.material = mat

  # MPPT sub-panel gusset (ply)
  grp = ents.add_group
  grp.name = "MPPT sub-panel gusset (ply)"
  face = grp.entities.add_face([2024.mm,0.mm,1430.mm], [2042.mm,0.mm,1430.mm], [2042.mm,120.mm,1430.mm], [2024.mm,120.mm,1430.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(130.mm)
  mat = model.materials["Wall backing (18mm ply)"] || model.materials.add("Wall backing (18mm ply)")
  mat.color = Sketchup::Color.new(178, 167, 154)
  mat.alpha = 0.18
  grp.material = mat

  # Fuse Block base (Blue Sea 5026)
  grp = ents.add_group
  grp.name = "Fuse Block base (Blue Sea 5026)"
  face = grp.entities.add_face([1844.mm,25.mm,1190.mm], [2008.mm,25.mm,1190.mm], [2008.mm,64.mm,1190.mm], [1844.mm,64.mm,1190.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(28.mm)
  mat = model.materials["Fuse Block base (Blue Sea 5026)"] || model.materials.add("Fuse Block base (Blue Sea 5026)")
  mat.color = Sketchup::Color.new(138, 138, 141)
  mat.alpha = 0.18
  grp.material = mat

  # Fuse A (5A — exhaust fan)
  grp = ents.add_group
  grp.name = "Fuse A (5A — exhaust fan)"
  face = grp.entities.add_face([1849.2142857142858.mm,40.mm,1218.mm], [1862.2142857142858.mm,40.mm,1218.mm], [1862.2142857142858.mm,49.mm,1218.mm], [1849.2142857142858.mm,49.mm,1218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
  mat.color = Sketchup::Color.new(191, 143, 142)
  mat.alpha = 0.18
  grp.material = mat

  # Fuse B (5A — intake fan)
  grp = ents.add_group
  grp.name = "Fuse B (5A — intake fan)"
  face = grp.entities.add_face([1872.642857142857.mm,40.mm,1218.mm], [1885.642857142857.mm,40.mm,1218.mm], [1885.642857142857.mm,49.mm,1218.mm], [1872.642857142857.mm,49.mm,1218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse B (5A — intake fan)"] || model.materials.add("Fuse B (5A — intake fan)")
  mat.color = Sketchup::Color.new(204, 168, 139)
  mat.alpha = 0.18
  grp.material = mat

  # Fuse C (15A — water pumps)
  grp = ents.add_group
  grp.name = "Fuse C (15A — water pumps)"
  face = grp.entities.add_face([1896.0714285714287.mm,40.mm,1218.mm], [1909.0714285714287.mm,40.mm,1218.mm], [1909.0714285714287.mm,49.mm,1218.mm], [1896.0714285714287.mm,49.mm,1218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse C (15A — water pumps)"] || model.materials.add("Fuse C (15A — water pumps)")
  mat.color = Sketchup::Color.new(138, 166, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Fuse D (5A — safelight)
  grp = ents.add_group
  grp.name = "Fuse D (5A — safelight)"
  face = grp.entities.add_face([1919.5.mm,40.mm,1218.mm], [1932.5.mm,40.mm,1218.mm], [1932.5.mm,49.mm,1218.mm], [1919.5.mm,49.mm,1218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse D (5A — safelight)"] || model.materials.add("Fuse D (5A — safelight)")
  mat.color = Sketchup::Color.new(173, 147, 187)
  mat.alpha = 0.18
  grp.material = mat

  # Fuse E (40A — cooler / inverter)
  grp = ents.add_group
  grp.name = "Fuse E (40A — cooler / inverter)"
  face = grp.entities.add_face([1942.9285714285713.mm,40.mm,1218.mm], [1955.9285714285713.mm,40.mm,1218.mm], [1955.9285714285713.mm,49.mm,1218.mm], [1942.9285714285713.mm,49.mm,1218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse E (40A — cooler / inverter)"] || model.materials.add("Fuse E (40A — cooler / inverter)")
  mat.color = Sketchup::Color.new(131, 180, 173)
  mat.alpha = 0.18
  grp.material = mat

  # Fuse F (20A — actuators (spare))
  grp = ents.add_group
  grp.name = "Fuse F (20A — actuators (spare))"
  face = grp.entities.add_face([1966.357142857143.mm,40.mm,1218.mm], [1979.357142857143.mm,40.mm,1218.mm], [1979.357142857143.mm,49.mm,1218.mm], [1966.357142857143.mm,49.mm,1218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse F (20A — actuators (spare))"] || model.materials.add("Fuse F (20A — actuators (spare))")
  mat.color = Sketchup::Color.new(168, 172, 176)
  mat.alpha = 0.18
  grp.material = mat

  # Fuse G (10A — white LED)
  grp = ents.add_group
  grp.name = "Fuse G (10A — white LED)"
  face = grp.entities.add_face([1989.7857142857142.mm,40.mm,1218.mm], [2002.7857142857142.mm,40.mm,1218.mm], [2002.7857142857142.mm,49.mm,1218.mm], [1989.7857142857142.mm,49.mm,1218.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(42.mm)
  mat = model.materials["Fuse G (10A — white LED)"] || model.materials.add("Fuse G (10A — white LED)")
  mat.color = Sketchup::Color.new(208, 192, 132)
  mat.alpha = 0.18
  grp.material = mat

  # Master pump switch (Cct C, on EP)
  grp = ents.add_group
  grp.name = "Master pump switch (Cct C, on EP)"
  face = grp.entities.add_face([1934.mm,0.mm,1045.mm], [1984.mm,0.mm,1045.mm], [1984.mm,46.mm,1045.mm], [1934.mm,46.mm,1045.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(84.mm)
  mat = model.materials["Master pump switch (Cct C, on EP)"] || model.materials.add("Master pump switch (Cct C, on EP)")
  mat.color = Sketchup::Color.new(133, 133, 136)
  mat.alpha = 0.18
  grp.material = mat

  # Master switch lever (OFF cutoff)
  grp = ents.add_group
  grp.name = "Master switch lever (OFF cutoff)"
  face = grp.entities.add_face([1951.mm,46.mm,1085.mm], [1967.mm,46.mm,1085.mm], [1967.mm,80.mm,1085.mm], [1951.mm,80.mm,1085.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(16.mm)
  mat = model.materials["Master switch lever (OFF cutoff)"] || model.materials.add("Master switch lever (OFF cutoff)")
  mat.color = Sketchup::Color.new(191, 135, 141)
  mat.alpha = 0.18
  grp.material = mat

  # Busbar (+)
  grp = ents.add_group
  grp.name = "Busbar (+)"
  face = grp.entities.add_face([1844.mm,30.mm,1320.mm], [1964.mm,30.mm,1320.mm], [1964.mm,50.mm,1320.mm], [1844.mm,50.mm,1320.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Fuse A (5A — exhaust fan)"] || model.materials.add("Fuse A (5A — exhaust fan)")
  mat.color = Sketchup::Color.new(191, 143, 142)
  mat.alpha = 0.18
  grp.material = mat

  # Busbar (-)
  grp = ents.add_group
  grp.name = "Busbar (-)"
  face = grp.entities.add_face([1844.mm,30.mm,1290.mm], [1964.mm,30.mm,1290.mm], [1964.mm,50.mm,1290.mm], [1844.mm,50.mm,1290.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(22.mm)
  mat = model.materials["Fuse Block base (Blue Sea 5026)"] || model.materials.add("Fuse Block base (Blue Sea 5026)")
  mat.color = Sketchup::Color.new(138, 138, 141)
  mat.alpha = 0.18
  grp.material = mat

  # Main Disconnect (m-Series)
  grp = ents.add_group
  grp.name = "Main Disconnect (m-Series)"
  ge = grp.entities
  circle = ge.add_circle([1884.mm,0.mm,1045.mm], [0,1,0], 35.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(60.mm)
  mat = model.materials["Main Disconnect (m-Series)"] || model.materials.add("Main Disconnect (m-Series)")
  mat.color = Sketchup::Color.new(198, 144, 143)
  mat.alpha = 0.18
  grp.material = mat

  # Main feed (disconnect → busbar +)
  grp = ents.add_group
  grp.name = "Main feed (disconnect → busbar +)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 7.649999999999999.mm, 0.mm)
  circle = ge.add_circle([1884.mm,30.mm,1135.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Main feed (disconnect → busbar +) elbow
  grp = ents.add_group
  grp.name = "Main feed (disconnect → busbar +) elbow"
  ge = grp.entities
  arc = ge.add_arc([1884.mm,37.65.mm,1142.35.mm], [0.000000,0.000000,-1.000000], [1.000000,0.000000,0.000000], 7.3500000000000005.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1884.mm,37.65.mm,1135.mm], [0.000000,1.000000,0.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Main feed (disconnect → busbar +)
  grp = ents.add_group
  grp.name = "Main feed (disconnect → busbar +)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 158.05000000000018.mm)
  circle = ge.add_circle([1884.mm,45.mm,1142.35.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Main feed (disconnect → busbar +) elbow
  grp = ents.add_group
  grp.name = "Main feed (disconnect → busbar +) elbow"
  ge = grp.entities
  arc = ge.add_arc([1864.4.mm,45.mm,1300.4.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 19.600000000000005.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1884.mm,45.mm,1300.4.mm], [0.000000,0.000000,1.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Main feed (disconnect → busbar +)
  grp = ents.add_group
  grp.name = "Main feed (disconnect → busbar +)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-20.40000000000009.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1864.4.mm,45.mm,1320.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Charge-line Fuse (60A, MPPT -> battery)
  grp = ents.add_group
  grp.name = "Charge-line Fuse (60A, MPPT -> battery)"
  face = grp.entities.add_face([1844.mm,95.mm,1305.mm], [1889.mm,95.mm,1305.mm], [1889.mm,125.mm,1305.mm], [1844.mm,125.mm,1305.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(45.mm)
  mat = model.materials["Master pump switch (Cct C, on EP)"] || model.materials.add("Master pump switch (Cct C, on EP)")
  mat.color = Sketchup::Color.new(133, 133, 136)
  mat.alpha = 0.18
  grp.material = mat

  # Interior E-stop collar (safety yellow)
  grp = ents.add_group
  grp.name = "Interior E-stop collar (safety yellow)"
  ge = grp.entities
  circle = ge.add_circle([2099.mm,0.mm,1065.mm], [0,1,0], 30.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(12.mm)
  mat = model.materials["Interior E-stop collar (safety yellow)"] || model.materials.add("Interior E-stop collar (safety yellow)")
  mat.color = Sketchup::Color.new(208, 191, 127)
  mat.alpha = 0.18
  grp.material = mat

  # Interior E-stop button (red mushroom)
  grp = ents.add_group
  grp.name = "Interior E-stop button (red mushroom)"
  ge = grp.entities
  circle = ge.add_circle([2099.mm,12.mm,1065.mm], [0,1,0], 24.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(26.mm)
  mat = model.materials["Interior E-stop button (red mushroom)"] || model.materials.add("Interior E-stop button (red mushroom)")
  mat.color = Sketchup::Color.new(192, 139, 137)
  mat.alpha = 0.18
  grp.material = mat

  # Battery 1 (12V 100Ah LiFePO4)
  grp = ents.add_group
  grp.name = "Battery 1 (12V 100Ah LiFePO4)"
  face = grp.entities.add_face([1829.mm,0.mm,160.mm], [2089.mm,0.mm,160.mm], [2089.mm,169.mm,160.mm], [1829.mm,169.mm,160.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(211.mm)
  mat = model.materials["Battery 1 (12V 100Ah LiFePO4)"] || model.materials.add("Battery 1 (12V 100Ah LiFePO4)")
  mat.color = Sketchup::Color.new(161, 155, 198)
  mat.alpha = 1.0
  grp.material = mat

  # Battery 2 (optional 2nd pack, ghosted)
  grp = ents.add_group
  grp.name = "Battery 2 (optional 2nd pack, ghosted)"
  face = grp.entities.add_face([1829.mm,0.mm,387.mm], [2089.mm,0.mm,387.mm], [2089.mm,169.mm,387.mm], [1829.mm,169.mm,387.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(211.mm)
  mat = model.materials["Battery 2 (optional 2nd pack, ghosted)"] || model.materials.add("Battery 2 (optional 2nd pack, ghosted)")
  mat.color = Sketchup::Color.new(161, 155, 198)
  mat.alpha = 0.28
  grp.material = mat

  # Battery Contactor (ML-RBS)
  grp = ents.add_group
  grp.name = "Battery Contactor (ML-RBS)"
  face = grp.entities.add_face([1839.mm,15.mm,618.mm], [1959.mm,15.mm,618.mm], [1959.mm,105.mm,618.mm], [1839.mm,105.mm,618.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(100.mm)
  mat = model.materials["Interior E-stop button (red mushroom)"] || model.materials.add("Interior E-stop button (red mushroom)")
  mat.color = Sketchup::Color.new(192, 139, 137)
  mat.alpha = 0.18
  grp.material = mat

  # MRBF Main Fuse (on + post)
  grp = ents.add_group
  grp.name = "MRBF Main Fuse (on + post)"
  face = grp.entities.add_face([1979.mm,20.mm,618.mm], [2019.mm,20.mm,618.mm], [2019.mm,60.mm,618.mm], [1979.mm,60.mm,618.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(38.mm)
  mat = model.materials["Master pump switch (Cct C, on EP)"] || model.materials.add("Master pump switch (Cct C, on EP)")
  mat.color = Sketchup::Color.new(133, 133, 136)
  mat.alpha = 0.18
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF → main disconnect)
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF → main disconnect)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 332.mm)
  circle = ge.add_circle([1999.mm,45.mm,656.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF → main disconnect) elbow
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF → main disconnect) elbow"
  ge = grp.entities
  arc = ge.add_arc([1977.mm,45.mm,988.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 22.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1999.mm,45.mm,988.mm], [0.000000,0.000000,1.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF → main disconnect)
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF → main disconnect)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-85.65000000000009.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1977.mm,45.mm,1010.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF → main disconnect) elbow
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF → main disconnect) elbow"
  ge = grp.entities
  arc = ge.add_arc([1891.35.mm,37.65.mm,1010.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 7.3500000000000005.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1891.35.mm,45.mm,1010.mm], [-1.000000,0.000000,0.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery + cable (2/0 AWG, MRBF → main disconnect)
  grp = ents.add_group
  grp.name = "Battery + cable (2/0 AWG, MRBF → main disconnect)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -7.649999999999999.mm, 0.mm)
  circle = ge.add_circle([1884.mm,37.65.mm,1010.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Main feed (disconnect → busbar +)"] || model.materials.add("Main feed (disconnect → busbar +)")
  mat.color = Sketchup::Color.new(139, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery − cable (2/0 AWG)
  grp = ents.add_group
  grp.name = "Battery − cable (2/0 AWG)"
  ge = grp.entities
  vec = Geom::Vector3d.new(78.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1869.mm,60.mm,598.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 cap"] || model.materials.add("Filter F1 cap")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery − cable (2/0 AWG) elbow
  grp = ents.add_group
  grp.name = "Battery − cable (2/0 AWG) elbow"
  ge = grp.entities
  arc = ge.add_arc([1947.mm,60.mm,620.mm], [0.000000,0.000000,-1.000000], [0.000000,-1.000000,0.000000], 22.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1947.mm,60.mm,598.mm], [1.000000,0.000000,0.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Filter F1 cap"] || model.materials.add("Filter F1 cap")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery − cable (2/0 AWG)
  grp = ents.add_group
  grp.name = "Battery − cable (2/0 AWG)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 658.mm)
  circle = ge.add_circle([1969.mm,60.mm,620.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 cap"] || model.materials.add("Filter F1 cap")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery − cable (2/0 AWG) elbow
  grp = ents.add_group
  grp.name = "Battery − cable (2/0 AWG) elbow"
  ge = grp.entities
  arc = ge.add_arc([1947.mm,60.mm,1278.mm], [1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 22.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1969.mm,60.mm,1278.mm], [0.000000,0.000000,1.000000], 11.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Filter F1 cap"] || model.materials.add("Filter F1 cap")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  # Battery − cable (2/0 AWG)
  grp = ents.add_group
  grp.name = "Battery − cable (2/0 AWG)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-78.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1947.mm,60.mm,1300.mm], vec, 11.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Filter F1 cap"] || model.materials.add("Filter F1 cap")
  mat.color = Sketchup::Color.new(26, 26, 26)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Other pinhole-wall equipment"
  inst.layer = model.layers["Pinhole Equipment"]

  # ═══ Corridor frame (deep box) ═══
  defn = model.definitions.add("Corridor frame (deep box)")
  ents = defn.entities
  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([4654.mm,1046.mm,0.mm], [4704.mm,1046.mm,0.mm], [4704.mm,1096.mm,0.mm], [4654.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([4654.mm,1266.mm,0.mm], [4704.mm,1266.mm,0.mm], [4704.mm,1316.mm,0.mm], [4654.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([5104.mm,1046.mm,0.mm], [5154.mm,1046.mm,0.mm], [5154.mm,1096.mm,0.mm], [5104.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Frame upright
  grp = ents.add_group
  grp.name = "Frame upright"
  face = grp.entities.add_face([5104.mm,1266.mm,0.mm], [5154.mm,1266.mm,0.mm], [5154.mm,1316.mm,0.mm], [5104.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2296.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([4654.mm,1096.mm,0.mm], [4704.mm,1096.mm,0.mm], [4704.mm,1266.mm,0.mm], [4654.mm,1266.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([5104.mm,1096.mm,0.mm], [5154.mm,1096.mm,0.mm], [5154.mm,1266.mm,0.mm], [5104.mm,1266.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.mm,1046.mm,0.mm], [5104.mm,1046.mm,0.mm], [5104.mm,1096.mm,0.mm], [4704.mm,1096.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.mm,1266.mm,0.mm], [5104.mm,1266.mm,0.mm], [5104.mm,1316.mm,0.mm], [4704.mm,1316.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([4654.mm,1096.mm,2246.mm], [4704.mm,1096.mm,2246.mm], [4704.mm,1266.mm,2246.mm], [4654.mm,1266.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Frame rail (Yd)
  grp = ents.add_group
  grp.name = "Frame rail (Yd)"
  face = grp.entities.add_face([5104.mm,1096.mm,2246.mm], [5154.mm,1096.mm,2246.mm], [5154.mm,1266.mm,2246.mm], [5104.mm,1266.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.mm,1046.mm,2246.mm], [5104.mm,1046.mm,2246.mm], [5104.mm,1096.mm,2246.mm], [4704.mm,1096.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Frame rail (X)
  grp = ents.add_group
  grp.name = "Frame rail (X)"
  face = grp.entities.add_face([4704.mm,1266.mm,2246.mm], [5104.mm,1266.mm,2246.mm], [5104.mm,1316.mm,2246.mm], [4704.mm,1316.mm,2246.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(50.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Foot plate
  grp = ents.add_group
  grp.name = "Foot plate"
  face = grp.entities.add_face([4604.mm,996.mm,0.mm], [4754.mm,996.mm,0.mm], [4754.mm,1146.mm,0.mm], [4604.mm,1146.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
  grp.material = mat

  # Foot plate
  grp = ents.add_group
  grp.name = "Foot plate"
  face = grp.entities.add_face([4604.mm,1216.mm,0.mm], [4754.mm,1216.mm,0.mm], [4754.mm,1366.mm,0.mm], [4604.mm,1366.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
  grp.material = mat

  # Foot plate
  grp = ents.add_group
  grp.name = "Foot plate"
  face = grp.entities.add_face([5054.mm,996.mm,0.mm], [5204.mm,996.mm,0.mm], [5204.mm,1146.mm,0.mm], [5054.mm,1146.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
  grp.material = mat

  # Foot plate
  grp = ents.add_group
  grp.name = "Foot plate"
  face = grp.entities.add_face([5054.mm,1216.mm,0.mm], [5204.mm,1216.mm,0.mm], [5204.mm,1366.mm,0.mm], [5054.mm,1366.mm,0.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(12.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
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
  mat.color = Sketchup::Color.new(141, 142, 147)
  mat.alpha = 0.18
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1096.mm,90.mm], [5152.mm,1096.mm,90.mm], [5152.mm,1136.mm,90.mm], [5122.mm,1136.mm,90.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1096.mm,1118.mm], [5152.mm,1096.mm,1118.mm], [5152.mm,1136.mm,1118.mm], [5122.mm,1136.mm,1118.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1096.mm,2146.mm], [5152.mm,1096.mm,2146.mm], [5152.mm,1136.mm,2146.mm], [5122.mm,1136.mm,2146.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1226.mm,90.mm], [5152.mm,1226.mm,90.mm], [5152.mm,1266.mm,90.mm], [5122.mm,1266.mm,90.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1226.mm,1118.mm], [5152.mm,1226.mm,1118.mm], [5152.mm,1266.mm,1118.mm], [5122.mm,1266.mm,1118.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  # Rear-panel bracket
  grp = ents.add_group
  grp.name = "Rear-panel bracket"
  face = grp.entities.add_face([5122.mm,1226.mm,2146.mm], [5152.mm,1226.mm,2146.mm], [5152.mm,1266.mm,2146.mm], [5122.mm,1266.mm,2146.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(60.mm)
  mat = model.materials["RWk Long beam X4329 upper"] || model.materials.add("RWk Long beam X4329 upper")
  mat.color = Sketchup::Color.new(185, 185, 191)
  mat.alpha = 0.18
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Corridor frame (deep box)"
  inst.layer = model.layers["Corridor Frame"]

  # ═══ Corridor rear panel ═══
  defn = model.definitions.add("Corridor rear panel")
  ents = defn.entities
  # Rear panel (18mm marine ply)
  grp = ents.add_group
  grp.name = "Rear panel (18mm marine ply)"
  face = grp.entities.add_face([5104.mm,1096.mm,50.mm], [5122.mm,1096.mm,50.mm], [5122.mm,1266.mm,50.mm], [5104.mm,1266.mm,50.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(2196.mm)
  mat = model.materials["Wall backing (18mm ply)"] || model.materials.add("Wall backing (18mm ply)")
  mat.color = Sketchup::Color.new(178, 167, 154)
  mat.alpha = 0.18
  grp.material = mat

  # Pump-mount ply shirt (25mm)
  grp = ents.add_group
  grp.name = "Pump-mount ply shirt (25mm)"
  face = grp.entities.add_face([5051.5.mm,1096.mm,325.mm], [5076.5.mm,1096.mm,325.mm], [5076.5.mm,1266.mm,325.mm], [5051.5.mm,1266.mm,325.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1866.mm)
  mat = model.materials["Wall backing (18mm ply)"] || model.materials.add("Wall backing (18mm ply)")
  mat.color = Sketchup::Color.new(178, 167, 154)
  mat.alpha = 0.18
  grp.material = mat

  # Shirt-to-panel spacer block
  grp = ents.add_group
  grp.name = "Shirt-to-panel spacer block"
  face = grp.entities.add_face([5076.5.mm,1096.mm,320.mm], [5104.mm,1096.mm,320.mm], [5104.mm,1136.mm,320.mm], [5076.5.mm,1136.mm,320.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Wall backing (18mm ply)"] || model.materials.add("Wall backing (18mm ply)")
  mat.color = Sketchup::Color.new(178, 167, 154)
  mat.alpha = 0.18
  grp.material = mat

  # Shirt-to-panel spacer block
  grp = ents.add_group
  grp.name = "Shirt-to-panel spacer block"
  face = grp.entities.add_face([5076.5.mm,1096.mm,920.mm], [5104.mm,1096.mm,920.mm], [5104.mm,1136.mm,920.mm], [5076.5.mm,1136.mm,920.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Wall backing (18mm ply)"] || model.materials.add("Wall backing (18mm ply)")
  mat.color = Sketchup::Color.new(178, 167, 154)
  mat.alpha = 0.18
  grp.material = mat

  # Shirt-to-panel spacer block
  grp = ents.add_group
  grp.name = "Shirt-to-panel spacer block"
  face = grp.entities.add_face([5076.5.mm,1096.mm,1560.mm], [5104.mm,1096.mm,1560.mm], [5104.mm,1136.mm,1560.mm], [5076.5.mm,1136.mm,1560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Wall backing (18mm ply)"] || model.materials.add("Wall backing (18mm ply)")
  mat.color = Sketchup::Color.new(178, 167, 154)
  mat.alpha = 0.18
  grp.material = mat

  # Shirt-to-panel spacer block
  grp = ents.add_group
  grp.name = "Shirt-to-panel spacer block"
  face = grp.entities.add_face([5076.5.mm,1226.mm,320.mm], [5104.mm,1226.mm,320.mm], [5104.mm,1266.mm,320.mm], [5076.5.mm,1266.mm,320.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Wall backing (18mm ply)"] || model.materials.add("Wall backing (18mm ply)")
  mat.color = Sketchup::Color.new(178, 167, 154)
  mat.alpha = 0.18
  grp.material = mat

  # Shirt-to-panel spacer block
  grp = ents.add_group
  grp.name = "Shirt-to-panel spacer block"
  face = grp.entities.add_face([5076.5.mm,1226.mm,920.mm], [5104.mm,1226.mm,920.mm], [5104.mm,1266.mm,920.mm], [5076.5.mm,1266.mm,920.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Wall backing (18mm ply)"] || model.materials.add("Wall backing (18mm ply)")
  mat.color = Sketchup::Color.new(178, 167, 154)
  mat.alpha = 0.18
  grp.material = mat

  # Shirt-to-panel spacer block
  grp = ents.add_group
  grp.name = "Shirt-to-panel spacer block"
  face = grp.entities.add_face([5076.5.mm,1226.mm,1560.mm], [5104.mm,1226.mm,1560.mm], [5104.mm,1266.mm,1560.mm], [5076.5.mm,1266.mm,1560.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(120.mm)
  mat = model.materials["Wall backing (18mm ply)"] || model.materials.add("Wall backing (18mm ply)")
  mat.color = Sketchup::Color.new(178, 167, 154)
  mat.alpha = 0.18
  grp.material = mat

  # Drain-riser backing spine (18mm ply)
  grp = ents.add_group
  grp.name = "Drain-riser backing spine (18mm ply)"
  face = grp.entities.add_face([5104.mm,1206.mm,280.mm], [5560.mm,1206.mm,280.mm], [5560.mm,1224.mm,280.mm], [5104.mm,1224.mm,280.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1966.mm)
  mat = model.materials["Wall backing (18mm ply)"] || model.materials.add("Wall backing (18mm ply)")
  mat.color = Sketchup::Color.new(178, 167, 154)
  mat.alpha = 0.18
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Corridor rear panel"
  inst.layer = model.layers["Corridor Panel"]

  # ═══ Corridor equipment ═══
  defn = model.definitions.add("Corridor equipment")
  ents = defn.entities
  # Pump P-01 (Blue supply) body
  grp = ents.add_group
  grp.name = "Pump P-01 (Blue supply) body"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1181.mm,615.mm], [0,0,1], 50.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(180.mm)
  mat = model.materials["Pump P-04 (Tray drain) body"] || model.materials.add("Pump P-04 (Tray drain) body")
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
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
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
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
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
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
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
  mat = model.materials["Pump P-04 (Tray drain) body"] || model.materials.add("Pump P-04 (Tray drain) body")
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
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
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
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
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
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
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
  mat = model.materials["Pump P-04 (Tray drain) body"] || model.materials.add("Pump P-04 (Tray drain) body")
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
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
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
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
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
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
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
  mat = model.materials["ACC-02 Accumulator"] || model.materials.add("ACC-02 Accumulator")
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
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
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
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
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
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-02 (Brown recycle) body
  grp = ents.add_group
  grp.name = "Pump P-02 (Brown recycle) body"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1181.mm,940.mm], [0,0,1], 50.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(180.mm)
  mat = model.materials["Pump P-04 (Tray drain) body"] || model.materials.add("Pump P-04 (Tray drain) body")
  mat.color = Sketchup::Color.new(69, 69, 82)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-02 (Brown recycle) head
  grp = ents.add_group
  grp.name = "Pump P-02 (Brown recycle) head"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1181.mm,1120.mm], [0,0,1], 53.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(30.mm)
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-02 (Brown recycle) in port
  grp = ents.add_group
  grp.name = "Pump P-02 (Brown recycle) in port"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1101.mm,1102.mm], [0,1,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(30.mm)
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Pump P-02 (Brown recycle) out port
  grp = ents.add_group
  grp.name = "Pump P-02 (Brown recycle) out port"
  ge = grp.entities
  circle = ge.add_circle([4984.mm,1231.mm,1102.mm], [0,1,0], 10.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(30.mm)
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Corridor equipment"
  inst.layer = model.layers["Corridor Equipment"]

  # ═══ Corridor plumbing ═══
  defn = model.definitions.add("Corridor plumbing")
  ents = defn.entities
  # IBC-4 waste merge tee run
  grp = ents.add_group
  grp.name = "IBC-4 waste merge tee run"
  ge = grp.entities
  circle = ge.add_circle([5374.mm,1195.mm,1230.mm], [1,0,0], 15.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(60.mm)
  mat = model.materials["IBC-4 waste merge tee run"] || model.materials.add("IBC-4 waste merge tee run")
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
  mat = model.materials["IBC-4 waste merge tee run"] || model.materials.add("IBC-4 waste merge tee run")
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
  mat = model.materials["IBC-4 waste merge tee run"] || model.materials.add("IBC-4 waste merge tee run")
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
  mat = model.materials["IBC-4 waste merge tee run"] || model.materials.add("IBC-4 waste merge tee run")
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
  mat = model.materials["IBC-4 waste merge tee run"] || model.materials.add("IBC-4 waste merge tee run")
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
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
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
  mat = model.materials["3W-BV-05 (spray selector) handle stem"] || model.materials.add("3W-BV-05 (spray selector) handle stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # BV-01 (P-01 suction) handle
  grp = ents.add_group
  grp.name = "BV-01 (P-01 suction) handle"
  face = grp.entities.add_face([4819.5.mm,1106.mm,976.mm], [4828.5.mm,1106.mm,976.mm], [4828.5.mm,1120.mm,976.mm], [4819.5.mm,1120.mm,976.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["3W-BV-05 (spray selector) handle stem"] || model.materials.add("3W-BV-05 (spray selector) handle stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 -> ACC-01 (in)
  grp = ents.add_group
  grp.name = "P-01 -> ACC-01 (in)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 19.63499999999999.mm, 0.mm)
  circle = ge.add_circle([4984.mm,1261.mm,777.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 -> ACC-01 (in) elbow
  grp = ents.add_group
  grp.name = "P-01 -> ACC-01 (in) elbow"
  ge = grp.entities
  arc = ge.add_arc([4984.mm,1280.635.mm,758.135.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 18.865000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4984.mm,1280.635.mm,777.mm], [0.000000,1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 -> ACC-01 (in)
  grp = ents.add_group
  grp.name = "P-01 -> ACC-01 (in)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -362.885.mm)
  circle = ge.add_circle([4984.mm,1299.5.mm,758.135.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 -> ACC-01 (in) elbow
  grp = ents.add_group
  grp.name = "P-01 -> ACC-01 (in) elbow"
  ge = grp.entities
  arc = ge.add_arc([4984.mm,1287.25.mm,395.25.mm], [0.000000,1.000000,0.000000], [-1.000000,-0.000000,-0.000000], 12.250000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4984.mm,1299.5.mm,395.25.mm], [0.000000,0.000000,-1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  # P-01 -> ACC-01 (in)
  grp = ents.add_group
  grp.name = "P-01 -> ACC-01 (in)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -12.75.mm, 0.mm)
  circle = ge.add_circle([4984.mm,1287.25.mm,383.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
  mat.color = Sketchup::Color.new(41, 121, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Corridor plumbing"
  inst.layer = model.layers["Corridor Plumbing"]

  # ═══ Corridor drains + X-ports ═══
  defn = model.definitions.add("Corridor drains + X-ports")
  ents = defn.entities
  # X1 fill camlock (end wall)
  grp = ents.add_group
  grp.name = "X1 fill camlock (end wall)"
  ge = grp.entities
  circle = ge.add_circle([5833.mm,1195.5.mm,2250.mm], [1,0,0], 26.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.x < 0
  cface.pushpull(60.mm)
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["IBC-4 waste merge tee run"] || model.materials.add("IBC-4 waste merge tee run")
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
  mat = model.materials["IBC-4 waste merge tee run"] || model.materials.add("IBC-4 waste merge tee run")
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
  mat = model.materials["IBC-4 waste merge tee run"] || model.materials.add("IBC-4 waste merge tee run")
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
  mat = model.materials["IBC-4 waste merge tee run"] || model.materials.add("IBC-4 waste merge tee run")
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
  mat = model.materials["IBC-4 waste merge tee run"] || model.materials.add("IBC-4 waste merge tee run")
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
  mat = model.materials["IBC-4 waste merge tee run"] || model.materials.add("IBC-4 waste merge tee run")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Blue trunk: corridor -> ribbon -> outside-rim strip"] || model.materials.add("Blue trunk: corridor -> ribbon -> outside-rim strip")
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
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
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
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
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
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
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
  mat = model.materials["IBC-4 waste merge tee run"] || model.materials.add("IBC-4 waste merge tee run")
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
  mat = model.materials["IBC-4 waste merge tee run"] || model.materials.add("IBC-4 waste merge tee run")
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
  mat = model.materials["IBC-4 waste merge tee run"] || model.materials.add("IBC-4 waste merge tee run")
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
  mat = model.materials["IBC-4 waste merge tee run"] || model.materials.add("IBC-4 waste merge tee run")
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
  mat = model.materials["IBC-4 waste merge tee run"] || model.materials.add("IBC-4 waste merge tee run")
  mat.color = Sketchup::Color.new(154, 160, 166)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 tap -> P-02 suction
  grp = ents.add_group
  grp.name = "IBC-3 tap -> P-02 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(-18.359999999999673.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4861.mm,1101.mm,308.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 tap -> P-02 suction elbow
  grp = ents.add_group
  grp.name = "IBC-3 tap -> P-02 suction elbow"
  ge = grp.entities
  arc = ge.add_arc([4842.64.mm,1083.36.mm,308.mm], [0.000000,1.000000,0.000000], [0.000000,0.000000,1.000000], 17.640000000000004.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4842.64.mm,1101.mm,308.mm], [-1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 tap -> P-02 suction
  grp = ents.add_group
  grp.name = "IBC-3 tap -> P-02 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -11.40359999999987.mm, 0.mm)
  circle = ge.add_circle([4825.mm,1083.36.mm,308.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 tap -> P-02 suction elbow
  grp = ents.add_group
  grp.name = "IBC-3 tap -> P-02 suction elbow"
  ge = grp.entities
  arc = ge.add_arc([4825.mm,1071.9564.mm,318.9564.mm], [0.000000,0.000000,-1.000000], [-1.000000,0.000000,0.000000], 10.956399999999952.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4825.mm,1071.9564.mm,308.mm], [0.000000,-1.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 tap -> P-02 suction
  grp = ents.add_group
  grp.name = "IBC-3 tap -> P-02 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 762.0436.mm)
  circle = ge.add_circle([4825.mm,1061.mm,318.9564.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 tap -> P-02 suction elbow
  grp = ents.add_group
  grp.name = "IBC-3 tap -> P-02 suction elbow"
  ge = grp.entities
  arc = ge.add_arc([4846.mm,1061.mm,1081.mm], [-1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 21.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4825.mm,1061.mm,1081.mm], [0.000000,0.000000,1.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 tap -> P-02 suction
  grp = ents.add_group
  grp.name = "IBC-3 tap -> P-02 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(118.39999999999964.mm, 0.mm, 0.mm)
  circle = ge.add_circle([4846.mm,1061.mm,1102.mm], vec, 10.5.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 tap -> P-02 suction elbow
  grp = ents.add_group
  grp.name = "IBC-3 tap -> P-02 suction elbow"
  ge = grp.entities
  arc = ge.add_arc([4964.4.mm,1080.6.mm,1102.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 19.600000000000005.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([4964.4.mm,1061.mm,1102.mm], [1.000000,0.000000,0.000000], 10.5.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["IBC-3 (Brown) tap -> P-02 inlet"] || model.materials.add("IBC-3 (Brown) tap -> P-02 inlet")
  mat.color = Sketchup::Color.new(107, 74, 46)
  mat.alpha = 1.0
  grp.material = mat

  # IBC-3 tap -> P-02 suction
  grp = ents.add_group
  grp.name = "IBC-3 tap -> P-02 suction"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 20.40000000000009.mm, 0.mm)
  circle = ge.add_circle([4984.mm,1080.6.mm,1102.mm], vec, 10.5.mm, 16)
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
  circle = ge.add_circle([4825.mm,1061.mm,928.mm], [0,0,1], 18.5.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.z < 0
  cface.pushpull(44.mm)
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
  mat.color = Sketchup::Color.new(128, 128, 138)
  mat.alpha = 1.0
  grp.material = mat

  # BV-03 (P-02 suction) handle stem
  grp = ents.add_group
  grp.name = "BV-03 (P-02 suction) handle stem"
  ge = grp.entities
  circle = ge.add_circle([4825.mm,1079.5.mm,950.mm], [0,1,0], 6.mm, 24)
  cface = ge.add_face(circle)
  cface.reverse! if cface.normal.y < 0
  cface.pushpull(28.mm)
  mat = model.materials["3W-BV-05 (spray selector) handle stem"] || model.materials.add("3W-BV-05 (spray selector) handle stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # BV-03 (P-02 suction) handle
  grp = ents.add_group
  grp.name = "BV-03 (P-02 suction) handle"
  face = grp.entities.add_face([4818.mm,1107.5.mm,926.mm], [4832.mm,1107.5.mm,926.mm], [4832.mm,1116.5.mm,926.mm], [4818.mm,1116.5.mm,926.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["3W-BV-05 (spray selector) handle stem"] || model.materials.add("3W-BV-05 (spray selector) handle stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
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
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
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
  mat = model.materials["3W-BV-05 (spray selector) handle stem"] || model.materials.add("3W-BV-05 (spray selector) handle stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # BV-02 (P-05 suction) handle
  grp = ents.add_group
  grp.name = "BV-02 (P-05 suction) handle"
  face = grp.entities.add_face([4842.5.mm,1070.5.mm,1393.mm], [4851.5.mm,1070.5.mm,1393.mm], [4851.5.mm,1084.5.mm,1393.mm], [4842.5.mm,1084.5.mm,1393.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["3W-BV-05 (spray selector) handle stem"] || model.materials.add("3W-BV-05 (spray selector) handle stem")
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
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
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
  mat = model.materials["Axle Pin 10mm L"] || model.materials.add("Axle Pin 10mm L")
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
  mat = model.materials["3W-BV-05 (spray selector) handle stem"] || model.materials.add("3W-BV-05 (spray selector) handle stem")
  mat.color = Sketchup::Color.new(192, 32, 42)
  mat.alpha = 1.0
  grp.material = mat

  # BV-06 (P-03 suction) handle
  grp = ents.add_group
  grp.name = "BV-06 (P-03 suction) handle"
  face = grp.entities.add_face([4842.5.mm,1070.5.mm,1768.mm], [4851.5.mm,1070.5.mm,1768.mm], [4851.5.mm,1084.5.mm,1768.mm], [4842.5.mm,1084.5.mm,1768.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(48.mm)
  mat = model.materials["3W-BV-05 (spray selector) handle stem"] || model.materials.add("3W-BV-05 (spray selector) handle stem")
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
  inst.name = "Corridor drains + X-ports"
  inst.layer = model.layers["Corridor Drains"]

  # ═══ Circuit-C power + cabling (both panels) ═══
  defn = model.definitions.add("Circuit-C power + cabling (both panels)")
  ents = defn.entities
  # Cct C feed (EP master sw -> corridor dist block)
  grp = ents.add_group
  grp.name = "Cct C feed (EP master sw -> corridor dist block)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, 1233.2600000000002.mm)
  circle = ge.add_circle([1959.mm,46.mm,1129.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct C feed (EP master sw -> corridor dist block)"] || model.materials.add("Cct C feed (EP master sw -> corridor dist block)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C feed (EP master sw -> corridor dist block) elbow
  grp = ents.add_group
  grp.name = "Cct C feed (EP master sw -> corridor dist block) elbow"
  ge = grp.entities
  arc = ge.add_arc([1959.mm,33.26.mm,2362.26.mm], [0.000000,1.000000,0.000000], [1.000000,0.000000,-0.000000], 12.740000000000002.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1959.mm,46.mm,2362.26.mm], [0.000000,0.000000,1.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Cct C feed (EP master sw -> corridor dist block)"] || model.materials.add("Cct C feed (EP master sw -> corridor dist block)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C feed (EP master sw -> corridor dist block)
  grp = ents.add_group
  grp.name = "Cct C feed (EP master sw -> corridor dist block)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, -6.762599999999999.mm, 0.mm)
  circle = ge.add_circle([1959.mm,33.26.mm,2375.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct C feed (EP master sw -> corridor dist block)"] || model.materials.add("Cct C feed (EP master sw -> corridor dist block)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C feed (EP master sw -> corridor dist block) elbow
  grp = ents.add_group
  grp.name = "Cct C feed (EP master sw -> corridor dist block) elbow"
  ge = grp.entities
  arc = ge.add_arc([1965.4974.mm,26.4974.mm,2375.mm], [-1.000000,0.000000,0.000000], [-0.000000,0.000000,1.000000], 6.4974.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([1959.mm,26.4974.mm,2375.mm], [0.000000,-1.000000,0.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Cct C feed (EP master sw -> corridor dist block)"] || model.materials.add("Cct C feed (EP master sw -> corridor dist block)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C feed (EP master sw -> corridor dist block)
  grp = ents.add_group
  grp.name = "Cct C feed (EP master sw -> corridor dist block)"
  ge = grp.entities
  vec = Geom::Vector3d.new(3166.5026.mm, 0.mm, 0.mm)
  circle = ge.add_circle([1965.4974.mm,20.mm,2375.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct C feed (EP master sw -> corridor dist block)"] || model.materials.add("Cct C feed (EP master sw -> corridor dist block)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C feed (EP master sw -> corridor dist block) elbow
  grp = ents.add_group
  grp.name = "Cct C feed (EP master sw -> corridor dist block) elbow"
  ge = grp.entities
  arc = ge.add_arc([5132.mm,34.mm,2375.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 14.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5132.mm,20.mm,2375.mm], [1.000000,0.000000,0.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Cct C feed (EP master sw -> corridor dist block)"] || model.materials.add("Cct C feed (EP master sw -> corridor dist block)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C feed (EP master sw -> corridor dist block)
  grp = ents.add_group
  grp.name = "Cct C feed (EP master sw -> corridor dist block)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 1133.mm, 0.mm)
  circle = ge.add_circle([5146.mm,34.mm,2375.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct C feed (EP master sw -> corridor dist block)"] || model.materials.add("Cct C feed (EP master sw -> corridor dist block)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C feed (EP master sw -> corridor dist block) elbow
  grp = ents.add_group
  grp.name = "Cct C feed (EP master sw -> corridor dist block) elbow"
  ge = grp.entities
  arc = ge.add_arc([5146.mm,1167.mm,2361.mm], [0.000000,0.000000,1.000000], [-1.000000,0.000000,0.000000], 14.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5146.mm,1167.mm,2375.mm], [0.000000,1.000000,0.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Cct C feed (EP master sw -> corridor dist block)"] || model.materials.add("Cct C feed (EP master sw -> corridor dist block)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C feed (EP master sw -> corridor dist block)
  grp = ents.add_group
  grp.name = "Cct C feed (EP master sw -> corridor dist block)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1045.5.mm)
  circle = ge.add_circle([5146.mm,1181.mm,2361.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct C feed (EP master sw -> corridor dist block)"] || model.materials.add("Cct C feed (EP master sw -> corridor dist block)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-04 (filter skid)
  grp = ents.add_group
  grp.name = "Cct C branch P-04 (filter skid)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1161.mm)
  circle = ge.add_circle([2800.mm,20.mm,2375.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct C feed (EP master sw -> corridor dist block)"] || model.materials.add("Cct C feed (EP master sw -> corridor dist block)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-04 (filter skid) elbow
  grp = ents.add_group
  grp.name = "Cct C branch P-04 (filter skid) elbow"
  ge = grp.entities
  arc = ge.add_arc([2814.mm,20.mm,1214.mm], [-1.000000,0.000000,0.000000], [0.000000,-1.000000,0.000000], 14.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([2800.mm,20.mm,1214.mm], [0.000000,0.000000,-1.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Cct C feed (EP master sw -> corridor dist block)"] || model.materials.add("Cct C feed (EP master sw -> corridor dist block)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-04 (filter skid)
  grp = ents.add_group
  grp.name = "Cct C branch P-04 (filter skid)"
  ge = grp.entities
  vec = Geom::Vector3d.new(502.mm, 0.mm, 0.mm)
  circle = ge.add_circle([2814.mm,20.mm,1200.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct C feed (EP master sw -> corridor dist block)"] || model.materials.add("Cct C feed (EP master sw -> corridor dist block)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-04 (filter skid) elbow
  grp = ents.add_group
  grp.name = "Cct C branch P-04 (filter skid) elbow"
  ge = grp.entities
  arc = ge.add_arc([3316.mm,34.mm,1200.mm], [0.000000,-1.000000,0.000000], [0.000000,0.000000,1.000000], 14.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([3316.mm,20.mm,1200.mm], [1.000000,0.000000,0.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Cct C feed (EP master sw -> corridor dist block)"] || model.materials.add("Cct C feed (EP master sw -> corridor dist block)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-04 (filter skid)
  grp = ents.add_group
  grp.name = "Cct C branch P-04 (filter skid)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 56.mm, 0.mm)
  circle = ge.add_circle([3330.mm,34.mm,1200.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct C feed (EP master sw -> corridor dist block)"] || model.materials.add("Cct C feed (EP master sw -> corridor dist block)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # 12V distribution block (Cct C, rear)
  grp = ents.add_group
  grp.name = "12V distribution block (Cct C, rear)"
  face = grp.entities.add_face([5122.mm,1151.mm,1222.5.mm], [5170.mm,1151.mm,1222.5.mm], [5170.mm,1211.mm,1222.5.mm], [5122.mm,1211.mm,1222.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(90.mm)
  mat = model.materials["Wheel L"] || model.materials.add("Wheel L")
  mat.color = Sketchup::Color.new(51, 52, 58)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C bus + P-03/P-01 elbow taps (rear)
  grp = ents.add_group
  grp.name = "Cct C bus + P-03/P-01 elbow taps (rear)"
  ge = grp.entities
  vec = Geom::Vector3d.new(108.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5024.mm,1181.mm,1830.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct C feed (EP master sw -> corridor dist block)"] || model.materials.add("Cct C feed (EP master sw -> corridor dist block)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C bus + P-03/P-01 elbow taps (rear) elbow
  grp = ents.add_group
  grp.name = "Cct C bus + P-03/P-01 elbow taps (rear) elbow"
  ge = grp.entities
  arc = ge.add_arc([5132.mm,1181.mm,1816.mm], [0.000000,0.000000,1.000000], [-0.000000,1.000000,0.000000], 14.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5132.mm,1181.mm,1830.mm], [1.000000,0.000000,0.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Cct C feed (EP master sw -> corridor dist block)"] || model.materials.add("Cct C feed (EP master sw -> corridor dist block)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C bus + P-03/P-01 elbow taps (rear)
  grp = ents.add_group
  grp.name = "Cct C bus + P-03/P-01 elbow taps (rear)"
  ge = grp.entities
  vec = Geom::Vector3d.new(0.mm, 0.mm, -1097.mm)
  circle = ge.add_circle([5146.mm,1181.mm,1816.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct C feed (EP master sw -> corridor dist block)"] || model.materials.add("Cct C feed (EP master sw -> corridor dist block)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C bus + P-03/P-01 elbow taps (rear) elbow
  grp = ents.add_group
  grp.name = "Cct C bus + P-03/P-01 elbow taps (rear) elbow"
  ge = grp.entities
  arc = ge.add_arc([5132.mm,1181.mm,719.mm], [1.000000,0.000000,0.000000], [0.000000,1.000000,0.000000], 14.mm, 0.0, 1.570796, 8)
  circle = ge.add_circle([5146.mm,1181.mm,719.mm], [0.000000,0.000000,-1.000000], 7.mm, 16)
  f = ge.add_face(circle)
  f.followme(arc)
  arc.each { |e| e.erase! if e && e.valid? && e.faces.empty? }
  mat = model.materials["Cct C feed (EP master sw -> corridor dist block)"] || model.materials.add("Cct C feed (EP master sw -> corridor dist block)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C bus + P-03/P-01 elbow taps (rear)
  grp = ents.add_group
  grp.name = "Cct C bus + P-03/P-01 elbow taps (rear)"
  ge = grp.entities
  vec = Geom::Vector3d.new(-108.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5132.mm,1181.mm,705.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct C feed (EP master sw -> corridor dist block)"] || model.materials.add("Cct C feed (EP master sw -> corridor dist block)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-02
  grp = ents.add_group
  grp.name = "Cct C branch P-02"
  ge = grp.entities
  vec = Geom::Vector3d.new(-122.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5146.mm,1181.mm,1030.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct C feed (EP master sw -> corridor dist block)"] || model.materials.add("Cct C feed (EP master sw -> corridor dist block)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  # Cct C branch P-05
  grp = ents.add_group
  grp.name = "Cct C branch P-05"
  ge = grp.entities
  vec = Geom::Vector3d.new(-122.mm, 0.mm, 0.mm)
  circle = ge.add_circle([5146.mm,1181.mm,1430.mm], vec, 7.mm, 16)
  pf = ge.add_face(circle)
  pf.reverse! if pf.normal.dot(vec) < 0
  pf.pushpull(vec.length)
  mat = model.materials["Cct C feed (EP master sw -> corridor dist block)"] || model.materials.add("Cct C feed (EP master sw -> corridor dist block)")
  mat.color = Sketchup::Color.new(142, 68, 173)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Circuit-C power + cabling (both panels)"
  inst.layer = model.layers["Power"]

  # ═══ Ribbon support cross-beams ═══
  defn = model.definitions.add("Ribbon support cross-beams")
  ents = defn.entities
  # Ribbon support cross-beam (welded 40x10)
  grp = ents.add_group
  grp.name = "Ribbon support cross-beam (welded 40x10)"
  face = grp.entities.add_face([4329.mm,197.mm,86.5.mm], [4629.mm,197.mm,86.5.mm], [4629.mm,203.mm,86.5.mm], [4329.mm,203.mm,86.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Ribbon support cross-beam (welded 40x10)
  grp = ents.add_group
  grp.name = "Ribbon support cross-beam (welded 40x10)"
  face = grp.entities.add_face([4329.mm,447.mm,86.5.mm], [4629.mm,447.mm,86.5.mm], [4629.mm,453.mm,86.5.mm], [4329.mm,453.mm,86.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Ribbon support cross-beam (welded 40x10)
  grp = ents.add_group
  grp.name = "Ribbon support cross-beam (welded 40x10)"
  face = grp.entities.add_face([4329.mm,697.mm,86.5.mm], [4629.mm,697.mm,86.5.mm], [4629.mm,703.mm,86.5.mm], [4329.mm,703.mm,86.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  # Ribbon support cross-beam (welded 40x10)
  grp = ents.add_group
  grp.name = "Ribbon support cross-beam (welded 40x10)"
  face = grp.entities.add_face([4329.mm,947.mm,86.5.mm], [4629.mm,947.mm,86.5.mm], [4629.mm,953.mm,86.5.mm], [4329.mm,953.mm,86.5.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(10.mm)
  mat = model.materials["Pole Mount Flange"] || model.materials.add("Pole Mount Flange")
  mat.color = Sketchup::Color.new(176, 176, 184)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Ribbon support cross-beams"
  inst.layer = model.layers["Ribbon Supports"]

  # ═══ Corridor panel (solid) ═══
  defn = model.definitions.add("Corridor panel (solid)")
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
  inst.name = "Corridor panel (solid)"
  inst.layer = model.layers["Corridor Panel Solid"]

  # ═══ Wall backing (solid) ═══
  defn = model.definitions.add("Wall backing (solid)")
  ents = defn.entities
  # Wall backing (18mm ply)
  grp = ents.add_group
  grp.name = "Wall backing (18mm ply)"
  face = grp.entities.add_face([2780.mm,0.mm,920.mm], [4575.mm,0.mm,920.mm], [4575.mm,18.mm,920.mm], [2780.mm,18.mm,920.mm])
  face.reverse! if face.normal.z < 0
  face.pushpull(1440.mm)
  mat = model.materials["Rear panel (18mm marine ply)"] || model.materials.add("Rear panel (18mm marine ply)")
  mat.color = Sketchup::Color.new(156, 123, 77)
  mat.alpha = 1.0
  grp.material = mat

  inst = entities.add_instance(defn, Geom::Transformation.new)
  inst.name = "Wall backing (solid)"
  inst.layer = model.layers["Backing Solid"]

# remove the FAR walkway deck AND its cantilever brackets (not wanted in this view)
model.definitions.each { |d| d.entities.grep(Sketchup::Group).each { |g| g.erase! if g.valid? && g.name =~ /^Walkway Far/ } }
# in-model callout labels on the 'Labels' tag (shown only in the Labeled scene)
anc = Geom::Point3d.new(3857.mm,104.mm,1007.mm)
txt = entities.add_text("ACC-02
(recycle spray)", anc, Geom::Vector3d.new(0.mm,470.mm,330.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(3300.mm,104.mm,2043.mm)
txt = entities.add_text("F1 (50um)", anc, Geom::Vector3d.new(0.mm,560.mm,215.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(3638.mm,104.mm,2043.mm)
txt = entities.add_text("F2 (KDF-55)", anc, Geom::Vector3d.new(0.mm,560.mm,215.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(3976.mm,104.mm,2043.mm)
txt = entities.add_text("F3 (GAC)", anc, Geom::Vector3d.new(0.mm,560.mm,215.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4250.mm,110.mm,1610.mm)
txt = entities.add_text("SV-01
(sample)", anc, Geom::Vector3d.new(-430.mm,430.mm,250.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4800.mm,1241.mm,235.mm)
txt = entities.add_text("DV-01
(3-way)", anc, Geom::Vector3d.new(-700.mm,0.mm,650.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(3300.mm,104.mm,1240.mm)
txt = entities.add_text("P-04
(tray drain)", anc, Geom::Vector3d.new(0.mm,470.mm,-180.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(3638.mm,104.mm,1312.mm)
txt = entities.add_text("SV-02
(sample)", anc, Geom::Vector3d.new(0.mm,470.mm,-120.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(3976.mm,104.mm,1312.mm)
txt = entities.add_text("DV-02 (3-way)", anc, Geom::Vector3d.new(0.mm,470.mm,-180.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4984.mm,1181.mm,705.mm)
txt = entities.add_text("P-01 (Blue supply)", anc, Geom::Vector3d.new(-700.mm,0.mm,-150.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4984.mm,1181.mm,1030.mm)
txt = entities.add_text("P-02 (recycle pump)", anc, Geom::Vector3d.new(-800.mm,0.mm,-150.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4984.mm,1181.mm,1430.mm)
txt = entities.add_text("P-05 (Brown drain)", anc, Geom::Vector3d.new(-900.mm,0.mm,150.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4984.mm,1181.mm,1830.mm)
txt = entities.add_text("P-03 (Waste drain)", anc, Geom::Vector3d.new(-1000.mm,0.mm,150.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4984.mm,1181.mm,442.mm)
txt = entities.add_text("ACC-01
(accumulator)", anc, Geom::Vector3d.new(-700.mm,0.mm,250.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(5146.mm,1181.mm,1267.5.mm)
txt = entities.add_text("12V DIST BLOCK
(Cct C)", anc, Geom::Vector3d.new(300.mm,0.mm,400.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4760.mm,1113.mm,1000.mm)
txt = entities.add_text("BV-01", anc, Geom::Vector3d.new(-600.mm,0.mm,250.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4898.mm,1077.5.mm,1417.mm)
txt = entities.add_text("BV-02", anc, Geom::Vector3d.new(350.mm,0.mm,250.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4825.mm,1061.mm,950.mm)
txt = entities.add_text("BV-03", anc, Geom::Vector3d.new(-600.mm,0.mm,250.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(4984.mm,1101.mm,1861.mm)
txt = entities.add_text("BV-06", anc, Geom::Vector3d.new(-1000.mm,0.mm,150.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(5693.mm,1195.5.mm,2250.mm)
txt = entities.add_text("CV-1
(X1 fill)", anc, Geom::Vector3d.new(-600.mm,300.mm,0.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(5863.mm,1195.5.mm,2250.mm)
txt = entities.add_text("X1
(fresh fill)", anc, Geom::Vector3d.new(-550.mm,250.mm,0.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(5863.mm,1109.mm,1700.mm)
txt = entities.add_text("X3
(brown drain out)", anc, Geom::Vector3d.new(-550.mm,0.mm,250.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(5863.mm,1235.mm,1620.mm)
txt = entities.add_text("X4
(waste drain out)", anc, Geom::Vector3d.new(-550.mm,0.mm,-250.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(2249.mm,69.mm,700.mm)
txt = entities.add_text("3W-BV-05
(spray selector)", anc, Geom::Vector3d.new(0.mm,380.mm,250.mm))
txt.layer = model.layers["Labels"] rescue nil
anc = Geom::Point3d.new(1130.mm,112.mm,1150.mm)
txt = entities.add_text("TAP-01
(chem tap)", anc, Geom::Vector3d.new(0.mm,450.mm,300.mm))
txt.layer = model.layers["Labels Context"] rescue nil
anc = Geom::Point3d.new(1130.mm,12.mm,1010.mm)
txt = entities.add_text("BV-04", anc, Geom::Vector3d.new(-450.mm,0.mm,250.mm))
txt.layer = model.layers["Labels Context"] rescue nil
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Pinhole Assembly" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.min.y, bb.center.z)
  txt = entities.add_text("PINHOLE
(optical ref)", anc, Geom::Vector3d.new(0.mm,700.mm,350.mm))
  txt.layer = model.layers["Labels Context"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "Other pinhole-wall equipment" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.min.y, bb.center.z)
  txt = entities.add_text("ELECTRICAL
(panel/inverter/batteries)", anc, Geom::Vector3d.new(0.mm,850.mm,500.mm))
  txt.layer = model.layers["Labels Context"] rescue nil
end
inst = entities.grep(Sketchup::ComponentInstance).find { |i| i.name == "IBC Tanks (full)" }
if inst
  bb = inst.bounds
  anc = Geom::Point3d.new(bb.center.x, bb.min.y, bb.center.z)
  txt = entities.add_text("IBCs
(space NOT available)", anc, Geom::Vector3d.new(-300.mm,900.mm,300.mm))
  txt.layer = model.layers["Labels Context"] rescue nil
end
v = model.active_view
v.camera = Sketchup::Camera.new(Geom::Point3d.new(800.mm, 6000.mm, 2300.mm), Geom::Point3d.new(2950.mm, 200.mm, 1100.mm), Geom::Vector3d.new(0,0,1), false, 52)
# Context/backdrop is built muted AT SOURCE (ov.muted() wraps the MUTE_TAGS builders above), so no
# post-build re-coloring pass is needed.  Keep ModelTransparency OFF so the per-material alpha renders
# as translucency (not a global X-ray that would leak across scenes).
model.rendering_options["ModelTransparency"] = false
def scene(model, name, on)
  model.layers.each { |l| l.visible = (l.name == "Layer0" || l == model.layers[0] || on.include?(l.name)) }
  pg = model.pages.add(name, 4095)
  pg.use_hidden_layers = true rescue nil
  pg
end
scene(model, "Overview", ["Context","Walkway","Film Plane","Processing Tray","Spray Bar","IBC","IBC Frame","Pinhole","Backing","Supply","Kit","Scale","Pinhole Equipment","Corridor Frame","Corridor Panel","Corridor Equipment","Corridor Plumbing","Corridor Drains","Power"])
scene(model, "Plumbing", ["Kit","Supply","Corridor Equipment","Corridor Plumbing","Corridor Drains","Power"])
scene(model, "Plumbing (labeled)", ["Kit","Supply","Corridor Equipment","Corridor Plumbing","Corridor Drains","Power","Labels","Corridor Panel Solid","Backing Solid"])
scene(model, "Plumbing + IBC", ["Kit","Supply","Corridor Equipment","Corridor Plumbing","Corridor Drains","Power","IBC","IBC Frame","Corridor Frame","Corridor Panel","Walkway"])
scene(model, "Labeled", ["Context","Walkway","Film Plane","Processing Tray","Spray Bar","IBC","IBC Frame","Pinhole","Backing","Supply","Kit","Scale","Pinhole Equipment","Corridor Frame","Corridor Panel","Corridor Equipment","Corridor Plumbing","Corridor Drains","Power","Labels","Labels Context"])
model.layers.each { |l| l.visible = true }
model.commit_operation
{ ok: true }.to_json
